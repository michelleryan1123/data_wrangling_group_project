 # DATA201/422 Group Project

Repository for our DATA201/422 Christchurch Rental Market group project.

## Dataset Source

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
