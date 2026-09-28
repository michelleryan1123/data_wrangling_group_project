## Load and clean the tenancy dataset for the same timeframe as the Airbnb dataset (Oct 2025 - Jun 2026)

# Add project root to Python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from pathlib import Path
from paths import data_path

# set start and end dates for the Airbnb dataset timeframe
start_date = pd.Timestamp("2025-10-01")
end_date = pd.Timestamp("2026-06-30")

def main():
    tenancy = pd.read_csv(data_path("raw","Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"))

    # Convert TimeFrame → datetime
    tenancy["TimeFrame"] = pd.to_datetime(tenancy["TimeFrame"], format="%d/%m/%Y", errors="coerce")

    # Filter to Airbnb timeframe

    tenancy_filtered = tenancy[tenancy["TimeFrame"].between(start_date, end_date)].copy()

    # Remove missing Location Id
    tenancy_cleaned = tenancy_filtered[tenancy_filtered["Location Id"].notna()].copy()

    # Remove Location Id = -99
    tenancy_cleaned = tenancy_cleaned[tenancy_cleaned["Location Id"] != -99].copy()

    # Fix datatype
    tenancy_cleaned["Location Id"] = tenancy_cleaned["Location Id"].astype("int64")

    # Handle missing Number Of Beds
    tenancy_cleaned["Number Of Beds"] = (
        tenancy_cleaned["Number Of Beds"]
        .astype("string")
        .fillna("Unknown")
        .str.strip()
    )

    # Standardise Dwelling Type
    tenancy_cleaned["Dwelling Type"] = (
        tenancy_cleaned["Dwelling Type"]
        .astype("string")
        .str.strip()
    )

    # Save cleaned tenancy dataset
    output_file = data_path("processed", "tenancy_cleaned_oct25_jun26.csv")
    tenancy_cleaned.to_csv(output_file, index=False)
    print("Saved cleaned tenancy dataset:", output_file)

if __name__ == "__main__":
    main()
