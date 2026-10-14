"""Month-by-month cross-check of the unemployment data behind the long animation.

The charts use the BLS API pull (03_fetch_bls.py). This script checks every month from
January 2016 through the latest month against two other published copies:
- BLS's own bulk download, la.data.34.Nebraska (Dawson County and Nebraska), a separate
  file from the API.
- FRED, the St. Louis Fed's republication of the same BLS series (Dawson County rate, Nebraska
  rate, U.S. rate), as a third path for the rates.
It also recomputes the county rate from unemployed and labor force for each month.

    python scripts/06_crosscheck_laus.py
"""
import csv
import io
import sys

from common import AREA, RAW, cached, read_csv

START = (int(sys.argv[1]), 1) if len(sys.argv) > 1 else (2016, 1)
FLAT = "https://download.bls.gov/pub/time.series/la/la.data.34.Nebraska"
FRED = {"Dawson County": "NEDAWS7URN", "Nebraska": "NEURN", "United States": "UNRATENSA"}
COUNTY = {f"LAUCN{AREA}0000000003": "unemployment_rate", f"LAUCN{AREA}0000000004": "unemployed",
          f"LAUCN{AREA}0000000005": "employed", f"LAUCN{AREA}0000000006": "labor_force"}
STATE = "LAUST310000000000003"

bad = 0
checked = 0


def check(what, a, b):
    global bad, checked
    checked += 1
    if a != b:
        bad += 1
        print(f"DIFF {what}: API {a} vs other {b}")


def main():
    # ---- the API pull, as charted
    laus = {(int(r["year"]), int(r["month"])): r for r in read_csv("laus_dawson_monthly.csv")
            if (int(r["year"]), int(r["month"])) >= START}
    cmp = {(r["geography"], int(r["year"]), int(r["month"])): r["unemployment_rate"]
           for r in read_csv("unemployment_rate_compare.csv") if (int(r["year"]), int(r["month"])) >= START}
    months = sorted(laus)

    # ---- BLS bulk file
    flat = {}
    text = cached(RAW / "bls_laus_flat" / "la.data.34.Nebraska", FLAT).decode()
    for line in text.splitlines()[1:]:
        f = [x.strip() for x in line.split("\t")]
        if len(f) < 4 or not f[2].startswith("M") or f[2] == "M13":
            continue
        if f[0] in COUNTY or f[0] == STATE:
            flat[(f[0], int(f[1]), int(f[2][1:]))] = f[3]

    blank = []
    for ym in months:
        r = laus[ym]
        if r["unemployment_rate"] == "":
            blank.append(ym)
            for sid in COUNTY:
                if (sid, *ym) in flat and flat[(sid, *ym)] not in ("-", ""):
                    print(f"DIFF {ym}: blank in API, {flat[(sid, *ym)]} in bulk file")
                    globals()["bad"] += 1
            continue
        for sid, name in COUNTY.items():
            v = flat.get((sid, *ym))
            a = r[name]
            b = None if v is None else (f"{float(v):.1f}" if name == "unemployment_rate" else str(int(float(v))))
            check(f"county {name} {ym}", a if name != "unemployment_rate" else f"{float(a):.1f}", b)
        # the published rate should equal unemployed over labor force, rounded to one decimal
        calc = round(100 * int(r["unemployed"]) / int(r["labor_force"]) + 1e-9, 1)
        check(f"county rate recomputed {ym}", f"{float(r['unemployment_rate']):.1f}", f"{calc:.1f}")
        # unemployed plus employed should equal the labor force
        check(f"county employed + unemployed {ym}", int(r["labor_force"]), int(r["unemployed"]) + int(r["employed"]))
    for ym in months:
        a = cmp.get(("Nebraska", *ym))
        v = flat.get((STATE, *ym))
        if a in (None, "") and v in (None, "-"):
            continue
        check(f"Nebraska rate {ym}", a and f"{float(a):.1f}", v and f"{float(v):.1f}")

    # ---- FRED, rates only
    for geo, fid in FRED.items():
        raw = cached(RAW / "fred" / f"{fid}.csv", f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={fid}").decode()
        fr = {}
        for row in csv.reader(io.StringIO(raw)):
            if row and row[0][:4].isdigit() and row[1] not in ("", "."):
                fr[(int(row[0][:4]), int(row[0][5:7]))] = f"{float(row[1]):.1f}"
        for ym in months:
            a = laus[ym]["unemployment_rate"] if geo == "Dawson County" else cmp.get((geo, *ym))
            if a in (None, ""):
                if ym in fr:
                    print(f"NOTE {geo} {ym}: blank in API, {fr[ym]} on FRED")
                continue
            check(f"FRED {geo} rate {ym}", f"{float(a):.1f}", fr.get(ym))

    print(f"\nmonths {months[0]} to {months[-1]}: {len(months)}; blank months {blank}")
    print(f"{checked} comparisons, {bad} differences")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
