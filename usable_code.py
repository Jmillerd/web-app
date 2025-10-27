from snowflake.snowpark import Session
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark.functions import col, count_distinct

def get_unique_email_count_df(session: Session) -> DataFrame:
    """
    Returns a Snowpark DataFrame containing the distinct count of email addresses.
    No table creation, no procedures, SELECT-only logic.
    """
    df: DataFrame = (
        session.table("DB.SCHEMA.TABLE_NAME")          # <-- replace with your table
        .filter(col("EMAIL_ADDRESS").is_not_null())    # remove NULLs
        .filter(col("EMAIL_ADDRESS") != "")            # remove blanks
        .agg(count_distinct(col("EMAIL_ADDRESS")).alias("UNIQUE_EMAIL_COUNT"))
    )
    return df

# --- Usage Example ---
result_df = get_unique_email_count_df(session)

# Show result as DF
result_df.show()

# Also print value as Python integer
unique_count = result_df.collect()[0]["UNIQUE_EMAIL_COUNT"]
print("Unique Email Count:", unique_count)
