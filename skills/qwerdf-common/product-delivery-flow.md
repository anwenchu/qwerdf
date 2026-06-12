# Codex Product Delivery 规则

本文件是所有 `$pd-*` skill 的共享规则源。它们是独立的开源 Codex Product Delivery Skills，不绑定任何外部变更生命周期，不参与外部研发流程状态流转。

产品和设计阶段模板见 [artifact-contracts.md](artifact-contracts.md)。工程阶段模板见 [engineering-contracts.md](engineering-contracts.md)。

## 1. 交付链路

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

| 阶段 | 负责 Skill | 必要产物 |
| --- | --- | --- |
| 想法验证 | `$pd-vet` | `idea-brief.md`、`user-problem.md`、`competitor-notes.md`、`mvp-hypothesis.md`、`validation-questions.md` |
| PRD 生成 | `$pd-prd` | `prd.md`、`requirements.md`、`user-stories.md`、`acceptance-criteria.md`、`open-questions.md` |
| 产品设计输入 | `$pd-blueprint` | `product-brief.md` |
| UI 页面蓝图 | `$pd-blueprint` | `ui-flows.md`、`ui-pages.md`、`ui-screens.md`、`ui-components.md` |
| Figma 设计交付 | `$pd-figma` | `ui-directions.md`、`figma-handoff.md` |
| 技术设计 | `$pd-plan` | `tech-plan.md`、`frontend-design.md`、`frontend-component-map.md`、`frontend-route-map.md`、`frontend-state-api.md`、`backend-design.md`、`api-contract.md`、`data-model.md`、`integration-map.md`、`task-slices.md`、`risk-plan.md` |
| 前端实现 | `$pd-fe` | `frontend-implementation-log.md`、`frontend-changed-files.md`、`frontend-dev-notes.md`、`frontend-acceptance.md` |
| 后端实现 | `$pd-be` | `backend-implementation-log.md`、`backend-changed-files.md`、`backend-dev-notes.md` |
| 前后端联调 | `$pd-sync` | `integration-plan.md`、`integration-report.md`、`api-mismatch.md`、`plan-revision.md` |
| 测试验证 | `$pd-test` | `test-plan.md`、`test-cases.md`、`test-report.md`、`regression-notes.md` |
| Code Review | `$pd-review` | `code-review.md` |
| Git 提交准备 | `$pd-git` | `commit-summary.md`、`pr-description.md` |
| 上线文档 | `$pd-release` | `release-plan.md`、`release-checklist.md`、`rollback-plan.md`、`release-notes.md` |

## 2. 默认工作目录

如果用户未指定输出目录，默认在当前工作区创建：

```text
pd-work/<name>/
```

其中 `<name>` 优先来自用户提供的项目名 / 产品名；没有明确名称时，用简短 kebab-case 名称推导，例如 `ai-crm-dashboard`。

如果用户明确要求写到其他目录，使用用户指定目录，但保持同一组文件名。

## 3. Skill 执行规范

- 每个 `$pd-*` skill 只读取本阶段需要的公共模板和上游产物，避免一次性加载无关模板。
- 触发描述必须说明 “做什么” 和 “什么时候使用”，不要只罗列命令名。
- 产物必须可复用：写清输入来源、关键判断、未验证假设、验证证据和下一步。
- 缺少关键输入时先列出缺口并提问，不生成看似完整但依据不足的文件。
- 需要修改代码、设计、Git 或外部系统时，遵守对应 skill 的边界；没有明确授权时只做计划、报告或文案。
- 执行命令、浏览器验证或截图检查后，必须在对应报告中记录命令 / 方式、结果和证据位置。
- 当任务反复出现相同机械步骤时，优先把步骤沉淀为脚本或公共模板，而不是在多个 skill 中复制长指令。
- 修改 skill 描述、触发词或阶段边界后，检查 `evals/trigger-queries.json`，确保 should-trigger 和 should-not-trigger 样例仍然成立。

### 产品事实与参考使用 Gate

- 产品事实源优先级：用户明确说明、PRD、需求清单、产品设计输入、UI 页面蓝图、现有代码 / 数据结构高于竞品、截图、Figma 参考和视觉样例。参考材料不能覆盖或扩展产品事实源。
- 设计前必须先建立产品事实锁：产品名称、目标用户、核心场景、支持的业务对象、页面 / 导航范围、明确不做的内容。
- 外部参考必须拆成两类：可借鉴的抽象视觉 / 交互模式，以及不得带入的业务语义 / 导航文案 / 产品模块 / 交易品类 / 品牌资产 / 受保护文案。
- 参考对象中出现但产品事实源未出现的功能、页面、tab、资产类型、合约类型、营销入口、社区 / 活动 / copy trading 等模块，默认视为参考禁区，只能写进“不得带入 / 不应照搬”，不能成为产品范围、页面结构、Figma frame、API 契约或任务切片。
- 如果无法判断某个参考元素是视觉风格还是产品能力，先提问；无人确认时按不带入处理。
- 设计输出必须能追溯：页面、组件、状态、导航和关键文案都要来自产品事实源或明确的用户确认；参考材料只贡献风格、布局密度、信息组织方式或微交互。
- Figma / 截图是表现层参考，不是需求来源。Figma handoff 与 PRD、product-brief 或 UI 蓝图冲突时，先记录冲突并停止，不把冲突内容下推到技术设计或实现。

## 4. 安全与意外最小化

- Skill 内容不能包含与描述不符的隐藏行为、越权访问、数据外传、恶意脚本或误导性流程。
- 不把 token、cookie、密钥、敏感信息写入命令、日志、产物或 PR 描述。
- 涉及 Git、Figma、发布平台、外部 API、真实部署或写入外部系统时，先说明目标、范围和动作后再执行。
- 默认不执行 destructive、push、deploy、publish、sync-to-external 等高影响动作，除非用户明确要求并且对应 skill 允许。
- 读取外部或远程规则时记录来源；规则版本可能变化时，不把旧规则当作当前事实。

## 5. 外部 SKILL.md 内容模式

本仓库补充规则参考以下具体 `SKILL.md` 内容模式，而不只是参考仓库目录结构：

- Anthropic `skill-creator/SKILL.md`：触发描述要“偏主动”，正文用渐进式披露；长规则放 references / common，脚本可作为黑盒执行；改 skill 时用测试提示和反馈迭代。
- Anthropic `frontend-design/SKILL.md`：设计前先钉住主体、受众和页面任务；先写颜色、字体、布局、标志性元素的短计划，再自检是否模板化。
- Anthropic `webapp-testing/SKILL.md`：浏览器验证采用决策树，先确认静态 / 动态、服务是否运行，再侦察渲染态，最后执行交互；动态页面检查前等待稳定加载。
- Vercel `react-best-practices/SKILL.md` 和 `composition-patterns/SKILL.md`：把规则按优先级分组，先处理 waterfalls、bundle、server/client 数据、重渲染、组件架构等高影响问题。
- Vercel `vercel-optimize/SKILL.md`：先收集信号，再用确定性 gate 收窄调查范围；建议必须绑定证据、文件和版本，不做泛泛扫描。
- Vercel `web-design-guidelines/SKILL.md`：外部规则源可能变化时，先读取最新规则，再按指定文件 / 范围输出定位清晰的 findings。

## 6. 外部生命周期边界

这些 Skill 不做以下事情：

- 不创建外部变更目录。
- 不修改 `.state.yaml`。
- 不设置外部 artifact 状态。
- 不改变外部 change 生命周期状态。
- 不要求外部方案、任务拆分或实现流程作为前置或后置。
- 不把交付产物同步到 Apifox / Lark，除非用户单独明确要求。

## 7. 设计与工程 Gate

- `$pd-plan` 完成前，不允许进入 `$pd-fe` 或 `$pd-be`。
- `$pd-fe` 和 `$pd-be` 必须基于同一份 `task-slices.md`、`api-contract.md` 和 `integration-map.md`。
- `$pd-fe` 和 `$pd-be` 每次只能执行一个 task slice。
- 并行执行时，`$pd-fe` 和 `$pd-be` 只能更新自己负责的 slice 状态。
- `contract` 类型任务只能由 `$pd-plan` 处理，不能由 `$pd-fe` 或 `$pd-be` 单方面修改。
- `$pd-sync` 发现契约不一致时，不得直接修代码，必须先生成 `plan-revision.md` 并回到 `$pd-plan`。
- `$pd-test` 未执行验证时，不得把结论写成“通过”；只能写“未执行 / 需人工验证 / 有残余风险”。
- `$pd-review` 发现 P0/P1 时，不进入 `$pd-git`；先回到对应实现或方案 skill。
- `$pd-release` 必须读取 `test-report.md` 和 `code-review.md`；缺失时不得声称可以上线。

## 8. Task Slice 规则

`task-slices.md` 的任务优先级：

```text
P0: 阻断主流程，必须先做
P1: 核心功能，必须做
P2: 增强或补充，可后做
```

任务类型：

```text
frontend
backend
contract
shared-frontend
shared-backend
sync
test
```

任务状态：

```text
pending
in_progress
done
blocked
```

并行标记：

```text
parallel-safe
blocked-by
blocks
```

`contract` 表示同时影响前后端的契约类任务，例如 API 字段、错误码、权限、状态枚举、数据模型、分页结构、mock 数据结构。

## 9. Review 严重级别

`$pd-review` 输出的问题必须使用：

```text
P0: 阻断发布
P1: 必须修复
P2: 建议修复
P3: 可选优化
```

## 10. Git 与发布边界

- `$pd-git` 默认只准备 commit / PR 文案。
- 用户明确要求时，`$pd-git` 可执行 `git add` 和 `git commit`。
- 执行 `git add` 前必须展示 planned files，并排除明显无关文件。
- 有未解决 P0/P1、失败测试或未解释的契约差异时，不建议提交。
- 默认不 push，除非用户明确要求。
- `$pd-release` 只生成通用 Markdown 上线文档，不接平台、不部署。
