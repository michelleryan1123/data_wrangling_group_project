 # DATA201/422 Group Project

Repository for our DATA201/422 Christchurch Rental Market group project.

## Dataset Source - AirBNB

For Deliverable 2, we use the `listings.csv` dataset provided by Inside Airbnb.

- **Source:** Inside Airbnb
- **Website:** https://insideairbnb.com/get-the-data/
- **Dataset:** `listings.csv`
- **Location:** New Zealand
- **Date:** June 2026
- **Format:** CSV
- **Number of observations:** 50,932 listings
- **Number of variables:** 18

The dataset contains summary information about Airbnb listings across New Zealand.

## Dataset Columns

| Column | Meaning |
|---|---|
| `id` | Unique identifier for each Airbnb listing |
| `name` | Name or title of the Airbnb listing |
| `host_id` | Unique identifier for the host |
| `host_name` | Name of the host |
| `neighbourhood_group` | Larger geographic area containing the listing |
| `neighbourhood` | Local area or neighbourhood of the listing |
| `latitude` | Latitude coordinate of the listing |
| `longitude` | Longitude coordinate of the listing |
| `room_type` | Type of accommodation, such as entire home, private room, shared room, or hotel room |
| `price` | Nightly price of the listing in NZD |
| `minimum_nights` | Minimum number of nights required for a booking |
| `number_of_reviews` | Total number of reviews received by the listing |
| `last_review` | Date of the most recent review |
| `reviews_per_month` | Average number of reviews received per month |
| `calculated_host_listings_count` | Number of listings belonging to the same host |
| `availability_365` | Number of days the listing is shown as available during the next 365 days |
| `number_of_reviews_ltm` | Number of reviews received in the last 12 months |
| `license` | Licence or registration information, if available |

## Data Notes

- Some listings have missing values for `last_review` and `reviews_per_month`.
- Some values of `price` are missing.
- The `license` column contains no values in the downloaded dataset.
- `availability_365` does not necessarily mean that the property was unbooked. A host may also manually block dates.

## Cleaning Airbnb Data
- initial dataset has 28795 entries and 19 columns
- keep only the following columns: `'id', 'neighbourhood', 'latitude', 'longitude', 'price', 'month_year', 'room_type'`
    `id` - property id
    `neighbourhood` - local area
    `latitude, longitude` - property location
    `price` per night ($)
    `month_year` Oct 25 - April 26
    `room_type` - room, whole house etc
    - kept these ones, rather than dropping others as 
        1. most of the other columns were not relevant for future analysis
        2. means that if new columns were added to the dataset that they wouldn't need to be cleaned in order for the dataset to work properly
        3. fewer columns to clean - reduces any risk of records being ignored during analysis if not cleaned properly and in some cases it would be difficult/impossible to resolve missing values without possibly introducing bias that doesn't need to exist

### Duplicates
As the dataset spans multiple months and each property can appear in each month we created a key based on property 'id' and 'month_year' to check for duplicates
- 0 duplicates found

### Missing values
'price' had 10667 missing values (37% of the total number of rows) so need to impute them

- 1. Check if there are any properties with no prices
    (assume that no price means that property was not available to rent)

    163 (0.57%) properties had no prices listed for all months - these were removed

- 2. Check percentage of missing prices per month
     - replace the missing values in those months with the `mean` price for that property for the months where it has a price

|APR26  |    5.39 |
|DEC25  |  100.00 |
|FEB26  |  100.00|
|JAN26  |  100.00|
|JUN26  |   5.95 |
|MAR26  |    4.32|
|MAY26  |    5.63|
|NOV25  |    4.93|
|OCT25  |    3.26|

This resolves the remaining missing prices
### Outliers



## Dataset - Tenancy bonds


