import json

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 18

# NOTE: Add new dataset entries here. That's it.
DATASETS = [
    ("2023 (Oct)", "raw/japanese_researchers_2023.json", "steelblue"),
    ("2026 (Jun)", "raw/japanese_researchers_2026.json", "darkred"),
]


def log_quadratic(x, log_a, b, c):
    log_x1 = np.log(x + 1)
    return log_a + b * log_x1 + c * log_x1 ** 2


last = 500
_, ax = plt.subplots(figsize=(12, 5))

for label, path, color in DATASETS:
    citations = np.sort(list(json.load(open(path)).values()))[::-1]
    x = np.arange(len(citations))
    ax.plot(x, citations, color=color, label=label)

    tail_start = max(1, len(citations) // 20)
    popt, _ = curve_fit(
        log_quadratic,
        x[tail_start:],
        np.log(citations[tail_start:]),
        p0=[np.log(citations[tail_start]), -0.5, 0.0],
        maxfev=10000,
    )
    dx = np.linspace(tail_start, last, 1000)
    ax.plot(dx, np.exp(log_quadratic(dx, *popt)), color=color, ls="dashed")

ax.set_xlim(-5, last + 5)
ax.set_yscale("log")
ax.set_xlabel("Ranking (among JP researchers)")
ax.set_ylabel("Citation Count")
ax.legend()
ax.grid(which="minor", color="gray", linestyle=":")
ax.grid(which="major", color="black")
plt.tight_layout()
plt.show()
