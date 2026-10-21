#!/usr/bin/env python3
"""Read stage-specific context and check product artifacts. Python 3.10+, stdlib only.

This is a completeness/reference checker, not a judge of product truth or value.
It never writes artifacts or marks a business decision as approved.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


COMMON = Path(__file__).resolve().parents[1]
ARTIFACTS = {
    "vet": ("product/idea-brief.md", "product/user-problem.md", "product/competitor-notes.md",
            "product/mvp-hypothesis.md", "product/validation-questions.md"),
    "prd": ("product/prd.md", "product/requirements.md", "product/user-stories.md",
            "product/acceptance-criteria.md", "product/open-questions.md"),
    "blueprint": ("product/product-brief.md", "ui/ui-design-system.md", "ui/ui-flows.md",
                  "ui/ui-pages.md", "ui/ui-screens.md", "ui/ui-components.md"),
    "ui-review": ("ui/ui-review-report.md",),
}
LIMITATION = "仅检查材料完整性与引用一致性；来源真实性、需求合理性和业务语义仍需审阅。"


def visible_lines(text: str) -> list[tuple[int, str]]:
    """Ignore fenced examples and HTML comments; retain original line numbers."""
    lines = []
    fence = None
    comment = False
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        if comment:
            if "-->" not in line:
                continue
            line = line.split("-->", 1)[1]
            comment = False
        while "<!--" in line:
            before, after = line.split("<!--", 1)
            if "-->" not in after:
                line, comment = before, True
                break
            line = before + after.split("-->", 1)[1]
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            fence = match[1]
            continue
        if not line.startswith(("    ", "\t")):
            lines.append((number, line))
    return lines


def section(text: str, title: str, *, children: bool = True) -> str:
    """Select a real Markdown section, never a heading inside a fenced example."""
    level = len(title) - len(title.lstrip("#"))
    start = None
    end = len(text.splitlines())
    for number, line in visible_lines(text):
        if start is None:
            if line.strip() == title:
                start = number - 1
        elif re.match(r"^#{1,6} ", line):
            next_level = len(line) - len(line.lstrip("#"))
            if not children or next_level <= level:
                end = number - 1
                break
    if start is None:
        raise ValueError(f"缺少章节 {title}")
    return "\n".join(text.splitlines()[start:end]).strip()


def stage_context(stage: str) -> str:
    flow = (COMMON / "product-delivery-flow.md").read_text(encoding="utf-8")
    templates = (COMMON / "artifact-contracts.md").read_text(encoding="utf-8")
    selected = [section(flow, "## 2. 默认工作目录", children=False),
                section(flow, "## 3. Skill 执行规范", children=False),
                section(flow, "### 产品事实与参考使用 Gate"),
                section(flow, "## 4. 安全与意外最小化"),
                section(flow, "## 6. 外部生命周期边界")]
    if stage == "blueprint":
        selected.append(section(flow, "### UI 设计系统与质量 Gate"))
        selected.append(section(flow, "### UI 职责边界"))
    selected.extend(section(templates, f"## `{path}`") for path in ARTIFACTS[stage])
    return "\n\n".join([f"# {stage} 阶段上下文\n\n规则源：product-delivery-flow.md；模板源：artifact-contracts.md。",
                           *selected]) + "\n"


def substantive(value: str) -> bool:
    if re.fullmatch(r"\s*<[^>]+>\s*", value):
        return False
    cleaned = re.sub(r"[`*_\[\]<>]", "", value).strip()
    return bool(cleaned) and not re.fullmatch(
        r"TODO|TBD|待补充|待填写|待确认|未提供|未确定|占位|[-—/]+|\.\.\.", cleaned, re.I)


def has_table_data(text: str) -> bool:
    separator = False
    for _, line in visible_lines(text):
        if not line.strip().startswith("|"):
            separator = False
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            separator = True
        elif separator and any(substantive(cell) for cell in cells):
            return True
    return False


def has_content(text: str) -> bool:
    prose = [line for _, line in visible_lines(text)
             if line.strip() and not re.match(r"^\s*(#|\|)", line)]
    return has_table_data(text) or any(
        substantive(line) and not re.fullmatch(r"[-* ]*[^:：]+[:：]\s*", line)
        for line in prose)


def rows(text: str, columns: tuple[str, ...], *, consumed: set[int] | None = None) -> list[tuple[int, dict[str, str]]]:
    """Read a pipe table; optionally record recognized header/separator/data lines."""
    result = []
    header = None
    for number, line in visible_lines(text):
        if not line.strip().startswith("|"):
            header = None
            continue
        body = line.strip()[1:]
        if body.endswith("|") and not body.endswith(r"\|"):
            body = body[:-1]
        cells = [cell.replace(r"\|", "|").strip().strip("`*")
                 for cell in re.split(r"(?<!\\)\|", body)]
        names = {re.sub(r"\s", "", column): column for column in columns}
        normalized = [names.get(re.sub(r"\s", "", cell), cell) for cell in cells]
        if set(columns).issubset(normalized):
            header = normalized
            if consumed is not None:
                consumed.add(number)
            continue
        if header is None:
            continue
        if consumed is not None:
            consumed.add(number)
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        # Preserve malformed rows so they fail rather than silently disappearing.
        values = dict(zip(header, cells)) if len(cells) == len(header) else {}
        result.append((number, values or {column: "" for column in columns}))
    return result


def validate(root: Path, stage: str) -> dict:
    issues = []
    warnings = []
    documents = {}
    paths = {}
    legacy = []

    def issue(path: str, line: int, code: str, message: str) -> None:
        issues.append({"file": str(paths.get(path, root / path)), "line": line,
                       "code": code, "message": message})

    def warn(path: str, line: int, code: str, message: str, *, review: bool = True) -> None:
        warnings.append({"file": str(paths.get(path, root / path)), "line": line,
                         "code": code, "message": message, "requires_review": review})

    for relative in ARTIFACTS[stage]:
        path = root / relative
        if not path.exists() and (root / Path(relative).name).is_file():
            path = root / Path(relative).name
            legacy.append(str(path))
        paths[relative] = path
        if not path.is_file():
            warn(relative, 1, "missing-file", "未找到此产物；结合本次范围人工核对，不强制补齐无关历史材料。")
            documents[relative] = ""
            continue
        text = path.read_text(encoding="utf-8")
        documents[relative] = text
        if not has_content(text):
            warn(relative, 1, "empty-artifact", "未识别到正文，不能据此报告材料完整。")

    if stage == "vet":
        idea = documents["product/idea-brief.md"]
        for title in ("原始想法", "用户", "问题", "初步价值", "判断"):
            try:
                body = section(idea, f"## {title}").split("\n", 1)
                if len(body) < 2 or not any(substantive(line.split("：", 1)[-1])
                                           for _, line in visible_lines(body[1]) if line.strip()):
                    raise ValueError()
            except ValueError:
                warn("product/idea-brief.md", 1, "missing-context", f"未识别章节内容：{title}；可用等价表达人工核对。")
        # Parse labeled fields, not business prose. Multiple candidates or an
        # unpaired reason need review; never choose the first/last decision.
        def decision_fields(text: str, label: str) -> list[str]:
            return [match[1].strip() for _, line in visible_lines(text)
                    if (match := re.fullmatch(rf"\s*(?:[-+]\s+)?{label}[:：][ \t]*(.*)",
                                             re.sub(r"[*_`]", "", line)))]

        try:
            current = section(idea, "## 判断")
        except ValueError:
            current = ""
        decisions = decision_fields(idea, "建议")
        reasons = decision_fields(idea, "理由")
        if not decisions or (len(decisions) == 1 and not re.fullmatch(r"进入\s*PRD|继续调研|暂停", decisions[0])):
            warn("product/idea-brief.md", 1, "missing-decision", "请核对实际建议；未识别到进入 PRD / 继续调研 / 暂停的明确选择。")
        if len(decisions) > 1 or len(reasons) > 1:
            warn("product/idea-brief.md", 1, "ambiguous-decision", "有多份建议或理由，无法确定本轮判断；请人工核对，不自动选择首条或末条。")
        if not reasons or (len(reasons) == 1 and not substantive(reasons[0])):
            warn("product/idea-brief.md", 1, "missing-decision-reason", "请人工核对建议依据或证据缺口。")
        if decisions != decision_fields(current, "建议") or reasons != decision_fields(current, "理由"):
            warn("product/idea-brief.md", 1, "decision-scope", "建议或理由位于判断章节之外；请人工确认本轮结论及对应依据，历史材料不作为新的业务阻断。")
    else:
        validate_prd(documents, issue, warn)

    status = "BLOCKED" if issues else "REVIEW" if any(w["requires_review"] for w in warnings) else "PASS"
    return {"stage": stage, "status": status, "passed": status == "PASS", "issues": issues,
            "warnings": warnings, "legacy_reads": legacy,
            "limitation": LIMITATION}


def validate_prd(documents: dict[str, str], issue, warn) -> None:
    prd = "product/prd.md"
    requirements = "product/requirements.md"
    acceptance = "product/acceptance-criteria.md"
    questions = "product/open-questions.md"

    def table(path: str, columns: tuple[str, ...]):
        records = rows(documents[path], columns)
        if not records:
            warn(path, 1, "missing-table", "未识别结构化表格，请按原格式人工核对内容及关联。")
        result = {}
        for number, row in records:
            key = row.get("ID", "")
            if not substantive(key):
                warn(path, number, "incomplete-row", "未识别稳定编号；请核对该行，不为通过检查强制重编号。")
                continue
            if key in result:
                issue(path, number, "duplicate-id", f"重复编号 {key}")
            for column in columns:
                if column not in {"ID", "确认状态"} and not substantive(row.get(column, "")):
                    warn(path, number, "incomplete-row", f"{key} 的 {column} 需要核对。")
            result[key] = number, row
        return result

    sources = table(prd, ("ID", "来源 / 定位", "事实 / 约束", "确认状态"))
    reqs = table(requirements, ("ID", "需求"))
    checks = table(acceptance, ("ID", "关联需求", "预期结果"))
    coverage = rows(documents[acceptance], ("需求 ID",))

    def references(path: str, number: int, value: str, family: str, target: dict, *, required: bool = True):
        # Match declared IDs literally; ASCII boundaries also work next to Chinese text.
        # Infer numeric ID families to catch R999/S999/A999 as well as new REQ/SRC/AC IDs.
        patterns = [re.escape(key) for key in target]
        patterns.append(rf"{family}[-_]?\d+")
        for key in target:
            numeric = re.fullmatch(r"([A-Za-z][A-Za-z_-]*)(\d+)", key)
            if numeric:
                patterns.append(re.escape(numeric[1]) + r"\d+")
        expression = r"(?<![A-Za-z0-9_.-])(?:" + "|".join(patterns) + r")(?![A-Za-z0-9_.-])"
        found = set(re.findall(expression, value))
        if not target:
            if required:
                warn(path, number, "unverified-reference", "未识别目标编号表，关联需人工核对。")
            return set()
        for key in sorted(found - target.keys()):
            issue(path, number, "unknown-reference", f"引用了不存在的 {key}")
        if required and not found:
            warn(path, number, "missing-reference", "未识别关联编号；保留原表达并人工核对。")
        return found & target.keys()

    for key, (number, row) in reqs.items():
        linked = references(requirements, number, row.get("来源", ""), "SRC", sources)
        for source_id in sorted(linked):
            state = sources[source_id][1].get("确认状态", "").casefold()
            if state in {"假设", "待确认", "未确认", "assumption", "pending", "unknown"}:
                issue(requirements, number, "unconfirmed-source", f"{key} 依赖未确认来源 {source_id}；保留为草稿，不能正式交接。")
            elif state not in {"已确认", "confirmed"}:
                warn(prd, sources[source_id][0], "invalid-source-status", f"请核对 {source_id} 的确认状态。")

    # AC -> requirement is the authoritative mapping. Reverse lists are optional views.
    check_reqs = {}
    for key, (number, row) in checks.items():
        check_reqs[key] = references(acceptance, number, row.get("关联需求", ""), "REQ", reqs)
        for column in ("前置条件", "操作 / 事件"):
            if not substantive(row.get(column, "")):
                warn(acceptance, number, "acceptance-detail", f"{key} 的 {column} 需人工核对。")
        if row.get("预期结果", "") in {"正常", "成功", "失败", "符合预期", "正常运行", "正常工作"}:
            warn(acceptance, number, "unobservable-result", f"{key} 的结果是否可观察，需要结合上下文判断。")
    mapped = set().union(*check_reqs.values()) if check_reqs else set()
    if checks and reqs and all(check_reqs.values()):
        for req_id in sorted(reqs.keys() - mapped):
            issue(acceptance, 1, "uncovered-requirement", f"{req_id} 没有关联验收；应补验收或明确移出本期。")

    for req_id, (number, row) in reqs.items():
        for ac_id in references(requirements, number, row.get("验收标准", ""), "AC", checks, required=False):
            if check_reqs[ac_id] and req_id not in check_reqs[ac_id]:
                issue(requirements, number, "mismatched-acceptance", f"摘要中的 {ac_id} 不属于 {req_id}。")

    # The coverage matrix is optional. If supplied, check explicit contradictions,
    # but do not require every requirement/dimension to repeat all AC references.
    for number, row in coverage:
        req_id = row.get("需求 ID", "")
        if not substantive(req_id):
            warn(acceptance, number, "coverage-gap", "未识别覆盖项的需求，请人工核对。")
        elif reqs and req_id not in reqs:
            issue(acceptance, number, "unknown-requirement", f"覆盖表出现未知需求 {req_id}。")
        for dimension, value in row.items():
            if dimension not in {"正常结果", "异常与恢复", "权限与可见性", "边界与重复操作", "状态流转"}:
                continue
            not_applicable = re.fullmatch(r"不适用[:：]\s*(.+)", value)
            if not_applicable and substantive(not_applicable[1]) and dimension != "正常结果":
                continue
            if not substantive(value) or value == "不适用" or (not_applicable and dimension == "正常结果"):
                warn(acceptance, number, "coverage-gap", f"请核对 {req_id} 的 {dimension}；不能据空值或不适用断定覆盖充分。")
                continue
            for ac_id in references(acceptance, number, value, "AC", checks, required=False):
                if check_reqs[ac_id] and req_id not in check_reqs[ac_id]:
                    issue(acceptance, number, "wrong-coverage", f"{dimension} 的 {ac_id} 不属于 {req_id}。")

    stories = "product/user-stories.md"
    for number, row in rows(documents[stories], ("用户角色", "我想要", "以便于")):
        if any(not substantive(row.get(column, "")) for column in ("用户角色", "我想要", "以便于")):
            warn(stories, number, "incomplete-story", "请核对用户故事，不必重复维护全部验收编号。")
        linked_reqs = references(stories, number, row.get("关联需求", ""), "REQ", reqs, required=False)
        for ac_id in references(stories, number, row.get("验收标准", ""), "AC", checks, required=False):
            if linked_reqs and check_reqs[ac_id] and not check_reqs[ac_id] & linked_reqs:
                issue(stories, number, "mismatched-story", f"{ac_id} 不属于该用户故事的需求。")

    consumed = set()
    pending = rows(documents[questions], ("问题", "是否阻断", "状态"), consumed=consumed)
    question_ids = set()
    for number, row in pending:
        key = row.get("ID", f"第 {number} 行问题")
        if row.get("ID"):
            if key in question_ids:
                issue(questions, number, "duplicate-id", f"重复问题编号 {key}")
            question_ids.add(key)
        blocker = row.get("是否阻断", "").casefold()
        state = row.get("状态", "").casefold()
        if blocker in {"是", "阻断", "yes", "true"} and state in {"未解决", "待确认", "open", "pending"}:
            issue(questions, number, "open-blocker", f"{key} 未解决，不能正式交接受影响需求。")
        elif blocker not in {"是", "阻断", "yes", "true", "否", "不阻断", "no", "false"} or state not in {"未解决", "待确认", "open", "pending", "已解决", "已关闭", "resolved", "closed"}:
            warn(questions, number, "invalid-question-status", f"请人工确认 {key} 是否阻断及是否已解决。")
        if not substantive(row.get("问题", "")):
            warn(questions, number, "incomplete-question", f"请补充 {key} 的问题内容。")
        if not substantive(row.get("需要谁确认", "")):
            warn(questions, number, "question-owner", f"{key} 的确认人尚未指定；按实际影响跟踪，不自动升级为业务阻断。", review=False)
    if pending:
        visible = visible_lines(documents[questions])
        unparsed = [number for number, line in visible
                    if number not in consumed and line.strip() and not re.match(r"^\s*#{1,6} ", line)]
        # Organizational headings are covered only when their section contains
        # parsed questions. A heading can itself be an unstructured question.
        headings = [(number, len(match[1])) for number, line in visible
                    if (match := re.match(r"^\s*(#{1,6}) ", line))]
        for index, (start, level) in enumerate(headings):
            end = next((number for number, depth in headings[index + 1:] if depth <= level), len(documents[questions].splitlines()) + 1)
            if not any(start < number < end for number, _ in pending):
                unparsed.append(start)
        if unparsed:
            warn(questions, min(unparsed), "unparsed-questions", "问题表外仍有未核对内容；保留原格式人工复核，不能据此认定无阻断，也不猜测其业务影响。")
    else:
        # A no-questions declaration must be visible, not inside an example/comment.
        prose = [line.strip().removeprefix("- ") for _, line in visible_lines(documents[questions])
                 if line.strip() and not re.match(r"^\s*(#|\|)", line)]
        explicit_none = len(prose) == 1 and re.fullmatch(r"(?:无|暂无开放问题|无开放问题|none|no open questions)[。. ]?", prose[0], re.I)
        if not explicit_none or has_table_data(documents[questions]):
            warn(questions, 1, "missing-question-status", "未能确认开放问题状态，请人工核对；示例、注释中的“无”不作为声明。")

    # Section names guide the author; equivalent headings are accepted. Other formats
    # get a review hint, never a business blocker solely because of a heading name.
    for alternatives in (("背景",), ("目标", "产品目标"), ("用户角色", "目标用户与角色", "目标用户"),
                         ("核心场景",), ("功能范围", "本期范围", "MVP 范围"), ("非目标范围", "不做的内容"),
                         ("业务规则",), ("用户流程",), ("验收标准",), ("假设与风险", "风险与假设"), ("开放问题",)):
        found = False
        for title in alternatives:
            try:
                body = section(documents[prd], f"## {title}").split("\n", 1)
                found = len(body) > 1 and has_content(body[1])
            except ValueError:
                continue
            if found:
                break
        if not found:
            warn(prd, 1, "missing-section", f"未识别到 {alternatives[0]} 的内容；可在原格式中人工核对。")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="退出码：0 无已识别阻断（须同时查看 PASS/REVIEW）；1 明确冲突或业务阻断；2 参数或读取失败。")
    commands = parser.add_subparsers(dest="command", required=True)
    context = commands.add_parser("context", help="只输出本阶段规则和模板，不加载脚本源码。")
    context.add_argument("--stage", choices=ARTIFACTS, required=True)
    check = commands.add_parser("validate", help="只读检查想法/PRD 产物；不会改写文件。")
    check.add_argument("--stage", choices=("vet", "prd"), required=True)
    check.add_argument("--root", type=Path, required=True, help="产物根目录，例如 pd-work/ad-alert")
    check.add_argument("--format", choices=("summary", "json"), default="summary")
    args = parser.parse_args()
    try:
        if args.command == "context":
            print(stage_context(args.stage), end="")
            return 0
        if not args.root.is_dir():
            parser.error(f"产物根目录不存在或不是目录：{args.root}")
        report = validate(args.root.resolve(), args.stage)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"读取失败：{error}\n")
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Product artifact check ({args.stage}): {report['status']}")
        findings = [("ERROR", item) for item in report["issues"]] + [("WARN", item) for item in report["warnings"]]
        for level, item in findings[:30]:
            print(f"{item['file']}:{item['line']} [{level}:{item['code']}] {item['message']}")
        if len(findings) > 30:
            print(f"另有 {len(findings) - 30} 项；使用 --format json 查看完整结果。")
        print(report["limitation"])
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
