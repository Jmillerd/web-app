# web-app

program_types = df["Priority"].dropna().unique()

for pt in sorted(program_types):
    subset = df[df["Priority"] == pt]
    by_agency = (subset.groupby("Agency Name", as_index=False)["Total Score"]
                        .mean()
                        .rename(columns={"Total Score": "Avg Score"}))
    if by_agency.empty:
        continue
    barh_with_labels(
        names=by_agency["Agency Name"],
        values=by_agency["Avg Score"],
        title=f"Agency Ranking by Average Score — Program Type: {pt}",
        xlabel="Average Total Score",
        top_n=15,
        integer=False
    )


---------------
pop_groups = df["Served Population"].dropna().unique()

for pop in sorted(pop_groups):
    subset = df[df["Served Population"] == pop]
    by_agency = (subset.groupby("Agency Name", as_index=False)["Total Score"]
                        .mean()
                        .rename(columns={"Total Score": "Avg Score"}))
    if by_agency.empty:
        continue
    barh_with_labels(
        names=by_agency["Agency Name"],
        values=by_agency["Avg Score"],
        title=f"Agency Ranking by Average Score — Served Population: {pop}",
        xlabel="Average Total Score",
        top_n=15,
        integer=False
    )


-----------
pivot_pt = (df.pivot_table(index="Agency Name",
                           columns="Priority",
                           values="Total Score",
                           aggfunc="mean")
              .round(2)
              .sort_index())

print(pivot_pt)      # readable table in console


from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# ---- EDIT THESE 4 LINES ONLY ----
DB              = "PROD"
SRC_SCHEMA      = "SALES"
SRC_TABLE       = "ORDERS"           # e.g., PROD.SALES.ORDERS
PRACTICE_SCHEMA = "PRACTICE_JESSIE"  # your isolated area
ROW_LIMIT       = 10000              # cap your practice set

def main(session: Session):
    # Context (safe)
    session.sql(f"USE DATABASE {DB}").collect()
    session.sql(f"USE SCHEMA {SRC_SCHEMA}").collect()
    session.sql("ALTER SESSION SET QUERY_TAG = 'practice_pyws'").collect()

    # Fully qualified names
    src_fqn       = f"{DB}.{SRC_SCHEMA}.{SRC_TABLE}"
    prac_schema   = f"{DB}.{PRACTICE_SCHEMA}"
    prac_table    = f"{prac_schema}.{SRC_TABLE}_PRACTICE"
    prac_view     = f"{prac_schema}.{SRC_TABLE}_PRACTICE_V"

    # 1) Ensure a private practice schema (safe: creates only if missing)
    session.sql(f"CREATE SCHEMA IF NOT EXISTS {prac_schema}").collect()

    # 2) Create a SMALL practice table (CTAS) — IF NOT EXISTS (no overwrite)
    #    Uses ROW_NUMBER() to cap to ROW_LIMIT deterministically
    session.sql(f"""
        CREATE TABLE IF NOT EXISTS {prac_table} AS
        WITH base AS (
          SELECT *
          FROM {src_fqn}
          QUALIFY ROW_NUMBER() OVER (ORDER BY 1) <= {ROW_LIMIT}
        )
        SELECT * FROM base
    """).collect()

    # 3) Create/refresh a view that points to the practice table (in practice schema only)
    session.sql(f"""
        CREATE OR REPLACE VIEW {prac_view} AS
        SELECT *
        FROM {prac_table}
    """).collect()

    print("✅ Practice table:", prac_table)
    print("✅ Practice view :", prac_view)

    # Preview (read-only)
    df_preview = session.table(prac_view).limit(20)
    df_preview.show()
    return df_preview

# Optional: pivot_pt.to_excel("agency_by_program_type_avg.xlsx")

def cleanup_practice_objects(session):
    DB              = "PROD"
    PRACTICE_SCHEMA = "PRACTICE_JESSIE"
    SRC_TABLE       = "ORDERS"  # same as in your practice script

    prac_table = f"{DB}.{PRACTICE_SCHEMA}.{SRC_TABLE}_PRACTICE"
    prac_view  = f"{DB}.{PRACTICE_SCHEMA}.{SRC_TABLE}_PRACTICE_V"

    print("🧹 Cleaning up practice objects...")

    # Drop view first (in case it references the table)
    session.sql(f"DROP VIEW IF EXISTS {prac_view}").collect()
    print(f"✅ Dropped view: {prac_view}")

    # Drop table next
    session.sql(f"DROP TABLE IF EXISTS {prac_table}").collect()
    print(f"✅ Dropped table: {prac_table}")

    print("Cleanup complete. Practice schema left intact.")
    return "Done"

# To execute it in your worksheet:
# cleanup_practice_objects(session)

DROP SCHEMA IF EXISTS PROD.PRACTICE_JESSIE CASCADE;

