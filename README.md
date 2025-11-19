// Quarterly Insights: textual summary for each quarter
// Assumes the view has [Year Quarter] on Columns or Rows
// and is ordered in time so LOOKUP(..., -1) refers to the previous quarter.

// Current quarter values
// ASP per quarter
// (Total pipeline / distinct opps)
"Quarter: " + STR(ATTR([Year Quarter]))
+ CHAR(10) +
"ASP: " 
+ STR(
    ROUND(
        SUM([pipeline]) / COUNTD([opportunity_name])
    , 0)
)
+ " | SW SALs: "
+ STR(
    SUM( INT([is_sw_sal]) )
)
+ " | iACV: "
+ STR(
    ROUND(
        SUM([iACV])
    , 0)
)
+ CHAR(10) +
"ASP Trend: "
+
CASE 
    // No previous quarter in the partition
    WHEN ISNULL(
        LOOKUP(
            SUM([pipeline]) / COUNTD([opportunity_name]),
            -1
        )
    ) THEN
        "First quarter in view (no QoQ comparison)."

    // ASP up > +5%
    WHEN (SUM([pipeline]) / COUNTD([opportunity_name])) 
         > LOOKUP(SUM([pipeline]) / COUNTD([opportunity_name]), -1) * 1.05
    THEN "Increased significantly QoQ (average deal value is rising)."

    // ASP down < -5%
    WHEN (SUM([pipeline]) / COUNTD([opportunity_name])) 
         < LOOKUP(SUM([pipeline]) / COUNTD([opportunity_name]), -1) * 0.95
    THEN "Decreased QoQ (mix may be shifting to smaller/discounted deals)."

    // Otherwise roughly flat
    ELSE "Roughly flat QoQ (deal size is relatively stable)."
END
+ CHAR(10) +
"SW SAL Volume Trend: "
+
CASE 
    WHEN ISNULL(
        LOOKUP(
            SUM( INT([is_sw_sal]) ),
            -1
        )
    ) THEN
        "First quarter in view (no QoQ comparison)."

    WHEN SUM( INT([is_sw_sal]) )
         > LOOKUP(SUM( INT([is_sw_sal]) ), -1) * 1.10
    THEN "Software deal count is up sharply QoQ."

    WHEN SUM( INT([is_sw_sal]) )
         < LOOKUP(SUM( INT([is_sw_sal]) ), -1) * 0.90
    THEN "Software deal count is down noticeably QoQ."

    ELSE "Software deal volume is roughly stable QoQ."
END
+ CHAR(10) +
"iACV Trend: "
+
CASE
    WHEN ISNULL(
        LOOKUP(
            SUM([iACV]),
            -1
        )
    ) THEN
        "First quarter in view (no QoQ comparison)."

    WHEN SUM([iACV])
         > LOOKUP(SUM([iACV]), -1) * 1.10
    THEN "Total revenue impact (iACV) is up strongly QoQ."

    WHEN SUM([iACV])
         < LOOKUP(SUM([iACV]), -1) * 0.90
    THEN "Total revenue impact (iACV) is down QoQ."

    ELSE "Overall iACV is relatively stable QoQ."
END
