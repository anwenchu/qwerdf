#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
COMMON_DIR = SKILLS_DIR / "qwerdf-common"
MANIFEST_FILE = SKILLS_DIR / "manifest.txt"
EVALS_DIR = ROOT / "evals"
EVAL_CASES_DIR = EVALS_DIR / "cases"
DOCS_DIR = ROOT / "docs"
CANONICAL_ARTIFACT_PREFIXES = ("product/", "ui/", "tech/", "sync/", "test/", "release/")
ARTIFACT_FILENAMES = {
    "idea-brief.md",
    "user-problem.md",
    "competitor-notes.md",
    "mvp-hypothesis.md",
    "validation-questions.md",
    "prd.md",
    "requirements.md",
    "user-stories.md",
    "acceptance-criteria.md",
    "open-questions.md",
    "product-brief.md",
    "ui-design-system.md",
    "ui-flows.md",
    "ui-pages.md",
    "ui-screens.md",
    "ui-components.md",
    "ui-directions.md",
    "figma-handoff.md",
    "ui-review-report.md",
    "tech-plan.md",
    "dependency-readiness.md",
    "frontend-design.md",
    "frontend-component-map.md",
    "frontend-route-map.md",
    "frontend-state-api.md",
    "backend-design.md",
    "api-contract.md",
    "data-model.md",
    "sql-execution-plan.md",
    "integration-map.md",
    "task-slices.md",
    "risk-plan.md",
    "frontend-implementation-log.md",
    "frontend-changed-files.md",
    "frontend-dev-notes.md",
    "frontend-acceptance.md",
    "backend-implementation-log.md",
    "backend-changed-files.md",
    "backend-dev-notes.md",
    "integration-plan.md",
    "integration-report.md",
    "api-mismatch.md",
    "plan-revision.md",
    "test-plan.md",
    "test-cases.md",
    "test-report.md",
    "regression-notes.md",
    "code-review.md",
    "commit-summary.md",
    "pr-description.md",
    "release-plan.md",
    "release-checklist.md",
    "rollback-plan.md",
    "release-notes.md",
}
FORBIDDEN_TERMS = [
    "个" + "人",
    "tb" + "-prd-ui",
    "tb" + "-ui-figma",
    "tb" + "-figma-code",
    "$" + "tb-",
    "product" + "-blueprint",
    "figma" + "-design",
    "frontend" + "-handoff",
    "pd" + "-code",
    "ui" + "-work",
    "ui" + "-delivery-flow.md",
]


def read_skill_names() -> list[str]:
    if not MANIFEST_FILE.exists():
        return []
    names: list[str] = []
    for raw_line in MANIFEST_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"{path}: missing frontmatter")
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(errors, f"{path}: unterminated frontmatter")
        return {}

    block = text[4:end]
    keys: dict[str, str] = {}
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
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
                keys[key] = " ".join(part for part in parts if part)
                continue
            keys[key] = value.strip().strip('"')
        index += 1

    key_set = set(keys)
    expected = {"name", "description"}
    if key_set != expected:
        fail(errors, f"{path}: frontmatter keys must be exactly {sorted(expected)}, got {sorted(key_set)}")
    return keys


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def is_flat_artifact_path(value: object) -> bool:
    return isinstance(value, str) and "/" not in value and value in ARTIFACT_FILENAMES


def parse_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*\"([^\"]*)\"\s*$", text, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def validate_skill(skill: str, errors: list[str]) -> None:
    skill_dir = SKILLS_DIR / skill
    skill_md = skill_dir / "SKILL.md"
    agent_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        fail(errors, f"{skill_md}: missing")
        return

    frontmatter = parse_frontmatter(skill_md, errors)
    if frontmatter.get("name") != skill:
        fail(errors, f"{skill_md}: name must match directory name {skill!r}")

    description = frontmatter.get("description", "")
    if "Use when the user mentions" not in description:
        fail(errors, f"{skill_md}: description must include trigger guidance with 'Use when the user mentions'")
    if f"${skill}" not in description:
        fail(errors, f"{skill_md}: description must mention ${skill}")
    if not (80 <= len(description) <= 700):
        fail(errors, f"{skill_md}: description length should be between 80 and 700 chars, got {len(description)}")

    if not agent_yaml.exists():
        fail(errors, f"{agent_yaml}: missing")
        return

    agent_text = agent_yaml.read_text(encoding="utf-8")
    for key in ("display_name", "short_description", "default_prompt"):
        value = parse_yaml_value(agent_text, key)
        if not value:
            fail(errors, f"{agent_yaml}: missing quoted interface.{key}")

    prompt = parse_yaml_value(agent_text, "default_prompt") or ""
    if f"${skill}" not in prompt:
        fail(errors, f"{agent_yaml}: default_prompt must mention ${skill}")


def iter_markdown_files() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "SECURITY.md", ROOT / "CHANGELOG.md"]
    paths.extend(sorted(DOCS_DIR.rglob("*.md")) if DOCS_DIR.exists() else [])
    paths.extend(sorted(SKILLS_DIR.rglob("*.md")))
    return [path for path in paths if path.exists()]


def validate_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            resolved = Path(target) if target.startswith("/") else (path.parent / target)
            if not resolved.exists():
                fail(errors, f"{path}: broken markdown link to {match.group(1)!r}")


def validate_forbidden_terms(errors: list[str]) -> None:
    checked = [ROOT / "README.md"]
    if DOCS_DIR.exists():
        checked.extend(sorted(DOCS_DIR.rglob("*")))
    checked.extend(sorted(SKILLS_DIR.rglob("*")))
    for path in checked:
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_TERMS:
            if term in text:
                fail(errors, f"{path}: forbidden or outdated term found: {term}")


def validate_open_source_files(errors: list[str]) -> None:
    for relative in ("LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"):
        path = ROOT / relative
        if not path.exists() or not path.is_file() or path.stat().st_size == 0:
            fail(errors, f"{path}: missing or empty")


def validate_reference_guardrails(errors: list[str]) -> None:
    required_tokens_by_file = {
        ROOT / "README.md": [
            "Quick Start",
            "Workflow",
            "Skills",
            "Repository Layout",
            "Documentation",
            "License",
            "中文",
            "docs/usage.md",
            "docs/architecture.md",
            "docs/benchmarking.md",
        ],
        DOCS_DIR / "usage.md": [
            "product/",
            "ui/",
            "tech/",
            "sync/",
            "test/",
            "release/",
            "legacy fallback",
            "sql-execution-plan.md",
            "ui-design-system.md",
            "MASTER",
            "Page Overrides",
            "bash scripts/install.sh",
        ],
        DOCS_DIR / "development.md": [
            "skills/manifest.txt",
            "evals/cases/trigger-queries.json",
            "evals/cases/benchmark-cases.json",
            "agents/openai.yaml",
            "validate_skills.py",
            "qwerdf-common",
        ],
        DOCS_DIR / "benchmarking.md": [
            "evals/cases/trigger-queries.json",
            "evals/cases/benchmark-cases.json",
            "evals/reports/",
            "evals/runs/",
            "--run-baseline",
            "--case",
            "--skill",
            "--list-cases",
            "dry-run",
            "真实执行",
            "rep-01",
            "command.json",
            "forbidden_contains",
            "last-message.txt",
            "checks/",
        ],
        DOCS_DIR / "architecture.md": [
            "skills/<skill-name>/SKILL.md",
            "skills/qwerdf-common",
            "Codex skill discovery",
            "qwerdf-common",
            "product-delivery-flow.md",
            "engineering-contracts.md",
        ],
        DOCS_DIR / "references.md": [
            "anthropics/skills",
            "vercel-labs/agent-skills",
            "nextlevelbuilder/ui-ux-pro-max-skill",
            "Design System Generator",
            "MASTER",
            "Page Overrides",
        ],
        COMMON_DIR / "product-delivery-flow.md": [
            "product/",
            "ui/",
            "tech/",
            "legacy fallback",
            "tech/dependency-readiness.md",
            "tech/backend/sql-execution-plan.md",
            "ui/ui-design-system.md",
            "ui/ui-review-report.md",
            "UI 设计系统与质量 Gate",
            "$pd-ui-review",
            "真实依赖 Gate",
            "mock-only",
            "Page Overrides",
            "管理后台",
            "截图级视觉 QA",
            "同类问题扫描",
            "UI 职责边界",
            "产品事实与参考使用 Gate",
            "产品事实源优先级",
            "参考禁区",
            "Figma / 截图是表现层参考",
            "$pd-sync` 没有明确通过",
            "$pd-git` 只能在 commit readiness gate 全部通过后准备提交",
        ],
        COMMON_DIR / "artifact-contracts.md": [
            "产品事实源",
            "参考使用边界",
            "产品事实锁定",
            "产品范围校验",
            "ui/ui-design-system.md",
            "ui/ui-review-report.md",
            "MASTER",
            "Page Overrides",
            "信息密度",
            "截图证据",
            "低级视觉问题零容忍",
            "同类问题扫描",
            "不能交付检查",
        ],
        COMMON_DIR / "ui-design-system.md": [
            "ui/ui-design-system.md",
            "MASTER",
            "Page Overrides",
            "产品类型",
            "管理后台",
            "设计系统门禁",
            "Typography semantic levels",
            "Spacing scale",
            "Complex information patterns",
            "移动端安全边距",
        ],
        COMMON_DIR / "ui-quality-checklist.md": [
            "低级视觉问题零容忍",
            "无横向溢出",
            "文本不重叠",
            "default",
            "loading",
            "empty",
            "permission",
            "frontend-acceptance.md",
            "ui-review-report.md",
            "spacing scale",
            "同类问题扫描",
            "Figma 交付前截图 QA",
        ],
        COMMON_DIR / "ui-patterns.md": [
            "SaaS",
            "管理后台",
            "数据看板",
            "表格",
            "Landing Page",
        ],
        COMMON_DIR / "ui-review-rules.md": [
            "UI Review",
            "P0",
            "P1",
            "基础视觉缺陷",
            "设计系统一致性",
            "响应式",
            "防误报",
            "不能交付条件",
            "同类问题扫描",
            "截图证据",
        ],
        SKILLS_DIR / "pd-ui-review" / "SKILL.md": [
            "ui/ui-review-report.md",
            "visual-defects.md",
            "figma-review.md",
            "screenshot-review.md",
            "$pd-figma",
            "$pd-fe",
            "$pd-plan",
            "$pd-blueprint",
            "P0",
            "P1",
            "不能交付条件",
            "同类问题扫描",
            "截图证据",
        ],
        SKILLS_DIR / "pd-ui-review" / "references" / "visual-defects.md": [
            "遮挡",
            "重叠",
            "溢出",
            "风格不统一",
            "字体不一致",
            "低级视觉问题零容忍",
            "复杂信息展示缺陷",
        ],
        SKILLS_DIR / "pd-ui-review" / "references" / "figma-review.md": [
            "Figma",
            "MASTER",
            "Page Overrides",
            "$pd-figma",
            "screenshot",
            "不能放行",
        ],
        SKILLS_DIR / "pd-ui-review" / "references" / "screenshot-review.md": [
            "375px",
            "768px",
            "1024px",
            "1440px",
            "横向溢出",
            "同类问题扫描",
            "不能放行",
        ],
        SKILLS_DIR / "pd-blueprint" / "SKILL.md": [
            "产品事实锁",
            "参考拆解",
            "不能从参考图直接搬运",
            "ui/ui-design-system.md",
            "信息密度",
            "管理后台",
        ],
        SKILLS_DIR / "pd-figma" / "SKILL.md": [
            "产品事实锁定",
            "参考使用边界",
            "没有新增范围外页面",
            "ui/ui-design-system.md",
            "MASTER",
            "page-level override",
            "截图级视觉 QA",
            "低级视觉问题零容忍",
            "同类问题扫描",
            "移动端安全边距",
        ],
        SKILLS_DIR / "pd-plan" / "SKILL.md": [
            "Figma handoff 是表现层输入",
            "范围外页面",
            "tech/dependency-readiness.md",
            "mock-only",
            "tech/backend/sql-execution-plan.md",
            "无 SQL 执行项",
            "UI 设计系统约束",
            "响应式",
            "可访问性",
        ],
        SKILLS_DIR / "pd-fe" / "SKILL.md": [
            "ui/ui-design-system.md",
            "tech/dependency-readiness.md",
            "mock-only",
            "ui-quality-checklist.md",
            "无横向溢出",
            "文本不重叠",
            "frontend-acceptance.md",
        ],
        SKILLS_DIR / "pd-be" / "SKILL.md": [
            "tech/dependency-readiness.md",
            "mock-only",
            "tech/backend/sql-execution-plan.md",
            "SQL / Migration 文件",
        ],
        SKILLS_DIR / "pd-test" / "SKILL.md": [
            ".gitignore",
            "integration-report.md` 缺失",
            "tech/dependency-readiness.md",
            "Mock 禁用检查",
            "可能漏提交",
            "可能多提交",
            "tech/backend/sql-execution-plan.md",
            "SQL 执行验证",
        ],
        SKILLS_DIR / "pd-release" / "SKILL.md": [
            "tech/backend/sql-execution-plan.md",
            "SQL / 数据变更执行计划",
            "前置备份",
        ],
        SKILLS_DIR / "pd-review" / "SKILL.md": [
            "产品范围漂移检查",
            "不能用“参考图里有”作为产品范围证据",
            "渐进式加载",
            "四阶段",
            "代码级审查",
            "UI Review",
            "ui/ui-review-report.md",
            "ui-review-rules.md",
            "UI 设计质量审查",
            "大 Diff 处理",
            "diff_triage.py",
            "自动化工具",
            "修复归属",
            "验证建议",
        ],
        SKILLS_DIR / "pd-review" / "scripts" / "diff_triage.py": [
            "Diff Triage",
            "Recommended references",
            "Risk tags",
            "frontend-code-review.md",
            "backend-code-review.md",
            "security-performance-review.md",
            "ui-review-rules.md",
        ],
        SKILLS_DIR / "pd-review" / "references" / "universal-code-quality.md": [
            "正确性",
            "数据一致性",
            "复用检查",
            "测试质量",
            "人工审查",
        ],
        SKILLS_DIR / "pd-review" / "references" / "frontend-code-review.md": [
            "TypeScript",
            "React",
            "useEffect",
            "API 契约",
            "请求竞态",
        ],
        SKILLS_DIR / "pd-review" / "references" / "backend-code-review.md": [
            "Java / Spring Boot",
            "事务",
            "SQL",
            "DTO 校验",
            "测试切片",
        ],
        SKILLS_DIR / "pd-review" / "references" / "security-performance-review.md": [
            "IDOR",
            "XSS",
            "SSRF",
            "N+1",
            "敏感字段",
        ],
        COMMON_DIR / "engineering-contracts.md": [
            "tech/dependency-readiness.md",
            "tech/frontend/frontend-design.md",
            "sync/integration-report.md",
            "test/test-report.md",
            "release/commit-summary.md",
            "Readiness gates",
            "ui/ui-review-report.md",
            "实现前置状态",
            "真实依赖验证",
            "Mock 禁用检查",
            "联调前置状态",
            "SQL 执行计划",
            "SQL 执行验证",
            "SQL / 数据变更执行计划",
            "Git / ignore 检查",
            "Possible missing files",
            "Possible extra files",
            "审查范围",
            "前置证据",
            "Diff triage",
            "Findings",
            "UI Review 摘要",
            "代码级检查摘要",
            "修复归属",
            "验证方式",
            "UI 设计系统约束",
        ],
        SKILLS_DIR / "pd-sync" / "SKILL.md": [
            "task-slices.md",
            "tech/dependency-readiness.md",
            "mock-only",
            "真实依赖验证",
            "Mock 禁用检查",
            "未完成实现 slice",
            "不得执行联调",
            "不进入 `$pd-test`",
        ],
        SKILLS_DIR / "pd-git" / "SKILL.md": [
            "Commit readiness gate",
            "提交范围门禁",
            "git add -A",
            "integration-report.md` 明确通过",
            "possible missing files",
            "possible extra files",
            "staged 与 planned 不一致",
        ],
    }
    for path, tokens in required_tokens_by_file.items():
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        for token in tokens:
            if token not in text:
                fail(errors, f"{path}: missing reference guardrail token {token!r}")


def validate_manifest(skill_names: list[str], errors: list[str]) -> None:
    if not MANIFEST_FILE.exists():
        fail(errors, f"{MANIFEST_FILE}: missing")
        return
    if not skill_names:
        fail(errors, f"{MANIFEST_FILE}: no skill names found")
        return
    seen: set[str] = set()
    for index, skill in enumerate(skill_names, start=1):
        if not re.match(r"^pd-[a-z0-9-]+$", skill):
            fail(errors, f"{MANIFEST_FILE}: line {index} invalid skill name {skill!r}")
        if skill in seen:
            fail(errors, f"{MANIFEST_FILE}: duplicate skill name {skill!r}")
        seen.add(skill)

    actual_dirs = sorted(
        path.name
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and path.name.startswith("pd-")
    )
    missing_from_manifest = sorted(set(actual_dirs) - set(skill_names))
    missing_dirs = sorted(set(skill_names) - set(actual_dirs))
    if missing_from_manifest:
        fail(errors, f"{MANIFEST_FILE}: missing skill dirs from manifest: {missing_from_manifest}")
    if missing_dirs:
        fail(errors, f"{MANIFEST_FILE}: manifest names without skill dirs: {missing_dirs}")


def validate_trigger_evals(skill_names: list[str], errors: list[str]) -> None:
    eval_file = EVAL_CASES_DIR / "trigger-queries.json"
    if not eval_file.exists():
        fail(errors, f"{eval_file}: missing")
        return

    try:
        items = json.loads(eval_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{eval_file}: invalid JSON: {exc}")
        return

    if not isinstance(items, list):
        fail(errors, f"{eval_file}: expected a JSON array")
        return

    true_by_skill = {skill: 0 for skill in skill_names}
    false_count = 0
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            fail(errors, f"{eval_file}: item {index} must be an object")
            continue

        eval_id = item.get("id")
        query = item.get("query")
        should_trigger = item.get("should_trigger")
        skill = item.get("skill")
        reason = item.get("reason")

        if not isinstance(eval_id, str) or not eval_id:
            fail(errors, f"{eval_file}: item {index} missing string id")
        elif eval_id in ids:
            fail(errors, f"{eval_file}: duplicate id {eval_id!r}")
        else:
            ids.add(eval_id)

        if not isinstance(query, str) or len(query.strip()) < 12:
            fail(errors, f"{eval_file}: item {index} query is too short")
        if not isinstance(should_trigger, bool):
            fail(errors, f"{eval_file}: item {index} should_trigger must be boolean")
        if skill is not None and skill not in skill_names:
            fail(errors, f"{eval_file}: item {index} has unknown skill {skill!r}")
        if not isinstance(reason, str) or not reason.strip():
            fail(errors, f"{eval_file}: item {index} missing reason")

        if should_trigger is True and skill in true_by_skill:
            true_by_skill[skill] += 1
        if should_trigger is False:
            false_count += 1

    for skill, count in true_by_skill.items():
        if count == 0:
            fail(errors, f"{eval_file}: missing should_trigger=true query for {skill}")
    if false_count < 6:
        fail(errors, f"{eval_file}: expected at least 6 should_trigger=false near-miss queries")


def validate_benchmark_cases(skill_names: list[str], errors: list[str]) -> None:
    cases_file = EVAL_CASES_DIR / "benchmark-cases.json"
    if not cases_file.exists():
        fail(errors, f"{cases_file}: missing")
        return

    try:
        items = json.loads(cases_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{cases_file}: invalid JSON: {exc}")
        return

    if not isinstance(items, list):
        fail(errors, f"{cases_file}: expected a JSON array")
        return

    cases_by_skill = {skill: 0 for skill in skill_names}
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            fail(errors, f"{cases_file}: item {index} must be an object")
            continue

        case_id = item.get("id")
        skill = item.get("skill")
        prompt = item.get("prompt")
        expected_files = item.get("expected_files")

        if not isinstance(case_id, str) or not case_id:
            fail(errors, f"{cases_file}: item {index} missing string id")
        elif case_id in ids:
            fail(errors, f"{cases_file}: duplicate id {case_id!r}")
        else:
            ids.add(case_id)

        if skill not in skill_names:
            fail(errors, f"{cases_file}: item {index} has unknown skill {skill!r}")
        else:
            cases_by_skill[str(skill)] += 1

        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            fail(errors, f"{cases_file}: item {index} prompt is too short")
        if not isinstance(expected_files, list) or not expected_files:
            fail(errors, f"{cases_file}: item {index} expected_files must be a non-empty array")
        elif not all(is_safe_relative_path(path) for path in expected_files):
            fail(errors, f"{cases_file}: item {index} expected_files must contain safe relative paths")
        elif any(is_flat_artifact_path(path) for path in expected_files):
            fail(errors, f"{cases_file}: item {index} expected_files must use canonical artifact subdirectories")

        setup_files = item.get("setup_files", {})
        if setup_files is not None and not isinstance(setup_files, dict):
            fail(errors, f"{cases_file}: item {index} setup_files must be an object when present")
        elif isinstance(setup_files, dict) and not all(is_safe_relative_path(path) for path in setup_files):
            fail(errors, f"{cases_file}: item {index} setup_files contains unsafe path")
        elif isinstance(setup_files, dict) and any(is_flat_artifact_path(path) for path in setup_files):
            fail(errors, f"{cases_file}: item {index} setup_files must use canonical artifact subdirectories")
        elif skill == "pd-git" and isinstance(setup_files, dict):
            for required in ("sync/integration-report.md", "test/test-report.md", "test/code-review.md"):
                if required not in setup_files:
                    fail(errors, f"{cases_file}: item {index} pd-git case must include {required}")
        elif skill == "pd-release" and isinstance(setup_files, dict):
            if "tech/backend/sql-execution-plan.md" not in setup_files:
                fail(errors, f"{cases_file}: item {index} pd-release case must include tech/backend/sql-execution-plan.md")
        elif skill == "pd-sync" and isinstance(setup_files, dict):
            if "tech/task-slices.md" not in setup_files:
                fail(errors, f"{cases_file}: item {index} pd-sync case must include tech/task-slices.md")

        fixture_dirs = item.get("fixture_dirs", {})
        if fixture_dirs is not None and not isinstance(fixture_dirs, dict):
            fail(errors, f"{cases_file}: item {index} fixture_dirs must be an object when present")
        elif isinstance(fixture_dirs, dict):
            for source, destination in fixture_dirs.items():
                if not is_safe_relative_path(source) or not is_safe_relative_path(destination):
                    fail(errors, f"{cases_file}: item {index} fixture_dirs contains unsafe path")
                elif not (ROOT / str(source)).is_dir():
                    fail(errors, f"{cases_file}: item {index} fixture dir not found: {source}")

        for key in ("required_contains", "all_contains", "any_contains", "forbidden_contains"):
            rules = item.get(key, {})
            if rules is not None and not isinstance(rules, dict):
                fail(errors, f"{cases_file}: item {index} {key} must be an object when present")
            elif isinstance(rules, dict):
                for path, snippets in rules.items():
                    if not is_safe_relative_path(path):
                        fail(errors, f"{cases_file}: item {index} {key} contains unsafe path")
                    if is_flat_artifact_path(path):
                        fail(errors, f"{cases_file}: item {index} {key} must use canonical artifact subdirectories")
                    if not isinstance(snippets, list) or not all(isinstance(snippet, str) for snippet in snippets):
                        fail(errors, f"{cases_file}: item {index} {key} values must be string arrays")

        check_commands = item.get("check_commands", [])
        if check_commands is not None and not isinstance(check_commands, list):
            fail(errors, f"{cases_file}: item {index} check_commands must be an array when present")
        elif isinstance(check_commands, list) and not all(isinstance(command, str) and command.strip() for command in check_commands):
            fail(errors, f"{cases_file}: item {index} check_commands values must be non-empty strings")

        all_contains = item.get("all_contains", {})
        if skill == "pd-plan":
            if "tech/backend/sql-execution-plan.md" not in expected_files:
                fail(errors, f"{cases_file}: item {index} pd-plan case must expect tech/backend/sql-execution-plan.md")
        if skill == "pd-test" and isinstance(all_contains, dict):
            test_report_tokens = all_contains.get("test/test-report.md", [])
            if not isinstance(test_report_tokens, list) or "联调前置状态" not in test_report_tokens:
                fail(errors, f"{cases_file}: item {index} pd-test case must assert 联调前置状态")
            if not isinstance(test_report_tokens, list) or "SQL 执行验证" not in test_report_tokens:
                fail(errors, f"{cases_file}: item {index} pd-test case must assert SQL 执行验证")
        if skill == "pd-sync" and isinstance(all_contains, dict):
            integration_report_tokens = all_contains.get("sync/integration-report.md", [])
            if not isinstance(integration_report_tokens, list) or "实现前置状态" not in integration_report_tokens:
                fail(errors, f"{cases_file}: item {index} pd-sync case must assert 实现前置状态")
        if skill == "pd-git" and isinstance(all_contains, dict):
            commit_tokens = all_contains.get("release/commit-summary.md", [])
            if not isinstance(commit_tokens, list) or "Readiness gates" not in commit_tokens:
                fail(errors, f"{cases_file}: item {index} pd-git case must assert Readiness gates")
        if skill == "pd-review" and isinstance(all_contains, dict):
            review_tokens = all_contains.get("test/code-review.md", [])
            if not isinstance(review_tokens, list) or "代码级检查摘要" not in review_tokens:
                fail(errors, f"{cases_file}: item {index} pd-review case must assert 代码级检查摘要")

    for skill, count in cases_by_skill.items():
        if count == 0:
            fail(errors, f"{cases_file}: missing benchmark case for {skill}")


def validate_benchmark_runner_contract(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    benchmark_doc = DOCS_DIR / "benchmarking.md"
    benchmark_text = benchmark_doc.read_text(encoding="utf-8") if benchmark_doc.exists() else ""
    benchmark_docs_text = f"{readme_text}\n{benchmark_text}"
    for token in (
        "--run-baseline",
        "--case",
        "--skill",
        "--list-cases",
        "dry-run",
        "真实执行",
        "rep-01",
        "command.json",
        "forbidden_contains",
        "last-message.txt",
        "checks/",
    ):
        if token not in benchmark_docs_text:
            fail(errors, f"{benchmark_doc}: benchmark docs must mention {token!r}")

    cases_file = EVAL_CASES_DIR / "benchmark-cases.json"
    if not cases_file.exists():
        return
    try:
        cases = json.loads(cases_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    if not isinstance(cases, list):
        return

    with tempfile.TemporaryDirectory(prefix="qwerdf-validate-benchmark-") as temp_dir:
        runs_dir = Path(temp_dir) / "runs"
        command = [
            sys.executable,
            str(ROOT / "scripts" / "run_skill_benchmark.py"),
            "--dry-run",
            "--run-baseline",
            "--repetitions",
            "1",
            "--runs-dir",
            str(runs_dir),
        ]
        try:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired:
            fail(errors, "scripts/run_skill_benchmark.py: dry-run smoke timed out")
            return

        if completed.returncode != 0:
            fail(
                errors,
                "scripts/run_skill_benchmark.py: dry-run smoke failed "
                f"with exit {completed.returncode}: {completed.stderr.strip()}",
            )
            return

        run_dirs = sorted(path for path in runs_dir.iterdir() if path.is_dir())
        if len(run_dirs) != 1:
            fail(errors, f"scripts/run_skill_benchmark.py: expected one dry-run directory, got {len(run_dirs)}")
            return
        run_dir = run_dirs[0]
        for path in (run_dir / "benchmark.json", run_dir / "benchmark.md"):
            if not path.exists():
                fail(errors, f"scripts/run_skill_benchmark.py: missing dry-run artifact {path}")
        benchmark_md = run_dir / "benchmark.md"
        if benchmark_md.exists():
            benchmark_md_text = benchmark_md.read_text(encoding="utf-8")
            if "Dry-run writes" not in benchmark_md_text:
                fail(errors, f"scripts/run_skill_benchmark.py: dry-run report must describe dry-run artifacts: {benchmark_md}")
            if "last message, artifacts, checks" in benchmark_md_text:
                fail(errors, f"scripts/run_skill_benchmark.py: dry-run report must not imply real-run artifacts: {benchmark_md}")

        for item in cases:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            case_id = item["id"]
            for mode in ("with_skill", "baseline"):
                rep_dir = run_dir / mode / case_id / "rep-01"
                for name in ("prompt.md", "command.json", "stdout.txt", "stderr.txt"):
                    if not (rep_dir / name).exists():
                        fail(errors, f"scripts/run_skill_benchmark.py: missing dry-run artifact {rep_dir / name}")
                if not (rep_dir / "outputs").is_dir():
                    fail(errors, f"scripts/run_skill_benchmark.py: missing dry-run outputs dir {rep_dir / 'outputs'}")
                if (rep_dir / "last-message.txt").exists():
                    fail(errors, f"scripts/run_skill_benchmark.py: dry-run must not create last-message.txt: {rep_dir}")
                if (rep_dir / "checks").exists():
                    fail(errors, f"scripts/run_skill_benchmark.py: dry-run must not create checks dir: {rep_dir}")
                if mode == "baseline" and (rep_dir / "outputs" / "__skills").exists():
                    fail(errors, f"scripts/run_skill_benchmark.py: baseline dry-run must not contain copied skills: {rep_dir}")
                if mode == "with_skill":
                    skill_name = str(item.get("skill"))
                    copied_common = rep_dir / "outputs" / "__skills" / "qwerdf-common"
                    copied_skill = rep_dir / "outputs" / "__skills" / skill_name
                    if not copied_common.is_dir() or not copied_skill.is_dir():
                        fail(errors, f"scripts/run_skill_benchmark.py: with-skill dry-run missing copied skill bundle: {rep_dir}")


def main() -> int:
    errors: list[str] = []
    skill_names = read_skill_names()

    if not COMMON_DIR.exists():
        fail(errors, f"{COMMON_DIR}: missing")

    for common_file in (
        "product-delivery-flow.md",
        "artifact-contracts.md",
        "engineering-contracts.md",
        "ui-design-system.md",
        "ui-quality-checklist.md",
        "ui-patterns.md",
        "ui-review-rules.md",
    ):
        if not (COMMON_DIR / common_file).exists():
            fail(errors, f"{COMMON_DIR / common_file}: missing")

    validate_manifest(skill_names, errors)

    for skill in skill_names:
        validate_skill(skill, errors)

    validate_open_source_files(errors)
    validate_reference_guardrails(errors)
    validate_links(errors)
    validate_forbidden_terms(errors)
    validate_trigger_evals(skill_names, errors)
    validate_benchmark_cases(skill_names, errors)
    validate_benchmark_runner_contract(errors)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
