"""Tyson Foods year-end earnings releases from SEC EDGAR (exhibit 99.1 to each November 8-K).
The beef segment figures in data/manual/tyson_beef_segment.csv were typed from these; this script
saves the releases and stops if a typed figure is not on the beef rows of the release it cites.
Basis: as Tyson reported them before its February 2026 change in segment reporting."""
import csv
import html
import re
import sys

from common import RAW, ROOT, cached

BASE = "https://www.sec.gov/Archives/edgar/data/100493/"
DOCS = {2019: "000010049319000117/tsn2019q4exh-991.htm", 2020: "000010049320000131/tsn2020q4exh-991.htm",
        2021: "000010049321000121/tsn2021q4exh-991.htm", 2022: "000010049322000096/tsn2022q4exh-991.htm",
        2023: "000010049323000104/tsn2023q4exh-991.htm", 2024: "000010049324000118/tsn2024q4exh-991.htm",
        2025: "000010049325000094/tsn2025q4exh-991.htm"}


def beef_rows(year):
    t = cached(RAW / "tyson" / f"fy{year}_q4_release.htm", BASE + DOCS[year]).decode("utf-8", "replace")
    t = re.sub(r"[\s\xa0]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    return [re.sub(r"\(\s*([\d,]+)\s*\)", r"(\1)", t[m.start():m.start() + 110]) for m in re.finditer(r"\bBeef\b (?=[\$\(\d])", t)]


def shown(n):
    n = int(n)
    return f"({-n:,})" if n < 0 else f"{n:,}"


def verify():
    bad = 0
    for r in csv.DictReader(open(ROOT / "data" / "manual" / "tyson_beef_segment.csv")):
        y = int(r["fiscal_year"])
        rows = beef_rows(2021 if y == 2020 else y)      # 2020 is the restated figure in the 2021 release
        for col in ("sales_musd", "operating_income_musd", "adjusted_operating_income_musd"):
            ok = any(re.search(r"(?<![\d,])" + re.escape(shown(r[col])) + r"(?![\d,])", row) for row in rows)
            bad += not ok
            print(f"{'ok  ' if ok else 'FAIL'} FY{y} {col} {shown(r[col])}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if verify() else 0)
