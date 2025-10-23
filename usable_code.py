# ================= READ-ONLY EXPLORATION TEMPLATE (Snowpark + optional pandas) =================
# What it does (all without creating any objects):
# - sets context
# - previews rows
# - samples deterministically
# - selects & computes columns
# - filters & aggregates
# - (optional) converts a small result to pandas
# Return value is a Snowpark DF so the worksheet shows a grid.

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, to_date, coalesce, when, lit, sum as ssum, count as scount

# ---- EDIT THESE ----
DB        = "PROD"
SCHEMA    = "SALES"
TABLE     = "ORDERS"         # fully qualifies to PROD.SALES.ORDERS
WAREHOUSE = None             # e.g., "BI_WH" or None to skip
ROLE      = None             # e.g., "ANALYST" or None to skip

ROW_PREVIEW = 20             # rows to preview in the grid
SAMPLE_FRAC = 0.02           # 2% sample for quick EDA
SAMPLE_SEED = 42             # seed for reproducible sampling
PANDAS_OUT  = False          # set True to also return a small pandas df

# ---- OPTIONAL FILTER PARAMS (adjust/remove as needed) ----
DATE_COL         = "ORDER_DATE"
DATE_START       = "2024-01-01"
MIN_TOTAL_AMOUNT = 0

def main(session: Session):
    # Context (read-only)
    if ROLE:      session.sql(f"USE ROLE {ROLE}").collect()
    if WAREHOUSE: session.sql(f"USE WAREHOUSE {WAREHOUSE}").collect()
    session.sql(f"USE DATABASE {DB}").collect()
    session.sql(f"USE SCHEMA {SCHEMA}").collect()
    session.sql("ALTER SESSION SET QUERY_TAG = 'pyws_readonly_explore'").collect()

    src_fqn = f"{DB}.{SCHEMA}.{TABLE}"
    df = session.table(src_fqn)

    # --- 1) Quick preview (safe) ---
    print("🔎 Preview of source:")
    df.limit(ROW_PREVIEW).show()

    # --- 2) Deterministic sample for EDA (server-side; no downloads yet) ---
    df_sample = df.sample(fraction=SAMPLE_FRAC, seed=SAMPLE_SEED)
    print(f"🔎 {int(SAMPLE_FRAC*100)}% sample (seed={SAMPLE_SEED}) preview:")
    df_sample.limit(ROW_PREVIEW).show()

    # --- 3) Select + compute columns (read-only transformations) ---
    # Example computed columns: cleaned date, safe amount, simple status bucket
    df_t = (
        df
        .with_column(DATE_COL, to_date(col(DATE_COL)))
        .with_column("TOTAL_AMOUNT_SAFE", coalesce(col("TOTAL_AMOUNT"), lit(0)).cast("NUMBER(18,2)"))
        .with_column(
            "AMOUNT_BUCKET",
            when(col("TOTAL_AMOUNT") <= 100, lit("small"))
            .when(col("TOTAL_AMOUNT") <= 1000, lit("medium"))
            .otherwise(lit("large"))
        )
        .select("ORDER_ID", "CUSTOMER_ID", DATE_COL, "TOTAL_AMOUNT_SAFE", "AMOUNT_BUCKET")
        .filter(col(DATE_COL) >= lit(DATE_START))
        .filter(col("TOTAL_AMOUNT_SAFE") > lit(MIN_TOTAL_AMOUNT))
    )

    print("🔧 Transformed preview:")
    df_t.limit(ROW_PREVIEW).show()

    # --- 4) Lightweight aggregation (still in Snowflake) ---
    by_bucket = (
        df_t.group_by("AMOUNT_BUCKET")
            .agg(
                scount(lit(1)).alias("ROW_COUNT"),
                ssum(col("TOTAL_AMOUNT_SAFE")).alias("TOTAL_AMOUNT_SUM")
            )
            .sort(col("TOTAL_AMOUNT_SUM").desc())
    )

    print("📊 Aggregation preview:")
    by_bucket.show()

    # --- 5) Optional small pandas extract (keep it tiny) ---
    if PANDAS_OUT:
        import pandas as pd  # ensure a supported pandas version is added in Packages
        small_pd = by_bucket.limit(1000).to_pandas()
        print("🧪 pandas head():")
        print(small_pd.head())

    # TIPs:
    # - Use df.explain() to see the SQL plan Snowflake will execute (no write).
    # - Avoid .collect() on huge sets; use .limit(), .sample(), or aggregate first.
    # - You can join to other existing tables similarly: session.table("PROD.SALES.CUSTOMERS") ...

    # Return a Snowpark DataFrame so the worksheet renders a grid
    return by_bucket
