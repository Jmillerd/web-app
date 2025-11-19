// =======================================================
// Calc 1: ASP_Qtr  (numeric)
// Average Selling Price per quarter
// =======================================================
{ FIXED [Year Quarter] :
    SUM([pipeline]) / COUNTD([opportunity_name])
}



// =======================================================
// Calc 2: ASP_Qtr_Formatted  (string)
// ASP_Qtr with commas (e.g., 1,234,567)
// =======================================================
IF ISNULL([ASP_Qtr]) THEN
    ""
ELSE

    // Remove any existing commas from the base string
    // so we can safely add our own.
    // s := REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")

    IF LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) <= 3 THEN

        REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")

    ELSEIF LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) <= 6 THEN

        LEFT(
            REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) - 3
        )
        + ","
        + RIGHT(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", ""), 3)

    ELSEIF LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) <= 9 THEN

        LEFT(
            REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) - 6
        )
        + ","
        + MID(
            REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")) - 5,
            3
        )
        + ","
        + RIGHT(REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", ""), 3)

    ELSE

        // If it’s longer than 9 digits, just show raw for now.
        REPLACE(STR(ROUND([ASP_Qtr], 0)), ",", "")

    END
END



// =======================================================
// Calc 3: iACV_Qtr  (numeric)
// iACV per quarter
// =======================================================
{ FIXED [Year Quarter] :
    SUM([iACV])
}



// =======================================================
// Calc 4: iACV_Qtr_Formatted  (string)
// iACV_Qtr with commas (e.g., 2,500,000)
// =======================================================
IF ISNULL([iACV_Qtr]) THEN
    ""
ELSE

    // s := REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")

    IF LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) <= 3 THEN

        REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")

    ELSEIF LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) <= 6 THEN

        LEFT(
            REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) - 3
        )
        + ","
        + RIGHT(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", ""), 3)

    ELSEIF LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) <= 9 THEN

        LEFT(
            REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) - 6
        )
        + ","
        + MID(
            REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", ""),
            LEN(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")) - 5,
            3
        )
        + ","
        + RIGHT(REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", ""), 3)

    ELSE

        REPLACE(STR(ROUND([iACV_Qtr], 0)), ",", "")

    END
END



// =======================================================
// Calc 5: QoQ_Trends_Text  (string)
// Final text block using formatted ASP / iACV + SW SALs
// =======================================================
"QoQ Trends"
+ CHAR(10)
+ CHAR(10)

+ "    • ASP: $" +
[ASP_Qtr_Formatted]
+ CHAR(10)

+ "    • iACV: $" +
[iACV_Qtr_Formatted]
+ CHAR(10)

+ "    • SW SALs: "
+ STR(
    { FIXED [Year Quarter] :
        SUM( INT([is_sw_sal]) )
    }
)
