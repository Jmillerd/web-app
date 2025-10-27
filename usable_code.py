from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, count_distinct

def get_unique_email_count(session):
    return (
        session.table("DB.SCHEMA.TABLE_NAME")
        .filter(col("EMAIL_ADDRESS").is_not_null())
        .filter(col("EMAIL_ADDRESS") != "")
        .agg(count_distinct(col("EMAIL_ADDRESS")).alias("UNIQUE_EMAIL_COUNT"))
    )

# normal (non-SP) entry
session = get_active_session()
df = get_unique_email_count(session)
df.show()
print(df.collect()[0][0])
