#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_home="${CODEX_HOME:-$HOME/.codex}/skills"
project_state_dir="$skills_home/.qwerdf"
manifest="$project_state_dir/manifest.tsv"
skill_manifest="$repo_root/skills/manifest.txt"
common_entry="qwerdf-common"
common_src="$repo_root/skills/$common_entry"
common_dest="$skills_home/$common_entry"
dry_run=0
copy_mode=0

is_project_copy() {
  local dest="$1"
  local marker="$dest/.qwerdf-install-source"
  [[ -d "$dest" && ! -L "$dest" && -f "$marker" ]] || return 1
  [[ "$(cat "$marker")" == "$repo_root" ]]
}

usage() {
  cat <<'USAGE'
Usage: bash scripts/install.sh [--dry-run] [--copy]

Installs qwerdf skills into ${CODEX_HOME:-$HOME/.codex}/skills.
Project-owned install state is kept in ${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/.

Options:
  --dry-run   Show planned actions without writing.
  --copy      Copy skill directories instead of creating symlinks.
  -h, --help  Show this help.
USAGE
}

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      dry_run=1
      ;;
    --copy)
      copy_mode=1
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

if [[ ! -f "$skill_manifest" ]]; then
  echo "Missing skill manifest: $skill_manifest" >&2
  exit 1
fi

if [[ ! -d "$common_src" ]]; then
  echo "Missing common directory: $common_src" >&2
  exit 1
fi

skills=()
while IFS= read -r line; do
  [[ -z "$line" || "$line" == \#* ]] && continue
  skills+=("$line")
done < "$skill_manifest"

if [[ "${#skills[@]}" -eq 0 ]]; then
  echo "No skills found in manifest: $skill_manifest" >&2
  exit 1
fi

echo "Target skills dir: $skills_home"
echo "Project state dir: $project_state_dir"

if [[ "$copy_mode" -eq 1 ]]; then
  if [[ -L "$common_dest" ]]; then
    echo "Refusing to overwrite existing common symlink: $common_dest -> $(readlink "$common_dest")" >&2
    exit 1
  fi
  if [[ -e "$common_dest" ]] && ! is_project_copy "$common_dest"; then
    echo "Refusing to overwrite existing common directory: $common_dest" >&2
    exit 1
  fi
else
  if [[ -L "$common_dest" ]]; then
    current="$(readlink "$common_dest")"
    if [[ "$current" != "$common_src" ]]; then
      echo "Refusing to overwrite existing common symlink: $common_dest -> $current" >&2
      exit 1
    fi
  elif [[ -e "$common_dest" ]]; then
    echo "Refusing to overwrite existing common directory: $common_dest" >&2
    exit 1
  fi
fi

for skill in "${skills[@]}"; do
  src="$repo_root/skills/$skill"
  dest="$skills_home/$skill"

  if [[ ! -d "$src" ]]; then
    echo "Missing skill directory: $src" >&2
    exit 1
  fi

  if [[ -L "$dest" ]]; then
    current="$(readlink "$dest")"
    if [[ "$current" == "$src" ]]; then
      if [[ "$copy_mode" -eq 1 ]]; then
        echo "Refusing to replace existing symlink install with copy mode: $dest" >&2
        echo "Run bash scripts/uninstall.sh first, then retry with --copy." >&2
        exit 1
      fi
      continue
    fi
    echo "Refusing to overwrite existing symlink: $dest -> $current" >&2
    exit 1
  fi

  if [[ -e "$dest" ]]; then
    if [[ "$copy_mode" -eq 1 ]] && is_project_copy "$dest"; then
      continue
    fi
    echo "Refusing to overwrite existing skill: $dest" >&2
    exit 1
  fi
done

if [[ "$dry_run" -eq 1 ]]; then
  echo "Would ensure project state dir exists: $project_state_dir"
  echo "Would write manifest: $manifest"
else
  mkdir -p "$skills_home" "$project_state_dir"
  {
    echo "# qwerdf skill install manifest"
    echo "# entry	mode	source	destination"
  } > "$manifest"
fi

if [[ "$copy_mode" -eq 1 ]]; then
  if [[ "$dry_run" -eq 1 ]]; then
    if is_project_copy "$common_dest"; then
      echo "Would keep existing common copy: $common_entry -> $common_dest"
    else
      echo "Would copy common templates: $common_src -> $common_dest"
    fi
  else
    if is_project_copy "$common_dest"; then
      echo "Already installed common templates: $common_entry -> $common_dest"
    else
      cp -R "$common_src" "$common_dest"
      printf '%s\n' "$repo_root" > "$common_dest/.qwerdf-install-source"
      echo "Copied common templates: $common_entry"
    fi
    printf '%s\t%s\t%s\t%s\n' "$common_entry" "copy" "$common_src" "$common_dest" >> "$manifest"
  fi
else
  if [[ "$dry_run" -eq 1 ]]; then
    if [[ -L "$common_dest" && "$(readlink "$common_dest")" == "$common_src" ]]; then
      echo "Would keep existing common symlink: $common_entry -> $common_src"
    else
      echo "Would symlink common templates: $common_dest -> $common_src"
    fi
  else
    if [[ -L "$common_dest" && "$(readlink "$common_dest")" == "$common_src" ]]; then
      echo "Already installed common templates: $common_entry -> $common_src"
    else
      ln -s "$common_src" "$common_dest"
      echo "Linked common templates: $common_entry -> $common_src"
    fi
    printf '%s\t%s\t%s\t%s\n' "$common_entry" "symlink" "$common_src" "$common_dest" >> "$manifest"
  fi
fi

for skill in "${skills[@]}"; do
  src="$repo_root/skills/$skill"
  dest="$skills_home/$skill"

  if [[ "$dry_run" -eq 1 ]]; then
    if [[ "$copy_mode" -eq 1 ]]; then
      if is_project_copy "$dest"; then
        echo "Would keep existing copy: $skill -> $dest"
      else
        echo "Would copy: $src -> $dest"
      fi
    elif [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
      echo "Would keep existing symlink: $skill -> $src"
    else
      echo "Would symlink: $dest -> $src"
    fi
    continue
  fi

  if [[ "$copy_mode" -eq 1 ]]; then
    if is_project_copy "$dest"; then
      echo "Already installed: $skill -> $dest"
    else
      cp -R "$src" "$dest"
      printf '%s\n' "$repo_root" > "$dest/.qwerdf-install-source"
      echo "Copied: $skill"
    fi
    printf '%s\t%s\t%s\t%s\n' "$skill" "copy" "$src" "$dest" >> "$manifest"
  else
    if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
      echo "Already installed: $skill -> $src"
    else
      ln -s "$src" "$dest"
      echo "Linked: $skill -> $src"
    fi
    printf '%s\t%s\t%s\t%s\n' "$skill" "symlink" "$src" "$dest" >> "$manifest"
  fi
done

echo "Install check complete."
