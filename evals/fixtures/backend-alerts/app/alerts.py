def list_open_alerts(alerts, user):
    """Return open alerts visible to the user, newest first."""
    # TODO: Enforce permission and filter open alerts.
    return alerts


def summarize_by_severity(alerts):
    summary = {}
    for alert in alerts:
        severity = alert.get("severity", "unknown")
        summary[severity] = summary.get(severity, 0) + 1
    return summary
