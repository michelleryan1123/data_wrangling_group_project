import pandas as pd

# Load Airbnb with existing SA2-2026 codes
airbnb = pd.read_csv(
    "Data/airbnb_with_sa2.csv",
    dtype={"sa2_code": "string"}
)

# Load the new SA2-2019 mapping
mapping = pd.read_csv(
    "Data/sa2_2019_mapping_iky.csv",
    dtype={"sa2_2019_code": "string"}
)

# Ensure one mapping per coordinate
assert not mapping.duplicated(
    ["latitude", "longitude"]
).any()

# Attach SA2-2019 codes
airbnb = airbnb.merge(
    mapping,
    on=["latitude", "longitude"],
    how="left",
    validate="many_to_one"
)

print("===== SA2-2019 AIRBNB VALIDATION =====")
print("Rows after merge:", len(airbnb))
print("Missing SA2-2019 codes:", airbnb["sa2_2019_code"].isna().sum())

# Validate
assert len(airbnb) == 28298
assert airbnb["sa2_2019_code"].notna().all()

# Compare the two versions
print(
    "Rows with different SA2 codes:",
    (airbnb["sa2_code"] != airbnb["sa2_2019_code"]).sum()
)

# Save updated dataset
airbnb.to_csv(
    "Data/airbnb_with_sa2_2019.csv",
    index=False
)

print("Updated Airbnb dataset saved successfully.")
