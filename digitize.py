#!/usr/bin/env python3
"""Digitize the 飞傲翡声 JT7 frequency response from the published charts.

Source charts: the PNGs in source/ (B&K 5128 measurement, published by
哔哩哔哩 UP主 "A子如是说"). Three charts show the same JT7 trace over
different comparison curves; they are extracted separately, aligned at
1 kHz and averaged.

Axis calibration, verified against the gridlines in all three images:
  x: log scale, 20 Hz .. 20 kHz span exactly three decades across the plot box
  y: linear, +25 dB .. -25 dB between the top and bottom plot borders

Usage:
    python digitize.py 24oct      > data/JT7_BK5128_1-24oct.csv
    python digitize.py normalized > data/JT7_BK5128_normalized.csv
    python digitize.py raw        > data/JT7_BK5128_raw.csv
    python digitize.py frd        > data/JT7_BK5128.frd
    python digitize.py rew        > data/JT7_BK5128_REW.txt

The script writes to stdout and never opens a file for writing; redirect
where you want it. The only files it reads are the fixed charts under source/.
"""
import os
import sys

import numpy as np
from PIL import Image

# (path, plot box x0, x1, y0, y1)
CHARTS = [
    ('chart.png', 125, 1464, 149, 721),                 # vs JM-1/DFR
    ('chart_2_editionxs.png', 135, 1474, 161, 733),     # vs HiFiMAN Edition XS
    ('chart_3_ft1pro.png', 98, 1437, 160, 732),         # vs FiiO FT1Pro
]

FMIN, FMAX = 20.0, 20000.0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def chart_path(name):
    """Resolve a chart under source/, refusing anything that escapes the repo."""
    joined = os.path.normpath(os.path.join(BASE_DIR, 'source', name))
    if os.path.commonpath([joined, BASE_DIR]) != BASE_DIR:
        raise ValueError(f'refusing path outside the repository: {joined!r}')
    return joined


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


def trace_red(name, x0, x1, y0, y1):
    """Return (frequency, dB) for the red JT7 stroke in one chart."""
    a = np.array(Image.open(chart_path(name)).convert('RGB')).astype(int)
    h, w, _ = a.shape
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

    # The JT7 stroke is red/crimson. Rejects the magenta target curve (high blue)
    # and the green comparison curve.
    red = (r > 110) & (r - g > 45) & (r - b > 30)

    yy, xx = np.mgrid[0:h, 0:w]
    inside = (xx >= x0 + 1) & (xx <= x1 - 1) & (yy >= y0 + 2) & (yy <= y1 - 1)
    # Legend swatches sit top-right inside the plot box and are the same red; if
    # they are not removed the tracker latches onto them.
    legend = (xx >= x1 - 415) & (yy <= y0 + 138)
    red &= inside & ~legend

    px_per_decade = (x1 - x0) / 3.0
    x_at_20hz = x0 - px_per_decade * np.log10(FMIN)

    def db_of(y):
        return 25.0 - (y - y0) * 50.0 / (y1 - y0)

    # Follow the stroke left to right, picking the run nearest the previous
    # column so near-vertical stretches and crossings do not derail it.
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
                continue
        prev = float(np.median(run))
        pts[x] = prev

    xs = np.array(sorted(pts), float)
    f = 10 ** ((xs - x_at_20hz) / px_per_decade)
    db = db_of(np.array([pts[x] for x in xs]))
    o = np.argsort(f)
    return f[o], db[o]


def smooth_log(lg, d, frac):
    """Gaussian smoothing with constant fractional-octave bandwidth."""
    sigma = (1.0 / frac) / 2.355
    out = np.empty_like(d)
    for i, x in enumerate(lg):
        w = np.exp(-0.5 * ((lg - x) / sigma) ** 2)
        out[i] = (w * d).sum() / w.sum()
    return out


def load_average():
    """Extract all charts, align at 1 kHz and return (fine grid, absolute dB).

    The three charts sit at slightly different vertical offsets but have the
    same shape, so each is anchored at 1 kHz before averaging and the mean
    offset is added back to keep the absolute values of the charts.
    """
    raw = [trace_red(*c) for c in CHARTS]

    # fine grid at the charts' own horizontal resolution (three decades)
    n_px = max(len(f) for f, _ in raw)
    lg = np.linspace(np.log10(FMIN), np.log10(FMAX), n_px)

    curves = np.array([np.interp(lg, np.log10(f), d) for f, d in raw])
    ref = int(np.argmin(np.abs(10 ** lg - 1000.0)))
    levels = curves[:, ref]
    aligned = curves - levels[:, None]
    mean_db = aligned.mean(axis=0) + levels.mean()
    return lg, mean_db


def resample(lg, db, frac, step):
    """Smooth to `frac` octave and sample every `step` octave."""
    n = int(np.floor(np.log2(FMAX / FMIN) * step)) + 1
    g = FMIN * 2 ** (np.arange(n) / step)
    sm = smooth_log(lg, db, frac)
    return g, np.interp(np.log10(g), lg, sm)


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    mode = sys.argv[1].lower()

    # Emit LF-only newlines regardless of platform, so the output is byte-identical
    # on Windows and Linux and REW tab files do not collect stray carriage returns.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(newline='\n')

    lg, db = load_average()

    if mode == '24oct':
        g, v = resample(lg, db, 24, 24)
        print('frequency,spl')
        for f, s in zip(g, v):
            print(f'{f:.2f},{s:.2f}')

    elif mode == 'normalized':
        g, v = resample(lg, db, 24, 24)
        v = v - np.interp(1000.0, g, v)
        print('frequency,spl')
        for f, s in zip(g, v):
            print(f'{f:.2f},{s:.2f}')

    elif mode == 'raw':
        print('frequency,spl')
        for f, s in zip(10 ** lg, db):
            print(f'{f:.2f},{s:.2f}')

    elif mode == 'frd':
        g, v = resample(lg, db, 24, 24)
        print('* JT7 frequency response, digitized from B&K 5128 chart')
        for f, s in zip(g, v):
            print(f'{f:9.2f} {s:8.2f}     0.0')

    elif mode == 'rew':
        g, v = resample(lg, db, 24, 24)
        for f, s in zip(g, v):
            print(f'{f:.2f}\t{s:.2f}')

    else:
        print(f'unknown mode: {mode!r}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
