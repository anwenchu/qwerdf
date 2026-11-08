#!/usr/bin/env python3
"""Generate a project TODO view from Markdown task sources; Python 3.10+, stdlib."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote

from product_artifacts import rows, section_spans, visible_lines


COLUMNS = ("顺序", "ID", "业务动作与交付结果", "状态", "完成标准", "证据 / 阻断")
GROUPS = ("进行中", "待推进", "受阻", "待验证 / 验收", "已确认待拆解")
STATES = {"pending": "待推进", "in_progress": "进行中", "blocked": "受阻"}
GENERATED = "<!-- qwerdf:generated-todo:v1 -->"


def cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


class Todo:
    def __init__(self, root: Path, index: str = "README.md"):
        self.root = root.resolve()
        self.index = self.local(index)
        if self.index == self.root / "TODO.md":
            raise ValueError("项目索引不能指向派生的 TODO.md")
        self.reads: dict[Path, bytes | None] = {}
        self.listings: dict[Path, tuple[str, ...]] = {}
        self.presence: dict[Path, bool] = {}
        self.items: list[tuple[str, str, str, str, str, str]] = []
        self.gaps: list[str] = []

    def local(self, value: str) -> Path:
        match = re.fullmatch(r"\[[^\]]*\]\(([^)]+)\)", value.strip())
        value = unquote(match[1] if match else value.strip().strip("`"))
        relative = Path(value)
        if not value or relative.is_absolute() or ".." in relative.parts or "#" in value:
            raise ValueError(f"须为项目内相对路径：{value}")
        path = self.root / relative
        if not path.resolve().is_relative_to(self.root):
            raise ValueError(f"路径越出项目：{value}")
        return path

    def read(self, path: Path, *, optional: bool = False) -> str | None:
        try:
            if not path.resolve().is_relative_to(self.root):
                raise ValueError("符号链接越出项目")
            data = path.read_bytes()
        except (OSError, ValueError) as error:
            self.reads[path] = None
            if not optional or path.exists() or path.is_symlink():
                self.gaps.append(f"{path.relative_to(self.root)}：无法读取（{error}）")
            return None
        self.reads[path] = data
        try:
            return data.decode("utf-8")
        except UnicodeError as error:
            self.gaps.append(f"{path.relative_to(self.root)}：不是有效 UTF-8（{error}）")
            return None

    def table(self, body: str, columns: tuple[str, ...], location: str, *, tasks_only: bool = False):
        consumed: set[int] = set()
        result = rows(body, columns, consumed=consumed)
        headings = section_spans(body, children=False)
        def relevant(number: int, line: str) -> bool:
            if not tasks_only:
                return True
            names = {part.strip().strip("`*") for part in re.split(r"(?<!\\)\|", line)}
            title = next((title for title, start, end in headings if start < number <= end), "")
            return {"ID", "状态"}.issubset(names) or title in {"## 前端任务", "## 后端任务", "## 验收任务"}
        if any(line.strip().startswith("|") and number not in consumed and relevant(number, line)
               for number, line in visible_lines(body)):
            self.gaps.append(f"{location}：存在未识别表格，需核对列名和错列")
        if not tasks_only and not result and any(
                line.strip() and not line.strip().startswith(("|", "#"))
                for _, line in visible_lines(body)):
            self.gaps.append(f"{location}：未按索引表登记的内容需核对，不能静默略过")
        return result

    def source(self, directory: Path, name: str) -> None:
        path = directory / "tech/task-slices.md"
        relative = path.relative_to(self.root).as_posix()
        text = self.read(path)
        if text is None:
            return
        source = [line.split("：", 1)[1].strip() for _, line in visible_lines(text)
                  if line.startswith("任务来源：")]
        def points_here(value: str) -> bool:
            if value == "本文件":
                return True
            link = re.fullmatch(r"\[[^\]]*\]\(([^)]+)\)", value)
            declared = Path(unquote(link[1] if link else value.strip("`")))
            # Accept equivalent source locations, not prose or another source.
            try:
                return bool(value) and any((base / declared).resolve() == path.resolve()
                                           for base in (self.root, directory, path.parent))
            except (OSError, ValueError, RuntimeError):
                return False

        # An explicit MD authority makes a leftover JSON irrelevant. Without a
        # declaration, track existence only; never decode an unknown legacy schema.
        legacy = directory / "tech/task-slices.json"
        if not source:
            self.presence[legacy] = legacy.exists() or legacy.is_symlink()
        if (source and not all(points_here(value) for value in source)) or (not source and self.presence[legacy]):
            self.gaps.append(f"{relative}：权威来源未确认指向当前 Markdown；沿既有工具核实来源及视图，未纳入自动汇总")
            return
        parsed = self.table(text, COLUMNS, relative, tasks_only=True)
        if not parsed:
            self.gaps.append(f"{relative}：未识别任务行；尚未拆解或格式需人工核对")
            return
        headings = section_spans(text, children=False)
        seen: set[str] = set()
        acceptance = False
        for line, item in parsed:
            title = next((title.lstrip("# ") for title, start, end in headings
                          if start < line <= end), "任务")
            if not all(item.get(key, "").strip() for key in COLUMNS[:-1]):
                self.gaps.append(f"{relative}:{line}：任务字段为空或表格错列")
                continue
            task_id, status = item["ID"], item["状态"]
            if task_id in seen:
                self.gaps.append(f"{relative}:{line}：重复任务 ID {task_id}")
                continue
            seen.add(task_id)
            if status not in {*STATES, "done"}:
                self.gaps.append(f"{relative}:{line}：未知状态 {status}，不得当作完成")
                continue
            acceptance |= title == "验收任务"
            evidence = item["证据 / 阻断"]
            if status == "done":
                if not evidence or re.fullmatch(r"[-—/]+|待补充|TODO|TBD", evidence, re.I):
                    self.gaps.append(f"{relative}:{line}：{task_id} 标为 done 但缺少证据定位，需复核")
                continue
            group = STATES[status]
            if title == "验收任务" and status != "blocked":
                group = "待验证 / 验收"
            link = f"[{cell(name)} / {cell(task_id)}]({quote(relative, safe='/')}#L{line})"
            self.items.append((group, link, f"{title} · {item['业务动作与交付结果']}",
                               status, item["完成标准"], evidence or "待补充下一动作 / 卡点"))
        tracking = [line.split("：", 1)[1].strip() for _, line in visible_lines(text)
                    if line.startswith("验收追踪：")]
        if not acceptance and tracking != ["随实现任务"]:
            self.gaps.append(f"{relative}：验收归属未明确；核对既有验收来源，将尚未通过的验收保留为任务，不能仅凭编码 done 清空待办")

    def collect(self) -> None:
        sources: dict[Path, str] = {}
        index_text = self.read(self.index, optional=self.index == self.root / "README.md")
        if index_text is not None:
            covered: set[int] = set()
            for title, start, end in section_spans(index_text):
                if title not in {"## 任务索引", "## 已确认待拆解"}:
                    continue
                body = "\n".join(index_text.splitlines()[start + 1:end])
                covered.update(range(start + 1, end + 1))
                columns = ("任务", "目录") if title == "## 任务索引" else ("ID", "事项", "来源")
                for line, item in self.table(body, columns, f"{self.index.name}:{start + 1}"):
                    if not all(item.get(key, "").strip() for key in columns):
                        self.gaps.append(f"{self.index.name}:{start + line + 1}：索引字段为空或错列")
                        continue
                    if title == "## 任务索引":
                        try:
                            directory = self.local(item["目录"])
                            sources[directory] = item["任务"]
                        except ValueError as error:
                            self.gaps.append(f"{self.index.name}:{start + line + 1}：{error}")
                    else:
                        link = f"[{cell(item['ID'])}]({quote(self.index.relative_to(self.root).as_posix(), safe='/')}#L{start + line + 1})"
                        self.items.append(("已确认待拆解", link, item["事项"], "未拆解 / 未归属", "沿原确认来源", item["来源"]))
            for columns in (("任务", "目录"), ("ID", "事项", "来源")):
                unplaced = [line for line, _ in rows(index_text, columns) if line not in covered]
                if unplaced:
                    self.gaps.append(f"{self.index.name}:{unplaced[0]}：索引表位于未识别章节，需人工核对归属，未纳入自动汇总")
        tasks = self.root / "tasks"
        try:
            if tasks.exists() or tasks.is_symlink():
                if not tasks.resolve().is_relative_to(self.root):
                    raise ValueError("tasks 符号链接越出项目")
                children = sorted(tasks.iterdir())
                self.listings[tasks] = tuple(child.name for child in children)
                for child in children:
                    if child.is_dir() or child.is_symlink():
                        sources.setdefault(child, child.name)
            else:
                self.listings[tasks] = ()
        except (OSError, ValueError) as error:
            self.gaps.append(f"tasks：无法枚举任务（{error}）")
        path = self.root / "tech/task-slices.md"
        if path.exists() or path.is_symlink():
            sources.setdefault(self.root, "项目共用任务")
        else:
            self.reads[path] = None
            legacy = self.root / "tech/task-slices.json"
            self.presence[legacy] = legacy.exists() or legacy.is_symlink()
            if self.presence[legacy]:
                sources.setdefault(self.root, "项目共用任务")
        if not sources:
            self.gaps.append("未定位任务来源；核对任务索引，不能认定项目已无待办")
        # Resolve aliases so an indexed directory and its symlink are not counted twice.
        visited = set()
        for directory, name in sorted(sources.items()):
            if directory.resolve() not in visited:
                self.source(directory, name)
                visited.add(directory.resolve())

    def render(self) -> str:
        self.collect()
        fingerprint = hashlib.sha256()
        for path, data in sorted(self.reads.items()):
            fingerprint.update(str(path.relative_to(self.root)).encode() + b"\0")
            fingerprint.update(b"missing" if data is None else data)
        for path, names in sorted(self.listings.items()):
            fingerprint.update(str(path.relative_to(self.root)).encode() + repr(names).encode())
        for path, exists in sorted(self.presence.items()):
            fingerprint.update(str(path.relative_to(self.root)).encode() + str(exists).encode())
        output = [GENERATED, "", "# 项目待办", "", "自动生成，请更新各任务权威源后刷新；勿手改本视图。",
                  "只汇总已登记事项，不判断需求完整性、真实输入就绪或上线资格；使用前运行同一命令加 `--check` 核对是否滞后。",
                  f"来源指纹：`{fingerprint.hexdigest()}`。", ""]
        for group in GROUPS:
            items = [item for item in self.items if item[0] == group]
            if not items:
                continue
            output.extend([f"## {group}", "", "| 归属 / ID | 业务动作 | 源状态 | 完成标准 / 剩余验收 | 证据 / 卡点 / 下一动作 |",
                           "| --- | --- | --- | --- | --- |"])
            output.extend("| " + " | ".join([item[1], *(cell(value) for value in item[2:])]) + " |" for item in items)
            output.append("")
        if self.gaps:
            output.extend(["## 来源缺口（汇总不完整）", ""])
            output.extend(f"- {gap}" for gap in self.gaps)
            output.append("")
        elif not self.items:
            output.extend(["已登记来源中无未完成项；不代表未登记需求已覆盖或项目已可上线。", ""])
        return "\n".join(output)

    def unchanged(self) -> bool:
        for path, original in self.reads.items():
            try:
                current = path.read_bytes() if path.resolve().is_relative_to(self.root) else None
            except OSError:
                current = None
            if current != original:
                return False
        for path, names in self.listings.items():
            if not path.resolve().is_relative_to(self.root):
                return False
            current = tuple(sorted(child.name for child in path.iterdir())) if path.exists() else ()
            if current != names:
                return False
        if any((path.exists() or path.is_symlink()) != exists for path, exists in self.presence.items()):
            return False
        return True


def read_generated(target: Path) -> bytes | None:
    """Refuse to take ownership of a hand-maintained or otherwise unknown file."""
    if target.is_symlink():
        raise ValueError("TODO.md 是符号链接，不覆盖其目标")
    try:
        data = target.read_bytes()
    except FileNotFoundError:
        return None
    if not data.startswith((GENERATED + "\n").encode()):
        raise ValueError("已有 TODO.md 缺少本工具生成标记，保留原文件；先核对归属，不自动接管或迁移")
    return data


def refresh(root: Path, index: str = "README.md", *, check: bool = False) -> tuple[int, str]:
    if not root.is_dir():
        raise ValueError(f"项目根目录不存在：{root}")
    view = Todo(root, index)
    target = view.root / "TODO.md"
    previous = read_generated(target)
    content = view.render()
    if not view.unchanged():
        raise ValueError("来源在读取期间发生变化，未发布视图；重新读取后刷新")
    if check:
        if previous != content.encode():
            return 1, "TODO.md 缺失或滞后；请刷新后再用于汇报"
    else:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=view.root,
                                             prefix=".TODO-", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(content)
            if not view.unchanged():
                raise ValueError("来源在发布前发生变化，未覆盖旧视图；重新读取后刷新")
            if read_generated(target) != previous:
                raise ValueError("TODO.md 在生成期间发生变化，保留最新文件；重新核对后刷新")
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    if view.gaps:
        return 1, "TODO.md 含来源缺口，汇总不完整：\n" + "\n".join(view.gaps)
    return 0, "TODO.md 已核对" if check else "TODO.md 已刷新（不改变源任务状态）"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="退出码：0 视图已刷新/一致；1 缺口或滞后；2 失败，旧视图不可当作最新结果。")
    parser.add_argument("--root", type=Path, required=True, help="项目根目录，也支持单个独立任务")
    parser.add_argument("--index", default="README.md", help="已有项目索引的根目录内相对路径")
    parser.add_argument("--check", action="store_true", help="只读检查视图是否与源一致")
    args = parser.parse_args()
    try:
        code, message = refresh(args.root, args.index, check=args.check)
        print(message)
        return code
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"TODO 刷新失败：{error}；未将旧视图认定为当前结果。\n")


if __name__ == "__main__":
    raise SystemExit(main())
