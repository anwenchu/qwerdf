#!/usr/bin/env python3
"""Benchmark-only evidence/consistency checks, not a UI quality approval tool.

Uses the repository Markdown reader; copied fixtures put it in verification/common.
The fixed scenarios are synthetic evaluation cases, not a schema for user reports.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

COMMON = Path(__file__).parent / "common"
if not COMMON.is_dir():
    COMMON = Path(__file__).resolve().parents[2] / "skills/qwerdf-common/scripts"
sys.path.insert(0, str(COMMON))
from product_artifacts import rows, section, substantive, visible_lines

SCENARIOS = {"mobile-form": "有阻断", "compact-report": "本轮范围可继续", "missing-visual": "证据不足",
             "amount-clipped": "有阻断", "amount-readable": "本轮范围可继续",
             "save-error": "有阻断", "save-error-feedback": "本轮范围可继续"}
FINDING_COLUMNS = ("级别", "问题", "用户影响", "验证方式", "证据", "归属")
LIMITATION = "仅校验评估用材料与报告一致性；不证明模型看过图片或视觉判断正确，仍须按图人工复核。"


def selected_value(raw: str, choices: tuple[str, ...], label: str, review: list[str]) -> str | None:
    """Read an enum with optional formatting/scope notes, never infer prose meaning."""
    value = re.sub(r"[*_`]", "", raw).strip()
    mentioned = {choice for choice in choices if choice in value}
    selected = next((choice for choice in choices
                     if re.match(rf"^{re.escape(choice)}(?=$|[，,；;。.:：\s（(])", value)), None)
    if selected is None or len(mentioned) != 1:
        review.append(f"{label}未能识别唯一选择；请人工确认本轮范围，不按第一个前缀放行")
        return None
    return selected


def unconsumed_findings(body: str, parsed_lines: set[int]) -> bool:
    """Only recognize table scaffolding; leave every other content to a reader."""
    for number, line in enumerate(body.splitlines(), 1):
        value = line.strip()
        if not value or value == "## Findings" or number in parsed_lines:
            continue
        if value.startswith("|"):
            cells = [cell.strip().strip("`*") for cell in value.strip("|").split("|")]
            if set(FINDING_COLUMNS).issubset(cells):
                continue
            if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                continue
        return True
    return False


def check(root: Path, scenario: str) -> dict:
    errors = []
    review = []
    report_path = root / "ui/ui-review-report.md"
    text = report_path.read_text(encoding="utf-8") if report_path.is_file() else ""
    if not text.strip():
        errors.append("缺少非空 UI review 报告")
    duplicate_sections = set()
    for heading in ("## 结论", "## Findings", "## 三层审查结果"):
        if sum(line.strip() == heading for _, line in visible_lines(text)) > 1:
            duplicate_sections.add(heading)
            review.append(f"重复章节 {heading}，不能只读取第一份结果")
    try:
        conclusion = section(text, "## 结论")
    except ValueError:
        conclusion = ""
    # Only read the conclusion, never keywords in examples or findings.
    states = [re.sub(r"[*_`]", "", match[1]).strip() for _, line in visible_lines(conclusion)
              if (match := re.fullmatch(r"\s*-?\s*状态[:：]\s*(.+)", line))]
    selected = selected_value(states[0] if len(states) == 1 and "## 结论" not in duplicate_sections else "",
                              tuple(dict.fromkeys(SCENARIOS.values())), "结论状态", review)
    if selected is not None and selected != SCENARIOS[scenario]:
        errors.append(f"本案例结论应为 {SCENARIOS[scenario]}，实际 {selected}")

    layers = {}
    duplicate_layers = set()
    for _, row in rows(text, ("检查层", "结果：已检查 / 不适用 / 未验证", "依据或理由")):
        key = row.get("检查层", "")
        if key in layers:
            duplicate_layers.add(key)
            review.append(f"重复检查层：{key}，需确认本轮范围")
        layers[key] = row
    executed = {}
    for layer in ("机器扫描", "视觉扫描", "模板扫描"):
        row = layers.get(layer, {})
        raw = "" if layer in duplicate_layers or "## 三层审查结果" in duplicate_sections else row.get("结果：已检查 / 不适用 / 未验证", "")
        executed[layer] = selected_value(raw,
                                         ("已检查", "不适用", "未验证"), layer, review)
        if not substantive(row.get("依据或理由", "")):
            review.append(f"{layer} 缺少可核对依据，需人工补证")
    # These fixtures provide no runtime page or Figma nodes. File hashes are not a UI scan.
    if executed["机器扫描"] == "已检查":
        errors.append("固定案例没有运行页面或 Figma 节点，不能声称完成 UI 机器扫描")
    if scenario == "missing-visual":
        if executed["视觉扫描"] not in {None, "未验证"}:
            errors.append("无图案例必须保持视觉未验证")
        if executed["模板扫描"] == "已检查":
            errors.append("无图案例没有目标组件证据，不能声称完成模板扫描")
    elif executed["视觉扫描"] not in {None, "已检查"}:
        errors.append("图片案例尚未完成必要视觉检查")
    if scenario == "compact-report" and executed["模板扫描"] not in {None, "已检查"}:
        errors.append("本案例有三条同类行，模板比较是必要检查，不能记未验证或不适用")

    image = None
    if scenario != "missing-visual":
        filename = f"{scenario}.png"
        fixture_dir = root / "visual-fixtures"
        baseline = fixture_dir / "baseline.json"
        try:
            records = json.loads(baseline.read_text(encoding="utf-8"))["images"]
            metadata = next(record for record in records if record["file"] == filename)
            if scenario.startswith("save-error"):
                if metadata.get("state") != "save-rejected" or metadata.get("attempt", {}).get("outcome") != "rejected":
                    errors.append("失败反馈案例缺少保存已被拒绝的采集记录，不能从默认图推断错误态")
            data = (fixture_dir / filename).read_bytes()
            image = filename
            if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
                errors.append("截图不是 PNG")
            elif struct.unpack(">II", data[16:24]) != (metadata["width"], metadata["height"]):
                errors.append("截图尺寸与基线不一致")
            if hashlib.sha256(data).hexdigest() != metadata["sha256"]:
                errors.append("截图与固定评估基线不一致")
        except (OSError, ValueError, KeyError, StopIteration, TypeError) as error:
            errors.append(f"缺失或损坏的真实截图基线：{error}")
        visible = "\n".join(line for _, line in visible_lines(text))
        if filename not in visible:
            errors.append("报告没有引用目标截图")
        if scenario.startswith("save-error") and "baseline.json" not in visible:
            errors.append("失败反馈结论须关联 baseline.json 的失败后状态证据")

    try:
        finding_body = section(text, "## Findings")
    except ValueError:
        finding_body = ""
        review.append("未识别 Findings 章节；需等价人工核对，不能自动当作无问题")
    findings = rows(finding_body, FINDING_COLUMNS)
    unknown_content = not finding_body or "## Findings" in duplicate_sections or unconsumed_findings(finding_body, {number for number, _ in findings})
    if findings or unknown_content:
        review.append("Findings 含非空行或自由内容：语义、分级及与核心任务的对应关系须按案例 review_notes 对图人工复核；不猜测是否为无问题说明")
    # A finding may cite E1 from the evidence index instead of repeating paths.
    aliases = set()
    if image:
        for _, row in rows(text, ("证据",)):
            if image in " ".join(row.values()):
                match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)[:：\s]", row.get("证据", ""))
                if match:
                    aliases.add(match[1])
    blockers = []
    actual_findings = []
    unknown_severity = False
    for _, row in findings:
        match = re.match(r"^(P[0-3])(?=$|[\s·:：（(-])", row.get("级别", ""))
        if match is None:
            unknown_severity = True
            continue  # Includes no-finding placeholder rows: REVIEW, not inferred harm/no-harm.
        severity = match[1]
        actual_findings.append(row)
        if any(not row.get(column, "").strip() for column in ("问题", "用户影响", "验证方式", "证据", "归属")):
            errors.append("finding 存在空的必填字段；内容是否充分另行人工复核")
        if severity in {"P0", "P1"}:
            blockers.append(row)
        evidence = row.get("证据", "")
        linked_alias = any(re.search(rf"(?<![A-Za-z0-9_-]){re.escape(alias)}(?![A-Za-z0-9_-])", evidence) for alias in aliases)
        if image and image not in evidence and not linked_alias:
            errors.append("finding 没有关联本案例截图")
    if SCENARIOS[scenario] == "有阻断" and not blockers and not unknown_content and not unknown_severity:
        errors.append("固定阻断案例未记录必要 P0/P1；不能用 P2/P3 或空结果替代")
    if SCENARIOS[scenario] == "本轮范围可继续" and blockers:
        errors.append("本固定正常对照与报告中的 P0/P1 阻断矛盾，须人工按图核对")
    if scenario == "missing-visual" and actual_findings:
        errors.append("无图案例不能声称发现已验证的视觉缺陷")
    status = "FAIL" if errors else "REVIEW" if review else "PASS"
    return {"scenario": scenario, "scope": "report-structure-and-evidence", "status": status, "mechanical_checks_passed": not errors,
            "automated_checks_passed": status == "PASS", "errors": errors,
            "review_required": list(dict.fromkeys(review)), "limitation": LIMITATION}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    args = parser.parse_args()
    report = check(args.root.resolve(), args.scenario)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return {"PASS": 0, "FAIL": 1, "REVIEW": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
