import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
pd.set_option('display.max_columns', None)
import glob
import numpy as np
from paths import data_path

import Code.utils.custom_functions as cf  # import the custom functions from the utils folder


def main():
    # Read through all the *_listings.csv files in the data folder
    # Filter out chch listings and add a month_year column

    chch_data = []  # create an empty dataframe to store the filtered Christchurch datasets

    for file in glob.glob(str(data_path("raw", "*_listings.csv"))):
        chch = cf.load_christchurch(file)
        chch_data.append(chch)

    chch_airbnb = pd.concat(chch_data, ignore_index=True)

    print(chch_airbnb.head())
    print("\nAirbnb month/year groups after label correction:")
    print(chch_airbnb["month_year"].value_counts())

    # Save output to data/processed/
    output_file = data_path("processed", "chch_airbnb_oct25_jun26.csv")
    chch_airbnb.to_csv(output_file, index=False)

    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()
