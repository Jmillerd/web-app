"QoQ Trends"
+ CHAR(10) + CHAR(10)

+ "    • ASP: $" +
IF [ASP_numeric] >= 1000000 THEN
    STR(INT([ASP_numeric] / 1000000)) + "M"
ELSEIF [ASP_numeric] >= 1000 THEN
    STR(INT([ASP_numeric] / 1000)) + "K"
ELSE
    STR(INT([ASP_numeric]))
END

+ CHAR(10)

+ "    • iACV: $" +
IF [iACV_numeric] >= 1000000 THEN
    STR(INT([iACV_numeric] / 1000000)) + "M"
ELSEIF [iACV_numeric] >= 1000 THEN
    STR(INT([iACV_numeric] / 1000)) + "K"
ELSE
    STR(INT([iACV_numeric]))
END

+ CHAR(10)

+ "    • SW SALs: " +
STR([SW_SALS_numeric])

