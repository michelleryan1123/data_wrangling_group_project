## Deliverable 4: cleaning the datasets

#import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import custom_functions as cf # import the custom functions from the utils folder

# import the airbnb dataset
airbnb_chch = pd.read_csv("Data\airbnb_oct25_jun26.csv")

pre_clean_size = airbnb_chch.shape
print(pre_clean_size)