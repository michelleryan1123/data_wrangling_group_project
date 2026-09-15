## Deliverable 4: cleaning the datasets

#import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import custom_functions as cf # import the custom functions from the utils folder

# import the airbnb dataset
airbnb_chch = pd.read_csv("Data\\chch_airbnb_oct25_jun26.csv")

pre_clean_size = airbnb_chch.shape # number of rows, cols before cleaning
print(pre_clean_size)

col_names = airbnb_chch.columns # get the column names
print(col_names)

#summary statistics for the dataset before cleaning
summary_all = cf.summary_stats(airbnb_chch) # calculate summary stats for the filtered
print(summary_all)

# define the columns to keep for the cleaned dataset
col_to_keep = ['id', 'neighbourhood', 'latitude', 'longitude', 'price', 'month_year', 'room_type']

airbnb_cleaned = airbnb_chch[col_to_keep].copy() # create a new dataframe with only the columns to keep
airbnb_filtered = airbnb_cleaned.shape # number of rows, cols after filtering to keep only the columns we want
print(airbnb_filtered)

# look at the strucutre of the filtered dataset
print(airbnb_cleaned.info()) # print the structure of the filtered dataset

#get some summary statistics for the filtered dataset
summary_stats = cf.summary_stats(airbnb_cleaned) # calculate summary stats for the filtered
print(summary_stats)

######## check for duplicates in the dataset ##############
# as dataset spans multiple months we can't just use property id to check for duplicates, we need to use a combination of property id and month_year
duplicates = airbnb_cleaned.duplicated(subset=['id', 'month_year'], keep= False) # check for duplicate rows based on property id and month_year
print(f"Number of duplicates found: {duplicates.sum()}")

# no duplicates found

####### missing values ##########
# there are 10667 missing values in the 'price' column

# check for properties that have no price at all
missing_by_id = (airbnb_cleaned
    .groupby("id")["price"] # group by property id and get the price column
    .apply(lambda x: x.isna().all()) # check if all the prices for that property id are missing - returns true if all prices are missing, false otherwise
)

missing_by_id = missing_by_id[missing_by_id] # filter to only 'True' values (all missing prices)
print("sum of properties with all missing prices: ", missing_by_id.sum())

# drop the properties that have no prices for all months
airbnb_cleaned = airbnb_cleaned[~airbnb_cleaned["id"].isin(missing_by_id.index)]

# check number of missing prices per month
missing_by_month =airbnb_cleaned.groupby("month_year")["price"].apply(lambda x: x.isna().mean()*100)
print(missing_by_month)

# replace the empty months with the mean price of the other months for that propery
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