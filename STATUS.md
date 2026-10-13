# Status

Project: DawsonCounty
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: lexington-tyson-plant-closure
Step: 2a
Since: 2026-10-13

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-10-13 | Eight charts; Claude's tie-out clean; independent tie-out by a fresh agent done on charts 01 to 07; source check of reported facts done |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-10-13 Step 1 opened. Topic: the story of Lexington and Dawson County,
  Nebraska, and the Tyson beef plant closure. Eric's outline: the history of
  the town; the metrics on the town (population and so on); when Tyson came
  and what it meant to the town; why they closed and the rationale they gave.
  Target publish date: October 14, 2026.
- 2026-10-13 First pull carried over from a session run in the
  AffordableHousing project: research/first-pull.md (history, metrics, the
  plant's arrival, the closure, what has happened since, sources, and a list
  of what is not verified) and scripts/01_first_pull.py (Census ACS and
  decennial, BLS LAUS and QCEW). The script was re-run from this project and
  reproduced the earlier figures. DATASETS.md is not written yet and comes
  before any chart. Nothing in AffordableHousing was changed.
- 2026-10-13 Plan approved by Eric, with one addition from him: a chart from
  public data on cattle prices or head count in the section on Tyson's
  losses. Built as chart 07: the January 1 herd (USDA) beside the price paid
  for steers and heifers in dollars per 100 pounds (USDA). Dollars were chosen
  over the BLS price index because they read more plainly; the index is kept
  as a cross-check.
- 2026-10-13 DATASETS.md written before any chart. Fetch scripts 02 to 04
  replace the first-pull script. Seven charts in charts/. Claude's tie-out
  (scripts/tieout.py) is clean. New from the pull: Lexington was 5% Hispanic
  in 1990 (329 of 6,601, from the 1990 census volume); BLS published the
  county's food manufacturing jobs for one quarter only, 2,909 in January
  2026 and 217 in March; the herd is the smallest since 1951; the steer and
  heifer price hit a record $258 in June 2026. City counts before 1970 are
  not charted because no Census Bureau file was found for them.
- 2026-10-13 Running: a source check of every fact taken from news reports
  (research/source-check.md) and the independent tie-out by a fresh agent.
  The Tyson beef segment chart waits on figures from the filings.
- 2026-10-13 Source check back (research/source-check.md). Eleven facts in
  the first pull corrected, among them: Tyson's November 21, 2025 release
  gives one reason only, to "right size its beef business", and no reason for
  choosing Lexington; the January 20 date is from the WARN notice; turnover of
  250% was over the first 21 months, not a yearly average; school enrollment
  rose 44% from 1990 to 1995, not 50%; the 1,200 to 1,300 workers was the 1988
  projection; the combine plant closed in 1985; the county was organized in
  1871 and the town platted in 1873. Not confirmed: the terms of the city tax
  deal, the plant's hourly pay, and several dates that rest on one secondary
  source. No buyer for the plant reported through October 13, 2026.
- 2026-10-13 Tyson beef segment figures typed from the year-end releases on
  SEC EDGAR and checked by script against the saved releases
  (scripts/05_fetch_tyson.py). Chart 08 built. Tyson changed its segment
  reporting in February 2026, so its fiscal 2026 guidance ($250 to $500
  million in February, $625 to $775 million by September) is not on the same
  basis as the $1.135 billion fiscal 2025 loss.
- 2026-10-13 Independent tie-out by a fresh agent back: every number on
  charts 01 to 07 reproduced from its own pulls, zero numeric differences.
  Fixed from its findings: the Nebraska and U.S. lines on chart 03 now break
  at October 2025; chart 07 no longer says "on record" without "before
  inflation", measures the price rise to the closure month (86%) and was
  renamed; chart 01's title states the census change without tying it to the
  plant; chart 06 says the shares are approximate; three DATASETS.md
  statements corrected (the 1990 city count was later revised to 6,600; the
  2020 estimates base; the retained-worker count). Not covered by the
  independent agent because they came after it: chart 08 and the reworded
  titles. Claude's own tie-out is clean on the final build.

- 2026-10-13 Chart 02 redrawn at Eric's request as a line on a time axis with
  a marker at November 1990, when the plant opened, so the share before and
  after can be read. Eric wants to offer the 1997 study's findings as a data
  point, not proof, in the debate over whether immigrants take jobs
  native-born workers do not want, tying back to his earlier reporting. What
  the study does and does not show on that is at the end of
  research/source-check.md.
- 2026-10-13 Earlier post to tie back to, given by Eric: "The Men Who
  Vanished" (August 30, 2026),
  https://www.data4thepeople.com/p/the-men-who-vanished. Read through the
  fetch tool as a summary, not word for word. Its claim is that native-born
  men did not take the jobs foreign-born men left, not that they did not want
  them; it calls the question "a live argument, not settled science." Link it
  at 2e.
- 2026-10-13 For step 2a, from Eric: link the 1997 Gouveia and Stull study
  directly in the body of the post, since much of the data comes from it.
  Link: https://jsri.msu.edu/upload/research-reports/rr26.pdf. Backup record
  if that file moves: https://eric.ed.gov/?id=ED414105.
- 2026-10-13 Step 1 confirmed by Eric. Not covered by the independent agent,
  because they came after it: chart 08 (Tyson beef segment, checked by script
  against the SEC releases), the reworded titles on charts 01, 06 and 07, and
  the redrawn chart 02. Claude's own tie-out is clean on the final build.
  Still open and carried into the post's limits: the terms of the city tax
  deal, the plant's hourly pay, several dates that rest on one secondary
  source, and where the workers went after the closure. Next: 2a, once Eric
  gives the slug and his draft.
- 2026-10-13 Step 2a opened. Slug: lexington-tyson-plant-closure. posts/lexington-tyson-plant-closure/POST.md created from the template; waiting for Eric's draft. Charts stay in charts/ until the draft sets their order.
- 2026-10-13 Step 2a: Eric's intro placed verbatim in POST.md. At his direction the body after it is Claude's, built on the six-step sequence, with all eight charts placed and numbered in order of appearance, the 1997 study linked at its first use, the tie-back to "The Men Who Vanished" framed as a data point, and a limits section. The intro's figures were checked against the Rentals Within Reach data. Proposed edits to Eric's prose sent as a numbered list; none applied. Title, subtitle and closing are Eric's to write.
- 2026-10-13 Step 2a: Eric accepted all 8 proposed edits and gave the Rentals Within Reach link; applied to POST.md.
