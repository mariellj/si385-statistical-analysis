# What Does a Mile Cost? — Used-Car Price Analysis

**SI 385 · University of Michigan · Fall 2026**

**[View Notebook & Results](https://mariellj.github.io/si385-statistical-analysis/DoU02-used-car-mileage/)** · **[View Python Source Code](notebook/DoU02_mj.py)** · **[View Decision Memo](decision_memo_only.pdf)**

## The question

How much should a credit union adjust a used car's estimated value for every additional 10,000 miles?

## What I found

I started with two course-provided regression analyses of Craigslist asking prices. I reproduced their estimates, added manufacturer to a third model, and checked whether differences came from model choices or the listings used.

- **Mileage only:** An estimated **$277 decrease** in asking price per additional 10,000 miles.
- **Mileage and age:** An estimated **$633 decrease** per additional 10,000 miles.
- **Mileage, age, and manufacturer:** My model estimated a **$757 decrease**. I also compared the models on the same listings to check the effect of sample selection.

## Takeaway

I recommended the simpler age-adjusted estimate of **about $630 per 10,000 miles** as a starting point, not a fixed lending rule. Adding more variables did not automatically make a model more useful for this decision. The data covers *asking prices*, not completed sales, so the recommendation would need more testing.

**Tools:** Python, pandas, statsmodels, marimo · OLS regression, model comparison, sensitivity analysis

*The starting analyses were provided for SI 385 coursework. My additional model, same-sample comparison, and recommendation are documented in the notebook and decision memo. The course dataset is not included in this repository.*
