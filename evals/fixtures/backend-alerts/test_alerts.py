from app.alerts import list_open_alerts, summarize_by_severity


ALERTS = [
    {"id": "a1", "status": "open", "severity": "warning", "created_at": 2, "account_id": "acct-a"},
    {"id": "a2", "status": "closed", "severity": "critical", "created_at": 4, "account_id": "acct-a"},
    {"id": "a3", "status": "open", "severity": "critical", "created_at": 1, "account_id": "acct-b"},
    {"id": "a4", "status": "open", "severity": "critical", "created_at": 3, "account_id": "acct-a"},
]


def test_list_open_alerts_filters_by_permission_and_status():
    user = {"permissions": ["alerts:read"], "account_id": "acct-a"}
    assert [alert["id"] for alert in list_open_alerts(ALERTS, user)] == ["a4", "a1"]


def test_list_open_alerts_rejects_missing_permission():
    user = {"permissions": [], "account_id": "acct-a"}
    try:
        list_open_alerts(ALERTS, user)
    except PermissionError:
        return
    raise AssertionError("expected PermissionError")


def test_summarize_by_severity():
    assert summarize_by_severity(ALERTS) == {"warning": 1, "critical": 3}


if __name__ == "__main__":
    test_list_open_alerts_filters_by_permission_and_status()
    test_list_open_alerts_rejects_missing_permission()
    test_summarize_by_severity()
