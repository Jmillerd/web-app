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
# Optional: pivot_pt.to_excel("agency_by_program_type_avg.xlsx")



