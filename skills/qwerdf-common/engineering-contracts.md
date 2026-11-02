# Engineering Artifact Contracts

本文件定义工程阶段 skill 共享的产物模板。Skill 执行时只读取本任务需要的模板。依据、范围与交接判断统一见 [技术设计依据与范围规则](technical-design-rules.md)；按本轮风险选用下列记录，不为局部修订重做无关历史材料。

当前产物职责以 [阶段产物表](product-delivery-flow.md#1-交付链路) 为准；规模评估、证据留存、短记录及续作入口统一按 [生命周期规则](artifact-lifecycle.md) 处理，不把以下模板展开成逐轮日志副本。

## 业务进度摘要

前后端实现记录及输出摘要共用以下结构；解释与完成口径统一按 [共享业务推进规则](product-delivery-flow.md#业务推进阻断恢复与进度汇报)，只填本轮适用范围，不复制整份需求或另算整体百分比。

```markdown
- 本轮目标：<里程碑 / 验收引用；目标 slice>
- 已实现与调用接线：<入口、关键状态变化、实际接入位置与仍未接通部分>
- 验证：<已执行的本端检查及证据；真实链路已验证 / 未验证及依据>
- 剩余与阻断：<未实现 / 未接线；契约缺口；依赖或验证阻塞，分别给位置、影响与下一步>
- 任务清单：<权威源及 tech/task-slices.md 视图；按权威源列本端 done / in_progress / pending / blocked 的计数与 ID；代码已完成但待验证的项单独指出，派生视图滞后时注明>
- 继续或结束依据：<连续执行时下一项 ID 与接下来的动作；结束时逐项说明剩余项为何无获准可执行动作，或引用用户限定 / 暂停要求>
```

恢复 blocked 时，在原实现记录保留原阻断，并补解除证据、当前交接 / 依赖复核及状态变更；不新造恢复报告。

## `tech/tech-plan.md`

```markdown
# 技术方案 — <name>

## 背景
## 目标
## 范围
- 确认需求 / 用户决定及本期验收：
- 本期业务链路与改动边界：
- 适用性：<前端 / 后端 / UI / 联调 / SQL；不适用的依据，引用受影响范围>
- 必要技术前置及因果依据：
## 非目标
## 仓库、分支与二方包版本
| 修改仓库 / 路径 | 本轮改动及归属 | 已确认开发分支 | 确认依据 | 二方包开发版本 / 不涉及 | 受影响消费者 |
| --- | --- | --- | --- | --- | --- |

- 只读参考仓库：<仅作依据，不属于本轮修改清单>

## 现有系统影响
- 只读影响核查的问题、边界与结论：
- 范围外发现及处理（仅记录 / 本期必要且已有授权 / 待确认范围变化）：
## 关键设计依据
| 关键链路 / 决策 | 已知事实及定位 | 设计选择与理由（复用 / 拟新增） | 未决项及影响范围 |
| --- | --- | --- | --- |

定位包含相关仓库 / 路径 / 符号；版本或配置改变结论时标明适用条件。具体接入契约在对应设计段落维护，此处可直接引用，不重复抄字段。

## 前后端一致性策略
## 实施顺序
- 业务里程碑：<本期验收引用、入口与关键状态变化、业务结果、必要契约 / 依赖及验证信号>
- 关联任务及优先推进顺序：<引用 task-slices；局部修复沿用既有目标>
## 风险与回滚
## 交接结论
- 本次设计核查范围、所依据的验收 / 设计段落与结论：
- 本轮可交接范围及依据：
- 决定性未决项、受影响任务与补证方式：
- 修订时旧结论及相关 contract / 实现任务状态的处理（无变动可注明）：
- 环境状态引用：`tech/dependency-readiness.md`（与设计是否明确分开记录）
```

## `tech/dependency-readiness.md`

填写时按 [共享开发门禁](product-delivery-flow.md#开发交接与依赖)、[并行规则](product-delivery-flow.md#frontend--backend-并行开发规则) 及 [阻断恢复](product-delivery-flow.md#业务推进阻断恢复与进度汇报) 判断，每项说明用途和消费者，不复制门禁正文。

```markdown
# 真实依赖准备清单 — <name>

## 判断依据
- 当前适用依据：<引用本轮技术方案与实际依赖证据，区分编码 / 验证用途>

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

默认作为任务权威源；已有 JSON 机器消费时也可作为派生视图。来源选择、冲突处理、任务粒度、完成证据与持续回填统一按 [共享任务清单规则](product-delivery-flow.md#任务清单与开发顺序) 执行，不在两种格式独立维护状态。

```markdown
# 任务切片 — <name>

任务来源：<权威源路径；默认本文件，使用已有 JSON 时明确其路径及本文件为派生视图>
派生方式与同步情况（仅多格式共存时）：<沿用的生成方式；与源一致 / 滞后及受影响项，不把旧视图当当前状态>

## 前端任务

| 顺序 | ID | 业务动作与交付结果 | 状态 | 完成标准 | 证据 / 阻断 |
| --- | --- | --- | --- | --- | --- |

## 后端任务

| 顺序 | ID | 业务动作与交付结果 | 状态 | 完成标准 | 证据 / 阻断 |
| --- | --- | --- | --- | --- | --- |

## 联调 / 测试范围
- 业务结果与关联实现 ID：
- 实际必需输入与通过条件：<引用原验收；开发状态读取上方权威条目，不再抄一份>
```

填写与执行只按 [共享任务清单与开发顺序](product-delivery-flow.md#任务清单与开发顺序) 及 [并行开发规则](product-delivery-flow.md#frontend--backend-并行开发规则)。任务记录或引用输入 / 契约、可观察结果、本端接线、必要异常 / 安全边界和最小验证，不复制设计全文。JSON 为权威源时表内顺序和状态均从该源派生；未涉及的端说明依据，不造空任务。UI 任务的状态、平台及证据要求引用共享质量清单。

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
- 业务里程碑 / 验收引用:

## 业务推进
按本文件 [业务进度摘要](#业务进度摘要) 填写。

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
- 类型：<dependency-readiness | contract-gap | ui-design-gap | none>
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
- 本端工程前置 / 共享产物：<仅列实际消费的具体产物与准备任务；边界按共享并行开发规则，不填写等待对端业务实现>
- 后端未就绪时的处理：<真实 API client + loading / empty / error / permission / service-unavailable；不得 mock 成功数据>
## 待联调点
## 顺序 / 归属问题（仅有实际问题时）
- 受影响任务与证据：
- 需回 `$pd-plan` 校正的顺序 / 输入说明：
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
- 业务里程碑 / 验收引用:

## 业务推进
按本文件 [业务进度摘要](#业务进度摘要) 填写。

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
- 类型：<dependency-readiness | contract-gap | sql-plan-gap | none>
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
- 本端工程前置 / 共享产物：<仅列实际消费的具体产物与准备任务；边界按共享并行开发规则，不填写等待对端业务实现>
- 前端未就绪时的处理：<接口契约 + service / repository / 权限 / 错误码 / 真实下游 / 后端测试；不得 fake 端到端通过>
## 待联调点
## 顺序 / 归属问题（仅有实际问题时）
- 受影响任务与证据：
- 需回 `$pd-plan` 校正的顺序 / 输入说明：
```

## `sync/integration-plan.md`

```markdown
# 联调计划 — <name>

| 场景 | 前端入口 | API | 数据准备 | 预期 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
```

## `sync/integration-report.md`

分类与修复路径按 [共享验证规则](product-delivery-flow.md#验证与审查)；slice-missing 从确认的权威源判断，先排除视图滞后。

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

## 本轮验证范围与整体结论
- 范围与适用性依据：
- 单项结果：<见下表，不外推未执行路径>
- 整体结论：<通过 / 未通过 / 未执行 / 有残余风险及依据；正式门禁沿用共享规则>

## 联调前置状态
| Gate | 状态 | 证据 | 处理 |
| --- | --- | --- | --- |

| 类型 | 命令 / 方式 | 结果 | 证据 |
| --- | --- | --- | --- |

## SQL 执行验证
不涉及可引用技术方案依据；涉及但缺执行计划或真实验证时保留缺口，不伪称通过。

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
- [ ] SQL 适用性有依据；涉及时执行计划与必要验证已确认，无 SQL 时引用技术方案的“不涉及”说明
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
