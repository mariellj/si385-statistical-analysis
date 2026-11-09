import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import statsmodels.formula.api as smf
    from pathlib import Path

    return Path, mo, pd, smf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 385 — Demonstration of Understanding 2
    ## What Does a Mile Cost?

    ### **Research question:** Which mileage adjustment should a credit union use when evaluating used-car asking prices?

    ### This analysis compares the estimates produced by Mensah and Varga, examines their analytical decisions, and evaluates whether an alternative model provides a more defensible estimate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Understanding Mensah's Regression

    Mensah uses a simple Ordinary Least Squares (OLS) regression to examine the relationship between vehicle mileage and asking price. His analysis uses mileage as the only independent variable, measuring it in increments of 10,000 miles.

    The regression estimates that for every additional 10,000 miles, a vehicle's asking price decreases by approximately $277 on average. This estimate comes from 4,086 listings.

    Mensah's approach provides a general understanding of how mileage relates to asking prices across the dataset. However, the regression does not account for other factors, such as vehicle age, condition, or manufacturer, that may also influence price.

    Analytical decision: Mensah chose a mileage-only regression without explicitly filtering out implausible listings. This makes his analysis straightforward, but it may not isolate the relationship between mileage and asking price from other vehicle characteristics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Understanding Varga's Regression

    Varga uses the same Craigslist dataset as Mensah but makes different decisions about data cleaning and the regression model. He removes listings with prices below $500 and odometer readings outside 100 to 500,000 miles using `listings["price"] >= 500` and `listings["odometer"].between(100, 500_000)`.

    Varga also creates an age variable using `cars["age"] = 2020 - cars["year"]` and runs a multiple OLS regression:

    `varga_model = smf.ols("price ~ miles_10k + age", data=cars).fit()`

    His regression uses 3,645 listings and estimates a $633 decrease in asking price for every additional 10,000 miles, holding vehicle age constant.

    Unlike Mensah, Varga accounts for vehicle age and excludes some potentially implausible listings. However, his filtering thresholds are choices that could affect the estimate. His model also does not account for vehicle condition or manufacturer.

    Varga's analysis provides a different estimate of the relationship between mileage and asking price, but we still need to determine how much of the difference comes from filtering the data versus including age.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## My Analysis: Understanding How Mileage Affects Car Prices

    After reviewing Mensah's and Varga's work, I wanted to understand why their results were so different, even though they used the same dataset. Mensah found that every additional 10,000 miles was linked to a $277 decrease in asking price, while Varga found a $633 decrease after filtering certain listings and accounting for vehicle age.

    For my analysis, I will first recreate both regressions to compare their results. Then, I will explore other vehicle characteristics, including model, condition, and manufacturer, to decide which variable would be useful to include in my own regression.

    My goal is to understand how these analytical decisions affect the mileage estimate and decide which approach makes the most sense for the credit union.
    """)
    return


@app.cell
def _(Path, pd):
    # Load the Craigslist dataset
    data_path = Path("data/craigslist_vehicles_sample.csv")

    if not data_path.exists():
        data_path = Path("../../data/craigslist_vehicles_sample.csv")

    listings = pd.read_csv(data_path, index_col=0)

    # Create mileage variable in units of 10,000 miles
    listings["miles_10k"] = listings["odometer"] / 10_000

    print(f"Total listings: {len(listings):,}")

    # Preview the variables we will analyze
    listings[["price", "year", "odometer", "condition"]].head()

    return (listings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Comparing Mensah's and Varga's Results

    I will recreate both regression models using the same dataset. Mensah uses mileage alone to estimate changes in asking price, while Varga removes certain listings and includes vehicle age. By comparing their results side by side, I can see how their different approaches affect the mileage estimate and the number of listings used.
    """)
    return


@app.cell
def _(listings, pd, smf):

    # Mensah's model: mileage only
    mensah_model = smf.ols(
        "price ~ miles_10k",
        data=listings
    ).fit()

    # Varga's model: filtered data with vehicle age
    filtered = listings[
        (listings["price"] >= 500)
        & listings["odometer"].between(100, 500_000)
    ].copy()

    filtered["age"] = 2020 - filtered["year"]

    varga_model = smf.ols(
        "price ~ miles_10k + age",
        data=filtered
    ).fit()

    # Compare the results
    comparison = pd.DataFrame({
        "Model": ["Mensah", "Varga"],
        "Mileage coefficient ($)": [
            round(mensah_model.params["miles_10k"], 2),
            round(varga_model.params["miles_10k"], 2)
        ],
        "Listings used": [
            int(mensah_model.nobs),
            int(varga_model.nobs)
        ],
        "R-squared": [
            round(mensah_model.rsquared, 3),
            round(varga_model.rsquared, 3)
        ]
    })

    comparison

    return filtered, mensah_model, varga_model


@app.cell
def _(listings):
    print("Unique vehicle models:", listings["model"].nunique())
    print("Missing model values:", listings["model"].isna().sum())
    print("Missing condition values:", listings["condition"].isna().sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My Regression: Including Vehicle Manufacturer

    After comparing Mensah's and Varga's results, I wanted to see if including another vehicle characteristic would change the mileage estimate. I first looked at vehicle model and condition, but found 2,127 different models and 2,213 listings missing condition information.

    I decided to use manufacturer because it allows me to account for differences between vehicle brands without making the regression too complicated. I will use Varga's filtered data and include mileage, age, and manufacturer in my model.
    """)
    return


@app.cell
def _(filtered, smf):

    # My model: Varga's approach with manufacturer included
    my_model = smf.ols(
        "price ~ miles_10k + age + C(manufacturer)",
        data=filtered
    ).fit()

    print("My mileage estimate:", round(my_model.params["miles_10k"], 2))
    print("Listings used:", int(my_model.nobs))
    print("R-squared:", round(my_model.rsquared, 3))

    return (my_model,)


@app.cell
def _(mensah_model, my_model, pd, varga_model):

    # Compare all three mileage estimates
    final_comparison = pd.DataFrame({
        "Model": ["Mensah", "Varga", "My model"],
        "Mileage estimate ($)": [
            round(mensah_model.params["miles_10k"], 2),
            round(varga_model.params["miles_10k"], 2),
            round(my_model.params["miles_10k"], 2)
        ],
        "Listings used": [
            int(mensah_model.nobs),
            int(varga_model.nobs),
            int(my_model.nobs)
        ],
        "R-squared": [
            round(mensah_model.rsquared, 3),
            round(varga_model.rsquared, 3),
            round(my_model.rsquared, 3)
        ]
    })

    final_comparison

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Checking the Effect of Manufacturer

    After running my regression, I wanted to understand whether the change in the mileage estimate came from adding manufacturer or from using fewer listings.

    To check this, I ran Varga's regression again using the same 3,529 listings as my model. This allows me to compare the two regressions using the same vehicles and see how much adding manufacturer changes the estimate.
    """)
    return


@app.cell
def _(filtered, my_model, smf):

    # Compare the two models using the same listings
    same_cars = filtered.loc[my_model.model.data.row_labels]

    same_sample_varga = smf.ols(
        "price ~ miles_10k + age",
        data=same_cars
    ).fit()

    print("Varga on same sample:",
          round(same_sample_varga.params["miles_10k"], 2))
    print("My model:",
          round(my_model.params["miles_10k"], 2))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion: Choosing a Mileage Adjustment

    After comparing the three regressions, I would recommend Varga's estimate of approximately $630 per 10,000 miles as a starting point for the credit union. His model accounts for vehicle age and removes listings with potentially unrealistic prices or mileage, making it a more reasonable choice than Mensah's mileage-only approach.

    My regression included manufacturer and produced a higher estimate of $757.39, with an R-squared of 0.438. However, after comparing both models using the same 3,529 listings, I found that changing the sample had a bigger impact on the mileage estimate than adding manufacturer.

    This helped me understand that a more detailed model does not always mean a better recommendation. Although my model explains more of the variation in asking prices, it also uses fewer listings and includes more variables.

    I would choose Varga's estimate because it is simpler and accounts for vehicle age while keeping more listings. However, I would recommend more testing before the credit union uses this as a fixed lending rule. Since the data comes from Craigslist asking prices rather than completed sales, I would also want to compare these estimates with actual sale prices before making a final lending decision.
    """)
    return


if __name__ == "__main__":
    app.run()
