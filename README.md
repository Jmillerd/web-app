"    • <Bucket Name>: " +
STR(
    ROUND(
        SUM(
            IF [Target Motion] = '<Bucket Name>' THEN [pipeline] END
        )
    , 0)
)
