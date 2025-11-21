"Current Quarter Pipeline: $" +
IF [Pipeline_Qtr] >= 1000000 THEN
    STR(INT([Pipeline_Qtr] / 1000000)) + "M"
ELSEIF [Pipeline_Qtr] >= 1000 THEN
    STR(INT([Pipeline_Qtr] / 1000)) + "K"
ELSE
    STR(INT([Pipeline_Qtr]))
END

+ CHAR(10) +

"Previous Quarter Pipeline: $" +
IF LOOKUP([Pipeline_Qtr], -1) >= 1000000 THEN
    STR(INT(LOOKUP([Pipeline_Qtr], -1) / 1000000)) + "M"
ELSEIF LOOKUP([Pipeline_Qtr], -1) >= 1000 THEN
    STR(INT(LOOKUP([Pipeline_Qtr], -1) / 1000)) + "K"
ELSE
    STR(INT(LOOKUP([Pipeline_Qtr], -1)))
END

+ CHAR(10) +

"Quarter-Over-Quarter Pipeline: $" +
IF ([Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1)) >= 1000000 THEN
    STR(INT(( [Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1) ) / 1000000)) + "M"
ELSEIF ([Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1)) >= 1000 THEN
    STR(INT(( [Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1) ) / 1000)) + "K"
ELSE
    STR(INT([Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1)))
END

+ CHAR(10) +

"Quarter-Over-Quarter % Change: " +
STR(
    ROUND(
        ( [Pipeline_Qtr] - LOOKUP([Pipeline_Qtr], -1) )
        / LOOKUP([Pipeline_Qtr], -1)
        * 100
    , 1)
) + "%"
