from datetime import date
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, count, sum as ssum, when, date_trunc, lit, to_date

session = get_active_session()

# ----- Step 1: define the current period -----
start_date = date(2025, 10, 1)
end_date   = date(2025, 10, 31)

# ----- Step 2: read your table -----
df = session.table("DB.SCHEMA.TABLE_NAME")

# ----- Step 3: filter to valid emails and current period -----
filtered = (
    df.filter(col("EMAIL_ADDRESS").is_not_null())
      .filter(col("EMAIL_ADDRESS") != "")
      .filter(
          (date_trunc('day', col("SEND_ACTIVITY_DATE")) >= to_date(lit(start_date))) &
          (date_trunc('day', col("SEND_ACTIVITY_DATE")) <= to_date(lit(end_date)))
      )
)

# ----- Step 4: compute KPIs from raw data -----
# (replace the column names below with your real event columns)
kpis = (
    filtered.agg(
        count(lit(1)).alias("Total_Sent"),
        ssum(when(col("STATUS") == "Delivered", 1).otherwise(0)).alias("Delivered"),
        ssum(when(col("STATUS") == "Bounced", 1).otherwise(0)).alias("Bounced"),
        ssum(when(col("ACTION") == "Open", 1).otherwise(0)).alias("Opens"),
        ssum(when(col("ACTION") == "Click", 1).otherwise(0)).alias("Clicks"),
        ssum(when(col("ACTION") == "Unsubscribe", 1).otherwise(0)).alias("Unsubscribes")
    )
)

# ----- Step 5: view results -----
kpis.show()
