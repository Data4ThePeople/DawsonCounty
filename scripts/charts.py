"""Static charts for the post, dark house palette. Every number is read from data/processed at
render time; nothing is typed in. Output: charts/01-*.png onward."""
import datetime as dt
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from common import CHARTS, read_csv  # noqa: E402
from plot_style import (BLUE, GRAY, GRID, INK, INK_DIM, MAGENTA, MUTED, SURFACE, YELLOW,  # noqa: E402
                        credit, titleblock, use_house_style)

W, H = 10, 6.2
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def frame(top=0.80, bottom=0.13, left=0.08, right=0.95, h=H):
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    return fig, ax


def save(fig, name):
    CHARTS.mkdir(exist_ok=True)
    fig.savefig(CHARTS / name)
    plt.close(fig)
    print("wrote charts/" + name)


def thousands(ax, axis="y"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def pct(a, b):
    return 100 * (b - a) / a


# ---------------------------------------------------------------- 01 population
def population():
    d = read_csv("decennial_population.csv")
    co = {int(r["year"]): int(r["population"]) for r in d if r["geography"] == "Dawson County"}
    ci = {int(r["year"]): int(r["population"]) for r in d if r["geography"] == "Lexington city"}
    fig, ax = frame()
    for s, c in ((co, BLUE), (ci, YELLOW)):
        ax.plot(list(s), list(s.values()), color=c, lw=2.4, marker="o", ms=5.5)
        for y, v in s.items():
            low = y == 1990          # the line rises steeply after 1990, so that label sits under the point
            ax.annotate(f"{v:,}", (y, v), xytext=(0, -15 if low else 9), textcoords="offset points", ha="center",
                        color=c, fontsize=9)
    ax.text(1940, co[1940] - 2300, "Dawson County", color=BLUE, fontsize=12, fontweight="bold", ha="left")
    ax.text(1970, ci[1970] - 2600, "Lexington", color=YELLOW, fontsize=12, fontweight="bold", ha="left")
    for x, lab in ((1985, "1985: combine plant closes"), (1990.85, "1990: beef plant opens")):
        ax.axvline(x, color=MUTED, lw=1, ls=(0, (3, 3)))
    ax.text(1984.3, 13300, "1985: combine\nplant closes", color=INK_DIM, fontsize=9.5, ha="right", va="center")
    ax.text(1991.6, 13300, "1990: beef\nplant opens", color=INK_DIM, fontsize=9.5, ha="left", va="center")
    ax.set_ylim(0, 28000)
    ax.set_xlim(1936, 2024)
    ax.set_xticks(range(1940, 2021, 10))
    thousands(ax)
    titleblock(fig, "Lexington grew by half in the decade after the beef plant opened",
               f"Residents counted in each census. Lexington went from {ci[1990]:,} in 1990 to {ci[2000]:,} in 2000, "
               f"up {pct(ci[1990], ci[2000]):.0f}%.\nDawson County grew {pct(co[1990], co[2000]):.0f}%. "
               "Both have changed little since.")
    credit(fig, "Source: U.S. Census Bureau, decennial census. City counts are available from 1970.")
    save(fig, "01-population.png")


# ---------------------------------------------------------------- 02 Hispanic share
def hispanic():
    d = [r for r in read_csv("decennial_population.csv") if r["geography"] == "Lexington city" and r["hispanic_or_latino"]]
    ys = [int(r["year"]) for r in d]
    sh = [100 * int(r["hispanic_or_latino"]) / int(r["population"]) for r in d]
    fig, ax = frame(left=0.08)
    ax.bar([str(y) for y in ys], sh, color=YELLOW, width=0.55)
    for i, (r, v) in enumerate(zip(d, sh)):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", color=INK, fontsize=14, fontweight="bold")
        ax.text(i, v + 6.3, f"{int(r['hispanic_or_latino']):,} of {int(r['population']):,}", ha="center", color=INK_DIM, fontsize=9)
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis="x", labelsize=12)
    titleblock(fig, "Lexington went from 5% Hispanic to 65% in thirty years",
               "Share of Lexington residents who reported Hispanic or Latino origin in each census.\n"
               "The beef plant opened in November 1990, seven months after the 1990 census.")
    credit(fig, "Source: U.S. Census Bureau, decennial census.")
    save(fig, "02-hispanic-share.png")


# ---------------------------------------------------------------- LAUS helpers
def laus(start=(2024, 1)):
    rows = [r for r in read_csv("laus_dawson_monthly.csv") if (int(r["year"]), int(r["month"])) >= start]
    x = [dt.date(int(r["year"]), int(r["month"]), 1) for r in rows]
    return rows, x


def col(rows, name):
    return [float(r[name]) if r[name] != "" else float("nan") for r in rows]


def month_axis(ax, x):
    ax.set_xlim(x[0] - dt.timedelta(days=20), x[-1] + dt.timedelta(days=25))
    ticks = [d for d in x if d.month in (1, 7)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{MONTHS[d.month - 1]}\n{d.year}" if d.month == 1 else MONTHS[d.month - 1] for d in ticks])


def closure_line(ax, y, text="Plant closes\nJan. 20, 2026", ha="right"):
    c = dt.date(2026, 1, 20)
    ax.axvline(c, color=MUTED, lw=1, ls=(0, (3, 3)))
    ax.text(c - dt.timedelta(days=8) if ha == "right" else c + dt.timedelta(days=8), y, text, color=INK_DIM,
            fontsize=9.5, ha=ha, va="top")


def label(d):
    return f"{MONTHS[d.month - 1]} {d.year}"


# ---------------------------------------------------------------- 03 unemployment rate
def unemployment():
    rows, x = laus()
    rate = col(rows, "unemployment_rate")
    cmp = read_csv("unemployment_rate_compare.csv")
    fig, ax = frame()
    for geo, c in (("United States", GRAY), ("Nebraska", BLUE)):
        s = {dt.date(int(r["year"]), int(r["month"]), 1): float(r["unemployment_rate"]) for r in cmp if r["geography"] == geo}
        xs = [d for d in x if d in s]
        ax.plot(xs, [s[d] for d in xs], color=c, lw=1.8, ls=(0, (4, 2)) if c == GRAY else "-")
        ax.text(xs[-1] + dt.timedelta(days=12), s[xs[-1]], f"{s[xs[-1]]:.1f}%", color=c, fontsize=9.5, va="center")
        if geo == "United States":
            us_first = s[xs[0]]
    ax.plot(x, rate, color=YELLOW, lw=2.6)
    known = [(d, v) for d, v in zip(x, rate) if v == v]
    peak = max(known, key=lambda t: t[1])
    jan = dict(known)[dt.date(2026, 1, 1)]
    feb = dict(known)[dt.date(2026, 2, 1)]
    last = known[-1]
    for d, v, dx, dy, ha in ((dt.date(2026, 1, 1), jan, -10, -13, "right"), (dt.date(2026, 2, 1), feb, -8, 0, "right"),
                             (peak[0], peak[1], 0, 9, "center"), (last[0], last[1], 8, 0, "left")):
        ax.plot([d], [v], "o", color=YELLOW, ms=5.5)
        ax.annotate(f"{v:.1f}%", (d, v), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    color=YELLOW, fontsize=11, fontweight="bold")
    ax.text(dt.date(2024, 1, 15), 6.4, "Dawson County", color=YELLOW, fontsize=12, fontweight="bold")
    ax.text(dt.date(2024, 9, 1), 6.4, "Nebraska", color=BLUE, fontsize=12, fontweight="bold")
    ax.text(dt.date(2025, 2, 10), 6.4, "United States", color=GRAY, fontsize=12, fontweight="bold")
    ax.set_ylim(0, 24)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
    month_axis(ax, x)
    closure_line(ax, 23.2)
    prelim = [label(d) for r, d in zip(rows, x) if r["flag"]]
    titleblock(fig, f"Dawson County's unemployment rate went from {jan:.1f}% to {feb:.1f}% in one month",
               f"Unemployment rate by month, not seasonally adjusted. The county peaked at {peak[1]:.1f}% in {label(peak[0])} "
               f"and was {last[1]:.1f}% in {label(last[0])}.")
    credit(fig, "Source: U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics and Current Population Survey. County figures are\n"
                f"model-based estimates. October 2025 was not published. {', '.join(prelim)} is preliminary.")
    save(fig, "03-unemployment-rate.png")


# ---------------------------------------------------------------- 04 employed residents
def employed():
    rows, x = laus()
    emp, lf = col(rows, "employed"), col(rows, "labor_force")
    fig, ax = frame()
    ax.plot(x, lf, color=BLUE, lw=2.2)
    ax.plot(x, emp, color=YELLOW, lw=2.6)
    e, f = dict(zip(x, emp)), dict(zip(x, lf))
    a, b = dt.date(2025, 8, 1), x[-1]
    for s, c, dy in ((f, BLUE, 11), (e, YELLOW, -13)):
        for d in (a, b):
            ax.plot([d], [s[d]], "o", color=c, ms=5.5)
            ax.annotate(f"{s[d]:,.0f}", (d, s[d]), xytext=(0, dy), textcoords="offset points", ha="center",
                        color=c, fontsize=10.5, fontweight="bold")
    ax.text(dt.date(2024, 1, 10), 14500, "Labor force", color=BLUE, fontsize=12, fontweight="bold")
    ax.text(dt.date(2024, 1, 10), 12500, "Employed residents", color=YELLOW, fontsize=12, fontweight="bold")
    ax.set_ylim(8000, 15500)
    thousands(ax)
    month_axis(ax, x)
    closure_line(ax, 15300)
    titleblock(fig, f"Dawson County has {-pct(e[a], e[b]):.0f}% fewer employed residents than a year ago",
               f"Dawson County residents with a job fell {-pct(e[a], e[b]):.0f}% from {label(a)} to {label(b)}. The labor force, those working "
               f"or looking\nfor work, fell {-pct(f[a], f[b]):.0f}%. The axis starts at 8,000.")
    credit(fig, "Source: U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics. Not seasonally adjusted; model-based estimates.\n"
                f"October 2025 was not published. {label(b)} is preliminary.")
    save(fig, "04-employed-residents.png")


# ---------------------------------------------------------------- 05 jobs located in the county
def qcew_monthly(series):
    out = {}
    for r in read_csv("qcew_dawson_quarterly.csv"):
        if r["series"] == series and r["flag"] == "":
            for i in (1, 2, 3):
                out[dt.date(int(r["year"]), (int(r["quarter"]) - 1) * 3 + i, 1)] = int(r[f"month{i}_jobs"])
    return out


def jobs():
    fig, ax = frame()
    spec = (("all jobs", GRAY, (0, (4, 2)), "All jobs"), ("private jobs", BLUE, "-", "Private jobs"),
            ("private manufacturing", YELLOW, "-", "Manufacturing jobs"))
    a, b = dt.date(2025, 3, 1), dt.date(2026, 3, 1)
    chg = {}
    for name, c, ls, lab in spec:
        s = qcew_monthly(name)
        x = sorted(s)
        ax.plot(x, [s[d] for d in x], color=c, lw=2.2, ls=ls)
        ax.text(dt.date(2014, 2, 1), s[x[0]] + (1150 if name == "all jobs" else 420), lab, color=c, fontsize=12, fontweight="bold")
        for d, ha, dx in ((a, "right", -7), (b, "left", 7)):
            ax.plot([d], [s[d]], "o", color=c, ms=5)
            ax.annotate(f"{s[d]:,}", (d, s[d]), xytext=(dx, 13 if d == a else 0), textcoords="offset points", ha=ha,
                        va="center", color=c, fontsize=10, fontweight="bold")
        chg[name] = (s[a], s[b])
    ax.set_ylim(0, 13500)
    ax.set_xlim(dt.date(2013, 10, 1), dt.date(2027, 4, 1))
    ax.set_xticks([dt.date(y, 1, 1) for y in range(2014, 2027, 2)])
    ax.set_xticklabels([str(y) for y in range(2014, 2027, 2)])
    thousands(ax)
    m0, m1 = chg["private manufacturing"]
    p0, p1 = chg["private jobs"]
    titleblock(fig, f"Dawson County had {m0:,} manufacturing jobs in March 2025 and {m1:,} a year later",
               f"Jobs located in Dawson County, by month, January 2014 to March 2026. Manufacturing jobs fell {-pct(m0, m1):.0f}% "
               f"in a year\nand private jobs fell {-pct(p0, p1):.0f}%. Labeled points are March 2025 and March 2026.")
    credit(fig, "Source: U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages. Jobs are counted where the job is,\n"
                "not where the worker lives. Manufacturing is every manufacturer in the county.")
    save(fig, "05-jobs-in-county.png")


# ---------------------------------------------------------------- 06 the town before the closure
def acs_share(rows, geo, num, den):
    g = {r["variable"]: float(r["estimate"]) for r in rows if r["geography"] == geo}
    n = sum(g[v] for v in num) if isinstance(num, tuple) else g[num]
    return 100 * n / g[den]


def before():
    rows = read_csv("acs_2020_2024.csv")
    geos = ["Lexington city", "Dawson County", "Nebraska", "United States"]
    names = ["Lexington", "Dawson County", "Nebraska", "United States"]
    panels = [("Born outside the U.S.", lambda g: acs_share(rows, g, "B05002_013", "B05002_001")),
              ("Speak a language other\nthan English at home", lambda g: 100 - acs_share(rows, g, "C16001_002", "C16001_001")),
              ("Workers employed\nin manufacturing", lambda g: acs_share(rows, g, ("C24030_007", "C24030_034"), "C24030_001"))]
    fig = plt.figure(figsize=(W, 5.6))
    for i, (ttl, fn) in enumerate(panels):
        ax = fig.add_axes([0.16 + i * 0.285, 0.14, 0.22, 0.50])
        vals = [fn(g) for g in geos]
        ax.barh(range(4), vals, color=[YELLOW, BLUE, MUTED, MUTED], height=0.62)
        for j, v in enumerate(vals):
            ax.text(v + 1.5, j, f"{v:.0f}%", va="center", color=INK, fontsize=12, fontweight="bold" if j == 0 else "normal")
        ax.set_ylim(3.6, -0.6)
        ax.set_xlim(0, 85)
        ax.set_xticks([])
        ax.set_yticks(range(4))
        ax.set_yticklabels(names if i == 0 else [""] * 4, fontsize=11.5, color=INK)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(ttl, color=INK, fontsize=12, fontweight="bold", loc="left", pad=10)
    titleblock(fig, "Before the closure, Lexington looked little like the rest of Nebraska",
               "Share of residents, 2020 to 2024. The manufacturing share is of employed residents age 16 and over,\n"
               "in any manufacturing job, not only at the beef plant.")
    credit(fig, "Source: U.S. Census Bureau, American Community Survey 2020-2024 (5-year). Survey estimates; Lexington's carry wide margins of error.")
    save(fig, "06-before-the-closure.png")


# ---------------------------------------------------------------- 07 fewer cattle, costlier cattle
def cattle():
    inv = {int(r["year"]): int(r["head"]) / 1e6 for r in read_csv("cattle_inventory_jan1.csv") if int(r["year"]) >= 1950}
    pr = {dt.date(int(r["year"]), int(r["month"]), 1): float(r["dollars_per_cwt"])
          for r in read_csv("steer_heifer_price_received_monthly.csv") if int(r["year"]) >= 2000}
    fig = plt.figure(figsize=(W, 6.6))
    ax1 = fig.add_axes([0.07, 0.13, 0.40, 0.56])
    ax2 = fig.add_axes([0.56, 0.13, 0.39, 0.56])
    for ax in (ax1, ax2):
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
    ys = sorted(inv)
    ax1.plot(ys, [inv[y] for y in ys], color=BLUE, lw=2.4)
    peak = max(ys, key=lambda y: inv[y])
    last = ys[-1]
    lower = [y for y in ys if y < last and inv[y] < inv[last]]
    since = max(lower)
    for y, dx, dy, ha in ((peak, 0, 10, "center"), (last, -4, -14, "right")):
        ax1.plot([y], [inv[y]], "o", color=BLUE, ms=5.5)
        ax1.annotate(f"{y}: {inv[y]:.1f} million", (y, inv[y]), xytext=(dx, dy), textcoords="offset points", ha=ha,
                     color=BLUE, fontsize=10.5, fontweight="bold")
    ax1.set_ylim(0, 145)
    ax1.set_xlim(1946, 2029)
    ax1.set_xticks(range(1950, 2021, 10))
    ax1.set_title("Fewer cattle", color=INK, fontsize=13, fontweight="bold", loc="left", pad=26)
    ax1.text(0, 1.035, "All cattle and calves in the U.S. on January 1, millions", transform=ax1.transAxes, color=INK_DIM, fontsize=9.5)

    xs = sorted(pr)
    f0, f1 = dt.date(2023, 10, 1), dt.date(2025, 9, 30)
    ax2.axvspan(f0, f1, color=GRID, lw=0)
    ax2.text(dt.date(2024, 10, 1), 22, "Tyson fiscal\n2024 and 2025", color=INK_DIM, fontsize=9, ha="center", va="bottom")
    ax2.plot(xs, [pr[d] for d in xs], color=YELLOW, lw=2)
    hi = max(xs, key=lambda d: pr[d])
    start = dt.date(2020, 1, 1)
    for d, dx, dy, ha, sep in ((start, 0, -30, "center", "\n"), (hi, -8, 6, "right", ": "), (xs[-1], 8, -6, "left", "\n")):
        ax2.plot([d], [pr[d]], "o", color=YELLOW, ms=5.5)
        ax2.annotate(f"{label(d)}{sep}${pr[d]:.0f}", (d, pr[d]), xytext=(dx, dy), textcoords="offset points", ha=ha,
                     va="center", color=YELLOW, fontsize=10.5, fontweight="bold")
    ax2.set_ylim(0, 290)
    ax2.set_xlim(dt.date(1998, 1, 1), dt.date(2031, 6, 1))
    ax2.set_xticks([dt.date(y, 1, 1) for y in range(2000, 2026, 5)])
    ax2.set_xticklabels([str(y) for y in range(2000, 2026, 5)])
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:.0f}"))
    ax2.set_title("Costlier cattle", color=INK, fontsize=13, fontweight="bold", loc="left", pad=26)
    ax2.text(0, 1.035, "Price paid to producers for steers and heifers, per 100 pounds", transform=ax2.transAxes, color=INK_DIM, fontsize=9.5)
    allpr = {dt.date(int(r["year"]), int(r["month"]), 1): float(r["dollars_per_cwt"])
             for r in read_csv("steer_heifer_price_received_monthly.csv")}
    if max(allpr, key=lambda d: allpr[d]) != hi:
        sys.exit("the price peak is not the record; rewrite the title")
    titleblock(fig, f"Smallest U.S. cattle herd since {since}, highest cattle prices on record",
               f"The herd on January 1, {last} was {-pct(inv[peak], inv[last]):.0f}% below its {peak} peak. The average price of the cattle "
               f"beef plants buy went\nfrom ${pr[start]:.0f} per 100 pounds in {label(start)} to ${pr[hi]:.0f} in {label(hi)}, up {pct(pr[start], pr[hi]):.0f}%. Prices are not adjusted for inflation.",
               y=0.97)
    credit(fig, "Source: USDA National Agricultural Statistics Service, Cattle report and Agricultural Prices. Survey estimates.")
    save(fig, "07-cattle-squeeze.png")


CHARTSET = {"population": population, "hispanic": hispanic, "unemployment": unemployment, "employed": employed,
            "jobs": jobs, "before": before, "cattle": cattle}

if __name__ == "__main__":
    use_house_style()
    for name in (sys.argv[1:] or CHARTSET):
        CHARTSET[name]()
