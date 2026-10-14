"""Tie-out. Reads the raw files in data/raw again with its own parsing, compares every value in
data/processed, then recomputes each number that appears in a chart or in research/first-pull.md.
Prints one line per check and exits non-zero on any mismatch."""
import csv
import glob
import io
import json
import re
import sys

from pypdf import PdfReader

from common import AREA, PROC, RAW, read_csv

bad = 0


def check(name, got, want, tol=0):
    global bad
    ok = abs(float(got) - float(want)) <= tol
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got} (expected {want})")


def note(name, value):
    print(f"     {name}: {value}")


# ---- LAUS, raw JSON against processed
raw = {}
for f in glob.glob(str(RAW / "bls_laus" / "LAUCN*.json")):
    for s in json.load(open(f))["Results"]["series"]:
        for o in s["data"]:
            if o["period"] != "M13":
                raw[(s["seriesID"][-1], int(o["year"]), int(o["period"][1:]))] = o["value"]
laus = read_csv("laus_dawson_monthly.csv")
names = {"3": "unemployment_rate", "4": "unemployed", "5": "employed", "6": "labor_force"}
diff = sum(1 for r in laus for k, n in names.items()
           if (raw[(k, int(r["year"]), int(r["month"]))] if raw[(k, int(r["year"]), int(r["month"]))] != "-" else "") != r[n])
check("LAUS processed values that differ from raw", diff, 0)
check("LAUS months", len(laus), len({(y, m) for _, y, m in raw}))
L = {(int(r["year"]), int(r["month"])): r for r in laus}
for (y, m), want in (((2026, 1), 3.4), ((2026, 2), 16.9), ((2026, 3), 20.1), ((2026, 8), 16.4)):
    check(f"unemployment rate {y}-{m:02d}", L[(y, m)]["unemployment_rate"], want)
check("peak rate since 1990 is March 2026", max((float(r["unemployment_rate"]) for r in laus if r["unemployment_rate"]), default=0), 20.1)
e0, e1 = int(L[(2025, 8)]["employed"]), int(L[(2026, 8)]["employed"])
f0, f1 = int(L[(2025, 8)]["labor_force"]), int(L[(2026, 8)]["labor_force"])
check("employed residents Aug 2025", e0, 13292)
check("employed residents Aug 2026", e1, 9941)
check("employed residents change, %", round(100 * (e1 - e0) / e0, 1), -25.2)
check("labor force change, %", round(100 * (f1 - f0) / f0, 1), -12.9)
note("employed residents lost, Aug 2025 to Aug 2026", e0 - e1)
note("blank months", [k for k, r in L.items() if r["unemployment_rate"] == ""])

# ---- QCEW, raw CSV against processed
q = read_csv("qcew_dawson_quarterly.csv")
Q = {(int(r["year"]), int(r["quarter"]), r["own_code"], r["industry_code"]): r for r in q}
diff = n = 0
for f in sorted(glob.glob(str(RAW / "bls_qcew" / f"*_{AREA}.csv"))):
    y, qq = re.search(r"(\d{4})_q(\d)", f).groups()
    for r in csv.DictReader(open(f)):
        k = (int(y), int(qq), r["own_code"], r["industry_code"])
        if k in Q and r["agglvl_code"] in ("70", "71", "73", "74", "75"):
            n += 1
            if r["disclosure_code"].strip() == "N":
                diff += Q[k]["flag"] != "withheld"
            else:
                diff += any(Q[k][a] != r[b] for a, b in (("month1_jobs", "month1_emplvl"), ("month2_jobs", "month2_emplvl"),
                                                         ("month3_jobs", "month3_emplvl"), ("avg_weekly_wage", "avg_wkly_wage")))
check("QCEW processed rows that differ from raw", diff, 0)
check("QCEW rows matched", n, len(q))


def jobs(y, qq, own, ind, month):
    return int(Q[(y, qq, own, ind)][f"month{month}_jobs"])


all25, all26 = jobs(2025, 1, "0", "10", 3), jobs(2026, 1, "0", "10", 3)
pr25, pr26 = jobs(2025, 1, "5", "10", 3), jobs(2026, 1, "5", "10", 3)
mf25, mf26 = jobs(2025, 1, "5", "31-33", 3), jobs(2026, 1, "5", "31-33", 3)
check("all jobs March 2025", all25, 11868)
check("private jobs March 2025", pr25, 9444)
check("private jobs March 2026", pr26, 5673)
check("manufacturing jobs March 2025", mf25, 3997)
check("manufacturing jobs March 2026", mf26, 677)
check("manufacturing change, %", round(100 * (mf26 - mf25) / mf25, 1), -83.1)
check("private change, %", round(100 * (pr26 - pr25) / pr25, 1), -39.9)
note("all jobs March 2026 and change, %", (all26, round(100 * (all26 - all25) / all25, 1)))
check("food manufacturing jobs January 2026", jobs(2026, 1, "5", "311", 1), 2909)
check("food manufacturing jobs March 2026", jobs(2026, 1, "5", "311", 3), 217)
WARN = 3212   # positions in the WARN notice, a reported figure, not from BLS
check("WARN positions as % of all jobs, March 2025 (editorial)", round(100 * WARN / all25, 1), 27.1)
check("WARN positions as % of private jobs, March 2025 (editorial)", round(100 * WARN / pr25, 1), 34.0)

# average annual pay, private manufacturing, 2024: total wages over average monthly jobs
mq = [r for r in q if r["year"] == "2024" and r["own_code"] == "5" and r["industry_code"] == "31-33"]
mpay = sum(int(r["total_quarterly_wages"]) for r in mq) / (sum(int(r[f"month{m}_jobs"]) for r in mq for m in (1, 2, 3)) / 12)
check("manufacturing quarters in 2024", len(mq), 4)
check("manufacturing average pay 2024, $ a year", round(mpay), 54247)
check("manufacturing average pay 2024, $ a week", round(mpay / 52), 1043)
note("food manufacturing quarters withheld", f"{sum(1 for r in q if r['industry_code'] == '311' and r['flag'])} of "
                                             f"{sum(1 for r in q if r['industry_code'] == '311')}")

# ---- Decennial: 1990 volumes re-read by a different route (whole-page regex), API years from raw JSON
d = {(r["geography"], int(r["year"])): r for r in read_csv("decennial_population.csv")}


def page(pdf, n):
    return re.sub(r"\s+", " ", (PdfReader(io.BytesIO((RAW / "census_hist" / pdf).read_bytes())).pages[n - 1].extract_text() or "")
                  .replace("/leaderdash", "").replace("†", ""))


m = re.search(r"Dawson County ((?:\d{1,3} \d{3} ){6})", page("cph-2-29.pdf", 18))
vals = [int(a + b) for a, b in re.findall(r"(\d{1,3}) (\d{3})", m.group(1))]
for y, v in zip((1990, 1980, 1970, 1960, 1950, 1940), vals):
    check(f"Dawson County {y}", d[("Dawson County", y)]["population"], v)
m = re.search(r"Lexington city (\d) (\d{3}) (\d) (\d{3}) (\d) (\d{3}) ", page("cph-2-29.pdf", 37))
g = m.groups()
for i, y in enumerate((1990, 1980, 1970)):
    check(f"Lexington city {y}", d[("Lexington city", y)]["population"], int(g[2 * i] + g[2 * i + 1]))
m = re.search(r"Lexington city (\d{3}) ", page("cp-1-29.pdf", 56))
check("Lexington Hispanic origin 1990", d[("Lexington city", 1990)]["hispanic_or_latino"], int(m.group(1)))
m = re.search(r"Lexington city (\d) (\d{3}) ", page("cp-1-29.pdf", 59))   # Table 12: White, not of Hispanic origin
note("Lexington 1990, White not of Hispanic origin (CP-1-29 Table 12)", int(m.group(1) + m.group(2)))
for f in glob.glob(str(RAW / "census_api" / "20*_dec_*.json")):
    rows = json.load(open(f))
    r = dict(zip(rows[0], rows[1]))
    geo = "Lexington city" if "place" in r else "Dawson County"
    y = int(re.search(r"/(20\d\d)_dec", f).group(1))
    tot = next(v for k, v in r.items() if k in ("P001001", "P1_001N"))
    his = next(v for k, v in r.items() if k in ("P004002", "P004003", "P2_002N"))
    check(f"{geo} {y} total", d[(geo, y)]["population"], tot)
    check(f"{geo} {y} Hispanic", d[(geo, y)]["hispanic_or_latino"], his)


def pop(geo, y):
    return int(d[(geo, y)]["population"])


check("Lexington growth 1990 to 2000, %", round(100 * (pop("Lexington city", 2000) / pop("Lexington city", 1990) - 1), 1), 51.7)
check("Dawson County growth 1990 to 2000, %", round(100 * (pop("Dawson County", 2000) / pop("Dawson County", 1990) - 1), 1), 22.2)
check("Lexington change 1980 to 1990, %", round(100 * (pop("Lexington city", 1990) / pop("Lexington city", 1980) - 1), 1), -6.2)
check("Dawson County change 1980 to 1990, %", round(100 * (pop("Dawson County", 1990) / pop("Dawson County", 1980) - 1), 1), -10.6)
for y, want in ((1990, 5.0), (2000, 51.2), (2010, 60.4), (2020, 65.2)):
    r = d[("Lexington city", y)]
    check(f"Lexington Hispanic share {y}, %", round(100 * int(r["hispanic_or_latino"]) / int(r["population"]), 1), want)

# ---- ACS, raw JSON against processed, then the shares in the comparison chart
acs = read_csv("acs_2020_2024.csv")
rawacs = {}
for f in glob.glob(str(RAW / "census_api" / "2024_acs_acs5_b*.json")):
    rows = json.load(open(f))
    r = dict(zip(rows[0], rows[1]))
    geo = "Lexington city" if "place" in r else "Dawson County" if "county" in r else "Nebraska" if "state" in r else "United States"
    rawacs.setdefault(geo, {}).update(r)
diff = sum(1 for r in acs if rawacs[r["geography"]][r["variable"] + "E"] != r["estimate"]
           or rawacs[r["geography"]][r["variable"] + "M"] != r["margin_of_error_90"])
check("ACS processed values that differ from raw", diff, 0)
A = {(r["geography"], r["variable"]): float(r["estimate"]) for r in acs}
want = {"Lexington city": (42, 69, 43, 14, 57), "Dawson County": (23, 37, 26, 11, 66),
        "Nebraska": (8, 13, 10, 11, 67), "United States": (14, 22, 10, 12, 65)}
for geo, w in want.items():
    got = (100 * A[(geo, "B05002_013")] / A[(geo, "B05002_001")],
           100 - 100 * A[(geo, "C16001_002")] / A[(geo, "C16001_001")],
           100 * (A[(geo, "C24030_007")] + A[(geo, "C24030_034")]) / A[(geo, "C24030_001")],
           100 * A[(geo, "B17001_002")] / A[(geo, "B17001_001")],
           100 * A[(geo, "B25003_002")] / A[(geo, "B25003_001")])
    for lab, gv, wv in zip(("foreign born", "language other than English", "manufacturing", "poverty", "homeowners"), got, w):
        check(f"{geo} {lab}, %", round(gv), wv)
lx = "Lexington city"
note("Lexington foreign born from Latin America, % of foreign born", round(100 * A[(lx, "B05006_139")] / A[(lx, "B05006_001")]))
note("Lexington foreign born from Africa, % of foreign born", round(100 * A[(lx, "B05006_095")] / A[(lx, "B05006_001")]))
note("Lexington born in Africa, estimate", int(A[(lx, "B05006_095")]))

# ---- Cattle, raw TSV against processed
rows = [l.rstrip("\n").split("\t") for l in open(RAW / "nass" / "cattle_national.tsv")]
h = {n: i for i, n in enumerate(rows[0])}
inv = {int(r["year"]): int(r["head"]) for r in read_csv("cattle_inventory_jan1.csv")}
rawinv = {int(r[h["YEAR"]]): int(r[h["VALUE"]].replace(",", "")) for r in rows[1:]
          if r[h["SHORT_DESC"]] == "CATTLE, INCL CALVES - INVENTORY" and r[h["REFERENCE_PERIOD_DESC"]] == "FIRST OF JAN"}
check("cattle inventory years that differ from raw", sum(1 for y in inv if rawinv.get(y) != inv[y]) + abs(len(inv) - len(rawinv)), 0)
check("cattle and calves, January 1, 2026", inv[2026], 86155300)
check("last year the herd was smaller than 2026", max(y for y in inv if y < 2026 and inv[y] < inv[2026]), 1951)
peak = max(inv, key=inv.get)
check("peak year", peak, 1975)
check("2026 against the peak, %", round(100 * (inv[2026] / inv[peak] - 1), 1), -34.7)
pr = {(int(r["year"]), int(r["month"])): float(r["dollars_per_cwt"]) for r in read_csv("steer_heifer_price_received_monthly.csv")}
hi = max(pr, key=pr.get)
check("record steer and heifer price is June 2026", hi[0] * 100 + hi[1], 202606)
check("price January 2020, $ per 100 pounds", pr[(2020, 1)], 125)
check("price June 2026", pr[hi], 258)
check("price August 2026", pr[(2026, 8)], 234)
check("price January 2026, the month the plant closed", pr[(2026, 1)], 233)
check("price change January 2020 to January 2026, %", round(100 * (pr[(2026, 1)] / pr[(2020, 1)] - 1)), 86)
check("price change January 2020 to June 2026, %", round(100 * (pr[hi] / pr[(2020, 1)] - 1)), 106)
ppi = {(int(r["year"]), int(r["month"])): float(r["index_1982_100"]) for r in read_csv("ppi_slaughter_cattle.csv")}
note("cross-check, BLS PPI slaughter cattle, January 2020 to June 2026, %", round(100 * (ppi[(2026, 6)] / ppi[(2020, 1)] - 1)))

# ---- Tyson beef segment, typed in from filings
tyson = PROC.parent / "manual" / "tyson_beef_segment.csv"
if tyson.exists():
    import importlib
    check("Tyson figures not found on the beef rows of the SEC release cited", importlib.import_module("05_fetch_tyson").verify(), 0)
    for r in csv.DictReader(open(tyson)):
        note(f"Tyson beef FY{r['fiscal_year']} (typed from {r['source']})",
             f"sales {r['sales_musd']}, operating income {r['operating_income_musd']}, adjusted {r['adjusted_operating_income_musd']}")
else:
    note("Tyson beef segment", "not entered yet")

print(f"\n{bad} mismatches")
sys.exit(1 if bad else 0)
