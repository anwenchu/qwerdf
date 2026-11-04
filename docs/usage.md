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
pd-work/<bounded-requirement>/
  product/prd.md             # 需求、规则、验收、开放问题
  tech/tech-plan.md          # 两端设计、数据、真实输入、接线、风险
  tech/task-slices.md        # 顺序、状态、简短结果与续作
```

Only maintain the stage currently requested. Discovery may use one `product/idea-brief.md`; UI adds a shared design system and page specification, with Figma handoff when delivered. Contracts shared by endpoints/external consumers and SQL execution/rollback plans remain independent when needed. Integration, test and review each maintain one formal report; release notes include the deployment plan/checks/rollback. Git text stays in the reply unless explicitly requested as files.

Do not create every available template or duplicate stage trees per task. Existing split sources are read and referenced without automatic migration/deletion. Requirement/acceptance IDs and their compact mapping remain in the main index; long explanations may link to unique topic details.


## Key Gates

- `ui/ui-design-system.md` is the UI system source of truth. `MASTER` defines global rules; `Page Overrides` records only necessary page-level differences.
- SQL execution plans are required for applicable execution/rollback work. With no SQL impact, record the basis in the technical plan; do not create an empty file.
- The technical plan’s real-input section (or an existing independent readiness source) classifies actual coding and validation dependencies before execution. No standalone file is required solely for its name.
- `$pd-sync`, `$pd-test`, and `$pd-review` must pass before `$pd-git` prepares a commit.
