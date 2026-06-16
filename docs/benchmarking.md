# Benchmarking

qwerdf has two evaluation layers: deterministic trigger preflight and real agent execution benchmark.

中文：trigger preflight 是本地确定性检查；benchmark runner 才是实际 agent 执行评估。

## Files

- Trigger cases: `evals/cases/trigger-queries.json`
- Execution cases: `evals/cases/benchmark-cases.json`
- Fixtures: `evals/fixtures/`
- Generated reports: `evals/reports/`
- Generated runs: `evals/runs/`

`evals/reports/` and `evals/runs/` are ignored by Git.

## Trigger Preflight

Run the deterministic router check:

```bash
python3 scripts/preflight_triggers.py --strict --format summary
```

Write default reports:

```bash
python3 scripts/preflight_triggers.py --strict --write-default-reports
```

This writes:

```text
evals/reports/trigger-preflight-report.json
evals/reports/trigger-preflight-report.md
```

Trigger preflight is not a model benchmark. It approximates routing from frontmatter descriptions and trigger examples.

## Execution Benchmark

Dry-run previews commands and output layout:

```bash
python3 scripts/run_skill_benchmark.py --dry-run
```

Real execution uses Codex CLI by default. 真实执行会调用外部 agent 命令，不会模拟产物：

```bash
python3 scripts/run_skill_benchmark.py \
  --repetitions 3 \
  --timeout-seconds 900 \
  --strict
```

Run a no-skill baseline:

```bash
python3 scripts/run_skill_benchmark.py \
  --run-baseline \
  --repetitions 3 \
  --timeout-seconds 900 \
  --strict
```

Select cases:

```bash
python3 scripts/run_skill_benchmark.py --list-cases
python3 scripts/run_skill_benchmark.py --dry-run --case pd-fe-single-slice-reporting
python3 scripts/run_skill_benchmark.py --dry-run --skill pd-fe
```

Custom command templates may use:

- `$prompt_file`
- `$output_dir`
- `$case_id`
- `$skill`
- `$skill_path`
- `$last_message_file`

## Case Assertions

`evals/cases/benchmark-cases.json` supports:

- `expected_files`
- `all_contains` / `required_contains`
- `any_contains`
- `forbidden_contains`
- `forbidden_files`
- `check_commands`

## Run Layout

Dry-run creates:

```text
evals/runs/<timestamp>/
  benchmark.json
  benchmark.md
  baseline/
    <case-id>/
      rep-01/
        prompt.md
        command.json
        stdout.txt
        stderr.txt
        outputs/
  with_skill/
    <case-id>/
      rep-01/
        prompt.md
        command.json
        stdout.txt
        stderr.txt
        outputs/
```

Real execution also creates `last-message.txt` and `checks/` when applicable.

## Notes

- Baseline runs do not copy qwerdf skills.
- With-skill runs copy the target skill and `qwerdf-common` under the case output directory.
- The runner does not simulate agent outputs or fabricate pass rates.
