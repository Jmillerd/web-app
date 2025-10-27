from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark.functions import col, count_distinct


def get_unique_email_count(session: Session) -> DataFrame:
    """
    Returns a Snowpark DataFrame with the distinct email count.
    """
    df: DataFrame = (
        session.table("DB.SCHEMA.TABLE_NAME")        # <-- update with your table
        .filter(col("EMAIL_ADDRESS").is_not_null())
        .filter(col("EMAIL_ADDRESS") != "")
        .agg(count_distinct(col("EMAIL_ADDRESS")).alias("UNIQUE_EMAIL_COUNT"))
    )
    return df


def main():
    # create or grab the session once
    session: Session = get_active_session()

    # call your method and pass the same session
    result_df = get_unique_email_count(session)

    # show the dataframe
    result_df.show()

    # print the Python integer
    rows = result_df.collect()
    unique_count = rows[0][0] if rows else 0
    print("Unique Email Count:", unique_count)


# standard Python entry point
if __name__ == "__main__":
    main()
