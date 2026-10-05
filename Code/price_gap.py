
# ============================================================
# Compare Airbnb vs Tenancy rental price gaps by SA2 location and quarter (using the joined dataset). Plots are saved to the out/plots folder.
# ============================================================

# Add project root to Python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from paths import data_path

from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

QUARTERS = pd.to_datetime(["2025-10-01", "2026-01-01", "2026-04-01"])
REQUIRED_AIRBNB = {"id", "month_year", "price", "room_type", "sa2_code", "sa2_name"}
REQUIRED_BONDS = {"Location Id", "TimeFrame", "Dwelling Type", "Number Of Beds", "Median Rent", "Total Bonds"}


def load_inputs(airbnb_file: Path, tenancy_file: Path):
    a = pd.read_csv(airbnb_file, dtype={"id": "string", "sa2_code": "string"})
    b = pd.read_csv(tenancy_file, dtype={"Location Id": "string"})

    # Rename Airbnb columns if needed
    a = a.rename(columns={
        "sa2_2019_code": "sa2_code",
        "sa2_2019_name": "sa2_name"
    })

    if REQUIRED_AIRBNB - set(a) or REQUIRED_BONDS - set(b):
        raise ValueError(f"Missing columns: Airbnb {REQUIRED_AIRBNB-set(a)} / Tenancy {REQUIRED_BONDS-set(b)}")
    if a.empty or b.empty:
        raise ValueError("Input is empty: verify D4 Tenancy date parsing (%Y-%m-%d) and Airbnb source")
    if a.id.isna().any() or not a.id.str.fullmatch(r"\d+").all():
        raise ValueError("Airbnb listing IDs are missing, damaged or in scientific notation")

    labels = a.month_year.astype("string").str.strip().str.upper().str.replace("APRIL", "APR", regex=False).str.replace("JUNE", "JUN", regex=False)
    a["month"] = pd.to_datetime(labels, format="%b%y", errors="raise")

    if a.duplicated(["id", "month"]).any():
        raise ValueError("Repeated listing-month observations")

    a["quarter"] = a.month.dt.to_period("Q").dt.start_time
    if not a.quarter.isin(QUARTERS).all() or set(a.quarter) != set(QUARTERS):
        raise ValueError("Unexpected or missing study quarters in Airbnb")

    a["price"] = pd.to_numeric(a.price, errors="raise")
    if a.price.isna().any() or not a.price.gt(0).all():
        raise ValueError("Missing/nonpositive Airbnb price")

    # Tenancy
    b["quarter"] = pd.to_datetime(b.TimeFrame, errors="raise")
    b["sa2_code"] = b["Location Id"].str.replace(r"\.0$", "", regex=True)

    b = b.loc[b.quarter.isin(QUARTERS) &
              b["Dwelling Type"].eq("ALL") &
              b["Number Of Beds"].eq("ALL")].copy()

    if b.empty or b.duplicated(["sa2_code", "quarter"]).any():
        raise ValueError("Overall Tenancy benchmarks missing or area-quarter not unique")

    b["Median Rent"] = pd.to_numeric(b["Median Rent"], errors="raise")
    b["Total Bonds"] = pd.to_numeric(b["Total Bonds"], errors="raise")

    if b[["Median Rent", "Total Bonds"]].isna().any().any() or not b["Median Rent"].gt(0).all():
        raise ValueError("Invalid bond benchmark rent/count")

    print(f"INPUTS: Airbnb {len(a):,} listing-months; bond ALL/ALL benchmarks {len(b):,} rows")
    return a, b[["sa2_code", "quarter", "Median Rent", "Total Bonds"]]


def compute(a, b, min_listings=5, min_quarters=2, min_bonds=5, moving="exclude_ids"):
    if moving == "exclude_ids":
        mult = a.groupby("id").sa2_code.nunique()
        bad_ids = set(mult[mult.gt(1)].index)
        selected = a.loc[~a.id.isin(bad_ids)].copy()
        removed_ids, removed_months = len(bad_ids), len(a) - len(selected)
    elif moving == "exclude_ambiguous_quarters":
        ambiguity = a.groupby(["id", "quarter"]).sa2_code.transform("nunique") > 1
        selected = a.loc[~ambiguity].copy()
        removed_ids, removed_months = a.loc[ambiguity, "id"].nunique(), int(ambiguity.sum())
    else:
        raise ValueError("Unsupported geographic-ambiguity policy")

    lq = selected.groupby(["id", "sa2_code", "quarter"], as_index=False).agg(
        nightly_price=("price", "median"),
        observed_months=("month", "nunique"),
        sa2_name=("sa2_name", "first"),
        room_type=("room_type", "first")
    )

    if lq.duplicated(["id", "quarter"]).any():
        raise ValueError("Listing-quarter duplicated after spatial ambiguity handling")

    merged = lq.merge(b, on=["sa2_code", "quarter"], how="left", validate="many_to_one", indicator=True)
    if len(merged) != len(lq):
        raise ValueError("Many-to-one bond join changed Airbnb listing-quarter count")

    matched = merged.loc[merged._merge.eq("both")].drop(columns="_merge").copy()
    if matched.empty:
        raise ValueError("No matching rent records. Check actual SA2 codes and dates")

    matched["long_term_nightly"] = matched["Median Rent"] / 7
    matched["gap_nzd_night"] = matched.nightly_price - matched.long_term_nightly

    aq = matched.groupby(["sa2_code", "quarter"], as_index=False).agg(
        sa2_name=("sa2_name", "first"),
        listings=("id", "nunique"),
        median_airbnb_nightly=("nightly_price", "median"),
        weekly_rent=("Median Rent", "first"),
        bonds=("Total Bonds", "first"),
        median_gap=("gap_nzd_night", "median"),
        max_individual_gap=("gap_nzd_night", "max")
    )

    qual = aq.loc[(aq.listings >= min_listings) & (aq.bonds >= min_bonds)]
    rank = qual.groupby("sa2_code", as_index=False).agg(
        sa2_name=("sa2_name", "first"),
        qualifying_quarters=("quarter", "nunique"),
        listing_quarters=("listings", "sum"),
        typical_gap_nzd_night=("median_gap", "median"),
        typical_airbnb_nightly=("median_airbnb_nightly", "median"),
        typical_weekly_rent=("weekly_rent", "median"),
        smallest_bond_count=("bonds", "min")
    )

    rank = rank.loc[rank.qualifying_quarters >= min_quarters].sort_values("typical_gap_nzd_night", ascending=False).reset_index(drop=True)

    audit = {
        "excluded_listing_ids": removed_ids,
        "excluded_listing_months": removed_months,
        "listing_quarters": len(lq),
        "matched_listing_quarters": len(matched),
        "unmatched_listing_quarters": len(lq) - len(matched),
        "qualifying_areas": len(rank)
    }

    return matched, aq, rank, audit


def make_charts(matched, aq, rank, output: Path):
    top_code = rank.iloc[0]["sa2_code"]
    top_name = rank.iloc[0]["sa2_name"]

    qualifying_quarters = aq.loc[
        (aq["sa2_code"] == top_code) &
        (aq["listings"] >= 5) &
        (aq["bonds"] >= 5),
        "quarter"
    ]

    vals = matched.loc[
        (matched["sa2_code"] == top_code) &
        (matched["quarter"].isin(qualifying_quarters)),
        "gap_nzd_night"
    ]

    assert len(vals) == rank.iloc[0]["listing_quarters"]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(vals, bins=min(15, max(5, len(vals)//2)))

    ax.set(
        xlabel="Individual listing-quarter price gap (NZD per night)",
        ylabel="Listing-quarter observations",
        title=f"Price-gap distribution: {top_name} (qualifying quarters only)"
    )

    fig.tight_layout()
    fig.savefig(output / "top_area_distribution.png", dpi=170)
    plt.close(fig)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--airbnb", type=Path, default=Path("Data/processed/airbnb_with_sa2.csv"))
    parser.add_argument("--tenancy", type=Path, default=Path("Data/processed/tenancy_cleaned.csv"))
    parser.add_argument("--out", type=Path, default=Path("out/plots"))
    args = parser.parse_args()

    a, b = load_inputs(args.airbnb, args.tenancy)
    matched, aq, rank, stats = compute(a, b)

    args.out.mkdir(parents=True, exist_ok=True)

    # Save outputs into Data/processed
    matched.to_csv(data_path("processed", "listing_quarter_gaps.csv"), index=False)
    aq.to_csv(data_path("processed", "area_quarter_gaps.csv"), index=False)
    rank.to_csv(data_path("processed", "area_gap_summary.csv"), index=False)

    # Sensitivity analysis
    cases = [
        ("primary", a, 5, 2, 5, "exclude_ids"),
        ("exclude only ambiguous listing-quarters", a, 5, 2, 5, "exclude_ambiguous_quarters"),
        ("at least 10 listings per quarter", a, 10, 2, 5, "exclude_ids"),
        ("at least 20 bonds per quarter", a, 5, 2, 20, "exclude_ids"),
        ("all three quarters", a, 5, 3, 5, "exclude_ids"),
        ("entire homes only", a.loc[a.room_type.eq("Entire home/apt")], 5, 2, 5, "exclude_ids"),
        ("exclude Dec 25 / Jan-Feb 26 fully imputed months",
         a.loc[~a.month.dt.strftime("%Y-%m").isin(["2025-12", "2026-01", "2026-02"])], 5, 2, 5, "exclude_ids"),
        ("exclude nightly prices above $3,000 (sensitivity)", a.loc[a.price.le(3000)], 5, 2, 5, "exclude_ids"),
        ("at least 20 listings per quarter", a, 20, 2, 5, "exclude_ids")
    ]

    sensitivity = []
    for label, frame, ml, mq, mb, moving in cases:
        try:
            _, _, r, s = compute(frame, b, ml, mq, mb, moving)
            first = r.iloc[0]
            sensitivity.append({
                "scenario": label,
                "leading_area": first.sa2_name,
                "area_code": first.sa2_code,
                "gap_nzd_night": round(first.typical_gap_nzd_night, 2),
                "qualifying_quarters": int(first.qualifying_quarters),
                "listing_quarters": int(first.listing_quarters),
                "qualifying_areas": len(r)
            })
        except ValueError as exc:
            sensitivity.append({"scenario": label, "leading_area": f"Unavailable: {exc}"})

    sensitivity = pd.DataFrame(sensitivity)
    sensitivity.to_csv(data_path("processed", "sensitivity.csv"), index=False)

    make_charts(matched, aq, rank, args.out)

    print("OUTPUT DIRECTORY:", args.out)
    return stats, rank, sensitivity


if __name__ == "__main__":
    main()
