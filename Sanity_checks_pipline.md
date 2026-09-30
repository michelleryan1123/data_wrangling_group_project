# Sanity Check Approach

sanity checks were performed in the pipeline by comparing the intended behaviour of
each pipeline step with its actual output.

1. **Identify Key Pipeline Steps**
   - Identify steps where errors or unexpected outputs could affect
     subsequent analysis.

2. **Define Expected Outcomes**
   - Determine what the output of each step should look like based on the
     the intended purpose of the code and the expected output of the CSV data based on the requirements of the relevant deliverable.

3. **Compare Inputs and Outputs**
   - Use AI to assist in comparing the data before and after each transformation to identify unexpected changes/incorrect outputs.

4. **Check Data Integrity**
   - Check for missing values.
   - Check for duplicate records.
   - Check for unexpected changes in the number of observations.
   - Check for unexpected or extreme values.

5. **Manually Inspect Results**
   - Inspect a sample of records to confirm that transformations have produced logically consistent results.

6. **Investigate Discrepancies**
   - Investigate differences between the expected and actual outputs and correct the code where necessary.

7. **Re-run the Pipeline**
   - Re-run the affected pipeline step after corrections to confirm that the intended result has been achieved.

## Example of a Discrepancy Identified and Corrected

During the sanity check of the Airbnb cleaning step (clean_airbnb.py), the output was reviewed
to determine whether it was consistent with the intended behaviour of the
code.

The pipeline was initially developed with the assistance of AI, and the
generated code incorrectly assumed that the calculated mean price should
replace all price values for each Airbnb ID, rather than only the missing
values.

The intended behaviour was to preserve existing observed prices and use the
mean only to replace missing prices.

The discrepancy was identified by comparing the expected behaviour of the
transformation with its actual output. The code was corrected to use
`fillna()`, ensuring that existing prices remain unchanged and only missing
values are imputed.

The affected pipeline step was then re-run to verify that the corrected
logic produced the intended result.

## corrected code
mean_price_per_id = airbnb_cleaned.groupby("id")["price"].mean()airbnb_cleaned["price"] = airbnb_cleaned["id"].map(mean_price_per_id)

corrected to

mean_price_per_id = airbnb_cleaned.groupby("id")["price"].mean()airbnb_cleaned["price"] = airbnb_cleaned["price"].fillna(airbnb_cleaned["id"].map(mean_price_per_id))
## Sanity Check Status

All pipeline functions were run locally as an initial sanity check for
errors and unexpected outputs.

















