"""Reproduce false-positive grading and preserve useful UI review exceptions."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


checker = module("ui_review_benchmark", ROOT / "evals/checks/ui_review.py")
runner = module("skill_benchmark_runner", ROOT / "scripts/run_skill_benchmark.py")


class UiReviewBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwerdf-ui-review-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report = self.root / "ui/ui-review-report.md"
        self.report.parent.mkdir()
        shutil.copytree(ROOT / "evals/fixtures/ui-review/images", self.root / "visual-fixtures")

    def write(self, scenario="compact-report", *, visual="已检查", template="已检查", finding=""):
        self.text = f"""# UI Review
## 审查范围
仅审查本轮截图的 default，可见布局；不验证接口、键盘或隐藏状态。
## 截图 / 视觉证据
visual-fixtures/{scenario}.png，视口及版本见 baseline.json。
## 结论
- 状态：{checker.SCENARIOS[scenario]}
- 残余风险：键盘、隐藏状态不在本轮；P2 由 pd-fe 负责，在页面局部复查。
## Findings
| 级别 | 问题 | 用户影响 | 验证方式 | 证据 | 归属 |
| --- | --- | --- | --- | --- | --- |
{finding}
## 三层审查结果
| 检查层 | 结果：已检查 / 不适用 / 未验证 | 依据或理由 |
| --- | --- | --- |
| 机器扫描 | 不适用 | 本轮只有截图，DOM/console/network 不可用 |
| 视觉扫描 | {visual} | 查看原图、底部操作与关键数据；仅判断可见布局 |
| 模板扫描 | {template} | 检查本图同类行的字段与布局策略 |
"""
        self.report.write_text(self.text)

    def check(self, scenario="compact-report"):
        return checker.check(self.root, scenario)

    def assertReview(self, result):
        self.assertFalse(result["automated_checks_passed"])
        self.assertEqual("REVIEW", result["status"])
        self.assertTrue(result["mechanical_checks_passed"])
        self.assertEqual([], result["errors"])
        self.assertTrue(result["review_required"])

    def test_unable_to_read_is_not_guessed_to_mean_no_harm(self):
        self.write(finding="| — | 本轮未发现可见缺陷 | 无法读取完整金额 | 修复后核对全文 | compact-report.png | pd-fe |")
        self.assertReview(self.check())

    def test_equivalent_no_finding_wording_is_review_not_failure(self):
        self.write(finding="| — | 本轮未发现阻断问题 | 核心任务不受影响 | 变更后复查 | compact-report.png | 无需修复 |")
        self.assertReview(self.check())

    def test_free_form_finding_content_is_never_silently_empty(self):
        for content in ("- P1：关键金额裁切，无法核对。", "发现问题：P1，关键金额裁切。", "### 金额核对\n右端文字不可读。", "| 严重性 | 说明 |\n| P1 | 金额裁切 |", "- Nothing actionable found.", "```markdown\n- P1：金额被裁切\n```", "<!-- P1: 金额被裁切 -->"):
            with self.subTest(content=content):
                self.write()
                self.report.write_text(self.text.replace("## 三层审查结果", content + "\n\n## 三层审查结果"))
                self.assertReview(self.check())

    def test_unknown_blocking_report_format_is_review_not_false_defect(self):
        self.write("mobile-form", finding="| P1 | 提交按钮遮挡 | 核心操作难辨 | 复查底部 | mobile-form.png | pd-fe |")
        self.report.write_text(self.text.replace("## Findings", "## 问题清单"))
        self.assertReview(self.check("mobile-form"))

    def test_duplicate_findings_cannot_hide_in_the_second_section(self):
        self.write()
        self.report.write_text(self.text + "\n## Findings\n- P1：金额不可读。\n")
        self.assertReview(self.check())

    def test_ambiguous_sections_are_not_decided_by_first_or_last_value(self):
        self.write()
        self.report.write_text(self.text.replace("状态：本轮范围可继续", "状态：有阻断") + "\n## 结论\n- 状态：本轮范围可继续\n")
        self.assertReview(self.check())
        self.write("mobile-form")
        self.report.write_text(self.text + "\n## Findings\n- P1：提交操作受损\n")
        self.assertReview(self.check("mobile-form"))
        self.write()
        self.report.write_text(self.text + "\n| 检查层 | 结果：已检查 / 不适用 / 未验证 | 依据或理由 |\n| --- | --- | --- |\n| 机器扫描 | 已检查 | 历史记录，范围未知 |\n")
        self.assertReview(self.check())

    def test_multiple_layer_choices_need_review_without_false_completion(self):
        self.write()
        self.report.write_text(self.text.replace("视觉扫描 | 已检查", "视觉扫描 | 已检查 / 未验证"))
        self.assertReview(self.check())

    def test_multiple_candidate_conclusions_need_a_decision(self):
        self.write()
        self.report.write_text(self.text.replace("状态：本轮范围可继续", "状态：本轮范围可继续 / 有阻断 / 证据不足"))
        self.assertReview(self.check())

    def test_scoped_conclusion_and_layer_notes_remain_usable(self):
        self.write()
        self.report.write_text(self.text.replace("状态：本轮范围可继续", "状态：**本轮范围可继续**，仅本张截图").replace("视觉扫描 | 已检查", "视觉扫描 | 已检查（仅本张截图）"))
        self.assertTrue(self.check()["automated_checks_passed"])

    def test_unavailable_runtime_and_template_cannot_claim_done(self):
        self.write("missing-visual", visual="未验证", template="未验证")
        self.report.write_text(self.text.replace("机器扫描 | 不适用", "机器扫描 | 已检查").replace("本轮只有截图，DOM/console/network 不可用", "DOM、console、network 检查均通过"))
        self.assertEqual("FAIL", self.check("missing-visual")["status"])
        self.write("missing-visual", visual="未验证", template="已检查")
        self.assertEqual("FAIL", self.check("missing-visual")["status"])

    def test_picture_only_runtime_scan_also_cannot_be_claimed(self):
        self.write()
        self.report.write_text(self.text.replace("机器扫描 | 不适用", "机器扫描 | 已检查"))
        self.assertEqual("FAIL", self.check()["status"])

    def test_cli_distinguishes_review_from_failure(self):
        self.write(finding="| — | 本轮未发现阻断问题 | 核心任务不受影响 | 变更后复查 | compact-report.png | 无需修复 |")
        result = subprocess.run([sys.executable, str(ROOT / "evals/checks/ui_review.py"), "--root", str(self.root), "--scenario", "compact-report"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertReview(json.loads(result.stdout))

    def test_screenshot_only_allows_runtime_not_applicable(self):
        self.write()
        self.assertTrue(self.check()["automated_checks_passed"])

    def test_uninspected_visual_cannot_claim_completion(self):
        self.write(visual="未验证")
        self.assertEqual("FAIL", self.check()["status"])

    def test_no_similar_component_allows_template_not_applicable(self):
        self.write("amount-readable", template="不适用：单一金额摘要，无同类组件")
        self.assertTrue(self.check("amount-readable")["automated_checks_passed"])

    def test_unrelated_clipping_is_not_automatically_approved_as_core_evidence(self):
        self.write("mobile-form", finding="| P1 | 页面顶部辅助说明被裁切 | 次要说明不完整 | 复查顶部说明 | mobile-form.png 顶部说明 | pd-fe |")
        self.assertReview(self.check("mobile-form"))

    def test_unrecognized_finding_table_requires_review(self):
        self.write(finding="| P1 | 侧距不足默认 16px | 只有 8px | 改成 16px | compact-report.png | pd-fe |")
        self.report.write_text(self.text.replace("| 级别 | 问题 |", "| 严重性 | 问题 |"))
        result = self.check()
        self.assertFalse(result["automated_checks_passed"])
        self.assertTrue(result["review_required"])

    def test_no_finding_phrase_cannot_swallow_an_actual_defect(self):
        self.write(finding="| — | 未发现恢复入口，关键金额被裁切 | 关键金额无法完整读取 | 修复后复查金额 | compact-report.png 右侧 | pd-fe |")
        self.assertReview(self.check())

    def test_required_template_cannot_be_unverified_or_not_applicable(self):
        for status in ("未验证", "不适用：无同类组件"):
            with self.subTest(status=status):
                self.write(template=status)
                self.assertEqual("FAIL", self.check()["status"])

    def test_unknown_second_table_cannot_hide_behind_valid_findings(self):
        self.write(finding="| P2 | 辅助说明可更清晰 | 不影响阅读 | 复查说明 | compact-report.png | pd-fe |")
        extra = "\n| 严重性 | 问题 | 用户影响 |\n| --- | --- | --- |\n| P1 | 错误阻断描述 | 主流程受损 |\n"
        self.report.write_text(self.text.replace("## 三层审查结果", extra + "\n## 三层审查结果"))
        self.assertTrue(self.check()["review_required"])
        self.assertFalse(self.check()["automated_checks_passed"])

    def test_missing_findings_section_is_review_not_empty_pass(self):
        self.write()
        self.report.write_text(self.text.replace("## Findings", "## 问题清单"))
        result = self.check()
        self.assertTrue(result["review_required"])
        self.assertFalse(result["automated_checks_passed"])

    def test_amount_observation_meaning_is_left_to_manual_review(self):
        self.write("amount-clipped", finding="| P1 | 应付金额尾部裁切 | 无法读取完整数值，不能核对付款 | 重取截图检查金额全文 | amount-clipped.png 金额区 | pd-fe |")
        self.assertReview(self.check("amount-clipped"))
        self.write("amount-clipped", finding="| P1 | 辅助说明被裁切 | 次要文本不全 | 复查说明 | amount-clipped.png 页脚 | pd-fe |")
        self.assertReview(self.check("amount-clipped"))

    def test_amount_readable_control_keeps_normal_design(self):
        self.write("amount-readable", template="不适用：仅一个金额摘要")
        self.assertTrue(self.check("amount-readable")["automated_checks_passed"])
        self.write("amount-readable", finding="| P1 | 金额容器宽度不是固定值 | 认为必须固定宽度 | 改固定宽度 | amount-readable.png | pd-fe |")
        self.assertFalse(self.check("amount-readable")["automated_checks_passed"])

    def test_required_error_feedback_cannot_be_skipped(self):
        self.write("save-error", finding="| P1 | 邮箱校验失败后缺少错误提示和修正指引 | 用户无法知道保存未成功或如何恢复 | 失败后复查可见反馈及输入保留 | save-error.png 表单 | pd-fe |")
        self.assertReview(self.check("save-error"))
        self.write("save-error")
        self.assertFalse(self.check("save-error")["automated_checks_passed"])

    def test_error_feedback_control_allows_recoverable_failure(self):
        self.write("save-error-feedback")
        self.assertTrue(self.check("save-error-feedback")["automated_checks_passed"])

    def test_error_judgment_needs_recorded_failure_not_default_image(self):
        self.write("save-error", finding="| P1 | 保存失败但没有错误反馈 | 无法定位邮箱错误 | 失败后复查 | save-error.png | pd-fe |")
        baseline = self.root / "visual-fixtures/baseline.json"
        data = json.loads(baseline.read_text())
        next(r for r in data["images"] if r["file"] == "save-error.png")["state"] = "default"
        baseline.write_text(json.dumps(data))
        self.assertEqual("FAIL", self.check("save-error")["status"])

    def test_english_observation_and_numbering_do_not_require_one_phrase(self):
        self.write("mobile-form", finding="| P1: F-02 | Submit label is cut off by navigation | Primary action is hard to identify | Retake the bottom screenshot | mobile-form.png | pd-fe |")
        self.assertReview(self.check("mobile-form"))

    def test_core_task_cannot_be_relegated_to_p2_to_pass_a_blocking_case(self):
        for scenario, issue in (("mobile-form", "底栏遮挡提交按钮"), ("amount-clipped", "应付金额被裁切"), ("save-error", "保存失败后缺少错误提示")):
            with self.subTest(scenario=scenario):
                self.write(scenario, finding=f"| P2 | {issue} | 核心任务受损 | 修复后复查 | {scenario}.png | pd-fe |")
                self.assertEqual("FAIL", self.check(scenario)["status"])

    def test_unrelated_defect_cannot_replace_required_error_feedback(self):
        self.write("save-error", finding="| P1 | 页脚被裁切 | 次要说明不全 | 复查页脚 | save-error.png | pd-fe |")
        self.assertReview(self.check("save-error"))

    def test_new_scenarios_are_executable_through_benchmark_commands(self):
        cases = json.loads((ROOT / "evals/cases/benchmark-cases.json").read_text())
        for scenario, issue in (("amount-clipped", "应付金额尾部裁切"), ("amount-readable", ""), ("save-error", "保存失败后缺少错误反馈"), ("save-error-feedback", "")):
            with self.subTest(scenario=scenario):
                case = next(c for c in cases if c["id"] == f"pd-ui-review-{scenario}")
                runner.materialize_fixture_dirs(case, self.root)
                finding = f"| P1 | {issue} | 核心任务受损 | 修复后复查本状态 | {scenario}.png | pd-fe |" if issue else ""
                self.write(scenario, finding=finding)
                checks = runner.run_check_commands(case, self.root, self.root / f"checks-{scenario}", 10)
                passed, _ = runner.grade_output(case, self.root, 0, False, checks)
                self.assertEqual(not bool(issue), passed, checks)
                result = json.loads(Path(checks[0]["evidence"]["stdout"]).read_text())
                if issue:
                    self.assertEqual(2, checks[0]["evidence"]["exit_code"])
                    self.assertReview(result)
                else:
                    self.assertEqual("PASS", result["status"])

    def test_explicit_no_finding_table_row_needs_no_wording_rewrite(self):
        self.write(finding="| — | 未发现有依据的可见缺陷 | 无已证实影响 | 如有变更复查 | E1 | 无需修复 |")
        self.assertReview(self.check())

    def test_observed_normal_result_can_describe_readability_as_impact(self):
        self.write("amount-readable", finding="| — | 当前样本未见金额裁切、重叠或主操作遮挡 | 可从截图完整读取应付金额并识别确认入口 | 原图及局部放大检查 | amount-readable.png | 无需修复 |")
        self.assertReview(self.check("amount-readable"))

    def test_observed_normal_feedback_can_describe_absence_of_harm(self):
        self.write("save-error-feedback", finding="| — | 本轮未发现需要登记的 P0/P1/P2/P3 问题 | 未见可见反馈妨碍理解或遮挡主操作 | 同状态原图复查 | save-error-feedback.png | 不适用 |")
        self.assertReview(self.check("save-error-feedback"))
        self.report.write_text(self.text.replace("未见可见反馈妨碍理解或遮挡主操作", "未见问题，但无法保存"))
        self.assertFalse(self.check("save-error-feedback")["automated_checks_passed"])

    def test_p2_is_not_a_structural_failure_or_automatic_semantic_pass(self):
        self.write(finding="| P2 | 辅助说明可更清晰 | 不影响读取联系方式 | 复查说明区域 | compact-report.png 第二行 | pd-fe |")
        self.assertReview(self.check())

    def test_screenshot_finding_can_leave_ownership_pending(self):
        self.write("mobile-form", finding="| P1 | 底栏覆盖提交按钮 | 主操作难辨 | 同条件截图复查 | mobile-form.png 底部 | 待确认 |")
        self.assertReview(self.check("mobile-form"))

    def test_compact_approved_design_must_not_be_blocked(self):
        self.write(finding="| P1 | 侧距不足默认 16px | 只有 8px | 强制改为 16px | compact-report.png 页面边缘 | pd-fe |")
        self.assertEqual("FAIL", self.check()["status"])

    def test_real_core_action_occlusion_is_recorded(self):
        self.write("mobile-form", finding="| P1 | 底部导航遮挡提交按钮文字 | 关键操作难辨认 | 修复后截图复查底部 | mobile-form.png 底部操作区 | pd-fe |")
        self.assertReview(self.check("mobile-form"))

    def test_scoped_bold_conclusion_and_numbered_finding_are_accepted(self):
        self.write("mobile-form", finding="| P1 · F-01 | 底部导航遮挡提交文字 | 主操作难辨 | 修复后截图复查 | E1 底部 | pd-fe |")
        index = "| 证据 | 类型 |\n| --- | --- |\n| E1：原始图 mobile-form.png | 浏览器截图 |\n"
        self.report.write_text(self.text.replace("## 结论", index + "\n## 结论").replace("状态：有阻断", "状态：**有阻断**，仅本轮截图"))
        self.assertReview(self.check("mobile-form"))

    def test_dangling_evidence_alias_is_not_accepted(self):
        self.write("mobile-form", finding="| P1 · F-01 | 底部导航遮挡提交文字 | 主操作难辨 | 截图复查 | E999 底部 | pd-fe |")
        self.assertEqual("FAIL", self.check("mobile-form")["status"])

    def test_blocking_case_cannot_be_replaced_by_generic_headings(self):
        self.write("mobile-form")
        self.assertFalse(self.check("mobile-form")["automated_checks_passed"])

    def test_missing_image_is_not_visual_evidence(self):
        self.write()
        (self.root / "visual-fixtures/compact-report.png").unlink()
        self.assertEqual("FAIL", self.check()["status"])

    def test_modified_image_requires_updated_baseline(self):
        self.write()
        with (self.root / "visual-fixtures/compact-report.png").open("ab") as stream:
            stream.write(b"changed")
        self.assertEqual("FAIL", self.check()["status"])

    def test_missing_visual_case_reports_evidence_gap_without_fake_findings(self):
        self.write("missing-visual", visual="未验证", template="未验证")
        self.assertTrue(self.check("missing-visual")["automated_checks_passed"])

    def test_missing_visual_case_cannot_claim_seen(self):
        self.write("missing-visual")
        self.assertEqual("FAIL", self.check("missing-visual")["status"])

    def test_example_conclusion_cannot_override_actual_conclusion(self):
        self.write()
        self.report.write_text(self.text.replace("## 结论", "```markdown\n## 结论").replace("## Findings", "```\n## Findings"))
        self.assertFalse(self.check()["automated_checks_passed"])

    def test_checker_does_not_modify_input_files(self):
        self.write()
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.check()
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_original_keywords_only_false_pass_is_rejected_end_to_end(self):
        cases = json.loads((ROOT / "evals/cases/benchmark-cases.json").read_text())
        case = next(c for c in cases if c["id"] == "pd-ui-review-screenshot-visual-defects")
        runner.materialize_fixture_dirs(case, self.root)
        self.report.write_text("# UI Review\n结论：整体通过，可进入下一阶段。\n机器扫描：未运行。视觉扫描：未看截图。模板扫描：未执行。\nFindings P 遮挡 横向溢出 截图证据 同类问题扫描 三层审查结果 机器扫描 视觉扫描 模板扫描 量化阈值检查 16px 12-16px label/value $pd-fe $pd-figma ui/ui-design-system.md\n")
        command_checks = runner.run_check_commands(case, self.root, self.root / "check-results", 10)
        passed, _ = runner.grade_output(case, self.root, 0, False, command_checks)
        self.assertFalse(passed)
        self.assertFalse(command_checks[0]["passed"])

    def test_positive_case_check_command_is_executable(self):
        self.write()
        result = subprocess.run([sys.executable, str(ROOT / "evals/checks/ui_review.py"), "--root", str(self.root), "--scenario", "compact-report"], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("不证明模型看过图片", json.loads(result.stdout)["limitation"])


if __name__ == "__main__":
    unittest.main()
