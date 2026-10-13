"""Census Bureau pulls for Lexington city, Dawson County, Nebraska and the U.S.

- ACS 5-year 2020-2024: estimates and margins of error (API).
- Decennial counts 2000, 2010, 2020: total and Hispanic or Latino (API).
- Decennial counts 1940 to 1990: read out of the Census Bureau's own 1990 volumes for Nebraska
  (CPH-2-29 for totals, CP-1-29 for Hispanic origin), parsed from the PDF text.
- Population estimates, vintage 2025: July 1, 2020 to 2025 (flat files).
"""
import csv
import io
import json
import re
import sys

from pypdf import PdfReader

from common import COUNTY, PLACE, RAW, STATE, cached, get_key, write_csv

GEOS = [("Lexington city", f"for=place:{PLACE}&in=state:{STATE}"),
        ("Dawson County", f"for=county:{COUNTY}&in=state:{STATE}"),
        ("Nebraska", f"for=state:{STATE}"),
        ("United States", "for=us:1")]

# code: what it counts
ACS = {
    "B01003_001": "total population",
    "B03003_003": "Hispanic or Latino",
    "B05002_001": "population, place-of-birth universe",
    "B05002_013": "foreign born",
    "B05001_006": "not a U.S. citizen",
    "B02001_003": "Black or African American alone",
    "C16001_001": "population age 5 and over",
    "C16001_002": "speak only English at home",
    "B19013_001": "median household income, dollars",
    "B17001_001": "population with poverty status determined",
    "B17001_002": "below the poverty level",
    "B25003_001": "occupied housing units",
    "B25003_002": "owner-occupied housing units",
    "B25077_001": "median home value, dollars",
    "B25064_001": "median gross rent, dollars",
    "B01002_001": "median age, years",
    "B25001_001": "housing units",
    "B25002_003": "vacant housing units",
    "C24030_001": "employed civilians age 16 and over",
    "C24030_007": "employed in manufacturing, men",
    "C24030_034": "employed in manufacturing, women",
    "B05006_001": "foreign born, place-of-birth detail universe",
    "B05006_095": "foreign born in Africa",
    "B05006_139": "foreign born in Latin America",
}


def api(path, variables, geo, tag):
    url = f"https://api.census.gov/data/{path}?get={','.join(variables)}&{geo}&key={get_key('CENSUS_API_KEY')}"
    name = re.sub(r"[^A-Za-z0-9]+", "_", f"{path}_{tag}_{geo}") + ".json"
    rows = json.loads(cached(RAW / "census_api" / name, url))
    if len(rows) != 2:
        sys.exit(f"expected one row for {path} {geo}, got {len(rows) - 1}")
    return dict(zip(rows[0], rows[1]))


def acs():
    out = []
    codes = list(ACS)
    for geo, q in GEOS:
        got = {}
        for i in range(0, len(codes), 20):
            part = codes[i:i + 20]
            got.update(api("2024/acs/acs5", [c + s for c in part for s in ("E", "M")], q, f"b{i}"))
        for c in codes:
            out.append((geo, c, ACS[c], got[c + "E"], got[c + "M"]))
    write_csv("acs_2020_2024.csv", ["geography", "variable", "what", "estimate", "margin_of_error_90"], out)


def nums(text):
    """Numbers as the 1990 volumes print them: thousands separated by a space."""
    return [int(m.replace(" ", "")) for m in re.findall(r"(?<![\d.])\d{1,3}(?: \d{3})*(?![\d.])", text)]


def pdf_line(pdf, page, table, starts):
    text = (pdf.pages[page - 1].extract_text() or "").replace("/leaderdash", "").replace("†", "")
    if table not in text:
        sys.exit(f"page {page}: expected {table}")
    hits = [l for l in text.split("\n") if re.sub(r"\s+", " ", l).strip().startswith(starts)]
    if len(hits) != 1:
        sys.exit(f"page {page}: {len(hits)} lines start with {starts!r}")
    return re.sub(r"\s+", " ", hits[0]).strip()[len(starts):]


def decennial():
    base = "https://www2.census.gov/library/publications/decennial/1990/"
    cph = PdfReader(io.BytesIO(cached(RAW / "census_hist" / "cph-2-29.pdf", base + "cph-2/cph-2-29.pdf")))
    cp1 = PdfReader(io.BytesIO(cached(RAW / "census_hist" / "cp-1-29.pdf", base + "cp-1/cp-1-29.pdf")))
    rows = []
    # County, 1940 to 1990: CPH-2-29 Table 3, page 18 of the PDF. Population comes first, newest year first.
    v = nums(pdf_line(cph, 18, "Table 3. Population and Housing Units: 1940 to 1990", "Dawson County"))
    for y, n in zip((1990, 1980, 1970, 1960, 1950, 1940), v[:6]):
        rows.append(("Dawson County", y, n, "", "1990 CPH-2-29, Table 3"))
    # City, 1970 to 1990: CPH-2-29 Table 8, page 37 of the PDF.
    v = nums(pdf_line(cph, 37, "Table 8. Population and Housing Units, 1970 to 1990", "Lexington city"))
    for y, n in zip((1990, 1980, 1970), v[:3]):
        rows.append(("Lexington city", y, n, "", "1990 CPH-2-29, Table 8"))
    # City, 1990, persons of Hispanic origin: CP-1-29 Table 11, page 56 of the PDF.
    hisp = nums(pdf_line(cp1, 56, "Table 11. Summary of General Characteristics of Hispanic Origin Persons", "Lexington city"))[0]
    rows = [(g, y, n, hisp if (g, y) == ("Lexington city", 1990) else h, s + ("; CP-1-29, Table 11" if (g, y) == ("Lexington city", 1990) else ""))
            for g, y, n, h, s in rows]
    for geo, q in GEOS[:2]:
        d = api("2000/dec/sf1", ["P001001", "P004002"], q, "t")
        rows.append((geo, 2000, int(d["P001001"]), int(d["P004002"]), "2000 SF1, P001 and P004"))
        d = api("2010/dec/sf1", ["P001001", "P004003"], q, "t")
        rows.append((geo, 2010, int(d["P001001"]), int(d["P004003"]), "2010 SF1, P1 and P4"))
        d = api("2020/dec/pl", ["P1_001N", "P2_002N"], q, "t")
        rows.append((geo, 2020, int(d["P1_001N"]), int(d["P2_002N"]), "2020 PL 94-171, P1 and P2"))
    keys = [(r[0], r[1]) for r in rows]
    if len(keys) != len(set(keys)):
        sys.exit("duplicate keys in decennial")
    write_csv("decennial_population.csv", ["geography", "year", "population", "hispanic_or_latino", "source"],
              sorted(rows))


def estimates():
    base = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/"
    out = []
    co = csv.DictReader(io.StringIO(cached(RAW / "popest" / "co-est2025-alldata.csv",
                                           base + "counties/totals/co-est2025-alldata.csv").decode("latin-1")))
    hit = [r for r in co if r["STATE"] == STATE and r["COUNTY"] == COUNTY]
    ci = csv.DictReader(io.StringIO(cached(RAW / "popest" / "sub-est2025_31.csv",
                                           base + "cities/totals/sub-est2025_31.csv").decode("latin-1")))
    hit2 = [r for r in ci if r["SUMLEV"] == "162" and r["PLACE"] == PLACE]
    if len(hit) != 1 or len(hit2) != 1:
        sys.exit("population estimates: expected one county row and one city row")
    for geo, r in (("Dawson County", hit[0]), ("Lexington city", hit2[0])):
        for y in range(2020, 2026):
            out.append((geo, y, int(r[f"POPESTIMATE{y}"])))
    write_csv("population_estimates_v2025.csv", ["geography", "july_1_year", "population"], out)


if __name__ == "__main__":
    acs()
    decennial()
    estimates()
