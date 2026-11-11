# 隔离工作流评估输入

各请求独立处理。仅在临时工作区生成材料，不接外部服务，不修改本输入。代码和记录均为合成材料。

## 请求 A

使用 `$pd-review` 审查下面工单关闭功能及其测试。只读，给出有源码依据的 findings、证据范围与后续处理，不修改代码。

确认需求：本租户工单仅管理员或当前处理人可以关闭，且状态必须为 OPEN；关闭记录操作者，成功后详情返回 CLOSED 和 audit_ref。发起人的个人资料是否完整不影响关闭。重复提交同一 request_id 返回原成功结果；其他租户不返回工单内容。

作者记录：本次关闭路径和 audit_ref 已修好，两个单测通过，可以提交。测试使用内存替身，真实数据库及 API 服务未运行。工作区没有其他测试报告 / 独立审查证据。

```python
# tickets.py
from dataclasses import dataclass

@dataclass
class Ticket:
    tenant_id: int
    assignee_id: int
    status: str
    reporter_profile_complete: bool
    audit_ref: str | None = None

def close(ticket, actor, request_id, repo):
    if ticket.tenant_id != actor.tenant_id:
        raise LookupError('not found')
    if actor.role != 'ADMIN' and ticket.assignee_id != actor.id:
        raise PermissionError('forbidden')
    previous = repo.by_request_id(request_id)
    if previous:
        return previous
    if ticket.status != 'OPEN':
        raise ValueError('state conflict')
    if not ticket.reporter_profile_complete:
        raise ValueError('profile incomplete')
    repo.close_and_audit(ticket, actor.id, request_id)
    return repo.detail(ticket)

# mapper.py: used by the actual repository detail method
DETAIL_SQL = 'SELECT tenant_id, assignee_id, status, reporter_profile_complete FROM ticket WHERE id = ?'
def map_detail(row):
    return Ticket(row['tenant_id'], row['assignee_id'], row['status'], row['reporter_profile_complete'])

# tests/test_close.py: both reported as passing with an in-memory repository
# test_close_success provides reporter_profile_complete=True and
# repo.detail returns Ticket(7, 11, 'CLOSED', True, audit_ref='audit-101').
# test_close_incomplete expects ValueError('profile incomplete') for False.
```

## 请求 B

使用 `$pd-test` 整理当前验证结论，不修业务代码。以上实现的单元测试用内存 repository，执行 2、失败 0、错误 0、跳过 0。只有上述作者摘要，没有可回查的原生报告。真实数据库不可用；此环境没有启动 API，也没有获准执行 SQL。判断能证明什么、还需什么，不替用户安装依赖或开启服务。

## 请求 C

使用 `$pd-plan` 检查一个静态帮助页面文案修订计划，只在回复给建议，不修改文件。项目规定 `TODO.md` 是唯一任务权威源，已删除 task-slices、JSON 和生成器；当前 TODO 有文案更新及必要页面检查两项。修订只把“提交后请等待”改为“提交后可在历史记录查看结果”，交互、接口、权限不变，已确认产品支持历史记录。不涉及数据库 / API 接入或新框架。现有设计系统与页面模板继续沿用。
