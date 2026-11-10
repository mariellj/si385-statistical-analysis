# SI 385 — Statistical Analysis Projects

**University of Michigan · School of Information · Fall 2026**

A portfolio of applied statistical analysis projects examining how data preparation, model selection, and analytical assumptions affect real-world conclusions.

## Projects

### 01 — [NYC Restaurant Health Inspection Analysis](nyc-restaurant-inspections/)

**Research question:** How sensitive is the difference in NYC restaurant inspection scores between independent and chain restaurants to analytical decisions?

Audited an inherited analysis, addressed repeated violation rows, tested alternative definitions of a chain, and compared results within cuisine groups. The estimated score gap changed under different analytical choices, illustrating the importance of sensitivity analysis. These descriptive differences do not establish unequal enforcement.

**Methods:** Data cleaning, descriptive statistics, grouped comparisons, sensitivity analysis  
**Tools:** Python, pandas, marimo

[Read the project and view the notebook](nyc-restaurant-inspections/)

### 02 — [What Does a Mile Cost? Used Vehicle Price Analysis](DoU02-used-car-mileage/)

**Research question:** Which mileage adjustment should a credit union consider when evaluating used-car asking prices?

Compared three ordinary least squares models: mileage only (approximately **−$277** per additional 10,000 miles), mileage plus vehicle age (**−$633**), and mileage plus age and manufacturer (**−$757**). Conducted a same-sample comparison and recommended the simpler age-adjusted estimate as a provisional starting point, not a final lending rule.

**Methods:** OLS regression, categorical controls, model comparison, same-sample sensitivity checks  
**Tools:** Python, pandas, statsmodels, marimo

[Read the project, view notebook exports, and access the decision memo](DoU02-used-car-mileage/)

## Skills demonstrated

Python · pandas · statsmodels · statistical modeling · data cleaning · exploratory analysis · sensitivity analysis · data interpretation · analytical communication · marimo

## Attribution and reproducibility

These projects were completed as part of SI 385 coursework. Each project README distinguishes inherited course-provided analyses from my additional work. Course datasets are not included. Findings are from coursework analyses and have not been independently validated as policy recommendations.
