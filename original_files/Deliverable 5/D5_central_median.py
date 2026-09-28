import pandas as pd

# Load Airbnb dataset with SA2 codes
airbnb = pd.read_csv(
    "Data/airbnb_with_sa2.csv",
    dtype={"sa2_code": "string"}
)

# Filter Christchurch Central
central = airbnb[
    airbnb["sa2_code"] == "326600"
].copy()

print("===== CHRISTCHURCH CENTRAL =====")

print("Listing-month observations:", len(central))

print("Unique Airbnb listings:", central["id"].nunique())

# Calculate median nightly price
median_price = central["price"].median()

print(f"Median Airbnb nightly price: NZ${median_price:.2f}")

# Check individual months
print("\nMedian Airbnb price by month:")

print(
    central.groupby("month_year")["price"].median()
)
