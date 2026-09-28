import pandas as pd

# Load the cleaned Airbnb dataset
airbnb = pd.read_csv(
    "Data/airbnb_cleaned_oct25_jun26.csv"
)

# Select unique latitude/longitude pairs
unique_locations = airbnb[
    ["latitude", "longitude"]
].drop_duplicates().copy()

# Display dataset information
print("Total Airbnb rows:", len(airbnb))
print("Unique coordinates:", len(unique_locations))

print("\nFirst five unique coordinates:")
print(unique_locations.head())

# ==========================================
# TEST 10 UNIQUE COORDINATES
# ==========================================

import requests
import os
from pathlib import Path

api_key = os.environ.get("KOORDINATES_API_KEY")

if not api_key:
    raise SystemExit("API key missing. Set it in PowerShell first.")

url = "https://koordinates.com/services/query/v1/vector.json"

checkpoint = Path("Data/sa2_mapping_iky_progress.csv")

# Load previous results, if available
if checkpoint.exists():
    results = pd.read_csv(checkpoint).to_dict("records")
else:
    results = []

completed = {
    (row["latitude"], row["longitude"])
    for row in results
}

# Test only 10 unique coordinates
test_locations = unique_locations

for _, row in test_locations.iterrows():

    lat = row["latitude"]
    lon = row["longitude"]

    # Skip coordinates already saved
    if (lat, lon) in completed:
        continue

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

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        features = data["vectorQuery"]["layers"]["123515"]["features"]

    except (requests.RequestException, ValueError, KeyError) as error:
        print("Query failed:", type(error).__name__)
        print("Stopping. Previous results remain saved.")
        break

    if features:
        properties = features[0]["properties"]

        sa2_code = properties["SA22026_V1_00"]
        sa2_name = properties["SA22026_V1_00_NAME"]

    else:
        sa2_code = None
        sa2_name = None

    results.append({
        "latitude": lat,
        "longitude": lon,
        "sa2_code": sa2_code,
        "sa2_name": sa2_name
    })

    # Save after every successful request
    pd.DataFrame(results).to_csv(
        checkpoint,
        index=False
    )

    completed.add((lat, lon))

    print("SA2 Code:", sa2_code)
    print("SA2 Name:", sa2_name)
    print("---------------------")

print("\n===== TEST COMPLETE =====")
print("Saved coordinates:", len(results))
print("Checkpoint:", checkpoint)