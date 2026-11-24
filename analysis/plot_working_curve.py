"""MNFT-3 DLP working curve: original time-axis and linearized plots.

Run from repository root:
    python -m pip install numpy matplotlib
    python analysis/plot_working_curve.py

Input: data/working_curve_corrected.csv
Outputs:
    data/working_curve_fit.csv (for the LaTeX pgfplots figures)
    data/predicted_exposures.csv
    figures/working_curve_time.png/.pdf
    figures/working_curve_linearized.png/.pdf
    figures/working_curve_residuals.png/.pdf
"""
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parents[1]
data_csv = root / "data" / "working_curve_corrected.csv"
fit_csv = root / "data" / "working_curve_fit.csv"
times_csv = root / "data" / "predicted_exposures.csv"
output_dir = root / "figures"
output_dir.mkdir(parents=True, exist_ok=True)

with data_csv.open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))

# Raw thickness includes the microscope glass: 0.025 cm = 250 µm.
# The corrected 'resin_height_um' column is a consistency check only.
t_s = np.asarray([float(row["exposure_s"]) for row in rows])
measured_cm = np.asarray([float(row["measured_with_glass_cm"]) for row in rows])
substrate_cm = np.asarray([float(row["glass_cm"]) for row in rows])
z_um = (measured_cm - substrate_cm) * 1e4
corrected_um = np.asarray([float(row["resin_height_um"]) for row in rows])
if not np.allclose(z_um, corrected_um, atol=1e-6):
    raise ValueError("Corrected depths and raw measurements are inconsistent")

# Only positive, measured cured depths contribute to the logarithmic fit.
# The 1-s, zero-height point is still plotted in the conventional curve.
positive = (t_s > 0) & (z_um > 0)
x_ln = np.log(t_s[positive])  # ln(t / 1s) is dimensionless.
y_um = z_um[positive]

# Linear fit z = h_a ln(t / 1s) + b.
(h_a, b), covariance = np.polyfit(x_ln, y_um, deg=1, cov=True)
fitted_um = h_a * x_ln + b
residual_um = y_um - fitted_um
T_c_s = np.exp(-b / h_a)
r_squared = 1 - (np.sum(residual_um**2)
                 / np.sum((y_um - y_um.mean())**2))
slope_standard_error = np.sqrt(covariance[0, 0])

# Export fit data used in the pgfplots figures in main.tex.
with fit_csv.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["exposure_s", "ln_t_s", "z_um", "fit_um", "residual_um"])
    for t, x, z, fit, residual in zip(
        t_s[positive], x_ln, y_um, fitted_um, residual_um
    ):
        writer.writerow([f"{t:g}", f"{x:.8f}", f"{z:.4f}",
                         f"{fit:.4f}", f"{residual:.4f}"])

target_depth_um = np.array([25, 50, 75, 100, 125, 150], dtype=float)
predicted_s = T_c_s * np.exp(target_depth_um / h_a)
with times_csv.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["target_depth_um", "predicted_exposure_s"])
    for depth, t in zip(target_depth_um, predicted_s):
        writer.writerow([f"{depth:.0f}", f"{t:.4f}"])

print(f"h_a = {h_a:.3f} µm (statistical SE {slope_standard_error:.3f} µm)")
print(f"T_c = {T_c_s:.4f} s, R² = {r_squared:.4f}")
print(f"z [µm] = {h_a:.4f} * ln(t/1 s) + ({b:.4f})")
for depth, t in zip(target_depth_um, predicted_s):
    print(f"{depth:.0f} µm -> {t:.3f} s (predicted curing threshold)")

t_fit = np.linspace(T_c_s, t_s.max(), 400)
z_fit = h_a * np.log(t_fit) + b

# 1. Original cure-depth working curve (linear time axis).
fig, ax = plt.subplots(figsize=(7.3, 4.8))
ax.scatter(t_s, z_um, label="Experimental data", zorder=4)
ax.plot(t_fit, z_fit, label="Logarithmic fit")
ax.set(
    xlabel="Exposure time $t_p$ (s)",
    ylabel="Cured resin depth $z_p$ ($\\mu$m)",
    title="Cure depth versus exposure time",
    xlim=(0, 31)
)
ax.set_ylim(bottom=-20)
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(output_dir / "working_curve_time.png", dpi=250)
fig.savefig(output_dir / "working_curve_time.pdf")
plt.close(fig)

# 2. Linearized form (log-transform time, linear horizontal axis).
fig, ax = plt.subplots(figsize=(7.3, 4.8))
ax.scatter(x_ln, y_um, label="Positive-depth data", zorder=4)
x_fit = np.log(t_fit)
ax.plot(x_fit, z_fit, label="Linear regression")
zero_depth = (t_s > 0) & (z_um == 0)
ax.scatter(np.log(t_s[zero_depth]), z_um[zero_depth],
           marker="x", label="No measured cure; excluded")
ax.set(
    xlabel=r"$\ln(t_p/1\,\mathrm{s})$",
    ylabel="Cured resin depth $z_p$ ($\\mu$m)",
    title="Linearized Jacobs working curve"
)
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(output_dir / "working_curve_linearized.png", dpi=250)
fig.savefig(output_dir / "working_curve_linearized.pdf")
plt.close(fig)

# 3. Diagnostics: linear regression residuals.
fig, ax = plt.subplots(figsize=(7.3, 4.2))
ax.scatter(x_ln, residual_um)
ax.axhline(0, linestyle="--", linewidth=1.0)
ax.set(
    xlabel=r"$\ln(t_p/1\,\mathrm{s})$",
    ylabel="Residual ($\\mu$m)",
    title="Linear-fit residuals"
)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / "working_curve_residuals.png", dpi=250)
fig.savefig(output_dir / "working_curve_residuals.pdf")
plt.close(fig)
