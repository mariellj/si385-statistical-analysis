# DoU02 — What Does a Mile Cost?

**SI 385 | Statistical Analysis | University of Michigan**

## Question
Which mileage adjustment should a credit union consider when evaluating used-car asking prices?

## Overview
This project re-examines two inherited ordinary least squares (OLS) analyses of Craigslist vehicle listings. The original analysts estimated approximately **-$277** (mileage only) and **-$633** (mileage plus vehicle age) per additional 10,000 miles. I reproduced these estimates, tested a third model controlling for manufacturer, and investigated whether sample selection influenced the comparison.

## Approach and findings
- Reproduced the original mileage-only model on **4,086** listings and the age-adjusted model on **3,645** listings.
- Fit an age- and manufacturer-adjusted model on **3,529** listings; its mileage coefficient was approximately **-$757.39 per 10,000 miles**.
- Re-ran the age-adjusted model on the same 3,529 listings to separate changes in the model specification from changes in the sample.
- Recommended the simpler age-adjusted estimate (approximately **-$630 per 10,000 miles**) as a provisional starting point, not a final lending rule. Craigslist *asking prices* are not completed sale prices, and unobserved condition or other vehicle characteristics may matter.

## Skills and tools
Python, pandas, statsmodels, OLS regression, categorical controls, model comparison, data filtering, sensitivity analysis, marimo.

## Files
- [`notebook/DoU02_mj.py`](notebook/DoU02_mj.py) — my marimo analysis notebook.
- [`notebook/DoU02_mj.html`](notebook/DoU02_mj.html) — exported notebook for viewing results.
- [`docs/decision_memo_and_revision.pdf`](docs/decision_memo_and_revision.pdf) — decision memo and revision account.

## Reproducibility
The notebook expects the course dataset at `data/craigslist_vehicles_sample.csv` (or `../../data/craigslist_vehicles_sample.csv`). The dataset is **not included** in this repository. To run it, use a local copy obtained through an authorized source and install `marimo`, `pandas`, and `statsmodels`.

## Attribution
The Mensah and Varga analyses were inherited reference notebooks supplied as part of the SI 385 course assignment. Their source files are not redistributed here. My notebook reproduces their models for comparison and adds the manufacturer-adjusted analysis and same-sample check.
