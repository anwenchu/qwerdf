# Engineering Artifact Contracts

本文件定义工程阶段 skill 共享的产物模板。Skill 执行时只读取本任务需要的模板。

## `tech-plan.md`

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

## `frontend-design.md`

```markdown
# 前端技术设计 — <name>

## 页面 / 路由
## 组件结构
## 状态模型
## API client / mock 策略
## 权限与可见性
## 错误 / 空态 / 加载态
## 响应式
## 验证方式
```

## `frontend-component-map.md`

```markdown
# 前端组件映射 — <name>

| Figma / UI 组件 | 前端组件 | 复用 / 新增 | Props / 事件 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
```

## `frontend-route-map.md`

```markdown
# 前端路由映射 — <name>

| 页面 | 路由 | 权限 / 守卫 | 对应 Figma frame | 入口 |
| --- | --- | --- | --- | --- |
```

## `frontend-state-api.md`

```markdown
# 前端状态与 API — <name>

## 页面：<页面名>
- 页面状态：default / loading / empty / error / permission
- 本地状态：
- 服务端状态 / query key：
- API client：
- Mock 策略：
- 错误映射：
```

## `backend-design.md`

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

## `api-contract.md`

```markdown
# API 契约 — <name>

| API | Method | Path | Request | Response | 状态码 / 错误码 | 权限 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

## `data-model.md`

```markdown
# 数据模型 — <name>

| 实体 | 字段 | 类型 | 约束 | 来源 | 前端映射 |
| --- | --- | --- | --- | --- | --- |
```

## `integration-map.md`

```markdown
# 前后端一致性映射 — <name>

| 页面 / 状态 | 前端字段 / 状态 | API / 后端字段 | 错误码 / 权限 | Mock | 备注 |
| --- | --- | --- | --- | --- | --- |
```

## `task-slices.md`

```markdown
# 任务切片 — <name>

| ID | 优先级 | 类型 | 状态 | 并行标记 | blocked-by | blocks | 任务 | 验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## `risk-plan.md`

```markdown
# 风险方案 — <name>

| 风险 | 影响 | 触发信号 | 缓解方案 | 回滚方案 |
| --- | --- | --- | --- | --- |
```

## `frontend-implementation-log.md`

```markdown
# 前端实现记录 — <name>

## Slice
- ID:
- 目标:
- 状态:

## 变更
## 验证
- 命令 / 方式：
- 结果：
- 证据：
## 阻塞
```

## `frontend-changed-files.md`

```markdown
# 前端变更文件 — <name>

| 文件 | 变更 | 原因 |
| --- | --- | --- |
```

## `frontend-dev-notes.md`

```markdown
# 前端开发说明 — <name>

## 实现取舍
## API / mock 说明
## 待联调点
```

## `frontend-acceptance.md`

```markdown
# 前端验收清单 — <name>

## 页面验收
- [ ] 页面可打开
- [ ] 无 console error
- [ ] default / loading / empty / error / permission 状态可验证
- [ ] 核心交互可用
- [ ] 桌面端布局正确
- [ ] 移动端无横向溢出

## 设计还原
- [ ] 结构与 Figma 一致
- [ ] 组件状态与 Figma 一致
- [ ] 间距 / 字号 / 颜色无明显偏差
- [ ] 文案无占位内容
```

## `backend-implementation-log.md`

```markdown
# 后端实现记录 — <name>

## Slice
- ID:
- 目标:
- 状态:

## 变更
## 验证
- 命令 / 方式：
- 结果：
- 证据：
## 阻塞
```

## `backend-changed-files.md`

```markdown
# 后端变更文件 — <name>

| 文件 | 变更 | 原因 |
| --- | --- | --- |
```

## `backend-dev-notes.md`

```markdown
# 后端开发说明 — <name>

## 实现取舍
## API / 数据说明
## 待联调点
```

## `integration-plan.md`

```markdown
# 联调计划 — <name>

| 场景 | 前端入口 | API | 数据准备 | 预期 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
```

## `integration-report.md`

```markdown
# 联调报告 — <name>

| 场景 | 结果 | 证据 | 问题 |
| --- | --- | --- | --- |

## 环境
- 前端：
- 后端：
- 数据：
- 未执行项：
```

## `api-mismatch.md`

```markdown
# API 差异 — <name>

| 差异 | 前端预期 | 后端实际 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
```

## `plan-revision.md`

```markdown
# 技术方案修订 — <name>

## 触发原因
## 影响范围
## 需要修改的契约
## 需要重做的 slice
## 决策建议
```

## `test-plan.md`

```markdown
# 测试计划 — <name>

| 类型 | 范围 | 风险 | 工具 / 命令 | 通过标准 |
| --- | --- | --- | --- | --- |
```

## `test-cases.md`

```markdown
# 测试用例 — <name>

| ID | 类型 | 关联验收标准 | 场景 | 步骤 | 预期 |
| --- | --- | --- | --- | --- | --- |
```

## `test-report.md`

```markdown
# 测试报告 — <name>

| 类型 | 命令 / 方式 | 结果 | 证据 |
| --- | --- | --- | --- |

## 未执行 / 未覆盖
| 项目 | 原因 | 风险 | 后续处理 |
| --- | --- | --- | --- |
```

## `regression-notes.md`

```markdown
# 回归说明 — <name>

## 覆盖范围
## 未覆盖范围
## 风险
```

## `code-review.md`

```markdown
# Code Review — <name>

| 级别 | 文件 / 区域 | 问题 | 影响 | 建议 | 证据 |
| --- | --- | --- | --- | --- | --- |

## 结论
- 阻断：
- 残余风险：
- 测试缺口：
```

## `commit-summary.md`

```markdown
# Commit Summary — <name>

## Planned files
## Commit message
## Summary
## Tests
```

## `pr-description.md`

```markdown
# PR / MR Description — <name>

## What changed
## Why
## Validation
## Risks
## Rollback
```

## `release-plan.md`

```markdown
# 上线计划 — <name>

## 上线范围
## 前置条件
## 步骤
## 验证
## 负责人 / 依赖
```

## `release-checklist.md`

```markdown
# 上线检查清单 — <name>

- [ ] 测试报告已通过
- [ ] Code Review 无 P0/P1
- [ ] 回滚方案已确认
- [ ] 监控 / 日志检查点已确认
```

## `rollback-plan.md`

```markdown
# 回滚方案 — <name>

## 回滚触发条件
## 回滚步骤
## 数据处理
## 验证
```

## `release-notes.md`

```markdown
# Release Notes — <name>

## 用户可见变化
## 内部变化
## 已知风险
```
