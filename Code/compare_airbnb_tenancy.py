# ==========================================================
# Compare Airbnb listings vs Active Rental Bonds based on SA2 location (from StatsNZ). The output is a CSV file saved to the processed folder, and a bar chart saved to out/plots.
# The output is a comparison csv saved to the processed folder, and a figure saved to the plots folder
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
from paths import data_path
from pathlib import Path


def main():

    print("\n=== STEP 8: Compare Airbnb listings vs Active Rental Bonds ===")

    # ============================================================
    # 1. LOAD THE ALREADY-JOINED DATASET
    # ============================================================

    df = pd.read_csv(data_path("processed", "airbnb_tenancy_joined.csv"))

    # ============================================================
    # 2. COUNT UNIQUE AIRBNB LISTINGS BY SA2 LOCATION
    # ============================================================

    airbnb_counts = (
        df.groupby(["sa2_code", "sa2_name"])["id"]
        .nunique()
        .reset_index(name="Airbnb Listings")
    )

    # ============================================================
    # 3. GET ACTIVE RENTAL BONDS BY SA2 LOCATION
    # ============================================================

    rental_data = (
        df[["sa2_code", "sa2_name", "quarter", "Active Bonds"]]
        .dropna(subset=["Active Bonds"])
        .drop_duplicates()
    )

    rental_counts = (
        rental_data.groupby(["sa2_code", "sa2_name"])["Active Bonds"]
        .max()
        .reset_index(name="Active Rental Bonds")
    )

    # ============================================================
    # 4. MERGE THE TWO COUNTS INTO ONE COMPARISON TABLE
    # ============================================================

    comparison = airbnb_counts.merge(
        rental_counts,
        on=["sa2_code", "sa2_name"],
        how="left"
    )

    # ============================================================
    # 5. CALCULATE THE DIFFERENCE
    # ============================================================

    comparison["Difference"] = (
        comparison["Airbnb Listings"] - comparison["Active Rental Bonds"]
    )

    # ============================================================
    # 6. SORT BY LOCATION
    # ============================================================

    comparison = comparison.sort_values("sa2_name")

    # ============================================================
    # 7. DISPLAY THE RESULTS
    # ============================================================

    print("\nAirbnb Listings vs Active Rental Bonds by Location:\n")
    print(
        comparison[
            [
                "sa2_code",
                "sa2_name",
                "Airbnb Listings",
                "Active Rental Bonds",
                "Difference"
            ]
        ].to_string(index=False)
    )

    # ============================================================
    # 8. SAVE THE COMPARISON TABLE
    # ============================================================

    output_csv = data_path("processed", "airbnb_vs_rental_comparison_final.csv")
    comparison.to_csv(output_csv, index=False)
    print(f"\nResults saved to {output_csv}")

    # ============================================================
    # 9. CREATE A BAR CHART
    # ============================================================

    chart_data = (
        comparison.sort_values("Airbnb Listings", ascending=False)
        .head(15)
        .sort_values("Airbnb Listings")
    )

    chart_data.set_index("sa2_name")[["Airbnb Listings", "Active Rental Bonds"]].plot(
        kind="barh",
        figsize=(12, 8)
    )

    plt.xlabel("Number")
    plt.ylabel("SA2 Location")
    plt.title("Airbnb Listings vs Active Rental Bonds by SA2 Location")
    plt.legend()
    plt.tight_layout()

    # Save plot into out/plots
    plots_dir = Path("out/plots")
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plots_dir / "airbnb_vs_rental_barchart.png", dpi=170)

    print(f"Plot saved to {plots_dir / 'airbnb_vs_rental_barchart.png'}")

    plt.close()

    print("\nComparison step complete.")


if __name__ == "__main__":
    main()
