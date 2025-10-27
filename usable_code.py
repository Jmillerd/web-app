from snowflake.snowpark.functions import col, count_distinct

def run(session):
    """
    Handler for the stored procedure execution context.
    Snowflake automatically passes the 'session' object here.
    """
    # ---- Query logic ----
    df = (
        session.table("DB.SCHEMA.TABLE_NAME")       # <-- update this path
        .filter(col("EMAIL_ADDRESS").is_not_null())
        .filter(col("EMAIL_ADDRESS") != "")
        .agg(count_distinct(col("EMAIL_ADDRESS")).alias("UNIQUE_EMAIL_COUNT"))
    )

    # ---- Display and return results ----
    df.show()

    rows = df.collect()
    unique_count = rows[0][0] if rows else 0

    # Return a message or scalar (depending on SP definition)
    return f"Unique Email Count: {unique_count}"

