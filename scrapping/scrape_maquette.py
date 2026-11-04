#!/usr/bin/env python3
"""
Scraper du catalogue des formations USMB (Ametys / ODF) -> JSON.

Cible par defaut : Diplome ingenieur Informatique, Donnees, Usages (Polytech Annecy).

Structure produite :
  formation -> parcours[] -> semestres[] -> ue[] -> modules[] -> sous_modules[]
avec, pour chaque noeud : code, titre, url, ECTS, heures CM/TD/TP (+ total contact),
contraintes (facultatif / "au choix : 1 parmi N") et le detail de la page du cours
(presentation, objectifs, prerequis, plan du cours, competences, ... + toutes les
sections trouvees dans `sections`).

Dependances : pip install requests beautifulsoup4
Usage       : python scrape_idu.py -o idu.json
              python scrape_idu.py -o idu.json --parcours alternance --workers 4
              python scrape_idu.py --no-details -o maquette_seule.json
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import logging
import re
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

DEFAULT_URL = (
    "https://formations.univ-smb.fr/fr/catalogue/cycle-preparatoire-et-diplome-d-ingenieur-FI/"
    "diplome-ingenieur-informatique-donnees-usages-M1JEXJEN.html"
)

log = logging.getLogger("scrape_idu")

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCKS = {"p", "div", "li", "br", "tr", "section", "article", "ul", "ol", "table", "dt", "dd"} | HEADINGS


# --------------------------------------------------------------------------- #
# Reseau : session, cache disque, retries, politesse
# --------------------------------------------------------------------------- #
class Fetcher:
    def __init__(self, cache_dir: Path, delay: float = 0.3, retries: int = 3):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; learnagement-scraper/1.0; usage interne Polytech)",
                "Accept-Language": "fr-FR,fr;q=0.9",
            }
        )
        self._lock = threading.Lock()
        self._last = 0.0

    def _throttle(self) -> None:
        with self._lock:
            wait = self._last + self.delay - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()

    def get(self, url: str) -> str:
        path = self.cache_dir / (hashlib.sha1(url.encode()).hexdigest() + ".html")
        if path.exists():
            return path.read_text(encoding="utf-8")
        last_exc: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                self._throttle()
                r = self.session.get(url, timeout=30)
                r.raise_for_status()
                r.encoding = "utf-8"
                path.write_text(r.text, encoding="utf-8")
                return r.text
            except requests.RequestException as exc:  # noqa: PERF203
                last_exc = exc
                log.warning("Echec %s (tentative %d/%d) : %s", url, attempt, self.retries, exc)
                time.sleep(1.5 * attempt)
        raise RuntimeError(f"Impossible de recuperer {url}") from last_exc


# --------------------------------------------------------------------------- #
# Utilitaires de parsing
# --------------------------------------------------------------------------- #
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def to_number(tok: str):
    """'40,5h' -> 40.5 ; '8' -> 8 ; '-' -> None."""
    m = re.search(r"\d+(?:[.,]\d+)?", tok or "")
    if not m:
        return None
    v = float(m.group(0).replace(",", "."))
    return int(v) if v.is_integer() else v


def own_text(li: Tag) -> str:
    """Texte propre d'un <li> (sans sous-listes ni liens)."""
    clone = copy.copy(li)
    for sub in clone.find_all(["ul", "ol"]):
        sub.decompose()
    for a in clone.find_all("a"):
        a.decompose()
    return clone.get_text(" ", strip=True)


def parse_row(li: Tag | None) -> dict:
    """Ligne de maquette : 4 cellules positionnelles ECTS | CM | TD | TP ('-' si vide)."""
    out = {"ects": None, "cm": None, "td": None, "tp": None}
    if li is None:
        return out
    txt = re.sub(r"cr[ée]dits?", "", own_text(li), flags=re.I)
    toks = txt.split()
    if len(toks) == 4:
        out["ects"], out["cm"], out["td"], out["tp"] = (to_number(t) for t in toks)
    elif toks:
        out["_ligne_brute"] = txt  # structure inattendue : on garde le texte pour debug
    return out


def parse_constraint(txt: str) -> dict | None:
    t = norm(txt)
    if t.startswith("facultatif"):
        return {"type": "facultatif", "libelle": txt}
    m = re.search(r"au choix\s*:?\s*(\d+)\s*parmi\s*(\d+)", txt, flags=re.I)
    if m:
        return {"type": "choix", "a_choisir": int(m.group(1)), "parmi": int(m.group(2)), "libelle": txt}
    if t.startswith("au choix"):
        return {"type": "choix", "libelle": txt}
    return None


def split_code(title: str) -> tuple[str | None, str]:
    """'UE704 Visualisation...' -> ('UE704', 'Visualisation...') ; 'Big Data (DATA831_IDU)' -> ('DATA831_IDU', 'Big Data')."""
    m = re.match(r"^(UE\d{3})\s+(.*)$", title)
    if m:
        return m.group(1), m.group(2).strip()
    m = re.search(r"\(\s*([A-Za-z0-9_]+)\s*\)\s*$", title)
    if m:
        return m.group(1), title[: m.start()].strip()
    return None, title.strip()


def semester_of(ue_code: str | None) -> int | None:
    """UE501 -> 5 ; UE001 (stage fin d'etudes) -> 10."""
    m = re.match(r"^UE(\d)\d{2}$", ue_code or "")
    if not m:
        return None
    d = int(m.group(1))
    return 10 if d == 0 else d


def contact_hours(n: dict) -> float | int | None:
    vals = [n[k] for k in ("cm", "td", "tp") if n.get(k) is not None]
    return sum(vals) if vals else None


# --------------------------------------------------------------------------- #
# Maquette (page de la formation)
# --------------------------------------------------------------------------- #
def group_constraints(li: Tag | None) -> list[dict]:
    """Remonte les <li> 'Facultatif' / 'Au choix' (sans lien propre) qui encadrent un item."""
    out: list[dict] = []
    node = li.find_parent("li") if li else None
    while node is not None:
        first = node.find("a", href=True)
        if first is not None and first.find_parent("li") is node:
            break  # on est arrive au module/UE parent
        c = parse_constraint(own_text(node))
        if c:
            out.append(c)
        node = node.find_parent("li")
    return out


def parse_program(soup: BeautifulSoup, formation_url: str):
    base = formation_url[: -len(".html")] + "/"
    parcours: dict[str, dict] = {}
    nodes: dict[str, dict] = {}

    for a in soup.find_all("a", href=True):
        url = urljoin(formation_url, a["href"]).split("#")[0].split("?")[0]
        if not (url.startswith(base) and url.endswith(".html")):
            continue
        segs = url[len(base): -len(".html")].split("/")
        title = a.get_text(" ", strip=True)
        if not title:
            continue

        if len(segs) == 1:  # page d'un parcours
            p = parcours.setdefault(segs[0], {"url": url, "nom": None})
            if p["nom"] is None and not norm(title).startswith("voir"):
                p["nom"] = title
            continue
        if url in nodes:
            continue

        li = a.find_parent("li")
        code, titre = split_code(title)
        node = {
            "type": "UE" if len(segs) == 2 else "module",
            "code": code,
            "titre": titre,
            "url": url,
            "_parcours": segs[0],
            "_depth": len(segs),
            "_parent": url.rsplit("/", 1)[0] + ".html",
            **parse_row(li),
            "contraintes": group_constraints(li),
        }
        nodes[url] = node

    # Hierarchie via le chemin d'URL
    ues: dict[str, list[dict]] = {k: [] for k in parcours}
    for n in nodes.values():
        parent = nodes.get(n["_parent"])
        if n["_depth"] == 2:
            ues.setdefault(n["_parcours"], []).append(n)
        elif parent is not None:
            parent.setdefault("sous_modules" if parent["type"] == "module" else "modules", []).append(n)
        else:
            log.warning("Parent introuvable pour %s", n["url"])
    return parcours, ues, nodes


# --------------------------------------------------------------------------- #
# Detail d'une page (formation, UE, module) : sections par titres + infos cle/valeur
# --------------------------------------------------------------------------- #
INFO_LABELS = {
    "ects": ["ects"],
    "composante": ["composante"],
    "langues_enseignement": ["langues d enseignement", "langue d enseignement"],
    "ouvert_echange": ["ouvert aux etudiants en echange"],
    "niveau_diplome": ["niveau de diplome"],
    "duree": ["duree"],
    "niveau_entree": ["niveau d entree"],
    "campus": ["campus"],
    "lieux": ["lieux"],
    "regimes_etude": ["regimes d etude"],
    "code_rncp": ["code rncp"],
    "responsables": ["responsable", "responsables", "responsable s", "responsable de l enseignement"],
    "enseignants": ["enseignant", "enseignants", "enseignant s", "intervenants"],
    "volume_horaire": ["volume horaire", "volume horaire total", "heures"],
    "semestre": ["semestre", "periode"],
    "coefficient": ["coefficient", "coefficients"],
    "modalites_enseignement": ["modalites d enseignement"],
}
LABEL_LOOKUP = {norm(v): k for k, vs in INFO_LABELS.items() for v in vs}

# Cle canonique <- prefixes de titres de sections (normalises)
CANON = [
    ("presentation", ["presentation", "description", "resume"]),
    ("objectifs", ["objectif"]),
    ("prerequis", ["prerequis", "pre requis", "connaissances prealables", "pre requis recommandes"]),
    ("plan_du_cours", ["plan du cours", "plan", "contenu", "programme du cours", "syllabus"]),
    ("competences", ["competences", "acquis d apprentissage"]),
    ("bibliographie", ["bibliograph", "ressources", "references"]),
    ("modalites_controle", ["modalites de controle", "controle des connaissances", "evaluation", "modalites d evaluation"]),
]


def canon_key(title: str) -> str | None:
    t = norm(title)
    for key, prefixes in CANON:
        if any(t == p or t.startswith(p) for p in prefixes):
            return key
    return None


def clean_lines(parts: list[str]) -> str:
    text = "".join(parts)
    lines = [re.sub(r"[ \t\u00a0]+", " ", l).strip() for l in text.split("\n")]
    out: list[str] = []
    for l in lines:
        if l or (out and out[-1]):
            out.append(l)
    return "\n".join(out).strip()


def parse_detail(html: str, drop_link_heavy_sections: bool = False) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    meta = {m["name"]: m.get("content") for m in soup.find_all("meta") if m.get("name")}

    for t in soup.find_all(["script", "style", "noscript", "header", "nav", "footer"]):
        t.decompose()
    root = soup.find("main") or soup.find(id="main-content") or soup.body or soup

    h1 = root.find("h1") or soup.find("h1")
    out: dict = {"titre_page": h1.get_text(" ", strip=True) if h1 else None}

    # PDF "Fiche synthetique"
    for a in root.find_all("a", href=True):
        if ".pdf" in a["href"].lower() or "fiche synth" in norm(a.get_text()):
            out["fiche_pdf"] = a["href"]
            break

    # Infos label -> valeur (ligne suivante)
    lines = [l.strip() for l in root.get_text("\n", strip=True).split("\n") if l.strip()]
    infos: dict[str, str] = {}
    for i, l in enumerate(lines[:-1]):
        key = LABEL_LOOKUP.get(norm(l))
        if key and key not in infos:
            infos[key] = lines[i + 1]
    if "ects" in infos:
        out["ects"] = to_number(infos["ects"])
    out["infos"] = infos

    # Sections decoupees par titres (ordre du document)
    sections: dict[str, str] = {}
    for h in root.find_all(sorted(HEADINGS)):
        title = h.get_text(" ", strip=True)
        if not title or h.name == "h1":
            continue
        parts: list[str] = []
        n_links = 0
        inside = {id(x) for x in h.descendants}
        for el in h.next_elements:
            if id(el) in inside:
                continue  # le titre lui-meme
            if isinstance(el, Tag):
                if el.name in HEADINGS:
                    break
                if el.name == "a":
                    n_links += 1
                if el.name in BLOCKS:
                    parts.append("\n")
                if el.name == "li":
                    parts.append("- ")
            elif isinstance(el, NavigableString) and not isinstance(el, Comment):
                parts.append(str(el))
        if drop_link_heavy_sections and n_links > 15:
            continue
        text = clean_lines(parts)
        if not text:
            continue
        key = title
        while key in sections:  # titres dupliques
            key += " (bis)"
        sections[key] = text
    out["sections"] = sections

    for title, text in sections.items():
        c = canon_key(title)
        if c and c not in out:
            out[c] = text

    out["meta"] = {
        k: v for k, v in meta.items() if k in ("DC.identifier", "DC.date", "DC.title", "DC.publisher")
    }
    out["texte_brut"] = "\n".join(lines)
    return out


# --------------------------------------------------------------------------- #
# Assemblage
# --------------------------------------------------------------------------- #
def enrich(node: dict, fetcher: Fetcher, keep_raw: bool) -> None:
    try:
        d = parse_detail(fetcher.get(node["url"]))
    except Exception as exc:  # noqa: BLE001
        node["erreur_detail"] = str(exc)
        log.error("Detail KO %s : %s", node["url"], exc)
        return
    if node.get("ects") is None and d.get("ects") is not None:
        node["ects"] = d["ects"]
    d.pop("titre_page", None)
    d.pop("ects", None)
    if not keep_raw:
        d.pop("texte_brut", None)
    node.update(d)


def finalize(node: dict) -> dict:
    node["heures"] = {
        "cm": node.pop("cm", None),
        "td": node.pop("td", None),
        "tp": node.pop("tp", None),
    }
    node["heures"]["contact_total"] = contact_hours(node["heures"])
    for k in ("_parcours", "_depth", "_parent"):
        node.pop(k, None)
    for child_key in ("modules", "sous_modules"):
        for ch in node.get(child_key, []):
            finalize(ch)
    return node


def walk(node: dict):
    yield node
    for k in ("modules", "sous_modules"):
        for ch in node.get(k, []):
            yield from walk(ch)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("-o", "--out", default="idu_maquette.json")
    ap.add_argument("--cache", default=".cache_formations", help="dossier de cache HTML (relancer = quasi instantane)")
    ap.add_argument("--no-details", action="store_true", help="maquette seule, sans visiter les pages UE/modules")
    ap.add_argument("--no-raw", action="store_true", help="ne pas inclure `texte_brut` des pages de detail")
    ap.add_argument("--parcours", help="ne garder que les parcours dont le nom/slug contient ce texte (ex: alternance)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--delay", type=float, default=0.3, help="delai mini entre requetes (s)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")

    fetcher = Fetcher(Path(args.cache), delay=args.delay)
    html = fetcher.get(args.url)
    soup = BeautifulSoup(html, "html.parser")

    formation = parse_detail(html, drop_link_heavy_sections=True)
    formation.pop("texte_brut", None)
    parcours, ues, nodes = parse_program(soup, args.url)
    log.info("%d parcours, %d noeuds (UE + modules)", len(parcours), len(nodes))

    selected = {
        slug: p
        for slug, p in parcours.items()
        if not args.parcours or norm(args.parcours) in norm((p["nom"] or "") + " " + slug)
    }
    targets = [n for slug in selected for ue in ues.get(slug, []) for n in walk(ue)]

    if not args.no_details:
        log.info("Telechargement du detail de %d pages...", len(targets))
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            list(ex.map(lambda n: enrich(n, fetcher, not args.no_raw), targets))

    result_parcours = []
    for slug, p in selected.items():
        sems: dict[int | None, list[dict]] = {}
        for ue in ues.get(slug, []):
            sems.setdefault(semester_of(ue["code"]), []).append(finalize(ue))
        semestres = []
        for num in sorted(sems, key=lambda x: (x is None, x)):
            semestres.append(
                {
                    "numero": num,
                    "ects": sum(u["ects"] or 0 for u in sems[num]),
                    "ue": sems[num],
                }
            )
        result_parcours.append({"nom": p["nom"] or slug, "url": p["url"], "semestres": semestres})

    data = {
        "source": args.url,
        "extrait_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "formation": formation,
        "parcours": result_parcours,
    }
    Path(args.out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    n_mod = sum(1 for n in targets if n["type"] == "module")
    log.info("OK -> %s (%d UE, %d modules)", args.out, len(targets) - n_mod, n_mod)


if __name__ == "__main__":
    main()