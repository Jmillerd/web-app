"📊 PIPELINE PERFORMANCE" +
"\nCurrent Pipeline: " + STR(SUM([Pipeline])) +

"\n\n🔁 WEEK OVER WEEK" +
"\nWoW Change: " +
STR(ROUND([WoW_Pipeline_Change]*100,1)) + "%" +

"\n\n📈 QUARTER OVER QUARTER TRENDS" +
"\nASP: " +
STR(ROUND([ASP_QoQ_Change]*100,1)) + "%" +
"\nSW SAL: " +
STR(ROUND([SW_SAL_QoQ_Change]*100,1)) + "%" +
"\niACV: " +
STR(ROUND([iACV_QoQ_Change]*100,1)) + "%"

