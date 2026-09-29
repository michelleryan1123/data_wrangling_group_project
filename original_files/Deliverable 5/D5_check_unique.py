import pandas as pd
import requests
import os

# ==========================================
# 1. LOAD CLEANED AIRBNB DATASET
# ==========================================

airbnb = pd.read_csv("Data/airbnb_cleaned_oct25_jun26.csv")

# Get unique coordinates
unique_locations = airbnb[
    ["latitude", "longitude"]
].drop_duplicates()

print("Total Airbnb rows:", len(airbnb))
print("Unique coordinates:", len(unique_locations))
print("Unique listing IDs:", airbnb["id"].nunique())


# ==========================================
# 2. GET API KEY
# ==========================================

api_key = os.environ["KOORDINATES_API_KEY"]

url = "https://koordinates.com/services/query/v1/vector.json"


# ==========================================
# 3. TEST ONLY 3 UNIQUE COORDINATES
# ==========================================

test_locations = unique_locations.head(3)

for _, row in test_locations.iterrows():

    params = {
        "key": api_key,
        "layer": 123515,
        "x": row["longitude"],
        "y": row["latitude"],
        "max_results": 1,
        "radius": 0,
        "geometry": "false",
        "with_field_names": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    features = data["vectorQuery"]["layers"]["123515"]["features"]

    if features:
        properties = features[0]["properties"]

        print("SA2 Code:", properties["SA22026_V1_00"])
        print("SA2 Name:", properties["SA22026_V1_00_NAME"])

    else:
        print("No matching SA2 found.")

    print("---------------------")