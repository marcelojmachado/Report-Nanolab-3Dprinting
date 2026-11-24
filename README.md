# MNFT-3 — DLP 3D Printing Laboratory Report

The project contains a preliminary **two-column** LaTeX scientific report in `main.tex`. The first page has a **full-width Vilnius University header with emblem, title, and abstract**. Later sections use two columns, with the SEM images arranged together as a legible, full-width figure. The document includes the objective, short theoretical background, measured curing-depth analysis, experimental and linearized graphs, residuals, target-depth exposure table, and provisional SEM measurements.

## References
The bibliography in `references.bib` cites peer-reviewed articles, Jacobs' stereolithography paper, and the primary Vilnius University lab guide:

*Vilnius University, Faculty of Physics, Laser Research Center, Laboratory Assignment No. MNFT-3: Assessment of the Spatial Resolution in Z Axis of the Digital Light Processing-Based 3D Printing Employing Beer–Lambert Law*, Vilnius (2020).

## University logo and layout
The first-page header now uses `figures/vu_logo_burgundy.svg` (burgundy vector emblem `#78003F`). The official university [brand guide](https://www.vu.lt/en/vu-brand-style-guidelines) specifies this colour. The artwork was adapted from the [verified Vilnius University emblem in ICPC logos](https://github.com/WISVCH/icpc-logos/blob/main/universities/logos/2643.svg). The black PNG is retained only for historical reference. LaTeX uses the `svg` package to convert SVG with Inkscape, requiring **Inkscape and shell escape**.

## Data and figures
- `data/working_curve_corrected.csv`: twenty times and thicknesses (glass already subtracted in the corrected-height column).
- `data/working_curve_fit.csv`: fit values and residuals for LaTeX figures.
- `data/SEM_measurements_preliminary.csv`: preliminary projected SEM measurements (not yet matched to CAD).
- `analysis/plot_working_curve.py`: regenerates the conventional curing-depth versus time graph, linearized graph, residuals, and fit CSV.
- `figures/stl_sections.png`: now included as an actual image, with a full-width figure in `main.tex`.
- `figures/SEM_7176_annotated.png` and `figures/SEM_7179_annotated.png`: still to be uploaded; placeholders remain until they are available.

To regenerate analysis:

~~~bash
python -m pip install numpy matplotlib
python analysis/plot_working_curve.py
~~~

To compile, use a LaTeX installation with `svg`, `pgfplots`, `booktabs`, and `lmodern`, plus Inkscape:

~~~bash
pdflatex -shell-escape main.tex
bibtex main
pdflatex -shell-escape main.tex
pdflatex -shell-escape main.tex
~~~

## Outstanding experimental details

Confirm the printer model, resin, illumination wavelength, projected pixel dimensions, exposure conditions and sample preparation. Assign the SEM images to specific features in the original STL and verify edge positions using ImageJ. Add photographs and parameters for the additional printed object.

The fit parameters **h_a ≈ 146 µm**, **T_c ≈ 1.75 s**, **R² ≈ 0.959** are provisional. Height measurements were recorded in 50-µm increments; predicted exposure times are curing-threshold estimates, not independently validated print settings. The exact Optica/Optics Express template will replace the temporary standard article class once available.
