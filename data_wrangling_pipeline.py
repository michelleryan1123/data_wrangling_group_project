# ============================================
# DATA422 GROUP PROJECT PIPELINE
# ============================================

import sys

# Ensure redirected pipeline output supports UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from Code.load_concat_airbnb import main as load_airbnb
from Code.chch_airbnb_stats import main as airbnb_stats
from Code.clean_airbnb import main as clean_airbnb
from Code.load_clean_tenancy import main as clean_tenancy
from Code.API_SA2query_airbnb_locations import main as query_sa2
from Code.join_airbnb_tenancy import main as join_airbnb_tenancy
from Code.price_gap import main as price_gap
from Code.compare_airbnb_tenancy import main as compare_airbnb_tenancy

from paths import data_path, out_path


# ------------------------------------------------------------
# 1. Create required project directories
# ------------------------------------------------------------

def setup_directories():

    required_directories = [
        data_path("raw"),
        data_path("processed"),
        out_path("plots"),
        out_path("logs"),
    ]

    for directory in required_directories:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

    print(
        "Required folders checked."
    )


# ------------------------------------------------------------
# 2. Check required raw inputs before running pipeline
# ------------------------------------------------------------

def check_inputs():

    raw_airbnb_directory = data_path(
        "raw"
    )

    airbnb_files = list(
        raw_airbnb_directory.glob(
            "*_listings.csv"
        )
    )

    if not airbnb_files:

        raise FileNotFoundError(
            "No raw Airbnb files were found in "
            "Data/raw/. Expected files matching "
            "'*_listings.csv'."
        )

    tenancy_file = data_path(
        "raw",
        "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
    )

    if not tenancy_file.exists():

        raise FileNotFoundError(
            "The raw Tenancy Services file was not "
            "found in Data/raw/:\n"
            "Detailed-Quarterly-Tenancy-"
            "Q1-2020-Q3-2026.csv"
        )

    print(
        f"Input check passed: "
        f"{len(airbnb_files)} Airbnb files "
        f"and 1 tenancy file found."
    )


# ------------------------------------------------------------
# 3. Check important pipeline outputs
# ------------------------------------------------------------

def check_outputs():

    expected_outputs = {

        "Combined Airbnb dataset":
            data_path(
                "processed",
                "chch_airbnb.csv"
            ),

        "Cleaned Airbnb dataset":
            data_path(
                "processed",
                "airbnb_cleaned.csv"
            ),

        "Cleaned tenancy dataset":
            data_path(
                "processed",
                "tenancy_cleaned.csv"
            ),

        "Airbnb with SA2 dataset":
            data_path(
                "processed",
                "airbnb_with_sa2.csv"
            ),

        "Joined Airbnb + tenancy dataset":
            data_path(
                "processed",
                "airbnb_tenancy_joined.csv"
            ),

        "Listing-quarter price gaps":
            data_path(
                "processed",
                "listing_quarter_gaps.csv"
            ),

        "Area-quarter price gaps":
            data_path(
                "processed",
                "area_quarter_gaps.csv"
            ),

        "Area gap summary":
            data_path(
                "processed",
                "area_gap_summary.csv"
            ),

        "Sensitivity analysis":
            data_path(
                "processed",
                "sensitivity.csv"
            ),

        "Airbnb vs rental comparison table":
            data_path(
                "processed",
                "airbnb_vs_rental_comparison_final.csv"
            ),

        "Price histogram":
            out_path(
                "plots",
                "price_histograms.png"
            ),

        "Review histogram":
            out_path(
                "plots",
                "review_histograms.png"
            ),

        "Price-gap distribution plot":
            out_path(
                "plots",
                "top_area_distribution.png"
            ),

        "Airbnb vs rental comparison plot":
            out_path(
                "plots",
                "airbnb_vs_rental_barchart.png"
            ),
    }

    print(
        "\n=== FINAL OUTPUT CHECK ==="
    )

    missing_outputs = []

    for description, file_path in expected_outputs.items():

        if file_path.exists():

            print(
                f"PASS: {description}"
            )

        else:

            print(
                f"FAIL: {description}"
            )

            missing_outputs.append(
                file_path
            )

    if missing_outputs:

        missing_text = "\n".join(
            str(path)
            for path in missing_outputs
        )

        raise FileNotFoundError(
            "\nPipeline finished running, but some "
            "expected outputs were not created:\n"
            f"{missing_text}"
        )

    print(
        "\nAll expected pipeline outputs were created."
    )


# ------------------------------------------------------------
# 4. Run complete pipeline
# ------------------------------------------------------------

def run_pipeline():

    setup_directories()

    check_inputs()

    print(
        "\nSTEP 1: Load + combine Airbnb raw files"
    )
    load_airbnb()

    print(
        "\nSTEP 2: Airbnb summary statistics + plots"
    )
    airbnb_stats()

    print(
        "\nSTEP 3: Clean Airbnb dataset"
    )
    clean_airbnb()

    print(
        "\nSTEP 4: Clean tenancy dataset"
    )
    clean_tenancy()

    print(
        "\nSTEP 5: SA2 lookup"
    )
    query_sa2()

    print(
        "\nSTEP 6: Join Airbnb and tenancy datasets "
        "and check CHCH central"
    )
    join_airbnb_tenancy()

    print(
        "\nSTEP 7: Biggest price gaps between Airbnb "
        "and rental bonds"
    )
    price_gap()

    print(
        "\nSTEP 8: Compare Airbnb listings vs "
        "active rental bonds"
    )
    compare_airbnb_tenancy()

    check_outputs()

    print(
        "\nPIPELINE COMPLETE"
    )


if __name__ == "__main__":
    run_pipeline()