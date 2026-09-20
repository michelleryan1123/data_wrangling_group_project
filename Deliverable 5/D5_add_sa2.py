import pandas as pd

# 1. Load the cleaned Airbnb dataset
airbnb = pd.read_csv(
    "Data/airbnb_cleaned_oct25_jun26.csv"
)

# 2. Load the completed SA2 mapping
mapping = pd.read_csv(
    "Data/sa2_mapping_iky_progress.csv",
    dtype={"sa2_code": "string"}
)

# 3. Check for duplicate coordinate mappings
assert not mapping.duplicated(
    subset=["latitude", "longitude"]
).any()

# 4. Add SA2 codes to Airbnb
airbnb_with_sa2 = airbnb.merge(
    mapping,
    on=["latitude", "longitude"],
    how="left",
    validate="many_to_one"
)

# 5. Validate the result
print("===== AIRBNB SA2 VALIDATION =====")

print("Original Airbnb rows:", len(airbnb))
print("Rows after merge:", len(airbnb_with_sa2))

print(
    "Missing SA2 codes:",
    airbnb_with_sa2["sa2_code"].isna().sum()
)

assert len(airbnb_with_sa2) == len(airbnb)

assert airbnb_with_sa2["sa2_code"].notna().all()

# 6. Check Christchurch Central
central = airbnb_with_sa2[
    airbnb_with_sa2["sa2_code"] == "326600"
]

print(
    "Christchurch Central listing-month rows:",
    len(central)
)

print(
    "Christchurch Central unique listings:",
    central["id"].nunique()
)

# 7. Save the updated Airbnb dataset
airbnb_with_sa2.to_csv(
    "Data/airbnb_with_sa2.csv",
    index=False
)

print("\nAirbnb with SA2 saved successfully.")