import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt
from paths import data_path, out_path
from Code.utils import custom_functions as cf


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
def load_data():
    df = pd.read_csv(data_path("processed", "chch_airbnb_oct25_jun26.csv"))
    print("Loaded dataset:", df.shape)
    return df


# ---------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------
def summary_statistics(df):
    print("\n=== Summary Stats for Entire Dataset ===")
    full_summary = cf.summary_stats(df)
    print(full_summary)

    print("\n=== Summary Stats for Top 10% Listings (by number_of_reviews) ===")
    top10per, top10_summary = cf.highest_reviews(df)
    print(top10_summary)


# ---------------------------------------------------------
# Price histograms
# ---------------------------------------------------------
def price_histograms(df):
    price = df["price"].dropna()

    fig, axes = plt.subplots(3, 1, figsize=(10, 15))

    # 1. Default bins
    axes[0].hist(price, bins=50)
    axes[0].set_title("Price Distribution (50 bins)")
    axes[0].set_xlabel("Price per night (NZD)")
    axes[0].set_ylabel("Listings")

    # 2. Custom bins
    bins = [0,100,200,300,400,500,750,1000,1250,1500,2000,3000,4000,5000]
    axes[1].hist(price, bins=bins)
    axes[1].set_title("Price Distribution (Custom bins)")
    axes[1].set_xlabel("Price per night (NZD)")
    axes[1].set_ylabel("Listings")

    # 3. Zoomed (<1000)
    price_below1000 = price[price <= 1000]
    axes[2].hist(price_below1000, bins=50)
    axes[2].set_title("Price Distribution (<$1000)")
    axes[2].set_xlabel("Price per night (NZD)")
    axes[2].set_ylabel("Listings")
    axes[2].set_xlim(0, 1000)

    plt.subplots_adjust(hspace=0.6)

    save_file = out_path("plots", "price_histograms.png")
    fig.savefig(save_file, dpi=300, bbox_inches="tight")
    print("Saved:", save_file)


# ---------------------------------------------------------
# Review histograms
# ---------------------------------------------------------
def review_histograms(df):
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    reference_date = pd.Timestamp("2026-06-22")
    df["days_since_last_review"] = (reference_date - df["last_review"]).dt.days

    review_data = df.dropna(subset=["days_since_last_review"])

    review_5000 = review_data[review_data["days_since_last_review"] <= 5000]
    review_750 = review_data[review_data["days_since_last_review"] <= 750]

    fig, axes = plt.subplots(3, 1, figsize=(10, 18))

    # 1. 100 bins
    axes[0].hist(review_5000["days_since_last_review"], bins=100)
    axes[0].set_title("Days Since Last Review (100 bins)")
    axes[0].set_xlabel("Days")
    axes[0].set_ylabel("Listings")

    # 2. Custom bins
    bins2 = [0,10,20,30,40,50,75,100,125,150,175,200,250,500,750,1000,
             1500,2000,3000,4000,5000]
    axes[1].hist(review_5000["days_since_last_review"], bins=bins2)
    axes[1].set_title("Days Since Last Review (Custom bins)")
    axes[1].set_xlabel("Days")
    axes[1].set_ylabel("Listings")

    # 3. Past 750 days
    axes[2].hist(review_750["days_since_last_review"], bins=50)
    axes[2].set_title("Days Since Last Review (<750 days)")
    axes[2].set_xlabel("Days")
    axes[2].set_ylabel("Listings")

    plt.subplots_adjust(hspace=0.5)

    save_file = out_path("plots", "review_histograms.png")
    fig.savefig(save_file, dpi=300, bbox_inches="tight")
    print("Saved:", save_file)


# ---------------------------------------------------------
# Main pipeline step
# ---------------------------------------------------------
def main():
    df = load_data()
    summary_statistics(df)
    price_histograms(df)
    review_histograms(df)


if __name__ == "__main__":
    main()
