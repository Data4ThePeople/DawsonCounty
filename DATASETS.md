# Datasets

One section per dataset, updated whenever we learn something new. The subject
is Lexington city (Census place 31-26910) and Dawson County, Nebraska (FIPS
31047), and the Tyson Foods beef plant at Lexington that closed January 20,
2026. Measured coverage figures are in section 9.

Facts that come from news reporting, company statements and the 1997 study
are not datasets. They are tracked one by one in `research/source-check.md`.

## 1. Decennial census counts (Census Bureau)

**What it is.** The count of residents on April 1 of each census year, and the
count who reported Hispanic or Latino origin.

**Where it comes from.** Three places, all the Census Bureau's own.
2000, 2010 and 2020: Census API (`2000/dec/sf1`, `2010/dec/sf1`,
`2020/dec/pl`), key required. 1940 to 1990 totals: the 1990 volume
*Population and Housing Unit Counts, Nebraska* (CPH-2-29), Table 3 for the
county and Table 8 for the city, a PDF on www2.census.gov. 1990 Hispanic
origin for the city: *General Population Characteristics, Nebraska*
(CP-1-29), Table 11. `scripts/02_fetch_census.py` reads the numbers out of the
PDF text and stops if a line is not found exactly once.

**Version and vintage.** Final counts. 1990 volumes printed 1992 and 1993.

**Coverage.** Dawson County 1940 to 2020. Lexington city 1970 to 2020 only:
the 1990 volume carries places back to 1970, and we have not found a Census
Bureau file for the city before that. City counts for 1890 to 1960 appear in
`research/first-pull.md` from Wikipedia's table and are not charted. Hispanic
origin: 1990 to 2020 for the city, 2000 to 2020 for the county.

**Changes over time.** A city's boundary moves when it annexes land, so the
city series is the city as it stood at each census. The 1990 volume notes
detachments from Lexington city to Lexington precinct in the 1980s. The Tyson
plant sits at the edge of town and the annexation history of that land is not
settled in our notes; workers who lived outside the city limits are in the
county count but not the city count. Hispanic origin has been asked of
everyone since 1980, with wording changes in 2000 and 2020. In 2000 and later
people could report more than one race; Hispanic origin is a separate question
and is not affected by that.

**Suppressed, censored or masked values.** None in 1940 to 2010 totals. The
2020 counts below state level carry deliberate statistical noise for privacy
(the Bureau's "disclosure avoidance system"). For a city of 10,000 the noise
in the total is small, a handful of people by the Bureau's published
accuracy measures, and larger in percentage terms for small groups.

**Missing data.** People the census could not reach are filled in from
neighbors' records ("imputation"). Rates for this city were not pulled.

**Revisions.** Counts are rarely revised. One case here: the 1990 volumes
print Lexington at 6,601, and the 2000 volume (PHC-3-29) prints the 1990
count as a revised 6,600. We use 6,601, as first published. The difference
does not change any rounded figure.

**Units and rounding.** Persons, unrounded.

**Known quirks.** Census counts miss people. The Bureau's own review found the
2020 census undercounted Hispanic residents nationally by about 5%. In a city
that is about two-thirds Hispanic this very likely matters, and it cuts toward
the true population being higher than the count.

**Uncertainty.** No margin of error is published for a count.

**License and attribution.** Public domain. Credit: U.S. Census Bureau.

## 2. American Community Survey 5-year, 2020-2024 (Census Bureau)

**What it is.** A sample survey pooled over five years. We use it for the
"town before the closure" table: foreign-born share, language spoken at home,
manufacturing share of workers, income, poverty, home ownership, home value,
median age, and region of birth of the foreign born.

**Where it comes from.** Census API, `2024/acs/acs5`, key required. Tables
B01003, B03003, B05002, B05001, B05006, B02001, C16001, B19013, B17001,
B25003, B25077, B25064, B01002, B25001, B25002, C24030. Estimates and margins
of error are both pulled.

**Version and vintage.** Released January 29, 2026. Interviews ran January
2020 through December 2024, so every answer predates the closure
announcement. Earlier 5-year files are not revised.

**Coverage.** All four geographies. Every value is a sample estimate.

**Changes over time.** Not used over time here. One period only.

**Suppressed, censored or masked values.** None of the cells we use is
suppressed.

**Missing data.** Missing answers are filled in by the Bureau before
tabulation. Allocation rates were not pulled.

**Revisions.** None.

**Units and rounding.** Persons, households, housing units, dollars, years.
Dollar figures are in 2024 dollars.

**Known quirks.** "Manufacturing" is where the person works by industry, not
where: a Lexington resident working at a plant in another town counts. It is
also every manufacturer, not Tyson alone. A 5-year file is an average over
five years, not a snapshot of 2024. The 2020 interviews were disrupted by the
pandemic.

**Uncertainty.** Margins of error are at 90% confidence and are wide for
Lexington. Foreign born: 4,531, give or take 524. Born in Africa: 829, give or
take 202. Below the poverty level: 1,488, give or take 507. Median household
income: $67,666, give or take $6,195. Vacant housing units: 122, give or take
84, which is too loose to use. The post should say "about" for every
Lexington share.

**License and attribution.** Public domain. Credit: U.S. Census Bureau,
American Community Survey 2020-2024.

## 3. Population estimates, vintage 2025 (Census Bureau)

**What it is.** The Bureau's estimate of residents on July 1 of each year,
2020 to 2025, for the county and the city.

**Where it comes from.** Flat files on www2.census.gov:
`co-est2025-alldata.csv` and `sub-est2025_31.csv`. No key.

**Version and vintage.** Vintage 2025. Each new vintage replaces every year
back to 2020.

**Coverage.** Not a count. County figures are built from births, deaths and
migration estimated from tax returns, Medicare and other records. City figures
split the county figure using housing unit changes. The latest date, July 1,
2025, is before the closure, so these files do not show its effect. The first
estimate that could is July 1, 2026, due in 2027.

**Known quirks.** The city's July 1, 2020 estimate (10,684; the April 1 base
is 10,682) is higher than the April 2020 count (10,348). We do not know why;
the county's base is within 5 of its count, so a boundary update for the city
is possible. Do not chart the two series as one line.

**Uncertainty.** No margin of error is published.

**License and attribution.** Public domain. Credit: U.S. Census Bureau.

## 4. Local Area Unemployment Statistics, LAUS (Bureau of Labor Statistics)

**What it is.** Monthly labor force, employed, unemployed and unemployment
rate for Dawson County residents. It counts people where they live, not where
they work.

**Where it comes from.** BLS API v2, key required. Series
`LAUCN310470000000003` (rate), `...04` (unemployed), `...05` (employed),
`...06` (labor force). Comparison rates: Nebraska `LAUST310000000000003` and
the U.S. `LNU04000000`. All not seasonally adjusted.

**Version and vintage.** Pulled October 13, 2026. January 1990 through August
2026.

**Coverage.** None of it is a direct measurement of the county. BLS has no
survey large enough for a county of 24,000. The figures are built from
unemployment insurance claims, employer job counts and Census data, then
scaled so counties add up to a state total that is itself a statistical model.
So 100% of the published values are model output in every month shown.

**Changes over time.** BLS has changed the method several times, including
redesigns in 2005 and 2015. Series are republished on the current method back to 1990, but a long
comparison is weaker than a recent one.

**Suppressed, censored or masked values.** None.

**Missing data.** October 2025 is blank in all four series, with the BLS note
"Data unavailable due to the 2025 lapse in appropriations." It is a gap, not a
zero. Charts leave a break there.

**Revisions.** The latest month is preliminary (August 2026 here) and is
revised the next month. Every spring BLS re-estimates the prior years. The
2026 figures in this project will change in spring 2027, and after a shock
this large the revision could be big.

**Units and rounding.** Persons, and a rate in percent to one decimal.

**Known quirks.** County series are not seasonally adjusted, so compare a
month with the same month a year earlier. A laid-off worker who moves away or
stops looking leaves the labor force and stops counting as unemployed, so the
rate can fall while the number of working residents keeps falling. The count
of employed residents is the steadier measure of the loss. Plant workers who
lived in other counties do not appear in Dawson County's figures at all.

**Uncertainty.** BLS publishes no error measure for county estimates.

**License and attribution.** Public domain. Credit: U.S. Bureau of Labor
Statistics, Local Area Unemployment Statistics.

## 5. Quarterly Census of Employment and Wages, QCEW (Bureau of Labor Statistics)

**What it is.** Jobs and wages reported by employers on their unemployment
insurance tax filings, by county and industry. It counts jobs where the job
is, so a worker who commutes into Dawson County is counted here.

**Where it comes from.** BLS open data files, one CSV per quarter:
`data.bls.gov/cew/data/api/<year>/<quarter>/area/31047.csv`. No key; needs a
browser-like user agent. 2014 Q1 through 2026 Q1.

**Version and vintage.** Pulled October 13, 2026. 2026 Q1 is the latest
quarter published. The open data files start in 2014; earlier years exist only
as very large national files, which we did not pull.

**Coverage.** A near-complete count, not a sample: about 95% of U.S. jobs are
covered. Not covered: most self-employed people, some farm workers, unpaid
family workers.

**Changes over time.** Industry codes were updated in 2017 and 2022. The
sectors we use (total, manufacturing, food manufacturing) did not change.

**Suppressed, censored or masked values.** BLS withholds a cell when it could
reveal one employer (`disclosure_code` N, printed as zeros). In Dawson County,
private food manufacturing (NAICS 311) is withheld in 48 of the 49 quarters
pulled. Total, private total and manufacturing are published in all 49. So
the plant's own job count cannot be read from BLS before 2026. The one
quarter that is published is 2026 Q1: 2,909 food manufacturing jobs in
January, 247 in February, 217 in March. We treat withheld cells as unknown,
never as zero.

**Missing data.** None in the published cells.

**Revisions.** Each quarter is revised in later releases for about a year.

**Units and rounding.** Jobs in each of the three months of the quarter, total
quarterly wages in dollars, average weekly wage in dollars.

**Known quirks.** A month's job count is everyone on a payroll in the pay
period that includes the 12th. The plant ran until January 20, 2026, so
January still shows it at close to full strength. News reports said nearly
300 workers were kept on after the closure; QCEW shows fewer in all of food
manufacturing, 247 in February and 217 in March. "Manufacturing" is every
manufacturer in the county, not Tyson alone. Wages include bonuses and
severance in the quarter they are paid, which can lift the average weekly
wage in a closing quarter. Wages exclude benefits.

**Uncertainty.** No sampling error. Reporting errors by employers exist and
are not measured.

**License and attribution.** Public domain. Credit: U.S. Bureau of Labor
Statistics, Quarterly Census of Employment and Wages.

## 6. Cattle inventory and prices received (USDA National Agricultural Statistics Service)

**What it is.** Two national series. (a) All cattle and calves in the United
States on January 1, 1867 to 2026. (b) The average price producers received
for steers and heifers weighing 500 pounds or more, in dollars per hundred
pounds of live weight, monthly, 1953 to August 2026. Steers and heifers are
the animals a beef plant like Lexington's buys.

**Where it comes from.** The Quick Stats bulk file
`qs.animals_products_<date>.txt.gz` at www.nass.usda.gov/datasets (about 460
MB, no key). `scripts/04_fetch_cattle.py` streams it and keeps national survey
rows for cattle inventory and cattle prices in `data/raw/nass/`. Items:
`CATTLE, INCL CALVES - INVENTORY` (reference period FIRST OF JAN) and
`CATTLE, STEERS & HEIFERS, GE 500 LBS - PRICE RECEIVED, MEASURED IN $ / CWT`.

**Version and vintage.** File dated October 13, 2026. The January 1, 2026
inventory was published January 30, 2026.

**Coverage.** The inventory is a survey estimate from a sample of producers,
not a count of animals. Prices are survey and market-report based. Every year
1867 to 2026 has a January figure; none is missing.

**Changes over time.** Early inventory figures (before the 1920s) are
historical reconstructions. Survey methods changed many times over 160 years.
We show 1950 on. The price series is an average over all grades and regions.

**Suppressed, censored or masked values.** None at the national level.

**Missing data.** None in the January series. A July 1 count also exists but
was skipped in some years; we do not use it.

**Revisions.** The prior year's inventory is revised in each January report,
and several years are revised after each five-year Census of Agriculture.
Monthly prices are preliminary for about two months.

**Units and rounding.** Head of cattle, published to the nearest hundred in
recent years and the nearest thousand earlier. Dollars per hundred pounds, to
the dollar in recent years. Prices are not adjusted for inflation.

**Known quirks.** The price is what ranchers and feedlots were paid on
average, not what Tyson paid. It tracks the cost of the packer's main input;
it says nothing by itself about the price packers got for beef, so it is one
side of the packer's margin. A second measure, the BLS Producer Price Index
for slaughter cattle (`WPU0131`, 1982 = 100), is pulled as a cross-check and
is not charted. The June 2026 price is the highest in the series only before
inflation: adjusted with the CPI, prices in the 1970s were higher (found by
the independent tie-out).

**Uncertainty.** NASS publishes survey reliability measures in the Cattle
report. We did not pull those tables, so we do not state an error range.

**License and attribution.** Public domain. Credit: USDA National
Agricultural Statistics Service.

## 7. Tyson Foods financial reports (Tyson Foods, Inc.)

**What it is.** Beef segment sales and operating income or loss by fiscal
year, from the company's annual reports (Form 10-K) and quarterly earnings
releases.

**Where it comes from.** SEC EDGAR (CIK 100493) and ir.tyson.com. Typed in by
hand from the filings into `data/manual/tyson_beef_segment.csv`, each row
with the document and table it came from.

**Version and vintage.** As filed. Tyson's fiscal year ends on the Saturday
closest to September 30, so fiscal 2025 ran from late September 2024 to late
September 2025.

**Changes over time.** Tyson has changed how it defines segments, and it
restates prior years when it does.

**Known quirks.** There are two versions of every profit figure. The reported
(GAAP) number includes one-time items such as legal settlements and write-offs
of goodwill. The "adjusted" number is the company's own, with those items
taken out. Outlets quote one or the other without saying which, which is why
the fiscal 2025 beef loss appears as both about $1.1 billion and about $0.4
billion in the reporting. The post must say which one it uses. A segment
result covers every Tyson beef plant, not Lexington. Tyson does not publish
results by plant.

**Uncertainty.** Audited annual figures. The adjusted figures are not audited.

**License and attribution.** Public filings. Credit: Tyson Foods, Inc., Form
10-K and earnings releases.

## 8. Single reported figures

- **WARN notice.** 3,212 positions at the Lexington plant, as cited by the
  University of Nebraska study from the notice Tyson filed. It is the employer's count
  of affected positions on the filing date, not an average headcount. The
  governor said fewer shifts were running than the figure implies.
- **Lexington Public Schools enrollment.** 3,172 before and 2,877 in fall
  2026, as reported by Nebraska Public Media from the district. Not yet
  checked against Nebraska Department of Education files.
- **Plant capacity and throughput.** About 5,000 head a day capacity; 3,600 to
  3,700 head a day in practice (trade press). Not from a public dataset.
- **UNL impact study.** 7,003 jobs statewide, $530 million in labor income.
  These are projections from an economic model, made in December 2025, not
  measurements.

## 9. Coverage check

Measured from the files in `data/`, October 13, 2026.

| Source | Direct measurement | Modeled or filled by the publisher | Withheld or blank |
|---|---|---|---|
| Decennial counts | A full count each census | 2020 has privacy noise added | None |
| ACS 2020-2024 | None: a sample | All values are sample estimates with margins | None used |
| Population estimates | None | 100% estimated from records | None |
| LAUS, 440 months | None for a county | 100% model-based | 1 month blank (October 2025); 1 preliminary (August 2026) |
| QCEW total, private, manufacturing | 49 of 49 quarters | None | None |
| QCEW food manufacturing | 1 of 49 quarters | None | 48 of 49 withheld |
| Cattle inventory, 1950 to 2026 | None: a sample survey | All values are survey estimates | None |

What this means for the post:

- The county unemployment rate is a model, in every month. The jobs count
  from QCEW is the stronger number and should carry the "what happened"
  claim, with the rate as the second measure.
- BLS cannot show the plant by itself except in the quarter it closed.
- Every Lexington share from the ACS is "about".
- No public dataset here reaches past August 2026, and the population effect
  of the closure is not in any Census file yet.
