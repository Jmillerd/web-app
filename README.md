METRIC EXPLAINER & HOW TO READ THE GRAPHS

1) ASP (Average Selling Price)

   • What it means:
     Average deal value per opportunity in that fiscal quarter.

   • Business definition:
     Total pipeline value / number of distinct opportunities.

   • Tableau calculation:
     { FIXED [Year Quarter] :
         SUM([pipeline]) / COUNTD([opportunity_name])
     }

   • How to read the ASP line:
     – Upward trend QoQ → we are closing larger deals on average.
     – Downward trend QoQ → mix is shifting toward smaller deals,
       discounts, or lower-value product tiers.
     – Flat ASP + rising volume → growth coming from more deals, not bigger deals.

   • When to worry / pay attention:
     – ASP drops while iACV stays flat → we might be needing more deals to hit the same revenue.
     – ASP rises but SW SAL volume drops → we may be relying on fewer, big wins (potential risk).


2) SW SAL (Software Sales Count)

   • What it means:
     How many opportunities in the quarter are flagged as software sales
     (is_sw_sal = TRUE).

   • Helper field (row-level):
     SW SAL Count =
       INT([is_sw_sal])

   • Aggregation in views:
     SUM([SW SAL Count])

   • How to read the SW SAL line:
     – Upward trend → more software deals being created/closed.
     – Downward trend → fewer software deals flowing through the pipeline.
     – Flat line with moving ASP/iACV → value per software deal is changing.

   • When to pay attention:
     – SW SAL volume drops while ASP rises → fewer, larger software deals.
     – SW SAL volume drops while iACV also drops → pipeline risk for software revenue.


3) iACV (Incremental ACV)

   • What it means:
     Total incremental annual contract value created in that quarter.

   • Tableau calculation:
     SUM([iACV])

   • How to read the iACV line:
     – Upward trend → more total revenue impact from closed / progressing deals.
     – Downward trend → softness in bookings or pipeline quality.
     – iACV rising while ASP is flat → growth driven by more deals, not bigger deals.
     – iACV rising while SW SAL rises → strong motion in software-led revenue.

   • When to pay attention:
     – iACV drops but SW SAL stays flat → deals may be smaller or downgraded.
     – iACV rises sharply but ASP drops → we’re doing more deals, but at a lower price point.


HOW TO USE THESE TOGETHER

   • ASP + SW SAL:
     – ASP shows "how big" the average deal is.
     – SW SAL shows "how many" software deals we’re doing.
     – High ASP + increasing SW SAL → ideal: more deals and they are big.

   • ASP + iACV:
     – ASP up + iACV up → we’re growing by bigger deals AND more overall value.
     – ASP down + iACV up → more deals, but at lower value each (high volume, lower price).

   • SW SAL + iACV:
     – Both up → software motion is a key revenue driver.
     – SW SAL up but iACV flat → lots of small software deals, not moving iACV much.
