#!/bin/sh

set -u

failures=0
warnings=0

say() {
  printf '%s\n' "$1"
}

fail() {
  failures=$((failures + 1))
  say "FAIL: $1"
}

warn() {
  warnings=$((warnings + 1))
  say "WARN: $1"
}

has_line() {
  grep -Eq "$1" "$2"
}

check_required_field() {
  field="$1"
  file="$2"
  if ! has_line "^$field:" "$file"; then
    fail "$file missing frontmatter field: $field"
  fi
}

check_required_section() {
  section="$1"
  file="$2"
  if ! grep -Fq "## $section" "$file"; then
    fail "$file missing section: $section"
  fi
}

check_source_paths() {
  file="$1"
  in_paths=0
  found_path=0

  while IFS= read -r line; do
    case "$line" in
      source_paths:*)
        in_paths=1
        ;;
      evidence:*|supersedes:*|related:*|---)
        in_paths=0
        ;;
      "  - "*)
        if [ "$in_paths" -eq 1 ]; then
          path=${line#  - }
          found_path=1
          if [ ! -e "$path" ]; then
            fail "$file source path does not exist: $path"
          fi
        fi
        ;;
      *)
        ;;
    esac
  done < "$file"

  if [ "$found_path" -eq 0 ]; then
    warn "$file has no source_paths entries"
  fi
}

if git_root=$(git rev-parse --show-toplevel 2>/dev/null); then
  cd "$git_root" || exit 2
fi

if [ ! -f ".remo/config.yml" ]; then
  fail "missing .remo/config.yml"
fi

if [ ! -d ".remo" ]; then
  fail "missing .remo/"
fi

if [ ! -d ".remo/logs" ]; then
  fail "missing .remo/logs/"
fi

for file in $(find .remo/logs -type f -name '*.md' 2>/dev/null | sort); do
  base=$(basename "$file")
  if ! printf '%s' "$base" | grep -Eq '^[0-9]{4}-'; then
    fail "log filename must start with HHMM-: $file (see skills/remo/templates/log-entry.md)"
  fi
done

if [ ! -d ".remo/knowledge" ]; then
  fail "missing .remo/knowledge/"
fi

if [ ! -d ".remo/knowledge/maps" ]; then
  warn "missing .remo/knowledge/maps/"
fi

if [ ! -d ".remo/knowledge/topics" ]; then
  warn "missing .remo/knowledge/topics/"
fi

if [ ! -f ".remo/knowledge/index.md" ]; then
  fail "missing .remo/knowledge/index.md"
fi

if [ -f ".remo/knowledge/index.md" ]; then
  for file in $(find .remo/knowledge -type f -name '*.md' | sort); do
    case "$file" in
      .remo/knowledge/index.md)
        ;;
      *)
        base=$(basename "$file")
        rel=${file#./}
        if ! grep -Fq "$base" ".remo/knowledge/index.md" && ! grep -Fq "$rel" ".remo/knowledge/index.md"; then
          fail "$file exists but is not mentioned in .remo/knowledge/index.md"
        fi
        ;;
    esac
  done
fi

for file in $(find .remo/knowledge -type f -name '*.md' ! -name 'index.md' 2>/dev/null | sort); do
  first_line=$(sed -n '1p' "$file")
  if [ "$first_line" != "---" ]; then
    fail "$file missing YAML frontmatter"
    continue
  fi

  for field in id title type status scope confidence last_verified source_paths evidence supersedes related; do
    check_required_field "$field" "$file"
  done

  for section in Summary "When To Read" "Current Knowledge" "Agent Guidance" Evidence "Invalidation Signals"; do
    check_required_section "$section" "$file"
  done

  check_source_paths "$file"
done

if [ -f ".cursor/rules/remo.mdc" ]; then
  if ! grep -Eq "(\.cursor/skills/remo/SKILL\.md|skills/remo/SKILL\.md)" ".cursor/rules/remo.mdc"; then
    fail ".cursor/rules/remo.mdc does not mention ReMo canonical SKILL.md path"
  fi
  if ! grep -Fq ".remo/knowledge/index.md" ".cursor/rules/remo.mdc"; then
    fail ".cursor/rules/remo.mdc does not mention .remo/knowledge/index.md"
  fi
else
  warn "no .cursor/rules/remo.mdc installed; ReMo will not be continuously prompted in Cursor"
fi

if [ -f "AGENTS.md" ]; then
  if ! grep -Fq "ReMo Project Memory" "AGENTS.md"; then
    fail "AGENTS.md does not contain a ReMo Project Memory section"
  fi
  if ! grep -Eq "(\.cursor/skills/remo/SKILL\.md|skills/remo/SKILL\.md)" "AGENTS.md"; then
    fail "AGENTS.md does not mention ReMo canonical SKILL.md path"
  fi
  if ! grep -Fq ".remo/knowledge/index.md" "AGENTS.md"; then
    fail "AGENTS.md does not mention .remo/knowledge/index.md"
  fi
else
  warn "no AGENTS.md installed; Codex and generic Coding Agents may not discover ReMo automatically"
fi

if git diff --cached --quiet 2>/dev/null; then
  :
else
  if git diff --cached --name-only | grep -Eq '^"?\.remo/'; then
    :
  else
    warn "staged changes exist without a staged .remo/ entry; the whole .remo/ knowledge base is git-tracked—add .remo/ changes unless this commit is truly knowledge-free"
  fi
fi

if [ "$failures" -gt 0 ]; then
  say "ReMo check failed: $failures failure(s), $warnings warning(s)."
  exit 1
fi

say "ReMo check passed: $warnings warning(s)."
