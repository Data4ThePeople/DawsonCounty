"""U.S. cattle inventory and cattle prices.

Inventory and prices received: USDA NASS Quick Stats, read from the public bulk file
(qs.animals_products_<date>.txt.gz, about 460 MB, no key needed). The file is streamed and only
national survey rows for cattle inventory and cattle prices are kept, in data/raw/nass/.

Price index: BLS Producer Price Index, commodity series WPU0131 (slaughter cattle), monthly.
"""
import csv
import gzip
import io
import re
import sys
import urllib.request

from common import RAW, bls_series, get, user_agent, write_csv

KEEP = RAW / "nass" / "cattle_national.tsv"
INDEX = "https://www.nass.usda.gov/datasets/"


def fetch_nass():
    if KEEP.exists():
        return
    KEEP.parent.mkdir(parents=True, exist_ok=True)
    name = sorted(set(re.findall(r"qs\.animals_products_\d{8}\.txt\.gz", get(INDEX).decode())))[-1]
    req = urllib.request.Request(INDEX + name, headers={"User-Agent": user_agent()})
    n = kept = 0
    tmp = KEEP.with_suffix(".part")
    # Plain tab split: the file has stray NUL bytes that the csv module refuses, and no quoted fields.
    with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "w") as out:
        rd = io.TextIOWrapper(gzip.GzipFile(fileobj=r), encoding="utf-8", errors="replace", newline="")
        head = next(rd).rstrip("\r\n").split("\t")
        out.write("\t".join(head) + "\n")
        c = {h: i for i, h in enumerate(head)}
        for line in rd:
            n += 1
            row = line.replace("\x00", "").rstrip("\r\n").split("\t")
            if len(row) != len(head):
                continue
            if (row[c["COMMODITY_DESC"]] == "CATTLE" and row[c["AGG_LEVEL_DESC"]] == "NATIONAL"
                    and row[c["SOURCE_DESC"]] == "SURVEY"
                    and ("INVENTORY" in row[c["SHORT_DESC"]] or "PRICE RECEIVED" in row[c["SHORT_DESC"]])):
                out.write("\t".join(row) + "\n")
                kept += 1
    tmp.rename(KEEP)
    (KEEP.parent / "pulled.txt").write_text(f"{name}: {n} rows read, {kept} kept\n")
    print(name, n, "rows read,", kept, "kept")


def num(v):
    v = v.replace(",", "").strip()
    return float(v) if re.fullmatch(r"-?\d+(\.\d+)?", v) else None


def build():
    rows = list(csv.DictReader(open(KEEP, newline=""), delimiter="\t", quoting=csv.QUOTE_NONE))
    # January 1 inventory, all cattle and calves, and beef cows
    for desc, out in (("CATTLE, INCL CALVES - INVENTORY", "cattle_inventory_jan1.csv"),
                      ("CATTLE, COWS, BEEF - INVENTORY", "beef_cows_jan1.csv")):
        sel = [r for r in rows if r["SHORT_DESC"] == desc and r["REFERENCE_PERIOD_DESC"] == "FIRST OF JAN"
               and r["DOMAIN_DESC"] == "TOTAL" and r["FREQ_DESC"] == "POINT IN TIME"]
        by = {}
        for r in sel:
            y = int(r["YEAR"])
            if y in by:
                sys.exit(f"duplicate key {desc} {y}")
            by[y] = num(r["VALUE"])
        write_csv(out, ["year", "head"], [(y, int(by[y])) for y in sorted(by) if by[y] is not None])
    # Monthly price received by producers for steers and heifers 500 pounds and over, dollars per
    # hundredweight. These are the animals beef plants like Lexington's buy; the broader "cattle, GE 500
    # LBS" series also counts cull cows and bulls.
    desc = "CATTLE, STEERS & HEIFERS, GE 500 LBS - PRICE RECEIVED, MEASURED IN $ / CWT"
    mon = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}
    by = {}
    for r in rows:
        if r["SHORT_DESC"] == desc and r["FREQ_DESC"] == "MONTHLY" and r["REFERENCE_PERIOD_DESC"] in mon \
                and r["DOMAIN_DESC"] == "TOTAL":
            k = (int(r["YEAR"]), mon[r["REFERENCE_PERIOD_DESC"]])
            if k in by:
                sys.exit(f"duplicate key price {k}")
            by[k] = num(r["VALUE"])
    write_csv("steer_heifer_price_received_monthly.csv", ["year", "month", "dollars_per_cwt"],
              [(y, m, by[(y, m)]) for y, m in sorted(by) if by[(y, m)] is not None])
    print("price descriptions on file:", sorted({r["SHORT_DESC"] for r in rows if "PRICE" in r["SHORT_DESC"]}))

    ppi = bls_series(["WPU0131"], 1990, 2026, "bls_ppi")["WPU0131"]
    write_csv("ppi_slaughter_cattle.csv", ["year", "month", "index_1982_100", "footnotes"],
              [(y, int(p[1:]), v, f) for y, p, v, f in ppi if p != "M13" and v not in ("-", "")])


if __name__ == "__main__":
    fetch_nass()
    build()
