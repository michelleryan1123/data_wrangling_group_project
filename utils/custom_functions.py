# Store custom functions to be used in the main notebook here.
import pandas as pd
import os
import glob

# load the csv datasets, filter to only include Christchurch listings, and add a month_year column
def load_christchurch(file_name):
    # Defines a function that loads and prepares one CSV dataset.
    # file_name is the name of the CSV file being processed.

    df = pd.read_csv(file_name)
    # Reads the CSV file into a pandas DataFrame called df.

    df = df[df["neighbourhood_group"] == "Christchurch City"].copy()
    # Filters the dataset to keep only listings from Christchurch City.
    # .copy() creates an independent copy of the filtered data.

    month_year = os.path.basename(file_name).replace("_listings.csv", "").upper()
    # Gets the filename without the folder path.
    # Removes "_listings.csv" from the filename.
    # Converts the remaining month/year text to uppercase.
    # For example, "Oct26_listings.csv" becomes "OCT26".

    df["month_year"] = month_year
    # Creates a new column called month_year.
    # Every row from this dataset receives its corresponding month/year.

    return df
    # Returns the processed Christchurch dataset.

# Calculate summary statistics for a dataframe
def summary_stats(df):

    summary={
        "total-count": len(df), #the total number of listings
        "data_type": df.dtypes, # data type of each column
        "count_na": df.isna().sum(), # the number of missing values for each column
        "count_unique": df.nunique(), # the number of unique values for each column
        "mean": df.mean(numeric_only=True), # the mean for each numeric column
        "min": df.min(numeric_only=True), # the minimum for each numeric column
        "max": df.max(numeric_only=True), # the maximum for each numeric column
        "std_dev": df.std(numeric_only=True), # the standard deviation for each numeric column
        
    }

    # convert the dictionary to a dataframe
    summary = pd.DataFrame(summary)

    return summary

# filter out the top 10% of listings based on number_of_reviews and calculate some summary statistics
def highest_reviews(df):
    # calculate the 90th percentile of number_of_reviews
    threshold = df["number_of_reviews"].quantile(0.9)

    # filter out the top 10% of listings based on number_of_reviews
    top10per = df[df["number_of_reviews"] <= threshold]

    # calculate summary statistics for the filtered dataframe
    summary = summary_stats(top10per)

    return summary, top10per