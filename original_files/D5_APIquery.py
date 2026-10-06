# Query the API for location data and enter into the AirBnB dataset

import requests
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def query_sa2(row):
    lat = row["latitude"]
    lon = row["longitude"]

    # the URL for the API query, including the API key and parameters for the specific layer and coordinates
    url = (
        "https://koordinates.com/services/query/v1/vector.json"
        f"?key=REDACTED"
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

        # SAFE JSON extraction
        vector = data.get("vectorQuery", {})
        layers = vector.get("layers", {})
        layer = layers.get("123515", {})
        features = layer.get("features", [])

        if len(features) > 0:
            props = features[0]["properties"]
            return {
                "id": row["id"],
                "sa2_name": props.get("SA22026_V1_00_NAME"),
                "sa2_code": props.get("SA22026_V1_00")
            }

        # if "features" in data and len(data["features"]) > 0:
        #     props = data["features"][0]["properties"]
        #     return {
        #         "id": row["id"],
        #         "sa2_name": props.get("SA22026_V1_00_NAME"),
        #         "sa2_code": props.get("SA22026_V1_00")
        #     }
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
        results = list(
            tqdm(
                pool.imap(query_sa2, rows),
                total=len(rows),
                desc="Querying SA2 API"
            )
        )

    return pd.DataFrame(results)

# -----------------------------
# MAIN EXECUTION BLOCK (required on Windows)
# -----------------------------
if __name__ == "__main__":
    clean_airbnb = pd.read_csv("Data\\airbnb_cleaned_oct25_jun26.csv")

    clean_airbnb["sa2_name"] = None
    clean_airbnb["sa2_code"] = None

    results = run_parallel(clean_airbnb, workers=5)

    clean_airbnb = clean_airbnb.merge(results, on="id", how="left")

    clean_airbnb.to_csv("Data\\airbnb_with_sa2.csv", index=False)

    print("SA2 lookup complete.")
