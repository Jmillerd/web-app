"PIPELINE PERFORMANCE" 
+ CHAR(10) +
"--------------------" + CHAR(10) +
"• Target Motion Buckets:" + CHAR(10) +
"    - Mkt: " 
+ STR( SUM( IF [Target Motion] = 'Mkt' THEN [pipeline] END ) )
+ " total pipeline." + CHAR(10) +
"    - <Bucket 2 Name>: <Insert calculation>" + CHAR(10) +
"    - <Bucket 3 Name>: <Insert calculation>" + CHAR(10)


