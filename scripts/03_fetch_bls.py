"""BLS pulls for Dawson County, Nebraska.

- LAUS: unemployment rate, unemployed, employed, labor force, monthly from 1990, not seasonally
  adjusted, counted where people live. Nebraska and U.S. rates for comparison.
- QCEW: jobs counted where the job is, quarterly from 2014 Q1 (the first quarter the open data
  files carry), all ownerships and private, total, manufacturing and food manufacturing.
"""
import csv
import io
import sys
import urllib.error

from common import AREA, RAW, bls_series, cached, write_csv

LAUS = {f"LAUCN{AREA}0000000003": "unemployment_rate", f"LAUCN{AREA}0000000004": "unemployed",
        f"LAUCN{AREA}0000000005": "employed", f"LAUCN{AREA}0000000006": "labor_force"}
COMPARE = {"LAUST310000000000003": "Nebraska", "LNU04000000": "United States"}

# own_code, industry_code: label
QCEW = {("0", "10"): "all jobs", ("5", "10"): "private jobs", ("5", "31-33"): "private manufacturing",
        ("5", "311"): "private food manufacturing", ("5", "3116"): "private animal slaughtering and processing"}


def laus():
    got = bls_series(list(LAUS), 1990, 2026, "bls_laus")
    table = {}
    for sid, name in LAUS.items():
        for y, p, v, f in got[sid]:
            if p == "M13":
                continue
            row = table.setdefault((y, int(p[1:])), {})
            row[name] = "" if v in ("-", "") else v
            row["flag"] = row.get("flag", "") or ("preliminary" if "P" in f else "")
    names = list(LAUS.values())
    write_csv("laus_dawson_monthly.csv", ["year", "month"] + names + ["flag"],
              [(y, m, *[table[(y, m)].get(n, "") for n in names], table[(y, m)].get("flag", ""))
               for y, m in sorted(table)])
    cmp = bls_series(list(COMPARE), 1990, 2026, "bls_laus")
    rows = []
    for sid, name in COMPARE.items():
        rows += [(name, y, int(p[1:]), v, "preliminary" if "P" in f else "")
                 for y, p, v, f in cmp[sid] if p != "M13" and v not in ("-", "")]
    write_csv("unemployment_rate_compare.csv", ["geography", "year", "month", "unemployment_rate", "flag"], rows)


def qcew():
    rows, seen = [], set()
    for y in range(2014, 2027):
        for q in (1, 2, 3, 4):
            try:
                txt = cached(RAW / "bls_qcew" / f"{y}_q{q}_{AREA}.csv",
                             f"https://data.bls.gov/cew/data/api/{y}/{q}/area/{AREA}.csv", tries=2).decode()
            except urllib.error.HTTPError as e:
                if e.code == 404 and y >= 2026:
                    continue          # not published yet
                raise
            for r in csv.DictReader(io.StringIO(txt)):
                k = (r["own_code"], r["industry_code"])
                if k not in QCEW or r["agglvl_code"] not in ("70", "71", "73", "74", "75"):
                    continue
                key = (y, q, k)
                if key in seen:
                    sys.exit(f"duplicate key {key}")
                seen.add(key)
                hidden = r["disclosure_code"].strip() == "N"
                rows.append((y, q, QCEW[k], r["own_code"], r["industry_code"], r["qtrly_estabs"],
                             *(["", "", "", "", ""] if hidden else
                               [r["month1_emplvl"], r["month2_emplvl"], r["month3_emplvl"],
                                r["total_qtrly_wages"], r["avg_wkly_wage"]]),
                             "withheld" if hidden else ""))
    write_csv("qcew_dawson_quarterly.csv",
              ["year", "quarter", "series", "own_code", "industry_code", "establishments", "month1_jobs",
               "month2_jobs", "month3_jobs", "total_quarterly_wages", "avg_weekly_wage", "flag"], rows)


if __name__ == "__main__":
    laus()
    qcew()
