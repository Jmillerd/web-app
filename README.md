// Text explainer: Pipeline performance week over week
// Assumes the view is partitioned by week (e.g., Week of [Opp Pipeline Date])
// and ordered in time so LOOKUP(..., -1) refers to the previous week.

"Pipeline Performance - Week Over Week"
+ CHAR(10) +
CHAR(10) +

"    • Current Week Pipeline: "
+ STR(
    ROUND(
        SUM([pipeline])
    , 0)
)
+ CHAR(10) +

"    • Previous Week Pipeline: "
+ STR(
    ROUND(
        LOOKUP(SUM([pipeline]), -1)
    , 0)
)
+ CHAR(10) +

"    • Week-over-Week Change: "
+ STR(
    ROUND(
        SUM([pipeline]) - LOOKUP(SUM([pipeline]), -1)
    , 0)
)
+ CHAR(10) +

"    • Week-over-Week % Change: "
+ 
IF LOOKUP(SUM([pipeline]), -1) = 0 OR ISNULL(LOOKUP(SUM([pipeline]), -1)) THEN
    "n/a"
ELSE
    STR(
        ROUND(
            (
                SUM([pipeline]) - LOOKUP(SUM([pipeline]), -1)
            )
            / ABS(LOOKUP(SUM([pipeline]), -1)) * 100
        , 1)
    ) + "%"
END
