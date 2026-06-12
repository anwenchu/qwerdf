#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from string import Template


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "benchmark-cases.json"
DEFAULT_RUNS_DIR = ROOT / "evals" / "runs"
SKILLS_DIR = ROOT / "skills"
SKILL_MANIFEST = SKILLS_DIR / "manifest.txt"


@dataclass
class CommandResult:
    label: str
    exit_code: int
    duration_seconds: float
    stdout_path: Path
    stderr_path: Path
    output_dir: Path
    passed: bool
    timed_out: bool
    checks: list[dict[str, object]]


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_template(template: str, values: dict[str, str]) -> str:
    return Template(template).safe_substitute(values)


def read_skill_names() -> list[str]:
    names: list[str] = []
    for raw_line in SKILL_MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def safe_relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return path


def copy_skill_bundle(skill: str, output_dir: Path) -> Path:
    skills_target = output_dir / "__skills"
    skills_target.mkdir(parents=True, exist_ok=True)
    for name in ("qwerdf-common", skill):
        src = SKILLS_DIR / name
        dest = skills_target / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    return skills_target / skill


def create_run_dir(runs_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for index in range(100):
        suffix = "" if index == 0 else f"-{index:02d}"
        candidate = runs_dir / f"{timestamp}{suffix}"
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError(f"could not create unique run directory under {runs_dir}")


def materialize_setup_files(case: dict[str, object], output_dir: Path) -> None:
    setup_files = case.get("setup_files", {})
    if not isinstance(setup_files, dict):
        return
    for relative, content in setup_files.items():
        target = output_dir / safe_relative_path(str(relative))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(content), encoding="utf-8")


def materialize_fixture_dirs(case: dict[str, object], output_dir: Path) -> None:
    fixture_dirs = case.get("fixture_dirs", {})
    if not isinstance(fixture_dirs, dict):
        return
    for source, destination in fixture_dirs.items():
        src = ROOT / safe_relative_path(str(source))
        dest = output_dir / safe_relative_path(str(destination))
        if not src.is_dir():
            raise FileNotFoundError(f"fixture dir not found: {src}")
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest)


def case_prompt(case: dict[str, object], output_dir: Path, skill_dir: Path | None) -> str:
    prompt = str(case["prompt"]).strip()
    case_id = str(case["id"])
    expected_files = case.get("expected_files", [])
    expected_text = "\n".join(f"- {item}" for item in expected_files)

    if skill_dir is not None:
        skill_block = f"""Target skill:
- Skill directory: `{skill_dir}`
- First read `{skill_dir / "SKILL.md"}` completely.
- Follow that skill and its linked common files before acting.
"""
    else:
        skill_block = """Baseline mode:
- Do not read qwerdf skill files.
- Solve from the user prompt and visible benchmark files only.
"""

    return f"""{prompt}

Benchmark constraints:
- Case id: `{case_id}`.
- Write all benchmark artifacts under this output directory: `{output_dir}`.
- Do not write benchmark artifacts outside that output directory.
- Preserve any setup or fixture files unless the task explicitly requires editing them.
{skill_block}
Expected files:
{expected_text}
"""


def build_codex_command(args: argparse.Namespace, output_dir: Path, last_message_path: Path) -> list[str]:
    command = [
        args.codex_bin,
        "exec",
        "-C",
        str(output_dir),
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--ask-for-approval",
        "never",
        "--ephemeral",
        "--output-last-message",
        str(last_message_path),
    ]
    if args.model:
        command.extend(["--model", args.model])
    command.append("-")
    return command


def build_custom_command(command_template: str, values: dict[str, str]) -> list[str]:
    return shlex.split(render_template(command_template, values))


def run_process(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    stdin_text: str,
    stdout_path: Path,
    stderr_path: Path,
    timeout_seconds: int,
) -> tuple[int, float, bool]:
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
    except FileNotFoundError as exc:
        duration = time.monotonic() - started
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"Failed to start command: {exc}\n", encoding="utf-8")
        return 127, duration, False
    except PermissionError as exc:
        duration = time.monotonic() - started
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"Failed to start command: {exc}\n", encoding="utf-8")
        return 126, duration, False

    timed_out = False
    try:
        stdout_text, stderr_text = process.communicate(stdin_text, timeout=timeout_seconds)
        exit_code = process.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout_text, stderr_text = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout_text, stderr_text = process.communicate()
        exit_code = 124
        stderr_text = f"{stderr_text}\nTimed out after {timeout_seconds} seconds.\n"

    duration = time.monotonic() - started
    stdout_path.write_text(stdout_text or "", encoding="utf-8")
    stderr_path.write_text(stderr_text or "", encoding="utf-8")
    return exit_code, duration, timed_out


def run_check_commands(
    case: dict[str, object],
    output_dir: Path,
    run_dir: Path,
    timeout_seconds: int,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    commands = case.get("check_commands", [])
    if not isinstance(commands, list):
        return checks

    checks_dir = run_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    for index, raw_command in enumerate(commands, start=1):
        command = shlex.split(str(raw_command))
        stdout_path = checks_dir / f"check-{index}.stdout.txt"
        stderr_path = checks_dir / f"check-{index}.stderr.txt"
        exit_code, duration, timed_out = run_process(
            command,
            cwd=output_dir,
            env=os.environ.copy(),
            stdin_text="",
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            timeout_seconds=timeout_seconds,
        )
        checks.append(
            {
                "text": f"check command passed: {raw_command}",
                "passed": exit_code == 0 and not timed_out,
                "evidence": {
                    "exit_code": exit_code,
                    "timed_out": timed_out,
                    "duration_seconds": duration,
                    "stdout": str(stdout_path),
                    "stderr": str(stderr_path),
                },
            }
        )
    return checks


def contains_checks(
    *,
    case: dict[str, object],
    output_dir: Path,
    key: str,
    mode: str,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    rules = case.get(key, {})
    if not isinstance(rules, dict):
        return checks

    for relative, snippets in rules.items():
        path = output_dir / safe_relative_path(str(relative))
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if not isinstance(snippets, list):
            continue
        if mode == "any":
            passed = any(str(snippet) in text for snippet in snippets)
            checks.append(
                {
                    "text": f"{relative} contains any of {snippets!r}",
                    "passed": passed,
                    "evidence": str(path),
                }
            )
        else:
            for snippet in snippets:
                passed = str(snippet) in text
                checks.append(
                    {
                        "text": f"{relative} contains {snippet!r}",
                        "passed": passed,
                        "evidence": str(path),
                    }
                )
    return checks


def forbidden_contains_checks(
    *,
    case: dict[str, object],
    output_dir: Path,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    rules = case.get("forbidden_contains", {})
    if not isinstance(rules, dict):
        return checks

    for relative, snippets in rules.items():
        path = output_dir / safe_relative_path(str(relative))
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if not isinstance(snippets, list):
            continue
        for snippet in snippets:
            passed = str(snippet) not in text
            checks.append(
                {
                    "text": f"{relative} does not contain {snippet!r}",
                    "passed": passed,
                    "evidence": str(path),
                }
            )
    return checks


def grade_output(
    case: dict[str, object],
    output_dir: Path,
    exit_code: int,
    timed_out: bool,
    command_checks: list[dict[str, object]],
) -> tuple[bool, list[dict[str, object]]]:
    checks: list[dict[str, object]] = [
        {
            "text": "agent command exited successfully",
            "passed": exit_code == 0 and not timed_out,
            "evidence": f"exit_code={exit_code}, timed_out={timed_out}",
        }
    ]

    for relative in case.get("expected_files", []):
        path = output_dir / safe_relative_path(str(relative))
        passed = path.exists() and path.is_file() and path.stat().st_size > 0
        checks.append(
            {
                "text": f"expected file exists: {relative}",
                "passed": passed,
                "evidence": str(path),
            }
        )

    checks.extend(contains_checks(case=case, output_dir=output_dir, key="all_contains", mode="all"))
    checks.extend(contains_checks(case=case, output_dir=output_dir, key="required_contains", mode="all"))
    checks.extend(contains_checks(case=case, output_dir=output_dir, key="any_contains", mode="any"))
    checks.extend(forbidden_contains_checks(case=case, output_dir=output_dir))

    forbidden_files = case.get("forbidden_files", [])
    for relative in forbidden_files if isinstance(forbidden_files, list) else []:
        path = output_dir / safe_relative_path(str(relative))
        checks.append(
            {
                "text": f"forbidden file absent: {relative}",
                "passed": not path.exists(),
                "evidence": str(path),
            }
        )

    checks.extend(command_checks)
    return all(bool(check["passed"]) for check in checks), checks


def run_one(
    *,
    label: str,
    args: argparse.Namespace,
    command_template: str | None,
    case: dict[str, object],
    run_dir: Path,
    include_skill: bool,
    dry_run: bool,
) -> CommandResult:
    output_dir = run_dir / label / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    materialize_setup_files(case, output_dir)
    materialize_fixture_dirs(case, output_dir)
    skill_dir = copy_skill_bundle(str(case["skill"]), output_dir) if include_skill else None

    prompt = case_prompt(case, output_dir, skill_dir)
    prompt_file = run_dir / label / "prompt.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(prompt, encoding="utf-8")

    last_message_path = run_dir / label / "last-message.txt"
    values = {
        "prompt_file": str(prompt_file),
        "output_dir": str(output_dir),
        "case_id": str(case["id"]),
        "skill": str(case["skill"]),
        "skill_path": str(skill_dir or ""),
        "last_message_file": str(last_message_path),
    }

    if command_template:
        command = build_custom_command(command_template, values)
    else:
        command = build_codex_command(args, output_dir, last_message_path)

    stdout_path = run_dir / label / "stdout.txt"
    stderr_path = run_dir / label / "stderr.txt"
    (run_dir / label / "command.json").write_text(json.dumps(command, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if dry_run:
        stdout_path.write_text("DRY RUN:\n" + " ".join(shlex.quote(part) for part in command) + "\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        checks = [
            {
                "text": "dry run only; command was not executed",
                "passed": False,
                "evidence": str(run_dir / label / "command.json"),
            }
        ]
        return CommandResult(label, 0, 0.0, stdout_path, stderr_path, output_dir, False, False, checks)

    env = os.environ.copy()
    env.update(
        {
            "QWERDF_BENCH_PROMPT_FILE": str(prompt_file),
            "QWERDF_BENCH_OUTPUT_DIR": str(output_dir),
            "QWERDF_BENCH_CASE_ID": str(case["id"]),
            "QWERDF_BENCH_SKILL": str(case["skill"]),
            "QWERDF_BENCH_SKILL_PATH": str(skill_dir or ""),
        }
    )
    exit_code, duration, timed_out = run_process(
        command,
        cwd=output_dir,
        env=env,
        stdin_text=prompt,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        timeout_seconds=args.timeout_seconds,
    )
    command_checks = run_check_commands(case, output_dir, run_dir / label, args.check_timeout_seconds)
    passed, checks = grade_output(case, output_dir, exit_code, timed_out, command_checks)
    return CommandResult(label, exit_code, duration, stdout_path, stderr_path, output_dir, passed, timed_out, checks)


def result_to_dict(result: CommandResult) -> dict[str, object]:
    return {
        "label": result.label,
        "exit_code": result.exit_code,
        "duration_seconds": result.duration_seconds,
        "stdout_path": str(result.stdout_path),
        "stderr_path": str(result.stderr_path),
        "output_dir": str(result.output_dir),
        "passed": result.passed,
        "timed_out": result.timed_out,
        "checks": result.checks,
    }


def summarize_runs(runs: list[dict[str, object]]) -> dict[str, object]:
    durations = [float(run["duration_seconds"]) for run in runs]
    passed = sum(1 for run in runs if run["passed"])
    return {
        "total": len(runs),
        "passed": passed,
        "pass_rate": passed / len(runs) if runs else 0.0,
        "duration_mean_seconds": mean(durations) if durations else 0.0,
        "duration_std_seconds": pstdev(durations) if len(durations) > 1 else 0.0,
    }


def filter_cases(
    cases: list[dict[str, object]],
    *,
    case_ids: list[str] | None,
    skill_filters: list[str] | None,
    skill_names: list[str],
) -> list[dict[str, object]]:
    selected = cases
    if case_ids:
        wanted = set(case_ids)
        selected = [case for case in selected if str(case["id"]) in wanted]
    if skill_filters:
        unknown = sorted(set(skill_filters) - set(skill_names))
        if unknown:
            raise ValueError(f"unknown skill filter(s): {', '.join(unknown)}")
        wanted_skills = set(skill_filters)
        selected = [case for case in selected if str(case["skill"]) in wanted_skills]
    if not selected:
        raise ValueError("no benchmark cases matched the requested filters")
    return selected


def render_markdown(report: dict[str, object]) -> str:
    rows = [
        "# Skill Execution Benchmark",
        "",
        f"- Runner: `{report['runner']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Cases: {report['total_cases']}",
        f"- Repetitions: {report['repetitions']}",
        f"- With-skill pass rate: {float(report['with_skill_summary']['pass_rate']) * 100:.1f}%" if report.get("with_skill_summary") else "- With-skill pass rate: not run",
        f"- Baseline pass rate: {float(report['baseline_summary']['pass_rate']) * 100:.1f}%" if report.get("baseline_summary") else "- Baseline pass rate: not run",
        f"- Run dir: `{report['run_dir']}`",
        "",
        "## Results",
        "",
        "| Case | Skill | With skill | Baseline | Mean duration |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for case in report["cases"]:  # type: ignore[index]
        if report.get("dry_run"):
            with_status = "DRY RUN"
        else:
            with_summary = case["with_skill_summary"]
            with_status = f"{with_summary['passed']}/{with_summary['total']}"
        baseline_summary = case.get("baseline_summary")
        if baseline_summary is None:
            baseline_status = "not run"
        elif report.get("dry_run"):
            baseline_status = "DRY RUN"
        else:
            baseline_status = f"{baseline_summary['passed']}/{baseline_summary['total']}"
        rows.append(
            f"| `{case['id']}` | `{case['skill']}` | {with_status} | {baseline_status} | "
            f"{float(case['with_skill_summary']['duration_mean_seconds']):.2f}s |"
        )

    rows.extend(
        [
            "",
            "## Notes",
            "",
            "- Default runner is Codex CLI: `codex exec` with stdin prompt, isolated per-case workspace, and copied skill files.",
            "- The runner executes real commands. It does not simulate an agent or fabricate pass rates.",
            "- With-skill runs read a copied target skill bundle under the case output directory. Baseline runs do not.",
        ]
    )
    if report.get("dry_run"):
        rows.append("- Dry-run writes prompt.md, command.json, stdout.txt, stderr.txt, and outputs/ only; it does not create last-message.txt or checks/.")
    else:
        rows.append("- Inspect each case directory for prompt.md, command.json, stdout.txt, stderr.txt, last-message.txt, outputs/, checks/, and grading results.")
    rows.append("")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run real qwerdf skill execution benchmark cases with Codex CLI by default.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--with-skill-command", help="Custom command template for with-skill runs. Defaults to Codex CLI.")
    parser.add_argument("--baseline-command", help="Optional custom command template for baseline runs without the skill.")
    parser.add_argument(
        "--run-baseline",
        action="store_true",
        help="Run a no-skill baseline with the default Codex CLI runner. Use --baseline-command for custom-agent baselines.",
    )
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--model", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--check-timeout-seconds", type=int, default=120)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--case", dest="case_ids", action="append", help="Run only the matching benchmark case id. Repeatable.")
    parser.add_argument("--skill", dest="skill_filters", action="append", help="Run only cases for this skill name. Repeatable.")
    parser.add_argument("--list-cases", action="store_true", help="List available benchmark cases and exit.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any with-skill repetition fails.")
    args = parser.parse_args()

    if args.repetitions < 1:
        print("--repetitions must be >= 1", file=sys.stderr)
        return 2
    if args.run_baseline and args.with_skill_command and not args.baseline_command:
        print(
            "--run-baseline without --baseline-command can only be used with the default Codex CLI with-skill runner",
            file=sys.stderr,
        )
        return 2

    cases_raw = read_json(args.cases)
    if not isinstance(cases_raw, list):
        print(f"{args.cases}: expected a JSON array", file=sys.stderr)
        return 2
    cases: list[dict[str, object]] = []
    for case in cases_raw:
        if not isinstance(case, dict):
            print("Invalid case entry: expected object", file=sys.stderr)
            return 2
        cases.append(case)

    try:
        skill_names = read_skill_names()
        if args.list_cases:
            for case in cases:
                print(f"{case['id']}\t{case['skill']}")
            return 0
        cases = filter_cases(
            cases,
            case_ids=args.case_ids,
            skill_filters=args.skill_filters,
            skill_names=skill_names,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        run_dir = create_run_dir(args.runs_dir)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    case_reports_by_id: dict[str, dict[str, object]] = {}
    with_skill_runs_all: list[dict[str, object]] = []
    baseline_runs_all: list[dict[str, object]] = []
    baseline_requested = bool(args.run_baseline or args.baseline_command)

    for case in cases:
        case_id = str(case["id"])
        case_reports_by_id[case_id] = {
            "id": case_id,
            "skill": case["skill"],
            "with_skill_runs": [],
            "baseline_runs": [],
        }

    if baseline_requested:
        for case in cases:
            case_id = str(case["id"])
            baseline_runs = case_reports_by_id[case_id]["baseline_runs"]
            if not isinstance(baseline_runs, list):
                print(f"Internal error: invalid baseline run bucket for {case_id}", file=sys.stderr)
                return 2
            for repetition in range(1, args.repetitions + 1):
                suffix = f"rep-{repetition:02d}"
                baseline_result = run_one(
                    label=f"baseline/{case_id}/{suffix}",
                    args=args,
                    command_template=args.baseline_command,
                    case=case,
                    run_dir=run_dir,
                    include_skill=False,
                    dry_run=args.dry_run,
                )
                baseline_dict = result_to_dict(baseline_result)
                baseline_runs.append(baseline_dict)
                baseline_runs_all.append(baseline_dict)

    for case in cases:
        case_id = str(case["id"])
        with_runs = case_reports_by_id[case_id]["with_skill_runs"]
        if not isinstance(with_runs, list):
            print(f"Internal error: invalid with-skill run bucket for {case_id}", file=sys.stderr)
            return 2
        for repetition in range(1, args.repetitions + 1):
            suffix = f"rep-{repetition:02d}"
            with_result = run_one(
                label=f"with_skill/{case_id}/{suffix}",
                args=args,
                command_template=args.with_skill_command,
                case=case,
                run_dir=run_dir,
                include_skill=True,
                dry_run=args.dry_run,
            )
            with_dict = result_to_dict(with_result)
            with_runs.append(with_dict)
            with_skill_runs_all.append(with_dict)

    case_reports: list[dict[str, object]] = []
    for case in cases:
        case_id = str(case["id"])
        report_case = case_reports_by_id[case_id]
        with_runs = report_case["with_skill_runs"]
        baseline_runs = report_case["baseline_runs"]
        if not isinstance(with_runs, list) or not isinstance(baseline_runs, list):
            print(f"Internal error: invalid run bucket for {case_id}", file=sys.stderr)
            return 2
        report_case["with_skill_summary"] = summarize_runs(with_runs)
        report_case["baseline_runs"] = baseline_runs if baseline_runs else None
        report_case["baseline_summary"] = summarize_runs(baseline_runs) if baseline_runs else None
        case_reports.append(report_case)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner": "codex-cli" if not args.with_skill_command else "custom-command",
        "run_dir": str(run_dir),
        "cases_file": str(args.cases),
        "dry_run": args.dry_run,
        "repetitions": args.repetitions,
        "total_cases": len(case_reports),
        "case_filters": args.case_ids or [],
        "skill_filters": args.skill_filters or [],
        "with_skill_summary": None if args.dry_run else summarize_runs(with_skill_runs_all),
        "baseline_summary": None if args.dry_run or not baseline_runs_all else summarize_runs(baseline_runs_all),
        "cases": case_reports,
    }

    write_json(run_dir / "benchmark.json", report)
    (run_dir / "benchmark.md").write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))

    if args.strict and not args.dry_run and any(not run["passed"] for run in with_skill_runs_all):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
