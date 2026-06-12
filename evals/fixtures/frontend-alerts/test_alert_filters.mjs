import assert from "node:assert/strict";
import { filterCriticalAlerts, summarizeAlerts } from "./src/alertFilters.mjs";

const alerts = [
  { id: "a1", severity: "warning", status: "open", createdAt: "2026-01-02T10:00:00Z" },
  { id: "a2", severity: "critical", status: "closed", createdAt: "2026-01-03T10:00:00Z" },
  { id: "a3", severity: "critical", status: "open", createdAt: "2026-01-01T10:00:00Z" },
  { id: "a4", severity: "critical", status: "open", createdAt: "2026-01-04T10:00:00Z" }
];

assert.deepEqual(
  filterCriticalAlerts(alerts).map((alert) => alert.id),
  ["a4", "a3"]
);

assert.deepEqual(summarizeAlerts(alerts), {
  total: 4,
  critical: 3,
  open: 3
});
