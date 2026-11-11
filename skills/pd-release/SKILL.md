---
name: pd-release
description: >-
  上线文档工作流，基于 PRD、技术方案、SQL 执行计划、实现记录、联调报告、测试报告、Code Review 和提交说明在一份 release notes 中维护上线计划、检查、回滚和风险；不接平台、不执行部署。Use when the user mentions $pd-release、pd-release、上线文档、发布计划、上线计划、回滚方案、release notes、上线SQL、数据库变更上线。
---

# $pd-release — 上线文档

生成上线前材料，不执行真实部署。

## 读取

默认从需求、方案、任务三份主文档的相关章节恢复上下文。下列旧分文件仅在已存在且是有效事实源、或确需独立消费时读取；同样内容已在主文档时不补建文件、不复制正文。真正缺失的契约 / 输入 / 证据仍保留缺口。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage release`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出只含 `release/release-notes.md`；发布计划、检查和回滚在同一文件维护。既有运维消费者确需独立材料时才按需读取相应旧模板。
3. 必须读取 `sync/integration-report.md`、`test/test-report.md`、`test/code-review.md` 及适用的 `tech/backend/sql-execution-plan.md`。
4. 读取 PRD、技术方案、实现记录和提交说明。
5. 按 [共享目录规则](../qwerdf-common/product-delivery-flow.md#2-默认工作目录) 先确定本次独立任务根目录，以下阶段路径相对于该目录。

## 边界

- 不接 GitHub Release、GitLab、GitOps、Lark 或其他平台。
- 不执行部署。
- 不 push。
- 缺少 `sync/integration-report.md`、`test/test-report.md`、`test/code-review.md` 或适用 SQL 的执行计划时，不得声称可以上线。
- 存在 P0/P1、失败测试、未解释的契约差异或缺少回滚路径时，结论必须写成有阻断风险。
- `tech/backend/sql-execution-plan.md` 存在 SQL 执行项但缺少测试环境执行证据、生产执行顺序、必要备份、执行后验证或回滚方案时，结论必须写成有阻断风险。
- 用户要求时可依据项目实际配置编写平台命令草案，未知参数明确待补；本阶段不执行命令、不部署，不要求另建 skill。

## 发布状态采集

生成上线材料前先确认：

1. 目标环境、发布范围和是否用户可见。
2. 关联 commit / PR / MR 是否明确；如不明确，写成待确认。
3. 测试报告、联调报告、Code Review 是否有阻断项。
4. 技术方案是否明确独立 SQL 执行项的适用性及依据；涉及此类项时，执行计划是否列全顺序、环境、验证和回滚；不因应用查询存在 SQL 就增加发布执行项。
5. 回滚路径是否真实可执行，是否涉及数据迁移或不可逆操作。
6. 监控、日志、告警、人工验收点和上线窗口是否明确。

## 流程

1. 采集发布状态，按共享正式上线规则检查测试、联调通过 / 有依据不适用、Code Review 和适用 SQL 执行计划，核对原生报告及当前版本对应的验证层级 / 范围、未执行项与审查实际状态，确认无 P0/P1、失败测试、契约阻断和未关闭 SQL 风险；开发阶段无需旧版本兼容时不额外发明过渡方案。
2. 在 `release/release-notes.md` 维护变更说明、发布范围 / 版本 / 环境、执行顺序、检查与监控、适用 SQL / 数据变更和必要备份。
3. 在同一文件写明回滚触发条件、可执行路径、数据影响、风险及人工确认；不可逆操作明确标风险，不用摘要替代必要执行细节。实际运维已有独立计划 / 回滚消费者时引用其唯一材料，不重复维护。
4. 输出上线风险和未决项；不执行部署或其他未获准操作。

## 输出摘要

```text
上线文档完成: <name>
目录: <output-dir>
文件:
  - release/release-notes.md
结论: <可进入上线审批 / 缺少验证 / 有阻断风险>
```
