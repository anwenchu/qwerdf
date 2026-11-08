"""Source ownership, coverage and publication checks for the generated TODO view."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/qwerdf-common/scripts/task_todo.py"
SPEC = importlib.util.spec_from_file_location("task_todo", SCRIPT)
todo = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(SCRIPT.parent))
try:
    SPEC.loader.exec_module(todo)
finally:
    sys.path.pop(0)


def table(*items):
    header = "| 顺序 | ID | 业务动作与交付结果 | 状态 | 完成标准 | 证据 / 阻断 |\n| --- | --- | --- | --- | --- | --- |\n"
    return header + "".join(f"| {n} | {key} | {action} | {status} | {criteria} | {evidence} |\n"
                            for n, (key, action, status, criteria, evidence) in enumerate(items, 1))


def source(status="pending", *, acceptance=None):
    text = "# 任务\n任务来源：本文件\n"
    if acceptance is None:
        text += "验收追踪：随实现任务\n"
    text += "\n## 后端任务\n" + table(("BE-01", "提交处理结果", status, "归属校验及重试不重复写入", "测试记录 #case-1"))
    if acceptance:
        text += "\n## 验收任务\n" + table(("AC-01", "验证实际业务闭环", acceptance, "真实接口联调通过", "真实环境尚未具备，继续独立编码"))
    return text


class TaskTodoTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="qwerdf-todo-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def view(self):
        return (self.root / "TODO.md").read_text(encoding="utf-8")

    def test_completion_reopen_and_same_ids_in_independent_tasks(self):
        first = self.write("tasks/first/tech/task-slices.md", source("done"))
        other = self.write("tasks/rework/tech/task-slices.md", source("in_progress"))
        originals = {p: p.read_bytes() for p in (first, other)}
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertNotIn("first / BE-01", self.view())
        self.assertIn("rework / BE-01", self.view())
        for path, original in originals.items():
            self.assertEqual(original, path.read_bytes())
        first.write_text(source("pending"))
        self.assertEqual(1, todo.refresh(self.root, check=True)[0])
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn("first / BE-01", self.view())
        self.assertEqual(0, todo.refresh(self.root, check=True)[0])

    def test_code_done_does_not_hide_acceptance_or_blocked_parent(self):
        self.write("tasks/unit/tech/task-slices.md", source("done", acceptance="pending"))
        self.write("tech/task-slices.md", source("blocked"))
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn("## 待验证 / 验收", self.view())
        self.assertIn("unit / AC-01", self.view())
        self.assertNotIn("unit / BE-01", self.view())
        self.assertIn("项目共用任务 / BE-01", self.view())
        self.assertIn("## 受阻", self.view())

    def test_blocked_acceptance_retains_reason(self):
        self.write("tech/task-slices.md", source("done", acceptance="blocked"))
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn("## 受阻", self.view())
        self.assertIn("真实环境尚未具备", self.view())
        self.assertNotIn("已登记来源中无未完成项", self.view())

    def test_confirmed_unplanned_items_and_existing_index_layout(self):
        self.write("overview.md", """# 项目
## 任务索引
| 任务 | 目录 | 范围 / 交付结果 |
| --- | --- | --- |
| 自定义任务 | [目录](work/item) | |
## 已确认待拆解
| ID | 事项 | 来源 |
| --- | --- | --- |
| REQ-02 | 用户已确认的补充动作 | product/prd.md#确认 |
""")
        self.write("work/item/tech/task-slices.md", source("done"))
        self.assertEqual(0, todo.refresh(self.root, "overview.md")[0])
        self.assertIn("REQ-02", self.view())
        self.assertIn("## 已确认待拆解", self.view())
        # Moving the navigation row to a task does not modify the original fact source.
        overview = self.root / "overview.md"
        overview.write_text(overview.read_text().replace("| REQ-02 | 用户已确认的补充动作 | product/prd.md#确认 |\n", ""))
        self.write("work/item/tech/task-slices.md", source("pending"))
        todo.refresh(self.root, "overview.md")
        self.assertNotIn("## 已确认待拆解", self.view())
        self.assertIn("自定义任务 / BE-01", self.view())

    def test_no_sources_and_missing_indexed_source_are_not_empty_success(self):
        self.write("README.md", "## 任务索引\n| 任务 | 目录 |\n| --- | --- |\n| 未拆解 | tasks/missing |\n")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("来源缺口", self.view())
        self.assertIn("tasks/missing/tech/task-slices.md", self.view())
        (self.root / "README.md").unlink()
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertNotIn("已登记来源中无未完成项", self.view())

    def test_missing_selected_index_or_unparsed_intake_is_not_silently_skipped(self):
        self.write("tech/task-slices.md", source("done"))
        self.assertEqual(1, todo.refresh(self.root, "overview.md")[0])
        self.assertIn("overview.md", self.view())
        self.write("README.md", "## 已确认待拆解\n- 已确认动作，见原需求 REQ-02\n")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("未按索引表登记", self.view())

    def test_closing_heading_markers_preserve_index_and_acceptance_items(self):
        self.write("README.md", """## 任务索引 ##
| 任务 | 目录 |
| --- | --- |
| 另一路任务 | work/item |
## 已确认待拆解 ###
| ID | 事项 | 来源 |
| --- | --- | --- |
| REQ-02 | 已确认补充动作 | product/prd.md#REQ-02 |
""")
        self.write("work/item/tech/task-slices.md", source("done", acceptance="pending").replace(
            "## 验收任务", "  ## 验收任务 ##"))
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn("REQ-02", self.view())
        self.assertIn("另一路任务 / AC-01", self.view())
        self.assertIn("## 待验证 / 验收", self.view())

    def test_known_index_table_under_unknown_heading_reports_review_gap(self):
        self.write("tech/task-slices.md", source("done"))
        self.write("README.md", """## 其他导航
| ID | 事项 | 来源 |
| --- | --- | --- |
| REQ-02 | 已确认补充动作 | product/prd.md#REQ-02 |
""")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("索引表位于未识别章节", self.view())
        self.assertNotIn("已登记来源中无未完成项", self.view())

    def test_invalid_status_malformed_table_duplicate_id_and_missing_evidence(self):
        cases = (
            (source("finished"), "未知状态"),
            (source().replace("| BE-01 |", "| BE-01 | extra |"), "错列"),
            (source() + "\n## 其他任务\n" + table(("BE-01", "同名动作", "pending", "验证", "记录")), "重复任务 ID"),
            (source("done").replace("测试记录 #case-1", "-"), "缺少证据"),
            (source("done").replace("验收追踪：随实现任务\n", ""), "验收归属未明确"),
            (source().replace("业务动作与交付结果", "旧格式结果"), "未识别表格"),
        )
        for content, expected in cases:
            with self.subTest(expected=expected):
                self.write("tech/task-slices.md", content)
                self.assertEqual(1, todo.refresh(self.root)[0])
                self.assertIn(expected, self.view())

    def test_unrelated_tables_and_code_examples_do_not_become_tasks(self):
        extra = "\n## 接口映射\n| 字段 | 语义 |\n| --- | --- |\n| id | 稳定标识 |\n\n```markdown\n## 示例\n" + source("in_progress") + "```\n"
        self.write("tech/task-slices.md", source("done") + extra)
        self.write("evidence/history/tech/task-slices.md", source("pending"))
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn("已登记来源中无未完成项", self.view())

    def test_markdown_source_and_json_compatibility_are_not_guessed(self):
        path = self.write("tech/task-slices.md", source())
        self.write("tech/task-slices.json", '{"old": true}')
        self.assertEqual(0, todo.refresh(self.root)[0])
        path.write_text(source("done").replace("任务来源：本文件", "任务来源：task-slices.json；沿用既有工具"))
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("未纳入自动汇总", self.view())
        path.write_text(source("done").replace("任务来源：本文件\n", ""))
        self.assertEqual(1, todo.refresh(self.root)[0])

    def test_equivalent_source_paths_are_accepted_but_other_authorities_are_not(self):
        path = self.write("tasks/item/tech/task-slices.md", source())
        for declaration in ("tech/task-slices.md", "tasks/item/tech/task-slices.md",
                            "./task-slices.md", str(path), "`tech/task-slices.md`",
                            "[权威源](tech/task-slices.md)"):
            with self.subTest(declaration=declaration):
                path.write_text(source().replace("任务来源：本文件", f"任务来源：{declaration}"))
                self.assertEqual(0, todo.refresh(self.root)[0])
                self.assertIn("item / BE-01", self.view())
        for declaration in ("../other/task-slices.md", "tech/task-slices.json",
                            "本文件；已从 JSON 导出，尚未同步"):
            with self.subTest(declaration=declaration):
                path.write_text(source().replace("任务来源：本文件", f"任务来源：{declaration}"))
                self.assertEqual(1, todo.refresh(self.root)[0])
                self.assertIn("未纳入自动汇总", self.view())

    def test_inactive_json_content_and_existence_do_not_affect_md_view(self):
        path = self.write("tech/task-slices.md", source())
        self.assertEqual(0, todo.refresh(self.root)[0])
        original_view = self.view()
        legacy = path.with_suffix(".json")
        legacy.write_bytes(b"\xff")
        original_read = Path.read_bytes
        def reject_legacy_read(checked):
            if checked == legacy:
                self.fail("inactive JSON must not be read")
            return original_read(checked)
        with patch.object(Path, "read_bytes", reject_legacy_read):
            self.assertEqual(0, todo.refresh(self.root, check=True)[0])
            legacy.write_bytes(b"changed legacy bytes")
            self.assertEqual(0, todo.refresh(self.root)[0])
            legacy.unlink()
            self.assertEqual(0, todo.refresh(self.root, check=True)[0])
        self.assertEqual(original_view, self.view())
        # No declaration plus an existing legacy source remains ambiguous.
        path.write_text(source().replace("任务来源：本文件\n", ""))
        legacy.write_bytes(b"\xff")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("未纳入自动汇总", self.view())
        self.assertNotIn("有效 UTF-8", self.view())

    def test_legacy_source_appearing_during_undeclared_md_read_is_detected(self):
        self.write("tech/task-slices.md", source().replace("任务来源：本文件\n", ""))
        view = todo.Todo(self.root)
        view.render()
        self.assertTrue(view.unchanged())
        self.write("tech/task-slices.json", "{}")
        self.assertFalse(view.unchanged())

    def test_pipe_cells_are_escaped_and_local_order_is_preserved(self):
        content = source().replace("提交处理结果", r"判断 a \| b")
        content += table(("BE-02", "后续独立动作", "pending", "必要输入具备", "复核中"))
        self.write("tech/task-slices.md", content)
        self.assertEqual(0, todo.refresh(self.root)[0])
        self.assertIn(r"判断 a \| b", self.view())
        self.assertLess(self.view().index("BE-01"), self.view().index("BE-02"))

    def test_failed_publication_preserves_old_view_and_source(self):
        path = self.write("tech/task-slices.md", source())
        todo.refresh(self.root)
        old = self.view()
        path.write_text(source("in_progress"))
        current = path.read_bytes()
        with patch.object(todo.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                todo.refresh(self.root)
        self.assertEqual(old, self.view())
        self.assertEqual(current, path.read_bytes())
        self.assertFalse(list(self.root.glob(".TODO-*")))

    def test_change_during_reading_does_not_publish_mixed_snapshot(self):
        self.write("tech/task-slices.md", source())
        self.write("TODO.md", todo.GENERATED + "\nold view")
        with patch.object(todo.Todo, "unchanged", side_effect=[True, False]):
            with self.assertRaisesRegex(ValueError, "发布前发生变化"):
                todo.refresh(self.root)
        self.assertEqual(todo.GENERATED + "\nold view", self.view())
        self.assertFalse(list(self.root.glob(".TODO-*")))

    def test_unmarked_todo_is_preserved_in_write_and_read_only_modes(self):
        path = self.write("tech/task-slices.md", source())
        for text in ("# 手工待办\n- 尚未归属的原始记录\n", "# 项目待办\n自动生成，请更新原任务。\n",
                     "# 手工文件\n```html\n" + todo.GENERATED + "\n```\n"):
            self.write("TODO.md", text)
            before = {p: p.read_bytes() for p in (path, self.root / "TODO.md")}
            for check in (False, True):
                with self.subTest(text=text, check=check):
                    with self.assertRaisesRegex(ValueError, "保留原文件"):
                        todo.refresh(self.root, check=check)
                    self.assertEqual(before, {p: p.read_bytes() for p in before})
            self.assertFalse(list(self.root.glob(".TODO-*")))

    def test_target_changed_during_generation_is_not_overwritten(self):
        self.write("tech/task-slices.md", source())
        todo.refresh(self.root)
        original = todo.Todo.unchanged
        calls = 0
        def concurrent_edit(view):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.root / "TODO.md").write_text("# 其他执行者更新的手工文件\n")
            return original(view)
        with patch.object(todo.Todo, "unchanged", concurrent_edit):
            with self.assertRaisesRegex(ValueError, "保留原文件"):
                todo.refresh(self.root)
        self.assertEqual("# 其他执行者更新的手工文件\n", self.view())
        self.assertFalse(list(self.root.glob(".TODO-*")))

    def test_symlinks_and_paths_cannot_escape_or_hide_missing_sources(self):
        self.write("tech/task-slices.md", source())
        (self.root / "TODO.md").symlink_to(self.root / "missing-view")
        with self.assertRaisesRegex(ValueError, "符号链接"):
            todo.refresh(self.root)
        (self.root / "TODO.md").unlink()
        (self.root / "tasks").mkdir()
        (self.root / "tasks/broken").symlink_to(self.root / "missing-task")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("tasks/broken/tech/task-slices.md", self.view())
        self.write("README.md", "## 任务索引\n| 任务 | 目录 |\n| --- | --- |\n| 错误目录 | ../outside |\n")
        todo.refresh(self.root)
        self.assertIn("须为项目内相对路径", self.view())

    def test_invalid_utf8_and_external_symlink_report_gaps_without_reading_outside(self):
        path = self.write("tech/task-slices.md", source())
        path.write_bytes(b"\xff")
        self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("有效 UTF-8", self.view())
        path.unlink()
        path.symlink_to(ROOT / "README.md")
        original = Path.read_bytes
        def read_inside(checked):
            if checked == path:
                self.fail("attempted to read a source symlink outside the project")
            return original(checked)
        with patch.object(Path, "read_bytes", read_inside):
            self.assertEqual(1, todo.refresh(self.root)[0])
        self.assertIn("符号链接越出项目", self.view())
        with self.assertRaisesRegex(ValueError, "派生的 TODO"):
            todo.refresh(self.root, "TODO.md")

    def test_check_is_read_only_and_cli_exit_codes_are_usable(self):
        self.write("tech/task-slices.md", source())
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--check"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_stage_contexts_load_principles_and_only_route_to_tool_details(self):
        product = sys.modules["product_artifacts"]
        for stage in product.CONTEXT_ARTIFACTS:
            with self.subTest(stage=stage):
                context = product.stage_context(stage)
                self.assertEqual(1, context.count("### 项目待办视图"))
                self.assertIn("engineering-contracts.md#待办工具用法", context)
                self.assertNotIn("task_todo.py", context)
                self.assertNotIn("### 待办工具用法", context)
                self.assertIn("验收及提交约束", context)


if __name__ == "__main__":
    unittest.main()
