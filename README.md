# qwerdf

Open-source Codex Product Delivery Skills for moving product work from idea validation to PRD, UI design, technical planning, implementation, integration, testing, review, Git readiness, and release documentation.

中文：qwerdf 是一组开源 Codex Product Delivery Skills，用于把产品想法推进到 PRD、UI 蓝图、Figma 交付、技术设计、前后端实现、联调、测试、审查、提交准备和上线文档。

## Quick Start

Install the skills into `${CODEX_HOME:-$HOME/.codex}/skills/`:

```bash
bash scripts/install.sh
```

Preview install actions:

```bash
bash scripts/install.sh --dry-run
```

Validate the repository:

```bash
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
python3 scripts/run_skill_benchmark.py --dry-run --skill pd-ui-review
```

## Workflow

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-ui-review -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

Default outputs are written to `pd-work/<name>/` with canonical folders such as `product/`, `ui/`, `tech/`, `sync/`, `test/`, and `release/`. Legacy fallback reads are allowed for older flat artifacts, but new outputs should use the canonical structure.

## Skills

| Skill | Purpose |
| --- | --- |
| `$pd-vet` | Validate an idea, user problem, competitor note, or MVP hypothesis. |
| `$pd-prd` | Produce PRD, requirements, user stories, acceptance criteria, and open questions. |
| `$pd-blueprint` | Convert PRD inputs into product brief, UI design system, flows, pages, screens, and components. |
| `$pd-figma` | Generate UI directions and deliver Figma handoff from product and UI artifacts. |
| `$pd-ui-review` | Review Figma frames, screenshots, handoff, and UI visual quality with P0/P1/P2/P3 findings. |
| `$pd-plan` | Produce technical plan, dependency readiness, API contract, frontend/backend design, SQL plan, integration map, and task slices. |
| `$pd-fe` | Implement one frontend slice with UI quality acceptance. |
| `$pd-be` | Implement one backend slice with real dependencies, data model, SQL/migration awareness, and tests. |
| `$pd-sync` | Run frontend/backend integration checks and reject mock-only implementation paths. |
| `$pd-test` | Plan and execute unit, integration, E2E, visual/UI, regression, and manual validation. |
| `$pd-review` | Run delivery and code review, including UI Review evidence and P0/P1/P2/P3 findings. |
| `$pd-git` | Prepare commit summary and PR/MR description after readiness gates pass. |
| `$pd-release` | Produce release plan, checklist, rollback plan, and release notes without deploying. |

## Repository Layout

```text
skills/
  manifest.txt
  qwerdf-common/
  pd-*/
docs/
  usage.md
  development.md
  benchmarking.md
  architecture.md
  references.md
evals/
  cases/
  fixtures/
  reports/
  runs/
scripts/
```

`skills/<skill-name>/SKILL.md` stays flat for Codex skill discovery. Do not move skills into nested category folders. The repository shows product/design/engineering/quality/release grouping through `skills/manifest.txt`, docs, and README tables.

## Documentation

- [Usage](docs/usage.md): install, uninstall, workflow, output artifacts, `MASTER`, `Page Overrides`, `ui-design-system.md`, `sql-execution-plan.md`, and delivery gates.
- [Development](docs/development.md): how to add or update a skill, update `skills/manifest.txt`, and maintain `evals/cases/trigger-queries.json` and `evals/cases/benchmark-cases.json`.
- [Benchmarking](docs/benchmarking.md): trigger preflight, real benchmark runs, dry-run layout, baseline mode, `forbidden_contains`, `last-message.txt`, and `checks/`.
- [Architecture](docs/architecture.md): Codex skill discovery, `skills/qwerdf-common`, progressive disclosure, and repository boundaries.
- [References](docs/references.md): how qwerdf adapts ideas from Anthropic Skills, Vercel Agent Skills, and UI/UX Pro Max Skill.

## Validation

```bash
python3 -m json.tool evals/cases/benchmark-cases.json
python3 -m json.tool evals/cases/trigger-queries.json
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
python3 scripts/run_skill_benchmark.py --dry-run --skill pd-ui-review --runs-dir /private/tmp/qwerdf-layout-bench
python3 -m py_compile scripts/validate_skills.py scripts/preflight_triggers.py scripts/run_skill_benchmark.py scripts/validate_codex_install.py
bash scripts/install.sh --dry-run
bash scripts/uninstall.sh --dry-run
git diff --check
```

## Boundaries

- qwerdf skills are local-first and do not create external lifecycle directories or mutate external state.
- `$pd-release` creates Markdown release artifacts; it does not deploy.
- Product facts outrank design references. References can shape visual style and interaction detail, not product scope.
- Generated reports under `evals/reports/`, benchmark runs under `evals/runs/`, local IDE files, Python caches, and `pd-work/` outputs should not be committed.

## License

License: see [LICENSE](LICENSE). Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md). Security: see [SECURITY.md](SECURITY.md). Changes: see [CHANGELOG.md](CHANGELOG.md).
