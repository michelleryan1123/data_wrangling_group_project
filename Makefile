# MakeFile to run the entire project pipeline

# ------------------------------------------
# PATHS
# ------------------------------------------
code = Code
data_raw = Data/raw
data_processed = Data/processed
plots = out/plots

# ------------------------------------------
# define the final target to ensure Makefile runs all steps
all: $(data_processed)/airbnb_vs_rental_comparison_final.csv

# ------------------------------------------
# STEP 1 — Load + concatenate Airbnb data
# Output: Data/processed/chch_airbnb.csv
# ------------------------------------------

$(data_processed)/chch_airbnb.csv: \
$(code)/load_concat_airbnb.py
	python $(code)/load_concat_airbnb.py

# ------------------------------------------
# STEP 2 — Summary statistics + plots
# Output: price_histograms.png, review_histograms.png
# ------------------------------------------

$(plots)/price_histograms.png $(plots)/review_histograms.png: \
$(code)/chch_airbnb_stats.py \
$(data_processed)/chch_airbnb.csv
	python $(code)/chch_airbnb_stats.py

analysis: $(plots)/price_histograms.png $(plots)/review_histograms.png

# ------------------------------------------
# STEP 3 — Clean Airbnb data
# Output: Data/processed/airbnb_cleaned.csv
# ------------------------------------------

$(data_processed)/airbnb_cleaned.csv: \
$(code)/clean_airbnb.py \
$(data_processed)/chch_airbnb.csv
	python $(code)/clean_airbnb.py

# ------------------------------------------
# STEP 4 — clean tenancy data
# Output: Data/processed/tenancy_cleaned.csv
# ------------------------------------------

$(data_processed)/tenancy_cleaned.csv: \
$(code)/load_clean_tenancy.py \
$(data_raw)/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv
	python $(code)/load_clean_tenancy.py

# ------------------------------------------
# STEP 5 - Add location to airbnb data from SA2
# Output: Data/processed/airbnb_with_SA2.csv
# ------------------------------------------

$(data_processed)/airbnb_with_sa2.csv: \
$(code)/API_SA2query_airbnb_locations.py \
$(data_processed)/airbnb_cleaned.csv
	python $(code)/API_SA2query_airbnb_locations.py

# ------------------------------------------
# STEP 6 - Join airbnb and tenancy data, check chch central
# Output: Data/processed/airbnb_tenancy_joined.csv
# ------------------------------------------

$(data_processed)/airbnb_tenancy_joined.csv: \
$(code)/join_airbnb_tenancy.py \
$(data_processed)/airbnb_with_sa2.csv \
$(data_processed)/tenancy_cleaned.csv
	python $(code)/join_airbnb_tenancy.py

# ------------------------------------------
# STEP 7 - - calculate the biggest difference between airbnb and tenancy data
# Outputs:
#   Data/processed/listing_quarter_gaps.csv
#   Data/processed/area_quarter_gaps.csv
#   Data/processed/area_gap_summary.csv
#   Data/processed/sensitivity.csv
#   out/plots/top_area_distribution.png
# ------------------------------------------

$(data_processed)/listing_quarter_gaps.csv \
$(data_processed)/area_quarter_gaps.csv \
$(data_processed)/area_gap_summary.csv \
$(data_processed)/sensitivity.csv \
$(plots)/top_area_distribution.png: \
$(code)/price_gap.py \
$(data_processed)/airbnb_with_sa2.csv \
$(data_processed)/tenancy_cleaned.csv
	python $(code)/price_gap.py


# ------------------------------------------
# STEP 8 
# Outputs:
#   Data/processed/airbnb_vs_rental_comparison_final.csv
#   out/plots/airbnb_vs_rental_barchart.png
# ------------------------------------------

$(data_processed)/airbnb_vs_rental_comparison_final.csv \
$(plots)/airbnb_vs_rental_barchart.png: \
$(code)/compare_airbnb_tenancy.py \
$(data_processed)/airbnb_tenancy_joined.csv
	python $(code)/compare_airbnb_tenancy.py