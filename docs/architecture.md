# Architecture

qwerdf is a Codex skill repository. It keeps the skill directory shape compatible with Codex discovery while organizing public documentation and evals like a normal open-source project.

中文：本仓库的 skill 物理目录保持扁平，是为了兼容 Codex skill discovery 和安装脚本。

## Repository Layout

```text
skills/
  manifest.txt
  qwerdf-common/
  pd-vet/
  pd-prd/
  pd-blueprint/
  pd-figma/
  pd-ui-review/
  pd-plan/
  pd-fe/
  pd-be/
  pd-sync/
  pd-test/
  pd-review/
  pd-git/
  pd-release/
docs/
evals/
  cases/
  fixtures/
  reports/
  runs/
scripts/
```

## Skill Discovery Constraint

Codex expects each skill at:

```text
skills/<skill-name>/SKILL.md
```

Do not move skills into nested directories such as `skills/product/pd-vet/`. That would break Codex skill discovery, install scripts, benchmark copying, and relative links to common files.

## Shared Rules

`skills/qwerdf-common` contains shared contracts and references:

- `product-delivery-flow.md`
- `artifact-contracts.md`
- `engineering-contracts.md`
- `ui-design-system.md`
- `ui-quality-checklist.md`
- `ui-patterns.md`
- `ui-review-rules.md`

Skills link to these files with `../qwerdf-common/...`. Keep this relative link model stable.

## Progressive Disclosure

- `SKILL.md` should contain the core workflow, boundaries, and output summary.
- Long checklists and reusable rules belong in `references/` or `qwerdf-common`.
- Deterministic logic belongs in `scripts/`.
- Repository-level instructions belong in `docs/`, not inside individual skill folders.

## Boundaries

- Skills do not create external change directories.
- Skills do not modify external lifecycle state.
- `$pd-release` writes Markdown release documents but does not deploy.
- Generated reports and benchmark runs are local artifacts, not source files.
