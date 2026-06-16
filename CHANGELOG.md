# Changelog

## Unreleased

- Reworked README into a concise bilingual open-source entrypoint and moved detailed usage, development, benchmark, architecture, and reference material into `docs/`.
- Moved eval case definitions into `evals/cases/` and generated reports into ignored `evals/reports/`.
- Added stage comments to `skills/manifest.txt` while preserving flat Codex skill discovery layout.
- Added a single skill manifest at `skills/manifest.txt`.
- Made copy installs include `skills/qwerdf-common/` so copied skills keep their shared-template links without colliding with other projects' `_common` directories.
- Isolated benchmark baseline execution before with-skill execution.
- Added benchmark case and skill filters.
- Added open-source hygiene files.
