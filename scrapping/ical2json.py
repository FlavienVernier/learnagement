#!/usr/bin/env python3
"""
Import d'emplois du temps ADE (iCal) -> snapshots JSON versionnés.

  python edt_snapshots.py [--racine snapshots] [--config refs.json] fetch <URL|fichier.ics> [--filiere IDU] [--tolerance 0]
  python edt_snapshots.py [--racine snapshots] [--config refs.json] reparse [--filiere IDU] [--force]

Arborescence produite :
  snapshots/<FILIERE>/<AAAA-MM-JJTHHMMZ>/edt.ics        (source brute)
                                         edt.json        (dernier parsing)
                                         edt.v<version>.json  (anciens parsings)
                                         manifest.json   (historique des parsings)
  snapshots/_rejets/<horodatage>/                         (imports refusés, pour intervention humaine)
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# À INCRÉMENTER à chaque modification de la logique d'analyse :
# c'est ce qui déclenche le reparsing des anciens snapshots.
PARSER_VERSION = "1.1.0"

TZ = ZoneInfo("Europe/Paris")

DEFAULT_REFS = {
    "enseignants": [
        "VIGNAND SYLVIE", "SALAMATIAN MOHAMMAD-REZA", "CLARK JULIE",
        "ENRIQUEZ CISNEROS DIANA-IRAIS", "GRAY ALICE", "BASCOP ALEXANDRE",
        "CIMPAN SORANA", "PETIT WILFRIED", "FERRER ROMAIN",
        "ATTO ABDOURRAHMANE", "CHOAIB MOHAMMAD", "PELINKU Sara",
    ],
    "salles": ["A-C215 (52pl.)", "A-C214 (32pl.)", "A-B120 (150pl.)"],
    "groupes": [
        "IDU-4-Promo", "IDU-4-A", "IDU-4-A1", "IDU-4-A2", "IDU-4", "IDU-5",
        "MECA-FISE-4", "MECA-FISE-3", "SNI-4", "SNI-5",
    ],
    "filieres": ["IDU", "SEA", "MECA", "SNI", "EPU", "BAT", "EN", "IB",
                 "EIT", "MC", "ITII", "Master"],
    "statuts": ["FISE", "FISA"],
    "types_cours": ["CM", "TD", "TP", "EXAMEN", "EXAMEN SESSION 2", "PROJET",
                    "REUNION", "TUTORAT", "ACTIVITE ASSOCIATIVE",
                    "ACCUEIL-RENTREE"],
}


class ErreurImport(Exception):
    """Erreur nécessitant une intervention humaine."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


# ==========================================================================
# Lecture / validation de l'iCal
# ==========================================================================
def lire_source(src: str) -> bytes:
    if re.match(r"^https?://", src, re.I):
        req = urllib.request.Request(src, headers={"User-Agent": "learnagement-scraper/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            raise ErreurImport(f"Téléchargement refusé : HTTP {e.code} {e.reason}", {"url": src})
        except urllib.error.URLError as e:
            raise ErreurImport(f"URL inaccessible : {e.reason}", {"url": src})
        except OSError as e:  # timeout, connexion coupée...
            raise ErreurImport(f"Erreur réseau : {e}", {"url": src})
    try:
        return Path(src).read_bytes()
    except OSError as e:
        raise ErreurImport(f"Fichier illisible : {e}", {"fichier": src})


def decoder(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise ErreurImport(f"Le contenu n'est pas de l'UTF-8 valide : {e}")


def unfold(text: str) -> str:
    return re.sub(r"\r?\n[ \t]", "", text)


def unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: "\n" if m.group(1) in "nN" else m.group(1), s)


def parse_vevents(text: str) -> list[dict]:
    events, cur = [], None
    for line in unfold(text).splitlines():
        if line == "BEGIN:VEVENT":
            cur = {}
        elif line == "END:VEVENT":
            events.append(cur)
            cur = None
        elif cur is not None and ":" in line:
            name, value = line.split(":", 1)
            cur[name.split(";")[0].upper()] = value
    return events


def parse_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)


def valider_ics(text: str) -> list[dict]:
    t = text.strip()
    if not t.startswith("BEGIN:VCALENDAR") or not t.endswith("END:VCALENDAR"):
        raise ErreurImport(
            "Le contenu reçu n'est pas un calendrier iCal (BEGIN/END:VCALENDAR absent). "
            "Page de connexion ou d'erreur ?", {"debut_du_contenu": t[:300]})
    raw = parse_vevents(text)
    if not raw:
        raise ErreurImport("Le calendrier ne contient aucun événement (VEVENT).")
    problemes = []
    for i, e in enumerate(raw):
        for champ in ("UID", "SUMMARY", "DTSTART", "DTEND"):
            if not e.get(champ):
                problemes.append(f"événement #{i} ({e.get('UID', '?')}) : champ {champ} manquant")
        try:
            if parse_dt(e["DTEND"]) <= parse_dt(e["DTSTART"]):
                problemes.append(f"événement #{i} ({e.get('UID', '?')}) : fin <= début")
        except (KeyError, ValueError) as ex:
            problemes.append(f"événement #{i} ({e.get('UID', '?')}) : date invalide ({ex})")
    if problemes:
        raise ErreurImport(f"{len(problemes)} problème(s) de structure iCal",
                           {"problemes": problemes[:50]})
    return raw


def horodatage(raw_events: list[dict]) -> str:
    """Date de l'export = plus grand DTSTAMP (ex. 20261103T201415Z -> 2026-11-03T2014Z)."""
    stamps = [e["DTSTAMP"] for e in raw_events if e.get("DTSTAMP")]
    if not stamps:
        raise ErreurImport("Aucun DTSTAMP : impossible de dater l'export.")
    return parse_dt(max(stamps)).strftime("%Y-%m-%dT%H%MZ")


# ==========================================================================
# Décomposition des champs
# ==========================================================================
def norm(s: str) -> str:
    s = re.sub(r"\(provisoire\)", "", s, flags=re.I)
    return re.sub(r"\s+", " ", s).strip().casefold()


ROOM_RE = re.compile(r"^(?P<nom>.*?)\s*\((?P<cap>\d+)\s*pl\.\)\s*$")
ROOM_ID_RE = re.compile(r"^(?P<bat>[A-Z])-(?P<salle>\S+)")


def parse_rooms(raw_location: str, known_rooms: set[str]) -> list[dict]:
    rooms = []
    for part in re.split(r"(?<!\\),", raw_location or ""):
        part = unescape(part).strip()
        if not part:
            continue
        m = ROOM_RE.match(part)
        nom = m["nom"] if m else part
        mid = ROOM_ID_RE.match(nom)
        rooms.append({
            "nom": nom,
            "capacite": int(m["cap"]) if m else None,
            "batiment": mid["bat"] if mid else None,
            "salle": mid["salle"] if mid else None,
            "distanciel": nom.lower().startswith("distanciel"),
            "connue": norm(nom) in known_rooms,
        })
    return rooms


def parse_group(name: str, filieres: set, statuts: set, connu: bool = True) -> dict:
    tokens = [t for t in re.split(r"[-_]", name) if t]
    statut, annee, reste = None, None, []
    for t in tokens[1:]:
        if t.upper() in statuts:
            statut = t.upper()
        elif t.isdigit() and annee is None:
            annee = int(t)
        else:
            reste.append(t)
    return {
        "nom": name,
        "connu": connu,
        "filiere": tokens[0] if tokens else None,
        "filiere_connue": bool(tokens) and tokens[0] in filieres,
        "statut": statut,
        "annee": annee,
        "sous_groupe": "-".join(reste) or None,
    }


def looks_like_group(item: str, filieres: set) -> bool:
    """Groupe absent de la liste, mais dont le préfixe est une filière connue."""
    return bool(re.fullmatch(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*", item)
                and re.split(r"[-_]", item)[0] in filieres)


CODE_RE = re.compile(r"(?<![A-Za-z])([A-Z]{2,5})\s?(\d{3})(?!\d)")
TITLE_TYPE_RE = re.compile(r"^(?P<titre>.*?)\s*\((?P<type>[^()]*)\)\s*$")


def decode_uid(uid: str):
    """ADE60<hex> -> 'Savoie2026-2027-12759-0-5' -> (12759, [0, 5])"""
    m = re.fullmatch(r"ADE60([0-9a-fA-F]+)", uid or "")
    if not m or len(m[1]) % 2:
        return None, None
    try:
        s = bytes.fromhex(m[1]).decode("ascii")
    except (ValueError, UnicodeDecodeError):
        return None, None
    m = re.search(r"-(\d+)-(\d+)-(\d+)$", s)
    return (int(m[1]), [int(m[2]), int(m[3])]) if m else (None, None)


def parse_description(raw: str, refs: dict) -> dict:
    groups_idx = {g.casefold(): g for g in refs["groupes"]}
    teachers_idx = {norm(t): t for t in refs["enseignants"]}
    filieres = set(refs["filieres"])
    statuts = {s.upper() for s in refs["statuts"]}

    head_raw, _, tail_raw = raw.partition("(Exporté le:")

    lines = [unescape(l).strip() for l in re.split(r"\\[nN]", head_raw)]
    first = lines[0] if lines else ""
    m = TITLE_TYPE_RE.match(first)
    titre = m["titre"].strip() if m else first
    type_raw = (m["type"].strip() if m else "") or None

    groupes, enseignants, ressources, autres = [], [], [], []
    for it in (l for l in lines[1:] if l):
        if it.casefold() in groups_idx:
            groupes.append(parse_group(groups_idx[it.casefold()], filieres, statuts))
        elif norm(it) in teachers_idx:
            enseignants.append({"nom": teachers_idx[norm(it)],
                                "provisoire": bool(re.search(r"\(provisoire\)", it, re.I))})
        elif looks_like_group(it, filieres):
            groupes.append(parse_group(it, filieres, statuts, connu=False))
        elif it.isdigit():
            ressources.append(it)
        else:
            autres.append(it)

    export_le = None
    m = re.match(r"^([^)]*)\)", tail_raw)
    if m:
        export_le = m.group(1).strip()
        tail_raw = tail_raw[m.end():]
    parts = [re.sub(r"(\\[nN])+", " ", p).strip() for p in re.split(r"\\,", tail_raw)]
    parts += [""] * (3 - len(parts))

    return {
        "titre": titre or None,
        "type_cours": type_raw,
        "type_connu": (type_raw in refs["types_cours"]) if type_raw else None,
        "groupes": groupes,
        "enseignants": enseignants,
        "ressources": ressources,
        "non_classes": autres,
        "export_le": export_le,
        "nom_module": parts[0] or None,
        "code_ue": parts[1] or None,
        "extra": parts[2] or None,
    }


def convert_event(ev: dict, refs: dict, known_rooms: set[str]) -> dict:
    start, end = parse_dt(ev["DTSTART"]), parse_dt(ev["DTEND"])
    desc = parse_description(ev.get("DESCRIPTION", ""), refs)
    summary = unescape(ev.get("SUMMARY", "")).strip()
    m = CODE_RE.search(desc["titre"] or "") or CODE_RE.search(summary)
    start_l, end_l = start.astimezone(TZ), end.astimezone(TZ)
    groupes = desc["groupes"]
    id_activite, uid_indices = decode_uid(ev.get("UID"))

    return {
        "uid": ev.get("UID"),
        "id_activite": id_activite,
        "uid_indices": uid_indices,
        "resume": summary,
        "code_matiere": f"{m.group(1)}{m.group(2)}" if m else None,
        "titre": desc["titre"],
        "nom_module": desc["nom_module"],
        "code_ue": desc["code_ue"],
        "type_cours": desc["type_cours"],
        "type_connu": desc["type_connu"],
        "debut": start_l.isoformat(),
        "fin": end_l.isoformat(),
        "debut_utc": start.isoformat(),
        "fin_utc": end.isoformat(),
        "date": start_l.date().isoformat(),
        "jour_semaine": start_l.strftime("%A"),
        "duree_minutes": int((end - start).total_seconds() // 60),
        "salles": parse_rooms(ev.get("LOCATION", ""), known_rooms),
        "enseignants": desc["enseignants"],
        "groupes": groupes,
        "filieres": sorted({g["filiere"] for g in groupes if g["filiere"]}),
        "statuts": sorted({g["statut"] for g in groupes if g["statut"]}),
        "ressources": desc["ressources"],
        "non_classes": desc["non_classes"],
        "extra": desc["extra"],
        "export_le": desc["export_le"],
        "cree_le": ev.get("CREATED"),
        "modifie_le": ev.get("LAST-MODIFIED"),
        "dtstamp": ev.get("DTSTAMP"),
        "sequence": int(ev["SEQUENCE"]) if ev.get("SEQUENCE", "").isdigit() else None,
    }


def build_referentiels(events: list[dict]) -> dict:
    return {
        "enseignants": sorted({e["nom"] for ev in events for e in ev["enseignants"]}),
        "salles": sorted({(s["nom"], s["capacite"]) for ev in events for s in ev["salles"]}),
        "groupes": sorted({g["nom"] for ev in events for g in ev["groupes"]}),
        "filieres": sorted({f for ev in events for f in ev["filieres"]}),
        "statuts": sorted({s for ev in events for s in ev["statuts"]}),
        "types_cours": sorted({ev["type_cours"] for ev in events if ev["type_cours"]}),
        "modules": sorted({(ev["code_matiere"], ev["nom_module"]) for ev in events
                           if ev["code_matiere"]}),
    }


# ==========================================================================
# Validation de la filière
# ==========================================================================
def detecter_filiere(events: list[dict], attendue: str | None, tolerance: int):
    compteur = Counter(f for ev in events for f in set(ev["filieres"]))
    if not compteur:
        raise ErreurImport("Aucune filière détectable dans les groupes des événements.",
                           {"astuce": "Compléter la liste 'groupes' / 'filieres' de la configuration."})
    if attendue:
        filiere = attendue
    else:
        top = compteur.most_common(2)
        if len(top) == 2 and top[0][1] == top[1][1]:
            raise ErreurImport("Filière ambiguë : plusieurs filières à égalité.",
                               {"repartition": dict(compteur)})
        filiere = top[0][0]

    hors = [ev for ev in events if filiere not in ev["filieres"]]
    if len(hors) > tolerance:
        raise ErreurImport(
            f"{len(hors)} événement(s) sur {len(events)} ne concernent pas la filière « {filiere} » "
            f"(tolérance : {tolerance}).",
            {"repartition_filieres": dict(compteur),
             "evenements_hors_filiere": [
                 {"uid": e["uid"], "resume": e["resume"], "debut": e["debut"],
                  "groupes": [g["nom"] for g in e["groupes"]]} for e in hors[:50]]})
    return filiere, hors


def analyser(text: str, refs: dict, filiere_attendue: str | None, tolerance: int):
    raw = valider_ics(text)
    known_rooms = {norm(ROOM_RE.match(r)["nom"] if ROOM_RE.match(r) else r)
                   for r in refs["salles"]}
    events = sorted((convert_event(e, refs, known_rooms) for e in raw),
                    key=lambda e: e["debut_utc"])
    filiere, hors = detecter_filiere(events, filiere_attendue, tolerance)
    return raw, events, filiere, hors


# ==========================================================================
# Écriture des snapshots (JSON courant + archives versionnées)
# ==========================================================================
def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def refs_hash(refs: dict) -> str:
    return sha256(json.dumps(refs, sort_keys=True, ensure_ascii=False).encode())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def nettoyer(nom: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", nom)


def lire_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def ecrire_json_fichier(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def construire_json(events, filiere, hors, data, source, horo, refs) -> dict:
    return {
        "meta": {
            "filiere": filiere,
            "source": source,
            "source_sha256": sha256(data),
            "horodatage_export": horo,
            "parser_version": PARSER_VERSION,
            "refs_sha256": refs_hash(refs),
            "genere_le": now_iso(),
            "fuseau": "Europe/Paris",
            "nb_evenements": len(events),
            "uid_hors_filiere": [e["uid"] for e in hors],
        },
        "evenements": events,
        "referentiels": build_referentiels(events),
    }


def ecrire_snapshot_json(dest: Path, data_json: dict, manifest: dict):
    """Écrit edt.json ; l'ancien edt.json est conservé sous edt.v<version>.json."""
    cible = dest / "edt.json"
    if cible.exists():
        ancien = lire_json(cible) or {}
        v = ancien.get("meta", {}).get("parser_version", "inconnue")
        archive = dest / f"edt.v{v}.json"
        n = 1
        while archive.exists():
            archive = dest / f"edt.v{v}.{n}.json"
            n += 1
        cible.rename(archive)
        for p in manifest.get("parsings", []):
            if p.get("fichier") == "edt.json":
                p["fichier"] = archive.name
    ecrire_json_fichier(cible, data_json)
    manifest.setdefault("parsings", []).append({
        "fichier": "edt.json",
        "parser_version": data_json["meta"]["parser_version"],
        "refs_sha256": data_json["meta"]["refs_sha256"],
        "genere_le": data_json["meta"]["genere_le"],
    })
    ecrire_json_fichier(dest / "manifest.json", manifest)


def archiver_rejet(racine: Path, source: str, data, err: ErreurImport) -> Path:
    d = racine / "_rejets" / datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    d.mkdir(parents=True, exist_ok=True)
    if data:
        (d / "recu.ics").write_bytes(data)
    ecrire_json_fichier(d / "erreur.json", {
        "source": source, "message": str(err), "details": err.details, "date": now_iso()})
    return d


# ==========================================================================
# Commandes
# ==========================================================================
def cmd_fetch(args, refs) -> int:
    racine = Path(args.racine)
    data = None
    try:
        data = lire_source(args.source)
        raw, events, filiere, hors = analyser(decoder(data), refs, args.filiere, args.tolerance)
        horo = horodatage(raw)
    except ErreurImport as e:
        d = archiver_rejet(racine, args.source, data, e)
        print(f"Import refusé, détails conservés dans {d}", file=sys.stderr)
        raise

    dest = racine / nettoyer(filiere) / horo
    if dest.exists():
        existant = dest / "edt.ics"
        if existant.exists() and sha256(existant.read_bytes()) == sha256(data):
            print(f"Déjà importé : {dest} (rien à faire)")
            return 0
        raise ErreurImport(f"Le dossier {dest} existe déjà avec un contenu différent.",
                           {"astuce": "Deux exports différents à la même minute : vérifier à la main."})

    dest.mkdir(parents=True)
    (dest / "edt.ics").write_bytes(data)
    manifest = {"filiere": filiere, "source": args.source, "source_sha256": sha256(data),
                "tolerance": args.tolerance, "importe_le": now_iso(), "parsings": []}
    ecrire_snapshot_json(dest, construire_json(events, filiere, hors, data, args.source, horo, refs),
                         manifest)
    msg = f"OK : {len(events)} événements, filière {filiere} -> {dest}"
    if hors:
        msg += f" ({len(hors)} événement(s) hors filière tolérés, voir meta.uid_hors_filiere)"
    print(msg)
    return 0


def cmd_reparse(args, refs) -> int:
    racine = Path(args.racine)
    rh = refs_hash(refs)
    refaits, ignores, erreurs = 0, 0, []

    for ics in sorted(racine.glob("*/*/edt.ics")):
        dest = ics.parent
        fil_dir = dest.parent.name
        if fil_dir.startswith("_") or (args.filiere and fil_dir != args.filiere):
            continue
        manifest = lire_json(dest / "manifest.json") or {}
        dernier = (manifest.get("parsings") or [{}])[-1]
        a_jour = (dernier.get("parser_version") == PARSER_VERSION
                  and dernier.get("refs_sha256") == rh
                  and (dest / "edt.json").exists())
        if a_jour and not args.force:
            ignores += 1
            continue
        try:
            data = ics.read_bytes()
            raw, events, filiere, hors = analyser(decoder(data), refs, fil_dir,
                                                  manifest.get("tolerance", 0))
            horo = dest.name
            manifest.setdefault("filiere", filiere)
            manifest.setdefault("source", "inconnue")
            manifest.setdefault("source_sha256", sha256(data))
            manifest.setdefault("tolerance", 0)
            # Le nouveau JSON est construit AVANT d'archiver l'ancien : en cas d'erreur, rien n'est modifié.
            ecrire_snapshot_json(dest, construire_json(events, filiere, hors, data,
                                                       manifest["source"], horo, refs), manifest)
            refaits += 1
            print(f"reparsé : {dest} (v{PARSER_VERSION})")
        except ErreurImport as e:
            erreurs.append((str(dest), str(e), e.details))
            print(f"ERREUR sur {dest} : {e}", file=sys.stderr)

    print(f"\n{refaits} reparsé(s), {ignores} déjà à jour, {len(erreurs)} en erreur.")
    if erreurs:
        ecrire_json_fichier(racine / "_reparse_erreurs.json",
                            [{"snapshot": s, "message": m, "details": d} for s, m, d in erreurs])
        print(f"Détails des erreurs : {racine / '_reparse_erreurs.json'}", file=sys.stderr)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="Snapshots JSON d'emplois du temps ADE")
    ap.add_argument("--racine", default="snapshots")
    ap.add_argument("--config", help="JSON des listes de référence")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="télécharger, valider et stocker un iCal")
    f.add_argument("source", help="URL de l'iCal (ou chemin d'un .ics local)")
    f.add_argument("--filiere", help="filière attendue (sinon déduite du contenu)")
    f.add_argument("--tolerance", type=int, default=0,
                   help="nb d'événements transversaux autorisés hors filière (défaut 0)")

    r = sub.add_parser("reparse", help="reparser les .ics existants")
    r.add_argument("--filiere", help="limiter à une filière")
    r.add_argument("--force", action="store_true",
                   help="reparser même si version et référentiels sont à jour")

    args = ap.parse_args()
    refs = dict(DEFAULT_REFS)
    if args.config:
        with open(args.config, encoding="utf-8") as fh:
            refs.update(json.load(fh))

    try:
        code = cmd_fetch(args, refs) if args.cmd == "fetch" else cmd_reparse(args, refs)
    except ErreurImport as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        if e.details:
            print(json.dumps(e.details, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    sys.exit(code)


if __name__ == "__main__":
    main()