#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_home="${CODEX_HOME:-$HOME/.codex}/skills"
project_state_dir="$skills_home/.qwerdf"
manifest="$project_state_dir/manifest.tsv"
dry_run=0

usage() {
  cat <<'USAGE'
Usage: bash scripts/uninstall.sh [--dry-run]

Uninstalls qwerdf skills from ${CODEX_HOME:-$HOME/.codex}/skills.
Only entries recorded in ${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/manifest.tsv are removed.

Options:
  --dry-run   Show planned actions without deleting.
  -h, --help  Show this help.
USAGE
}

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      dry_run=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

echo "Target skills dir: $skills_home"
echo "Project state dir: $project_state_dir"

if [[ ! -f "$manifest" ]]; then
  echo "No qwerdf manifest found: $manifest"
  echo "Nothing to uninstall."
  exit 0
fi

while IFS=$'\t' read -r skill mode src dest; do
  if [[ -z "${skill:-}" || "$skill" == \#* ]]; then
    continue
  fi

  expected_src="$repo_root/skills/$skill"
  expected_dest="$skills_home/$skill"

  if [[ "$src" != "$expected_src" || "$dest" != "$expected_dest" ]]; then
    echo "Refusing manifest entry outside this repository: $skill" >&2
    echo "  source: $src" >&2
    echo "  destination: $dest" >&2
    exit 1
  fi

  if [[ ! -e "$dest" && ! -L "$dest" ]]; then
    echo "Not installed: $skill"
    continue
  fi

  case "$mode" in
    symlink)
      if [[ ! -L "$dest" ]]; then
        echo "Refusing to remove non-symlink skill recorded as symlink: $dest" >&2
        exit 1
      fi
      current="$(readlink "$dest")"
      if [[ "$current" != "$src" ]]; then
        echo "Refusing to remove symlink pointing elsewhere: $dest -> $current" >&2
        exit 1
      fi
      if [[ "$dry_run" -eq 1 ]]; then
        echo "Would remove symlink: $dest"
      else
        rm "$dest"
        echo "Removed symlink: $skill"
      fi
      ;;
    copy)
      marker="$dest/.qwerdf-install-source"
      if [[ ! -d "$dest" || -L "$dest" ]]; then
        echo "Refusing to remove invalid copy install target: $dest" >&2
        exit 1
      fi
      if [[ ! -f "$marker" || "$(cat "$marker")" != "$repo_root" ]]; then
        echo "Refusing to remove copied skill without matching qwerdf marker: $dest" >&2
        exit 1
      fi
      if [[ "$dry_run" -eq 1 ]]; then
        echo "Would remove copied skill directory: $dest"
      else
        rm -rf "$dest"
        echo "Removed copied skill: $skill"
      fi
      ;;
    *)
      echo "Unknown install mode in manifest for $skill: $mode" >&2
      exit 1
      ;;
  esac
done < "$manifest"

if [[ "$dry_run" -eq 1 ]]; then
  echo "Would remove project manifest directory if empty: $project_state_dir"
else
  rm -f "$manifest"
  rmdir "$project_state_dir" 2>/dev/null || true
fi

echo "Uninstall check complete."
