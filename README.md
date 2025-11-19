"QoQ Trends"
+ CHAR(10)
+ CHAR(10)
+ 
"    • ASP: $" +
STR(
    ROUND(
        { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
        }
    , 0)
)
+ CHAR(10)
+
"    • iACV: $" +
STR(
    ROUND(
        { FIXED [Year Quarter] :
            SUM([iACV])
        }
    , 0)
)
+ CHAR(10)
+
"    • SW SALs: " +
STR(
    { FIXED [Year Quarter] :
        SUM( INT([is_sw_sal]) )
    }
)
