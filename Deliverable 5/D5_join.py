import pandas as pd

# Load Airbnb dataset with SA2 codes
airbnb = pd.read_csv(
    "Data/airbnb_with_sa2.csv",
    dtype={"sa2_code": "string"}
)

# Standardise month labels
month = airbnb["month_year"].str.upper()

month = month.str.replace("APRIL", "APR", regex=False)
month = month.str.replace("JUNE", "JUN", regex=False)

# Convert month-year into a date
airbnb["date"] = pd.to_datetime(
    month,
    format="%b%y"
)

# Convert each month into its quarter start
airbnb["quarter"] = (
    airbnb["date"]
    .dt.to_period("Q")
    .dt.start_time
)

# Check the result
print("===== AIRBNB TIME CONVERSION =====")

print(
    airbnb[["month_year", "quarter"]]
    .drop_duplicates()
    .sort_values("quarter")
)

# ==========================================
# 2. PREPARE TENANCY DATA
# ==========================================

tenancy = pd.read_csv(
    "Data/tenancy_cleaned_oct25_jun26.csv"
)

print("\n===== TENANCY DATA =====")

print("Original Tenancy rows:", len(tenancy))

# Convert TimeFrame into datetime
tenancy["TimeFrame"] = pd.to_datetime(
    tenancy["TimeFrame"]
)

# Select overall rental statistics
tenancy_summary = tenancy[
    (tenancy["Dwelling Type"] == "ALL") &
    (tenancy["Number Of Beds"] == "ALL")
].copy()

print("Rows after selecting ALL categories:", len(tenancy_summary))

# Check whether area + quarter uniquely identifies each row
duplicates = tenancy_summary.duplicated(
    subset=["Location Id", "TimeFrame"]
).sum()

print("Duplicate area-quarter combinations:", duplicates)

# Check whether Christchurch Central exists
central = tenancy_summary[
    tenancy_summary["Location Id"] == 326600
]

print("\nChristchurch Central Tenancy records:")
print(
    central[["TimeFrame", "Location Id", "Median Rent"]]
)

print("\nTenancy timeframes:")
print(tenancy_summary["TimeFrame"].value_counts().sort_index())

# ==========================================
# 3. CHECK SA2 CODE COVERAGE
# ==========================================

tenancy_codes = set(
    tenancy_summary["Location Id"]
    .dropna()
    .astype(int)
    .astype(str)
)

matched = airbnb["sa2_code"].isin(tenancy_codes)

print("\n===== SA2 CODE COVERAGE =====")
print("Airbnb rows:", len(airbnb))
print("Rows with a code found in Tenancy:", matched.sum())
print("Rows without a matching code:", (~matched).sum())

missing_codes = set(airbnb["sa2_code"].dropna()) - tenancy_codes

print("Number of SA2 codes absent from Tenancy:", len(missing_codes))
print("Absent codes:", sorted(missing_codes))