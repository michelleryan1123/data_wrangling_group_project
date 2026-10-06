# ==========================================================
# Reusable helper functions for the DATA422 project
# ==========================================================

import os

import pandas as pd


# ----------------------------------------------------------
# Load one Airbnb CSV, keep Christchurch listings,
# and create a consistent month_year label.
# ----------------------------------------------------------

def load_christchurch(file_name):

    df = pd.read_csv(
        file_name
    )

    # Keep Christchurch City listings only
    df = df[
        df["neighbourhood_group"]
        == "Christchurch City"
    ].copy()

    # Extract month/year from filename
    #
    # Example:
    # Oct26_listings.csv -> OCT26
    month_year = (
        os.path.basename(file_name)
        .replace(
            "_listings.csv",
            ""
        )
        .upper()
    )

    # Standardise full month names if they occur
    month_year = (
        month_year
        .replace(
            "APRIL",
            "APR"
        )
        .replace(
            "JUNE",
            "JUN"
        )
    )

    # Correct the known Deliverable 3 year-label issue.
    #
    # The intended study period begins in October 2025,
    # not October 2026.
    month_corrections = {
        "OCT26": "OCT25",
        "NOV26": "NOV25",
        "DEC26": "DEC25"
    }

    month_year = (
        month_corrections.get(
            month_year,
            month_year
        )
    )

    df["month_year"] = (
        month_year
    )

    return df


# ----------------------------------------------------------
# Calculate general summary statistics for a dataframe
# ----------------------------------------------------------

def summary_stats(df):

    summary = {
        "total-count":
            len(df),

        "data_type":
            df.dtypes,

        "count_na":
            df.isna().sum(),

        "count_unique":
            df.nunique(),

        "mean":
            df.mean(
                numeric_only=True
            ),

        "min":
            df.min(
                numeric_only=True
            ),

        "max":
            df.max(
                numeric_only=True
            ),

        "std_dev":
            df.std(
                numeric_only=True
            )
    }

    return pd.DataFrame(
        summary
    )


# ----------------------------------------------------------
# Select approximately the top 10% of listings based on
# number_of_reviews and calculate summary statistics.
# ----------------------------------------------------------

def highest_reviews(df):

    # Calculate the 90th percentile.
    # Listings at or above this threshold belong to
    # approximately the highest 10%.
    threshold = (
        df["number_of_reviews"]
        .quantile(0.9)
    )

    top10per = (
        df[
            df["number_of_reviews"]
            >= threshold
        ]
        .copy()
    )

    top10_summary = (
        summary_stats(
            top10per
        )
    )

    # chch_airbnb_stats.py expects:
    #
    # top10per, top10_summary = highest_reviews(df)
    return (
        top10per,
        top10_summary
    )