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

The product skills use `skills/qwerdf-common/scripts/product_artifacts.py` (Python 3.10+, standard library). `context --stage <name>` covers all 13 stages (vet, prd, blueprint, figma, ui-review, plan, fe, be, sync, test, review, git, release) and selects rules (including shared safety boundaries) and templates from their canonical common files; do not duplicate those templates in references. `validate --stage vet|prd --root <artifact-root>` is read-only and checks completeness and references, not business truth or product approval. It reports `BLOCKED` for definite contradictions/business blockers, `REVIEW` for gaps needing human interpretation, and `PASS` when no mechanical issue is detected. Exit 0 includes `REVIEW`; automation claiming a pass must check JSON `status == "PASS"` or `passed == true`.

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

Figma connection selection, task-session reuse and bounded failure handling live in [the shared connection rules](../skills/qwerdf-common/product-delivery-flow.md#figma-连接与会话复用). Design, frontend implementation, planning and UI review consume that same policy. Do not probe every account to discover a usable login, recreate a session for every follow-up/file change, or treat file-access errors as authentication expiry. Actual provider session requirements still apply; a failed initial attempt does not establish a usable session or prohibit bounded recovery after reauthorization. Candidate and handoff templates preserve unknown write outcomes under the shared status definitions; restoring access does not authorize replaying an unverified write. The Figma regression cases include synthetic connection/session scenarios; routine checks do not exercise OAuth, reconnect a live account or establish successful Figma reads/writes.

## Technical Design Evidence and Scope

`skills/qwerdf-common/technical-design-rules.md` owns evidence, scope and design-readiness decisions shared by planning, implementation and review. Frontend and backend implementation run in parallel against the confirmed contract; the [shared parallel-development rules](../skills/qwerdf-common/product-delivery-flow.md#frontend--backend-并行开发规则) own ordered frontend/backend execution, minimal shared-artifact preparation and the distinction between coding prerequisites and cross-end acceptance. Concrete service/protocol and data mappings belong in the relevant design paragraphs; other artifacts reference them. Record existing facts, proposals and unresolved decisions separately. Read-only impact investigation does not authorize adding unrelated work to the plan or slices; do not infer a mandatory dependency upgrade from one inspected artifact.

[Engineering omissions and business decisions](../skills/qwerdf-common/technical-design-rules.md#工程漏项与业务决策分类) are classified at the shared source before planning or implementation asks for a decision. Check the confirmed requirement, contract and actual parameter path first; repair evidenced in-scope implementation omissions, or revise the plan/contract through its owner without treating that internal handoff as a new user approval. Unresolved business choices, required unavailable inputs and identity/funds checks retain their existing boundaries. Phone cases cover collection, forwarding and the provider's actual lookup, rather than treating a request field as proof of safe identity matching.

[Business execution and progress rules](../skills/qwerdf-common/product-delivery-flow.md#业务推进阻断恢复与进度汇报) own milestone-oriented task choice, blocked-task recovery and evidence-based progress reporting. Planning uses the existing implementation-order paragraphs; task descriptions reference the milestone or acceptance criterion. Frontend/backend logs and summaries use the shared progress template in `engineering-contracts.md`. Recheck the original blocking reasons and current contracts/dependencies before resuming; slice counts and local test totals do not measure business completion. No new command, status vocabulary or percentage grader is introduced.

[Task lists and execution order](../skills/qwerdf-common/product-delivery-flow.md#任务清单与开发顺序) define a single task authority and an actual `tech/task-slices.md` delivery. Markdown is the default authority; an existing JSON consumer can retain JSON as the authority, with Markdown derived from it. Do not require a second format or migrate an existing schema solely for this workflow. Resolve existing conflicts from declared ownership, actual consumers and implementation/verification evidence; failed view refresh does not undo a successful authoritative update. Plan independently verifiable business increments and necessary preparation outputs, preserve existing implementation evidence, and keep each endpoint's order and status in that same authority. The task template uses two ordered lists without bidirectional dependency columns, parallel markers or mandatory contract tasks; contract readiness is established at design handoff. Legacy fields required by existing tools are not silently deleted or allowed to substitute for actual input checks. Scope each integration gate to its actual result and prerequisites. Implementations update their own authoritative entries, refresh views and derive counts from that source. An authorized batch continues past local blockers without relaxing real coding inputs, validation requirements or external-operation permissions. [Task-source snapshots](../evals/fixtures/technical-design/task-authority-inputs.md) provide consistent and conflicting synthetic JSON/Markdown inputs; they do not exercise a real scheduler or prove model decisions.

[Artifact lifecycle and recovery](../skills/qwerdf-common/artifact-lifecycle.md) own current-document updates, size review, incremental evidence and the short resume entry. The shared flow table is the sole stage-output catalog. Size budgets trigger review and task/topic decomposition rather than truncation or an automatic failure; essential contracts, safety backups and verification evidence remain required. Reuse the existing artifact entry instead of another status ledger, and recheck authoritative facts when resuming. All stage context extraction includes the common work rules; manual fallbacks reference the same source. [Lifecycle cases](../evals/fixtures/artifact-lifecycle/cases.md) cover large tasks, valid exceptions, stale entries, evidence reuse, parallel updates and read-only/cleanup boundaries. They are semantic review inputs, not claims of live project cleanup or model execution.

[Technical design cases](../evals/fixtures/technical-design/cases.md) provide synthetic contract, caller and configuration evidence plus positive/negative cases for missing semantics, new interfaces, duplicate classes, runtime uncertainty, scope changes and planning-to-implementation handoff. Design review is read-only; stale completion labels do not override newly discovered gaps. Explicit phased delivery can proceed only within its agreed independent scope. Judge whether the cited evidence actually supports the decision and whether each proposed change is necessary for the confirmed request. These cases require semantic review, not keyword grades or a forced universal schema; their existence and the repository's static checks do not count as real model execution or service verification.

Java coding guidance is maintained in `qwerdf-common/java-coding-rules.md`, with source/version and adaptation decisions in `java-coding-sources.md`. Java persistence design, implementation and backend review read that shared source directly, without a separate skill command. The team's MyBatis Mapper / XML choice is distinct from Alibaba handbook requirements. [Java positive/negative cases](../evals/fixtures/java-coding/cases.md) cover precision, representation equality, collection mutability, Mapper / XML binding, transaction preservation, retries, compatibility and scope. These are manual semantic review inputs, not automated grading or proof of model behavior.

`evals/fixtures/java-coding/LockCacheProbe.java` preserves the isolated MyBatis 3.5.17 / H2 2.3.232 reproduction and controls: a cached locking read, an uncached locking read (including repeated reads in the same transaction and lock release), and an ordinary cached read. Compile it for Java 11 into a temporary directory using existing jars on the classpath, then run `LockCacheProbe`. It uses only an in-memory database and asserts competing-write results; no dependency download or production connection is required. This proves the bounded cache/lock example, not Spring wiring, business-MySQL behavior or model execution. Routine Python tests do not run this Java probe.

## Shared gates and engineering context

Shared gate definitions live in `product-delivery-flow.md`: applicability, design handoff, runnable checks versus formal acceptance, and commit/release readiness. Entries and report templates reference these owners. Early testing and read-only review do not imply overall acceptance. Task coverage and state always come from the declared authority, including when a derived Markdown view is stale.

`context --stage plan --area backend` (or `frontend`) selects one endpoint's templates for a confirmed single-end scope. Default plan includes both ends. This is a context filter, not permission to drop actual cross-end impacts. Other engineering stages load their own templates and applicable shared rules; UI, Java and Figma operational references remain conditional. Without Python, read the same named common sections and template blocks manually. `validate --stage vet|prd` remains product-only: engineering context extraction is not an engineering acceptance validator.

`validate_skills.py` checks manifest/frontmatter, local links, exact retired identifiers and executable context routes / template sections. It does not require repeated prose fragments in every consumer, reject normal Chinese words, or prove rule semantics. `test_skill_structure.py` covers current-plugin / legacy-name pairs, missing context inputs, endpoint selection and read-only CLI behavior. W1–W24 in the technical-design fixture are paired semantic review cases; review them before claiming workflow quality.

Selected runtime rule sections, including nested sections, must contain actual content. The context helper reuses its Markdown reader and content check; it accepts short references, populated tables and code bodies without prescribing wording or length. Blank headings, comments and empty code/table scaffolding do not satisfy the check. Output templates retain unfilled fields; this rule check is not a generated-document completeness validator or a proof of rule semantics.

SQL files are declared by each benchmark case's applicable inputs and `expected_files`, rather than forced by the skill name. The no-SQL plan/release cases omit the plan and prohibit generating an unnecessary one; existing SQL cases keep their declared-file checks. Regression tests exercise both no-SQL schema acceptance and missing-file rejection for declared SQL outputs. Benchmark file grading does not establish whether a real request involves SQL; review the source scope and the design evidence. Review's formal readiness decisions reference the shared gate, including genuine integration passes and justified non-applicability.

Heading extraction and rule-body validation share actual section spans, including Markdown ATX headings indented by up to three spaces. Duplicate headings retain separate spans; validating one occurrence does not look up the first occurrence by name. Nonempty nested containers and legitimate duplicate headings remain supported; code/comment examples do not create heading boundaries.

`forbidden_files` is optional and defaults to an empty array. When present, it must be an array of nonempty relative path strings; absolute paths, parent traversal, root-only paths and NUL characters are rejected. This field does not force canonical artifact directories or prohibit ordinary filenames, Unicode, spaces or `./` prefixes. `scripts/benchmark_contracts.py` owns this check for both the validator and runner. The CLI reports invalid configuration before materializing a run; direct execution and grading entrypoints reject it as well, instead of treating invalid values as no forbidden files.

Fence closure requires matching characters, sufficient marker length and only trailing spaces/tabs; non-closing prefix lines remain code. Forbidden-path grading checks path presence including dangling symlinks, without changing relative-path configuration rules. Regression pairs cover both boundaries and valid controls.

Confirmed modification repositories, development branches and second-party package development versions are owned by the repository/branch section of `technical-design-rules.md` and recorded once in the technical plan. Plan, frontend and backend contexts load that same section; entries reference it. Changed package consumers use the provider repository's confirmed branch-derived version, not their own branch. Unchanged packages and third-party dependencies are outside this version rule, and version confirmation is separate from artifact readiness or publication permission. Existing planning benchmark inputs now supply synthetic confirmed scope/branches; executable fixture cases explicitly permit preparing a temporary Git repository when absent. No real model benchmark, repository initialization or artifact publication is performed by routine checks. W20–W24 require semantic review; loading the text does not prove a model followed it.
