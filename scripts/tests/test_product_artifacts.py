"""Behavioral checks for product traceability, missing states and selective context."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/qwerdf-common/scripts/product_artifacts.py"
SPEC = importlib.util.spec_from_file_location("product_artifacts", SCRIPT)
product = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(product)


def valid_prd():
    sections = {
        "背景": "运营每天逐条处理异常，手工确认容易遗漏。",
        "目标": "减少遗漏；处理耗时基线尚无数据，不设虚构数值。",
        "用户角色": "运营处理本租户异常，其他租户无权查看。",
        "核心场景": "运营查看待处理异常并标记处理。",
        "功能范围": "REQ-001 标记异常已处理。",
        "非目标范围": "不做自动投放或跨租户查看。",
        "业务规则": "只能处理本租户待处理异常，重复操作不重复变更。",
        "用户流程": "查看异常、确认归属、标记处理、查看状态。",
        "验收标准": "以 product/acceptance-criteria.md 的 AC-001 至 AC-005 为准。",
        "假设与风险": "节省耗时尚无数据，将在试用中验证。",
        "开放问题": "无。",
    }
    prd = "# PRD\n\n## 事实与来源\n| ID | 来源 / 定位 | 事实 / 约束 | 确认状态 |\n| --- | --- | --- | --- |\n| SRC-001 | 用户需求确认记录第 1 条 | 运营仅处理本租户异常 | 已确认 |\n"
    prd += "\n".join(f"\n## {title}\n{body}\n" for title, body in sections.items())
    return {
        "product/prd.md": prd,
        "product/requirements.md": "# 需求清单\n| ID | 需求 | 优先级 | 来源 | 验收标准 |\n| --- | --- | --- | --- | --- |\n| REQ-001 | 标记异常处理结果 | P0 | SRC-001 | AC-001、AC-002、AC-003、AC-004、AC-005 |\n",
        "product/user-stories.md": "# 用户故事\n| 用户角色 | 我想要 | 以便于 | 关联需求 | 验收标准 |\n| --- | --- | --- | --- | --- |\n| 运营 | 标记处理结果 | 避免重复处理 | REQ-001 | AC-001 |\n",
        "product/acceptance-criteria.md": """# 验收标准
## 功能验收
| ID | 关联需求 | 前置条件 | 操作 / 事件 | 预期结果 |
| --- | --- | --- | --- | --- |
| AC-001 | REQ-001 | 本租户待处理异常 | 标记处理 | 异常显示已处理 |
| AC-002 | REQ-001 | 网络不可用 | 标记处理 | 保留待处理状态并提供重试操作 |
| AC-003 | REQ-001 | 其他租户异常 | 打开异常 | 拒绝访问且不返回记录内容 |
| AC-004 | REQ-001 | 已处理异常 | 再次提交 | 保持已处理且不重复产生处理记录 |
| AC-005 | REQ-001 | 已处理异常 | 恢复待处理 | 拒绝非法流转并保持原状态 |
## 业务状态与边界覆盖
| 需求 ID | 正常结果 | 异常与恢复 | 权限与可见性 | 边界与重复操作 | 状态流转 |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | AC-001 | AC-002 | AC-003 | AC-004 | AC-005 |
## 状态验收
页面反馈见 AC-001、AC-002、AC-003。
## 非目标确认
不自动调整广告投放。
""",
        "product/open-questions.md": "# 开放问题\n\n无。\n",
    }


def consolidated_prd():
    """Same source facts and acceptance as the legacy fixture, in one document."""
    docs = valid_prd()
    text = docs['product/prd.md']
    for title, path in (('功能范围', 'product/requirements.md'),
                        ('验收标准', 'product/acceptance-criteria.md'),
                        ('开放问题', 'product/open-questions.md')):
        body = '\n'.join(docs[path].splitlines()[1:])
        body = '\n'.join('#' + line if line.startswith('## ') else line
                         for line in body.splitlines())
        lines = text.splitlines()
        for heading, start, end in product.section_spans(text):
            if heading == f'## {title}':
                lines[start:end] = [heading, body, '']
                text = '\n'.join(lines)
                break
    return {'product/prd.md': text}


class ProductArtifactTests(unittest.TestCase):
    def test_atx_closing_hashes_keep_section_boundaries_and_literal_hashes(self):
        text = "## 第一节 ##\n第一节正文\n## C#\n语言名\n## 第二节 ###\n第二节正文\n"
        self.assertEqual([("## 第一节", 0, 2), ("## C#", 2, 4), ("## 第二节", 4, 6)],
                         product.section_spans(text))
        self.assertEqual("## 第一节 ##\n第一节正文", product.section(text, "## 第一节"))
        escaped = "## 标题 \\##\n正文\n"
        self.assertEqual("## 标题 \\##", product.section_spans(escaped)[0][0])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwerdf-product-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs = valid_prd()

    def check(self, docs=None, stage="prd"):
        for relative, text in (self.docs if docs is None else docs).items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return product.validate(self.root, stage)

    def assert_code(self, code):
        report = self.check()
        self.assertFalse(report["passed"])
        self.assertEqual("BLOCKED", report["status"])
        self.assertIn(code, {issue["code"] for issue in report["issues"]})

    def assert_review(self, code):
        report = self.check()
        self.assertEqual("REVIEW", report["status"])
        self.assertFalse(report["passed"])
        self.assertEqual([], report["issues"])
        self.assertIn(code, {warning["code"] for warning in report["warnings"]})

    def test_complete_traceable_prd_passes(self):
        self.assertTrue(self.check()["passed"])

    def test_consolidated_prd_passes_without_creating_companion_files(self):
        report = self.check(consolidated_prd())
        self.assertEqual('PASS', report['status'], report)
        self.assertEqual(['product/prd.md'],
                         [str(path.relative_to(self.root)) for path in self.root.rglob('*.md')])

    def test_independent_task_roots_keep_validation_and_issue_locations_separate(self):
        project = self.root / 'project'
        project.mkdir()
        (project / 'README.md').write_text('# 项目索引\n[任务一](tasks/first/)\n[独立返工](tasks/rework/)\n')
        first = project / 'tasks/first'
        rework = project / 'tasks/rework'
        for task in (first, rework):
            path = task / 'product/prd.md'
            path.parent.mkdir(parents=True)
            path.write_text(consolidated_prd()['product/prd.md'])
        self.assertEqual('PASS', product.validate(first, 'prd')['status'])
        self.assertEqual('PASS', product.validate(rework, 'prd')['status'])
        path = rework / 'product/prd.md'
        path.write_text(path.read_text().replace('| P0 | SRC-001 |', '| P0 | SRC-999 |', 1))
        before = {path: path.read_bytes() for path in project.rglob('*') if path.is_file()}
        self.assertEqual('PASS', product.validate(first, 'prd')['status'])
        report = product.validate(rework, 'prd')
        self.assertEqual('BLOCKED', report['status'])
        issue = next(item for item in report['issues'] if item['code'] == 'unknown-reference')
        self.assertEqual(str(rework / 'product/prd.md'), issue['file'])
        parent = product.validate(project, 'prd')
        self.assertFalse(parent['passed'])
        self.assertEqual(before, {path: path.read_bytes() for path in project.rglob('*') if path.is_file()})

    def test_consolidated_prd_preserves_blockers_and_actual_locations(self):
        for code, old, new in (
            ('unknown-reference', '| P0 | SRC-001 |', '| P0 | SRC-999 |'),
            ('unconfirmed-source', '| 已确认 |', '| 待确认 |'),
            ('duplicate-id', '| AC-002 |', '| AC-001 |'),
        ):
            with self.subTest(code=code):
                docs = consolidated_prd()
                docs['product/prd.md'] = docs['product/prd.md'].replace(old, new, 1)
                report = self.check(docs)
                self.assertEqual('BLOCKED', report['status'])
                issue = next(item for item in report['issues'] if item['code'] == code)
                self.assertEqual(str(self.root / 'product/prd.md'), issue['file'])
                marker = 'REQ-001' if code == 'unconfirmed-source' else new.strip().strip('|').split('|')[0].strip()
                self.assertIn(marker,
                              docs['product/prd.md'].splitlines()[issue['line'] - 1])

    def test_inline_open_blocker_points_to_its_actual_prd_line(self):
        docs = consolidated_prd()
        question = '| Q-001 | 权限归属待定 | 本期 | 是 | 未解决 | 用户 |'
        docs['product/prd.md'] = docs['product/prd.md'].replace('## 开放问题\n\n无。',
            '## 开放问题\n| ID | 问题 | 影响范围 | 是否阻断 | 状态 | 需要谁确认 |\n'
            '| --- | --- | --- | --- | --- | --- |\n' + question)
        report = self.check(docs)
        issue = next(item for item in report['issues'] if item['code'] == 'open-blocker')
        self.assertEqual('BLOCKED', report['status'])
        self.assertEqual(str(self.root / 'product/prd.md'), issue['file'])
        self.assertEqual(question, docs['product/prd.md'].splitlines()[issue['line'] - 1])

    def test_consolidated_and_split_sources_cannot_silently_disagree(self):
        docs = valid_prd()
        docs['product/prd.md'] = consolidated_prd()['product/prd.md'].replace(
            '| AC-001 | REQ-001 |', '| AC-001 | REQ-002 |', 1)
        report = self.check(docs)
        self.assertEqual('REVIEW', report['status'])
        self.assertIn('ambiguous-artifact-source', {item['code'] for item in report['warnings']})

    def test_duplicate_inline_questions_cannot_hide_a_later_blocker(self):
        docs = consolidated_prd()
        docs['product/prd.md'] += ('\n## 开放问题\n'
            '| ID | 问题 | 影响范围 | 是否阻断 | 状态 | 需要谁确认 |\n'
            '| --- | --- | --- | --- | --- | --- |\n'
            '| Q-002 | 金额口径未定 | 本期 | 是 | 未解决 | 用户 |\n')
        report = self.check(docs)
        self.assertEqual('BLOCKED', report['status'])
        self.assertIn('ambiguous-inline-section', {item['code'] for item in report['warnings']})
        issue = next(item for item in report['issues'] if item['code'] == 'open-blocker')
        self.assertIn('Q-002', docs['product/prd.md'].splitlines()[issue['line'] - 1])

    def test_duplicate_inline_no_questions_declarations_need_review(self):
        docs = consolidated_prd()
        docs['product/prd.md'] += '\n## 开放问题\n无。\n'
        report = self.check(docs)
        self.assertEqual('REVIEW', report['status'])
        self.assertIn('ambiguous-inline-section', {item['code'] for item in report['warnings']})

    def test_existing_split_question_source_does_not_require_summary_rewrite(self):
        docs = valid_prd()
        docs['product/prd.md'] += '\n## 开放问题\n无。\n'
        # The existing independent question file is still the source; repeated
        # summaries without structured conflicting facts do not require migration.
        report = self.check(docs)
        self.assertEqual('PASS', report['status'], report)

    def test_topic_details_keep_traceability_in_the_main_index(self):
        docs = consolidated_prd()
        docs['product/prd.md'] = docs['product/prd.md'].replace(
            '保留待处理状态并提供重试操作', '保持待处理，可重试；[步骤详情](retry-details.md)')
        docs['product/retry-details.md'] = '# 重试说明\n保持既有权限边界，失败不写入已处理状态。\n'
        self.assertEqual('PASS', self.check(docs)['status'])
        docs['product/prd.md'] = '\n'.join(line for line in docs['product/prd.md'].splitlines()
                                         if not line.startswith('| AC-002 |'))
        report = self.check(docs)
        self.assertEqual('BLOCKED', report['status'])
        self.assertIn('unknown-reference', {item['code'] for item in report['issues']})

    def test_single_vet_brief_retains_context_and_decision_checks(self):
        text = '''# 想法简报
## 原始想法
帮助运营减少遗漏。
## 用户
租户运营。
## 问题
异常需要逐条确认。
## 初步价值
减少手工遗漏，尚无访谈证据。
## 判断
建议：继续调研
理由：需要验证实际处理频次。
## 竞品与参考边界
未提供竞品，不能据此增加功能。
## MVP 假设
仅处理本租户异常。
## 验证问题
确认处理频次和既有替代方案。
'''
        report = self.check({'product/idea-brief.md': text}, stage='vet')
        self.assertEqual('PASS', report['status'], report)
        self.assertEqual(1, len(list(self.root.rglob('*.md'))))

    def test_missing_artifact_needs_review_without_forcing_history_rewrite(self):
        del self.docs["product/requirements.md"]
        self.assert_review("missing-table")

    def test_header_only_story_does_not_count_as_content(self):
        self.docs["product/user-stories.md"] = "# 用户故事\n| 用户角色 | 我想要 |\n| --- | --- |\n"
        self.assert_review("empty-artifact")

    def test_fenced_and_commented_acceptance_cannot_fake_coverage(self):
        self.docs["product/acceptance-criteria.md"] = "```markdown\n" + self.docs["product/acceptance-criteria.md"] + "```\n<!-- | REQ-001 | AC-001 | -->"
        self.assert_review("missing-table")

    def test_missing_permission_dimension_needs_review(self):
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"].replace("| AC-003 | AC-004 | AC-005 |", "| | AC-004 | AC-005 |")
        self.assert_review("coverage-gap")

    def test_explained_non_applicable_dimension_passes(self):
        path = "product/acceptance-criteria.md"
        self.docs[path] = self.docs[path].replace("| AC-003 | AC-004 | AC-005 |", "| AC-003 | AC-004 | 不适用：该需求只读，不改变业务状态 |")
        self.assertTrue(self.check()["passed"])

    def test_non_applicable_without_reason_needs_review(self):
        path = "product/acceptance-criteria.md"
        self.docs[path] = self.docs[path].replace("| AC-003 | AC-004 | AC-005 |", "| 不适用 | AC-004 | AC-005 |")
        self.assert_review("coverage-gap")

    def test_normal_result_cannot_be_non_applicable(self):
        path = "product/acceptance-criteria.md"
        self.docs[path] = self.docs[path].replace("| REQ-001 | AC-001 | AC-002 |", "| REQ-001 | 不适用：没有结果 | AC-002 |")
        self.assert_review("coverage-gap")

    def test_unknown_source_blocks(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("SRC-001", "SRC-999")
        self.assert_code("unknown-reference")

    def test_unconfirmed_requirement_source_blocks(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("| 已确认 |", "| 假设 |")
        self.assert_code("unconfirmed-source")

    def test_unused_unconfirmed_evidence_is_allowed(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("| 已确认 |\n", "| 已确认 |\n| SRC-002 | 调研笔记 | 付费意愿尚需访谈 | 待确认 |\n")
        self.assertTrue(self.check()["passed"])

    def test_missing_source_locator_needs_manual_review(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("用户需求确认记录第 1 条", "")
        self.assert_review("incomplete-row")

    def test_duplicate_requirement_blocks(self):
        path = "product/requirements.md"
        self.docs[path] += self.docs[path].splitlines()[-1] + "\n"
        self.assert_code("duplicate-id")

    def test_dangling_acceptance_blocks(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("AC-005", "AC-999")
        self.assert_code("unknown-reference")

    def test_reverse_acceptance_list_need_not_be_complete(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("、AC-005", "")
        self.assertTrue(self.check()["passed"])

    def test_wrong_requirement_coverage_blocks(self):
        path = "product/acceptance-criteria.md"
        self.docs[path] = self.docs[path].replace("| AC-003 | REQ-001 |", "| AC-003 | REQ-999 |")
        self.assert_code("unknown-reference")

    def test_vague_result_needs_context_review(self):
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"].replace("异常显示已处理", "符合预期")
        self.assert_review("unobservable-result")

    def test_open_blocker_prevents_handoff(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| ID | 问题 | 影响范围 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- | --- | --- |\n| Q-001 | 是否支持撤回处理 | REQ-001 | 是 | 未解决 | 产品负责人 |\n"
        self.assert_code("open-blocker")

    def test_nonblocking_open_question_is_allowed(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| ID | 问题 | 影响范围 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- | --- | --- |\n| Q-001 | 未来渠道偏好需调研 | 后续版本 | 否 | 未解决 | 产品负责人 |\n"
        self.assertTrue(self.check()["passed"])

    def test_malformed_table_row_cannot_disappear(self):
        self.docs["product/requirements.md"] += "| REQ-002 | incomplete |\n"
        self.assert_review("incomplete-row")

    def test_escaped_pipe_in_content_is_supported(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("标记异常处理结果", r"标记异常\|处理结果")
        self.assertTrue(self.check()["passed"])

    def test_unknown_story_reference_blocks(self):
        self.docs["product/user-stories.md"] = self.docs["product/user-stories.md"].replace("REQ-001", "REQ-999")
        self.assert_code("unknown-reference")

    def test_missing_prose_section_needs_review(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("## 业务规则", "## 遗漏规则")
        self.assert_review("missing-section")

    def test_empty_field_labels_are_not_prd_content(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("减少遗漏；处理耗时基线尚无数据，不设虚构数值。", "- 目标：\n- 指标：")
        self.assert_review("missing-section")

    def test_failed_cli_check_has_structured_issues_and_exit_one(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("SRC-001", "SRC-999")
        self.check()
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--stage", "prd", "--root", str(self.root), "--format", "json"], capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        report = json.loads(result.stdout)
        self.assertFalse(report["passed"])
        self.assertTrue(all({"file", "line", "code", "message"} <= issue.keys() for issue in report["issues"]))

    def test_canonical_file_wins_over_legacy(self):
        self.check()
        (self.root / "requirements.md").write_text("invalid old version")
        self.assertTrue(product.validate(self.root, "prd")["passed"])

    def test_legacy_read_does_not_rewrite(self):
        report = self.check({Path(path).name: text for path, text in self.docs.items()})
        self.assertTrue(report["passed"])
        self.assertEqual(5, len(report["legacy_reads"]))
        self.assertFalse((self.root / "product").exists())

    def test_cli_json_and_read_only_behavior(self):
        self.check()
        before = {path: path.read_bytes() for path in self.root.rglob("*.md")}
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--stage", "prd", "--root", str(self.root), "--format", "json"], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(json.loads(result.stdout)["passed"])
        self.assertEqual(before, {path: path.read_bytes() for path in self.root.rglob("*.md")})

    def test_cli_missing_directory_returns_two(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--stage", "prd", "--root", str(self.root / "missing")], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn("不存在", result.stderr)

    def test_context_loads_only_selected_templates(self):
        full = (product.COMMON / "product-delivery-flow.md").read_text() + (product.COMMON / "artifact-contracts.md").read_text()
        for stage in product.ARTIFACTS:
            context = product.stage_context(stage)
            self.assertLess(len(context), len(full))
            self.assertIn("## 4. 安全与意外最小化", context)
            self.assertIn("token、cookie、密钥", context)
            for path in product.CONTEXT_ARTIFACTS[stage]:
                self.assertIn(f"## `{path}`", context)
        for stage in ("vet", "prd"):
            self.assertNotIn("## `ui/", product.stage_context(stage))
            self.assertNotIn("真实依赖 Gate", product.stage_context(stage))
            self.assertNotIn("Commit readiness", product.stage_context(stage))

    def test_context_includes_shared_lifecycle_rules_without_full_reference(self):
        lifecycle = (product.COMMON / "artifact-lifecycle.md").read_text()
        rules = product.section(lifecycle, "## 工作规则")
        for stage in product.ARTIFACTS:
            context = product.stage_context(stage)
            self.assertEqual(1, context.count(rules), stage)
            self.assertNotIn("## 简短续作入口", context, stage)

    def test_missing_template_fails_instead_of_silently_omitting(self):
        with self.assertRaises(ValueError):
            product.section("# templates\n", "## `product/prd.md`")

    def test_figma_connection_rules_reach_design_and_ui_review(self):
        flow = (product.COMMON / "product-delivery-flow.md").read_text()
        rules = product.section(flow, "### Figma 连接与会话复用")
        for stage in ("figma", "ui-review", "fe", "plan"):
            with self.subTest(stage=stage):
                self.assertEqual(1, product.stage_context(stage).count(rules))
        self.assertEqual(1, product.stage_context("plan", area="frontend").count(rules))
        self.assertNotIn(rules, product.stage_context("plan", area="backend"))
        for stage in ("vet", "prd", "be"):
            with self.subTest(stage=stage):
                self.assertNotIn(rules, product.stage_context(stage))

    def test_missing_figma_connection_rules_fail_before_stage_context_is_returned(self):
        with tempfile.TemporaryDirectory() as directory:
            common = Path(directory) / "common"
            shutil.copytree(product.COMMON, common)
            flow_path = common / "product-delivery-flow.md"
            flow = flow_path.read_text()
            rules = product.section(flow, "### Figma 连接与会话复用")
            flow_path.write_text(flow.replace(rules, "", 1))
            with patch.object(product, "COMMON", common):
                for stage in ("figma", "ui-review", "fe", "plan"):
                    with self.subTest(stage=stage), self.assertRaises(ValueError):
                        product.stage_context(stage)
                with self.assertRaises(ValueError):
                    product.stage_context("plan", area="frontend")
                # Backend-only work must remain usable without Figma rules.
                product.stage_context("plan", area="backend")
                product.stage_context("be")

    def test_ui_review_context_excludes_unrelated_stages(self):
        context = product.stage_context("ui-review")
        self.assertIn("## `ui/ui-review-report.md`", context)
        self.assertIn("## 4. 安全与意外最小化", context)
        self.assertIn("产品事实源优先级", context)
        for unrelated in ("## `product/prd.md`", "## `ui/ui-pages.md`", "真实依赖 Gate", "SQL 执行", "Commit readiness"):
            self.assertNotIn(unrelated, context)

    def test_vet_allows_hypothesis_but_requires_explicit_decision(self):
        docs = {path: "# 材料\n尚无访谈证据，需先向运营确认当前做法。\n" for path in product.ARTIFACTS["vet"]}
        docs["product/idea-brief.md"] = "# 想法\n## 原始想法\n- 一句话：广告异常提醒。\n## 用户\n- 用户：跨境电商运营。\n## 问题\n- 痛点：不能及时发现异常。\n## 初步价值\n- 假设：及时提醒能减少遗漏，尚需访谈。\n## 判断\n- 建议：继续调研\n- 理由：尚缺付费意愿证据。\n"
        self.assertTrue(self.check(docs, "vet")["passed"])
        docs["product/idea-brief.md"] = docs["product/idea-brief.md"].replace("建议：继续调研", "建议：进入 PRD / 继续调研 / 暂停")
        report = self.check(docs, "vet")
        self.assertEqual("REVIEW", report["status"])
        self.assertIn("missing-decision", {issue["code"] for issue in report["warnings"]})

    def test_vet_requires_decision_reason(self):
        docs = {path: "# 材料\n需调研运营当前做法。\n" for path in product.ARTIFACTS["vet"]}
        docs["product/idea-brief.md"] = "# 想法\n## 原始想法\n提醒。\n## 用户\n运营。\n## 问题\n遗漏异常。\n## 初步价值\n减少遗漏。\n## 判断\n- 建议：继续调研\n- 理由：\n## 证据与假设\n尚缺访谈证据。\n"
        report = self.check(docs, "vet")
        self.assertEqual("REVIEW", report["status"])
        self.assertIn("missing-decision-reason", {issue["code"] for issue in report["warnings"]})

    def test_existing_R1_S1_A1_ids_are_preserved(self):
        self.docs = {key: value.replace("REQ-001", "R1").replace("SRC-001", "S1") for key, value in self.docs.items()}
        for number in range(1, 6):
            self.docs = {key: value.replace(f"AC-00{number}", f"A{number}") for key, value in self.docs.items()}
        self.assertTrue(self.check()["passed"])

    def test_unknown_legacy_id_is_still_rejected(self):
        self.docs = {key: value.replace("REQ-001", "R1") for key, value in self.docs.items()}
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"].replace("| AC-001 | R1 |", "| AC-001 | R999 |")
        self.assert_code("unknown-reference")

    def test_chinese_adjacent_source_reference(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("| SRC-001 |", "| 依据SRC-001 |")
        self.assertTrue(self.check()["passed"])

    def test_chinese_adjacent_requirement_reference(self):
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"].replace("| AC-001 | REQ-001 |", "| AC-001 | 对应需求REQ-001 |")
        self.assertTrue(self.check()["passed"])

    def test_chinese_adjacent_unknown_reference_still_blocks(self):
        self.docs["product/requirements.md"] = self.docs["product/requirements.md"].replace("| SRC-001 |", "| 依据SRC-999 |")
        self.assert_code("unknown-reference")

    def test_nonblocking_unknown_owner_is_only_a_reminder(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| ID | 问题 | 影响范围 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- | --- | --- |\n| Q-001 | 下季度渠道偏好需调研 | 后续版本 | 否 | 未解决 | 待确认 |\n"
        report = self.check()
        self.assertTrue(report["passed"])
        self.assertEqual([], report["issues"])
        self.assertIn("question-owner", {warning["code"] for warning in report["warnings"]})

    def test_blocker_is_checked_even_without_an_owner_or_id(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| 问题 | 是否阻断 | 状态 |\n| --- | --- | --- |\n| 本期权限未确认 | 是 | 未解决 |\n"
        self.assert_code("open-blocker")

    def test_example_or_comment_none_cannot_hide_unconfirmed_permission(self):
        for example in ("```text\n无\n```", "<!--\n无\n-->", "    无"):
            with self.subTest(example=example):
                self.docs["product/open-questions.md"] = "# 开放问题\n本期权限尚未确认，不能交接。\n\n" + example
                self.assert_review("missing-question-status")

    def test_visible_none_does_not_override_an_unrecognized_question_table(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| 问题 | 处理建议 |\n| --- | --- |\n| 本期权限尚未确认 | 停止交接 |\n\n无。\n"
        self.assert_review("missing-question-status")

    def test_equivalent_user_heading_is_accepted(self):
        self.docs["product/prd.md"] = self.docs["product/prd.md"].replace("## 用户角色", "## 目标用户与角色")
        self.assertTrue(self.check()["passed"])

    def test_custom_format_needs_review_not_a_false_pass_or_business_block(self):
        report = self.check({"product/prd.md": "# 简短需求\n用户：运营；本期只调整按钮文案。\n"})
        self.assertEqual("REVIEW", report["status"])
        self.assertFalse(report["passed"])
        self.assertEqual([], report["issues"])

    def test_acceptance_mapping_is_authoritative_without_reverse_lists(self):
        self.docs["product/requirements.md"] = "# 需求清单\n| ID | 需求 | 来源 |\n| --- | --- | --- |\n| REQ-001 | 标记异常处理结果 | SRC-001 |\n"
        self.docs["product/user-stories.md"] = "# 用户故事\n运营希望标记处理结果以避免重复处理。关联需求：REQ-001。\n"
        start = self.docs["product/acceptance-criteria.md"].index("## 业务状态与边界覆盖")
        end = self.docs["product/acceptance-criteria.md"].index("## 状态验收")
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"][:start] + self.docs["product/acceptance-criteria.md"][end:]
        self.assertTrue(self.check()["passed"])

    def test_known_requirement_without_any_acceptance_still_blocks(self):
        self.docs["product/requirements.md"] += "| REQ-002 | 新增另一个功能 | P1 | SRC-001 | 关联验收待补 |\n"
        self.assert_code("uncovered-requirement")

    def test_one_acceptance_can_cover_multiple_requirements(self):
        self.docs["product/requirements.md"] += "| REQ-002 | 同一处理动作的结果反馈 | P1 | SRC-001 | 见权威验收表 |\n"
        self.docs["product/acceptance-criteria.md"] = self.docs["product/acceptance-criteria.md"].replace("| AC-001 | REQ-001 |", "| AC-001 | REQ-001、REQ-002 |")
        self.assertTrue(self.check()["passed"])

    def test_optional_coverage_can_repeat_requirement_for_different_risks(self):
        self.docs["product/acceptance-criteria.md"] += "\n| 需求 ID | 权限与可见性 |\n| --- | --- |\n| REQ-001 | AC-003 |\n| REQ-001 | 直接访问同样拒绝跨租户查看 |\n"
        self.assertTrue(self.check()["passed"])

    def test_optional_partial_coverage_still_checks_explicit_wrong_mapping(self):
        self.docs["product/requirements.md"] += "| REQ-002 | 另一项功能 | P1 | SRC-001 | AC-006 |\n"
        self.docs["product/acceptance-criteria.md"] += "\n| ID | 关联需求 | 前置条件 | 操作 / 事件 | 预期结果 |\n| --- | --- | --- | --- | --- |\n| AC-006 | REQ-002 | 有权查看 | 查看 | 显示另一项功能结果 |\n\n| 需求 ID | 权限与可见性 |\n| --- | --- |\n| REQ-001 | AC-006 |\n"
        self.assert_code("wrong-coverage")

    def test_contradictory_reverse_view_still_blocks(self):
        self.docs["product/requirements.md"] += "| REQ-002 | 另一项功能 | P1 | SRC-001 | AC-001 |\n"
        self.docs["product/acceptance-criteria.md"] += "\n| ID | 关联需求 | 前置条件 | 操作 / 事件 | 预期结果 |\n| --- | --- | --- | --- | --- |\n| AC-006 | REQ-002 | 有权查看 | 查看 | 显示另一项功能结果 |\n"
        self.assert_code("mismatched-acceptance")

    def test_unclosed_html_comment_in_example_does_not_eat_real_content(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n```html\n<!-- example\n```\n无。\n"
        self.assertTrue(self.check()["passed"])

    def test_review_exit_zero_is_explicitly_not_machine_pass(self):
        self.docs["product/requirements.md"] = "# 需求\n用原有格式记录需求，关联需人工核对。\n"
        self.check()
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--stage", "prd", "--root", str(self.root), "--format", "json"], capture_output=True, text=True)
        self.assertEqual(0, result.returncode)
        report = json.loads(result.stdout)
        self.assertEqual("REVIEW", report["status"])
        self.assertFalse(report["passed"])

    def test_mixed_question_formats_need_review_without_guessing_business_impact(self):
        standard = "# 开放问题\n| ID | 问题 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- | --- |\n| Q-001 | 下季度渠道偏好 | 否 | 未解决 | 产品负责人 |\n"
        for extra in ("\n## 本期权限待定\n| 待确认事项 | 交接限制 |\n| --- | --- |\n| 跨租户可见性 | 本期不能交接 |\n", "\n- 本期权限尚未确认，需产品复核。\n", "\n补充说明：这是已解决事项的背景记录。\n", "\n## 本期权限尚未确认\n"):
            with self.subTest(extra=extra):
                self.docs["product/open-questions.md"] = standard + extra
                self.assert_review("unparsed-questions")

    def test_multiple_recognized_question_tables_are_allowed(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n## 本期\n| 问题 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- |\n| 交互文案确认 | 否 | 已解决 | 设计负责人 |\n\n## 后续\n| 问题 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- |\n| 下季度渠道偏好 | 否 | 未解决 | 产品负责人 |\n"
        self.assertTrue(self.check()["passed"])

    def test_question_explanations_can_remain_in_the_recognized_row(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| 问题 | 是否阻断 | 状态 | 需要谁确认 | 处理说明 |\n| --- | --- | --- | --- | --- |\n| 下季度渠道偏好 | 否 | 未解决 | 待确认 | 仅后续版本，不影响本期 |\n"
        self.assertTrue(self.check()["passed"])

    def test_mixed_unparsed_content_does_not_hide_a_known_blocker(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| 问题 | 是否阻断 | 状态 |\n| --- | --- | --- |\n| 本期权限 | 是 | 未解决 |\n\n补充说明待审阅。\n"
        self.assert_code("open-blocker")

    def test_examples_and_comments_do_not_create_extra_question_items(self):
        self.docs["product/open-questions.md"] = "# 开放问题\n| 问题 | 是否阻断 | 状态 | 需要谁确认 |\n| --- | --- | --- | --- |\n| 渠道偏好 | 否 | 未解决 | 产品负责人 |\n\n```markdown\n| 待确认事项 | 交接限制 |\n| --- | --- |\n| 示例 | 示例 |\n```\n<!-- 仅示例，不是当前问题 -->\n"
        self.assertTrue(self.check()["passed"])

    def vet_docs(self):
        docs = {path: "# 材料\n需调研运营当前做法。\n" for path in product.ARTIFACTS["vet"]}
        docs["product/idea-brief.md"] = "# 想法\n## 原始想法\n广告异常提醒。\n## 用户\n跨境电商运营。\n## 问题\n发现异常不及时。\n## 初步价值\n及时提醒，尚待验证。\n## 判断\n- 建议：进入 PRD\n- 理由：用户与场景足够明确，可以定义需求。\n"
        return docs

    def test_conflicting_vet_decisions_need_review(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] += "\n## 复核判断\n- 建议：暂停\n- 理由：关键需求约束尚未得到确认。\n"
        result = self.check(docs, "vet")
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual([], result["issues"])
        self.assertIn("ambiguous-decision", {w["code"] for w in result["warnings"]})

    def test_same_vet_advice_in_two_unscoped_sections_also_needs_review(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] += "\n## 另一份判断\n- 建议：进入 PRD\n- 理由：另一份尚未核对的依据。\n"
        self.assertEqual("REVIEW", self.check(docs, "vet")["status"])

    def test_vet_reason_cannot_be_taken_from_another_section(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] = docs["product/idea-brief.md"].replace("- 理由：用户与场景足够明确，可以定义需求。", "") + "\n## 其他记录\n- 理由：这不是当前决定的依据。\n"
        self.assertEqual("REVIEW", self.check(docs, "vet")["status"])

    def test_quoted_vet_history_does_not_override_current_decision(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] += "\n## 历史记录（引用）\n> - 建议：暂停\n> - 理由：当时缺少使用场景。\n"
        self.assertTrue(self.check(docs, "vet")["passed"])

    def test_vet_current_decision_supports_formatting_and_notes(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] = docs["product/idea-brief.md"].replace("- 建议：进入 PRD", "- **建议：进入 PRD**").replace("## 判断", "## 判断\n本轮仅决定是否继续定义需求。")
        self.assertTrue(self.check(docs, "vet")["passed"])

    def test_vet_examples_do_not_override_current_decision(self):
        docs = self.vet_docs()
        docs["product/idea-brief.md"] += "\n```markdown\n- 建议：暂停\n- 理由：示例。\n```\n<!-- 建议：暂停 -->\n"
        self.assertTrue(self.check(docs, "vet")["passed"])

    def test_benchmark_requires_pass_and_rejects_review(self):
        cases = json.loads((ROOT / "evals/cases/benchmark-cases.json").read_text(encoding="utf-8"))
        case = next(case for case in cases if case["id"] == "pd-prd-from-vet-artifacts")
        verification = self.root / "verification"
        verification.mkdir()
        (verification / "product_artifacts.py").write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
        self.check()
        command = case["check_commands"][0]
        result = subprocess.run(command, shell=True, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("PASS", json.loads(result.stdout)["status"])
        self.docs["product/requirements.md"] = "# 原格式需求\n需人工核对关联。\n"
        self.check()
        result = subprocess.run(command, shell=True, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("REVIEW", json.loads(result.stdout)["status"])


if __name__ == "__main__":
    unittest.main()
