# ==========================================================
# Clean the Christchurch Airbnb dataset to remove missing prices and extreme outliers. 
# the output is a CSV file saved to the processed folder.
# ==========================================================

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
import numpy as np
from pathlib import Path
from Code.utils import custom_functions as cf
from paths import data_path

def main():
    # Load raw combined Airbnb dataset
    airbnb_chch = pd.read_csv(data_path("processed","chch_airbnb.csv"))

    # Summary before cleaning
    print("\nAirbnb summary before cleaning:")
    print(cf.summary_stats(airbnb_chch))

    # Select relevant columns
    col_to_keep = ['id', 'neighbourhood', 'latitude', 'longitude', 'price', 'month_year', 'room_type']
    airbnb_cleaned = airbnb_chch[col_to_keep].copy()

    # Remove listings with all missing prices
    missing_by_id = airbnb_cleaned.groupby("id")["price"].apply(lambda x: x.isna().all())
    airbnb_cleaned = airbnb_cleaned[~airbnb_cleaned["id"].isin(missing_by_id[missing_by_id].index)]

    # Impute missing prices using mean per ID
    mean_price_per_id = airbnb_cleaned.groupby("id")["price"].mean()
    airbnb_cleaned["price"] = airbnb_cleaned["price"].fillna(airbnb_cleaned["id"].map(mean_price_per_id))

    # Handle extreme outliers (>3000)
    grouped = airbnb_cleaned.groupby("id")
    ids_to_drop = []

    for listing_id, group in grouped:
        extreme_prices = group[group["price"] > 3000]
        reasonable_prices = group[group["price"] <= 3000]["price"]

        if len(extreme_prices) > 0:
            if len(reasonable_prices) == 0:
                ids_to_drop.append(listing_id)
            else:
                mean_price = reasonable_prices.mean()
                airbnb_cleaned.loc[(airbnb_cleaned["id"] == listing_id) &
                                   (airbnb_cleaned["price"] > 3000), "price"] = mean_price

    airbnb_cleaned = airbnb_cleaned[~airbnb_cleaned["id"].isin(ids_to_drop)]

    #print summary after cleaning
    print("\nAirbnb summary after cleaning:")
    print(cf.summary_stats(airbnb_cleaned))

    # Save cleaned Airbnb dataset
    output_file = data_path("processed", "airbnb_cleaned.csv")
    airbnb_cleaned.to_csv(output_file, index=False)
    print("Saved cleaned Airbnb dataset:", output_file)

if __name__ == "__main__":
    main()
