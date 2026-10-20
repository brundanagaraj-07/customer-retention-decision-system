import pandas as pd
from sqlalchemy import create_engine
import sys

# -----------------------------------------------------------------------------
# Configuration Settings
# -----------------------------------------------------------------------------
DB_USER = "root"          # Your MySQL username
DB_PASSWORD = "" # Your actual MySQL password (handles special characters safely)
DB_HOST = "localhost"     # Usually localhost
DB_PORT = "3306"          # Default MySQL port
DB_NAME = "revguard_db"   # Target database name

def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine for connecting to MySQL.
    Uses connect_args to safely handle passwords containing special characters like '@'.
    """
    connection_uri = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        engine = create_engine(
            connection_uri,
            connect_args={"password": DB_PASSWORD}
        )
        return engine
    except Exception as e:
        print(f"❌ Error creating database engine: {e}")
        sys.exit(1)

def load_analytics_views():
    """
    Loads all core analytics views from MySQL into Pandas DataFrames.
    Returns a dictionary containing the dataframes.
    """
    engine = get_db_engine()
    
    print("🔌 Connecting to MySQL database 'revguard_db'...")
    
    queries = {
        "rfm": "SELECT * FROM vw_customer_rfm",
        "value_friction": "SELECT * FROM vw_customer_value_friction",
        "cohort_revenue": "SELECT * FROM vw_cohort_monthly_revenue"
    }
    
    dataframes = {}
    
    try:
        with engine.connect() as conn:
            for key, query in queries.items():
                print(f"📥 Loading view '{key}'...")
                dataframes[key] = pd.read_sql(query, con=conn)
                print(f"   ✓ Success! Loaded {len(dataframes[key])} rows and {len(dataframes[key].columns)} columns.")
                
        print("\n✅ All analytics views successfully loaded into memory!")
        return dataframes

    except Exception as e:
        print(f"❌ Error querying views from MySQL: {e}")
        print("💡 Hint: Ensure PyMySQL is installed (`pip install pymysql`) and check your password.")
        return None

if __name__ == "__main__":
    # Test script execution
    dfs = load_analytics_views()
    
    if dfs:
        print("\n--- Quick Data Inspection ---")
        print("\n1. RFM View Preview:")
        print(dfs["rfm"].head(3))
        
        print("\n2. Value Friction View Preview:")
        print(dfs["value_friction"].head(3))
        
        print("\n3. Cohort Monthly Revenue Preview:")
        print(dfs["cohort_revenue"].head(3))
