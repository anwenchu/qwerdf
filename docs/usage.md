# Usage

This guide covers installation, the Product Delivery workflow, and generated artifacts.

中文：本文说明如何安装 qwerdf skills、如何按 Product Delivery 链路使用，以及产物默认写到哪里。

## Install

Install skills as live symlinks into `${CODEX_HOME:-$HOME/.codex}/skills/`:

```bash
bash scripts/install.sh
```

Live symlink mode is the default and recommended mode for local development. When the output says `Already installed as live symlink`, it does not mean a stale copy was skipped. It means Codex points directly at this repository, so every `SKILL.md` or `qwerdf-common` edit is already effective after reinstall or restart.

Preview the install:

```bash
bash scripts/install.sh --dry-run
```

Use copy mode only when symlinks are not desired. Copy mode refreshes existing qwerdf-owned copies on each install:

```bash
bash scripts/install.sh --copy
```

Switch install modes explicitly:

```bash
bash scripts/install.sh --copy --force  # replace qwerdf-owned symlinks with refreshed copies
bash scripts/install.sh --force         # replace qwerdf-owned copies with live symlinks
```

The installer refuses to overwrite non-qwerdf entries under `${CODEX_HOME:-$HOME/.codex}/skills/`. Only current qwerdf live symlinks or copies marked with `.qwerdf-install-source` are refreshed or replaced.

Uninstall only qwerdf-owned entries recorded in `${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/manifest.tsv`:

```bash
bash scripts/uninstall.sh
bash scripts/uninstall.sh --dry-run
```

## Workflow

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-ui-review -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

- Product discovery: `$pd-vet`, `$pd-prd`
- Product and UI design: `$pd-blueprint`, `$pd-figma`, `$pd-ui-review`
- Engineering design and implementation: `$pd-plan`, `$pd-fe`, `$pd-be`
- Quality gates: `$pd-sync`, `$pd-test`, `$pd-review`
- Git and release: `$pd-git`, `$pd-release`

For Figma work, the default is to show candidate directions in a separate Figma exploration page before asking the user to choose, then refine the chosen direction. Existing approved directions can be reused; explicit local-only or choose-before-writing requests take precedence. Identify the destination early and report actual file/frame links and preview type; local boards do not count as Figma delivery. The maintained rules are in [pd-figma](../skills/pd-figma/SKILL.md#gate-1在-figma-比较并选择-ui-方向).

## Output Directory

Java implementation and backend review directly read the [shared Java coding conventions](../skills/qwerdf-common/java-coding-rules.md); no separate command is required. The [source and adaptation notes](../skills/qwerdf-common/java-coding-sources.md) explain how Alibaba's handbook is applied to current repository contracts and configuration.

By default, skills write artifacts under `pd-work/<name>/`. New artifacts must use canonical subdirectories. Legacy flat files may be read as a legacy fallback, but new outputs should not be written flat.

```text
pd-work/<name>/
  product/
    idea-brief.md
    user-problem.md
    competitor-notes.md
    mvp-hypothesis.md
    validation-questions.md
    prd.md
    requirements.md
    user-stories.md
    acceptance-criteria.md
    open-questions.md
    product-brief.md
  ui/
    ui-design-system.md
    ui-flows.md
    ui-pages.md
    ui-screens.md
    ui-components.md
    ui-directions.md
    figma-handoff.md
    ui-review-report.md
  tech/
    tech-plan.md
    dependency-readiness.md
    api-contract.md
    integration-map.md
    task-slices.md
    risk-plan.md
    frontend/
      frontend-design.md
      frontend-component-map.md
      frontend-route-map.md
      frontend-state-api.md
      frontend-implementation-log.md
      frontend-changed-files.md
      frontend-dev-notes.md
      frontend-acceptance.md
    backend/
      backend-design.md
      data-model.md
      sql-execution-plan.md
      backend-implementation-log.md
      backend-changed-files.md
      backend-dev-notes.md
  sync/
    integration-plan.md
    integration-report.md
    api-mismatch.md
    plan-revision.md
  test/
    test-plan.md
    test-cases.md
    test-report.md
    regression-notes.md
    code-review.md
  release/
    commit-summary.md
    pr-description.md
    release-plan.md
    release-checklist.md
    rollback-plan.md
    release-notes.md
```

## Key Gates

- `ui/ui-design-system.md` is the UI system source of truth. `MASTER` defines global rules; `Page Overrides` records only necessary page-level differences.
- `tech/backend/sql-execution-plan.md` must exist. If no SQL is needed, it must explicitly say so.
- `tech/dependency-readiness.md` must classify real dependencies before `$pd-fe` or `$pd-be`.
- `$pd-sync`, `$pd-test`, and `$pd-review` must pass before `$pd-git` prepares a commit.
