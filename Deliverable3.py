# Deliverable 3

import pandas as pd
pd.set_option('display.max_columns', None)
import glob
#import matplotlib.pyplot as plt

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


df = pd.read_csv("Data\chch_airbnb_oct25_jun26.csv")
print(df.head())

# reproduce the days since last listing histograms - Ammar


# filter out top 10% and calculate # in CHCH - Michelle