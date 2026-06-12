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
FORBIDDEN_TERMS = [
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
    checked.extend(sorted(SKILLS_DIR.rglob("*")))
    for path in checked:
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_TERMS:
            if term in text:
                fail(errors, f"{path}: forbidden old command name found: {term}")


def validate_open_source_files(errors: list[str]) -> None:
    for relative in ("LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"):
        path = ROOT / relative
        if not path.exists() or not path.is_file() or path.stat().st_size == 0:
            fail(errors, f"{path}: missing or empty")


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
    eval_file = EVALS_DIR / "trigger-queries.json"
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
    cases_file = EVALS_DIR / "benchmark-cases.json"
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

        setup_files = item.get("setup_files", {})
        if setup_files is not None and not isinstance(setup_files, dict):
            fail(errors, f"{cases_file}: item {index} setup_files must be an object when present")
        elif isinstance(setup_files, dict) and not all(is_safe_relative_path(path) for path in setup_files):
            fail(errors, f"{cases_file}: item {index} setup_files contains unsafe path")

        fixture_dirs = item.get("fixture_dirs", {})
        if fixture_dirs is not None and not isinstance(fixture_dirs, dict):
            fail(errors, f"{cases_file}: item {index} fixture_dirs must be an object when present")
        elif isinstance(fixture_dirs, dict):
            for source, destination in fixture_dirs.items():
                if not is_safe_relative_path(source) or not is_safe_relative_path(destination):
                    fail(errors, f"{cases_file}: item {index} fixture_dirs contains unsafe path")
                elif not (ROOT / str(source)).is_dir():
                    fail(errors, f"{cases_file}: item {index} fixture dir not found: {source}")

        for key in ("required_contains", "all_contains", "any_contains"):
            rules = item.get(key, {})
            if rules is not None and not isinstance(rules, dict):
                fail(errors, f"{cases_file}: item {index} {key} must be an object when present")
            elif isinstance(rules, dict):
                for path, snippets in rules.items():
                    if not is_safe_relative_path(path):
                        fail(errors, f"{cases_file}: item {index} {key} contains unsafe path")
                    if not isinstance(snippets, list) or not all(isinstance(snippet, str) for snippet in snippets):
                        fail(errors, f"{cases_file}: item {index} {key} values must be string arrays")

        check_commands = item.get("check_commands", [])
        if check_commands is not None and not isinstance(check_commands, list):
            fail(errors, f"{cases_file}: item {index} check_commands must be an array when present")
        elif isinstance(check_commands, list) and not all(isinstance(command, str) and command.strip() for command in check_commands):
            fail(errors, f"{cases_file}: item {index} check_commands values must be non-empty strings")

    for skill, count in cases_by_skill.items():
        if count == 0:
            fail(errors, f"{cases_file}: missing benchmark case for {skill}")


def validate_benchmark_runner_contract(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    for token in (
        "--run-baseline",
        "--case",
        "--skill",
        "--list-cases",
        "dry-run",
        "真实执行",
        "rep-01",
        "command.json",
        "last-message.txt",
        "checks/",
    ):
        if token not in readme_text:
            fail(errors, f"{readme}: benchmark docs must mention {token!r}")

    cases_file = EVALS_DIR / "benchmark-cases.json"
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

    for common_file in ("product-delivery-flow.md", "artifact-contracts.md", "engineering-contracts.md"):
        if not (COMMON_DIR / common_file).exists():
            fail(errors, f"{COMMON_DIR / common_file}: missing")

    validate_manifest(skill_names, errors)

    for skill in skill_names:
        validate_skill(skill, errors)

    validate_open_source_files(errors)
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
