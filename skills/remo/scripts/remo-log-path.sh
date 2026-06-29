#!/bin/sh
# Print a ReMo log file path using the repo machine's local date/time.
# Usage: sh skills/remo/scripts/remo-log-path.sh "记忆语言标题"
#
# Agents MUST use this script for log paths. Do not infer or hand-write
# YYYY/MM/DD/HHMM- from session time, cloud timezone, or model context.

set -eu

title="${1:-}"
if [ -z "$title" ]; then
  printf 'Usage: %s "记忆语言标题"\n' "$0" >&2
  exit 1
fi

case "$title" in
  */* | *\\*)
    printf 'log title must not contain path separators: %s\n' "$title" >&2
    exit 1
    ;;
esac

if git_root=$(git rev-parse --show-toplevel 2>/dev/null); then
  cd "$git_root" || exit 2
fi

year=$(date +%Y)
month=$(date +%m)
day=$(date +%d)
hhmm=$(date +%H%M)

dir=".remo/logs/$year/$month/$day"
mkdir -p "$dir"

path="$dir/${hhmm}-${title}.md"
if [ -e "$path" ]; then
  suffix=2
  while [ -e "$dir/${hhmm}-${title}-${suffix}.md" ]; do
    suffix=$((suffix + 1))
  done
  path="$dir/${hhmm}-${title}-${suffix}.md"
fi

printf '%s\n' "$path"
