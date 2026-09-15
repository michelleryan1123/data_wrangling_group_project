 # DATA201/422 Group Project

Repository for our DATA201/422 Christchurch Rental Market group project.

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

#### Sanity checks and outliers

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

