# ============================================================
# Query SA2 (Statistical Area 2) from Koordinates for each Airbnb listing
# ============================================================

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import requests
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from paths import data_path


# ------------------------------------------------------------
# 1. Query Koordinates API for SA2
# ------------------------------------------------------------

def query_sa2(row):
    lat = row["latitude"]
    lon = row["longitude"]

    url = (
        "https://koordinates.com/services/query/v1/vector.json"
        f"?key=ab6b9d0f62314f00840b4637d351ce5a"
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
        else:
            return {"id": row["id"], "sa2_name": None, "sa2_code": None}

    except Exception:
        return {"id": row["id"], "sa2_name": None, "sa2_code": None}


# ------------------------------------------------------------
# 2. Parallel processing wrapper
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 3. MAIN FUNCTION (pipeline‑safe)
# ------------------------------------------------------------

def main():

    print("\n=== STEP 5: SA2 LOOKUP ===")

    sa2_file = data_path("processed", "airbnb_with_sa2.csv")
    run_query = True

    # Check if SA2 file already exists
    if sa2_file.exists():
        df_existing = pd.read_csv(sa2_file)

        if df_existing["sa2_name"].notna().all() and df_existing["sa2_code"].notna().all():
            print("SA2 query already completed. No action taken.")
            run_query = False
        else:
            print("Existing SA2 file incomplete. Running SA2 query again...")
    else:
        print("No existing SA2 file found. Running SA2 query...")

    # Run query if needed
    if run_query:
        clean_airbnb = pd.read_csv(data_path("processed", "airbnb_cleaned_oct25_jun26.csv"))

        unique_rows = clean_airbnb.drop_duplicates(subset=["id"])[["id", "latitude", "longitude"]]

        results = run_parallel(unique_rows, workers=5)

        clean_airbnb = clean_airbnb.merge(results, on="id", how="left")

        output_file = data_path("processed", "airbnb_with_sa2.csv")
        clean_airbnb.to_csv(output_file, index=False)
        print("Saved SA2 Airbnb dataset:", output_file)
    else:
        print("Skipping SA2 query")

    print("SA2 lookup complete.")

    # ---------------------------------------------------------
    # SANITY CHECKS
    # ---------------------------------------------------------

    print("\n=== SANITY CHECKS ON FINAL SA2 FILE ===")

    pre_API = pd.read_csv(data_path("processed", "airbnb_cleaned_oct25_jun26.csv"))
    after_API = pd.read_csv(data_path("processed", "airbnb_with_sa2.csv"))

    print(f"Rows in cleaned Airbnb dataset: {len(pre_API)}")
    print(f"Rows in SA2 output file:        {len(after_API)}")

    if len(pre_API) == len(after_API):
        print("✓ Row count unchanged — no duplicates added.")
    else:
        print("✗ WARNING: Row count changed — duplicates likely added!")

    unique_ids_before = pre_API["id"].nunique()
    unique_ids_after = after_API["id"].nunique()

    print(f"Unique IDs before merge: {unique_ids_before}")
    print(f"Unique IDs after merge:  {unique_ids_after}")

    if unique_ids_before == unique_ids_after:
        print("✓ Unique ID count unchanged.")
    else:
        print("✗ WARNING: Unique ID count changed — merge may be incorrect!")

    missing_sa2 = after_API["sa2_name"].isna().sum() + after_API["sa2_code"].isna().sum()

    if missing_sa2 == 0:
        print("✓ All listings have SA2 values.")
    else:
        print(f"✗ WARNING: {missing_sa2} SA2 values missing.")

    if after_API.duplicated().any():
        print("✗ WARNING: Duplicate rows found in final SA2 file!")
    else:
        print("✓ No duplicate rows in final SA2 file.")


# ------------------------------------------------------------
# 4. Allow standalone execution
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
