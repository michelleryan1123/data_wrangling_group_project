#check the airbnb data
import pandas as pd

original_airbnb = pd.read_csv("Data\\chch_airbnb_oct25_jun26.csv")
print("original_airbnb size", original_airbnb.shape[0])

clean_airbnb = pd.read_csv("Data\\airbnb_cleaned_oct25_jun26.csv")
print("clean_airbnb size", clean_airbnb.shape[0])

sa2_airbnb = pd.read_csv("Data\\airbnb_with_sa2.csv")
print("sa2_airbnb size", sa2_airbnb.shape[0])
print(sa2_airbnb.head(20))

# check for duplicates in the sa2 file
duplicates = sa2_airbnb.duplicated(subset=['id', 'month_year'], keep= False) # Check for duplicate rows based on property id and month_year
# print(f"Number of duplicates found: {duplicates.sum()}")
# print(sa2_airbnb[duplicates])
# print(duplicates)

#remove duplicates from sa2_airbnb
sa2_airbnb = sa2_airbnb.drop_duplicates(subset=['id', 'month_year'], keep='first') # Keep the first occurrence of each duplicate row

print("sa2_airbnb size after removing duplicates", sa2_airbnb.shape[0])

#write the cleaned sa2_airbnb to a new CSV file
sa2_airbnb.to_csv("Data\\airbnb_with_sa2.csv", index=False)