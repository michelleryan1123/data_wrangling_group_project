# =======================================================
# Join Airbnb + Tenancy datasets using SA2 + year quarter. Output is a CSV file saved to the processed folder.
# =======================================================

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from paths import data_path
import pandas as pd


def main():

    print("\n=== STEP 6: JOIN AIRBNB + TENANCY DATASETS ===")

    # 1. Load Airbnb with SA2 codes
    airbnb = pd.read_csv(
        data_path("processed", "airbnb_with_sa2.csv"),
        dtype={"sa2_code": "string"}
    )

    # 2. Convert Airbnb months to quarters
    month = airbnb["month_year"].str.upper()
    month = month.str.replace("APRIL", "APR", regex=False)
    month = month.str.replace("JUNE", "JUN", regex=False)
    month = month.str.replace("JLY", "JUL", regex=False)

    airbnb["quarter"] = (
        pd.to_datetime(month, format="%b%y")
        .dt.to_period("Q")
        .dt.start_time
    )

    # 3. Load Tenancy
    tenancy = pd.read_csv(
        data_path("processed", "tenancy_cleaned.csv"),
        dtype={"Location Id": "string"}
    )

    print("Loaded tenancy dataset:", tenancy.shape)
    print(tenancy.head())

    # Select overall rental records
    tenancy = tenancy[
        (tenancy["Dwelling Type"] == "ALL") &
        (tenancy["Number Of Beds"] == "ALL")
    ].copy()

    tenancy["quarter"] = pd.to_datetime(tenancy["TimeFrame"])

    # 4. Check Tenancy join keys are unique
    assert not tenancy.duplicated(["Location Id", "quarter"]).any()

    # 5. Join using area code AND quarter
    joined = airbnb.merge(
        tenancy,
        left_on=["sa2_code", "quarter"],
        right_on=["Location Id", "quarter"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    # 6. Validate
    print("===== JOIN VALIDATION =====")
    print("Original Airbnb rows:", len(airbnb))
    print("Joined rows:", len(joined))

    assert len(joined) == len(airbnb)

    print("\nJoin results:")
    print(joined["_merge"].value_counts())

    print("\nJoin results by quarter:")
    print(
        pd.crosstab(
            joined["quarter"],
            joined["_merge"]
        )
    )

    # 7. Check Christchurch Central
    central = joined[joined["sa2_code"] == "326600"]

    print("\n===== CHRISTCHURCH CENTRAL =====")
    print("Airbnb observations:", len(central))
    print("Median Airbnb nightly price:", central["price"].median())

    print("\nTenancy median rent by quarter:")
    print(
        central.groupby("quarter")["Median Rent"].first()
    )

    # 8. Save
    output_file = data_path("processed", "airbnb_tenancy_joined.csv")
    joined.to_csv(output_file, index=False)

    print("\nJoined dataset saved successfully:", output_file)


if __name__ == "__main__":
    main()
