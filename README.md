"Pipeline Performance - Week Over Week"
+ CHAR(10) +
CHAR(10) +

"    • Current Week Pipeline: $" +
IF SUM([PL]) >= 1000000 THEN
    STR(INT(SUM([PL]) / 1000000)) + "M"
ELSEIF SUM([PL]) >= 1000 THEN
    STR(INT(SUM([PL]) / 1000)) + "K"
ELSE
    STR(INT(SUM([PL])))
END
+ CHAR(10) +

"    • Previous Week Pipeline: $" +
IF LOOKUP(SUM([PL]), -1) >= 1000000 THEN
    STR(INT(LOOKUP(SUM([PL]), -1) / 1000000)) + "M"
ELSEIF LOOKUP(SUM([PL]), -1) >= 1000 THEN
    STR(INT(LOOKUP(SUM([PL]), -1) / 1000)) + "K"
ELSE
    STR(INT(LOOKUP(SUM([PL]), -1)))
END
+ CHAR(10) +

"    • Week-over-Week Change: $" +
IF (SUM([PL]) - LOOKUP(SUM([PL]), -1)) >= 1000000 THEN
    STR(INT((SUM([PL]) - LOOKUP(SUM([PL]), -1)) / 1000000)) + "M"
ELSEIF (SUM([PL]) - LOOKUP(SUM([PL]), -1)) >= 1000 THEN
    STR(INT((SUM([PL]) - LOOKUP(SUM([PL]), -1)) / 1000)) + "K"
ELSE
    STR(INT(SUM([PL]) - LOOKUP(SUM([PL]), -1)))
END
+ CHAR(10) +

"    • Week-over-Week % Change: " +
IF LOOKUP(SUM([PL]), -1) = 0 OR ISNULL(LOOKUP(SUM([PL]), -1)) THEN
    "n/a"
ELSE
    STR(
        ROUND(
            ( SUM([PL]) - LOOKUP(SUM([PL]), -1) )
            / ABS(LOOKUP(SUM([PL]), -1)) * 100
        , 1)
    ) + "%"
END

