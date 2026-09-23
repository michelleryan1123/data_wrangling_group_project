import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD THE ALREADY-JOINED DATASET
# ============================================================

df = pd.read_csv("airbnb_tenancy_joined.csv")


# ============================================================
# 2. COUNT UNIQUE AIRBNB LISTINGS BY SA2 LOCATION
# ============================================================

airbnb_counts = (
    df.groupby(
        ["sa2_2019_code", "sa2_2019_name"]
    )["id"]
    .nunique()
    .reset_index(name="Airbnb Listings")
)


# ============================================================
# 3. GET ACTIVE RENTAL BONDS BY SA2 LOCATION
# ============================================================

# Rental information is repeated across Airbnb rows
# because the datasets have already been joined.
#
# Keep one record for each location and quarter.

rental_data = (
    df[
        [
            "sa2_2019_code",
            "sa2_2019_name",
            "quarter",
            "Active Bonds"
        ]
    ]
    .dropna(subset=["Active Bonds"])
    .drop_duplicates()
)


# Get the rental measure for each location.
# Use the maximum value across quarters to avoid
# adding repeated rental data together.

rental_counts = (
    rental_data
    .groupby(
        ["sa2_2019_code", "sa2_2019_name"]
    )["Active Bonds"]
    .max()
    .reset_index(name="Active Rental Bonds")
)


# ============================================================
# 4. MERGE THE TWO COUNTS INTO ONE COMPARISON TABLE
# ============================================================

comparison = airbnb_counts.merge(
    rental_counts,
    on=["sa2_2019_code", "sa2_2019_name"],
    how="left"
)


# ============================================================
# 5. CALCULATE THE DIFFERENCE
# ============================================================

comparison["Difference"] = (
    comparison["Airbnb Listings"]
    - comparison["Active Rental Bonds"]
)


# ============================================================
# 6. SORT BY LOCATION
# ============================================================

comparison = comparison.sort_values(
    "sa2_2019_name"
)


# ============================================================
# 7. DISPLAY THE RESULTS
# ============================================================

print("\nAirbnb Listings vs Active Rental Bonds by Location:\n")

print(
    comparison[
        [
            "sa2_2019_code",
            "sa2_2019_name",
            "Airbnb Listings",
            "Active Rental Bonds",
            "Difference"
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. SAVE THE COMPARISON TABLE
# ============================================================

comparison.to_csv(
    "airbnb_vs_rental_comparison_final.csv",
    index=False
)

print("\nResults saved to airbnb_vs_rental_comparison.csv")


# ============================================================
# 9. CREATE A BAR CHART
# ============================================================

chart_data = comparison.sort_values(
    "Airbnb Listings",
    ascending=False
).head(15)

chart_data = chart_data.sort_values(
    "Airbnb Listings"
)

chart_data.set_index("sa2_2019_name")[
    ["Airbnb Listings", "Active Rental Bonds"]
].plot(
    kind="barh",
    figsize=(12, 8)
)

plt.xlabel("Number")
plt.ylabel("SA2 Location")

plt.title(
    "Airbnb Listings vs Active Rental Bonds by SA2 Location"
)

plt.legend()

plt.tight_layout()

plt.show()