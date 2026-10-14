# Status

Project: DawsonCounty
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: lexington-tyson-plant-closure
Step: complete
Since: 2026-10-14

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-10-13 | Eight charts; Claude's tie-out clean; independent tie-out by a fresh agent done on charts 01 to 07; source check of reported facts done |
| 2a | Draft with brackets resolved | 2026-10-14 | Eric's intro and closing; body built on the six-step sequence at his direction; title, subtitle and closing header set |
| 2b | Eric's edit, Claude's look-over | 2026-10-14 | Look-over items 1 to 9 accepted; publish time 6:45 a.m. EDT |
| 2c | Slice markup | 2026-10-14 | Defaults; divider dots above the closing and above the limits; spacer and GitHub blurb at the end |
| 2d | Hero 1680x1080 + alt text | 2026-10-14 | Lexington water tower photo, Tony Webster, CC BY 2.0, credited at the end of the post |
| 2e | SEO | 2026-10-14 | Meta title, description, 8 keywords; Article schema, section Research |
| 2f | Pushed to Prismic (draft) | 2026-10-14 | Draft as9W-RcAADEAEMN8 in the Migration Release; section Research |
| 2g | Mailchimp teaser | 2026-10-14 | Eric's intro verbatim, no chart, link to the report |

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
- 2026-10-13 Step 2a: the mayor's quote cut at Eric's direction; it could not be confirmed on the page.
- 2026-10-13 Eric: do not use the food manufacturing job count (2,909 in January 2026) anywhere in the post, email or social copy, because BLS has published that cell in one quarter only. It stays in DATASETS.md as a record of what was found.
- 2026-10-13 Step 2a: at Eric's direction the "One more data point in a long debate" section is removed and the link to "The Men Who Vanished" now sits in one short paragraph after the study's hiring findings. Filler trimmed from Claude's sections only. Eric is fine with the length and will write the closing later. Trims to his intro proposed as a numbered list; none applied.
- 2026-10-13 Step 2a: Eric accepted all 4 trims to his intro; applied to POST.md. Waiting on his title, subtitle and closing.
- 2026-10-13 Step 2a: "with loads of subsidized housing" removed from the Greenlee County sentence at Eric's direction.
- 2026-10-13 Step 2a: Greenlee County now described as "home to a Freeport-McMoRan copper mine" (Eric accepted).
- 2026-10-14 Step 2a: Eric's closing placed verbatim in POST.md. Proposed edits sent as a numbered list; none applied. Still waiting on title and subtitle.
- 2026-10-14 Step 2a: Eric accepted closing edits 1 to 7; applied. JobsOhio aside kept at his direction and linked to his earlier post, https://www.data4thepeople.com/p/jobsohio-post. Waiting on title and subtitle.
- 2026-10-14 Step 2a: title and subtitle set at Eric's choice. Title: "The Data Led Us to Lexington." Subtitle: "Our rental affordability map pointed us to a county in Nebraska. A 1997 study had already told the first part of its story. We picked it back up the year the beef plant closed."
- 2026-10-14 Step 2a: subtitle's last sentence changed to "We brought it up to date the year the beef plant closed." at Eric's direction.
- 2026-10-14 Step 2a: at Eric's direction the closing now comes before "What this does not tell you", so the limits section ends the post.
- 2026-10-14 Step 2a: closing given the header "How we found this story" (Eric's choice).
- 2026-10-14 Step 2a confirmed by Eric. Next: 2b, Eric's edit and Claude's look-over.
- 2026-10-14 WARN notice linked in the post at Eric's request: Tyson's November 21, 2025 letter on the Nebraska Department of Labor WARN list, https://dol.nebraska.gov/webdocs/getfile/a16e7080-54f1-43f4-bbd7-f9011a5f3453 (3,212 positions, "on or around January 20, 2026", read directly this time). The same list has a January 21, 2026 Tyson extension notice for 294 positions.
- 2026-10-14 Tyson's extension notice (letter dated January 20, 2026, listed January 21) read and linked at Eric's request: https://dol.nebraska.gov/webdocs/getfile/7eb5ba08-b9ba-461f-8559-5a162f9fa4dd. The letter says "approximately 292" kept on; its table totals 294; the last group of 127 was to stay through July 24, 2026. Supports "about 290" and the July 24 date in the post.
- 2026-10-14 At Eric's request, a labor force sentence added after the employed-residents line (13,658 in August 2025 to 11,897 in August 2026, 1,761 fewer, 13%; August 2026 preliminary), linked to https://www.data4thepeople.com/p/five-takeaways-labor-force-decline.
- 2026-10-14 Chart 08 caption shortened at Eric's direction; the 13% labor force figure now sits only in the sentence after the chart.
- 2026-10-14 At Eric's direction the pay limit now gives the closest public measure: average annual pay for private manufacturing jobs in Dawson County, 2024, $54,247 ($1,043 a week), computed from the four QCEW quarters already pulled (total wages divided by average monthly jobs). 2024 chosen as the last full year before the closure was announced; 2025 Q4 pay jumped after the announcement. The plant was about 80% of county manufacturing jobs (3,212 of about 3,925, editorial calculation). The UNL modeled figure is left out. Kept in the limits section, not the body, at Eric's choice.
- 2026-10-14 Step 2b opened. Eric's edits are complete (among them: closing point 1 now ends on whether there are enough working-age people; "completed" changed to "continued"). Claude's look-over sent as a numbered list; none applied.
- 2026-10-14 Step 2b: Eric accepted look-over items 1 to 9; applied (cattle link now quotes Tyson's February 2026 investor call, the August 2026 quote moved to the Joslin sentence, AP claim linked, intro and closing wording). Publish time set to October 14, 2026, 6:45 a.m. EDT (time: 06:45:00-04:00). The closing's "Yesterday morning" holds only for an October 14 publish.
- 2026-10-14 Step 2b confirmed by Eric. Next: 2c, slice markup.
- 2026-10-14 Step 2c opened. Defaults kept (drop cap, 20px spacers before headings and after captions); no embeds, so no added spacers. One fence added: ::: divider above "How we found this story", where the article body ends. Convert-only run: 89 blocks, 8 images, all alt text under 500 characters; hero and hero_alt still missing (step 2d).
- 2026-10-14 Step 2c: at Eric's direction, divider dots also above "What this does not tell you", then a 20px spacer and a no-title blurb after the limits linking to the GitHub repo (https://github.com/Data4ThePeople/DawsonCounty). The repo is private, so the link will not open for readers until Eric makes it public.
- 2026-10-14 README.md added for readers who follow the GitHub link. scripts/common.py now falls back to environment variables when the central key helper is not present, so the scripts run outside this machine; tie-out still 0 mismatches. Repo made public at Eric's direction.
- 2026-10-14 Step 2c confirmed by Eric. Next: 2d, hero at 1680x1080.
- 2026-10-14 Step 2d opened. Eric asked for a real, openly licensed photo of Lexington, the plant or the old combine factory. Wikimedia Commons has none of the plant or the factory under an open license. Hero is Tony Webster's 2018 photo of the Lexington water tower (CC BY 2.0, https://commons.wikimedia.org/wiki/File:City_of_Lexington,_Nebraska_-_Water_Tower_(46537540401).jpg), cropped to 1680x1080 from the center; source kept as images/lexington-tyson-plant-closure-hero-source.jpg. hero_alt written (265 characters). The license requires credit, so an italic credit line was added at the end of the post.
- 2026-10-14 Step 2d confirmed by Eric. Step 2e opened. Eric gave no target searches given the 6:45 a.m. publish; Claude drafted meta title, description and eight keywords into the front matter for his review. Schema: Article, Data 4 Thought, house conventions. Earlier posts already linked in the body: Rentals Within Reach, The Men Who Vanished, JobsOhio, labor force decline.
- 2026-10-14 Step 2e confirmed by Eric. Step 2f opened.
- 2026-10-14 Step 2f: dry run clean (45 slices, 8 charts and the hero to upload, creates blog_post uid lexington-tyson-plant-closure). The live push was blocked by Claude Code's auto-mode permission check; Eric to run it with the ! prefix.
- 2026-10-14 Step 2f: Eric ran the push. All 8 charts and the hero uploaded; draft as9W-RcAADEAEMN8 created in the Migration Release (tags and author empty).
- 2026-10-14 After the push, at Eric's direction: "home of Lexington" added to "So today, we tell the story of Dawson County, Nebraska." The draft needs a re-push, which updates the same document.
- 2026-10-14 Re-pushed at Eric's request; draft as9W-RcAADEAEMN8 updated in the Migration Release.
- 2026-10-14 20px spacer added between the GitHub blurb and the photo credit at Eric's direction; re-pushed to the same draft.
- 2026-10-14 Section changed from Data 4 Thought to Research at Eric's direction (schema articleSection); re-pushed to the same draft.
- 2026-10-14 Step 2f confirmed by Eric. Step 2g opened: Eric wants his intro verbatim as the email body, no charts, then the link to the report.
- 2026-10-14 Step 2g: EMAIL.md drafted. Eric's intro verbatim (links kept as plain words, with a note to link Rentals Within Reach in Mailchimp), no chart, link to the report. Hero email JPG exported (175KB). Photo credit line included for the CC BY 2.0 license.
- 2026-10-14 Step 2g approved by Eric. Post lexington-tyson-plant-closure complete through 2g. Publishing in Prismic (tags, author, release) is Eric's.
- 2026-10-14 SOCIAL.md drafted (X single, optional 4-post X thread, LinkedIn with first-comment link, alt text). Animated unemployment chart built by scripts/animate.py: posts/lexington-tyson-plant-closure/social/unemployment-rate.gif, 8 seconds drawing in and a 5-second hold on the published chart.
- 2026-10-14 Ten-year unemployment animation, at Eric's request. Assessment: every month from January 1990 to August 2026 matches across the BLS API pull, BLS's bulk file la.data.34.Nebraska and FRED (4,390 comparisons, 0 differences; January 2016 onward, 1,270 comparisons, 0 differences), via scripts/06_crosscheck_laus.py. Built January 2016 to August 2026 as Eric capped it at ten years: static charts/09-unemployment-rate-since-2016.png and social/unemployment-rate-since-2016.gif. It shows two numbers not in the post, the county's 5.2% (May 2020) and the U.S. 14.4% (April 2020), so it waits on Eric before any social use. Tie-out covers the new figures; 0 mismatches.
