// Helper inline function pattern: format a number as K/M
// (We’ll reuse the logic inline for ASP and iACV)

"QoQ Trends"
+ CHAR(10)
+ CHAR(10)

+ "    • ASP: $" +
IF { FIXED [Year Quarter] :
        SUM([pipeline]) / COUNTD([opportunity_name])
   } >= 1000000 THEN
    // Millions
    STR(ROUND(
        { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
        } / 1000000.0
    , 1)) + "M"
ELSEIF { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
       } >= 1000 THEN
    // Thousands
    STR(ROUND(
        { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
        } / 1000.0
    , 1)) + "K"
ELSE
    STR(ROUND(
        { FIXED [Year Quarter] :
            SUM([pipeline]) / COUNTD([opportunity_name])
        }
    , 0))
END

+ CHAR(10)

+ "    • iACV: $" +
IF { FIXED [Year Quarter] : SUM([iACV]) } >= 1000000 THEN
    STR(ROUND(
        { FIXED [Year Quarter] : SUM([iACV]) } / 1000000.0
    , 1)) + "M"
ELSEIF { FIXED [Year Quarter] : SUM([iACV]) } >= 1000 THEN
    STR(ROUND(
        { FIXED [Year Quarter] : SUM([iACV]) } / 1000.0
    , 1)) + "K"
ELSE
    STR(ROUND(
        { FIXED [Year Quarter] : SUM([iACV]) }
    , 0))
END

+ CHAR(10)

+ "    • SW SALs: " +
STR(
    { FIXED [Year Quarter] :
        SUM( INT([is_sw_sal]) )
    }
)

