# MNFT-3 — DLP 3D Printing Laboratory Report

The project contains a preliminary **two-column** LaTeX scientific report in `main.tex`. The first page has a **full-width Vilnius University header with emblem, title, and abstract**. Later sections use two columns, with the SEM images arranged together as a legible, full-width figure. The document includes the objective, short theoretical background, measured curing-depth analysis, experimental and linearized graphs, residuals, target-depth exposure table, and provisional SEM measurements.

## References
The bibliography in `references.bib` cites peer-reviewed articles, Jacobs' stereolithography paper, and the primary Vilnius University lab guide:

*Vilnius University, Faculty of Physics, Laser Research Center, Laboratory Assignment No. MNFT-3: Assessment of the Spatial Resolution in Z Axis of the Digital Light Processing-Based 3D Printing Employing Beer–Lambert Law*, Vilnius (2020).

## University logo and layout
The first-page header uses `figures/vu_logo_burgundy.png`, a ready-to-use burgundy Vilnius University emblem and English wordmark, sourced from a [Vilnius University presentation project](https://github.com/00riddle00/MSc1-Functional-Data-Analysis/blob/main/Presentations/vu_logo.png). The image retains its original proportions, and the separate faculty name is placed beside it. **No SVG package, Inkscape or shell escape is needed.** The older black PNG and burgundy SVG are retained as unused reference assets.

## Data and figures
- `data/working_curve_corrected.csv`: twenty times and thicknesses (glass already subtracted in the corrected-height column).
- `data/working_curve_fit.csv`: fit values and residuals for LaTeX figures.
- `data/SEM_measurements_preliminary.csv`: preliminary projected SEM measurements (not yet matched to CAD).
- `analysis/plot_working_curve.py`: regenerates the conventional curing-depth versus time graph, linearized graph, residuals, and fit CSV.
- `figures/xy_resolution_3d_perspective.png`: perspective rendering of the actual uploaded `resolution_test_XY.stl` mesh; **the only CAD/design figure** in `main.tex`, spanning two columns. The earlier `figures/stl_sections.png` is retained in the repository but no longer used in the report.
- `figures/SEM_7176_annotated.png` and `figures/SEM_7179_annotated.png`: still to be uploaded; placeholders remain until they are available.

To regenerate analysis:

~~~bash
python -m pip install numpy matplotlib
python analysis/plot_working_curve.py
~~~

To compile, use a standard LaTeX installation with `pgfplots`, `booktabs`, and `lmodern`. Inkscape is not needed:

~~~bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
~~~

## Outstanding experimental details

Confirm the printer model, resin, illumination wavelength, projected pixel dimensions, exposure conditions and sample preparation. Assign the SEM images to specific features in the original STL and verify edge positions using ImageJ. Add photographs and parameters for the additional printed object.

The fit parameters **h_a ≈ 146 µm**, **T_c ≈ 1.75 s**, **R² ≈ 0.959** are provisional. Height measurements were recorded in 50-µm increments; predicted exposure times are curing-threshold estimates, not independently validated print settings. The exact Optica/Optics Express template will replace the temporary standard article class once available.
