# Development

This guide is for maintainers changing or adding qwerdf skills.

中文：维护 skill 时要保持触发边界清晰、共享规则可复用、校验可重复。

## Skill Layout

Each skill lives directly under `skills/`:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/   # optional
  scripts/      # optional
```

Do not add per-skill README files. Keep user-facing repository documentation in `docs/` and keep long reusable skill rules in `references/` or `skills/qwerdf-common/`.

## Adding or Renaming a Skill

1. Add the skill directory under `skills/`.
2. Add the skill name to `skills/manifest.txt`.
3. Add or update trigger examples in `evals/cases/trigger-queries.json`.
4. Add or update benchmark coverage in `evals/cases/benchmark-cases.json`.
5. Add `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt`.
6. Keep shared templates in `skills/qwerdf-common/` instead of duplicating long instructions.

## SKILL.md Rules

- Frontmatter must contain only `name` and `description`.
- `description` must explain what the skill does and when to use it; include `$skill-name`.
- Keep `SKILL.md` focused on core workflow and routing.
- Move long checklists, templates, and language/framework details into references or common files.
- Use relative links from the skill to `../qwerdf-common/...` for shared rules.

## Validation

Run these before submitting changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
python3 scripts/run_skill_benchmark.py --dry-run --run-baseline
bash scripts/install.sh --dry-run
```

After editing skills, rerun `bash scripts/install.sh`. In the default live symlink mode, `Already installed as live symlink` means the installed skill points at this repository and the edit is effective. If you intentionally installed with `--copy`, rerun `bash scripts/install.sh --copy` to refresh qwerdf-owned copies, or use `--copy --force` / `--force` when switching between copy and symlink mode.

If you changed Python scripts:

```bash
python3 -m py_compile scripts/validate_skills.py scripts/preflight_triggers.py scripts/run_skill_benchmark.py scripts/validate_codex_install.py
```

Generated reports and runs belong under ignored directories:

- `evals/reports/`
- `evals/runs/`

Do not commit secrets, local credentials, generated benchmark runs, private workspace state, or `pd-work/` outputs.

## Product Skill Checks

The product skills use `skills/qwerdf-common/scripts/product_artifacts.py` (Python 3.10+, standard library). `context --stage vet|prd|blueprint|ui-review` selects rules (including shared safety boundaries) and templates from their canonical common files; do not duplicate those templates in references. `validate --stage vet|prd --root <artifact-root>` is read-only and checks completeness and references, not business truth or product approval. It reports `BLOCKED` for definite contradictions/business blockers, `REVIEW` for gaps needing human interpretation, and `PASS` when no mechanical issue is detected. Exit 0 includes `REVIEW`; automation claiming a pass must check JSON `status == "PASS"` or `passed == true`.

After changing product rules, templates or the helper, run:

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/validate_skills.py
python3 scripts/preflight_triggers.py --strict --format summary
```

Add cases for accepted existing IDs/equivalent formats, review hints such as missing permission coverage, and real blockers such as dangling AC references, unconfirmed sources and unresolved critical questions. Keep AC → requirement mapping authoritative in acceptance criteria; reverse lists and coverage matrices are optional. Preserve old artifacts; unavailable Python or unsupported formats allow documented equivalent human checks. Do not fill unknown business rules merely to make validation pass. See [Product Skills](product-skills.md) for sources and evaluation boundaries.

Decision checks review multiple labeled candidates or reasons outside the current judgment section; they do not select the first or last candidate. Question-table checks retain the parser's consumed line numbers so recognized rows cannot hide other visible content. Extra prose (including benign notes) needs interpretation, not a business blocker or a forced format migration.

## UI Skill Checks

UI review applicability, severity and handoff decisions live only in `skills/qwerdf-common/ui-review-rules.md`; quality checks and default design starting points live in `ui-quality-checklist.md`. Screenshot/Figma references describe evidence acquisition, not competing release gates. `context --stage ui-review` selects only core boundaries and the report template; machine checks are not mandatory for screenshot-only inputs.

The UI benchmark fixtures contain six original synthetic browser screenshots plus their HTML, capture script and baseline hashes under `evals/fixtures/ui-review/`. To regenerate them, use a local Node environment with Playwright and Chrome, then run `node evals/fixtures/ui-review/source/capture.cjs` (`QWERDF_CHROME` can select the browser). Generation is optional for normal skill use; it uses local files and no production data. Inspect the images before accepting a changed baseline.

`evals/checks/ui_review.py` checks only fixed benchmark evidence integrity and report consistency; it reuses the common Markdown reader. It is not a validator for user-authored UI reports, does not force their format, and cannot prove the model viewed an image or judged it correctly. Seven fixed scenarios cover CTA occlusion, an approved compact layout, missing evidence, and defective/normal pairs for amount readability and rejected-save feedback. The save pair records a real local form-validation rejection in `baseline.json`, not a live API response. The checker only parses report structure, references and known fixture conditions. It does not interpret finding prose or guess whether a no-finding sentence means no harm. Nonempty finding rows (including no-finding placeholders), free text, unsupported formats and ambiguous choices go to `REVIEW`; existing reports need not be rewritten. The benchmark cases carry `review_notes` for human readback. Inspect the actual screenshot and generated findings before reporting a visual result; a runner pass means its automated assertions passed. See [Design Skills](design-skills.md#当前自动校验边界) for the current result contract.

Run `python3 -m unittest discover -s scripts/tests -v` for the reproduced keyword-only false pass, missing/changed images, unsupported evidence claims, screenshot-only exceptions, approved compact layouts and nonblocking P2 behavior. See [Design Skills](design-skills.md) for source adaptations and verification results.

UI checker exit codes are `PASS=0`, `FAIL=1`, `REVIEW=2`; inspect JSON `status`, `mechanical_checks_passed`, `automated_checks_passed` and `review_required`. `REVIEW` is pending interpretation, not a confirmed UI defect or a failed model decision. The generic benchmark runner counts only exit 0 as automatically passed, so REVIEW remains displayed as not automatically passed. Record human readback separately without rewriting runner results; do not describe its binary pass rate as visual accuracy. `PASS` also makes no visual approval claim. This benchmark contract adds no validator or approval gate to ordinary skill use. Do not remove real findings or rewrite old reports to obtain exit 0.

[Handoff and layout cases](../evals/fixtures/ui-review/handoff-and-layout-cases.md) cover direct UI report repair, missing slices, upstream scope changes, insufficient evidence, and three operable mobile-table variants. These are human interpretation cases, separate from the seven fixed automated scenarios. Use the local HTML with browser evidence; do not add keyword grading or count the presence of a report as a correct routing/visual decision. Repair handoff rules live in `ui-review-rules.md`; mobile-table strategy lives in `ui-quality-checklist.md`, with consumers linking to those sources.

[Figma direction cases](../evals/fixtures/figma-directions/cases.md) cover previewing candidates in Figma before selection, explicit local-only requests, existing/delegated choices, destination discovery, partial failures, editable/image previews and scope/QA. Validate actual frame links and screenshots only in an authorized test file; local boards, keyword matches and dry-runs do not prove external writes. Workflow policy is maintained in `pd-figma` Gate 1; templates and shared-flow summaries reference it.

## Technical Design Evidence and Scope

`skills/qwerdf-common/technical-design-rules.md` owns evidence, scope and design-readiness decisions shared by planning, implementation and review. Concrete service/protocol and data mappings belong in the relevant design paragraphs; other artifacts reference them. Record existing facts, proposals and unresolved decisions separately. Read-only impact investigation does not authorize adding unrelated work to the plan or slices; do not infer a mandatory dependency upgrade from one inspected artifact.

[Technical design cases](../evals/fixtures/technical-design/cases.md) provide synthetic contract, caller and configuration evidence plus positive/negative cases for missing semantics, new interfaces, duplicate classes, runtime uncertainty and scope changes. Judge whether the cited evidence actually supports the decision and whether each proposed change is necessary for the confirmed request. These cases require semantic review, not keyword grades or a forced universal schema; their existence and the repository's static checks do not count as real model execution or service verification.
