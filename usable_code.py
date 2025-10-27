(no spaces) from snowflake.snowpark import Session
(no spaces) from snowflake.snowpark.dataframe import DataFrame
(no spaces) from snowflake.snowpark.functions import col, count_distinct

(no spaces) def get_unique_email_count_df(session: Session) -> DataFrame:
(4 spaces) """
(4 spaces) Returns a Snowpark DataFrame with the distinct email count.
(4 spaces) """
(4 spaces) df: DataFrame = (
(8 spaces) session.table("DB.SCHEMA.TABLE_NAME")
(8 spaces) .filter(col("EMAIL_ADDRESS").is_not_null())
(8 spaces) .filter(col("EMAIL_ADDRESS") != "")
(8 spaces) .agg(count_distinct(col("EMAIL_ADDRESS")).alias("UNIQUE_EMAIL_COUNT"))
(4 spaces) )
(4 spaces) return df

(no spaces) result_df = get_unique_email_count_df(session)
(no spaces) result_df.show()
(no spaces) print(result_df.collect()[0]["UNIQUE_EMAIL_COUNT"])
