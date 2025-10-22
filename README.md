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

SRC_DB, SRC_SCHEMA, SRC_TABLE = "PROD", "SALES", "ORDERS"     # read from here
OUT_DB, OUT_SCHEMA            = "USER$JESSIE", "PRACTICE"     # write to your sandbox
ROW_LIMIT                     = 10000

def main(session: Session):
    # Read context
    session.sql(f"USE DATABASE {SRC_DB}").collect()
    session.sql(f"USE SCHEMA {SRC_SCHEMA}").collect()

    # Write context (your sandbox)
    session.sql(f"USE DATABASE {OUT_DB}").collect()
    session.sql(f"CREATE SCHEMA IF NOT EXISTS {OUT_DB}.{OUT_SCHEMA}").collect()
    session.sql(f"USE SCHEMA {OUT_SCHEMA}").collect()

    src_fqn  = f"{SRC_DB}.{SRC_SCHEMA}.{SRC_TABLE}"
    out_tbl  = f"{OUT_DB}.{OUT_SCHEMA}.{SRC_TABLE}_PRACTICE"
    out_view = f"{OUT_DB}.{OUT_SCHEMA}.{SRC_TABLE}_PRACTICE_V"

    # Create small practice table
    session.sql(f"""
        CREATE OR REPLACE TABLE {out_tbl} AS
        SELECT * FROM {src_fqn} LIMIT {ROW_LIMIT}
    """).collect()

    # Create view on top (for Tableau or testing)
    session.sql(f"CREATE OR REPLACE VIEW {out_view} AS SELECT * FROM {out_tbl}").collect()

    print("✅ Practice table:", out_tbl)
    print("✅ Practice view :", out_view)

    df = session.table(out_view).limit(20)
    df.show()
    return df

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

