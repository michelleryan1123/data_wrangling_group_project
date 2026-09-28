# DATA201 D5 price-gap audit — supplied file labelled SA2-2019

**Conditional finding:** confirm the mapping's provenance as Stats NZ SA2-2019 and reconcile D4 Airbnb cleaning before calling this final.

Method: convert Tenancy ALL/ALL median weekly rent to nightly by dividing by 7; take one median asking price for each Airbnb listing-quarter; take median of listing gaps per area-quarter; take median of qualifying area-quarter gaps per area. Filters: >=5 listings/area-quarter, >=5 bonds and >=2 qualifying quarters. These thresholds are analyst choices.

Input listing-months: 28,298; excluded ambiguous listing IDs: 37 (244 listing-month rows). Remaining listing-quarters: 10,000; matched to bonds: 8,537; unmatched: 1,463; eligible areas: 115.

Largest typical gap with the stated rules: **Wigram South** (SA2-2019 323600), **NZ$263.36/night**, based on 10 listing-quarter records in 2 qualifying quarters. This is a descriptive gap, not nightly income or profit.

Cautions: D4 cleaned Airbnb file supplied still has prices above NZ$3,000 and differs from README row count; Dec 2025–Feb 2026 were entirely imputed; SA2 mapping provenance/shapefile not independently supplied; some properties shift mapped SA2 over months; geographic coverage incomplete after bond matching; bond data are provisional, privately lodged bonds, not all Christchurch properties.

## Sensitivity

                                         scenario   leading_area area_code  gap_nzd_night  qualifying_quarters  listing_quarters  qualifying_areas
                                          primary   Wigram South    323600         263.36                    2                10               115
          exclude only ambiguous listing-quarters   Wigram South    323600         263.36                    2                10               115
                 at least 10 listings per quarter        Malvern    322100         227.22                    3                46                76
                    at least 20 bonds per quarter        Malvern    322100         227.22                    3                46                65
                               all three quarters        Malvern    322100         227.22                    3                46               101
                                entire homes only Sockburn North    321000         289.22                    2                13                89
 exclude Dec 25 / Jan-Feb 26 fully imputed months   Wigram South    323600         291.86                    2                10               113
exclude nightly prices above $3,000 (sensitivity)   Wigram South    323600         263.36                    2                10               115
                 at least 20 listings per quarter         Sumner    332700         203.96                    3               199                32
