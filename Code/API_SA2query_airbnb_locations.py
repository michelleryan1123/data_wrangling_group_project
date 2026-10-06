# =======================================================================
# Query SA2 (Statistical Area 2) from Koordinates for each Airbnb listing
# =======================================================================

import os
import sys
from multiprocessing import Pool
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import requests
from tqdm import tqdm

from config import API_WORKERS, KOORDINATES_LAYER_ID
from paths import data_path


# ------------------------------------------------------------
# 1. Query Koordinates API for one Airbnb listing
# ------------------------------------------------------------

def query_sa2(row):

    api_key = os.getenv("KOORDINATES_API_KEY")

    if not api_key:
        raise RuntimeError(
            "KOORDINATES_API_KEY environment variable is not set."
        )

    latitude = row["latitude"]
    longitude = row["longitude"]

    url = (
        "https://koordinates.com/"
        "services/query/v1/vector.json"
    )

    params = {
        "key": api_key,
        "layer": KOORDINATES_LAYER_ID,
        "x": longitude,
        "y": latitude,
        "max_results": 1,
        "radius": 0,
        "geometry": "false",
        "with_field_names": "true"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        vector_query = data.get(
            "vectorQuery",
            {}
        )

        layers = vector_query.get(
            "layers",
            {}
        )

        layer = layers.get(
            str(KOORDINATES_LAYER_ID),
            {}
        )

        features = layer.get(
            "features",
            []
        )

        if not features:

            return {
                "id": row["id"],
                "sa2_name": None,
                "sa2_code": None
            }

        properties = (
            features[0]
            .get(
                "properties",
                {}
            )
        )

        return {
            "id": row["id"],
            "sa2_name": properties.get(
                "SA22026_V1_00_NAME"
            ),
            "sa2_code": properties.get(
                "SA22026_V1_00"
            )
        }

    except requests.RequestException as error:

        print(
            f"API request failed for listing "
            f"{row['id']}: {error}"
        )

        return {
            "id": row["id"],
            "sa2_name": None,
            "sa2_code": None
        }

    except (
        KeyError,
        TypeError,
        ValueError
    ) as error:

        print(
            f"Invalid API response for listing "
            f"{row['id']}: {error}"
        )

        return {
            "id": row["id"],
            "sa2_name": None,
            "sa2_code": None
        }


# ------------------------------------------------------------
# 2. Query multiple Airbnb listings in parallel
# ------------------------------------------------------------

def run_parallel(
    dataframe,
    workers=API_WORKERS
):

    rows = dataframe.to_dict(
        "records"
    )

    if not rows:

        return pd.DataFrame(
            columns=[
                "id",
                "sa2_name",
                "sa2_code"
            ]
        )

    with Pool(
        processes=workers
    ) as pool:

        results = list(
            tqdm(
                pool.imap(
                    query_sa2,
                    rows
                ),
                total=len(rows),
                desc="Querying SA2 API"
            )
        )

    return pd.DataFrame(
        results
    )


# ------------------------------------------------------------
# 3. Load any reusable SA2 mappings
# ------------------------------------------------------------

def load_existing_mapping(
    sa2_file
):

    if not sa2_file.exists():

        return pd.DataFrame(
            columns=[
                "id",
                "sa2_name",
                "sa2_code"
            ]
        )

    existing = pd.read_csv(
        sa2_file
    )

    required_columns = {
        "id",
        "sa2_name",
        "sa2_code"
    }

    if not required_columns.issubset(
        existing.columns
    ):

        print(
            "Existing SA2 file does not contain "
            "the required mapping columns. "
            "Existing mappings will not be reused."
        )

        return pd.DataFrame(
            columns=[
                "id",
                "sa2_name",
                "sa2_code"
            ]
        )

    existing_mapping = (
        existing[
            [
                "id",
                "sa2_name",
                "sa2_code"
            ]
        ]
        .dropna(
            subset=[
                "sa2_name",
                "sa2_code"
            ]
        )
        .drop_duplicates(
            subset=["id"],
            keep="last"
        )
        .copy()
    )

    return existing_mapping


# ------------------------------------------------------------
# 4. Main SA2 pipeline step
# ------------------------------------------------------------

def main():

    print(
        "\n=== STEP 5: SA2 LOOKUP ==="
    )

    cleaned_airbnb_file = data_path(
        "processed",
        "airbnb_cleaned.csv"
    )

    sa2_file = data_path(
        "processed",
        "airbnb_with_sa2.csv"
    )

    # --------------------------------------------------------
    # Load CURRENT cleaned Airbnb dataset
    # --------------------------------------------------------

    clean_airbnb = pd.read_csv(
        cleaned_airbnb_file
    )

    required_columns = {
        "id",
        "latitude",
        "longitude"
    }

    missing_columns = (
        required_columns
        - set(clean_airbnb.columns)
    )

    if missing_columns:

        raise ValueError(
            "Cleaned Airbnb dataset is missing "
            f"required columns: {missing_columns}"
        )

    current_unique = (
        clean_airbnb[
            [
                "id",
                "latitude",
                "longitude"
            ]
        ]
        .drop_duplicates(
            subset=["id"]
        )
        .copy()
    )

    print(
        "Current unique Airbnb listings:",
        len(current_unique)
    )

    # --------------------------------------------------------
    # Load reusable existing mappings
    # --------------------------------------------------------

    existing_mapping = (
        load_existing_mapping(
            sa2_file
        )
    )

    print(
        "Existing valid SA2 mappings available:",
        len(existing_mapping)
    )

    # --------------------------------------------------------
    # Find IDs that still require an API query
    # --------------------------------------------------------

    mapped_ids = set(
        existing_mapping["id"]
    )

    rows_to_query = (
        current_unique[
            ~current_unique["id"]
            .isin(mapped_ids)
        ]
        .copy()
    )

    print(
        "Listings requiring SA2 query:",
        len(rows_to_query)
    )

    # --------------------------------------------------------
    # Query only missing mappings
    # --------------------------------------------------------

    if not rows_to_query.empty:

        print(
            "Querying missing SA2 mappings..."
        )

        new_mapping = run_parallel(
            rows_to_query,
            workers=API_WORKERS
        )

        full_mapping = pd.concat(
            [
                existing_mapping,
                new_mapping
            ],
            ignore_index=True
        )

    else:

        print(
            "All current listings already have "
            "reusable SA2 mappings."
        )

        full_mapping = (
            existing_mapping.copy()
        )

    full_mapping = (
        full_mapping
        .drop_duplicates(
            subset=["id"],
            keep="last"
        )
        .copy()
    )

    # --------------------------------------------------------
    # Rebuild SA2 output using CURRENT Airbnb dataset
    # --------------------------------------------------------

    airbnb_with_sa2 = (
        clean_airbnb.merge(
            full_mapping,
            on="id",
            how="left",
            validate="many_to_one"
        )
    )

    sa2_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    airbnb_with_sa2.to_csv(
        sa2_file,
        index=False
    )

    print(
        "Saved refreshed SA2 Airbnb dataset:",
        sa2_file
    )

    # --------------------------------------------------------
    # 5. Sanity checks
    # --------------------------------------------------------

    print(
        "\n=== SA2 SANITY CHECKS ==="
    )

    row_count_before = len(
        clean_airbnb
    )

    row_count_after = len(
        airbnb_with_sa2
    )

    print(
        "Rows before SA2 merge:",
        row_count_before
    )

    print(
        "Rows after SA2 merge:",
        row_count_after
    )

    if (
        row_count_before
        == row_count_after
    ):

        print(
            "PASS: Row count unchanged."
        )

    else:

        print(
            "WARNING: Row count changed."
        )

    unique_ids_before = (
        clean_airbnb["id"]
        .nunique()
    )

    unique_ids_after = (
        airbnb_with_sa2["id"]
        .nunique()
    )

    print(
        "Unique IDs before SA2 merge:",
        unique_ids_before
    )

    print(
        "Unique IDs after SA2 merge:",
        unique_ids_after
    )

    if (
        unique_ids_before
        == unique_ids_after
    ):

        print(
            "PASS: Unique ID count unchanged."
        )

    else:

        print(
            "WARNING: Unique ID count changed."
        )

    missing_sa2_rows = (
        airbnb_with_sa2[
            [
                "sa2_name",
                "sa2_code"
            ]
        ]
        .isna()
        .any(axis=1)
        .sum()
    )

    print(
        "Rows with missing SA2 values:",
        missing_sa2_rows
    )

    if missing_sa2_rows == 0:

        print(
            "PASS: All listings have SA2 values."
        )

    else:

        print(
            "WARNING: Some rows have missing "
            "SA2 values."
        )

    duplicate_rows = (
        airbnb_with_sa2
        .duplicated()
        .sum()
    )

    print(
        "Duplicate rows:",
        duplicate_rows
    )

    if duplicate_rows == 0:

        print(
            "PASS: No duplicate rows."
        )

    else:

        print(
            "WARNING: Duplicate rows found."
        )

    print(
        "\nSA2 lookup complete."
    )


if __name__ == "__main__":
    main()