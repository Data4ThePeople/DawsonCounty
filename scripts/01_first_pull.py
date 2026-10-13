import sys, os, json, urllib.request, urllib.parse
sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import load_env, get_key
load_env()
CK = get_key("CENSUS_API_KEY"); BK = get_key("BLS_API_KEY")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) D4TP research"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()

def census(path, vars_, geo):
    url = f"https://api.census.gov/data/{path}?get={','.join(vars_)}&{geo}&key={CK}"
    try:
        rows = json.loads(get(url))
        return dict(zip(rows[0], rows[1]))
    except Exception as e:
        return {"error": str(e)[:200]}

GEOS = {
    "Lexington city": "for=place:26910&in=state:31",
    "Dawson County": "for=county:047&in=state:31",
    "Nebraska": "for=state:31",
    "US": "for=us:1",
}
B = ["B01003_001E","B03003_003E","B05002_013E","B05002_001E","B19013_001E","B17001_001E","B17001_002E",
     "C16001_001E","C16001_002E","B25003_001E","B25003_002E","B25077_001E","B25064_001E","B01002_001E",
     "B02001_003E","B05001_006E","B25001_001E","B25002_003E"]
DP = ["DP03_0032E","DP03_0035E","DP03_0035PE","DP03_0033E","DP03_0033PE","DP03_0025E"]
for yr in ("2024",):
    print(f"=== ACS 5-year ending {yr} ===")
    for name, geo in GEOS.items():
        d = census(f"{yr}/acs/acs5", B, geo)
        p = census(f"{yr}/acs/acs5/profile", DP, geo)
        print(name, json.dumps(d), json.dumps(p))

print("=== Decennial ===")
for name, geo in list(GEOS.items())[:2]:
    print(name, "2020", census("2020/dec/pl", ["P1_001N","P2_002N","P2_005N","P2_006N"], geo))
    print(name, "2010", census("2010/dec/sf1", ["P001001","P004003","P005003","P005004"], geo))
    print(name, "2000", census("2000/dec/sf1", ["P001001","P004002","P004005","P004006"], geo))

print("=== LAUS Dawson County ===")
ids = [f"LAUCN31047000000000{n}" for n in (3,4,5,6)]
body = json.dumps({"seriesid": ids, "startyear": "2024", "endyear": "2026", "registrationkey": BK}).encode()
req = urllib.request.Request("https://api.bls.gov/publicAPI/v2/timeseries/data/", data=body,
                             headers={"Content-Type": "application/json", **UA})
res = json.loads(urllib.request.urlopen(req, timeout=60).read())
tab = {}
for s in res.get("Results", {}).get("series", []):
    for o in s["data"]:
        tab.setdefault((o["year"], o["period"]), {})[s["seriesID"][-1]] = o["value"] + ("p" if any(f.get("code")=="P" for f in o.get("footnotes",[]) if f) else "")
print("period  rate unemployed employed laborforce")
for k in sorted(tab):
    v = tab[k]; print(k[0], k[1], v.get("3"), v.get("4"), v.get("5"), v.get("6"))
print(res.get("message"))

print("=== QCEW Dawson County ===")
import csv, io
for yr, q in (("2019","1"),("2025","1"),("2025","3"),("2025","4"),("2026","1")):
    try:
        txt = get(f"https://data.bls.gov/cew/data/api/{yr}/{q}/area/31047.csv")
    except Exception as e:
        print(yr, q, "error", str(e)[:100]); continue
    for r in csv.DictReader(io.StringIO(txt)):
        if r["industry_code"] in ("10","31-33","311","3116","311611") and r["own_code"] in ("0","5"):
            print(yr, "Q"+q, "own", r["own_code"], "ind", r["industry_code"], "discl", repr(r["disclosure_code"]),
                  "estabs", r["qtrly_estabs"], "emp", r["month1_emplvl"], r["month2_emplvl"], r["month3_emplvl"],
                  "wages", r["total_qtrly_wages"], "avg_wk", r["avg_wkly_wage"])
