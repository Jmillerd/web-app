# web-app

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


