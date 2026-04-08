def get_event_after_nav_click(df, session_id=None, **filters):
    temp = df.copy()

    # Optional: limit to one session for testing
    if session_id is not None:
        temp = temp[temp["SESSION_ID"] == session_id]

    temp = temp.sort_values(["SESSION_ID", "EVENT_TIMESTAMP"])

    click_filter = temp["EVENT_NAME"] == "link_click"

    for col, val in filters.items():
        click_filter &= temp[col] == val

    temp["prev_is_target_click"] = click_filter.groupby(temp["SESSION_ID"]).shift(1, fill_value=False)

    return temp[temp["prev_is_target_click"]].copy()


def get_events_after_click(df, session_id=None, include_click=False, **filters):
    temp = df.copy()

    # Optional: limit to one session for testing
    if session_id is not None:
        temp = temp[temp["SESSION_ID"] == session_id]

    temp = temp.sort_values(["SESSION_ID", "EVENT_TIMESTAMP"])

    click_filter = temp["EVENT_NAME"] == "link_click"

    for col, val in filters.items():
        click_filter &= temp[col] == val

    temp["after_target_click"] = click_filter.groupby(temp["SESSION_ID"]).cummax()

    result = temp[temp["after_target_click"]].copy()

    if not include_click:
        result = result[~click_filter.loc[result.index]]

    return result
