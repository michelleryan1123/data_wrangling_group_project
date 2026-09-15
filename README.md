 # DATA201/422 Group Project

Repository for our DATA201/422 Christchurch Rental Market group project.

## Dataset Source - Airbnb

For Deliverable 4, we use the combined Christchurch Airbnb dataset created in
Deliverable 3.

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
price variation for listings with missing observations.


### Outliers and Sanity Checks

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

Although some prices were extremely high compared with the majority of
listings, they were not automatically removed. An extreme value does not
necessarily indicate a data error, and there was insufficient evidence to
classify these observations as invalid.

Additional sanity checks found:

- 0 non-positive price values
- 0 missing latitude values
- 0 missing longitude values

The extreme values were therefore retained in the cleaned dataset, but should
be considered when interpreting Airbnb price summaries and visualisations.


### Final Cleaned Airbnb Dataset

The final cleaned Airbnb dataset contains:

- **28,298 rows**
- **7 variables**

The cleaned dataset is saved locally as:

`Data/airbnb_cleaned_oct25_jun26.csv`

The cleaned dataset will be used in later analysis to compare short-term Airbnb
prices with long-term rental-market information from the Tenancy Services data.


### Airbnb Data Limitation to Verify

The current combined dataset contains the `month_year` labels `OCT26`, `NOV26`,
and `DEC26`, even though the intended study period begins in October 2025.

These labels appear inconsistent with the intended October 2025 to June 2026
study period and should be checked against the original Deliverable 3 monthly
files before the final analysis. If confirmed as a labelling error, the labels
should be corrected reproducibly in the data-processing code rather than by
manually editing the CSV.

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

#### Aggregate location records

127 rows had `Location Id = -99`, representing aggregate location records
rather than individual geographic areas.

These rows were removed so aggregate values would not be mixed with
location-level observations in later analysis.

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

