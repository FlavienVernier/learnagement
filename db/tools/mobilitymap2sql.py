import csv
from pathlib import Path

CSV = Path("mobility_map/public/mobility.csv")  # fichier CSV attendu avec les en-têtes fournis
OUT = Path("db/freeData/5_mob_partner_universities.sql")

def sql_val(v):
    if v is None or v == "":
        return "NULL"
    v = str(v).replace("'", "''")
    return f"'{v}'"

def int_val(v):
    if v is None or v == "":
        return "NULL"
    try:
        return str(int(float(str(v).replace(',', '.'))))
    except Exception:
        return "NULL"

def float_val(v):
    if v is None or v == "":
        return "NULL"
    try:
        return str(float(str(v).replace(',', '.')))
    except Exception:
        return "NULL"

def parse_lat_long(s):
    if not s:
        return (None, None)
    s = str(s).strip()
    for sep in (',', ';'):
        if sep in s:
            parts = [p.strip() for p in s.split(sep) if p.strip()]
            if len(parts) >= 2:
                return parts[0], parts[1]
    parts = s.split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return (None, None)

# colonnes (dans l'ordre) correspondant à la table MOB_partner_university (sans la PK auto-incrémentée)
cols = [
    "name","code","country","address","latitude","longitude","website","languages",
    "S8_total_places","S8_MM","S8_MC","S8_MMT","S8_SNI","S8_BAT","S8_EIT","S8_IDU","S8_ESB","S8_AM",
    "S9_total_places","S9_MM","S9_MC","S9_MMT","S9_SNI","S9_BAT","S9_EIT","S9_IDU","S9_ESB","S9_AM",
    "note_min","type"
]

with CSV.open(newline='', encoding='utf-8') as f_in, OUT.open('w', encoding='utf-8') as f_out:
    rdr = csv.DictReader(f_in, delimiter=';')
    rows = []
    for r in rdr:
        vals = []
        # mapping des en-têtes fournis vers les colonnes
        vals.append(sql_val(r.get("\ufeffnom_partenaire", "")))  # name
        vals.append(sql_val(r.get("code", "")))  # code
        vals.append(sql_val(r.get("pays", "")))  # country
        vals.append(sql_val(r.get("adresse", "")))  # address

        # latitude / longitude : possibilité de colonnes séparées ou d'une seule colonne "lat long"
        lat = (r.get("latitude") or "").strip()
        lon = (r.get("longitude") or "").strip()
        vals.append(float_val(lat))   # latitude (DECIMAL)
        vals.append(float_val(lon))   # longitude (DECIMAL)

        vals.append(sql_val(r.get("site_web", "")))  # website
        vals.append(sql_val(r.get("langue_des_cours", "")))  # languages

        # colonnes S8 / S9 (entiers)
        s8_fields = ["S8_total_places","S8_MM","S8_MC","S8_MMT","S8_SNI","S8_BAT","S8_EIT","S8_IDU","S8_ESB","S8_AM"]
        s9_fields = ["S9_total_places","S9_MM","S9_MC","S9_MMT","S9_SNI","S9_BAT","S9_EIT","S9_IDU","S9_ESB","S9_AM"]
        for field in s8_fields:
            vals.append(int_val(r.get(field, "")))
        for field in s9_fields:
            vals.append(int_val(r.get(field, "")))

        # note_min (décimal) et type
        vals.append(float_val(r.get("note_min", "") or r.get("note min", "")))
        vals.append(sql_val(r.get("type", "")))

        rows.append("(" + ",".join(vals) + ")")

    if rows:
        f_out.write("LOCK TABLES `MOB_partner_university` WRITE;\n")
        f_out.write("INSERT INTO `MOB_partner_university` (" + ",".join(cols) + ") VALUES\n")
        f_out.write(",\n".join(rows) + ";\n")
        f_out.write("UNLOCK TABLES;\n")

print("Wrote:", OUT)