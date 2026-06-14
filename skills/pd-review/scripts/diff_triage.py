#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


FRONTEND_EXTS = {".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".sass", ".less"}
BACKEND_EXTS = {".java", ".kt", ".groovy", ".xml"}
SQL_EXTS = {".sql"}
TEST_PATTERNS = ("test", "spec", "__tests__", "tests/")
DOC_EXTS = {".md", ".mdx", ".txt"}
GENERATED_DIRS = ("dist/", "build/", "coverage/", "target/", ".next/", "node_modules/")
UI_REVIEW_PATH_MARKERS = (
    "ui/ui-design-system.md",
    "ui/figma-handoff.md",
    "ui/ui-screens.md",
    "ui/ui-components.md",
    "frontend-acceptance.md",
    "frontend-design.md",
    "ui-review-rules.md",
    "ui-quality-checklist.md",
    "ui-patterns.md",
    "ui-design-system.md",
)
UI_REVIEW_TEXT_MARKERS = (
    "ui review",
    "ui 设计",
    "设计系统",
    "design system",
    "page overrides",
    "响应式",
    "无横向溢出",
    "frontend-acceptance",
)


@dataclass
class FileChange:
    path: str
    additions: int = 0
    deletions: int = 0
    hunks: int = 0
    changed_lines: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.additions + self.deletions


def get_git_diff(staged: bool) -> str:
    command = ["git", "diff", "--no-ext-diff", "--unified=80"]
    if staged:
        command.insert(2, "--cached")
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return result.stdout


def parse_diff(text: str) -> list[FileChange]:
    files: list[FileChange] = []
    current: FileChange | None = None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            match = re.match(r"diff --git a/(.*?) b/(.*)$", line)
            path = match.group(2) if match else line.rsplit(" ", 1)[-1].removeprefix("b/")
            current = FileChange(path=path)
            files.append(current)
            continue
        if current is None:
            continue
        if line.startswith("+++ b/"):
            current.path = line[6:]
        elif line.startswith("@@"):
            current.hunks += 1
        elif line.startswith("+") and not line.startswith("+++"):
            current.additions += 1
            current.changed_lines.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            current.deletions += 1
            current.changed_lines.append(line[1:])
    return files


def has_any(text: str, patterns: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def classify(file: FileChange) -> tuple[str, list[str], list[str]]:
    path = file.path
    lowered_path = path.lower()
    suffix = Path(path).suffix.lower()
    changed = "\n".join(file.changed_lines)
    lowered = changed.lower()
    tags: list[str] = []
    refs: list[str] = ["universal-code-quality.md"]

    if lowered_path.startswith(GENERATED_DIRS):
        tags.append("generated-or-build")
    if suffix in DOC_EXTS:
        tags.append("docs")

    if any(marker in lowered_path for marker in UI_REVIEW_PATH_MARKERS) or has_any(lowered, UI_REVIEW_TEXT_MARKERS):
        tags.append("ui-design")
        refs.append("../qwerdf-common/ui-review-rules.md")
        refs.append("../qwerdf-common/ui-quality-checklist.md")

    if suffix in FRONTEND_EXTS or any(part in lowered_path for part in ("frontend/", "client/", "web/", "src/components", "src/pages")):
        tags.append("frontend")
        refs.append("frontend-code-review.md")
        refs.append("../qwerdf-common/ui-review-rules.md")
        if suffix in {".css", ".scss", ".sass", ".less"} or any(part in lowered_path for part in ("components", "pages", "routes", "styles", "theme", "tokens")):
            tags.append("ui-design")
            refs.append("../qwerdf-common/ui-quality-checklist.md")
        if suffix in {".tsx", ".jsx"} or has_any(lowered, ("react", "usestate", "useeffect", "usereducer", "usememo", "usecallback")):
            tags.append("react-state")
        if has_any(lowered, ("fetch(", "axios", "query", "mutation", "api client", "request", "response")):
            tags.append("api-client")

    if suffix in BACKEND_EXTS or any(part in lowered_path for part in ("backend/", "server/", "controller", "service", "repository", "mapper", "dao")):
        tags.append("backend")
        refs.append("backend-code-review.md")
        if has_any(lowered, ("@transactional", "transaction", "rollback", "commit")):
            tags.append("transaction")

    if suffix in SQL_EXTS or "migration" in lowered_path or has_any(lowered, ("create table", "alter table", "insert ", "update ", "delete ", "select ")):
        tags.append("data-model-sql")
        refs.append("backend-code-review.md")

    if has_any(lowered_path + "\n" + lowered, ("auth", "permission", "role", "tenant", "accountid", "userid", "token", "secret", "password", "csrf", "cors", "redirect", "webhook", "callback")):
        tags.append("security")
        refs.append("security-performance-review.md")
    if has_any(lowered, ("http://", "https://", "url", "uri", "resttemplate", "webclient", "fetch(", "axios", "external", "third-party")):
        tags.append("external-call")
        refs.append("security-performance-review.md")
    if has_any(lowered, ("for ", "while ", ".map(", ".filter(", "stream()", "select ", "join ", "limit ", "offset ", "pagination", "pageable", "cache")):
        tags.append("performance")
        refs.append("security-performance-review.md")
    if has_any(lowered, ("catch", "throw", "exception", "error", "errcode", "status", "problem")):
        tags.append("error-handling")
    if any(pattern in lowered_path for pattern in TEST_PATTERNS):
        tags.append("test")
    if file.total > 400 or file.hunks > 12:
        tags.append("large-file")

    refs = sorted(set(refs))
    tags = sorted(set(tags)) or ["general-code"]
    return infer_area(path, tags), tags, refs


def infer_area(path: str, tags: list[str]) -> str:
    if "docs" in tags:
        return "docs"
    if "test" in tags:
        return "test"
    if "frontend" in tags:
        return "frontend"
    if "backend" in tags or "data-model-sql" in tags:
        return "backend"
    return "shared"


def priority(tags: list[str], file: FileChange) -> int:
    score = file.total
    if any(tag in tags for tag in ("security", "transaction", "data-model-sql")):
        score += 500
    if any(tag in tags for tag in ("api-client", "external-call", "error-handling")):
        score += 250
    if "test" in tags:
        score += 100
    if "docs" in tags:
        score -= 100
    if "generated-or-build" in tags:
        score -= 500
    return score


def build_report(files: list[FileChange]) -> dict[str, object]:
    rows = []
    reference_set: set[str] = set()
    for file in files:
        area, tags, refs = classify(file)
        reference_set.update(refs)
        rows.append(
            {
                "path": file.path,
                "area": area,
                "additions": file.additions,
                "deletions": file.deletions,
                "hunks": file.hunks,
                "tags": tags,
                "references": refs,
                "priority": priority(tags, file),
            }
        )
    rows.sort(key=lambda item: (-int(item["priority"]), str(item["path"])))
    totals = {
        "files": len(files),
        "additions": sum(file.additions for file in files),
        "deletions": sum(file.deletions for file in files),
        "hunks": sum(file.hunks for file in files),
    }
    return {"totals": totals, "references": sorted(reference_set), "files": rows}


def print_markdown(report: dict[str, object]) -> None:
    totals = report["totals"]
    assert isinstance(totals, dict)
    refs = report["references"]
    files = report["files"]
    print("# Diff Triage")
    print()
    print(f"- Files: {totals['files']}")
    print(f"- Additions: {totals['additions']}")
    print(f"- Deletions: {totals['deletions']}")
    print(f"- Hunks: {totals['hunks']}")
    print(f"- Recommended references: {', '.join(refs) if refs else '-'}")
    print()
    print("## Review Order")
    print()
    print("| File | Area | +/- | Hunks | Risk tags | References |")
    print("| --- | --- | ---: | ---: | --- | --- |")
    for item in files:
        assert isinstance(item, dict)
        delta = f"+{item['additions']} / -{item['deletions']}"
        print(
            "| {path} | {area} | {delta} | {hunks} | {tags} | {refs} |".format(
                path=item["path"],
                area=item["area"],
                delta=delta,
                hunks=item["hunks"],
                tags=", ".join(item["tags"]),
                refs=", ".join(item["references"]),
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage a git diff for pd-review.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--staged", action="store_true", help="Read staged diff from git when stdin is empty.")
    args = parser.parse_args()

    stdin_text = sys.stdin.read()
    diff_text = stdin_text if stdin_text.strip() else get_git_diff(staged=args.staged)
    files = parse_diff(diff_text)
    report = build_report(files)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_markdown(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
