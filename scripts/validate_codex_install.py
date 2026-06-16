#!/usr/bin/env python3
from __future__ import annotations

import filecmp
import os
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_FILE = SKILLS_DIR / "manifest.txt"
COMMON_ENTRY = "qwerdf-common"
MARKER_FILE = ".qwerdf-install-source"


@dataclass(frozen=True)
class InstallCheck:
    entry: str
    status: str
    source: Path
    destination: Path
    detail: str

    @property
    def ok(self) -> bool:
        return self.status == "OK installed"


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")
    return Path(configured).expanduser()


def skills_home() -> Path:
    return codex_home() / "skills"


def read_manifest() -> list[str]:
    if not MANIFEST_FILE.exists():
        raise SystemExit(f"Missing skill manifest: {MANIFEST_FILE}")

    skills: list[str] = []
    for raw_line in MANIFEST_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        skills.append(line)
    if not skills:
        raise SystemExit(f"No skills found in manifest: {MANIFEST_FILE}")
    return skills


def relative_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if MARKER_FILE in relative.parts:
            continue
        files.append(relative)
    return files


def copy_is_stale(source: Path, destination: Path) -> tuple[bool, str]:
    source_files = relative_files(source)
    destination_files = relative_files(destination)

    source_set = set(source_files)
    destination_set = set(destination_files)
    missing = sorted(source_set - destination_set)
    extra = sorted(destination_set - source_set)
    if missing:
        return True, f"missing copied file: {missing[0]}"
    if extra:
        return True, f"extra copied file: {extra[0]}"

    for relative in source_files:
        src_file = source / relative
        dest_file = destination / relative
        if not filecmp.cmp(src_file, dest_file, shallow=False):
            return True, f"stale copied file: {relative}"
    return False, "copy content matches current repository"


def source_marker_matches(destination: Path) -> bool:
    marker = destination / MARKER_FILE
    if not marker.is_file():
        return False
    return marker.read_text(encoding="utf-8").strip() == str(ROOT)


def check_entry(entry: str, install_root: Path) -> InstallCheck:
    source = SKILLS_DIR / entry
    destination = install_root / entry

    if not source.is_dir():
        return InstallCheck(entry, "MISSING", source, destination, "source directory is missing from repository")

    if not destination.exists() and not destination.is_symlink():
        return InstallCheck(entry, "MISSING", source, destination, "not installed in Codex skills directory")

    if destination.is_symlink():
        target = destination.resolve(strict=False)
        expected = source.resolve(strict=False)
        if target != expected:
            return InstallCheck(entry, "WRONG_TARGET", source, destination, f"symlink points to {target}")
        if not (destination / "SKILL.md").exists() and entry != COMMON_ENTRY:
            return InstallCheck(entry, "MISSING", source, destination, "installed symlink has no SKILL.md")
        return InstallCheck(entry, "OK installed", source, destination, "symlink points to current repository")

    if not destination.is_dir():
        return InstallCheck(entry, "CONFLICT", source, destination, "destination exists but is not a directory or symlink")

    if not source_marker_matches(destination):
        return InstallCheck(entry, "CONFLICT", source, destination, f"directory is not a qwerdf copy install from {ROOT}")

    if not (destination / "SKILL.md").exists() and entry != COMMON_ENTRY:
        return InstallCheck(entry, "MISSING", source, destination, "copied skill has no SKILL.md")

    stale, detail = copy_is_stale(source, destination)
    if stale:
        return InstallCheck(entry, "STALE_COPY", source, destination, detail)
    return InstallCheck(entry, "OK installed", source, destination, detail)


def advice_for(checks: list[InstallCheck]) -> list[str]:
    statuses = {check.status for check in checks if not check.ok}
    advice: list[str] = []
    if "MISSING" in statuses:
        advice.append("MISSING: run `bash scripts/install.sh` for symlink install, or `bash scripts/install.sh --copy` for copy install.")
    if "STALE_COPY" in statuses:
        advice.append("STALE_COPY: run `bash scripts/uninstall.sh && bash scripts/install.sh --copy` to refresh copied skills.")
    if "WRONG_TARGET" in statuses:
        advice.append("WRONG_TARGET: remove the conflicting symlink or run `bash scripts/uninstall.sh` if it was installed by qwerdf.")
    if "CONFLICT" in statuses:
        advice.append("CONFLICT: inspect the destination manually; this script will not treat non-qwerdf directories as installed.")
    if not advice:
        advice.append("All qwerdf skills are installed and match the current repository. No reinstall is needed.")
    advice.append("Note: this verifies files in the Codex skills directory; restart or refresh Codex if this session was already open.")
    return advice


def main() -> int:
    install_root = skills_home()
    entries = [COMMON_ENTRY, *read_manifest()]
    checks = [check_entry(entry, install_root) for entry in entries]

    print(f"Codex skills dir: {install_root}")
    print(f"Repository: {ROOT}")
    print("")
    print("| Entry | Status | Destination | Detail |")
    print("| --- | --- | --- | --- |")
    for check in checks:
        print(f"| `{check.entry}` | {check.status} | `{check.destination}` | {check.detail} |")

    print("")
    print("Advice:")
    for item in advice_for(checks):
        print(f"- {item}")

    return 0 if all(check.ok for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
