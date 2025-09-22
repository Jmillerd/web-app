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

---------------
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

-----------
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


