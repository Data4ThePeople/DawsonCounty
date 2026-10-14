# Dawson County, Nebraska, and the Lexington beef plant

Data, code and charts behind the Data 4 The People post
[The Data Led Us to Lexington](https://www.data4thepeople.com/p/lexington-tyson-plant-closure)
(October 14, 2026).

## What is here

- `DATASETS.md`: every dataset used, where it comes from, and its limits.
- `scripts/`: the code. `02` to `05` fetch the data, `charts.py` draws the
  charts, and `tieout.py` recomputes every number in the charts and the post
  from the raw files.
- `data/processed/`: the cleaned data behind each chart.
- `data/manual/`: Tyson beef segment figures typed from its SEC filings and
  checked by `05_fetch_tyson.py`.
- `charts/`: the charts.
- `posts/lexington-tyson-plant-closure/`: the post and its images.
- `research/source-check.md`: a fact-by-fact check of what we took from news
  reports, Tyson's filings and the 1997 study.
- `research/first-pull.md`: early notes, kept as a record. Several facts in it
  were later corrected; `source-check.md` has the corrections.

## Running it

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/02_fetch_census.py
.venv/bin/python scripts/03_fetch_bls.py
.venv/bin/python scripts/04_fetch_cattle.py
.venv/bin/python scripts/05_fetch_tyson.py
.venv/bin/python scripts/charts.py
.venv/bin/python scripts/tieout.py
```

Set three environment variables first: `CENSUS_API_KEY` and `BLS_API_KEY`
(both free), and `D4TP_CONTACT_EMAIL`, an email address sent in the
User-Agent header of each request. Raw downloads go to `data/raw/`, which is
not in the repo.
