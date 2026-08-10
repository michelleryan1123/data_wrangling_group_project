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

