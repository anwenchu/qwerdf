# Engineering Artifact Contracts

本文件定义工程阶段 skill 共享的产物模板。Skill 执行时只读取本任务需要的模板。依据、范围与交接判断统一见 [技术设计依据与范围规则](technical-design-rules.md)；按本轮风险选用下列记录，不为局部修订重做无关历史材料。

## `tech/tech-plan.md`

```markdown
# 技术方案 — <name>

## 背景
## 目标
## 范围
- 确认需求 / 用户决定及本期验收：
- 本期业务链路与改动边界：
- 必要技术前置及因果依据：
## 非目标
## 现有系统影响
- 只读影响核查的问题、边界与结论：
- 范围外发现及处理（仅记录 / 本期必要且已有授权 / 待确认范围变化）：
## 关键设计依据
| 关键链路 / 决策 | 已知事实及定位 | 设计选择与理由（复用 / 拟新增） | 未决项及影响范围 |
| --- | --- | --- | --- |

定位包含相关仓库 / 路径 / 符号；版本或配置改变结论时标明适用条件。具体接入契约在对应设计段落维护，此处可直接引用，不重复抄字段。

## 前后端一致性策略
## 实施顺序
## 风险与回滚
## 交接结论
- 本轮可交接范围及依据：
- 决定性未决项、受影响任务与补证方式：
- 环境状态引用：`tech/dependency-readiness.md`（与设计是否明确分开记录）
```

## `tech/dependency-readiness.md`

```markdown
# 真实依赖准备清单 — <name>

## 规则
- 只有 `ready` / `not-required` 允许进入 `$pd-fe` / `$pd-be` 正式开发。
- `unknown` / `blocked` / `mock-only` 必须阻断正式开发、联调通过和测试通过。
- 本地真实服务、官方本地容器或测试环境真实服务可算 `ready`；mock server、stub client、fake adapter、contract simulator 必须标为 `mock-only` 并阻断，不算 `ready`。
- 技术实现禁止使用任何 mock；mock / stub / fake / fixture / simulator 只能作为阻断信号记录，不能作为设计、开发、联调、测试或验收通过证据。

## 依赖清单
| 依赖 ID | 类别 | 名称 | 适用 slice | 真实资源 / 地址 | 验证命令 | 状态 | 证据 | 阻断原因 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

状态枚举：

- `ready`: 真实依赖已可用，并有命令、连接、健康检查、版本或配置证据。
- `not-required`: 当前 scope 不需要该依赖，并说明原因。
- `unknown`: 尚未确认依赖是否存在或如何连接。
- `blocked`: 依赖已知不可用，缺账号、配置、网络、服务、版本或数据。
- `mock-only`: 发现 mock / stub / fake / fixture / contract simulator 依赖或实现，不能进入正式开发、联调通过或测试通过。

## `tech/frontend/frontend-design.md`

```markdown
# 前端技术设计 — <name>

## UI 设计系统约束
- MASTER 来源：`ui/ui-design-system.md`
- 产品类型 / 信息密度：
- 视觉气质：
- 组件圆角 / 间距 / 字体 / 颜色：
- 后台 / SaaS / CRM / 操作台约束：
- Page overrides：

## 页面 / 路由
## 组件结构
## 状态模型
## API client / 真实依赖策略
## 权限与可见性
## 错误 / 空态 / 加载态
## 响应式
## 可访问性
## 表单校验 / 错误映射
## UI 验收方式
## 验证方式
```

## `tech/frontend/frontend-component-map.md`

```markdown
# 前端组件映射 — <name>

| Figma / UI 组件 | 前端组件 | 复用 / 新增 | Design System 规则 | Props / 事件 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
```

## `tech/frontend/frontend-route-map.md`

```markdown
# 前端路由映射 — <name>

| 页面 | 路由 | 权限 / 守卫 | 对应 Figma frame | UI 模式 / 信息密度 | 入口 |
| --- | --- | --- | --- | --- | --- |
```

## `tech/frontend/frontend-state-api.md`

状态范围统一按 [UI Quality Checklist](ui-quality-checklist.md#4-适用的状态与交互) 判断，模板记录结果，不重列全量必检状态。

```markdown
# 前端状态与 API — <name>

## 页面：<页面名>
- 页面状态及证据：按 qwerdf-common/ui-quality-checklist.md「适用的状态与交互」记录；共享组件状态引用，不适用说明理由
- 本地状态：
- 服务端状态 / query key：
- API client：
- 真实依赖策略：
- 错误映射：
- 表单校验：
- 响应式 / 移动端：
- 可访问性：
```

## `tech/backend/backend-design.md`

```markdown
# 后端技术设计 — <name>

## 接口
## 关键业务链路
- 对应需求 / 验收及入口：
- 现有调用方 / 提供服务 / 协议与方法全名，或拟新增的归属与契约引用：
- 关键参数来源及返回字段的业务语义 / 单位 / 状态：
- 前置校验、执行顺序、失败 / 空值处理及适用的副作用约束：
- 复用 / 拟修改 / 拟新增位置，依据定位及未确认项：
- 验证方式与可观察结果：

仅列本期关键链路；API / 数据模型引用权威段落，不在各文件复制同一事实表。简单局部修改只说明受影响步骤。

## 服务逻辑
## 数据模型
## 权限校验
## 错误码
## 幂等 / 并发 / 事务
## 日志与观测
## 验证方式
```

## `tech/api-contract.md`

```markdown
# API 契约 — <name>

| API | Method | Path | Request | Response | 状态码 / 错误码 | 权限 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

现有能力引用已核对的协议 / 调用位置，拟新增接口明确标为设计提案并关联实现任务。非 HTTP 接口按实际协议记录 service/method、topic 等，不编造 HTTP Path；关键接入语义与依据可引用 backend-design / tech-plan 的对应段落。
```

## `tech/backend/data-model.md`

```markdown
# 数据模型 — <name>

| 实体 | 字段 | 类型 | 约束 | 来源 | 前端映射 |
| --- | --- | --- | --- | --- | --- |
```

## `tech/backend/sql-execution-plan.md`

```markdown
# SQL 执行计划 — <name>

## 结论
- SQL 执行项：<有 / 无>
- 说明：<不涉及时写明“无 SQL 执行项 / 不涉及”；涉及时概述目的和风险>

## 执行清单
| ID | 类型 | 环境 | SQL / Migration 文件 | 执行时机 | 是否可回滚 | 回滚 SQL / 方案 | 验证方式 | 风险 | 负责人 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 执行顺序
1.

## 提测要求
- 测试环境执行：
- 验证数据 / 命令：
- 未执行风险：

## 上线要求
- 生产执行窗口：
- 前置备份 / 快照：
- 执行后验证：
- 回滚触发条件：
```

## `tech/integration-map.md`

```markdown
# 前后端一致性映射 — <name>

| 页面 / 状态 | 前端字段 / 状态 | API / 后端字段 | 错误码 / 权限 | 真实依赖 / Mock 禁用 | 备注 |
| --- | --- | --- | --- | --- | --- |
```

## `tech/task-slices.md`

```markdown
# 任务切片 — <name>

| ID | 优先级 | 类型 | 状态 | 并行标记 | blocked-by | blocks | 任务 | 验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

列说明：

- 任务说明关联本期需求或必要技术前置的方案段落；范围外影响发现不因出现在技术文档就自动成为开发任务。
- `并行标记` 只表达调度属性，只允许 `parallel-safe`、`serial`、`stage-gate`。禁止写入任务 ID，禁止出现 `blocked-by XXX`、`blocks XXX`、`blocked-by SYNC-001` 等依赖内容。
- `blocked-by` 是当前任务的前置任务 ID 列；`blocks` 是当前任务阻塞的后续任务 ID 列。所有任务 ID 依赖只能写入这两列。
- `-` 表示无依赖，不得和任务 ID 混用。
- `parallel-safe` 只能表示可并行调度，不代表无依赖；真实依赖仍必须写入 `blocked-by` / `blocks`。

依赖一致性：

- 如果 `A.blocked-by` 包含 `B`，则 `B.blocks` 必须包含 `A`。
- 如果 `B.blocks` 包含 `A`，则 `A.blocked-by` 必须包含 `B`。
- 不允许出现只在 `blocks` 单边声明、但对方 `blocked-by` 缺失的关系。
- 不允许出现只在 `blocked-by` 单边声明、但对方 `blocks` 缺失的关系。
- 生成后必须做一次依赖闭环自检；发现不一致时，先修正 `tech/task-slices.md` 再输出。

Frontend / Backend 双向依赖：

- `frontend` / `shared-frontend` slice 默认不依赖 `backend` / `shared-backend` 实现进度；前端实现应基于 `tech/api-contract.md`、`tech/frontend/frontend-state-api.md`、UI 设计系统和前端运行依赖推进。
- 真实后端 API 未完成或真实数据暂不可用，默认写入 `SYNC-*` / `test` 的前置和验证要求，不写入 `FE-* blocked-by BE-*`。
- 只有后端 slice 会先产出前端编码必须消费的具体工程产物时，才允许 `FE-* blocked-by BE-*`，例如 generated client、共享 SDK、schema / type 文件、认证适配文件；必须在“任务”或“验证”列写明产物路径和阶段门理由。
- 如果前端只是在等待后端成功响应，切片应拆成 `FE-*` 与 `BE-*` 并行实现，二者共同 `blocks SYNC-*`，由 `SYNC-*` 验证真实链路。
- 前端实现验证可以覆盖真实 API client、错误态、空态、配置缺失态、服务不可用态和 UI / 构建 / 组件检查；不得用 mock 成功数据作为 `done` 或联调通过证据。
- `backend` / `shared-backend` slice 默认不依赖 `frontend` / `shared-frontend` 实现进度；后端实现应基于 `tech/api-contract.md`、`tech/backend/backend-design.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md` 和真实依赖准备推进。
- 真实前端页面未完成或浏览器链路暂不可用，默认写入 `SYNC-*` / `test` 的前置和验证要求，不写入 `BE-* blocked-by FE-*`。
- 只有前端 slice 会先产出后端编码必须消费的具体工程产物时，才允许 `BE-* blocked-by FE-*`，例如共享 schema / type 包、回调 payload fixture、契约样例文件；必须在“任务”或“验证”列写明产物路径和阶段门理由。
- 如果后端只是在等待前端页面发起真实请求，切片应拆成 `BE-*` 与 `FE-*` 并行实现，二者共同 `blocks SYNC-*`，由 `SYNC-*` 验证真实链路。
- 后端实现验证可以覆盖接口契约、service / repository、权限、错误码、事务、migration、真实下游和后端测试；不得用 fake frontend request 或 fixture-only 成功路径作为端到端通过证据。

`SYNC-*` 建模：

- `SYNC-*` 只能表示前后端真实联调阶段门；执行前相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 必须全部 `done`。
- `SYNC-*` 的 `blocked-by` 应包含它要联调的所有前后端实现任务。
- `SYNC-*` 的 `blocks` 禁止包含 `FE-*`、`BE-*` 或 `shared-*` 开发任务，只允许指向 `test` 或后续非开发门禁任务，或写 `-`。
- `frontend` / `backend` / `shared-*` 开发任务的 `blocked-by` 禁止包含 `SYNC-*`。
- 联调发现的实现问题不预建为 `blocked-by SYNC-*` 的开发任务；由 `$pd-sync` 写成 `implementation-defect` 回已有实现 slice，或写成 `slice-missing` 回 `$pd-plan`。
- `SYNC-*` 的“验证”列必须说明联调范围和通过条件。
- 前端 UI slice 的“验证”列必须包含 UI 质量验证要求，例如桌面 / 移动端、无横向溢出、状态覆盖、表单错误、设计系统一致性或截图 / 浏览器证据。

## `tech/risk-plan.md`

```markdown
# 风险方案 — <name>

| 风险 | 影响 | 触发信号 | 缓解方案 | 回滚方案 |
| --- | --- | --- | --- | --- |
```

## `tech/frontend/frontend-implementation-log.md`

独立 UI finding 的分类与 slice 映射按 [UI finding 修复交接](ui-review-rules.md#6-ui-finding-修复交接) 核对；修复来源直接引用原报告，不复制 finding 正文。

```markdown
# 前端实现记录 — <name>

## Slice
- ID:
- 目标:
- 状态:

## 修复来源（如适用）
- 来源：<原报告路径与 finding ID / 区域；独立 UI 报告可直接引用 ui/ui-review-report.md>
- 问题 ID：
- 类型：<implementation-defect>
- 契约证据：
- 实现证据：

## 变更
## 验证
- 命令 / 方式：
- 结果：
- 证据：
## 阻塞
- 类型：<dependency-readiness | over-constrained-slice | contract-gap | ui-design-gap | none>
- 证据：
- 下一步：
```

## `tech/frontend/frontend-changed-files.md`

```markdown
# 前端变更文件 — <name>

| 文件 | 变更 | 原因 |
| --- | --- | --- |
```

## `tech/frontend/frontend-dev-notes.md`

```markdown
# 前端开发说明 — <name>

## 实现取舍
## API / 真实依赖说明
- 前端实现是否依赖后端进度：<否 / 是，若是必须写明后端产出文件或 SDK 路径>
- 后端未就绪时的处理：<真实 API client + loading / empty / error / permission / service-unavailable；不得 mock 成功数据>
## 待联调点
## 切片建模问题（如适用）
- 类型：<over-constrained-slice | none>
- 被过度阻塞的 FE slice：
- 相关 BE / shared-backend slice：
- 建议回 `$pd-plan` 修正：
```

## `tech/frontend/frontend-acceptance.md`

状态范围与必要证据沿用 [UI Quality Checklist](ui-quality-checklist.md#4-适用的状态与交互) 和 [UI Review Rules](ui-review-rules.md)，不适用与未验证分别记录。

```markdown
# 前端验收清单 — <name>

## 设计系统前置
- [ ] 已读取 `ui/ui-design-system.md`
- [ ] 已对照 `ui/figma-handoff.md`
- [ ] MASTER / Page override 差异已记录

## 页面验收
- [ ] 页面可打开
- [ ] 无 console error
- [ ] 已按共享 UI Quality Checklist「适用的状态与交互」确认本次状态范围；不适用说明理由
- [ ] 适用状态已有证据，共享组件可引用；必要检查未执行时明确记为未验证
- [ ] 核心交互可用
- [ ] 桌面端布局正确
- [ ] 移动端无横向溢出
- [ ] 无文本重叠 / 遮挡
- [ ] 固定栏 / 弹窗 / 抽屉不遮挡关键操作

## 设计还原
- [ ] 结构与 Figma 一致
- [ ] 组件状态与 Figma 一致
- [ ] 间距 / 字号 / 颜色无明显偏差
- [ ] 圆角 / 阴影 / badge / 按钮层级符合设计系统
- [ ] 文案无占位内容
- [ ] 如存在 `ui/ui-review-report.md`，P0/P1 已修复或明确阻断

## UI 质量验证
| 页面 / 状态 | 桌面端证据 | 移动端证据 | 问题 | 处理 |
| --- | --- | --- | --- | --- |
```

## `tech/backend/backend-implementation-log.md`

```markdown
# 后端实现记录 — <name>

## Slice
- ID:
- 目标:
- 状态:

## 修复来源（如适用）
- 来源：<sync/integration-report.md | test/test-report.md | test/code-review.md>
- 问题 ID：
- 类型：<implementation-defect>
- 契约证据：
- 实现证据：

## 变更
## 验证
- 命令 / 方式：
- 结果：
- 证据：
## 阻塞
- 类型：<dependency-readiness | over-constrained-slice | contract-gap | sql-plan-gap | none>
- 证据：
- 下一步：
```

## `tech/backend/backend-changed-files.md`

```markdown
# 后端变更文件 — <name>

| 文件 | 变更 | 原因 |
| --- | --- | --- |
```

## `tech/backend/backend-dev-notes.md`

```markdown
# 后端开发说明 — <name>

## 实现取舍
## API / 数据说明
- 后端实现是否依赖前端进度：<否 / 是，若是必须写明前端产出文件、schema、type 或契约样例路径>
- 前端未就绪时的处理：<接口契约 + service / repository / 权限 / 错误码 / 真实下游 / 后端测试；不得 fake 端到端通过>
## 待联调点
## 切片建模问题（如适用）
- 类型：<over-constrained-slice | none>
- 被过度阻塞的 BE slice：
- 相关 FE / shared-frontend slice：
- 建议回 `$pd-plan` 修正：
```

## `sync/integration-plan.md`

```markdown
# 联调计划 — <name>

| 场景 | 前端入口 | API | 数据准备 | 预期 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
```

## `sync/integration-report.md`

```markdown
# 联调报告 — <name>

## 结论
| Gate | 状态 | 证据 | 下一步 |
| --- | --- | --- | --- |

## 实现前置状态
| Slice | 类型 | 状态 | 证据 | 处理 |
| --- | --- | --- | --- | --- |

## 真实依赖验证
| 依赖 ID | 状态 | 真实资源 / 地址 | 验证方式 | 证据 | 处理 |
| --- | --- | --- | --- | --- | --- |

## Mock 禁用检查
| 区域 | 检查对象 | 结果 | 证据 | 处理 |
| --- | --- | --- | --- | --- |

| 场景 | 结果 | 证据 | 问题 |
| --- | --- | --- | --- |

## 修复路由
| 问题 ID | 分类 | 契约证据 | 实现证据 | 归属 slice | 下一步 | 处理规则 |
| --- | --- | --- | --- | --- | --- | --- |

分类枚举：
- `implementation-defect`: 契约清楚且已有实现 slice 覆盖，但真实代码 / 运行结果不符合契约；回 `$pd-fe` / `$pd-be` 缺陷修复模式。
- `contract-mismatch`: 契约、数据模型、权限或状态枚举本身缺失 / 冲突 / 模糊；回 `$pd-plan`。
- `slice-missing`: 契约清楚但没有实现 slice 覆盖；回 `$pd-plan`。
- `slice-model-invalid`: 任务依赖建模错误，例如开发任务 `blocked-by SYNC-*` 或 `SYNC-* blocks` 开发任务；回 `$pd-plan`。
- `environment-blocked`: 环境、数据、账号、依赖服务或配置导致无法判断；留在 `$pd-sync` / 环境准备。

## 环境
- 前端：
- 后端：
- 数据：
- 未执行项：
```

## `sync/api-mismatch.md`

```markdown
# API 差异 — <name>

| 差异 | 分类 | 前端预期 | 后端实际 | 契约证据 | 实现证据 | 归属 slice | 影响 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## `sync/plan-revision.md`

```markdown
# 技术方案修订 — <name>

## 触发原因
## 影响范围
## 需要修改的契约
## 需要重做的 slice
## 不应由 plan 处理的实现缺陷
## 决策建议
```

## `test/test-plan.md`

```markdown
# 测试计划 — <name>

| 类型 | 范围 | 风险 | 工具 / 命令 | 通过标准 |
| --- | --- | --- | --- | --- |
```

## `test/test-cases.md`

```markdown
# 测试用例 — <name>

| ID | 类型 | 关联验收标准 | 场景 | 步骤 | 预期 |
| --- | --- | --- | --- | --- | --- |
```

## `test/test-report.md`

```markdown
# 测试报告 — <name>

## 联调前置状态
| Gate | 状态 | 证据 | 处理 |
| --- | --- | --- | --- |

| 类型 | 命令 / 方式 | 结果 | 证据 |
| --- | --- | --- | --- |

## SQL 执行验证
| SQL ID | 环境 | SQL / Migration 文件 | 执行状态 | 验证方式 | 证据 | 风险 / 处理 |
| --- | --- | --- | --- | --- | --- | --- |

## 真实依赖验证
| 依赖 ID | 状态 | 真实资源 / 地址 | 验证方式 | 证据 | 处理 |
| --- | --- | --- | --- | --- | --- |

## Mock 禁用检查
| 区域 | 检查对象 | 结果 | 证据 | 处理 |
| --- | --- | --- | --- | --- |

## 未执行 / 未覆盖
| 项目 | 原因 | 风险 | 后续处理 |
| --- | --- | --- | --- |

## Git / ignore 检查
| 检查项 | 命令 / 来源 | 结果 | 处理 |
| --- | --- | --- | --- |

## 提交候选风险
- 应提交候选：
- 应排除候选：
- 可能漏提交：
- 可能多提交：
```

## `test/regression-notes.md`

```markdown
# 回归说明 — <name>

## 覆盖范围
## 未覆盖范围
## 风险
```

## `test/code-review.md`

```markdown
# Code Review — <name>

## 审查范围
- 目标：
- Diff 范围：
- Diff triage 摘要：
- 涉及技术栈：
- 读取的专项 reference：

## 前置证据
| 证据 | 状态 | 路径 / 命令 | 备注 |
| --- | --- | --- | --- |
| UI Review 报告 |  | `ui/ui-review-report.md` |  |
| 联调报告 |  | `sync/integration-report.md` |  |
| 测试报告 |  | `test/test-report.md` |  |
| Diff triage |  | `scripts/diff_triage.py` |  |
| Git diff |  |  |  |
| 实现记录 |  |  |  |

## Findings
| 级别 | 类别 | 文件 / 行号或区域 | 问题 | 影响 | 修复归属 | 建议 | 验证方式 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## UI Review 摘要
| 维度 | 结论 | 证据 / 缺口 |
| --- | --- | --- |
| 独立 UI Review 报告 |  | `ui/ui-review-report.md` |
| 设计系统一致性 |  |  |
| 产品类型匹配 |  |  |
| 信息层级 |  |  |
| 状态覆盖 |  |  |
| 响应式 / 移动端 |  |  |
| 可访问性 |  |  |
| 表单 / 表格 / 图表 |  |  |

## 代码级检查摘要
| 维度 | 结论 | 证据 / 缺口 |
| --- | --- | --- |
| 正确性 |  |  |
| 数据一致性 |  |  |
| 错误处理 |  |  |
| 安全与隐私 |  |  |
| 性能 |  |  |
| 可维护性 / 复用 |  |  |
| 测试质量 |  |  |

## 自动化与人工边界
- 已参考的自动化结果：
- 自动化未执行 / 失败：
- 人工重点审查范围：

## 结论
- 阻断：
- 非阻断建议：
- 残余风险：
- 未覆盖范围：
- 测试缺口：
- 下一步：
```

## `release/commit-summary.md`

```markdown
# Commit Summary — <name>

## Readiness gates
| Gate | 状态 | 证据 | 阻断 / 下一步 |
| --- | --- | --- | --- |

## Git state
## Gitignore check
## Planned files
## Excluded files
## Possible missing files
## Possible extra files
## Commit message
## Summary
## Tests
## Known risks
```

## `release/pr-description.md`

```markdown
# PR / MR Description — <name>

## What changed
## Why
## Validation
## Risks
## Rollback
```

## `release/release-plan.md`

```markdown
# 上线计划 — <name>

## 上线范围
## 前置条件
## SQL / 数据变更执行计划
| SQL ID | 环境 | SQL / Migration 文件 | 执行时机 | 前置备份 | 验证方式 | 回滚方案 |
| --- | --- | --- | --- | --- | --- | --- |
## 步骤
## 验证
## 负责人 / 依赖
```

## `release/release-checklist.md`

```markdown
# 上线检查清单 — <name>

- [ ] 测试报告已通过
- [ ] Code Review 无 P0/P1
- [ ] SQL 执行计划已确认；无 SQL 时已明确“不涉及”
- [ ] 涉及 SQL / migration 时，测试环境执行和验证证据已记录
- [ ] 涉及 SQL / migration 时，生产执行顺序、备份、验证和回滚方案已确认
- [ ] 回滚方案已确认
- [ ] 监控 / 日志检查点已确认
```

## `release/rollback-plan.md`

```markdown
# 回滚方案 — <name>

## 回滚触发条件
## 回滚步骤
## 数据处理
- SQL / 数据回滚：
## 验证
```

## `release/release-notes.md`

```markdown
# Release Notes — <name>

## 用户可见变化
## 内部变化
## 已知风险
```
