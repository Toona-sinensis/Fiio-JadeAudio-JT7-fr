import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

d = np.loadtxt("jt7_fr_48oct_normalized.csv", delimiter=",", skiprows=1)
grid, norm = d[:, 0], d[:, 1]

fig, ax = plt.subplots(figsize=(13, 5.5), dpi=145)
ax.semilogx(grid, norm, lw=2.0, color="#111")
ax.axhline(0, color="#aaa", lw=0.6)
ax.set_xlim(20, 20000)
ax.set_ylim(-27, 18)
ax.set_yticks(np.arange(-25, 16, 5))
ax.set_xticks([20, 30, 50, 100, 200, 500, 1000, 2000, 3000, 5000, 10000, 20000])
ax.set_xticklabels(["20", "30", "50", "100", "200", "500",
                    "1k", "2k", "3k", "5k", "10k", "20k"])
ax.grid(True, which="both", alpha=0.25)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("dB re 1 kHz")
ax.set_title("Jade Audio JT7 - frequency response (B&K 5128, digitized)")
fig.tight_layout()
fig.savefig("jt7_frequency_response.png")
print("saved jt7_frequency_response.png")
