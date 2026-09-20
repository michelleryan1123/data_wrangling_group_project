import geopandas as gpd

# Load SA2-2019 shapefile
sa2 = gpd.read_file(
    "Data/sa2_2019/statistical-area-2-higher-geographies-2019-generalised.shp"
)

print("===== SA2-2019 DATA =====")

print("Total areas:", len(sa2))
print("Coordinate system (CRS):", sa2.crs)

print("\nAll columns:")
print(sa2.columns.tolist())

# Preview columns related to SA2 codes and names
sa2_columns = [
    col for col in sa2.columns
    if "SA2" in col.upper() or "NAME" in col.upper()
]

print("\nSA2-related columns:")
print(sa2[sa2_columns].head())

# ==========================================
# MAP AIRBNB COORDINATES TO SA2-2019
# ==========================================

import pandas as pd

# Load Airbnb data
airbnb = pd.read_csv("Data/airbnb_with_sa2.csv")

# Use unique coordinates to avoid repeated processing
locations = airbnb[
    ["latitude", "longitude"]
].drop_duplicates().copy()

print("\n===== SA2-2019 SPATIAL MAPPING =====")
print("Unique Airbnb coordinates:", len(locations))

# Convert latitude/longitude into geographic points
points = gpd.GeoDataFrame(
    locations,
    geometry=gpd.points_from_xy(
        locations["longitude"],
        locations["latitude"]
    ),
    crs="EPSG:4326"
)

# Convert coordinates to match the shapefile CRS
points = points.to_crs(sa2.crs)

# Find which SA2 polygon contains each coordinate
mapped = gpd.sjoin(
    points,
    sa2[["SA22019_V1", "SA22019__1", "geometry"]],
    how="left",
    predicate="within"
)

# Rename columns
mapped = mapped.rename(columns={
    "SA22019_V1": "sa2_2019_code",
    "SA22019__1": "sa2_2019_name"
})

print("Rows after spatial join:", len(mapped))

print(
    "Duplicate coordinates:",
    mapped.duplicated(
        subset=["latitude", "longitude"]
    ).sum()
)

print(
    "Missing SA2-2019 codes:",
    mapped["sa2_2019_code"].isna().sum()
)

print("\nFirst five mapped records:")
print(
    mapped[
        ["latitude", "longitude",
         "sa2_2019_code", "sa2_2019_name"]
    ].head()
)

# Save mapping only if no duplicate coordinates exist
if mapped.duplicated(
    subset=["latitude", "longitude"]
).any():
    raise ValueError("Duplicate coordinates detected. Check the spatial join.")

mapped[
    ["latitude", "longitude",
     "sa2_2019_code", "sa2_2019_name"]
].to_csv(
    "Data/sa2_2019_mapping.csv",
    index=False
)

print("\nSA2-2019 mapping saved.")