"""Structural regressions; workflow semantics are reviewed using paired cases."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


contracts = load('benchmark_contracts', ROOT / 'scripts/benchmark_contracts.py')
validator = load('skill_validator', ROOT / 'scripts/validate_skills.py')
context = load('stage_context_tests', ROOT / 'skills/qwerdf-common/scripts/product_artifacts.py')
runner = load('structure_benchmark_runner', ROOT / 'scripts/run_skill_benchmark.py')


class SkillStructureTests(unittest.TestCase):
    def test_current_plugin_and_personal_profile_are_not_legacy(self):
        samples = ('用户可以更新个人资料。', 'Use figma-design-to-code for this operation.',
                   '$figma-design-to-code', 'figma-design-to-code/SKILL.md', 'pd-code-example')
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertIsNone(validator.LEGACY_REFERENCE.search(sample))

    def test_exact_retired_commands_and_paths_are_detected(self):
        for sample in ('$pd-code', '`figma-design`', '../figma-design/SKILL.md',
                       'frontend-handoff.md', '$tb-ui-figma', '../ui-delivery-flow.md', '使用$pd-code生成'):
            with self.subTest(sample=sample):
                self.assertIsNotNone(validator.LEGACY_REFERENCE.search(sample))

    def test_document_scan_accepts_current_references_but_rejects_retired_ones(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'skills').mkdir()
            readme = root / 'README.md'
            with patch.multiple(validator, ROOT=root, SKILLS_DIR=root / 'skills', DOCS_DIR=root / 'docs'):
                readme.write_text('个人资料使用 figma-design-to-code。')
                errors = []
                validator.validate_forbidden_terms(errors)
                self.assertEqual([], errors)
                readme.write_text('运行 $pd-code。')
                validator.validate_forbidden_terms(errors)
                self.assertEqual(1, len(errors))

    def test_every_stage_is_routable_with_its_own_templates(self):
        names = {name.removeprefix('pd-') for name in validator.read_skill_names()}
        self.assertEqual(names, set(context.CONTEXT_ARTIFACTS))
        for stage, paths in context.CONTEXT_ARTIFACTS.items():
            with self.subTest(stage=stage):
                result = context.stage_context(stage)
                self.assertIn(context.section((context.COMMON / 'product-delivery-flow.md').read_text(),
                                              '## 4. 安全与意外最小化'), result)
                for path in paths:
                    self.assertIn(f'## `{path}`', result)
                others = set().union(*context.CONTEXT_ARTIFACTS.values()) - set(paths)
                for path in others:
                    self.assertNotIn(f'## `{path}`', result)
                self.assertNotIn('## 5. 规则来源', result)

    def test_backend_plan_omits_frontend_templates_and_ui_gate(self):
        result = context.stage_context('plan', area='backend')
        self.assertIn('## `tech/tech-plan.md`', result)
        self.assertNotIn('## `tech/backend/backend-design.md`', result)
        self.assertIn('## `tech/task-slices.md`', result)
        self.assertNotIn('## `tech/api-contract.md`', result)
        self.assertNotIn('## `tech/frontend/', result)
        self.assertNotIn('### UI 设计系统与质量 Gate', result)
        self.assertNotIn('### Figma 连接与会话复用', result)

    def test_frontend_plan_omits_backend_templates_without_losing_contract(self):
        result = context.stage_context('plan', area='frontend')
        self.assertIn('### UI 设计系统与质量 Gate', result)
        self.assertIn('## `tech/task-slices.md`', result)
        self.assertNotIn('## `tech/api-contract.md`', result)
        self.assertNotIn('## `tech/backend/', result)

    def test_execution_entries_share_business_window_rules_without_per_edit_loop(self):
        """Check loading and entry consistency, not an agent's real execution."""
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        rules = context.section(flow, '### 验证与审查')
        for stage in ('fe', 'be'):
            with self.subTest(stage=stage):
                result = context.stage_context(stage)
                self.assertEqual(1, result.count(rules))
                self.assertLess(result.index('### 验证与审查'), result.index('## 2. 默认工作目录'))
                first_lines = '\n'.join(result.splitlines()[:25])
                self.assertIn('到界先复核收尾，否则退出原循环', first_lines)
                self.assertIn('只读排查或验证也计入', first_lines)
                self.assertIn('不因业务窗口刚耗尽就中断', first_lines)
                skill = (ROOT / 'skills' / f'pd-{stage}' / 'SKILL.md').read_text()
                prompt = (ROOT / 'skills' / f'pd-{stage}' / 'agents/openai.yaml').read_text()
                self.assertIn('共享验证规则', skill)
                self.assertIn('整个修改验证循环的剩余限额', skill)
                self.assertNotIn('每个迭代闭合一个', skill)
                self.assertNotIn('逐片验证并回填状态', prompt)
                self.assertIn('按业务动作集中实现与必要验证', prompt)
        # The rule applies to the whole retry loop and cannot disappear at resume.
        self.assertIn('不只覆盖单条命令', rules)
        self.assertIn('都不自动重置', rules)
        self.assertIn('不标 done', rules)
        self.assertIn('共享资源可用', rules)
        self.assertIn('失败、超时或中断不返还额度', rules)
        self.assertIn('不按工具调用数机械拆轮', rules)
        self.assertIn('收尾不是重新发放整轮额度', rules)
        self.assertIn('不能延长原命令超时', rules)
        self.assertIn('或把新问题接成下一轮收尾', rules)
        self.assertIn('有界采样作为一次整体尝试计数', rules)
        self.assertIn('不重置外层限额', rules)
        progress_rules = context.section(flow, '### 业务推进、阻断恢复与进度汇报')
        self.assertIn('复核必要收尾条件', progress_rules)

    def test_resume_and_progress_templates_keep_existing_window_and_business_gap(self):
        templates = (context.COMMON / 'engineering-contracts.md').read_text()
        lifecycle = (context.COMMON / 'artifact-lifecycle.md').read_text()
        resume = context.section(templates, '## `tech/task-slices.md`')
        progress = context.section(templates, '## 业务进度摘要')
        self.assertIn('剩余验证限额或耗尽后的恢复条件', resume)
        self.assertIn('不因恢复上下文重置', lifecycle)
        self.assertIn('用户询问统计时再按源列本端计数', progress)
        self.assertIn('原业务断点、已执行的分流及实际结果', progress)
        self.assertIn('必要收尾，注明原位范围及退出条件', progress)
        self.assertIn('不覆盖原限额', resume)

    def test_migration_batch_rules_cover_production_and_tests_without_new_ledger(self):
        """Loading/consistency check; paired cases carry the semantic review."""
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        rules = context.section(flow, '### 验证与审查')
        for stage in ('fe', 'be'):
            with self.subTest(stage=stage):
                loaded = context.stage_context(stage)
                self.assertEqual(1, loaded.count(rules))
                entry = (ROOT / 'skills' / f'pd-{stage}' / 'SKILL.md').read_text()
                self.assertIn('共享验证规则核对批次影响面', entry)
                self.assertIn('旧测试同步迁移', entry)
        templates = (context.COMMON / 'engineering-contracts.md').read_text()
        resume = context.section(templates, '## `tech/task-slices.md`')
        self.assertIn('待接通清单的原位引用', resume)
        self.assertIn('不全仓重查', rules)
        self.assertIn('不恢复已作废设计', rules)
        self.assertIn('不删掉仍适用的断言', rules)

    def test_check_reuse_rule_is_loaded_once_for_every_stage(self):
        """Exercise the real context loader; this does not prove agent compliance."""
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        execution = context.section(flow, '## 3. Skill 执行规范', children=False)
        reuse = next(line for line in execution.splitlines()
                     if line.startswith('- 检查围绕本轮交付结果安排'))
        for stage in context.CONTEXT_ARTIFACTS:
            with self.subTest(stage=stage):
                self.assertEqual(1, context.stage_context(stage).count(reuse))
        # Product/design stages do not get the whole engineering validation section.
        for stage in ('vet', 'prd', 'blueprint', 'figma', 'ui-review'):
            self.assertNotIn('### 验证与审查', context.stage_context(stage))

    def test_ui_and_engineering_share_one_loop_core_without_extra_ui_gates(self):
        """Test actual loading, scope and manual fallback links, not agent behavior."""
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        core = context.section(flow, '#### 验证循环与退出')
        engineering = context.section(flow, '#### 工程验证覆盖与证据')
        for stage in ('figma', 'ui-review', 'fe', 'be', 'sync', 'test', 'review'):
            with self.subTest(stage=stage):
                result = context.stage_context(stage)
                self.assertEqual(1, result.count(core))
                if stage in ('figma', 'ui-review'):
                    self.assertLess(result.index(core), result.index('## 2. 默认工作目录'))
                    self.assertNotIn(engineering, result)
                    self.assertNotIn('### 正式提交与上线', result)
                    self.assertNotIn('## `tech/task-slices.md`', result)
                    entry = (ROOT / 'skills' / f'pd-{stage}' / 'SKILL.md').read_text()
                    self.assertIn('product-delivery-flow.md#验证循环与退出', entry)
                else:
                    self.assertEqual(1, result.count(engineering))
        for stage in ('vet', 'prd', 'blueprint'):
            self.assertNotIn(core, context.stage_context(stage))
        templates = (context.COMMON / 'artifact-contracts.md').read_text()
        for path in ('ui/ui-directions.md', 'ui/figma-handoff.md', 'ui/ui-review-report.md'):
            self.assertIn('验证续作（如需；已有记录则引用）',
                          context.section(templates, f'## `{path}`'))

    def test_ui_loop_core_missing_fails_instead_of_silently_dropping_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / 'common'
            shutil.copytree(context.COMMON, common)
            path = common / 'product-delivery-flow.md'
            path.write_text(path.read_text().replace('#### 验证循环与退出',
                                                    '#### Renamed loop rules', 1))
            with patch.object(context, 'COMMON', common):
                for stage in ('figma', 'ui-review'):
                    with self.subTest(stage=stage), self.assertRaisesRegex(ValueError, '缺少章节'):
                        context.stage_context(stage)

    def test_validation_entry_provenance_reaches_all_execution_consumers(self):
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        rules = context.section(flow, '### 验证与审查')
        provenance = next(line for line in rules.splitlines()
                          if line.startswith('- **验证入口与当前产物对应**'))
        self.assertIn('纯编译、类型 / 静态检查', provenance)
        self.assertIn('不强制执行测试断言；执行测试时', provenance)
        self.assertIn('构建通过不能写成测试通过', provenance)
        for stage in ('fe', 'be', 'sync', 'test', 'review'):
            with self.subTest(stage=stage):
                self.assertEqual(1, context.stage_context(stage).count(provenance))
        for stage in ('fe', 'be'):
            entry = (ROOT / 'skills' / f'pd-{stage}' / 'SKILL.md').read_text()
            self.assertIn('本业务批次的检查集合', entry)
            self.assertNotIn('确定本片最小有效检查', entry)
        figma = (ROOT / 'skills/pd-figma/SKILL.md').read_text()
        self.assertNotIn('每个 section 或页面完成后用 Figma 截图验证', figma)
        self.assertIn('每个断点都要截图', figma)

    def test_ordered_task_template_and_handoff_rules_reach_their_consumers(self):
        flow = (context.COMMON / 'product-delivery-flow.md').read_text()
        templates = (context.COMMON / 'engineering-contracts.md').read_text()
        task_template = context.section(templates, '## `tech/task-slices.md`')
        expected_columns = ['顺序', 'ID', '业务动作与交付结果', '状态', '完成标准', '证据 / 阻断']
        tables = [line for line in task_template.splitlines() if line.startswith('| 顺序 |')]
        self.assertEqual(2, len(tables))
        for table in tables:
            self.assertEqual(expected_columns, [cell.strip() for cell in table.strip('|').split('|')])
        for stage in ('plan', 'fe', 'be'):
            with self.subTest(stage=stage):
                result = context.stage_context(stage)
                for title in ('### 任务清单与开发顺序', '### Frontend / Backend 并行开发规则',
                              '### 业务推进、阻断恢复与进度汇报', '### 联调与验收交接'):
                    self.assertEqual(1, result.count(context.section(flow, title)))
                if stage in ('fe', 'be'):
                    self.assertEqual(1, result.count(context.section(flow, '### 验证与审查')))
                    self.assertEqual(1, result.count(context.section(templates, '## 业务进度摘要')))
        result = context.stage_context('sync')
        self.assertIn(context.section(flow, '### 联调与验收交接'), result)
        # Scheduling is not a new requirement for read-only review or an early unit test.
        for stage in ('test', 'review', 'git'):
            result = context.stage_context(stage)
            self.assertIn(context.section(flow, '### 任务清单与开发顺序'), result)
            self.assertNotIn('### Frontend / Backend 并行开发规则', result)

    def test_sync_context_fails_if_its_actual_acceptance_rules_are_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / 'common'
            shutil.copytree(context.COMMON, common)
            path = common / 'product-delivery-flow.md'
            text = path.read_text()
            path.write_text(text.replace('### 联调与验收交接', '### Renamed acceptance rules', 1))
            with patch.object(context, 'COMMON', common), self.assertRaises(ValueError):
                context.stage_context('sync')

    def test_task_source_examples_match_source_order_and_expose_stale_views(self):
        text = (ROOT / 'evals/fixtures/technical-design/task-authority-inputs.md').read_text()
        source = json.loads(text.split('```json\n', 1)[1].split('```', 1)[0])

        def read_view(title):
            block = text.split(title, 1)[1].split('```markdown\n', 1)[1].split('```', 1)[0]
            rows = []
            owner = None
            for line in block.splitlines():
                if line == '## 前端任务':
                    owner = 'frontend'
                elif line == '## 后端任务':
                    owner = 'backend'
                elif line.startswith('| ') and line.split('|')[1].strip().isdigit():
                    order, task_id, task, status, acceptance, evidence = (
                        cell.strip() for cell in line.strip('|').split('|'))
                    rows.append(dict(id=task_id, owner=owner, order=int(order), task=task,
                                     status=status, acceptance=acceptance, evidence=evidence))
            return rows

        expected = sorted(source, key=lambda item: (item['owner'], item['order']))
        fresh = read_view('## 正例：从权威输入刷新后的视图')
        stale = read_view('## 反例：滞后的 Markdown 视图')
        self.assertEqual(expected, sorted(fresh, key=lambda item: (item['owner'], item['order'])))
        self.assertEqual({item['id'] for item in source}, {item['id'] for item in stale})
        self.assertNotEqual(expected, sorted(stale, key=lambda item: (item['owner'], item['order'])))
        stale_by_id = {item['id']: item for item in stale}
        for item in source:
            if item['owner'] == 'backend':
                self.assertNotEqual(item['order'], stale_by_id[item['id']]['order'])
                self.assertNotEqual(item['status'], stale_by_id[item['id']]['status'])

    def test_default_plan_rejects_duplicate_task_store_but_allows_other_json(self):
        cases = json.loads((ROOT / 'evals/cases/benchmark-cases.json').read_text())
        defaults = {'pd-plan-from-design', 'pd-plan-dependency-readiness-required',
                    'pd-plan-backend-no-sql'}
        selected = [case for case in cases if case['id'] in defaults]
        self.assertEqual(defaults, {case['id'] for case in selected})
        for source in selected:
            with self.subTest(case=source['id']), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                (output / 'tech').mkdir()
                (output / 'tech/task-slices.md').write_text('# Tasks\nCurrent task authority.\n')
                # Ordinary API examples may still be JSON; only duplicate task stores are forbidden.
                (output / 'tech/response-example.json').write_text('{"items": []}')
                case = {'expected_files': ['tech/task-slices.md'],
                        'forbidden_files': source.get('forbidden_files', [])}
                self.assertTrue(runner.grade_output(case, output, 0, False, [])[0])
                for relative in ('tech/task-slices.json', 'task-slices.json'):
                    duplicate = output / relative
                    duplicate.write_text('[]')
                    self.assertFalse(runner.grade_output(case, output, 0, False, [])[0], relative)
                    duplicate.unlink()

    def test_all_stages_load_shared_scope_rules_once(self):
        rules = context.section((context.COMMON / 'artifact-lifecycle.md').read_text(), '## 工作规则')
        for stage in context.CONTEXT_ARTIFACTS:
            with self.subTest(stage=stage):
                self.assertEqual(1, context.stage_context(stage).count(rules))
        for area in ('frontend', 'backend'):
            self.assertEqual(1, context.stage_context('plan', area=area).count(rules))

    def test_invalid_stage_or_scope_does_not_silently_fall_back(self):
        for stage, area in [('unknown', 'all'), ('test', 'backend'), ('plan', 'other')]:
            with self.subTest(stage=stage, area=area), self.assertRaises(ValueError):
                context.stage_context(stage, area=area)

    def test_missing_shared_section_or_template_fails_context_extraction(self):
        for filename, title in [('product-delivery-flow.md', '## 4. 安全与意外最小化'),
                                ('engineering-contracts.md', '## `test/test-report.md`')]:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                common = Path(directory) / 'common'
                shutil.copytree(context.COMMON, common)
                path = common / filename
                text = path.read_text()
                path.write_text(text.replace(title, title + ' renamed', 1))
                with patch.object(context, 'COMMON', common), self.assertRaises(ValueError):
                    context.stage_context('test')

    def test_reference_routes_do_not_require_duplicate_prose_and_detect_missing_template(self):
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory) / 'skills'
            shutil.copytree(ROOT / 'skills', skills)
            # Entry prose can be shortened without copying shared gate sentences.
            (skills / 'pd-test/SKILL.md').write_text(
                'Use shared `context --stage \"test\"` and current inputs.\n')
            with patch.multiple(validator, SKILLS_DIR=skills, COMMON_DIR=skills / 'qwerdf-common'):
                errors = []
                validator.validate_reference_guardrails(errors)
                self.assertEqual([], errors)
                templates = skills / 'qwerdf-common/engineering-contracts.md'
                text = templates.read_text()
                templates.write_text(text.replace('## `test/test-report.md`', '## Removed report template'))
                validator.validate_reference_guardrails(errors)
                self.assertTrue(errors)
                self.assertIn('invalid context route', errors[-1])

    def test_engineering_context_is_not_an_engineering_artifact_validator(self):
        script = ROOT / 'skills/qwerdf-common/scripts/product_artifacts.py'
        result = subprocess.run([sys.executable, str(script), 'validate', '--stage', 'be',
                                 '--root', str(ROOT)], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn('invalid choice', result.stderr)

    def test_empty_selected_rules_are_rejected_including_nested_sections(self):
        cases = (
            ('### 正式提交与上线', ''),
            ('### 正式提交与上线', '\n<!-- hidden text -->\n'),
            ('### 正式提交与上线', '\n```text\n\n```\n'),
            ('### 正式提交与上线', '\n| Rule | Evidence |\n| --- | --- |\n'),
            ('### 任务清单与开发顺序', '\n#### Pending rules\n'),
        )
        for title, body in cases:
            with self.subTest(title=title, body=body), tempfile.TemporaryDirectory() as directory:
                common = Path(directory) / 'common'
                shutil.copytree(context.COMMON, common)
                path = common / 'product-delivery-flow.md'
                text = path.read_text()
                path.write_text(text.replace(context.section(text, title), title + body, 1))
                with patch.object(context, 'COMMON', common), self.assertRaisesRegex(ValueError, '正文为空'):
                    context.stage_context('git')
                with patch.object(validator, 'COMMON_DIR', common):
                    errors = []
                    validator.validate_reference_guardrails(errors)
                    self.assertTrue(errors)
                    self.assertIn('正文为空', errors[-1])

    def test_short_references_tables_code_and_container_rules_are_valid(self):
        bodies = (
            '\n按 [既定条件](technical-design-rules.md) 核对当前交接证据。\n',
            '\n| Rule | Evidence |\n| --- | --- |\n| Confirm scope | Current design |\n',
            '\n```python\ncheck_current_evidence()\n```\n',
            '\n```markdown\n| Rule | Evidence |\n| --- | --- |\n| Scope | Design |\n```\n',
            '\n    check_current_evidence()\n',
            '\n#### Conditions\n按当前范围核对必要证据，保留缺口。\n',
        )
        for body in bodies:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                common = Path(directory) / 'common'
                shutil.copytree(context.COMMON, common)
                path = common / 'product-delivery-flow.md'
                text = path.read_text()
                title = '### 正式提交与上线'
                path.write_text(text.replace(context.section(text, title), title + body, 1))
                with patch.object(context, 'COMMON', common):
                    result = context.stage_context('git')
                    self.assertIn(body.strip(), result)
                with patch.object(validator, 'COMMON_DIR', common):
                    errors = []
                    validator.validate_reference_guardrails(errors)
                    self.assertEqual([], errors)

    def test_empty_template_fields_are_not_empty_rule_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / 'common'
            shutil.copytree(context.COMMON, common)
            path = common / 'engineering-contracts.md'
            text = path.read_text()
            title = '## `test/test-report.md`'
            skeleton = title + '\n\n```markdown\n# Report\n## Results\n- Evidence:\n```'
            path.write_text(text.replace(context.section(text, title), skeleton, 1))
            with patch.object(context, 'COMMON', common):
                self.assertIn(skeleton, context.stage_context('test'))

    def test_empty_rules_cannot_borrow_indented_sibling_or_duplicate_bodies(self):
        for body in (
            '\n\n  ### Adjacent rule\nOnly the adjacent rule has content.\n',
            '\n\n#### Conditions\nThe first occurrence has content.\n\n#### Conditions\n',
            '\n\n#### Conditions\n\n#### Conditions\nOnly the second occurrence has content.\n',
        ):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                common = Path(directory) / 'common'
                shutil.copytree(context.COMMON, common)
                path = common / 'product-delivery-flow.md'
                text = path.read_text()
                title = '### 正式提交与上线'
                path.write_text(text.replace(context.section(text, title), title + body, 1))
                with patch.object(context, 'COMMON', common), self.assertRaisesRegex(ValueError, '正文为空'):
                    context.stage_context('git')
                with patch.object(validator, 'COMMON_DIR', common):
                    errors = []
                    validator.validate_reference_guardrails(errors)
                    self.assertTrue(errors)
                    self.assertIn('正文为空', errors[-1])

    def test_indented_and_duplicate_headings_keep_distinct_content(self):
        for indent in range(4):
            with self.subTest(indent=indent):
                text = ('# Root\n' + ' ' * indent + '## Conditions\nFirst rule.\n' +
                        ' ' * indent + '## Conditions\nSecond rule.\n' +
                        '```markdown\n## Example only\n```\n')
                lines = text.splitlines()
                spans = context.section_spans(text)
                duplicates = ['\n'.join(lines[start + 1:end])
                              for title, start, end in spans if title == '## Conditions']
                self.assertEqual(2, len(duplicates))
                self.assertIn('First rule.', duplicates[0])
                self.assertNotIn('Second rule.', duplicates[0])
                self.assertIn('Second rule.', duplicates[1])
                self.assertNotIn('First rule.', duplicates[1])
                self.assertNotIn('Second rule.', context.section(text, '## Conditions'))
                self.assertNotIn('First rule.', context.section(text, '# Root', children=False))
                self.assertNotIn('## Example only', [title for title, _, _ in spans])

    def test_nonempty_duplicate_rule_sections_are_not_forbidden(self):
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / 'common'
            shutil.copytree(context.COMMON, common)
            path = common / 'product-delivery-flow.md'
            text = path.read_text()
            title = '### 正式提交与上线'
            body = '\n\n  #### Conditions\nFirst rule.\n\n   #### Conditions\nSecond rule.\n'
            path.write_text(text.replace(context.section(text, title), title + body, 1))
            with patch.object(context, 'COMMON', common):
                self.assertIn(body.strip(), context.stage_context('git'))
            with patch.object(validator, 'COMMON_DIR', common):
                errors = []
                validator.validate_reference_guardrails(errors)
                self.assertEqual([], errors)

    def test_fence_content_cannot_create_headings_or_swallow_following_sections(self):
        text = ('# Actual section\n\n```text\n``` not a closing fence\n'
                '## Example only\nExample body.\n```\n\n# Next section\nNext body.\n')
        self.assertEqual(['# Actual section', '# Next section'],
                         [title for title, _, _ in context.section_spans(text)])
        self.assertIn('## Example only', context.section(text, '# Actual section'))
        self.assertNotIn('Next body.', context.section(text, '# Actual section'))
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / 'common'
            shutil.copytree(context.COMMON, common)
            path = common / 'product-delivery-flow.md'
            source = path.read_text()
            title = '### 正式提交与上线'
            body = '\n\n```text\n``` not a closing fence\n#### Example only\nExample body.\n```\n'
            path.write_text(source.replace(context.section(source, title), title + body, 1))
            with patch.object(context, 'COMMON', common):
                self.assertIn(body.strip(), context.stage_context('git'))

    def test_fence_closing_requires_matching_length_character_and_whitespace(self):
        for opening, closing in (('```python', '```'), ('````text', '`````'),
                                 ('~~~text', '~~~~~'), ('~~~ format`name', '~~~')):
            for indent in range(4):
                with self.subTest(opening=opening, closing=closing, indent=indent):
                    text = ('# Before\n' + opening + '\n## Code heading\ncode\n' +
                            ' ' * indent + closing + ' \t\n# After\nActual body.\n')
                    self.assertEqual(['# Before', '# After'],
                                     [title for title, _, _ in context.section_spans(text)])
                    self.assertNotIn('Actual body.', context.section(text, '# Before'))
        for non_closing in ('```', '~~~~', '```` extra', '    ````', '\t````', '````\u00a0'):
            with self.subTest(non_closing=non_closing):
                text = ('# Before\n````text\n' + non_closing +
                        '\n## Code heading\ncode\n````\n# After\nActual body.\n')
                self.assertEqual(['# Before', '# After'],
                                 [title for title, _, _ in context.section_spans(text)])
                self.assertIn(non_closing, context.section(text, '# Before'))
        invalid_opening = '# Before\n``` invalid`info\n# After\nActual body.\n'
        self.assertEqual(['# Before', '# After'],
                         [title for title, _, _ in context.section_spans(invalid_opening)])

    def test_confirmed_repo_branch_and_version_rules_load_for_both_ends(self):
        rules = context.section((context.COMMON / 'technical-design-rules.md').read_text(),
                                '### 仓库、分支与二方包版本')
        for stage in ('plan', 'fe', 'be'):
            self.assertEqual(1, context.stage_context(stage).count(rules), stage)
        self.assertEqual(1, context.stage_context('plan', area='backend').count(rules))
        self.assertEqual(1, context.stage_context('plan', area='frontend').count(rules))
        for stage in ('vet', 'prd', 'blueprint', 'figma', 'ui-review'):
            self.assertNotIn(rules, context.stage_context(stage), stage)

    def test_forbidden_path_presence_includes_broken_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / 'forbidden.sql'
            case = {'forbidden_files': ['forbidden.sql']}
            self.assertTrue(runner.grade_output(case, output, 0, False, [])[0])
            path.write_text('Unexpected artifact.')
            self.assertFalse(runner.grade_output(case, output, 0, False, [])[0])
            path.unlink()
            path.mkdir()
            self.assertFalse(runner.grade_output(case, output, 0, False, [])[0])
            path.rmdir()
            target = output / 'present-target.sql'
            target.write_text('Existing target.')
            path.symlink_to(target)
            self.assertFalse(runner.grade_output(case, output, 0, False, [])[0])
            path.unlink()
            path.symlink_to(output / 'missing-target.sql')
            self.assertFalse(path.exists())
            self.assertTrue(path.is_symlink())
            self.assertFalse(runner.grade_output(case, output, 0, False, [])[0])

    def test_invalid_forbidden_files_is_reported_and_cannot_silently_pass(self):
        invalid_values = ('tech/backend/sql-execution-plan.md', None, {}, True, 1,
                          [None], [1], [''], ['   '], ['.'], ['./'],
                          ['/tmp/out.sql'], ['../out.sql'], ['tech/../out.sql'], ['bad\0name'])
        for value in invalid_values:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                cases = json.loads((ROOT / 'evals/cases/benchmark-cases.json').read_text())
                case = next(item for item in cases if item['id'] == 'pd-plan-backend-no-sql')
                case['forbidden_files'] = value
                path = Path(directory)
                (path / 'benchmark-cases.json').write_text(json.dumps(cases))
                with patch.object(validator, 'EVAL_CASES_DIR', path):
                    errors = []
                    validator.validate_benchmark_cases(validator.read_skill_names(), errors)
                    self.assertTrue(errors)
                    self.assertIn('forbidden_files', errors[0])
                with self.assertRaisesRegex(ValueError, 'forbidden_files'):
                    runner.grade_output(case, path, 0, False, [])
                with self.assertRaisesRegex(ValueError, 'forbidden_files'):
                    runner.run_one(label='invalid', args=Namespace(), command_template=None,
                                   case=case, run_dir=path / 'run', include_skill=False, dry_run=False)
                self.assertFalse((path / 'run').exists())

    def test_valid_forbidden_files_preserve_omitted_empty_and_relative_paths(self):
        values = ([], ['plain.sql'], ['./nested/file.sql'], ['目录/文件 with spaces.sql'],
                  ['sql-execution-plan.md'])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            self.assertTrue(runner.grade_output({}, output, 0, False, [])[0])
            for value in values:
                with self.subTest(value=value):
                    self.assertEqual(value, contracts.forbidden_file_paths(value))
                    case = {'forbidden_files': value}
                    self.assertTrue(runner.grade_output(case, output, 0, False, [])[0])
                    if value:
                        target = output / value[0]
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text('Unexpected artifact.')
                        self.assertFalse(runner.grade_output(case, output, 0, False, [])[0])
                        target.unlink()

    def test_invalid_forbidden_files_cli_fails_before_materializing_runs(self):
        for value in ('out.sql', ['../out.sql']):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                path = Path(directory)
                config = path / 'cases.json'
                config.write_text(json.dumps([{'id': 'invalid-config', 'forbidden_files': value}]))
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_skill_benchmark.py'),
                                         '--cases', str(config), '--runs-dir', str(path / 'runs'),
                                         '--dry-run'], capture_output=True, text=True)
                self.assertEqual(2, result.returncode)
                self.assertIn('invalid-config', result.stderr)
                self.assertIn('forbidden_files', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((path / 'runs').exists())

    def test_no_sql_cases_pass_schema_without_forcing_sql_files(self):
        cases = json.loads((ROOT / 'evals/cases/benchmark-cases.json').read_text())
        selected = {case['id']: case for case in cases}
        plan = selected['pd-plan-backend-no-sql']
        release = selected['pd-release-no-sql']
        sql_path = 'tech/backend/sql-execution-plan.md'
        self.assertNotIn(sql_path, plan['expected_files'])
        self.assertNotIn(sql_path, release['setup_files'])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'benchmark-cases.json').write_text(json.dumps(cases))
            with patch.object(validator, 'EVAL_CASES_DIR', path):
                errors = []
                validator.validate_benchmark_cases(validator.read_skill_names(), errors)
                self.assertEqual([], errors)

    def test_no_sql_grading_and_explicit_sql_file_requirements(self):
        cases = json.loads((ROOT / 'evals/cases/benchmark-cases.json').read_text())
        selected = {case['id']: case for case in cases}
        sql_path = 'tech/backend/sql-execution-plan.md'
        for case_id in ('pd-plan-backend-no-sql', 'pd-release-no-sql'):
            with self.subTest(case_id=case_id), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                for relative in selected[case_id]['expected_files']:
                    path = output / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('Synthetic grading input; not a semantic acceptance result.')
                self.assertTrue(runner.grade_output(selected[case_id], output, 0, False, [])[0])
                unexpected = output / sql_path
                unexpected.parent.mkdir(parents=True, exist_ok=True)
                unexpected.write_text('Unnecessary empty-scope SQL plan')
                self.assertFalse(runner.grade_output(selected[case_id], output, 0, False, [])[0])
        # Exercise declared-file grading, independently of prose-based checks.
        expected = selected['pd-plan-dependency-readiness-required']['expected_files']
        self.assertIn(sql_path, expected)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for relative in expected:
                path = output / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('Synthetic declared-file input.')
            self.assertTrue(runner.grade_output({'expected_files': expected}, output, 0, False, [])[0])
            (output / sql_path).unlink()
            passed, checks = runner.grade_output({'expected_files': expected}, output, 0, False, [])
            self.assertFalse(passed)
            self.assertEqual([f'expected file exists: {sql_path}'],
                             [check['text'] for check in checks if not check['passed']])

    def test_plan_context_cli_selects_backend_and_is_read_only(self):
        script = ROOT / 'skills/qwerdf-common/scripts/product_artifacts.py'
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(script), 'context', '--stage', 'plan',
                                     '--area', 'backend'], cwd=directory, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(context.stage_context('plan', area='backend'), result.stdout)
            self.assertEqual([], list(Path(directory).iterdir()))


if __name__ == '__main__':
    unittest.main()
