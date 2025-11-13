"📊 PIPELINE PERFORMANCE" +
"\nCurrent Pipeline: " +
STR(ROUND([Pipeline_Total], 0)) +

"\n\n🔁 WEEK OVER WEEK" +
"\nWoW Change: " +
IF ISNULL([WoW_Pipeline_Change]) THEN
    "n/a"
ELSE
    STR(ROUND([WoW_Pipeline_Change] * 100, 1)) + "%"
END +

"\n\n📈 QUARTER OVER QUARTER TRENDS" +
"\nASP: " +
STR(ROUND([ASP_QoQ_Change] * 100, 1)) + "%" +
"\nSW SAL: " +
STR(ROUND([SW_SAL_QoQ_Change] * 100, 1)) + "%" +
"\niACV: " +
STR(ROUND([iACV_QoQ_Change] * 100, 1)) + "%"
