# Contributing

This repository keeps a small, practical set of Codex skills. Changes should preserve local-first behavior, clear trigger boundaries, and reproducible validation.

Before submitting a change, run:

```bash
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict
python3 scripts/run_skill_benchmark.py --dry-run --run-baseline
bash scripts/install.sh --dry-run
```

When adding or renaming a skill:

1. Add the skill directory under `skills/`.
2. Add the skill name to `skills/manifest.txt`.
3. Add or update trigger examples in `evals/trigger-queries.json`.
4. Add or update benchmark coverage in `evals/benchmark-cases.json`.
5. Keep shared templates in `skills/qwerdf-common/` instead of duplicating long instructions.

Do not add secrets, local credentials, generated benchmark runs, or private workspace state.
