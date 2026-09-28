import requests
import pandas as pd
import os

# ==========================================
# STEP 1: LOAD CLEANED AIRBNB DATA
# ==========================================

airbnb = pd.read_csv("Data/airbnb_cleaned_oct25_jun26.csv")

# Select the first Airbnb listing
row = airbnb.iloc[0]

lat = row["latitude"]
lon = row["longitude"]

print("Testing coordinates:")
print("Latitude:", lat)
print("Longitude:", lon)


# ==========================================
# STEP 2: GET API KEY
# ==========================================

api_key = os.environ.get("KOORDINATES_API_KEY")

if not api_key:
    raise ValueError(
        "API key not found. Set KOORDINATES_API_KEY in PowerShell first."
    )


# ==========================================
# STEP 3: QUERY KOORDINATES API
# ==========================================

url = "https://koordinates.com/services/query/v1/vector.json"

params = {
    "key": api_key,
    "layer": 123515,
    "x": lon,
    "y": lat,
    "max_results": 1,
    "radius": 0,
    "geometry": "false",
    "with_field_names": "true"
}

response = requests.get(url, params=params, timeout=20)

print("\nHTTP status:", response.status_code)

response.raise_for_status()


# ==========================================
# STEP 4: EXTRACT SA2 INFORMATION
# ==========================================

data = response.json()

features = data["vectorQuery"]["layers"]["123515"]["features"]

if len(features) > 0:

    properties = features[0]["properties"]

    sa2_code = properties["SA22026_V1_00"]
    sa2_name = properties["SA22026_V1_00_NAME"]

    print("\n===== SA2 QUERY RESULT =====")
    print("SA2 Code:", sa2_code)
    print("SA2 Name:", sa2_name)

else:
    print("\nNo matching SA2 area found for this coordinate.")


print("\nSingle API query completed.")

