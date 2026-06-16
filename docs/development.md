# Development

This guide is for maintainers changing or adding qwerdf skills.

中文：维护 skill 时要保持触发边界清晰、共享规则可复用、校验可重复。

## Skill Layout

Each skill lives directly under `skills/`:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/   # optional
  scripts/      # optional
```

Do not add per-skill README files. Keep user-facing repository documentation in `docs/` and keep long reusable skill rules in `references/` or `skills/qwerdf-common/`.

## Adding or Renaming a Skill

1. Add the skill directory under `skills/`.
2. Add the skill name to `skills/manifest.txt`.
3. Add or update trigger examples in `evals/cases/trigger-queries.json`.
4. Add or update benchmark coverage in `evals/cases/benchmark-cases.json`.
5. Add `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt`.
6. Keep shared templates in `skills/qwerdf-common/` instead of duplicating long instructions.

## SKILL.md Rules

- Frontmatter must contain only `name` and `description`.
- `description` must explain what the skill does and when to use it; include `$skill-name`.
- Keep `SKILL.md` focused on core workflow and routing.
- Move long checklists, templates, and language/framework details into references or common files.
- Use relative links from the skill to `../qwerdf-common/...` for shared rules.

## Validation

Run these before submitting changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
python3 scripts/run_skill_benchmark.py --dry-run --run-baseline
bash scripts/install.sh --dry-run
```

If you changed Python scripts:

```bash
python3 -m py_compile scripts/validate_skills.py scripts/preflight_triggers.py scripts/run_skill_benchmark.py scripts/validate_codex_install.py
```

Generated reports and runs belong under ignored directories:

- `evals/reports/`
- `evals/runs/`

Do not commit secrets, local credentials, generated benchmark runs, private workspace state, or `pd-work/` outputs.
