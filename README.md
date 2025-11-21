"PIPELINE PERFORMANCE: " +

" Total - " + "$" +
IF SUM([PL $]) >= 1000000 THEN
    STR(INT(SUM([PL $]) / 1000000)) + "M"
ELSEIF SUM([PL $]) >= 1000 THEN
    STR(INT(SUM([PL $]) / 1000)) + "K"
ELSE
    STR(INT(SUM([PL $])))
END

+ CHAR(10) +
CHAR(10) +

" • Focused BDR: $" +
IF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000000)) + "M"
ELSEIF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000)) + "K"
ELSE
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END )))
END

+ CHAR(10) +

" • Market Response: $" +
IF SUM( IF [Target Motion Buckets] = '' THEN [Pipeline $] END ) >= 1000000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [Pipeline $] END ) / 1000000)) + "M"
ELSEIF SUM( IF [Target Motion Buckets] = '' THEN [Pipeline $] END ) >= 1000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [Pipeline $] END ) / 1000)) + "K"
ELSE
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [Pipeline $] END )))
END

+ CHAR(10) +

" • ISR: $" +
IF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000000)) + "M"
ELSEIF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000)) + "K"
ELSE
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END )))
END

+ CHAR(10) +

" • No Motion: $" +
IF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000000)) + "M"
ELSEIF SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) >= 1000 THEN
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END ) / 1000)) + "K"
ELSE
    STR(INT(SUM( IF [Target Motion Buckets] = '' THEN [PL $] END )))
END
