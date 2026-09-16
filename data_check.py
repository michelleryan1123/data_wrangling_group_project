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

# remove the extreme outliers based on price
# Step 1: Identify extreme values
extreme_mask = sa2_airbnb["price"] > 3000

# Step 2: Group by listing ID
grouped = sa2_airbnb.groupby("id")

# Step 3: Build a list of IDs to drop entirely
ids_to_drop = []

# Step 4: Process each listing
for listing_id, group in grouped:
    extreme_prices = group[group["price"] > 3000]
    reasonable_prices = group[group["price"] <= 3000]["price"]

    if len(extreme_prices) > 0:
        if len(reasonable_prices) == 0:
            # No reasonable prices → drop entire listing
            ids_to_drop.append(listing_id)
        else:
            # Replace extreme values with mean of reasonable prices
            mean_price = reasonable_prices.mean()
            sa2_airbnb.loc[(sa2_airbnb["id"] == listing_id) & (sa2_airbnb["price"] > 3000), "price"] = mean_price

# Step 5: Drop listings with no reasonable prices
sa2_airbnb = sa2_airbnb[~sa2_airbnb["id"].isin(ids_to_drop)]
print("sa2_airbnb size after removing extreme outliers", sa2_airbnb.shape[0])

#write the cleaned sa2_airbnb to a new CSV file
sa2_airbnb.to_csv("Data\\airbnb_with_sa2.csv", index=False)