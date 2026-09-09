## Deliverable 4: cleaning the datasets

#import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import custom_functions as cf # import the custom functions from the utils folder

# import the airbnb dataset
airbnb_chch = pd.read_csv("Data\\airbnb_oct25_jun26.csv")
print(airbnb_chch.head()) # print the first 5 rows of the dataset to the console

pre_clean_size = airbnb_chch.shape # number of rows, cols before cleaning
print(pre_clean_size)

col_names = airbnb_chch.columns # get the column names
print(col_names)

#summary statistics for the dataset before cleaning
summary_all = cf.summary_stats(airbnb_chch) # calculate summary stats for the filtered
print(summary_all)

# define the columns to keep for the cleaned dataset
col_to_keep = ['id', 'neighbourhood', 'latitude', 'longitude', 'price', 'minimum_nights']

airbnb_cleaned = airbnb_chch[col_to_keep].copy() # create a new dataframe with only the columns to keep
airbnb_filtered = airbnb_cleaned.shape # number of rows, cols after filtering to keep only the columns we want
print(airbnb_filtered)

# look at the strucutre of the filtered dataset
print(airbnb_cleaned.info()) # print the structure of the filtered dataset

#get some summary statistics for the filtered dataset
summary_stats = cf.summary_stats(airbnb_cleaned) # calculate summary stats for the filtered
print(summary_stats)
