# Query the API for location data and enter into the AirBnB dataset

import requests
import pandas as pd
from multiprocessing import Pool, cpu_count

# Load the cleaned AirBnB dataset with lat/lon columns
clean_airbnb = pd.read_csv("Data\\airbnb_cleaned_oct25_jun26.csv") 
print(clean_airbnb.columns) 

# Add a new column for SA2 name and code
clean_airbnb["sa2_name"] = None
clean_airbnb["sa2_code"] = None


def query_sa2(row):
    lat = row["latitude"]
    lon = row["longitude"]

    # the URL for the API query, including the API key and parameters for the specific layer and coordinates
    url = (
        "https://datafinder.stats.govt.nz/services/query/v1/vector.json"
        f"?key=246ea4e450254b1195d146fa1708d286"
        f"&layer=123515"
        f"&x={lon}"
        f"&y={lat}"
        "&max_results=1"
        "&radius=0"
        "&geometry=false"
        "&with_field_names=true"
    )

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "features" in data and len(data["features"]) > 0:
            props = data["features"][0]["properties"]
            return {
                "id": row["id"],
                "sa2_name": props.get("SA22026_V1_00_NAME"),
                "sa2_code": props.get("SA22026_V1_00")
            }
        else:
            return {
                "id": row["id"],
                "sa2_name": None,
                "sa2_code": None
            }

    except Exception as e:
        return {
            "id": row["id"],
            "sa2_name": None,
            "sa2_code": None
        }

def run_parallel(df, workers=None):
    workers = workers or cpu_count()
    rows = df.to_dict("records")

    with Pool(workers) as pool:
        results = pool.map(query_sa2, rows)

    return pd.DataFrame(results)

# -----------------------------
# MAIN EXECUTION BLOCK (required on Windows)
# -----------------------------
if __name__ == "__main__":
    clean_airbnb = pd.read_csv("Data\\airbnb_cleaned_oct25_jun26.csv")

    clean_airbnb["sa2_name"] = None
    clean_airbnb["sa2_code"] = None

    results = run_parallel(clean_airbnb, workers=8)

    clean_airbnb = clean_airbnb.merge(results, on="id", how="left")

    clean_airbnb.to_csv("Data\\airbnb_with_sa2.csv", index=False)

    print("SA2 lookup complete.")