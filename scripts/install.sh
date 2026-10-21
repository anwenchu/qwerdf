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
force_mode=0

is_project_copy() {
  local dest="$1"
  local marker="$dest/.qwerdf-install-source"
  [[ -d "$dest" && ! -L "$dest" && -f "$marker" ]] || return 1
  [[ "$(cat "$marker")" == "$repo_root" ]]
}

is_current_symlink() {
  local dest="$1"
  local src="$2"
  [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]
}

remove_project_owned_install() {
  local dest="$1"
  local src="$2"

  if is_current_symlink "$dest" "$src"; then
    rm "$dest"
    return 0
  fi

  if is_project_copy "$dest"; then
    rm -rf "$dest"
    return 0
  fi

  return 1
}

usage() {
  cat <<'USAGE'
Usage: bash scripts/install.sh [--dry-run] [--copy] [--force]

Installs qwerdf skills into ${CODEX_HOME:-$HOME/.codex}/skills.
Project-owned install state is kept in ${CODEX_HOME:-$HOME/.codex}/skills/.qwerdf/.

Options:
  --dry-run   Show planned actions without writing.
  --copy      Copy skill directories instead of creating symlinks. Existing qwerdf-owned copies are refreshed.
  --force     Replace qwerdf-owned installs when switching between symlink and copy mode.
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
    --force)
      force_mode=1
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
  if [[ -e "$common_dest" || -L "$common_dest" ]]; then
    if is_project_copy "$common_dest"; then
      :
    elif is_current_symlink "$common_dest" "$common_src"; then
      if [[ "$force_mode" -ne 1 ]]; then
        echo "Refusing to replace existing common symlink with copy mode: $common_dest" >&2
        echo "Use --copy --force to replace the qwerdf-owned symlink with a refreshed copy." >&2
        exit 1
      fi
    elif [[ -L "$common_dest" ]]; then
      echo "Refusing to overwrite existing common symlink: $common_dest -> $(readlink "$common_dest")" >&2
      exit 1
    else
      echo "Refusing to overwrite existing common directory: $common_dest" >&2
      exit 1
    fi
  fi
else
  if [[ -L "$common_dest" ]]; then
    current="$(readlink "$common_dest")"
    if [[ "$current" != "$common_src" ]]; then
      echo "Refusing to overwrite existing common symlink: $common_dest -> $current" >&2
      exit 1
    fi
  elif [[ -e "$common_dest" ]]; then
    if [[ "$force_mode" -eq 1 ]] && is_project_copy "$common_dest"; then
      :
    else
      echo "Refusing to overwrite existing common directory: $common_dest" >&2
      echo "Use --force to replace a qwerdf-owned copy with a live symlink." >&2
      exit 1
    fi
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
        if [[ "$force_mode" -eq 1 ]]; then
          continue
        fi
        echo "Refusing to replace existing symlink install with copy mode: $dest" >&2
        echo "Use --copy --force to replace the qwerdf-owned symlink with a refreshed copy." >&2
        exit 1
      fi
      continue
    fi
    echo "Refusing to overwrite existing symlink: $dest -> $current" >&2
    exit 1
  fi

  if [[ -e "$dest" ]]; then
    if is_project_copy "$dest"; then
      if [[ "$copy_mode" -eq 1 || "$force_mode" -eq 1 ]]; then
        continue
      fi
      echo "Refusing to replace existing qwerdf-owned copy with symlink mode: $dest" >&2
      echo "Use --force to replace the qwerdf-owned copy with a live symlink." >&2
      exit 1
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
      echo "Would refresh existing common copy: $common_entry -> $common_dest"
    elif is_current_symlink "$common_dest" "$common_src"; then
      echo "Would replace common symlink with copy: $common_entry -> $common_dest"
    else
      echo "Would copy common templates: $common_src -> $common_dest"
    fi
  else
    if is_project_copy "$common_dest" || is_current_symlink "$common_dest" "$common_src"; then
      remove_project_owned_install "$common_dest" "$common_src"
      cp -R "$common_src" "$common_dest"
      printf '%s\n' "$repo_root" > "$common_dest/.qwerdf-install-source"
      echo "Refreshed common templates copy: $common_entry"
    else
      cp -R "$common_src" "$common_dest"
      printf '%s\n' "$repo_root" > "$common_dest/.qwerdf-install-source"
      echo "Copied common templates: $common_entry"
    fi
    printf '%s\t%s\t%s\t%s\n' "$common_entry" "copy" "$common_src" "$common_dest" >> "$manifest"
  fi
else
  if [[ "$dry_run" -eq 1 ]]; then
    if is_current_symlink "$common_dest" "$common_src"; then
      echo "Would keep existing live common symlink: $common_entry -> $common_src"
    elif is_project_copy "$common_dest"; then
      echo "Would replace existing common copy with live symlink: $common_entry -> $common_src"
    else
      echo "Would symlink common templates: $common_dest -> $common_src"
    fi
  else
    if is_current_symlink "$common_dest" "$common_src"; then
      echo "Already installed common templates as live symlink: $common_entry -> $common_src"
    else
      if is_project_copy "$common_dest"; then
        remove_project_owned_install "$common_dest" "$common_src"
      fi
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
        echo "Would refresh existing copy: $skill -> $dest"
      elif is_current_symlink "$dest" "$src"; then
        echo "Would replace symlink with copy: $skill -> $dest"
      else
        echo "Would copy: $src -> $dest"
      fi
    elif is_current_symlink "$dest" "$src"; then
      echo "Would keep existing live symlink: $skill -> $src"
    elif is_project_copy "$dest"; then
      echo "Would replace existing copy with live symlink: $skill -> $src"
    else
      echo "Would symlink: $dest -> $src"
    fi
    continue
  fi

  if [[ "$copy_mode" -eq 1 ]]; then
    if is_project_copy "$dest" || is_current_symlink "$dest" "$src"; then
      remove_project_owned_install "$dest" "$src"
      cp -R "$src" "$dest"
      printf '%s\n' "$repo_root" > "$dest/.qwerdf-install-source"
      echo "Refreshed copy: $skill"
    else
      cp -R "$src" "$dest"
      printf '%s\n' "$repo_root" > "$dest/.qwerdf-install-source"
      echo "Copied: $skill"
    fi
    printf '%s\t%s\t%s\t%s\n' "$skill" "copy" "$src" "$dest" >> "$manifest"
  else
    if is_current_symlink "$dest" "$src"; then
      echo "Already installed as live symlink: $skill -> $src"
    else
      if is_project_copy "$dest"; then
        remove_project_owned_install "$dest" "$src"
      fi
      ln -s "$src" "$dest"
      echo "Linked: $skill -> $src"
    fi
    printf '%s\t%s\t%s\t%s\n' "$skill" "symlink" "$src" "$dest" >> "$manifest"
  fi
done

echo "Install check complete."
