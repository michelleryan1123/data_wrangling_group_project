# Deliverable 3

import pandas as pd
pd.set_option('display.max_columns', None)
import glob
import matplotlib.pyplot as plt

from utils import custom_functions as cf # import the custom functions from the utils folder

# Read through all the *_listings.csv files in the data folder
# Filter out chch listings and add a month_year column
chch_data = [] #create an empty dataframe to store the filtered Christchurch datasets

for file in glob.glob("Data/*_listings.csv"): # run through all the files in the Data folder that end with "_listings.csv"
    chch=cf.load_christchurch(file) # apply the load_christchurch function to filter Chch and add month_year column
    chch_data.append(chch)  #append the filtered dataset to the chch_airbnb list

chch_airbnb = pd.concat(chch_data, ignore_index=True) # concatenate all the filtered Christchurch datasets into one dataframe called combined, and reset the index


# change the format of any columns that need to be changed

# # save concatenated data
# chch_airbnb.to_csv(
#     "Data\chch_airbnb_oct25_jun26.csv",
#     index=False
# )


# Summary stats

chch_airbnb_summary = cf.summary_stats(chch_airbnb) # calculate summary stats for the total Chch airbnb dataset
print(chch_airbnb_summary) # print the summary stats to the console

# reproduce the price histograms - Iky

df = pd.read_csv("christchurch_listings.csv")
print(df.head())

# remove missing price value - Iky
price = df["price"].dropna()

# Create histogram of price - Iky
plt.hist(price, bins = 50)

plt.xlabel("Price (NZD)")
plt.ylabel("Number of listings")
plt.title("Distribution of Airbnb Prices in Christchurch - Oct 2025 to Jun 2026")
plt.show()

# Zoomed histogram to show the majority of listings more clearly - Iky

plt.hist(price, bins = 50)

plt.xlabel("Price (NZD)")
plt.ylabel("Number of listings")
plt.title("Distribution of Airbnb Prices in Christchurch - Oct 2025 to Jun 2026")

# set the x-axis limits to zoom in on the majority of listings
plt.xlim(0, 1000) 
plt.show()

# reproduce the days since last listing histograms - Ammar


# summary stats for the top 10% of listings (based on number reviews)
top10per, top10_summary = cf.highest_reviews(chch_airbnb) # calculate summary stats for the top 10% of listings based on number_of_reviews
print(top10_summary) # print the summary stats to the console
print(top10per.head()) # print the first 5 rows of the top 10% of listings to the console