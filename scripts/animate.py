"""Animated GIFs of the unemployment charts for social posts.

short: charts/03-unemployment-rate.png, January 2024 to the latest month.
long:  charts/09-unemployment-rate-since-2016.png, January 2016 to the latest month.
The lines draw in over about eight seconds (long: ten), then the finished chart holds. The last
frame is the static chart itself, resized. Labels show only published monthly values.

    python scripts/animate.py [short|long] [seconds] [hold_seconds]
"""
import datetime as dt
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import charts as C  # noqa: E402
from common import CHARTS, ROOT, read_csv  # noqa: E402
from plot_style import BLUE, GRAY, INK_DIM, MUTED, SURFACE, YELLOW, credit, titleblock, use_house_style  # noqa: E402

OUT = ROOT / "posts" / "lexington-tyson-plant-closure" / "social"
MODE = sys.argv[1] if len(sys.argv) > 1 else "short"
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else (10.0 if MODE == "long" else 8.0)
HOLD = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
FRAME_MS = 80
WIDTH_PX = 1200


def series():
    rows, x = C.laus()
    cmp = read_csv("unemployment_rate_compare.csv")
    out = []
    for geo, color, dashed in (("United States", GRAY, True), ("Nebraska", BLUE, False)):
        s = {dt.date(int(r["year"]), int(r["month"]), 1): float(r["unemployment_rate"]) for r in cmp if r["geography"] == geo}
        out.append((geo, color, dashed, x, [s.get(d, float("nan")) for d in x]))
    out.append(("Dawson County", YELLOW, False, x, C.col(rows, "unemployment_rate")))
    return rows, x, out


def short():
    use_house_style()
    OUT.mkdir(parents=True, exist_ok=True)
    rows, x, ss = series()
    xn = np.array([mdates.date2num(d) for d in x])

    fig, ax = C.frame()
    fig.set_dpi(WIDTH_PX / fig.get_figwidth())
    ax.set_ylim(0, 24)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
    C.month_axis(ax, x)
    ax.text(dt.date(2024, 1, 15), 6.4, "Dawson County", color=YELLOW, fontsize=12, fontweight="bold")
    ax.text(dt.date(2024, 9, 1), 6.4, "Nebraska", color=BLUE, fontsize=12, fontweight="bold")
    ax.text(dt.date(2025, 2, 10), 6.4, "United States", color=GRAY, fontsize=12, fontweight="bold")
    titleblock(fig, "Dawson County's unemployment rate went from 3.4% to 16.9% in one month",
               "Unemployment rate by month, not seasonally adjusted.")
    credit(fig, "Source: U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics and Current Population Survey. County figures are\n"
                "model-based estimates. October 2025 was not published.")
    closure = mdates.date2num(dt.date(2026, 1, 20))
    cl = ax.axvline(dt.date(2026, 1, 20), color=MUTED, lw=1, ls=(0, (3, 3)), visible=False)
    ct = ax.text(dt.date(2026, 1, 12), 23.2, "Plant closes\nJan. 20, 2026", color=INK_DIM, fontsize=9.5, ha="right", va="top", visible=False)
    lines = [ax.plot([], [], color=c, lw=2.6 if g == "Dawson County" else 1.8, ls=(0, (4, 2)) if dash else "-")[0]
             for g, c, dash, _, _ in ss]
    tip = ax.annotate("", (xn[0], 0), xytext=(8, 0), textcoords="offset points", color=YELLOW, fontsize=11,
                      fontweight="bold", va="center", annotation_clip=False, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
    clock = ax.text(0.02, 0.93, "", transform=ax.transAxes, color=INK_DIM, fontsize=15, fontweight="bold", va="center")

    def draw(cursor):
        for ln, (_, _, _, _, y) in zip(lines, ss):
            keep = xn <= cursor
            ln.set_data(xn[keep], np.array(y)[keep])
        county = np.array(ss[-1][4])
        seen = [i for i in range(len(xn)) if xn[i] <= cursor and county[i] == county[i]]
        if seen:
            i = seen[-1]                                   # last published month, never an in-between value
            tip.xy = (xn[i], county[i]); tip.set_text(f"{county[i]:.1f}%")
            clock.set_text(C.label(x[i]))
        on = cursor >= closure
        cl.set_visible(on); ct.set_visible(on)
        fig.canvas.draw()
        return Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB").copy()

    n = int(round(SECONDS * 1000 / FRAME_MS))
    frames = [draw(xn[0] + (xn[-1] - xn[0]) * i / (n - 1)) for i in range(n)]
    size = frames[0].size
    plt.close(fig)

    # The held frame is the published chart, so the GIF ends on exactly what the post shows.
    last = Image.open(CHARTS / "03-unemployment-rate.png").convert("RGB").resize(size, Image.LANCZOS)
    pal = last.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames] + [last.quantize(palette=pal, dither=Image.Dither.NONE)]
    path = OUT / "unemployment-rate.gif"
    q[0].save(path, save_all=True, append_images=q[1:], duration=[FRAME_MS] * n + [int(HOLD * 1000)], loop=0, optimize=False, disposal=1)
    last.save(OUT / "unemployment-rate-final-frame.png")
    print(f"{path.name}: {len(q)} frames, {size[0]}x{size[1]}, {n * FRAME_MS / 1000:.1f}s + {HOLD:.0f}s hold, "
          f"{path.stat().st_size / 1e6:.2f} MB")


def long():
    use_house_style()
    OUT.mkdir(parents=True, exist_ok=True)
    rows, x, ss = C.long_series()
    m = C.long_marks(x, ss)
    xn = np.array([mdates.date2num(d) for d in x])

    fig, ax = C.frame()
    fig.set_dpi(WIDTH_PX / fig.get_figwidth())
    C.long_axes(ax, x)
    title, sub = C.long_title(m)
    titleblock(fig, title, sub)
    credit(fig, C.long_credit(rows, x))
    closure = mdates.date2num(dt.date(2026, 1, 20))
    cl = ax.axvline(dt.date(2026, 1, 20), color=MUTED, lw=1, ls=(0, (3, 3)), visible=False)
    ct = ax.text(dt.date(2026, 1, 12), 23.2, "Plant closes\nJan. 20, 2026", color=INK_DIM, fontsize=9.5, ha="right", va="top", visible=False)
    lines = [ax.plot([], [], color=c, lw=2.6 if g == "Dawson County" else 1.8, ls=(0, (4, 2)) if dash else "-")[0]
             for g, c, dash, _ in ss]
    marks = C.long_point_labels(ax, m)                      # pairs: point, label, in the order of long_marks
    when = [m["cpk"], m["upk"], m["jan"], m["feb"], m["pk"], m["last"]]
    tip = ax.annotate("", (xn[0], 0), xytext=(8, 0), textcoords="offset points", color=YELLOW, fontsize=11,
                      fontweight="bold", va="center", annotation_clip=False, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
    clock = ax.text(0.02, 0.93, "", transform=ax.transAxes, color=INK_DIM, fontsize=15, fontweight="bold", va="center")
    county = np.array(ss[-1][3])

    def draw(cursor):
        for ln, (_, _, _, y) in zip(lines, ss):
            keep = xn <= cursor
            ln.set_data(xn[keep], np.array(y)[keep])
        seen = [i for i in range(len(xn)) if xn[i] <= cursor and county[i] == county[i]]
        i = seen[-1]                                       # last published month, never an in-between value
        shown = [mdates.date2num(d) <= cursor for d in when]
        for k, on in enumerate(shown):
            marks[2 * k].set_visible(on); marks[2 * k + 1].set_visible(on)
        labeled = any(on and when[k] == x[i] for k, on in enumerate(shown))
        tip.xy = (xn[i], county[i]); tip.set_text("" if labeled else f"{county[i]:.1f}%")
        clock.set_text(C.label(x[i]))
        on = cursor >= closure
        cl.set_visible(on); ct.set_visible(on)
        fig.canvas.draw()
        return Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB").copy()

    n = int(round(SECONDS * 1000 / FRAME_MS))
    frames = [draw(xn[0] + (xn[-1] - xn[0]) * i / (n - 1)) for i in range(n)]
    size = frames[0].size
    plt.close(fig)
    finish(frames, CHARTS / "09-unemployment-rate-since-2016.png", "unemployment-rate-since-2016", size, n)


def finish(frames, static, name, size, n):
    # The held frame is the static chart, so the GIF ends on exactly what the chart shows.
    last = Image.open(static).convert("RGB").resize(size, Image.LANCZOS)
    pal = last.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames] + [last.quantize(palette=pal, dither=Image.Dither.NONE)]
    path = OUT / f"{name}.gif"
    q[0].save(path, save_all=True, append_images=q[1:], duration=[FRAME_MS] * n + [int(HOLD * 1000)], loop=0, optimize=False, disposal=1)
    last.save(OUT / f"{name}-final-frame.png")
    print(f"{path.name}: {len(q)} frames, {size[0]}x{size[1]}, {n * FRAME_MS / 1000:.1f}s + {HOLD:.0f}s hold, "
          f"{path.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    {"short": short, "long": long}[MODE]()
