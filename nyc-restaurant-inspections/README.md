[nyc_restaurant_README_recruiter.md](https://github.com/user-attachments/files/35129532/nyc_restaurant_README_recruiter.md)
# NYC Restaurant Health Inspection Analysis

**SI 385 · University of Michigan · Fall 2026**

**[View Notebook & Results](https://mariellj.github.io/si385-statistical-analysis/nyc-restaurant-inspections/analysis/)** · **[View Python Source Code](notebooks/DoU01_mariellj.py)**

## The question

Do independent restaurants receive higher health inspection scores than chains in NYC, and how much does that difference depend on how the data is analyzed? Higher scores mean more violation points.

## What I found

I started with a course-provided analysis reporting that independents scored **44% worse** than chains. I checked three decisions behind that figure:

- **Counting inspections:** Some inspections appeared on multiple rows because of separate violations. Counting each inspection once reduced the reported gap to **about 41%**.
- **Defining a chain:** Depending on whether a chain meant **5+, 10+, or 20+ locations**, the gap ranged from **37% to 53%**.
- **Comparing cuisines:** Independents had higher average scores in **42 of 48** cuisines where both groups could be compared.

## Takeaway

The overall pattern held across these checks, but the size of the gap changed with the analytical choices. These results show a difference in scores—not proof that inspectors treat independent restaurants differently.

**Tools:** Python, pandas, marimo, matplotlib · data cleaning, group comparisons, sensitivity analysis

*The starting analysis and assignment were course-provided. My additional checks and interpretations are documented in the linked notebook. The dataset is not included in this repository.*
