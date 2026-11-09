# NYC Restaurant Health Inspection Analysis

**Course:** SI 385 — Data Science / Statistical Analysis (Fall 2026)

## Question
Are independent restaurants held to a different standard than chain restaurants in NYC health inspections? More specifically, how sensitive is the observed score gap to analytical decisions? Higher inspection scores indicate more violation points.

## Approach
- Audited an inherited marimo analysis that reported independent restaurants scoring approximately **44% worse** than chains.
- Identified repeated violation rows for the same restaurant inspection and recalculated the comparison with **one observation per inspection** (reported gap: about **41%**).
- Tested definitions of a chain based on **5+, 10+, or 20+** locations; the reported gap varied from **37% to 53%**.
- Compared restaurant types within cuisines; independents had higher average scores in **42 of 48** comparable cuisines (**87.5%**).

These are descriptive associations, not proof that inspection standards or treatment differ. Results are reported from the student's notebook and have not been independently reproduced for this portfolio.

## Files
- [`notebooks/DoU01_mariellj.py`](notebooks/DoU01_mariellj.py) — student's marimo notebook, with one unparseable duplicate text cell removed for portability.
- [`notebooks/DoU01_inherited.py`](notebooks/DoU01_inherited.py) — original inherited starter analysis, included for methodological comparison; course-provided material, not authored by the student.

## Run
Install Python 3.11+ and the notebook dependencies (`marimo`, `pandas`, `pyarrow`, `matplotlib`). From the project folder, run:

```bash
marimo edit notebooks/DoU01_mariellj.py
```

The notebook attempts to load `nyc_inspections.parquet` from the original course data location, then falls back to a course GitHub URL. Availability of the external dataset is not guaranteed.

## Attribution
The inherited notebook and assignment framing were provided as SI 385 coursework. The additional investigations, interpretations, and sensitivity analysis appear in the student notebook.
