# MNFT-3 — DLP 3D Printing Laboratory Report

The project contains a preliminary **two-column** LaTeX scientific report in `main.tex`. The first page has a **full-width Vilnius University header with emblem, title, and abstract**. Later sections use two columns, with the SEM images arranged together as a legible, full-width figure. The document includes the objective, short theoretical background, measured curing-depth analysis, experimental and linearized graphs, residuals, target-depth exposure table, and provisional SEM measurements.

## References
The bibliography in `references.bib` cites peer-reviewed articles, Jacobs' stereolithography paper, and the primary Vilnius University lab guide:

*Vilnius University, Faculty of Physics, Laser Research Center, Laboratory Assignment No. MNFT-3: Assessment of the Spatial Resolution in Z Axis of the Digital Light Processing-Based 3D Printing Employing Beer–Lambert Law*, Vilnius (2020).

## University logo and layout
The image `figures/vu_logo.png` is included directly from the repository and used without recolouring or stretching. Its source is the public [`ramojus/typst-template-VU-thesis`](https://github.com/ramojus/typst-template-VU-thesis) template; see the [official VU visual identity guide](https://www.vu.lt/en/vu-brand-style-guidelines) for logo usage. The layout uses an article-like two-column body rather than the final Optica journal style. Equations/plots fit a single column; the two SEM micrographs span both columns.

## Data and figures
- `data/working_curve_corrected.csv`: twenty times and thicknesses (glass already subtracted in the corrected-height column).
- `data/working_curve_fit.csv`: fit values and residuals for LaTeX figures.
- `data/SEM_measurements_preliminary.csv`: preliminary projected SEM measurements (not yet matched to CAD).
- `analysis/plot_working_curve.py`: regenerates the conventional curing-depth versus time graph, linearized graph, residuals, and fit CSV.
- `figures/SEM_7176_annotated.png`, `figures/SEM_7179_annotated.png`, `figures/stl_sections.png`: referenced by LaTeX but not yet uploaded; missing-image placeholders are shown automatically.

To regenerate analysis:

~~~bash
python -m pip install numpy matplotlib
python analysis/plot_working_curve.py
~~~

To compile, use a LaTeX installation with `pgfplots`, `booktabs`, and `lmodern`:

~~~bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
~~~

## Outstanding experimental details

Confirm the printer model, resin, illumination wavelength, projected pixel dimensions, exposure conditions and sample preparation. Assign the SEM images to specific features in the original STL and verify edge positions using ImageJ. Add photographs and parameters for the additional printed object.

The fit parameters **h_a ≈ 146 µm**, **T_c ≈ 1.75 s**, **R² ≈ 0.959** are provisional. Height measurements were recorded in 50-µm increments; predicted exposure times are curing-threshold estimates, not independently validated print settings. The exact Optica/Optics Express template will replace the temporary standard article class once available.
