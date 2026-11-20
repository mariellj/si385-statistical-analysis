[README.md](https://github.com/user-attachments/files/35127231/README.md)
# NYC Restaurant Health Inspection Analysis

**SI 385 | University of Michigan | Fall 2026**

I started this assignment with an analysis that said independent restaurants had inspection scores about 44% worse than chains in New York City. I wanted to know how much that number depended on the choices behind it.

**[View the analysis and findings](analysis/index.html)** · **[View my source code (Python / marimo)](notebooks/DoU01_mariellj.py)**

> The analysis link opens as a webpage once GitHub Pages is enabled. On GitHub itself, HTML files appear as code.

## The question

Are independent restaurants getting higher violation scores than chains? And does that difference change when we count inspections differently or change what qualifies as a chain?

Higher inspection scores mean more violation points, so a higher score is worse.

## 1. I started by checking the original result

The inherited notebook reported a **44% gap** between independent restaurants and chains. Before accepting that number, I looked at how the data was organized.

I found that a single inspection could show up on several rows when multiple violations were recorded. The inspection score was repeated across those rows, which could give some inspections extra weight.

**What changed:** When I counted each inspection once, the reported gap dropped to **about 41%**.

## 2. I tested what counts as a chain

The dataset didn't include a chain label. The original analysis treated restaurant names with **10 or more locations** as chains, so I checked other cutoffs:

| Minimum locations | Reported gap |
|---|---:|
| 5+ | 37% |
| 10+ (original) | 44% |
| 20+ | 53% |

This showed me that the headline could change quite a bit without changing the inspection scores themselves.

## 3. I compared restaurants within cuisines

I also wanted to see whether the overall pattern appeared within different types of food. Among **48 cuisines** where I could compare both groups, independents had higher average scores in **42 (87.5%)**.

## What I took away

The general pattern held up across several checks, but the exact percentage depended on how I defined and grouped the data. I wouldn't use the original 44% figure without explaining those decisions. The results describe score differences; they don't prove that inspectors treat independent restaurants differently.

## Explore the project

- **[View analysis and findings](analysis/index.html)** — a readable walkthrough of the results (publish with GitHub Pages).
- **[View my source code](notebooks/DoU01_mariellj.py)** — the Python/marimo notebook with my additional analysis.
- **[View the inherited notebook](notebooks/DoU01_inherited.py)** — the course-provided starting point, included for comparison.

**Tools:** Python, pandas, marimo, matplotlib, data grouping, exploratory analysis, sensitivity checks.

## Running the notebook

Install Python 3.11+ and `marimo`, `pandas`, `pyarrow`, and `matplotlib`. From the project directory:

```bash
marimo edit notebooks/DoU01_mariellj.py
```

The notebook first looks for `nyc_inspections.parquet` locally and otherwise tries the course GitHub dataset. The dataset isn't included here, and the external source may not always be available.

## Attribution and limitations

The original notebook and assignment framing were provided as SI 385 coursework. My added investigations and interpretations appear in `DoU01_mariellj.py`. The findings shown here come from that notebook and have not been independently reproduced for this portfolio.
