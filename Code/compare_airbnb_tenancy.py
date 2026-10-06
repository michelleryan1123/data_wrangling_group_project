# ==========================================================
# Compare Airbnb listings vs Active Rental Bonds based on
# SA2 location.
#
# Outputs:
# - comparison CSV in Data/processed
# - comparison bar chart in out/plots
# ==========================================================

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import matplotlib.pyplot as plt

from paths import data_path, out_path


def main():

    print(
        "\n=== STEP 8: Compare Airbnb listings "
        "vs Active Rental Bonds ==="
    )

    # ============================================================
    # 1. Load the already-joined dataset
    # ============================================================

    df = pd.read_csv(
        data_path(
            "processed",
            "airbnb_tenancy_joined.csv"
        )
    )

    # ============================================================
    # 2. Count unique Airbnb listings by SA2
    # ============================================================

    airbnb_counts = (
        df
        .groupby(
            [
                "sa2_code",
                "sa2_name"
            ]
        )["id"]
        .nunique()
        .reset_index(
            name="Airbnb Listings"
        )
    )

    # ============================================================
    # 3. Get Active Rental Bonds by SA2
    # ============================================================

    rental_data = (
        df[
            [
                "sa2_code",
                "sa2_name",
                "quarter",
                "Active Bonds"
            ]
        ]
        .dropna(
            subset=[
                "Active Bonds"
            ]
        )
        .drop_duplicates()
    )

    rental_counts = (
        rental_data
        .groupby(
            [
                "sa2_code",
                "sa2_name"
            ]
        )["Active Bonds"]
        .max()
        .reset_index(
            name="Active Rental Bonds"
        )
    )

    # ============================================================
    # 4. Merge Airbnb and rental counts
    # ============================================================

    comparison = airbnb_counts.merge(
        rental_counts,
        on=[
            "sa2_code",
            "sa2_name"
        ],
        how="left"
    )

    # ============================================================
    # 5. Calculate difference
    # ============================================================

    comparison["Difference"] = (
        comparison["Airbnb Listings"]
        - comparison["Active Rental Bonds"]
    )

    # ============================================================
    # 6. Sort by location
    # ============================================================

    comparison = comparison.sort_values(
        "sa2_name"
    )

    # ============================================================
    # 7. Display results
    # ============================================================

    print(
        "\nAirbnb Listings vs Active Rental Bonds "
        "by Location:\n"
    )

    print(
        comparison[
            [
                "sa2_code",
                "sa2_name",
                "Airbnb Listings",
                "Active Rental Bonds",
                "Difference"
            ]
        ].to_string(
            index=False
        )
    )

    # ============================================================
    # 8. Save comparison table
    # ============================================================

    output_csv = data_path(
        "processed",
        "airbnb_vs_rental_comparison_final.csv"
    )

    comparison.to_csv(
        output_csv,
        index=False
    )

    print(
        f"\nResults saved to {output_csv}"
    )

    # ============================================================
    # 9. Create comparison bar chart
    # ============================================================

    chart_data = (
        comparison
        .sort_values(
            "Airbnb Listings",
            ascending=False
        )
        .head(15)
        .sort_values(
            "Airbnb Listings"
        )
    )

    chart_data.set_index(
        "sa2_name"
    )[
        [
            "Airbnb Listings",
            "Active Rental Bonds"
        ]
    ].plot(
        kind="barh",
        figsize=(12, 8)
    )

    plt.xlabel("Number")
    plt.ylabel("SA2 Location")

    plt.title(
        "Airbnb Listings vs Active Rental Bonds "
        "by SA2 Location"
    )

    plt.legend()
    plt.tight_layout()

    # Use central project output-path helper
    plot_file = out_path(
        "plots",
        "airbnb_vs_rental_barchart.png"
    )

    plot_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.savefig(
        plot_file,
        dpi=170
    )

    print(
        f"Plot saved to {plot_file}"
    )

    plt.close()

    print(
        "\nComparison step complete."
    )


if __name__ == "__main__":
    main()