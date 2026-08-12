# Deliverable 3

import pandas as pd
pd.set_option('display.max_columns', None)
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")   # to make each figure pop up in a separate window, rather than inline in the notebook

from utils import custom_functions as cf # import the custom functions from the utils folder

# Read through all the *_listings.csv files in the data folder
# Filter out chch listings and add a month_year column
chch_data = [] #create an empty dataframe to store the filtered Christchurch datasets

for file in glob.glob("Data/*_listings.csv"): # run through all the files in the Data folder that end with "_listings.csv"
    chch=cf.load_christchurch(file) # apply the load_christchurch function to filter Chch and add month_year column
    chch_data.append(chch)  #append the filtered dataset to the chch_airbnb list

chch_airbnb = pd.concat(chch_data, ignore_index=True) # concatenate all the filtered Christchurch datasets into one dataframe called combined, and reset the index

# save concatenated data
chch_airbnb.to_csv(
    "Data\chch_airbnb_oct25_jun26.csv",
    index=False
)

###### Summary stats #######

chch_airbnb_summary = cf.summary_stats(chch_airbnb) # calculate summary stats for the total Chch airbnb dataset
print(chch_airbnb_summary) # print the summary stats to the console

######### reproduce the price histograms #########

df = pd.read_csv("Data\chch_airbnb_oct25_jun26.csv")

print(df.head())

# remove missing price values
price = df["price"].dropna()

# # Create histogram of price
# plt.hist(price, bins = 50)

# plt.xlabel("Price per night (NZD)")
# plt.ylabel("Number of listings")
# plt.title("Distribution of Airbnb Prices in Christchurch\nOct 2025 to Jun 2026")
# plt.show()

# # create custom bins for the histogram to better visualize the distribution
# bins = [0,100, 200, 300, 400, 500, 750, 1000, 1250, 1500, 2000, 3000, 4000, 5000]
# # Create histogram of price
# plt.hist(price, bins = bins)
# plt.xlabel("Price per night (NZD)")
# plt.ylabel("Number of listings")
# plt.title("Distribution of Airbnb Prices in Christchurch\nOct 2025 to Jun 2026")
# plt.show()

# # Zoomed histogram (below $1000 per night) to show the majority of listings more clearly
# price_below1000 = price[price <= 1000]
# plt.hist(price_below1000, bins = 50)

# plt.xlabel("Price per night (NZD)")
# plt.ylabel("Number of listings")
# plt.title("Distribution of Airbnb Prices below $1000 per night in Christchurch\nOct 2025 to Jun 2026")

# # set the x-axis limits to zoom in on the majority of listings
# plt.xlim(0, 1000) 
# plt.show()



fig, axes = plt.subplots(3, 1, figsize=(10, 15))  # 3 rows, 1 column

# --- Subplot 1: Default 50-bin histogram ---
axes[0].hist(price, bins=50)
axes[0].set_xlabel("Price per night (NZD)")
axes[0].set_ylabel("Number of listings")
axes[0].set_title("Distribution of Airbnb Prices in Christchurch\nOct 2025 to Jun 2026")

# --- Subplot 2: Custom bins ---
bins = [0,100,200,300,400,500,750,1000,1250,1500,2000,3000,4000,5000]
axes[1].hist(price, bins=bins)
axes[1].set_xlabel("Price per night (NZD)")
axes[1].set_ylabel("Number of listings")
axes[1].set_title("Distribution of Airbnb Prices (Custom Bins)\nOct 2025 to Jun 2026")

# --- Subplot 3: Zoomed histogram below $1000 ---
price_below1000 = price[price <= 1000]
axes[2].hist(price_below1000, bins=50)
axes[2].set_xlabel("Price per night (NZD)")
axes[2].set_ylabel("Number of listings")
axes[2].set_title("Distribution of Airbnb Prices below $1000 per night\nOct 2025 to Jun 2026")
axes[2].set_xlim(0, 1000)

# plt.tight_layout()
plt.subplots_adjust(hspace=0.7)
plt.show()

######### reproduce the days since last review histograms #########

print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.to_list())

print("\nMonth/year groups:")
print(df["month_year"].value_counts())

print("\nLast review examples:")
print(df[["month_year", "last_review"]].head(20))

#convert last_review from text to datetime
df["last_review"] = pd.to_datetime(df["last_review"],
                                #    format="%Y/%m/%d",
                                   errors="coerce")

print(df[["month_year", "last_review"]].head(20))
print("\nMissing last_review values:", df["last_review"].isna().sum())

#Calculate days since last review
reference_date = pd.Timestamp("2026-06-22")

df["days_since_last_review"] = (
    reference_date - df["last_review"]
).dt.days

#check the calculation
print("\nDays since last review examples:")

print(
    df[
        [
            "last_review",
            "days_since_last_review"
        ]
        ].head(20)
)

#remove listings with no last review
review_data = df.dropna(
    subset=["days_since_last_review"]
).copy()

print(
    "\nListings with a valid last review:",
    len(review_data)
)

#Histogram 1
#Distribution up to 5000 days

review_5000 = review_data[
    review_data["days_since_last_review"] <= 5000
]

# plt.figure(figsize=(10, 6))

# plt.hist(
#     review_5000["days_since_last_review"],
#     bins=100
# )

# plt.xlabel("Days since last review")
# plt.ylabel("Number of listings")
# plt.title(
#     "Distribution of Days Since Last Review"
# )

# plt.tight_layout()
# plt.show()

# # create custom bins for the histogram to better visualize the distribution
# bins2=[0,10,20,30,40, 50, 75, 100, 125, 150, 175, 200, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000]
# plt.hist(
#     review_5000["days_since_last_review"],
#     bins=bins2
# )

# plt.xlabel("Days since last review")
# plt.ylabel("Number of listings")
# plt.title(
#     "Distribution of Days Since Last Review"
# )

# plt.tight_layout()
# plt.show()

# #Histogram 2

# #Distribution for the past 750 days
# review_750 = review_data[
#     review_data["days_since_last_review"] <= 750
# ]

# plt.figure(figsize=(10, 6))

# plt.hist(
#     review_750["days_since_last_review"],
#     bins=50
# )

# plt.xlabel("Days since last review")
# plt.ylabel("Number of listings")
# plt.title(
#     "Distribution of Days Since Last Review - Past 750 Days"
# )

# plt.tight_layout()
# plt.show()

fig, axes = plt.subplots(3, 1, figsize=(10, 18))

# --- Subplot 1: 100-bin histogram ---
axes[0].hist(
    review_5000["days_since_last_review"],
    bins=100
)
axes[0].set_xlabel("Days since last review")
axes[0].set_ylabel("Number of listings")
axes[0].set_title("Distribution of Days Since Last Review")

# --- Subplot 2: Custom bins ---
bins2 = [0,10,20,30,40,50,75,100,125,150,175,200,250,500,750,1000,
         1500,2000,3000,4000,5000]

axes[1].hist(
    review_5000["days_since_last_review"],
    bins=bins2
)
axes[1].set_xlabel("Days since last review")
axes[1].set_ylabel("Number of listings")
axes[1].set_title("Distribution of Days Since Last Review (Custom Bins)")

# --- Subplot 3: Past 750 days ---
review_750 = review_data[
    review_data["days_since_last_review"] <= 750
]

axes[2].hist(
    review_750["days_since_last_review"],
    bins=50
)
axes[2].set_xlabel("Days since last review")
axes[2].set_ylabel("Number of listings")
axes[2].set_title("Distribution of Days Since Last Review - Past 750 Days")

# spacing fix
plt.subplots_adjust(hspace=0.5)

plt.show()

######### summary stats for the top 10% of listings (based on number reviews) #########
top10per, top10_summary = cf.highest_reviews(chch_airbnb) # calculate summary stats for the top 10% of listings based on number_of_reviews
print(top10_summary) # print the summary stats to the console
print(top10per.head()) # print the first 5 rows of the top 10% of listings to the console
