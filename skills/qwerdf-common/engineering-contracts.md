# Engineering Artifact Contracts

本文件定义工程阶段 skill 共享的产物模板。Skill 执行时只读取本任务需要的模板。

## `tech/tech-plan.md`

```markdown
# 技术方案 — <name>

## 背景
## 目标
## 范围
## 非目标
## 现有系统影响
## 前后端一致性策略
## 实施顺序
## 风险与回滚
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

```markdown
# 前端状态与 API — <name>

## 页面：<页面名>
- 页面状态：default / loading / empty / error / permission
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

`SYNC-*` 建模：

- `SYNC-*` 的 `blocked-by` 应包含它要联调的所有前后端实现任务。
- `SYNC-*` 的 `blocks` 只应包含确实需要联调结果作为阶段门的后续任务。
- `frontend` / `backend` 开发任务默认依赖具体 `C-*`、`FE-*`、`BE-*` 前置任务；只有后续开发必须基于已通过真实联调的契约、字段、数据、错误码或端到端行为时，才允许依赖 `SYNC-*`。
- 如果 `SYNC-*` 只是验证建议，写入“验证”列或并行建议，不写入 `blocked-by`。
- 被 `SYNC-*` 阻塞的开发任务必须在任务描述或“验证”列说明阶段门理由。
- `SYNC-*` 的“验证”列必须说明联调范围和通过条件。
- 前端 UI slice 的“验证”列必须包含 UI 质量验证要求，例如桌面 / 移动端、无横向溢出、状态覆盖、表单错误、设计系统一致性或截图 / 浏览器证据。

## `tech/risk-plan.md`

```markdown
# 风险方案 — <name>

| 风险 | 影响 | 触发信号 | 缓解方案 | 回滚方案 |
| --- | --- | --- | --- | --- |
```

## `tech/frontend/frontend-implementation-log.md`

```markdown
# 前端实现记录 — <name>

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
## 待联调点
```

## `tech/frontend/frontend-acceptance.md`

```markdown
# 前端验收清单 — <name>

## 设计系统前置
- [ ] 已读取 `ui/ui-design-system.md`
- [ ] 已对照 `ui/figma-handoff.md`
- [ ] MASTER / Page override 差异已记录

## 页面验收
- [ ] 页面可打开
- [ ] 无 console error
- [ ] default / loading / empty / error / permission 状态可验证
- [ ] saving / submitting / disabled 状态可验证
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
## 待联调点
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
