# Contributing

This repository keeps a small, practical set of Codex skills. Changes should preserve local-first behavior, clear trigger boundaries, and reproducible validation.

Before submitting a change, run:

```bash
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
python3 scripts/run_skill_benchmark.py --dry-run --run-baseline
bash scripts/install.sh --dry-run
```

When adding or renaming a skill:

1. Add the skill directory under `skills/`.
2. Add the skill name to `skills/manifest.txt`.
3. Add or update trigger examples in `evals/cases/trigger-queries.json`.
4. Add or update benchmark coverage in `evals/cases/benchmark-cases.json`.
5. Keep shared templates in `skills/qwerdf-common/` instead of duplicating long instructions.

Repository docs live under `docs/`. Do not add README files inside individual skill directories.

Do not add secrets, local credentials, generated benchmark runs, generated reports, `pd-work/` outputs, or private workspace state.
