import pandas as pd

# Load Airbnb with SA2-2019 codes
airbnb = pd.read_csv(
    "Data/airbnb_with_sa2_2019.csv",
    dtype={"sa2_2019_code": "string"}
)

# Load Tenancy
tenancy = pd.read_csv(
    "Data/tenancy_cleaned_oct25_jun26.csv",
    dtype={"Location Id": "string"}
)

# Select overall rental records
tenancy = tenancy[
    (tenancy["Dwelling Type"] == "ALL") &
    (tenancy["Number Of Beds"] == "ALL")
].copy()

# Compare area codes
tenancy_codes = set(tenancy["Location Id"].dropna())

matched = airbnb["sa2_2019_code"].isin(tenancy_codes)

print("===== SA2-2019 COVERAGE =====")
print("Total Airbnb rows:", len(airbnb))
print("Rows with matching Tenancy area code:", matched.sum())
print("Rows without matching Tenancy area code:", (~matched).sum())

missing_codes = (
    set(airbnb["sa2_2019_code"].dropna())
    - tenancy_codes
)

print("Number of unmatched SA2 codes:", len(missing_codes))
print("Unmatched codes:", sorted(missing_codes))

# Recheck Christchurch Central using SA2-2019
central = airbnb[
    airbnb["sa2_2019_code"] == "326600"
]

print("\n===== CHRISTCHURCH CENTRAL (SA2-2019) =====")
print("Area names:", central["sa2_2019_name"].unique())
print("Listing-month rows:", len(central))
print("Unique listings:", central["id"].nunique())
print("Median nightly price:", central["price"].median())