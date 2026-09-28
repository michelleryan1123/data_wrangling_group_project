import pandas as pd

# Load the saved API mapping
mapping = pd.read_csv(
    "Data/sa2_mapping_iky_progress.csv",
    dtype={"sa2_code": "string"}
)

print("===== SA2 MAPPING VALIDATION =====")

# 1. Check total rows
print("Total mapping rows:", len(mapping))

# 2. Check duplicate coordinates
duplicates = mapping.duplicated(
    subset=["latitude", "longitude"]
).sum()

print("Duplicate coordinates:", duplicates)

# 3. Check missing area codes
print("Missing SA2 codes:", mapping["sa2_code"].isna().sum())

# 4. Check Christchurch Central
central = mapping[
    mapping["sa2_code"] == "326600"
]

print("Christchurch Central coordinates:", len(central))

# 5. Display sample
print("\nFirst five mapping records:")
print(mapping.head())