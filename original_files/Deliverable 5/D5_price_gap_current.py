"""DATA201 Deliverable 5: area-level Airbnb vs Tenancy rental price comparison.

Run from the project root after running D5_prepare_from_mapping.py and fixing D4 Tenancy:
    python D5_price_gap_current.py
All input datasets stay local. Results are written to out/d5_ammar_gap.
The source coordinate mapping's geographic vintage must be verified separately.
"""
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

QUARTERS = pd.to_datetime(["2025-10-01", "2026-01-01", "2026-04-01"])
REQUIRED_AIRBNB = {"id", "month_year", "price", "room_type", "sa2_2019_code", "sa2_2019_name"}
REQUIRED_BONDS = {"Location Id", "TimeFrame", "Dwelling Type", "Number Of Beds", "Median Rent", "Total Bonds"}


def load_inputs(airbnb_file: Path, tenancy_file: Path):
    a = pd.read_csv(airbnb_file, dtype={"id": "string", "sa2_2019_code": "string"})
    b = pd.read_csv(tenancy_file, dtype={"Location Id": "string"})
    if REQUIRED_AIRBNB-set(a) or REQUIRED_BONDS-set(b):
        raise ValueError(f"Missing columns: Airbnb {REQUIRED_AIRBNB-set(a)} / Tenancy {REQUIRED_BONDS-set(b)}")
    if a.empty or b.empty:
        raise ValueError("Input is empty: verify D4 Tenancy date parsing (%Y-%m-%d) and Airbnb source")
    if a.id.isna().any() or not a.id.str.fullmatch(r"\d+").all():
        raise ValueError("Airbnb listing IDs are missing, damaged or in scientific notation")
    if a.sa2_2019_code.isna().any() or not a.sa2_2019_code.str.fullmatch(r"\d{6}").all():
        raise ValueError("Missing or malformed 2019 area codes")
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

    b["quarter"] = pd.to_datetime(b.TimeFrame, format="%Y-%m-%d", errors="raise")
    b["sa2_2019_code"] = b["Location Id"].str.replace(r"\.0$", "", regex=True)
    b = b.loc[b.quarter.isin(QUARTERS) & b["Dwelling Type"].eq("ALL") & b["Number Of Beds"].eq("ALL")].copy()
    if b.empty or b.duplicated(["sa2_2019_code", "quarter"]).any():
        raise ValueError("Overall Tenancy benchmarks missing or area-quarter not unique")
    b["Median Rent"] = pd.to_numeric(b["Median Rent"], errors="raise")
    b["Total Bonds"] = pd.to_numeric(b["Total Bonds"], errors="raise")
    if b[["Median Rent", "Total Bonds"]].isna().any().any() or not b["Median Rent"].gt(0).all():
        raise ValueError("Invalid bond benchmark rent/count")
    print(f"INPUTS: Airbnb {len(a):,} listing-months; bond ALL/ALL benchmarks {len(b):,} rows")
    return a,b[["sa2_2019_code", "quarter", "Median Rent", "Total Bonds"]]


def compute(a, b, min_listings=5, min_quarters=2, min_bonds=5, moving="exclude_ids"):
    if moving == "exclude_ids":
        mult = a.groupby("id").sa2_2019_code.nunique()
        bad_ids = set(mult[mult.gt(1)].index)
        selected = a.loc[~a.id.isin(bad_ids)].copy()
        removed_ids, removed_months = len(bad_ids),len(a)-len(selected)
    elif moving == "exclude_ambiguous_quarters":
        ambiguity = a.groupby(["id", "quarter"]).sa2_2019_code.transform("nunique") > 1
        selected = a.loc[~ambiguity].copy()
        removed_ids, removed_months = a.loc[ambiguity,"id"].nunique(),int(ambiguity.sum())
    else:
        raise ValueError("Unsupported geographic-ambiguity policy")

    # Only one observation per listing and quarter; never average over multiple SA2s.
    lq = selected.groupby(["id", "sa2_2019_code", "quarter"],as_index=False).agg(
        nightly_price=("price", "median"), observed_months=("month", "nunique"),
        sa2_name=("sa2_2019_name", "first"), room_type=("room_type", "first"))
    if lq.duplicated(["id", "quarter"]).any():
        raise ValueError("Listing-quarter duplicated after spatial ambiguity handling")
    merged = lq.merge(b, on=["sa2_2019_code", "quarter"], how="left",validate="many_to_one", indicator=True)
    if len(merged)!=len(lq):
        raise ValueError("Many-to-one bond join changed Airbnb listing-quarter count")
    matched = merged.loc[merged._merge.eq("both")].drop(columns="_merge").copy()
    if matched.empty:
        raise ValueError("No matching rent records. Check actual 2019 codes and dates")
    matched["long_term_nightly"] = matched["Median Rent"]/7
    matched["gap_nzd_night"] = matched.nightly_price-matched.long_term_nightly
    aq=matched.groupby(["sa2_2019_code", "quarter"],as_index=False).agg(
        sa2_name=("sa2_name","first"), listings=("id","nunique"),
        median_airbnb_nightly=("nightly_price","median"), weekly_rent=("Median Rent","first"),
        bonds=("Total Bonds","first"),median_gap=("gap_nzd_night","median"),
        max_individual_gap=("gap_nzd_night","max"))
    if not ((aq.median_gap - (aq.median_airbnb_nightly-aq.weekly_rent/7)).abs()<1e-7).all():
        raise ValueError("Manual-equivalent median gap check failed")
    qual=aq.loc[(aq.listings>=min_listings) & (aq.bonds>=min_bonds)]
    rank=qual.groupby("sa2_2019_code",as_index=False).agg(
        sa2_name=("sa2_name","first"),qualifying_quarters=("quarter","nunique"),
        listing_quarters=("listings","sum"),typical_gap_nzd_night=("median_gap","median"),
        typical_airbnb_nightly=("median_airbnb_nightly","median"),
        typical_weekly_rent=("weekly_rent","median"),smallest_bond_count=("bonds","min"))
    rank=rank.loc[rank.qualifying_quarters>=min_quarters].sort_values("typical_gap_nzd_night",ascending=False).reset_index(drop=True)
    if rank.empty:
        raise ValueError("No areas meet thresholds")
    audit={"excluded_listing_ids":removed_ids, "excluded_listing_months":removed_months,
           "listing_quarters":len(lq), "matched_listing_quarters":len(matched),
           "unmatched_listing_quarters":len(lq)-len(matched), "qualifying_areas":len(rank)}
    return matched,aq,rank,audit


def make_charts(matched, aq, rank, output: Path):
    # Identify the area with the largest typical gap
    top_code = rank.iloc[0]["sa2_2019_code"]
    top_name = rank.iloc[0]["sa2_name"]

    # Find quarters that meet the minimum requirements
    qualifying_quarters = aq.loc[
        (aq["sa2_2019_code"] == top_code)
        & (aq["listings"] >= 5)
        & (aq["bonds"] >= 5),
        "quarter"
    ]

    # Select only observations from qualifying quarters
    vals = matched.loc[
        (matched["sa2_2019_code"] == top_code)
        & (matched["quarter"].isin(qualifying_quarters)),
        "gap_nzd_night"
    ]

    # Check that the histogram matches the analysis sample
    assert len(vals) == rank.iloc[0]["listing_quarters"]

    print("Histogram observations:", len(vals))

    # Create the corrected histogram
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.hist(vals, bins=min(15, max(5, len(vals)//2)))

    ax.set(
        xlabel="Individual listing-quarter price gap (NZD per night)",
        ylabel="Listing-quarter observations",
        title=f"Price-gap distribution: {top_name} (qualifying quarters only)"
    )

    fig.tight_layout()

    fig.savefig(
        output / "top_area_distribution.png",
        dpi=170
    )

    plt.close(fig)

def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("--airbnb",type=Path,default=Path("Data/airbnb_with_sa2_2019.csv"))
    parser.add_argument("--tenancy",type=Path,default=Path("Data/tenancy_cleaned_oct25_jun26.csv"))
    parser.add_argument("--out",type=Path,default=Path("out/d5_ammar_gap"))
    args=parser.parse_args()
    a,b=load_inputs(args.airbnb,args.tenancy)
    matched,aq,rank,stats=compute(a,b)
    cases=[("primary",a,5,2,5,"exclude_ids"),
           ("exclude only ambiguous listing-quarters",a,5,2,5,"exclude_ambiguous_quarters"),
           ("at least 10 listings per quarter",a,10,2,5,"exclude_ids"),
           ("at least 20 bonds per quarter",a,5,2,20,"exclude_ids"),
           ("all three quarters",a,5,3,5,"exclude_ids"),
           ("entire homes only",a.loc[a.room_type.eq("Entire home/apt")],5,2,5,"exclude_ids"),
           ("exclude Dec 25 / Jan-Feb 26 fully imputed months",
            a.loc[~a.month.dt.strftime("%Y-%m").isin(["2025-12","2026-01","2026-02"])],5,2,5,"exclude_ids"),
           ("exclude nightly prices above $3,000 (sensitivity)",a.loc[a.price.le(3000)],5,2,5,"exclude_ids"),
           ("at least 20 listings per quarter",a,20,2,5,"exclude_ids")]
    sensitivity=[]
    for label,frame,ml,mq,mb,moving in cases:
        try:
            _,_,r,s=compute(frame,b,ml,mq,mb,moving)
            first=r.iloc[0]
            sensitivity.append({"scenario":label,"leading_area":first.sa2_name,"area_code":first.sa2_2019_code,
                                "gap_nzd_night":round(first.typical_gap_nzd_night,2),
                                "qualifying_quarters":int(first.qualifying_quarters),
                                "listing_quarters":int(first.listing_quarters),
                                "qualifying_areas":len(r)})
        except ValueError as exc:
            sensitivity.append({"scenario":label,"leading_area":f"Unavailable: {exc}"})
    sensitivity=pd.DataFrame(sensitivity)
    args.out.mkdir(parents=True,exist_ok=True)
    matched.to_csv(args.out/"listing_quarter_gaps.csv",index=False)
    aq.to_csv(args.out/"area_quarter_gaps.csv",index=False)
    rank.to_csv(args.out/"area_gap_summary.csv",index=False)
    sensitivity.to_csv(args.out/"sensitivity.csv",index=False)
    make_charts(matched,aq,rank,args.out)
    first=rank.iloc[0]
    print("ANALYSIS AUDIT",stats)
    print("\nTOP AREAS\n",rank.head(12).to_string(index=False))
    print("\nSENSITIVITY\n",sensitivity.to_string(index=False))
    text=("# DATA201 D5 price-gap audit — supplied file labelled SA2-2019\n\n"
          "**Conditional finding:** confirm the mapping's provenance as Stats NZ SA2-2019 and reconcile D4 Airbnb cleaning before calling this final.\n\n"
          "Method: convert Tenancy ALL/ALL median weekly rent to nightly by dividing by 7; take one median asking price "
          "for each Airbnb listing-quarter; take median of listing gaps per area-quarter; take median of qualifying "
          "area-quarter gaps per area. Filters: >=5 listings/area-quarter, >=5 bonds and >=2 qualifying quarters. "
          "These thresholds are analyst choices.\n\n"
          f"Input listing-months: {len(a):,}; excluded ambiguous listing IDs: {stats['excluded_listing_ids']:,} "
          f"({stats['excluded_listing_months']:,} listing-month rows). Remaining listing-quarters: {stats['listing_quarters']:,}; "
          f"matched to bonds: {stats['matched_listing_quarters']:,}; unmatched: {stats['unmatched_listing_quarters']:,}; "
          f"eligible areas: {stats['qualifying_areas']:,}.\n\n"
          f"Largest typical gap with the stated rules: **{first.sa2_name}** (SA2-2019 {first.sa2_2019_code}), "
          f"**NZ${first.typical_gap_nzd_night:.2f}/night**, based on {first.listing_quarters} listing-quarter records "
          f"in {first.qualifying_quarters} qualifying quarters. "
          "This is a descriptive gap, not nightly income or profit.\n\n"
          "Cautions: D4 cleaned Airbnb file supplied still has prices above NZ$3,000 and differs from README row count; "
          "Dec 2025–Feb 2026 were entirely imputed; SA2 mapping provenance/shapefile not independently supplied; "
          "some properties shift mapped SA2 over months; geographic coverage incomplete after bond matching; "
          "bond data are provisional, privately lodged bonds, not all Christchurch properties.\n\n"
          "## Sensitivity\n\n"+sensitivity.to_string(index=False)+"\n")
    (args.out/"analysis_notes.md").write_text(text,encoding="utf-8")
    print("OUTPUT DIRECTORY:",args.out)
    return stats,rank,sensitivity


if __name__ == "__main__":
    main()
