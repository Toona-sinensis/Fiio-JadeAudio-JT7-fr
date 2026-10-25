# Jade Audio JT7 — Frequency Response Data

Digitized frequency response of the **FiiO / Jade Audio JT7** (飞傲翡声 JT7) headphone,
recovered by pixel-tracing published measurement plots.

## Data source

All curves come from measurement charts shown in this video:

- **Video:** <https://www.bilibili.com/video/BV1Y31UBuE7K>
- **Title:** 【A子】推荐评级：S，ChiFi供应链的奇迹之声。 —— FIIO 翡声 JT7
- **Uploader:** A子如是说
- **Stated measurement rig:** B&K 5128
- **Stated listening target:** JM1 - DF Target

The charts themselves are captioned `Measure by B&K 5128`. Three separate charts were
used, each plotting the same JT7 trace against a different comparison curve
(JM-1/DFR, HiFiMAN Edition XS, FiiO FT1Pro).

These are digitized from screenshots of a review video, **not** original measurement
files. See [Accuracy](#accuracy) before relying on the numbers.

## Files

| File | Contents |
|---|---|
| `data/jt7_fr_48oct_normalized.csv` | **Main file.** 1/48-octave, 479 points, 20 Hz–20 kHz, normalized to 0 dB at 1 kHz |
| `data/jt7_fr_48oct_absolute.csv` | Same grid, but keeps the vertical offset as printed in the source charts |
| `data/jt7_fr_12oct_normalized.csv` | 1/12-octave, 120 points, normalized — easier for manual EQ work |
| `data/jt7_autoeq.csv` | Two-column `frequency,raw` format for AutoEQ / REW / squig.link import |
| `data/jt7_frequency_response_report.txt` | Full analysis: band averages, peak positions, consistency checks |
| `charts/jt7_frequency_response.png` | The three source traces overlaid, their average, and their spread |
| `charts/jt7_source_comparison.png` | Independent cross-check against a separate plot (`graph.png`) |
| `scripts/extract_from_screenshots.py` | Reproduces the extraction from the source screenshots |
| `scripts/plot.py` | Reproduces the chart |

### CSV format

```csv
Frequency (Hz),JT7 (dB re 1kHz)
20.000,-7.539
20.291,-7.432
...
```

Frequency is in Hz, level in dB. The normalized column is 0 dB at 1 kHz; the absolute
column preserves the chart's vertical placement, which is **not** a calibrated
playback SPL.

## Single channel — not left/right

The source charts draw **one** JT7 trace each. There is no left/right split in this
data, and therefore no channel-matching information. (An earlier iteration used a
squig.link-style plot that did carry L/R; that is not what is published here.)

## Measurement summary

Normalized to 1 kHz:

| Band | Level |
|---|---|
| 20–60 Hz | −0.8 dB |
| 60–200 Hz | −0.2 dB |
| 200–1000 Hz | −0.1 dB |
| 1–2 kHz | +0.8 dB |
| 2–4 kHz | +10.5 dB |
| 4–8 kHz | +7.4 dB |
| 8–16 kHz | +2.7 dB |

Notable points:

- 20 Hz: −7.3 dB (sub-bass roll-off)
- 50 Hz: +1.6 dB (small bass rise)
- **3.18 kHz: +13.0 dB** — the pinna-gain peak, the largest feature in the response
- 4.83 kHz: +2.7 dB (dip following the peak)
- 6 kHz: +11.7 dB (second peak)
- 10 kHz: +4.2 dB
- 20 kHz: −19.2 dB

Overall: flat midrange within about 1 dB from 200 Hz to 2 kHz, a strong ~3 kHz pinna
gain, and a steep roll-off above 10 kHz.

## Accuracy

**Reliability of the three source charts against each other.** After aligning at
1 kHz, the three traces agree to RMS 0.11 dB (max 0.66 dB). Their absolute vertical
placement in the chart differs by 1.11 dB, which is a layout difference between
screenshots, not a difference in the data.

**Coverage.** 155329 is complete. 155349 is missing part of 3.0–3.4 kHz. In 155402
the red JT7 trace is hidden beneath the blue FT1Pro curve in several bands (notably
0.13–0.30 kHz and 3.6–4.0 kHz). The average uses every chart that actually covers a
given frequency.

**Independent check.** A separate squig.link-style plot of the same headphone
(`graph.png`, not used to build this data) agrees with the result to RMS 0.36 dB in
1–4 kHz and 0.48 dB in 100 Hz–1 kHz. Above 10 kHz it differs by 2.9 dB, but that plot
is under-sampled there — 43% of its high-frequency points lie on straight lines — so
the disagreement is attributed to that source, not to the data published here.

**Expect roughly ±0.3 dB reading error from 100 Hz to 8 kHz, and worse above 15 kHz**
where the traces run steeply. Black regions of the chart and the comparison curves
were masked out during extraction; the colour separation was verified at each point
where the JT7 trace crosses a comparison curve.

## License

The digitized data is released under CC0 1.0 (public domain dedication).

The underlying measurement is the work of the video author (**A子如是说**); this
repository only re-publishes it in machine-readable form, with attribution above.
If you redistribute the data, please keep the source link.
