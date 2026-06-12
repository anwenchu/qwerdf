#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_FILE = SKILLS_DIR / "manifest.txt"
EVALS_FILE = ROOT / "evals" / "trigger-queries.json"
REPORT_MD = ROOT / "evals" / "trigger-preflight-report.md"
REPORT_JSON = ROOT / "evals" / "trigger-preflight-report.json"

NEGATION_PATTERNS = [
    "不需要",
    "不要",
    "不用",
    "无需",
    "只帮我",
    "只需要",
    "直接帮我",
]

SKILL_HINTS = {
    "pd-vet": ["产品机会", "想法验证", "值不值得", "继续调研", "mvp 假设", "用户痛点"],
    "pd-prd": ["prd", "需求清单", "用户故事", "验收标准", "产品需求文档"],
    "pd-blueprint": ["产品设计输入", "页面蓝图", "页面地图", "页面规格", "组件清单", "用户流程"],
    "pd-figma": ["figma", "ui 方向", "ui方向", "写到 figma", "figma 设计"],
    "pd-plan": ["技术设计", "技术方案", "api 契约", "数据模型", "task-slices", "任务切片"],
    "pd-fe": ["fe-", "前端 slice", "前端任务", "前端筛选", "api client", "前端验收"],
    "pd-be": ["be-", "后端 slice", "后端接口", "service", "权限校验", "错误码", "后端测试"],
    "pd-sync": ["联调", "接口联调", "api 联调", "mock 切真实", "契约联调", "真实接口"],
    "pd-test": ["测试计划", "测试验证", "单测", "集成测试", "浏览器验证", "回归测试", "验收测试"],
    "pd-review": ["code review", "review 当前", "代码审查", "审查改动", "测试缺口", "状态覆盖"],
    "pd-git": ["git diff", "commit summary", "commit message", "pr 描述", "mr 描述", "准备提交"],
    "pd-release": ["上线计划", "上线文档", "发布计划", "回滚方案", "release notes"],
}

GENERIC_STOP_WORDS = {
    "use",
    "when",
    "the",
    "user",
    "mentions",
    "and",
    "or",
    "with",
    "from",
    "based",
    "skill",
    "个人",
    "工作流",
    "基于",
    "输出",
    "生成",
    "记录",
    "当前",
    "用户",
    "项目",
    "不接入",
    "外部",
    "生命周期",
}


@dataclass
class SkillMeta:
    name: str
    description: str
    aliases: list[str]
    tokens: set[str]


@dataclass
class Prediction:
    predicted_skill: str | None
    score: float
    runner_should_trigger: bool
    reason: str
    top_scores: list[tuple[str, float]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_skill_names() -> list[str]:
    names: list[str] = []
    for raw_line in read_text(MANIFEST_FILE).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    block = text[4:end]
    result: dict[str, str] = {}
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            index += 1
            continue
        key, value = match.group(1), match.group(2)
        if value in {">", ">-", "|", "|-"}:
            index += 1
            parts: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", next_line):
                    break
                parts.append(next_line.strip())
                index += 1
            result[key] = " ".join(part for part in parts if part)
            continue
        result[key] = value.strip().strip('"')
        index += 1
    return result


def normalize(text: str) -> str:
    return text.lower().replace("：", ":").replace("，", ",").replace("。", ".")


def tokenize(text: str) -> set[str]:
    normalized = normalize(text)
    tokens: set[str] = set()
    for match in re.finditer(r"[a-z0-9][a-z0-9_-]{1,}", normalized):
        token = match.group(0).strip("_-")
        if token and token not in GENERIC_STOP_WORDS:
            tokens.add(token)

    cjk_chars = re.findall(r"[\u4e00-\u9fff]", normalized)
    for size in (2, 3, 4):
        for index in range(0, max(0, len(cjk_chars) - size + 1)):
            token = "".join(cjk_chars[index : index + size])
            if token not in GENERIC_STOP_WORDS:
                tokens.add(token)
    return tokens


def extract_aliases(name: str, description: str) -> list[str]:
    aliases = {name, f"${name}"}
    marker = "Use when the user mentions"
    if marker in description:
        tail = description.split(marker, 1)[1]
        tail = tail.replace("。", ",").replace("，", ",").replace("、", ",")
        for raw in tail.split(","):
            alias = raw.strip().strip(".").strip()
            if alias:
                aliases.add(alias.lower())
    return sorted(aliases, key=len, reverse=True)


def load_skills(skill_names: list[str]) -> dict[str, SkillMeta]:
    skills: dict[str, SkillMeta] = {}
    for name in skill_names:
        text = read_text(SKILLS_DIR / name / "SKILL.md")
        frontmatter = parse_frontmatter(text)
        description = frontmatter.get("description", "")
        aliases = extract_aliases(name, description)
        skills[name] = SkillMeta(
            name=name,
            description=description,
            aliases=aliases,
            tokens=tokenize(f"{name} {description}"),
        )
    return skills


def explicit_skill(query: str, skill_names: list[str]) -> str | None:
    normalized = normalize(query)
    for name in skill_names:
        if f"${name}" in normalized or re.search(rf"\b{re.escape(name)}\b", normalized):
            return name
    return None


def has_negated_skill_intent(query: str, best_skill: str) -> bool:
    normalized = normalize(query)
    if best_skill == "pd-git" and ("不要 push" in normalized or "先不要 push" in normalized or "不 push" in normalized):
        return False
    return any(pattern in normalized for pattern in NEGATION_PATTERNS)


def score_skill(query: str, query_tokens: set[str], skill: SkillMeta) -> tuple[float, list[str]]:
    normalized = normalize(query)
    score = 0.0
    evidence: list[str] = []

    for alias in skill.aliases:
        alias_norm = normalize(alias)
        if alias_norm and alias_norm in normalized:
            weight = 45.0 if alias_norm.startswith("$") or alias_norm == skill.name else 20.0
            score += weight
            evidence.append(f"alias:{alias}")

    for hint in SKILL_HINTS.get(skill.name, []):
        if normalize(hint) in normalized:
            score += 18.0
            evidence.append(f"hint:{hint}")

    overlap = query_tokens & skill.tokens
    useful_overlap = {token for token in overlap if len(token) >= 3 or "-" in token}
    score += min(len(useful_overlap), 12) * 2.0
    if useful_overlap:
        evidence.append("tokens:" + ",".join(sorted(useful_overlap)[:6]))

    return score, evidence


def predict(query: str, skills: dict[str, SkillMeta]) -> Prediction:
    explicit = explicit_skill(query, list(skills))
    if explicit:
        return Prediction(
            predicted_skill=explicit,
            score=100.0,
            runner_should_trigger=True,
            reason=f"explicit skill mention: {explicit}",
            top_scores=[(explicit, 100.0)],
        )

    query_tokens = tokenize(query)
    scored: list[tuple[str, float, list[str]]] = []
    for skill in skills.values():
        score, evidence = score_skill(query, query_tokens, skill)
        scored.append((skill.name, score, evidence))

    scored.sort(key=lambda item: item[1], reverse=True)
    best_name, best_score, best_evidence = scored[0]
    second_score = scored[1][1] if len(scored) > 1 else 0.0
    margin = best_score - second_score
    negated = has_negated_skill_intent(query, best_name)

    threshold = 14.0
    runner_should_trigger = best_score >= threshold and margin >= 3.0 and not negated
    predicted = best_name if runner_should_trigger else None
    if negated and best_score >= threshold:
        reason = "near-miss negation suppressed trigger"
    elif runner_should_trigger:
        reason = "; ".join(best_evidence) or "score threshold met"
    else:
        reason = "no score exceeded threshold with enough margin"

    return Prediction(
        predicted_skill=predicted,
        score=best_score,
        runner_should_trigger=runner_should_trigger,
        reason=reason,
        top_scores=[(name, score) for name, score, _ in scored[:3]],
    )


def load_evals() -> list[dict[str, object]]:
    return json.loads(read_text(EVALS_FILE))


def evaluate() -> dict[str, object]:
    skill_names = read_skill_names()
    skills = load_skills(skill_names)
    evals = load_evals()
    results: list[dict[str, object]] = []
    correct = 0
    false_positive = 0
    false_negative = 0
    wrong_skill = 0

    for item in evals:
        query = str(item["query"])
        expected_trigger = bool(item["should_trigger"])
        expected_skill = item.get("skill")
        prediction = predict(query, skills)
        passed = (
            prediction.runner_should_trigger == expected_trigger
            and (not expected_trigger or prediction.predicted_skill == expected_skill)
        )
        correct += int(passed)
        if not passed:
            if prediction.runner_should_trigger and not expected_trigger:
                false_positive += 1
            elif not prediction.runner_should_trigger and expected_trigger:
                false_negative += 1
            else:
                wrong_skill += 1

        results.append(
            {
                "id": item["id"],
                "query": query,
                "expected_trigger": expected_trigger,
                "expected_skill": expected_skill,
                "predicted_trigger": prediction.runner_should_trigger,
                "predicted_skill": prediction.predicted_skill,
                "score": prediction.score,
                "passed": passed,
                "reason": prediction.reason,
                "top_scores": prediction.top_scores,
            }
        )

    total = len(results)
    pass_rate = correct / total if total else 0.0
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner": "deterministic-frontmatter-router-v1",
        "total": total,
        "passed": correct,
        "pass_rate": pass_rate,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "wrong_skill": wrong_skill,
        "results": results,
    }


def render_markdown(report: dict[str, object]) -> str:
    rows = [
        "# Skill Trigger Preflight",
        "",
        f"- Runner: `{report['runner']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Total: {report['total']}",
        f"- Passed: {report['passed']}",
        f"- Pass rate: {float(report['pass_rate']) * 100:.1f}%",
        f"- False positives: {report['false_positive']}",
        f"- False negatives: {report['false_negative']}",
        f"- Wrong skill: {report['wrong_skill']}",
        "",
        "## Results",
        "",
        "| ID | Expected | Predicted | Score | Result | Reason |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]

    for result in report["results"]:  # type: ignore[index]
        expected = result["expected_skill"] if result["expected_trigger"] else "none"
        predicted = result["predicted_skill"] if result["predicted_trigger"] else "none"
        status = "PASS" if result["passed"] else "FAIL"
        reason = str(result["reason"]).replace("|", "\\|")
        rows.append(
            f"| `{result['id']}` | `{expected}` | `{predicted}` | "
            f"{float(result['score']):.1f} | {status} | {reason} |"
        )

    rows.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a deterministic local preflight. It approximates routing from frontmatter descriptions and trigger examples.",
            "- It is not a real model benchmark. Use `scripts/run_skill_benchmark.py` for actual agent runs.",
            "- Near-miss prompts with explicit negation are intentionally suppressed to catch over-broad descriptions.",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight qwerdf skill trigger examples.")
    parser.add_argument("--format", choices=("summary", "markdown", "json"), default="summary")
    parser.add_argument("--out", type=Path, default=None, help="Write report to this path.")
    parser.add_argument("--write-default-reports", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero unless all evals pass.")
    args = parser.parse_args()

    report = evaluate()

    if args.write_default_reports:
        REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        REPORT_MD.write_text(render_markdown(report), encoding="utf-8")

    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "markdown":
        output = render_markdown(report)
    else:
        output = (
            f"Skill trigger preflight: {report['passed']}/{report['total']} passed "
            f"({float(report['pass_rate']) * 100:.1f}%). "
            f"false_positive={report['false_positive']} "
            f"false_negative={report['false_negative']} "
            f"wrong_skill={report['wrong_skill']}"
        )

    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)

    if args.strict and report["passed"] != report["total"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
