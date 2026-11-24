"""Linearized DLP cure-depth working curve for MNFT-3.
Run: python analysis/plot_working_curve.py
Requires: numpy, matplotlib. Reads the uploaded (corrected) CSV in data/.
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
path = root / "data" / "working_curve_corrected.csv"

with path.open(newline="", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

# The raw height includes the microscope glass. Subtract it ONCE.
t_s = np.array([float(row["exposure_s"]) for row in data])
total_cm = np.array([float(row["measured_with_glass_cm"]) for row in data])
glass_cm = np.array([float(row["glass_cm"]) for row in data])
z_um = (total_cm - glass_cm) * 10_000.0

# Cross-check against the pre-corrected column.
assert np.allclose(z_um, [float(r["resin_height_um"]) for r in data])

# A zero-thickness point is not a positive cure-depth measurement.
valid = (t_s > 0) & (z_um > 0)
x = np.log(t_s[valid])  # ln(t_s / 1 s); dimensionless
z = z_um[valid]

# z = h_a * ln(t_s / 1s) + b
(h_a, b), cov = np.polyfit(x, z, 1, cov=True)
T_c = np.exp(-b / h_a)
pred = h_a * x + b
r2 = 1 - np.sum((z - pred)**2) / np.sum((z - np.mean(z))**2)

# Required exposure for selected curing depths (micrometres).
target_um = np.array([25, 50, 75, 100, 125, 150])
target_t_s = T_c * np.exp(target_um / h_a)
print(f"h_a = {h_a:.2f} µm; T_c = {T_c:.3f} s; R² = {r2:.4f}")
for depth, t in zip(target_um, target_t_s):
    print(f"  {depth} µm: {t:.3f} s")

fig, ax = plt.subplots(figsize=(8, 5.2))
ax.scatter(x, z, label="Measured cured depth (z > 0)")
zero = (t_s > 0) & (z_um <= 0)
ax.scatter(np.log(t_s[zero]), z_um[zero], marker="x", label="No measured cure; excluded")
xx = np.linspace(np.log(T_c), np.log(np.max(t_s)), 300)
ax.plot(xx, h_a * xx + b, label="Linear fit")
ax.axvline(np.log(T_c), linestyle=":", label=rf"$T_c={T_c:.2f}$ s")
ax.set_xlabel(r"$\ln(t_p / 1\,\mathrm{s})$")
ax.set_ylabel(r"Cured resin depth $z_p$ ($\mu$m)")
ax.set_title("Linearized Jacobs working curve")
ax.grid(alpha=0.25)
ax.legend()
ax.text(0.02, 0.98,
        f"$h_a={h_a:.1f}$ µm\n$T_c={T_c:.2f}$ s\n$R^2={r2:.3f}$",
        transform=ax.transAxes, va="top",
        bbox={"facecolor": "white", "alpha": 0.9})
fig.tight_layout()
out = root / "figures"
out.mkdir(exist_ok=True)
fig.savefig(out / "working_curve_linearized.png", dpi=250)
fig.savefig(out / "working_curve_linearized.pdf")
plt.close(fig)
