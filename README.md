WITH ordered_events AS (
    SELECT
        user_id,                     -- or session_id
        event_timestamp,
        page_path,
        event_name,
        LEAD(page_path) OVER (
            PARTITION BY user_id     -- or session_id
            ORDER BY event_timestamp
        ) AS next_page_path
    FROM events_table
    WHERE event_name IN (
        'form_start',
        'form_submit_success',
        'page_view'
    )
)

SELECT
    page_path AS form_page,
    next_page_path,
    COUNTIF(event_name = 'form_start') AS form_starts,
    COUNTIF(event_name = 'form_submit_success') AS form_submits
FROM ordered_events
WHERE page_path = '/your/form/page'
GROUP BY
    page_path,
    next_page_path
ORDER BY
    form_starts DESC;
