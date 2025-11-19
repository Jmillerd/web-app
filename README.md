"QoQ Trends"
+ CHAR(10) +
CHAR(10) +

"    • ASP: $" +
FORMAT(
    ROUND(
        { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
        }
    , 0),
    "#,###"
)
+ CHAR(10) +

"    • iACV: $" +
FORMAT(
    ROUND(
        { FIXED [Year Quarter] :
            SUM([iACV])
        }
    , 0),
    "#,###"
)
+ CHAR(10) +

"    • SW SALs: " +
STR(
    { FIXED [Year Quarter] :
        SUM( INT([is_sw_sal]) )
    }
)

    ) + "%"
END
