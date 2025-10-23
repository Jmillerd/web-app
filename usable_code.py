# ================= SIMPLE PYTHON WORKSHEET TEMPLATE =================
# Read and explore an existing Snowflake table (no object creation)

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# ---- EDIT THESE ----
DB        = "PROD"
SCHEMA    = "SALES"
TABLE     = "ORDERS"     # full path: PROD.SALES.ORDERS
ROW_LIMIT = 20           # rows to preview

def main(session: Session):
    # Set context
    session.sql(f"USE DATABASE {DB}").collect()
    session.sql(f"USE SCHEMA {SCHEMA}").collect()

    # Load the table
    df = session.table(f"{DB}.{SCHEMA}.{TABLE}")

    # Example filter (optional)
    df_filtered = df.filter(col("TOTAL_AMOUNT") > 0)

    # Show preview
    df_filtered.limit(ROW_LIMIT).show()

    # Return Snowpark DataFrame (renders as grid)
    return df_filtered.limit(ROW_LIMIT)
