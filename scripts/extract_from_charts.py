#!/usr/bin/env python3
"""Digitize the JT7 frequency response from the source measurement charts.

The source charts are frames from the review video named in README.md. They are not
redistributed here; place the three screenshots in this directory (or pass paths in
IMGS) before running.

Output: jt7_fr_48oct_normalized.csv, jt7_fr_48oct_absolute.csv,
        jt7_fr_12oct_normalized.csv, jt7_autoeq.csv, jt7_frequency_response_report.txt

Requires: numpy, Pillow
"""

import numpy as np
from PIL import Image

# Each chart plots one red JT7 trace over a different comparison curve.
# The plot box coordinates (x0, x1, y0, y1) are the inner edges of the axes.
IMGS = [
    ("屏幕截图 2026-10-25 155329.png", 125, 1464, 149, 721),  # vs JM-1/DFR
    ("屏幕截图 2026-10-25 155349.png", 135, 1474, 161, 733),  # vs HiFiMAN Edition XS
    ("屏幕截图 2026-10-25 155402.png", 98, 1437, 160, 732),   # vs FiiO FT1Pro
]
FMIN, FMAX = 20.0, 20000.0


def runs_of(ys, gap=4):
    """Split a sorted column of y-pixels into contiguous runs."""
    runs, cur = [], [ys[0]]
    for y in ys[1:]:
        if y - cur[-1] <= gap:
            cur.append(y)
        else:
            runs.append(cur)
            cur = [y]
    runs.append(cur)
    return runs


def trace_red_curve(path, x0, x1, y0, y1):
    """Return (frequency, dB) for the red JT7 stroke in one chart."""
    a = np.array(Image.open(path).convert("RGB")).astype(int)
    h, w, _ = a.shape
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

    # The JT7 stroke is red/crimson. This test rejects the magenta target curve
    # (high blue) and the green comparison curve.
    red = (r > 110) & (r - g > 45) & (r - b > 30)

    yy, xx = np.mgrid[0:h, 0:w]
    inside = (xx >= x0 + 1) & (xx <= x1 - 1) & (yy >= y0 + 2) & (yy <= y1 - 1)
    # The legend swatches are in the top-right of the plot box and are the same red,
    # so they must be excluded or the tracker latches onto them.
    legend = (xx >= x1 - 415) & (yy <= y0 + 138)
    red &= inside & ~legend

    # x: plot box spans exactly three decades, 20 Hz to 20 kHz
    px_per_decade = (x1 - x0) / 3.0
    x_at_20hz = x0 - px_per_decade * np.log10(FMIN)

    # y: top edge +25 dB, bottom edge -25 dB
    def db_of(y):
        return 25.0 - (y - y0) * 50.0 / (y1 - y0)

    # Follow the stroke left to right, choosing the run nearest the previous column
    # so that near-vertical stretches and crossings do not derail the track.
    pts, prev = {}, None
    for x in range(x0 + 1, x1):
        if not red[:, x].any():
            continue
        runs = runs_of(np.nonzero(red[:, x])[0])
        if prev is None:
            run = max(runs, key=len)
        else:
            run = min(runs, key=lambda rr: abs(np.median(rr) - prev))
            if abs(np.median(run) - prev) > 45:
                continue  # a jump this large is a different curve, not this one
        prev = float(np.median(run))
        pts[x] = prev

    xs = np.array(sorted(pts), float)
    f = 10 ** ((xs - x_at_20hz) / px_per_decade)
    db = db_of(np.array([pts[x] for x in xs]))
    order = np.argsort(f)
    return f[order], db[order]


def smooth_log(lg, d, frac=48.0):
    """Gaussian smoothing with constant fractional-octave bandwidth."""
    sigma = (1.0 / frac) / 2.355
    out = np.empty_like(d)
    for i, x in enumerate(lg):
        w = np.exp(-0.5 * ((lg - x) / sigma) ** 2)
        out[i] = (w * d).sum() / w.sum()
    return out


def main():
    grid = FMIN * 2 ** (np.arange(int(np.log2(FMAX / FMIN) * 48) + 1) / 48.0)
    lg = np.log10(grid)

    curves = []
    for path, x0, x1, y0, y1 in IMGS:
        f, db = trace_red_curve(path, x0, x1, y0, y1)
        curves.append(smooth_log(lg, np.interp(lg, np.log10(f), db)))
        print(f"{path}: {len(f)} columns, {f[0]:.0f}-{f[-1]:.0f} Hz")
    curves = np.array(curves)

    # The three charts differ in vertical placement but not in shape, so anchor each
    # at 1 kHz before averaging.
    ref = int(np.argmin(np.abs(grid - 1000.0)))
    levels = curves[:, ref]
    print(f"\n1 kHz level per chart: {np.round(levels, 2)}")
    print(f"spread: {levels.max() - levels.min():.2f} dB")

    aligned = curves - levels[:, None]
    norm = aligned.mean(axis=0)
    spread = aligned.max(axis=0) - aligned.min(axis=0)
    print(f"shape agreement: RMS {np.sqrt(np.mean(spread ** 2)):.3f} dB, "
          f"max {spread.max():.2f} dB")

    absolute = norm + levels.mean()

    np.savetxt("jt7_fr_48oct_normalized.csv", np.column_stack([grid, norm]),
               fmt="%.3f", delimiter=",", header="Frequency (Hz),JT7 (dB re 1kHz)",
               comments="")
    np.savetxt("jt7_fr_48oct_absolute.csv", np.column_stack([grid, absolute]),
               fmt="%.3f", delimiter=",", header="Frequency (Hz),JT7 (dB SPL as printed)",
               comments="")
    np.savetxt("jt7_autoeq.csv", np.column_stack([grid, norm]),
               fmt="%.3f", delimiter=",", header="frequency,raw", comments="")

    n12 = int(np.floor(np.log2(FMAX / FMIN) * 12)) + 1
    g12 = FMIN * 2 ** (np.arange(n12) / 12.0)
    np.savetxt("jt7_fr_12oct_normalized.csv",
               np.column_stack([g12, np.interp(np.log10(g12), lg, norm)]),
               fmt="%.3f", delimiter=",", header="Frequency (Hz),JT7 (dB re 1kHz)",
               comments="")

    def at(f0):
        return float(np.interp(np.log10(f0), lg, norm))

    pk = (grid > 2000) & (grid < 5000)
    dp = (grid > 4000) & (grid < 7000)
    report = [
        "Jade Audio JT7 - frequency response",
        "",
        "Source: three measurement charts from https://www.bilibili.com/video/BV1Y31UBuE7K",
        '         (A子如是说), captioned "Measure by B&K 5128".',
        "",
        "Single trace per chart: this data set is ONE channel, there is no L/R split.",
        "",
        "Normalised to 0 dB at 1 kHz.",
        "",
        "  Pinna gain peak    %+6.1f dB at %.0f Hz"
        % (float(norm[pk].max()), grid[pk][np.argmax(norm[pk])]),
        "  Following dip      %+6.1f dB at %.0f Hz"
        % (float(norm[dp].min()), grid[dp][np.argmin(norm[dp])]),
        "  20 Hz              %+6.1f dB" % at(20),
        "  1 kHz              %+6.1f dB" % at(1000),
        "  20 kHz             %+6.1f dB" % at(20000),
        "",
        "The three charts agree to RMS %.2f dB after 1 kHz alignment."
        % np.sqrt(np.mean(spread ** 2)),
    ]
    np.savetxt("jt7_frequency_response_report.txt", np.array(report, dtype=object),
               fmt="%s")
    print("\nWrote 5 files.")


if __name__ == "__main__":
    main()
