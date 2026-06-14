# qwerdf

开源 Codex Product Delivery Skills 仓库。

本仓库维护一组 `pd-` 前缀的开源 Codex Product Delivery Skills，用于把 idea 推进到 PRD、产品设计输入、页面蓝图、Figma 高保真设计、技术设计、前后端并行实现、联调、测试、审查、提交准备和上线文档。它们不接入任何外部变更生命周期，不创建外部变更目录，不修改外部状态文件，默认把交付产物写入当前工作区的 `pd-work/<name>/`。

## Workflow

产品设计段：

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma
```

工程实现段：

```text
$pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test
```

审查交付段：

```text
$pd-review -> $pd-git -> $pd-release
```

完整链路：

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

## Skills

- `$pd-vet`：把一句话 idea、竞品 URL、截图或市场观察拆成问题、用户、竞品、MVP 假设和验证问题。
- `$pd-prd`：把已验证 idea、用户问题、MVP 假设和竞品参考整理成正式 PRD 与验收口径。
- `$pd-blueprint`：把 PRD、竞品 URL、截图、产品想法或已有 spec 拆成产品设计输入、UI 设计系统和 UI 页面蓝图。
- `$pd-figma`：基于产品设计输入、UI 设计系统和页面蓝图先生成 3 个 UI 方向，用户选择后再写入或整理 Figma 设计交付。
- `$pd-plan`：把 PRD、UI 设计系统、UI 蓝图、Figma handoff 和现有代码库串成前后端一致的技术设计，并输出前端组件、路由、状态/API 映射。
- `$pd-fe`：按 `tech/task-slices.md` 执行一个前端 slice，实现页面、组件、状态、API client 和前端 UI 质量验收。
- `$pd-be`：按 `tech/task-slices.md` 执行一个后端 slice，实现接口、服务逻辑、数据模型、权限和后端测试。
- `$pd-sync`：做前后端联调，记录接口、状态、权限、mock/真实接口差异；发现契约问题时回到 `$pd-plan`。
- `$pd-test`：制定并执行测试验证，区分 unit、integration、e2e、visual/UI regression、regression、manual acceptance。
- `$pd-review`：做结构化 Code Review 和 UI Review，按 `P0/P1/P2/P3` 输出风险、UI 质量问题和测试缺口。
- `$pd-git`：准备 commit/PR 文案；用户明确要求时可执行 `git add`、`git commit`，默认不 push。
- `$pd-release`：生成通用 Markdown 上线计划、检查清单、回滚方案和 release notes，不执行部署。

## Output

默认产物目录：

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
  tech/
    tech-plan.md
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

`<name>` 优先使用用户给出的项目名或产品名；没有明确名称时，由 skill 推导简短 kebab-case 名称。新产物必须写入上述分目录；旧平铺文件只作为 legacy fallback 读取。

## Install

把 skill 以 symlink 安装到 `${CODEX_HOME:-$HOME/.codex}/skills/`。Codex 需要 skill 出现在 `skills/` 顶层才能被发现；qwerdf 自己的安装记录会独立放在 `${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/`：

```bash
bash scripts/install.sh
```

预览安装动作：

```bash
bash scripts/install.sh --dry-run
```

不想使用 symlink 时复制安装。copy 模式会同时复制 `skills/qwerdf-common/`，否则每个 skill 的 `../qwerdf-common/...` 相对链接会断开：

```bash
bash scripts/install.sh --copy
```

安装脚本不会覆盖同名的非本仓库 skill。
安装脚本会写入 `${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/manifest.tsv`，卸载时只处理这个 manifest 记录的 qwerdf 条目。

卸载已安装的 skill：

```bash
bash scripts/uninstall.sh
```

预览卸载动作：

```bash
bash scripts/uninstall.sh --dry-run
```

卸载脚本只会读取 `${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/manifest.tsv`，并删除其中记录的 qwerdf symlink 或带 qwerdf marker 的 copy 安装；不会删除同名真实目录、指向其他位置的链接或其他项目的安装记录。

## Validate

```bash
python3 scripts/validate_skills.py
```

验证内容包括：

- `SKILL.md` frontmatter 只有 `name` 和 `description`。
- `skills/manifest.txt` 是唯一 skill 清单，且必须与 `skills/pd-*` 目录完全一致。
- `name` 与目录名一致。
- `agents/openai.yaml` 存在，并包含 `display_name`、`short_description`、`default_prompt`。
- `default_prompt` 显式包含 `$skill-name`。
- Markdown 相对链接可解析。
- README 和 skills 中不出现旧命令名或废弃目录名。
- `evals/trigger-queries.json` 存在，且每个 `$pd-*` skill 至少有一个 should-trigger 样例。
- trigger evals 至少包含 6 个 should-not-trigger 近似反例。
- `evals/benchmark-cases.json` 存在，且每个 `$pd-*` skill 至少有一个真实执行 benchmark case。
- README 中记录的 benchmark 核心产物结构与 runner 的 dry-run 输出保持一致。

## Benchmark

触发 preflight 是本地确定性检查，只用于快速发现描述过宽或过窄：

```bash
python3 scripts/preflight_triggers.py --strict --write-default-reports
```

触发 preflight 不是模型路由评估，不代表真实 Codex skill 选择效果；真实质量以执行 benchmark 的产物、检查命令和评分结果为准。

`evals/benchmark-cases.json` 的核心断言字段：

- `expected_files`：必须生成且非空的文件。
- `all_contains` / `required_contains`：目标文件必须包含的片段。
- `any_contains`：目标文件至少包含其中一个片段。
- `forbidden_contains`：目标文件不得包含的片段，用于防止把参考产品的业务模块、导航、资产类型或文案带入本产品。
- `forbidden_files`：不得生成的文件。
- `check_commands`：在 case 输出目录中执行的真实校验命令。

真实 benchmark 必须运行外部 agent 命令。runner 不会伪造模型输出；dry-run 只预览命令、prompt 和目录结构：

```bash
python3 scripts/run_skill_benchmark.py --dry-run
```

真实运行默认绑定 Codex CLI，使用 `codex exec`、隔离 case workspace、复制目标 skill bundle，并通过 stdin 传入 prompt：

```bash
python3 scripts/run_skill_benchmark.py \
  --repetitions 3 \
  --timeout-seconds 900 \
  --strict
```

如需和 no-skill baseline 对照，默认也可以使用 Codex CLI baseline。baseline run 不会复制或读取 qwerdf skill bundle：

```bash
python3 scripts/run_skill_benchmark.py \
  --run-baseline \
  --repetitions 3 \
  --timeout-seconds 900 \
  --strict
```

baseline 会先整批执行，之后才执行 with-skill；这样 baseline 执行期间不会看到本轮 benchmark 复制出来的 skill bundle。

如果要接其他 agent，传入自定义命令模板；runner 会为每个 case 写入 prompt、输出目录、命令、stdout、stderr、产物和评分结果：

```bash
python3 scripts/run_skill_benchmark.py \
  --with-skill-command 'your-agent --skill "$skill_path" --prompt-file "$prompt_file"' \
  --baseline-command 'your-agent --prompt-file "$prompt_file"'
```

自定义命令模板可使用这些变量：

- `$prompt_file`
- `$output_dir`
- `$case_id`
- `$skill`
- `$skill_path`
- `$last_message_file`

调试单个 case 或单个 skill：

```bash
python3 scripts/run_skill_benchmark.py --list-cases
python3 scripts/run_skill_benchmark.py --dry-run --case pd-fe-single-slice-reporting
python3 scripts/run_skill_benchmark.py --dry-run --skill pd-fe
```

`evals/fixtures/` 中的前端和后端 fixture 是故意未实现的红灯用例，只有 agent 按对应 skill 完成实现后，case 内的 `check_commands` 才应通过。

dry-run 只生成核心目录、命令文件和空输出目录；它不会执行 agent 或 check commands，因此不会生成 `last-message.txt` 或 `checks/`：

```text
evals/runs/<timestamp>/
  benchmark.json
  benchmark.md
  baseline/
    <case-id>/
      rep-01/
        prompt.md
        command.json
        stdout.txt
        stderr.txt
        outputs/
  with_skill/
    <case-id>/
      rep-01/
        prompt.md
        command.json
        stdout.txt
        stderr.txt
        outputs/
```

真实执行会额外生成 `checks/`。使用默认 Codex CLI 时还会生成 `last-message.txt`；自定义命令如果需要保留最终回复，应写入 `$last_message_file`。

`baseline/` 只有传入 `--run-baseline` 或 `--baseline-command` 时才会生成。

## skill-creator 是什么

`skill-creator` 是 Codex 内置的 skill 创建/维护规范。它规定了 skill 的目录结构、`SKILL.md` frontmatter 只能包含 `name` 和 `description`、如何写触发描述、什么时候把长模板放进 references/common 文件、如何生成 `agents/openai.yaml`，以及如何做基础校验。

本仓库按它的原则维护：skill 名短、统一前缀、`SKILL.md` 只放执行流程，详细产物模板放在 `skills/qwerdf-common/`。参考 Anthropic skills 和 Vercel agent-skills 的组织方式，每个 skill 都保持明确触发场景、渐进式读取、边界、流程、输出摘要和可验证证据。

## External Skill References

本仓库不是只参考两个开源仓库的目录结构，也参考了其中代表性 `SKILL.md` 的内容写法：

- `anthropics/skills/skills/skill-creator/SKILL.md`：采用主动触发描述、渐进式披露、测试提示和反馈迭代思路。
- `anthropics/skills/skills/frontend-design/SKILL.md`：采用先确定主体 / 受众 / 页面任务，再写颜色、字体、布局、标志性元素和反模板化自检的设计流程。
- `anthropics/skills/skills/webapp-testing/SKILL.md`：采用静态 / 动态、服务是否运行、先侦察后操作的浏览器验证决策树。
- `vercel-labs/agent-skills/skills/react-best-practices/SKILL.md`：采用按影响优先级组织工程规则的方式，补入 waterfalls、bundle、server/client 边界、重渲染等前端检查点。
- `vercel-labs/agent-skills/skills/composition-patterns/SKILL.md`：采用组件架构优先级，补入避免 boolean prop 膨胀、组合组件和 provider 边界等检查点。
- `vercel-labs/agent-skills/skills/vercel-optimize/SKILL.md`：采用证据优先、确定性 gate、候选范围收窄、建议绑定文件和版本的审查方式。
- `vercel-labs/agent-skills/skills/deploy-to-vercel/SKILL.md`：采用先采集项目状态、再选择动作路径、默认避免高影响动作的安全流程；本仓库只借鉴状态采集，不执行部署。
- `vercel-labs/agent-skills/skills/web-design-guidelines/SKILL.md`：采用先读取最新规则，再按文件范围输出定位 findings 的审查模式。
- `nextlevelbuilder/ui-ux-pro-max-skill`：借鉴 data / scripts / templates 分层、按需加载 UI/UX 知识、Design System Generator、MASTER design system + page override、以及 UI 质量 checklist 的组织方式；本仓库只吸收结构和可验证规则，不复制外部风格库、营销话术或平台模板。

## Boundaries

- 不要求外部探索或变更初始化流程。
- 不创建外部变更目录。
- 不修改 `.state.yaml`。
- 不设置外部 artifact 状态。
- 不新增总入口 skill。
- 不接 GitHub Release、GitLab、GitOps、Lark 等发布平台。
- 不执行真实部署；未来如需部署，另行设计 `$pd-deploy`。
- 竞品只提炼模式，不照抄视觉、文案或受保护资产。
- 设计参考只能提供视觉风格、信息密度、布局节奏、组件形态和交互细节；产品范围、页面、导航、资产类型、业务模块和关键文案必须来自 PRD、product-brief、UI 蓝图或用户明确确认。
- 参考材料与产品文档冲突时，以产品文档为准；冲突内容必须写入“不应照搬 / 参考使用边界”，不得下推到 Figma、技术设计或实现。
- `ui/ui-design-system.md` 是 UI 设计系统事实源；`MASTER` 定义全局规则，页面级差异写入 `Page Overrides`。`$pd-blueprint` 生成草案，`$pd-figma` 确认和补齐，`$pd-plan` / `$pd-fe` / `$pd-review` 只读取、执行和验证。
- SaaS、CRM、管理后台和操作台默认采用克制、密集、可扫描、效率优先的界面方向；不得把 landing page hero、过度卡片化或装饰性视觉带入操作型产品，除非 PRD 明确要求。
- 提交和 PR 准备必须晚于联调、测试和 Code Review；`$pd-sync` 未通过、`$pd-test` 未通过或 `$pd-review` 有 P0/P1 时，不得进入 `$pd-git` 执行提交。
- 提交前必须检查 `.gitignore`、ignored / untracked 状态和 planned files，确认没有漏提交相关文件，也没有多提交缓存、日志、截图、构建产物、临时报告或历史 benchmark run。

## Structure

```text
skills/
  qwerdf-common/
    artifact-contracts.md
    engineering-contracts.md
    product-delivery-flow.md
    ui-design-system.md
    ui-quality-checklist.md
    ui-patterns.md
    ui-review-rules.md
  manifest.txt
  pd-vet/
    SKILL.md
    agents/openai.yaml
  pd-prd/
    SKILL.md
    agents/openai.yaml
  pd-blueprint/
    SKILL.md
    agents/openai.yaml
  pd-figma/
    SKILL.md
    agents/openai.yaml
  pd-plan/
    SKILL.md
    agents/openai.yaml
  pd-fe/
    SKILL.md
    agents/openai.yaml
  pd-be/
    SKILL.md
    agents/openai.yaml
  pd-sync/
    SKILL.md
    agents/openai.yaml
  pd-test/
    SKILL.md
    agents/openai.yaml
  pd-review/
    SKILL.md
    agents/openai.yaml
  pd-git/
    SKILL.md
    agents/openai.yaml
  pd-release/
    SKILL.md
    agents/openai.yaml
scripts/
  install.sh
  uninstall.sh
  validate_skills.py
  preflight_triggers.py
  run_skill_benchmark.py
evals/
  trigger-queries.json
  benchmark-cases.json
  fixtures/
```

## Open Source Hygiene

- License: see [LICENSE](LICENSE).
- Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).
- Security reporting: see [SECURITY.md](SECURITY.md).
- Changes: see [CHANGELOG.md](CHANGELOG.md).
