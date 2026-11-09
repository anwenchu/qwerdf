---
name: pd-sync
description: >-
  前后端联调工作流，基于前端实现、后端实现、已确认契约和方案中的接线映射 检查接口、字段、状态码、错误结构、权限、分页、状态页、真实依赖接入和 Mock 禁用；发现契约问题时记录差异并回原方案修订，不直接修代码。Use when the user mentions $pd-sync、pd-sync、前后端联调、接口联调、API联调、真实接口联调、Mock禁用检查。
---

# $pd-sync — 前后端联调

验证前后端实现是否符合统一契约。

## 读取

默认从需求、方案、任务三份主文档的相关章节恢复上下文。下列旧分文件仅在已存在且是有效事实源、或确需独立消费时读取；同样内容已在主文档时不补建文件、不复制正文。真正缺失的契约 / 输入 / 证据仍保留缺口。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage sync`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出只含 `sync/integration-report.md`；计划、场景、差异、证据及修复路由在同一报告维护，不默认再生成计划、差异及修订三份文件。
3. 读取技术方案的契约、接线、真实输入及任务中的实现 / 验证证据；独立 API 契约或既有分文件事实源存在时定向引用。
   任务覆盖、归属、顺序及状态从 [共享规则](../qwerdf-common/product-delivery-flow.md#任务清单与开发顺序) 确认的权威源读取；先处理来源冲突或滞后视图，不能仅因 Markdown 缺行就判 `slice-missing`。
4. 识别本地前端、后端启动方式和环境配置。
5. 按 [共享目录规则](../qwerdf-common/product-delivery-flow.md#2-默认工作目录) 先确定本次独立任务根目录，以下阶段路径相对于该目录。

## 边界

- 本阶段不改代码、契约或数据模型；执行条件、真实依赖要求、修复分类与回退统一按 [共享验证规则](../qwerdf-common/product-delivery-flow.md#验证与审查) 和 [联调与验收交接规则](../qwerdf-common/product-delivery-flow.md#联调与验收交接)。
- 真实证据按当前场景实际依赖核对：需要数据库 / 下游时不可缺少真实调用，项目无此依赖不强加；相对路径 / 同源路由须有真实请求目标与运行证据，不要求额外绝对 base URL。
- 静态公开内容且无跨端交互可说明联调不适用及依据；应动态查询却写死的数据、mock client / server、stub、fake、fixture-only 或 simulator 仍阻断真实联调通过。
- 只启动或连接本次获准环境，账号 / 订单 / 资金 / SQL 操作不因联调自动获权。不能执行时记录具体影响，允许后续独立测试或只读审查，不宣称完整联调通过或可提交。

## 流程

1. 从已确认的权威任务源及联调 / 测试范围核对业务结果、相关实现与必要准备；视图缺行先核对来源。任务归属 / 顺序不可执行记 slice-model-invalid 回 `$pd-plan`；相关实现未完成则记录 ID 与归属，停止该正式联调场景，不扩大为无关任务等待，也不因没有独立 SYNC 任务或依赖列而拒绝联调。
2. 按场景核对方案中的真实输入章节或已确认的独立事实源：实际必需输入须 ready / not-required 且有依据，unknown / blocked / mock-only 不可放行；无跨端交互的范围记录不适用，不启动无用环境。
3. 在 `sync/integration-report.md` 的计划章节维护场景、入口、API、真实资源、数据准备及预期；按共享验证规则核对并引用仍有效的证据，集中补验本轮真实联调缺口，不用局部开发检查替代真实场景。连接可用环境，先侦察渲染态 / API 再执行交互断言。
4. 检查 path、method、request / response、状态码、错误结构、权限、分页、状态页与真实调用。核查 client、repository、配置、日志及请求目标，确认生产路径无模拟替代；名称只作线索，不能因普通静态内容就判 mock。
5. 在 `sync/integration-report.md` 记录实现前置、真实依赖验证、Mock 禁用检查、单场景结果、未执行范围与证据。实现 done 不等于真实链路通过，连接成功也不等于接口验收。
6. 按共享分类给每个阻断写修复路由、证据和归属：contract-mismatch / slice-missing / slice-model-invalid 回 `$pd-plan` 在同一报告记录差异并交回原方案 / 契约修订；implementation-defect 回已有端 slice；environment-blocked 记录具体恢复入口。契约正确的实现错误不靠改方案掩盖；归属不明先核实，不让开发凭空造任务。

## 输出摘要

```text
联调完成: <name>
目录: <output-dir>
文件:
  - sync/integration-report.md
结论: <通过 / 不适用及依据 / implementation-defect / contract-mismatch / slice-missing / slice-model-invalid / environment-blocked>
下一步: <通过则用 $pd-test；实现缺陷回 $pd-fe / $pd-be 并注明归属 slice；契约或切片问题回 $pd-plan；环境问题继续 $pd-sync>
```
