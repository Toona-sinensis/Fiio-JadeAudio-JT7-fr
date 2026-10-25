#!/usr/bin/env python3
"""Generate the overview plot and the extraction-check overlay.

Usage:
    python make_figures.py

Reads the CSVs in data/ and the charts in source/, writes:
    plots/JT7_BK5128_response.png
    verification/JT7_BK5128_extraction_check.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# Chinese labels need a CJK face; fall back through common Windows/Linux families.
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Noto Sans SC', 'SimHei',
                                   'DengXian', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

import digitize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKS = [20, 30, 50, 100, 200, 500, 1000, 2000, 3000, 5000, 10000, 20000]
TICKLABELS = ['20', '30', '50', '100', '200', '500',
              '1k', '2k', '3k', '5k', '10k', '20k']


def overview():
    absl = np.loadtxt(os.path.join(BASE_DIR, 'data', 'JT7_BK5128_1-24oct.csv'),
                      delimiter=',', skiprows=1)
    norm = np.loadtxt(os.path.join(BASE_DIR, 'data', 'JT7_BK5128_normalized.csv'),
                      delimiter=',', skiprows=1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)

    ax1.semilogx(absl[:, 0], absl[:, 1], lw=1.8, color='#111')
    ax1.set_title('绝对 SPL / Absolute (as printed)', fontsize=11)
    ax1.set_ylim(-25, 20)

    ax2.semilogx(norm[:, 0], norm[:, 1], lw=1.8, color='#b71c1c')
    ax2.axhline(0, color='#aaa', lw=0.7)
    ax2.set_title('以 1 kHz 归一 / Normalized to 1 kHz', fontsize=11)
    ax2.set_ylim(-25, 20)

    for ax in (ax1, ax2):
        ax.set_xlim(20, 20000)
        ax.set_xticks(TICKS)
        ax.set_xticklabels(TICKLABELS)
        ax.set_yticks(np.arange(-25, 21, 5))
        ax.grid(True, which='both', alpha=0.25)
        ax.set_xlabel('频率 Frequency (Hz)')
        ax.set_ylabel('dB')

    fig.suptitle('飞傲翡声 JT7 频响曲线 / Frequency Response (B&K 5128)', fontsize=13)
    fig.tight_layout()
    out = os.path.join(BASE_DIR, 'plots', 'JT7_BK5128_response.png')
    fig.savefig(out)
    print('wrote', out)


def extraction_check():
    """Draw the extracted trace over each source chart and stack them."""
    panels = []
    for name, x0, x1, y0, y1 in digitize.CHARTS:
        img = Image.open(digitize.chart_path(name)).convert('RGB')
        f, db = digitize.trace_red(name, x0, x1, y0, y1)

        px_per_decade = (x1 - x0) / 3.0
        x_at_20hz = x0 - px_per_decade * np.log10(digitize.FMIN)

        d = ImageDraw.Draw(img)
        pts = [(x_at_20hz + px_per_decade * np.log10(v),
                y0 + (25.0 - s) * (y1 - y0) / 50.0) for v, s in zip(f, db)]
        d.line(pts, fill=(0, 230, 255), width=2)
        # mark the legend area that was masked out during extraction
        d.rectangle([x1 - 415, y0, x1, y0 + 138], outline=(255, 200, 0), width=2)
        d.text((x0 + 8, y1 - 26), name, fill=(0, 0, 0))
        panels.append(img)

    wid = max(p.width for p in panels)
    total_h = sum(p.height for p in panels)
    canvas = Image.new('RGB', (wid, total_h), (255, 255, 255))
    y = 0
    for p in panels:
        canvas.paste(p, (0, y))
        y += p.height
    out = os.path.join(BASE_DIR, 'verification', 'JT7_BK5128_extraction_check.png')
    canvas.save(out)
    print('wrote', out)


if __name__ == '__main__':
    overview()
    extraction_check()
