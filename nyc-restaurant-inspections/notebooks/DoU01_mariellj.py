# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.23.3",
#     "pandas>=3.0.5",
#     "pyarrow>=25.0.1",
#     "matplotlib>=3.9",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import urllib.request
    from io import BytesIO
    from pathlib import Path

    import pandas as pd
    import matplotlib.pyplot as plt

    REMOTE = ("https://raw.githubusercontent.com/"
              "cteplovs/si385-fa2026-student/main/data/")

    def course_parquet(name):
        try:
            local = Path(__file__).resolve().parents[2] / "data" / name
            if local.exists():
                return pd.read_parquet(local)
        except (NameError, IndexError, OSError):
            pass
        with urllib.request.urlopen(REMOTE + name) as _response:
            return pd.read_parquet(BytesIO(_response.read()))

    return course_parquet, mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Are independent restaurants held to a different standard?

    ## Briefing note for the Small Business Services committee — draft 3

    *R. Okonjo, Office of Data Analytics.  Handed over on leaving.*

    ---

    The committee asked whether the chains have an advantage in health
    inspections.  This notebook is the analysis behind the headline number in the
    briefing.

    **Finding: independent restaurants score about 44% worse than chain
    restaurants.**  A higher score is worse — the score counts violation points,
    so zero is a clean inspection.

    Anyone picking this up: the numbers regenerate from the source file, and the
    committee wants the figure updated before the March session.
    """)
    return


@app.cell
def _(course_parquet):
    inspections = course_parquet("nyc_inspections.parquet")
    inspections.head()
    return (inspections,)


@app.cell
def _(inspections):
    # How big is this thing.
    print(f"{len(inspections):,} rows")
    print(f"{inspections['restaurant_id'].nunique():,} restaurants")
    print(f"{inspections['inspection_date'].min()} to {inspections['inspection_date'].max()}")
    return


@app.cell
def _(inspections, pd):
    # The file has no chain flag, so build one from the trading name.  A name
    # operating at ten or more restaurant_ids is a chain.
    locations = inspections.groupby("name")["restaurant_id"].nunique()
    chain_names = set(locations[locations >= 10].index)

    flagged = inspections.copy()
    flagged["kind"] = pd.Categorical(
        flagged["name"].isin(chain_names).map({True: "chain", False: "independent"}),
        categories=["chain", "independent"],
    )

    print(f"{len(chain_names)} chain names, "
          f"{flagged['kind'].value_counts()['chain']:,} of the rows")
    return flagged, locations


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Show every row for restaurant 30075445 on August 1, 2023. After recognizing that a restaurant can have multiple rows because of multiple violations, we want to see whether the inspection score changes across those rows.
    """)
    return


@app.cell
def _(inspections):
    inspections[
        (inspections["restaurant_id"] == "30075445") &
        (inspections["inspection_date"] == "2023-08-01")
    ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Discovery
    Finding: The same restaurant and inspection date appears three times with different violations, but the inspection score remains 38 in every row. This shows that one inspection can appear multiple times in the dataset. Because Okonjo calculates the mean using every row, inspections with more violation records may have more influence on the headline score.
    """)
    return


@app.cell
def _(flagged):
    # The headline comparison.
    summary = flagged.groupby("kind", observed=True)["score"].agg(["count", "mean"])
    summary["mean"] = summary["mean"].round(2)
    summary
    return (summary,)


@app.cell
def _(summary):
    gap = summary.loc["independent", "mean"] - summary.loc["chain", "mean"]
    pct = 100 * gap / summary.loc["chain", "mean"]
    print(f"independents score {gap:.2f} points worse, which is {pct:.0f}%")
    return


@app.cell
def _(flagged, plt):
    # Distribution behind the two means.
    _fig, _ax = plt.subplots(figsize=(7, 4))
    for _k, _c in [("chain", "#4477aa"), ("independent", "#ee6677")]:
        _ax.hist(flagged.loc[flagged["kind"] == _k, "score"],
                 bins=40, range=(0, 80), alpha=0.55, label=_k,
                 density=True, color=_c)
    _ax.set_xlabel("inspection score (higher is worse)")
    _ax.set_ylabel("density")
    _ax.legend(frameon=False)
    _fig
    return


@app.cell
def _(flagged):
    # Holds up across the boroughs too.
    flagged.groupby(["borough", "kind"], observed=True)["score"].mean().unstack().round(2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## For the briefing

    Independents run about 44% above the chains on inspection score, and the
    pattern holds in every borough. The committee's line can be that the gap is
    real and consistent across the city.

    ### Still to do

    - Update before the March session.
    - Committee asked for a borough breakdown in the appendix; the table above
      will do.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Alternative Analysis
    One Observation Per Inspection
    Okonjo's original analysis calculates the mean using every row in the dataset. Since one inspection can appear across multiple rows when several violations are recorded, I will group records by restaurant and inspection date. Each inspection will contribute its score once, while the number of violation records associated with that inspection will still be preserved.
    """)
    return


@app.cell
def one_observation_per_inspection(flagged):
    one_per_inspection = (
        flagged.groupby(
            ["restaurant_id", "inspection_date", "kind"],
            observed=True
        )
        .agg(
            score=("score", "first"),
            violations=("violation", "count")
        )
        .reset_index()
    )

    one_per_inspection.head()
    return (one_per_inspection,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Recalculating the Headline Comparison
    Now that each row represents one inspection instead of one violation record, I will recalculate the mean inspection score for chain and independent restaurants. This allows me to compare Okonjo's original result to a version where each inspection contributes to the mean only once.
    """)
    return


@app.cell
def _(one_per_inspection):
    new_summary = (
        one_per_inspection.groupby("kind", observed=True)["score"]
        .agg(["count", "mean"])
        .round(2)
    )

    new_summary
    return (new_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Calculate the New Percentage Difference
    Using the new mean scores, I will calculate the percentage difference between independent and chain restaurants using the same formula as the original analysis. This will show whether the original 44% headline changes when each inspection is counted once.
    """)
    return


@app.cell
def recalculated_headline(new_summary):
    new_gap = (
        new_summary.loc["independent", "mean"]
        - new_summary.loc["chain", "mean"]
    )

    new_pct = 100 * new_gap / new_summary.loc["chain", "mean"]

    print(f"Independents score {new_gap:.2f} points worse, which is {new_pct:.0f}%")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Findings: Okonjo's row-level approach increases the estimated difference somewhat, but the broader conclusion that independents have higher average scores survives when each inspection is counted once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Cost of this alternative
    Counting each inspection only once treats an inspection with one violation record the same as an inspection with several violation records. Although I preserve the number of violations in the violations column, those additional violations no longer give an inspection more weight in the average.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Investigating the Chain Definition
    Since the dataset does not provide a chain indicator, this threshold is an analytical choice. Before changing the threshold, I want to understand how many restaurant names operate at 5, 10, and 20 or more locations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Okonjo already created the locations variable, which counts the number of unique restaurant IDs associated with each restaurant name. He then defines a chain as a restaurant name with 10 or more locations. Using his existing definition of locations, I will count how many restaurant names have 5+, 10+, and 20+ locations to better understand the impact of the 10-location threshold.
    """)
    return


@app.cell
def _(locations):
    print("5+ locations:", (locations >= 5).sum())
    print("10+ locations:", (locations >= 10).sum())
    print("20+ locations:", (locations >= 20).sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finding: The number of restaurant names classified as chains changes substantially depending on the threshold. A 5+ location definition includes 302 restaurant names, Okonjo's 10+ definition includes 109, and a stricter 20+ definition includes only 49. This shows that the 10-location cutoff has a meaningful effect on which restaurants are considered chains.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Testing Different Chain Thresholds
    Since the number of restaurants classified as chains changes across the 5+, 10+, and 20+ location thresholds, I will calculate the headline percentage under each definition. I will keep the rest of Okonjo's original analysis the same so that the chain threshold is the only decision being changed.
    """)
    return


@app.cell
def chain_threshold_test(inspections, locations):
    for cutoff in [5, 10, 20]:
        chain_names_test = set(locations[locations >= cutoff].index)

        threshold_test = inspections.copy()
        threshold_test["test_kind"] = threshold_test["name"].isin(
            chain_names_test
        ).map({True: "chain", False: "independent"})

        threshold_means = threshold_test.groupby("test_kind")["score"].mean()

        threshold_gap = (
            threshold_means["independent"] - threshold_means["chain"]
        )
    
        threshold_pct = (
            100 * threshold_gap / threshold_means["chain"]
        )

        print(
            f"{cutoff}+ locations: "
            f"{threshold_gap:.2f} points worse, "
            f"{threshold_pct:.0f}%"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finding: The headline result changes depending on how a chain is defined. Using a 5+ location threshold, independent restaurants score 37% worse than chains. Okonjo's 10+ threshold produces the original 44%, while a stricter 20+ threshold increases the difference to 53%. This shows that the headline is sensitive to the decision of where to set the chain threshold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Restaurants Between the 5+ and 10+ Thresholds
    Changing the chain threshold from 10+ to 5+ locations changes the headline from 44% to 37%. To understand why, I will examine the restaurant names with 5–9 locations. Okonjo's definition classifies these restaurants as independent, while the 5+ alternative would classify them as chains.
    """)
    return


@app.cell
def _(locations):
    middle_restaurants = locations[
        (locations >= 5) & (locations < 10)
    ]

    middle_restaurants.sort_values(ascending=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finding: There are 193 restaurant names with 5–9 locations that Okonjo's 10+ threshold classifies as independent. Some restaurant names have as many as 9 separate locations but fall just below his cutoff. This shows that the independent category includes multi-location restaurants, making the choice of where to separate chains from independents important to the headline result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Checking Okonjo's Result Within Cuisine
    Okonjo's analysis compares chain and independent restaurants overall and across boroughs, but restaurant cuisine may also be related to inspection scores. I will keep Okonjo's original 10+ location definition and compare chain and independent inspection scores within cuisine. This allows me to check whether his overall pattern survives when cuisine is considered.
    """)
    return


@app.cell
def _(flagged):
    cuisine_results = flagged.groupby(
        ["cuisine", "kind"]
    )["score"].mean().unstack()

    cuisine_results
    return (cuisine_results,)


@app.cell
def _(cuisine_results):
    cuisine_compare = cuisine_results.dropna()

    cuisine_compare.round(2)
    return (cuisine_compare,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In how many cuisines do independents score worse than chains?
    """)
    return


@app.cell
def cuisine_comparison(cuisine_compare):
    (cuisine_compare["independent"] > cuisine_compare["chain"]).value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finding: Of the 48 cuisines where both chain and independent restaurants could be compared, independent restaurants had higher average inspection scores in 42 cuisines (87.5%). Only 6 cuisines showed the opposite pattern. This suggests that Okonjo's overall finding generally holds when cuisine is considered, although the difference is not consistent across every cuisine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conclusion
    Okonjo's overall finding is supported by the data, but the exact 44% difference is sensitive to analytical decisions. Counting each inspection once reduced the gap to about 41%, while changing the chain threshold produced differences ranging from 37% to 53%. However, independents still had worse average scores in 42 of 48 comparable cuisines (87.5%). Overall, independent restaurants generally score worse than chains, but the size of the difference depends heavily on how the data is defined and analyzed.
    """)
    return


if __name__ == "__main__":
    app.run()
