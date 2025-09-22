# web-app

TOP_N = 15

# Take top N by average score
top_avg = (df.groupby("Agency Name", as_index=False)["Total Score"].mean()
             .rename(columns={"Total Score": "Overall Score (Avg)"}))
top_avg = top_avg.sort_values("Overall Score (Avg)", ascending=False)
top_avg["Rank"] = range(1, len(top_avg) + 1)
top_avg = top_avg.head(TOP_N).sort_values("Overall Score (Avg)")

# Plot
plt.figure(figsize=(10, max(5, 0.5 * TOP_N)))
bars = plt.barh(top_avg["Agency Name"], top_avg["Overall Score (Avg)"])

# Add labels and rank badges at left
for bar, (_, row) in zip(bars, top_avg.iterrows()):
    val = row["Overall Score (Avg)"]
    y = bar.get_y() + bar.get_height()/2
    # value at the end
    plt.text(bar.get_width(), y, f" {val:.2f}", va="center")
    # rank on the left margin
    plt.text(0, y, f"#{int(row['Rank'])}", va="center", ha="right")

plt.title(f"Top {TOP_N} Agencies by Average Total Score")
plt.xlabel("Average Total Score")
plt.ylabel("Agency Name")
pad_xlim(plt.gca())
plt.tight_layout()
plt.show()

# Build Sum and Avg
agency_sum = df.groupby("Agency Name", as_index=False)["Total Score"].sum()
agency_sum.rename(columns={"Total Score": "Overall Score (Sum)"}, inplace=True)

agency_avg = df.groupby("Agency Name", as_index=False)["Total Score"].mean()
agency_avg.rename(columns={"Total Score": "Overall Score (Avg)"}, inplace=True)

combo = agency_sum.merge(agency_avg, on="Agency Name", how="inner")

# Focus on top N by Avg (change to Sum if preferred)
TOP_N = 12
combo = combo.sort_values("Overall Score (Avg)", ascending=False).head(TOP_N)

# Prepare positions for grouped bars
idx = np.arange(len(combo))
h = 0.4  # bar height
plt.figure(figsize=(12, max(5, 0.55 * TOP_N)))

bars1 = plt.barh(idx + h/2, combo["Overall Score (Avg)"], height=h, label="Avg")
bars2 = plt.barh(idx - h/2, combo["Overall Score (Sum)"], height=h, label="Sum")

# Y-ticks as Agency names
plt.yticks(idx, combo["Agency Name"])

# Labels for both bar groups
for b in bars1:
    x = b.get_width()
    y = b.get_y() + b.get_height()/2
    plt.text(x, y, f" {x:.2f}", va="center")
for b in bars2:
    x = b.get_width()
    y = b.get_y() + b.get_height()/2
    plt.text(x, y, f" {x:.0f}", va="center")  # Sum often integer-like

plt.legend(loc="lower right")
plt.title(f"Top {TOP_N} Agencies — Average vs Sum of Total Scores")
plt.xlabel("Score")
plt.ylabel("Agency Name")
pad_xlim(plt.gca())
plt.tight_layout()
plt.show()


# Build a clean ranking table you can export
agg = df.groupby("Agency Name", as_index=False)["Total Score"].agg(
    Overall_Avg="mean",
    Overall_Sum="sum",
    Program_Count="count"
)

# Ranks
agg["Rank_Avg"] = agg["Overall_Avg"].rank(method="min", ascending=False).astype(int)
agg["Rank_Sum"] = agg["Overall_Sum"].rank(method="min", ascending=False).astype(int)

# Percentiles (0–100)
agg["Percentile_Avg"] = agg["Overall_Avg"].rank(pct=True) * 100

# Sort how you’ll present it (by Avg rank)
final_table = agg.sort_values(["Rank_Avg", "Rank_Sum", "Agency Name"])
print(final_table.head(20))

# Optional export
# final_table.to_excel("agency_overall_ranking.xlsx", index=False)


# Utility: standard labelled horizontal bars
def barh_with_labels(names, values, title, xlabel, top_n=None, integer=False):
    ser = pd.Series(values, index=names)
    if top_n:
        ser = ser.sort_values(ascending=False).head(top_n)
    ser = ser.sort_values(ascending=True)

    plt.figure(figsize=(11, max(5, 0.45 * len(ser))))
    bars = plt.barh(ser.index, ser.values)
    for bar, val in zip(bars, ser.values):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height()/2
        fmt = f"{val:.0f}" if integer else f"{val:.2f}"
        plt.text(x, y, f" {fmt}", va="center", fontsize=9)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("")
    pad_xlim(plt.gca())
    plt.tight_layout()
    plt.show()


    agency_avg = (df.groupby("Agency Name", as_index=False)["Total Score"]
                .mean()
                .rename(columns={"Total Score": "Overall Avg"}))

barh_with_labels(
    names=agency_avg["Agency Name"],
    values=agency_avg["Overall Avg"],
    title="Agency Ranking by Average Total Score (All Programs, All Populations)",
    xlabel="Average Total Score",
    top_n=None,  # set to e.g., 15 if you want Top 15
    integer=False
)

agency_sum = (df.groupby("Agency Name", as_index=False)["Total Score"]
                .sum()
                .rename(columns={"Total Score": "Overall Sum"}))

barh_with_labels(
    names=agency_sum["Agency Name"],
    values=agency_sum["Overall Sum"],
    title="Agency Ranking by Sum of Total Scores (All Programs, All Populations)",
    xlabel="Sum of Scores",
    top_n=15,
    integer=True
)

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


pivot_pt = (df.pivot_table(index="Agency Name",
                           columns="Priority",
                           values="Total Score",
                           aggfunc="mean")
              .round(2)
              .sort_index())

print(pivot_pt)      # readable table in console
# Optional: pivot_pt.to_excel("agency_by_program_type_avg.xlsx")

