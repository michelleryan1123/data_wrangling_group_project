# ======================================
# Deliverable 4: Cleaning The Datasets
# ======================================

# Import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Import the custom functions from the utils folder
from utils import custom_functions as cf 

# ============================================================
# Airbnb Data: Load and Initial Inspection
# ============================================================

# Load the combined Christchurch Airbnb dataset
airbnb_chch = pd.read_csv("Data\\chch_airbnb_oct25_jun26.csv")

# Correct month labels inherited from Deliverable 3
month_label_corrections = {
    "OCT26": "OCT25",
    "NOV26": "NOV25",
    "DEC26": "DEC25"
}

airbnb_chch["month_year"] = (
    airbnb_chch["month_year"]
    .replace(month_label_corrections)
)

# Verify corrected month labels
print("\nAirbnb month/year groups after label correction:")
print(
    airbnb_chch["month_year"]
    .value_counts()
)

# Record the dataset size before cleaning
pre_clean_size = airbnb_chch.shape # Number of rows, cols before cleaning
print("\nAirbnb dataset shape before cleaning:")
print(pre_clean_size)

# Display column names
col_names = airbnb_chch.columns # Get the column names
print(col_names)

# Summary statistics for the dataset before cleaning
print("\nAirbnb summary statistics before cleaning:")
summary_all = cf.summary_stats(airbnb_chch) # Calculate summary stats for the filtered
print(summary_all)

# ============================================================
# Airbnb Data: Select Relevant Columns
# ============================================================

# Define the columns to keep for the cleaned dataset
col_to_keep = ['id', 'neighbourhood', 'latitude', 'longitude', 'price', 'month_year', 'room_type']

airbnb_cleaned = airbnb_chch[col_to_keep].copy() # Create a new dataframe with only the columns to keep
airbnb_filtered = airbnb_cleaned.shape # Number of rows, cols after filtering to keep only the columns we want
print(airbnb_filtered)

# Look at the strucutre of the filtered dataset
# Print the structure of the filtered dataset
print(airbnb_cleaned.info())

# Get some summary statistics for the filtered dataset
print("\nAirbnb summary statistics after selecting columns:")
summary_stats = cf.summary_stats(airbnb_cleaned)
print(summary_stats)

# ============================================================
# Airbnb Data: Duplicate Check
# ============================================================

# Check for duplicates in the dataset 
# As dataset spans multiple months we can't just use property id to check for duplicates, we need to use a combination of property id and month_year
duplicates = airbnb_cleaned.duplicated(subset=['id', 'month_year'], keep= False) # Check for duplicate rows based on property id and month_year
print(f"Number of duplicates found: {duplicates.sum()}")

# No duplicates found

# ============================================================
# Airbnb Data: Missing Price Values
# ============================================================

# There are 10667 missing values in the 'price' column

# Check for properties that have no price at all
missing_by_id = (airbnb_cleaned
    .groupby("id")["price"] # group by property id and get the price column
    .apply(lambda x: x.isna().all()) # check if all the prices for that property id are missing - returns true if all prices are missing, false otherwise
)

missing_by_id = missing_by_id[missing_by_id] # filter to only 'True' values (all missing prices)
print("sum of properties with all missing prices: ", missing_by_id.sum())

# Drop the properties that have no prices for all months
airbnb_cleaned = airbnb_cleaned[~airbnb_cleaned["id"].isin(missing_by_id.index)]

# Check number of missing prices per month
missing_by_month =airbnb_cleaned.groupby("month_year")["price"].apply(lambda x: x.isna().mean()*100)
print(missing_by_month)

# Impute missing prices using the mean observed price for each property
mean_price_per_id = (
    airbnb_cleaned
    .groupby("id")["price"] # group by property id and get the price column
    .mean() # calculate the mean price for each property id
)

airbnb_cleaned["price"] = airbnb_cleaned["price"].fillna( # impute the missing prices with the mean price for that property id
    airbnb_cleaned["id"].map(mean_price_per_id)
)

# check number of missing prices per month
missing_by_month =airbnb_cleaned.groupby("month_year")["price"].apply(lambda x: x.isna().mean()*100)
print(missing_by_month)

######### check for outliers ###########

print("\nPrice summary:")
print(airbnb_cleaned["price"].describe())

print("\nPrice quantiles:")
print(
    airbnb_cleaned["price"].quantile(
        [0.50, 0.90, 0.95, 0.99, 0.995, 1.00]
    )
)

pd.set_option("display.max_columns", None)

print("\n20 highest prices:")
print(
    airbnb_cleaned
    .sort_values("price", ascending=False)
    [["id", "month_year", "price",
      "room_type", "neighbourhood",
      "latitude", "longitude"]]
    .head(20)
)

# Count high-price observations
print("\nRows with price above $1000:")
print((airbnb_cleaned["price"] > 1000).sum())

print("\nRows with price above $2000:")
print((airbnb_cleaned["price"] > 2000).sum())

print("\nRows with price above $5000:")
print((airbnb_cleaned["price"] > 5000).sum())

print("\nRows with price above $10000:")
print((airbnb_cleaned["price"] > 10000).sum())


######### sanity checks ###########

print("\nNon-positive prices:")
print((airbnb_cleaned["price"] <= 0).sum())

print("\nMissing latitude/longitude:")
print(
    airbnb_cleaned[
        ["latitude", "longitude"]
    ].isna().sum()
)

print("\nLatitude range:")
print(
    airbnb_cleaned["latitude"].min(),
    airbnb_cleaned["latitude"].max()
)

print("\nLongitude range:")
print(
    airbnb_cleaned["longitude"].min(),
    airbnb_cleaned["longitude"].max()
)


######### visual check ###########

plt.figure(figsize=(10, 6))

plt.boxplot(
    airbnb_cleaned["price"].dropna(),
    orientation="horizontal"
)

plt.xlabel("Price per night (NZD)")
plt.title("Airbnb Price Outlier Check")

plt.tight_layout()
plt.show()





##### save the cleaned data ##########
airbnb_cleaned.to_csv("Data/airbnb_cleaned_oct25_jun26.csv", index=False) # save as a csv file in the Data folder without adding a new index column


##### Clean tenancy bond data ####

#Load the quarterly Tenancy Services dataset.
tenancy_path = Path("Data") / "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
tenancy = pd.read_csv(tenancy_path)

print("\n=============== RAW TENANCY DATA ===============")
print("Shape:", tenancy.shape)
print("\nColumns:")
print(tenancy.columns.tolist())

print("\nMissing values:")
print(tenancy.isna().sum())

#Convert Timeframe to Datetime

print("\nRaw TimeFrame examples:")
print(tenancy["TimeFrame"].head(20))

print("\nUnique TimeFrame examples:")
print(
    tenancy["TimeFrame"]
    .drop_duplicates()
    .head(20)
)

# Convert TimeFrame to datetime
tenancy["TimeFrame"] = pd.to_datetime(
    tenancy["TimeFrame"],
    format="%d/%m/%Y",
    errors="coerce"
)

print("\nAvailable Tenancy timeframes:")
print(
    tenancy["TimeFrame"]
    .drop_duplicates()
    .sort_values()
)

#Filter to airbnb timeframe
######## filter tenancy data to match Airbnb timeframe ########

# Airbnb data covers October 2025 to June 2026
start_date = pd.Timestamp("2025-10-01")
end_date = pd.Timestamp("2026-06-30")

tenancy_filtered = tenancy[
    tenancy["TimeFrame"].between(start_date, end_date)
].copy()

print("\n============= FILTERED TIMEFRAME ==========")

print("Shape after timeframe filtering:")
print(tenancy_filtered.shape)

print("\nTimeframes retained:")
print(
    tenancy_filtered["TimeFrame"]
    .value_counts()
    .sort_index()
)

######## inspect missing values after timeframe filtering ########

print("\n============= MISSING VALUES AFTER FILTERING ==========")

print(
    tenancy_filtered.isna().sum()
)

print("\nPercentage missing:")

print(
    tenancy_filtered.isna().mean() * 100
)

######## inspect rows with missing Location Id ########

missing_location = tenancy_filtered[
    tenancy_filtered["Location Id"].isna()
]

print("\n============= MISSING LOCATION ROWS ==========")

print(
    missing_location[
        [
            "TimeFrame",
            "Location Id",
            "Dwelling Type",
            "Number Of Beds",
            "Total Bonds",
            "Median Rent",
            "Geometric Mean Rent",
            "Upper Quartile Rent",
            "Lower Quartile Rent"
        ]
    ].head(20)
)

print(
    "\nNumber of rows with missing Location Id:",
    len(missing_location)
)

######## remove rows with missing Location Id ########

rows_before_location_clean = len(tenancy_filtered)

tenancy_cleaned = tenancy_filtered[
    tenancy_filtered["Location Id"].notna()
].copy()

rows_after_location_clean = len(tenancy_cleaned)

rows_removed_missing_location = (
    rows_before_location_clean
    - rows_after_location_clean
)

print("\n============= REMOVE MISSING LOCATION ID ==========")

print("Rows before:", rows_before_location_clean)
print("Rows removed:", rows_removed_missing_location)
print("Rows remaining:", rows_after_location_clean)

######## investigate special Location Id values ########

minus99_rows = tenancy_cleaned[
    tenancy_cleaned["Location Id"] == -99
]

print("\n============= LOCATION ID = -99 ==========")

print("Number of rows:", len(minus99_rows))

print(
    minus99_rows[
        [
            "TimeFrame",
            "Location Id",
            "Dwelling Type",
            "Number Of Beds",
            "Total Bonds",
            "Active Bonds",
            "Median Rent"
        ]
    ].head(20)
)

######## Remove Special Location Id = -99 ########

rows_before_aggregate_removal = len(tenancy_cleaned)

tenancy_cleaned = tenancy_cleaned[
    tenancy_cleaned["Location Id"] != -99
].copy()

rows_after_aggregate_removal = len(tenancy_cleaned)

rows_removed_aggregate = (
    rows_before_aggregate_removal
    - rows_after_aggregate_removal
)

print("\n============= REMOVE LOCATION ID = -99 ==========")

print("Rows before:", rows_before_aggregate_removal)
print("Rows removed:", rows_removed_aggregate)
print("Rows remaining:", rows_after_aggregate_removal)

######## correct Location Id datatype ########

tenancy_cleaned["Location Id"] = (
    tenancy_cleaned["Location Id"]
    .astype("int64")
)

print("\nLocation Id datatype:")
print(tenancy_cleaned["Location Id"].dtype)

print("\nExample Location Id values:")
print(
    tenancy_cleaned["Location Id"]
    .head(10)
)

######## investigate Number Of Beds ########

print("\n============= NUMBER OF BEDS ==========")

print("Missing Number Of Beds:")
print(
    tenancy_cleaned["Number Of Beds"]
    .isna()
    .sum()
)

print("\nNumber Of Beds categories:")
print(
    tenancy_cleaned["Number Of Beds"]
    .value_counts(dropna=False)
)
missing_bedrooms = tenancy_cleaned[
    tenancy_cleaned["Number Of Beds"].isna()
]

print("\nExample rows with missing Number Of Beds:")

print(
    missing_bedrooms[
        [
            "TimeFrame",
            "Location Id",
            "Dwelling Type",
            "Number Of Beds",
            "Total Bonds",
            "Active Bonds",
            "Median Rent"
        ]
    ].head(20)
)
print("\nMissing bedrooms by dwelling type:")

print(
    missing_bedrooms["Dwelling Type"]
    .value_counts()
)

######## handle missing Number Of Beds ########

tenancy_cleaned["Number Of Beds"] = (
    tenancy_cleaned["Number Of Beds"]
    .astype("string")
    .fillna("Unknown")
)

print("\n============= NUMBER OF BEDS AFTER CLEANING ==========")

print(
    tenancy_cleaned["Number Of Beds"]
    .value_counts(dropna=False)
)

print(
    "\nMissing Number Of Beds after cleaning:",
    tenancy_cleaned["Number Of Beds"].isna().sum()
)

######## standardise categorical columns ########

tenancy_cleaned["Dwelling Type"] = (
    tenancy_cleaned["Dwelling Type"]
    .astype("string")
    .str.strip()
)

tenancy_cleaned["Number Of Beds"] = (
    tenancy_cleaned["Number Of Beds"]
    .str.strip()
)

print("\nDwelling Type categories:")

print(
    tenancy_cleaned["Dwelling Type"]
    .value_counts()
)

print("\nNumber Of Beds categories:")

print(
    tenancy_cleaned["Number Of Beds"]
    .value_counts()
)

######## check duplicate tenancy records ########

tenancy_key = [
    "TimeFrame",
    "Location Id",
    "Dwelling Type",
    "Number Of Beds"
]

duplicate_tenancy = tenancy_cleaned.duplicated(
    subset=tenancy_key,
    keep=False
)

print("\n============= DUPLICATE CHECK ==========")

print(
    "Number of duplicate key rows:",
    duplicate_tenancy.sum()
)

######## sanity checks for bond counts ########

print("\n============= BOND COUNT SANITY CHECKS ==========")

bond_count_columns = [
    "Total Bonds",
    "Active Bonds",
    "Closed Bonds"
]

for column in bond_count_columns:
    negative_count = (
        tenancy_cleaned[column] < 0
    ).sum()

    print(
        f"{column}: {negative_count} negative values"
    )

######## sanity checks for rent values ########

print("\n============= RENT SANITY CHECKS ==========")

rent_columns = [
    "Median Rent",
    "Geometric Mean Rent",
    "Upper Quartile Rent",
    "Lower Quartile Rent"
]

for column in rent_columns:
    non_positive = (
        tenancy_cleaned[column] <= 0
    ).sum()

    print(
        f"{column}: {non_positive} non-positive values"
    )

lower_above_median = (
    tenancy_cleaned["Lower Quartile Rent"]
    > tenancy_cleaned["Median Rent"]
).sum()

median_above_upper = (
    tenancy_cleaned["Median Rent"]
    > tenancy_cleaned["Upper Quartile Rent"]
).sum()

print(
    "\nRows where Lower Quartile Rent > Median Rent:",
    lower_above_median
)

print(
    "Rows where Median Rent > Upper Quartile Rent:",
    median_above_upper
)

######## investigate possible rent outliers ########

print("\n============= MEDIAN RENT SUMMARY ==========")

print(
    tenancy_cleaned["Median Rent"].describe()
)

print("\nHighest 10 median rents:")

print(
    tenancy_cleaned.nlargest(
        10,
        "Median Rent"
    )[
        [
            "TimeFrame",
            "Location Id",
            "Dwelling Type",
            "Number Of Beds",
            "Total Bonds",
            "Active Bonds",
            "Median Rent"
        ]
    ]
)

print("\nLowest 10 median rents:")

print(
    tenancy_cleaned.nsmallest(
        10,
        "Median Rent"
    )[
        [
            "TimeFrame",
            "Location Id",
            "Dwelling Type",
            "Number Of Beds",
            "Total Bonds",
            "Active Bonds",
            "Median Rent"
        ]
    ]
)

######## check Log Std Dev Weekly Rent ########

print("\n============= LOG STD DEV CHECK ==========")

print(
    "Negative values:",
    (tenancy_cleaned["Log Std Dev Weekly Rent"] < 0).sum()
)

print(
    "Minimum:",
    tenancy_cleaned["Log Std Dev Weekly Rent"].min()
)

print(
    "Maximum:",
    tenancy_cleaned["Log Std Dev Weekly Rent"].max()
)

######## final missing value check ########

print("\n============= FINAL MISSING VALUES ==========")

print(
    tenancy_cleaned.isna().sum()
)

print("\n============= FINAL TENANCY DATA ==========")

print("Final shape:")
print(tenancy_cleaned.shape)

print("\nFinal data types:")
print(tenancy_cleaned.dtypes)

print("\nFirst five rows:")
print(tenancy_cleaned.head())

######## save cleaned tenancy dataset ########

tenancy_cleaned.to_csv(
    "Data/tenancy_cleaned_oct25_jun26.csv",
    index=False
)

print(
    "\nCleaned tenancy dataset saved successfully."
)
