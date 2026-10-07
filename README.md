 # DATA201/422 Group Project

Repository for our DATA201/422 Christchurch Rental Market group project.

 Dataset Source - Airbnb
 
# Deliverable 6 – Automation Changes and Updated Airbnb Data
## Overview

For Deliverable 6, the existing data-wrangling workflow was converted into a reproducible, automated end-to-end pipeline. The pipeline reduces manual work, improves reproducibility, adds validation, and makes the project easier for another team member to run.

The complete workflow can now be run with:

```bash
python data_wrangling_pipeline.py
```


The pipeline runs all 8 project stages in sequence.

---

## 1. One-Command End-to-End Pipeline

Created `data_wrangling_pipeline.py` as the single entry point for the project.

```bash
python data_wrangling_pipeline.py
```

This runs all 8 stages of the data wrangling workflow in the correct order.

---

## 2. Automatic Input Checking

The pipeline checks that the required Airbnb and Tenancy Services input files exist before processing begins.

If an important input file is missing, the pipeline stops early and reports a clear error.

---

## 3. Automatic Folder Creation

The pipeline automatically creates the required project folders:

```text
Data/raw/
Data/processed/
out/plots/
out/logs/
```

This reduces the amount of manual project setup required.

---

## 4. Centralised Path Management

`paths.py` was improved so that the project root is determined from the location of `paths.py` itself.

The project therefore no longer depends on the repository being named exactly:

```text
DATA422_group_project
```

This improves portability and reproducibility across different machines and folder locations.

---

## 5. Centralised Configuration

A new `config.py` file was added to store important project settings in one location, including:

* Airbnb extreme-price threshold
* Koordinates layer ID
* Number of API workers

This reduces hard-coded values across individual scripts and makes configuration easier to maintain.

---

## 6. Smarter SA2 API Automation

The SA2 mapping process was improved so that existing valid mappings are reused.

Only listings without an existing SA2 mapping are sent to the Koordinates API.

Final run:

* Current listings: **3,949**
* Reusable mappings: **3,949**
* New API queries required: **0**

This avoids unnecessary API requests and significantly reduces processing time when the pipeline is rerun.

---

## 7. Secure API Key Handling

The Koordinates API key is no longer stored directly in the active project code.

Instead, it is read from the environment variable:

```text
KOORDINATES_API_KEY
```

This prevents the API key from being exposed in the repository and improves security when working with GitHub and collaborating as a team.

---

## 8. Final Output Validation

At the end of the pipeline, the expected datasets and plots are checked automatically.

Each expected output is reported as either:

```text
PASS
```

or

```text
FAIL
```

If an important output is missing, the pipeline raises an error instead of silently completing.

---

## 9. End-to-End Validation

The complete pipeline was run from beginning to end.

Results:

* All 8 stages completed successfully.
* All expected outputs passed the final validation.
* The pipeline completed successfully with:

```text
PIPELINE COMPLETE
```

---

## 10. Automatic Month-Label Correction

Automatic month-label correction was added to handle incorrect month labels in the Airbnb data.

The following incorrect labels:

```text
OCT26
NOV26
DEC26
```

are automatically corrected to:

```text
OCT25
NOV25
DEC25
```

The correction is applied every time the data is loaded, so it does not require manual editing of the source data.

---

## 11. Improved Airbnb Cleaning Checks

The Airbnb cleaning stage now checks for:

* Missing prices
* Non-positive prices
* Extreme prices
* Duplicate listing-month rows

Final cleaning results:

- **35,181 listing-month observations**
- **4,099 unique listings**
- **0 missing prices**
- **0 non-positive prices**
- **0 prices above the $3,000 threshold**
- **0 duplicate listing-month rows**

---

## 12. Corrected Top 10% Reviews Logic

The review filtering logic was corrected.

The previous implementation selected values below the 90th percentile, which represented approximately the bottom 90% rather than the top 10%.

The logic was changed to select values **at or above the 90th percentile**, correctly representing approximately the top 10% of reviews.

---

## 13. Corrected Helper Function Return Order

A helper function was returning the summary and dataframe in the wrong order.

The return order was corrected so that it matches the order expected by the calling script.

---

## 14. Join Validation

Validation was added to the Airbnb and Tenancy join to ensure that Airbnb rows are preserved and that the join does not unexpectedly remove or duplicate records.

Final results:

| Check       |   Rows |
| ----------- | -----: |
| Before join | 28,281 |
| After join  | 28,281 |
| Matched     | 21,558 |
| Unmatched   |  6,723 |

This helps detect accidental row loss or duplication during the join.

---

## 15. Defensive Programming

Additional validation checks were added throughout the pipeline for:

* Required columns
* Duplicate rows
* Missing values
* Unexpected row-count changes
* Missing SA2 mappings
* Invalid API responses
* API request failures

These checks allow problems to be detected earlier during processing.

---

## 16. Reusable Intermediate Outputs

Processed datasets are saved between pipeline stages.

Later stages can reuse these outputs rather than repeating expensive processing.

This is particularly useful for the SA2 mapping stage, where existing mappings can be reused instead of making unnecessary API requests.

---

## 17. UTF-8 Output Support

The pipeline was updated to support UTF-8 terminal output more reliably.

This allows terminal output to be saved to log files without issues caused by unsupported characters.

---

## 18. Pipeline Logging

Complete pipeline runs can be saved to a log file.

Example:

```powershell
python .\data_wrangling_pipeline.py 2>&1 | Tee-Object -FilePath .\out\logs\d6_full_pipeline_test.txt
```

This provides a record of the pipeline execution and evidence that the workflow completed successfully.

---

## 19. Generated Files Excluded from Git

The following generated output directories were added to `.gitignore`:

```text
out/logs/
out/plots/
```

These files can be regenerated automatically by running the pipeline and therefore do not need to be committed to the repository.

---

## 20. Removed Hard-Coded API Key from Archived Code

An archived script containing a hard-coded Koordinates API key was sanitised.

The API key is no longer visible in the current repository version.

---

## 21. Integration with the Main Branch

The automation changes were integrated into the latest main branch.

The process included:

* Integrating the automation with the latest team code
* Resolving merge conflicts
* Testing the complete integrated pipeline
* Pushing the changes
* Merging through a pull request
* Pulling the updated changes back into `main`

---

## 22. Compatibility with Shared Project Scripts

The automated pipeline uses the existing core scripts from the group project.

The automation is therefore integrated into the existing project workflow rather than being a separate duplicate system.

---

## 23. Methodological Limitation

The current Koordinates API uses **SA2-2026** geography, while the Tenancy geography had previously been documented as **SA2-2019**.

This remains a methodological limitation of the current workflow and should be considered when interpreting the joined results.

---

## Summary

The Deliverable 6 work converted the existing individual scripts into a reproducible end-to-end pipeline.

The pipeline now:

* Runs the complete workflow with one command
* Checks required inputs automatically
* Creates required folders
* Uses centralised paths and configuration
* Reuses existing SA2 mappings
* Handles the Koordinates API key securely
* Validates intermediate and final outputs
* Saves reusable processed datasets
* Supports pipeline logging
* Detects data and processing errors earlier

Overall, the automation makes the project **more reproducible, secure, reliable, and easier to rerun**.


For Deliverable 6, the Airbnb dataset was updated to include two additional months that were not available in Deliverable 4: **July 2026 and August 2026**.

The Deliverable 4 dataset covered the period from **October 2025 to June 2026**, so July and August 2026 were previously omitted from the analysis.

| **Item** | **Deliverable 4** | **Deliverable 6** |
| ---------- | ----------------- | ----------------- |
| Study period | October 2025 – June 2026 | October 2025 – August 2026 |
| Number of Airbnb months | 9 | 11 |
| Newly added months | None | July 2026, August 2026 |
| Source | Inside Airbnb | Inside Airbnb |
| Location | Christchurch City, New Zealand | Christchurch City, New Zealand |

The two newly added Airbnb source files were:

- `JLY26_listings.csv`
- `AUG26_listings.csv`

These files were incorporated into the existing Airbnb processing pipeline so that they underwent the same cleaning and processing procedures as the previously used monthly datasets.

### Previously Omitted Data

The July and August 2026 Airbnb observations were omitted from Deliverable 4 because the study period ended in June 2026.

Deliverable 6 extends the Airbnb study period to **August 2026**, allowing more recent Airbnb activity in Christchurch to be included in the analysis.

### Month Label Correction

The July 2026 Airbnb dataset used the month label `JLY26`. This did not match the standard month format used by the processing code.

The processing pipeline was therefore updated to convert:

`JLY26` → `JUL26`

This allowed July 2026 to be interpreted correctly during date conversion and subsequent analysis.

### Updated Airbnb Dataset

After incorporating the additional months and processing the complete dataset, the updated Airbnb dataset contains:

- **35,181 listing-month observations**
- **7 variables**
- **Study period:** October 2025 – August 2026

The variables retained are:

| **Column** | **Meaning** |
| ---------- | ----------- |
| `id` | Unique Airbnb listing identifier |
| `neighbourhood` | Christchurch neighbourhood or ward |
| `latitude` | Latitude of the Airbnb listing |
| `longitude` | Longitude of the Airbnb listing |
| `price` | Nightly Airbnb listing price |
| `month_year` | Month and year associated with the monthly dataset |
| `room_type` | Type of Airbnb accommodation |

### Tenancy Services Coverage

The Tenancy Services dataset used in the project does not contain a corresponding Q3 2026 quarter. The available tenancy data covers the quarters through **April–June 2026 (Q2 2026)**.

Therefore:

- July 2026 Airbnb observations do not have a corresponding Tenancy Services quarter.
- August 2026 Airbnb observations do not have a corresponding Tenancy Services quarter.
- Direct Airbnb-to-Tenancy comparisons remain limited to quarters where both datasets are available.

### 

The addition of July and August 2026 means that the Airbnb time series now contains two months that were previously omitted.

------------------------------------------------------------------------------------------

For Deliverable 4, we use the combined Christchurch Airbnb dataset created in
Deliverable 3.

- **Source:** Inside Airbnb
- **Website:** [https://insideairbnb.com/get-the-data/]
- **Dataset:** `chch_airbnb_oct25_jun26.csv`
- **Location:** Christchurch City, New Zealand
- **Study period:** October 2025 to June 2026
- **Format:** CSV
- **Number of observations before cleaning:** 28,795
- **Number of variables before cleaning:** 19

The dataset contains monthly Airbnb listing information for Christchurch,
including listing identifiers, neighbourhoods, geographic coordinates, room
types, prices, availability, and review information.


## Cleaning Airbnb Data

For Deliverable 4, the combined Christchurch Airbnb dataset was cleaned and
reduced to the variables required for the later rental-market analysis.

The following columns were retained:

| Column | Meaning |
| --- | --- |
| `id` | Unique Airbnb listing identifier |
| `neighbourhood` | Christchurch neighbourhood or ward |
| `latitude` | Latitude of the Airbnb listing |
| `longitude` | Longitude of the Airbnb listing |
| `price` | Nightly Airbnb listing price |
| `month_year` | Month and year associated with the monthly dataset |
| `room_type` | Type of Airbnb accommodation |

Latitude and longitude were retained so listings could still be geographically
identified and used in later spatial or location-based analysis.


### Duplicates

Because the dataset contains repeated observations of Airbnb listings across
different months, listing `id` alone cannot be used to identify duplicates.

Duplicates were therefore checked using the combination:

`id + month_year`

This identifies whether the same listing appears more than once within the same
monthly dataset.

No duplicate listing-month combinations were found.


### Missing Price Values

Before cleaning, the `price` column contained 10,667 missing values.

Properties were first grouped by listing `id` to identify listings where price
was missing for every observed month.

A total of 163 properties had no observed price in any month. These properties
were removed because there was no observed price information available that
could be used to estimate their missing values.

This removed 497 rows from the dataset, reducing the Airbnb dataset from 28,795
to 28,298 rows.

For the remaining listings, missing prices were imputed using the mean observed
price for the same property across the other available months.

This approach retains listings that contain some valid price information while
avoiding the use of an overall dataset-wide mean that would ignore differences
between individual properties.

After imputation, there were no remaining missing values in the `price` column.

A limitation of this approach is that an imputed value represents an estimate
rather than an observed nightly price. It may therefore reduce real month-to-month
price variation for listings with missing observations. (e.g. prices may change over the course of the year due to seasonal demand, or newer properties are often priced very cheaply for the first few months they are listed).


### Outliers Checks

Airbnb nightly prices were inspected for possible outliers using summary
statistics, quantiles, the highest-price observations, threshold counts, and a
boxplot.

The cleaned Airbnb price data had:

- Median nightly price: `$206`
- 90th percentile: `$401`
- 95th percentile: `$505`
- 99th percentile: `$925.75`
- Maximum nightly price: `$43,654`

There were:

- 219 observations above `$1,000`
- 38 observations above `$2,000`
- 16 observations above `$5,000`
- 9 observations above `$10,000`

The highest prices were inspected together with listing ID, month, room type,
neighbourhood, latitude, and longitude.

Prices above $3000 are likely to be errors in the data. A manual check of those properties revealed that they were not on Airbnb, had a different listed price, or the property description did not match the price (e.g. a cottage wouldn't cost $20 000 per night).
Each listing with a price exceeding $3000 was checked to see if it had other months where the price was less and was replaced with the mean of those, otherwise it was removed from the dataset.

Additional sanity checks found:

- 0 non-positive price values
- 0 missing latitude values
- 0 missing longitude values

The extreme values were therefore retained in the cleaned dataset, but should
be considered when interpreting Airbnb price summaries and visualisations.


### Cleaned Airbnb Dataset

The final cleaned Airbnb dataset contains:

- **27,266 rows**
- **7 variables**

The cleaned dataset is saved locally as:

`Data/airbnb_cleaned_oct25_jun26.csv`

The cleaned dataset will be used in later analysis to compare short-term Airbnb
prices with long-term rental-market information from the Tenancy Services data.


### Airbnb Month Label Correction

During Deliverable 4, a month-label inconsistency inherited from Deliverable 3 was identified.

The combined Airbnb dataset contained the labels `OCT26`, `NOV26`, and `DEC26`, even though the intended study period is October 2025 to June 2026.

The Deliverable 3 processing code created the `month_year` value from the monthly dataset filename. The first three files had been labelled with `26`, causing those incorrect labels to be carried into the combined dataset.

The following corrections were therefore applied reproducibly in the Deliverable 4 code:

- `OCT26` → `OCT25`
- `NOV26` → `NOV25`
- `DEC26` → `DEC25`

This correction only changed the month-year labels. It did not alter prices, listing IDs, geographic information, or the number of observations.

The corrected study period is therefore October 2025 to June 2026.

An additional limitation was identified in the monthly price data. Before imputation, December 2025, January 2026, and February 2026 had 100% missing values in the `price` column.

As a result, all price values for these three months after cleaning are imputed estimates based on each listing's observed prices in other available months rather than directly observed monthly prices.

This should be considered when interpreting changes in Airbnb prices over time, because the imputation may reduce genuine seasonal or month-to-month variation.

## Dataset Source - Tenancy Services

For Deliverable 4, we use the `Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv` dataset provided by TenancyServices website.

- **Source:** TenancyServices website
- **Website:** [https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/]
- **Dataset:** `Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv`
- **Location:** New Zealand
- **Date:** September 2026
- **Format:** CSV
- **Number of observations:** 226080
- **Number of variables:** 12

The dataset contains quarterly summary information about rental bonds across New Zealand, including rental prices, bond activity, dwelling types, bedroom numbers, and geographical locations.

## Dataset Columns

| Column | Meaning |
|---|---|
| `TimeFrame` | Time period that the rental bond data relates to |
| `Location Id` | Identifier for the SA2-2019 geographical area |
| `Dwelling Type` | Type of dwelling associated with the rental bond |
| `Number Of Beds` | Number of bedrooms in the dwelling |
| `Total Bonds` | Total number of rental bonds recorded |
| `Active Bonds` | Number of active rental bonds |
| `Closed Bonds` | Number of rental bonds that have been closed |
| `Median Rent` | Median weekly rent |
| `Geometric Mean Rent` | Geometric mean of weekly rent |
| `Upper Quartile Rent` | Synthetic upper quartile (75th percentile) of weekly rent |
| `Lower Quartile Rent` | Synthetic lower quartile (25th percentile) of weekly rent |
| `Log Std Dev Weekly Rent` | Standard deviation of weekly rent on a logarithmic scale |

## Data Notes

- Geometric mean (replacing median): Calculated by multiplying the values together and taking the nth root. When rent is log-normally distributed, it closely approximates the median.
- Synthetic quartiles (replacing quartiles): Estimate the 25th percentile (lower quartile) and 75th percentile (upper quartile), assuming rent is log-normally distributed. The mean and variance are calculated from the data rather than assumed.
- The type of dwelling, with `ALL` representing all dwelling types combined.
- `NULL` values indicate missing information for that field.

### Duplicates
Total rows: 226,080
Duplicate rows: 0

### Cleaning Tenancy Data

The detailed quarterly Tenancy Services dataset was filtered to match the
Airbnb study period of October 2025 to June 2026.

The quarterly `TimeFrame` values retained were:

- `2025-10-01` — October to December 2025
- `2026-01-01` — January to March 2026
- `2026-04-01` — April to June 2026

The original dataset contained 226,080 rows. After filtering the timeframe,
27,212 rows remained.

#### Missing Location Id

94 rows had a missing `Location Id`. These records were removed because
they could not be geographically linked in the intended analysis. These
rows also had missing rent-summary values.

This reduced the dataset from 27,212 to 27,118 rows.

#### Special Location Id Records

127 rows had `Location Id = -99`.

Because `-99` is a special non-standard location identifier rather than an ordinary geographic Location Id, these rows were excluded from the location-level dataset so that special records would not be mixed with ordinary geographic observations.

This reduced the dataset from 27,118 to 26,991 rows.

#### Number Of Beds

858 remaining records had no value for `Number Of Beds`.

These rows were retained because they still contained useful location,
rent and bond information. Missing bedroom values were labelled `Unknown`
rather than imputing a bedroom count.

The existing `ALL` category was retained because it represents an aggregate
category in the source data rather than a missing value.

#### Duplicates

Duplicates were checked using the combination:

`TimeFrame + Location Id + Dwelling Type + Number Of Beds`

No duplicate key combinations were found.

#### Sanity checks and outliers of Tenancy Data

Bond count variables were checked for negative values and none were found.

Rent variables were checked for non-positive values and none were found.

The logical ordering

`Lower Quartile Rent <= Median Rent <= Upper Quartile Rent`

was also checked, and no violations were found.

Median weekly rent ranged from $90 to $3350.

Extreme rent values were inspected but were retained because there was
insufficient evidence that they were data errors. No arbitrary outlier
threshold was applied.

The final cleaned Tenancy dataset contains 26,991 rows and 12 columns.

# Deliverable 5 – SA2 Mapping, Data Integration and Christchurch Central Median

## 1. Objective

This section prepares the Airbnb and Tenancy datasets for integration by assigning Statistical Area 2 (SA2) codes to Airbnb listings and joining the datasets using location and time. It also calculates the median Airbnb nightly price in Christchurch Central (Location ID 326600).

The analysis covers October 2025 to June 2026.

## 2. SA2 Mapping

The cleaned Airbnb dataset contains **28,298 observations**, representing **3,796 unique latitude/longitude pairs**.

The Koordinates Query API was initially tested on a single Airbnb coordinate before processing the unique coordinates using the SA2-2026 layer (Layer ID 123515). The mapping results were saved as a checkpoint to avoid repeating completed queries.

All 3,796 coordinates were successfully mapped, with no duplicate coordinates or missing SA2 codes.

The SA2-2026 codes were added to the Airbnb dataset and saved as `Data/airbnb_with_sa2.csv`. The merge preserved all 28,298 original observations.

### Aligning the geographic areas

A comparison with the Tenancy dataset identified differences in SA2 code coverage. An SA2-2019 shapefile was therefore used to generate a second mapping based on the Airbnb coordinates.

The shapefile was loaded using GeoPandas. Airbnb coordinates were converted from EPSG:4326 to EPSG:2193 before a point-in-polygon spatial join.

The SA2-2019 mapping produced:

| Validation             | Result |
| ---------------------- | -----: |
| Unique coordinates     |  3,796 |
| Duplicate coordinates  |      0 |
| Missing SA2-2019 codes |      0 |

The mapping was saved as `Data/sa2_2019_mapping.csv`.

SA2-2019 codes and area names were subsequently added to the Airbnb dataset and saved as `Data/airbnb_with_sa2_2019.csv`.

Both geographic versions were retained for comparison.

## 3. Joining Airbnb and Tenancy

Airbnb's monthly observations were assigned to the corresponding quarterly Tenancy reference dates:

| Airbnb months         | Quarter    |
| --------------------- | ---------- |
| October–December 2025 | 2025-10-01 |
| January–March 2026    | 2026-01-01 |
| April–June 2026       | 2026-04-01 |

The Tenancy dataset was filtered to records where both `Dwelling Type` and `Number Of Beds` were `ALL`, selecting overall rental summaries rather than individual dwelling and bedroom categories.

This produced **4,865 Tenancy records**, with no duplicate area-quarter combinations.

A left join was performed using:

* Airbnb `sa2_2019_code` = Tenancy `Location Id`
* Airbnb `quarter` = Tenancy `TimeFrame`

The join used `validate="many_to_one"` to prevent the Tenancy dataset from duplicating Airbnb observations.

### Join validation

| Result                 | Observations |
| ---------------------- | -----------: |
| Original Airbnb rows   |       28,298 |
| Rows after joining     |       28,298 |
| Successfully matched   |       24,107 |
| Unmatched and retained |        4,191 |

All original Airbnb observations were preserved. Unmatched records have missing Tenancy values.

The combined dataset was saved as:

`Data/airbnb_tenancy_joined.csv`

## 4. Christchurch Central Median Airbnb Price

Airbnb records were filtered using Christchurch Central's SA2 code, `326600`.

| Measurement                 |        Result |
| --------------------------- | ------------: |
| Listing-month observations  |         1,105 |
| Unique Airbnb listings      |           152 |
| Median Airbnb nightly price | **NZ$237.83** |

The median was calculated across listing-month observations covering October 2025 to June 2026.

The Christchurch Central median was also checked using the SA2-2019 mapping and produced the same result.

## 5. Limitations

* Airbnb prices for December 2025, January 2026 and February 2026 were imputed during Deliverable 4. The calculated median therefore includes estimated prices.
* The SA2-2019 shapefile uses generalised boundaries, which may introduce geographic assignment inaccuracies near area boundaries.
* The left join retained 4,191 Airbnb observations without matching Tenancy records. These observations should be handled appropriately in subsequent analyses.
* Airbnb prices are expressed per night, whereas Tenancy median rents are expressed per week. Weekly rents must be divided by seven for a basic daily-rate comparison; this does not account for differences in occupancy, property type or rental arrangements.

## 6. Scripts and Data Availability

The Python scripts are organised in the `Deliverable 5/` folder.

| Script                 | Purpose                                                    |
| ---------------------- | ---------------------------------------------------------- |
| `D5_test_api.py`       | Tests a single Koordinates API query                       |
| `D5_mapping.py`        | Queries and saves SA2-2026 mapping results                 |
| `D5_add_sa2.py`        | Adds SA2-2026 codes to Airbnb                              |
| `D5_sa2_2019.py`       | Maps Airbnb coordinates using the SA2-2019 shapefile       |
| `D5_add_sa2_2019.py`   | Adds SA2-2019 codes to Airbnb                              |
| `D5_final_join.py`     | Joins Airbnb and Tenancy using SA2-2019 codes and quarters |
| `D5_central_median.py` | Calculates the Christchurch Central median Airbnb price    |

Scripts should be executed from the project root because their data paths are relative to that directory.

**Data availability:** The `Data/` folder is excluded by `.gitignore`. Generated datasets, including `airbnb_tenancy_joined.csv`, are not automatically shared through GitHub and must be provided separately to team members who need them.

The API scripts obtain the Koordinates API key through the `KOORDINATES_API_KEY` environment variable. API keys should not be committed to the repository.



## Deliverable 6 – Pipeline Design Principles

### Design Principles Task

For Deliverable 6, we reviewed the reorganised `clean_tidy` pipeline and documented its design principles.

The purpose of this review was to describe:

1. the inputs to the pipeline,
2. the outputs produced by the pipeline,
3. the main processing stages, and
4. the coding and software strategies used throughout the project.

The document was checked against the actual implementation in the `clean_tidy` branch so that the documentation reflects what the code currently does.

---

### 1. Pipeline Inputs

The pipeline uses two main data sources.

#### Airbnb data

Monthly Airbnb listing CSV files are stored in:

`Data/raw/`

These files contain variables such as:

- listing ID,
- latitude and longitude,
- nightly price,
- room type,
- neighbourhood,
- observation month,
- and review-related information.

#### Tenancy data

The raw Tenancy Services quarterly dataset is:

`Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv`

It contains long-term rental information such as:

- Location ID,
- dwelling type,
- number of bedrooms,
- median weekly rent,
- Active Bonds,
- Total Bonds,
- and other rental statistics.

#### Geographic information

The pipeline also uses the Koordinates Query API to obtain Statistical Area 2 (SA2) codes and area names from Airbnb latitude and longitude coordinates.

The current implementation queries Koordinates layer `123515`, which provides SA2-2026 geographic areas.

---

### 2. Pipeline Outputs

Processed datasets are stored in:

`Data/processed/`

Important outputs include:

- `chch_airbnb_oct25_jun26.csv`
- `airbnb_cleaned_oct25_jun26.csv`
- `tenancy_cleaned_oct25_jun26.csv`
- `airbnb_with_sa2.csv`
- `airbnb_tenancy_joined.csv`
- `listing_quarter_gaps.csv`
- `area_quarter_gaps.csv`
- `area_gap_summary.csv`
- `sensitivity.csv`
- `airbnb_vs_rental_comparison_final.csv`

Visual outputs are stored separately in:

`out/plots/`

Examples include:

- Airbnb price histograms,
- Airbnb review histograms,
- price-gap distributions,
- and Airbnb versus Active Rental Bonds comparison charts.

---

### 3. Main Pipeline Steps

The complete workflow is controlled by:

`data_wrangling_pipeline.py`

The pipeline runs eight main stages in sequence.

#### Step 1 – Load and combine Airbnb files

`load_concat_airbnb.py`

Loads the monthly raw Airbnb CSV files, combines them, filters the data to Christchurch, and produces the combined Christchurch Airbnb dataset.

#### Step 2 – Airbnb summary statistics and plots

`chch_airbnb_stats.py`

Produces exploratory summary statistics and visualisations for the combined Airbnb dataset.

#### Step 3 – Clean Airbnb data

`clean_airbnb.py`

Keeps the variables required for later analysis, handles missing prices, deals with extreme price values, and produces the cleaned Airbnb dataset.

#### Step 4 – Clean Tenancy data

`load_clean_tenancy.py`

Loads and cleans the quarterly Tenancy Services dataset and restricts it to the study period.

#### Step 5 – Add SA2 geographic information

`API_SA2query_airbnb_locations.py`

Uses Airbnb latitude and longitude coordinates to query the Koordinates API and assign SA2 area codes and names.

The script also checks whether a complete SA2 output already exists so that thousands of API requests do not need to be repeated unnecessarily.

#### Step 6 – Join Airbnb and Tenancy datasets

`join_airbnb_tenancy.py`

Converts Airbnb monthly observations into calendar quarters and joins Airbnb with the Tenancy dataset using SA2 area code and quarter.

A left join is used so that all Airbnb observations are retained.

The join is validated using `validate="many_to_one"` and row-count checks.

#### Step 7 – Analyse rental price gaps

`price_gap.py`

Calculates Airbnb listing-quarter median nightly prices and compares them with the nightly equivalent of Tenancy median weekly rents.

The analysis also performs sensitivity checks using different minimum listing, bond, and quarter requirements.

#### Step 8 – Compare Airbnb listings and rental activity

`compare_airbnb_tenancy.py`

Counts unique Airbnb listings by SA2 area and compares them with the maximum recorded Active Bonds value for each location.

The results are saved as a comparison table and visualised using a bar chart.

---

### 4. Coding and Software Strategies

Several coding practices were adopted to improve the structure, readability and reproducibility of the project.

#### Modular code structure

Each major processing task is stored in a separate Python script with a `main()` function.

This separates different responsibilities such as loading, cleaning, joining and analysis.

#### Single pipeline entry point

`data_wrangling_pipeline.py` runs the major scripts in the required order.

This makes the workflow easier to reproduce because the user does not need to manually remember the execution order of every script.

#### Centralised path management

The project uses `paths.py` to construct paths through reusable functions such as:

- `data_path()`
- `code_path()`
- `out_path()`

This reduces repeated path code and avoids machine-specific absolute paths.

#### Separation of raw and processed data

Original input data and generated processed data are stored separately.

This makes it easier to distinguish source data from files produced by the pipeline.

#### Descriptive file naming

Scripts are named according to their purpose, for example:

- `clean_airbnb.py`
- `join_airbnb_tenancy.py`
- `price_gap.py`

rather than only being identified by assignment deliverable numbers.

#### Validation and defensive programming

Several pipeline stages perform explicit checks before continuing.

Examples include:

- checking required columns,
- detecting duplicate observations,
- validating expected quarters,
- checking prices,
- checking unique join keys,
- checking missing SA2 values,
- comparing row counts before and after joins,
- and using `validate="many_to_one"` during merges.

These checks help detect data-processing errors before they affect later analysis.

#### Reusable intermediate outputs

Important processed datasets are saved between stages.

This allows later stages to reuse existing results instead of repeating expensive operations such as API queries.

#### Parameterisation and sensitivity analysis

The price-gap analysis allows parameters such as minimum listings, minimum bonds and qualifying quarters to be changed.

Several sensitivity scenarios are run to test whether the conclusions depend strongly on particular analytical assumptions.

---

### AI Use

This Design Principles document was drafted with assistance from **ChatGPT by OpenAI (GPT-5.6 Sol)**.

The generated content was reviewed against the actual project code in the `clean_tidy` branch. The project team is responsible for checking and revising the document so that it accurately reflects the final implementation and intended workflow.
