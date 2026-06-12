export function filterCriticalAlerts(alerts) {
  // TODO: Return only open critical alerts sorted by newest first.
  return alerts;
}

export function summarizeAlerts(alerts) {
  return {
    total: alerts.length,
    critical: alerts.filter((alert) => alert.severity === "critical").length,
    open: alerts.filter((alert) => alert.status === "open").length
  };
}
