# =================================
# DATA422 Group Project - SIMPLE PIPELINE
# =================================

from Code.load_concat_airbnb import main as load_airbnb
from Code.chch_airbnb_stats import main as airbnb_stats
from Code.clean_airbnb import main as clean_airbnb
from Code.load_clean_tenancy import main as clean_tenancy
from Code.API_SA2query_airbnb_locations import main as query_sa2
from Code.join_airbnb_tenancy import main as join_airbnb_tenancy
from Code.price_gap import main as price_gap
from Code.compare_airbnb_tenancy import main as compare_airbnb_tenancy


def run_pipeline():
    print("\nSTEP 1: Load + combine Airbnb raw files")
    load_airbnb()

    print("\nSTEP 2: Airbnb summary statistics + plots")
    airbnb_stats()

    print("\nSTEP 3: Clean Airbnb dataset")
    clean_airbnb()

    print("\nSTEP 4: Clean tenancy dataset")
    clean_tenancy()

    print("\nSTEP 5: SA2 lookup")
    query_sa2()

    print("\nSTEP 6: Join Airbnb and tenancy datasets and check CHCH central")
    join_airbnb_tenancy()

    print("\nSTEP 7: Biggest price gaps between Airbnb and rental bonds")
    price_gap()

    print("\nSTEP 8: Compare Airbnb listings vs active rental bonds")
    compare_airbnb_tenancy()

    print("\nPIPELINE COMPLETE")

if __name__ == "__main__":
    run_pipeline()
