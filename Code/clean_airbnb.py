# ==========================================================
# Clean the Christchurch Airbnb dataset to remove missing
# prices and extreme outliers.
# The output is a CSV file saved to the processed folder.
# ==========================================================

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from Code.utils import custom_functions as cf
from paths import data_path
from config import AIRBNB_EXTREME_PRICE_THRESHOLD


def main():

    # ----------------------------------------------------------
    # 1. Load combined Airbnb dataset
    # ----------------------------------------------------------

    airbnb_chch = pd.read_csv(
        data_path(
            "processed",
            "chch_airbnb.csv"
        )
    )

    print("\nAirbnb summary before cleaning:")

    print(
        cf.summary_stats(
            airbnb_chch
        )
    )

    # ----------------------------------------------------------
    # 2. Select relevant columns
    # ----------------------------------------------------------

    col_to_keep = [
        "id",
        "neighbourhood",
        "latitude",
        "longitude",
        "price",
        "month_year",
        "room_type"
    ]

    airbnb_cleaned = (
        airbnb_chch[
            col_to_keep
        ]
        .copy()
    )

    # ----------------------------------------------------------
    # 3. Check for duplicate listing-month observations
    # ----------------------------------------------------------

    duplicates = airbnb_cleaned.duplicated(
        subset=[
            "id",
            "month_year"
        ],
        keep=False
    )

    print(
        "\nNumber of duplicate listing-month rows:",
        duplicates.sum()
    )

    # ----------------------------------------------------------
    # 4. Remove listings where ALL prices are missing
    # ----------------------------------------------------------

    missing_by_id = (
        airbnb_cleaned
        .groupby("id")["price"]
        .apply(
            lambda x: x.isna().all()
        )
    )

    ids_all_missing = (
        missing_by_id[
            missing_by_id
        ]
        .index
    )

    print(
        "Listings with all prices missing:",
        len(ids_all_missing)
    )

    airbnb_cleaned = (
        airbnb_cleaned[
            ~airbnb_cleaned["id"].isin(
                ids_all_missing
            )
        ]
        .copy()
    )

    # ----------------------------------------------------------
    # 5. Impute partially missing prices
    #
    # Fill only missing observations using the mean observed
    # price for the SAME Airbnb listing.
    # ----------------------------------------------------------

    mean_price_per_id = (
        airbnb_cleaned
        .groupby("id")["price"]
        .mean()
    )

    airbnb_cleaned["price"] = (
        airbnb_cleaned["price"]
        .fillna(
            airbnb_cleaned["id"]
            .map(mean_price_per_id)
        )
    )

    # ----------------------------------------------------------
    # 6. Handle extreme prices
    #
    # Prices above the configured threshold are considered
    # extreme.
    #
    # If a listing has at least one reasonable observed price,
    # extreme values are replaced using the listing's mean
    # reasonable price.
    #
    # If every price for the listing is extreme, the listing is
    # removed because there is no reasonable price available.
    # ----------------------------------------------------------

    grouped = airbnb_cleaned.groupby(
        "id"
    )

    ids_to_drop = []

    for listing_id, group in grouped:

        extreme_prices = group[
            group["price"]
            > AIRBNB_EXTREME_PRICE_THRESHOLD
        ]

        reasonable_prices = group[
            group["price"]
            <= AIRBNB_EXTREME_PRICE_THRESHOLD
        ]["price"]

        if len(extreme_prices) > 0:

            if len(reasonable_prices) == 0:

                ids_to_drop.append(
                    listing_id
                )

            else:

                mean_reasonable_price = (
                    reasonable_prices.mean()
                )

                airbnb_cleaned.loc[
                    (
                        airbnb_cleaned["id"]
                        == listing_id
                    )
                    &
                    (
                        airbnb_cleaned["price"]
                        > AIRBNB_EXTREME_PRICE_THRESHOLD
                    ),
                    "price"
                ] = mean_reasonable_price

    airbnb_cleaned = (
        airbnb_cleaned[
            ~airbnb_cleaned["id"]
            .isin(ids_to_drop)
        ]
        .copy()
    )

    # ----------------------------------------------------------
    # 7. Sanity checks
    # ----------------------------------------------------------

    print(
        "\n=== AIRBNB CLEANING SANITY CHECKS ==="
    )

    print(
        "Final row count:",
        len(airbnb_cleaned)
    )

    print(
        "Final unique listing IDs:",
        airbnb_cleaned["id"].nunique()
    )

    print(
        "Missing prices:",
        airbnb_cleaned["price"]
        .isna()
        .sum()
    )

    print(
        "Non-positive prices:",
        (
            airbnb_cleaned["price"]
            <= 0
        )
        .sum()
    )

    print(
        "Rows above extreme-price threshold:",
        (
            airbnb_cleaned["price"]
            > AIRBNB_EXTREME_PRICE_THRESHOLD
        )
        .sum()
    )

    print(
        "Duplicate listing-month rows:",
        airbnb_cleaned
        .duplicated(
            subset=[
                "id",
                "month_year"
            ]
        )
        .sum()
    )

    # ----------------------------------------------------------
    # 8. Summary after cleaning
    # ----------------------------------------------------------

    print(
        "\nAirbnb summary after cleaning:"
    )

    print(
        cf.summary_stats(
            airbnb_cleaned
        )
    )

    # ----------------------------------------------------------
    # 9. Save cleaned Airbnb dataset
    # ----------------------------------------------------------

    output_file = data_path(
        "processed",
        "airbnb_cleaned.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    airbnb_cleaned.to_csv(
        output_file,
        index=False
    )

    print(
        "\nSaved cleaned Airbnb dataset:",
        output_file
    )


if __name__ == "__main__":
    main()