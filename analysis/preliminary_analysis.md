# MNFT-3 preliminary assessment of uploaded measurements

Source: student workbook **MNFT Lab.xlsx** (2026-11-24). Substrate (microscope glass) thickness = 0.025 cm = 250 µm. This thickness is subtracted **only** when raw measurements include the glass; the workbook's 'z (cm)' column is already corrected.

Correction: z_resin [µm] = (z_total [cm] - 0.025 cm) * 10000.

There are 20 recorded exposure-time/thickness pairs: exposure 1–30 s, cured resin 0–450 µm, values in 50 µm increments.

Exploratory ordinary-least-squares fit of z[µm] vs ln(t[s]) using 19 positive-height observations (2–30 s) gives:
- h_a = 146.12 µm (statistical slope standard error 7.31 µm, excludes systematic/quantization errors)
- T_c = 1.746 s
- R² = 0.9592
- RMS fit residual = 23.41 µm
- predicted t for 25, 50, 75, 100, 125, 150 µm cured depths: 2.07, 2.46, 2.92, 3.46, 4.11, 4.87 s, respectively.

**These are provisional values**. The zero-thickness point at 1 s is treated as a non-cured/unresolved point rather than a positive-height datum; the 50-µm reporting steps limit precision and target depths below those steps require cautious extrapolation. Some data are non-monotonic (e.g. 12 to 14 s, 28 to 30 s); check the physical measurement method before interpreting uncertainty. A cure-threshold time is not necessarily the optimal layer printing time.

## XY STL inspection

The uploaded `resolution_test_XY.stl` is dimensioned 10 × 10 × 1.5 in its coordinate units (assumed mm, as is customary for the assignment). A slice shows arrays of rectangular bars and square elements with nominal lateral feature widths 0.050, 0.075, 0.100, 0.150, 0.200, 0.300 and 0.400 mm; these are nominal CAD dimensions, not yet verified by SEM.

## SEM metadata

Hitachi TM-1000 images include paired *.txt metadata for magnifications x40, x150, x200, and x500. PixelSize is interpreted tentatively as nm/pixel (consistent with the calibration marker), yielding 4.58984, 1.22396, 0.91797 and 0.36719 µm/pixel respectively. Confirm units/scale marker before final dimensional quantification. Use original unresized 1280x1040 JPGs.

## Pending

Identify which SEM fields belong to the XY resolution specimen, measure corresponding nominal bar/square feature widths and gaps, and add representative SEM panels. Record the resin, printer and actual exposure/irradiance parameters before drafting the final quantitative conclusions.
