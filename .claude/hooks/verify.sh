#!/bin/bash
# PostToolUse: run the project's own type/lint check after an edit.
#
# Replaces the TypeScript-only hook this template used to ship. It detects the
# stack from the marker files that are actually present and runs the cheapest
# correctness check that stack offers -- so the template works for a Node, a
# Python, a Rust, a Go, or a .NET project without being edited.
#
# async + asyncRewake: never blocks an edit, silent on success, wakes the model
# only when the check actually fails.
#
# Silence is the design. If a stack is not set up (no tsconfig, no venv, no
# lockfile) the hook exits 0 without saying anything, so a fresh repo does not
# report failures that have nothing to do with the code.
set -uo pipefail

payload=$(cat)

read_field() {
  printf '%s' "$payload" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    print(''); raise SystemExit
ti = d.get('tool_input') or {}
tr = d.get('tool_response') or {}
print(tr.get('filePath') or ti.get('file_path') or '')
" 2>/dev/null || printf ''
}

file=$(read_field)
[ -n "$file" ] || exit 0

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$root" || exit 0

# The edit may have been a delete, a rename, or a path outside the project.
# Nothing to check in any of those cases.
[ -f "$file" ] || exit 0

run() {  # run <label> <command...>
  local label="$1"; shift
  local out status
  out=$("$@" 2>&1); status=$?
  if [ $status -ne 0 ]; then
    echo "$label FAILED after editing $(basename "$file"):"
    printf '%s\n' "$out" | head -30
    exit 2
  fi
  exit 0
}

case "$file" in
  *.ts|*.tsx|*.mts|*.cts)
    [ -f tsconfig.json ] || exit 0
    if [ -x node_modules/.bin/tsc ]; then run "tsc" node_modules/.bin/tsc --noEmit; fi
    exit 0 ;;

  *.js|*.jsx|*.mjs|*.cjs)
    [ -f package.json ] || exit 0
    if [ -x node_modules/.bin/eslint ]; then run "eslint" node_modules/.bin/eslint "$file"; fi
    exit 0 ;;

  *.py)
    if command -v ruff >/dev/null 2>&1; then run "ruff" ruff check "$file"; fi
    if [ -f pyproject.toml ] && command -v mypy >/dev/null 2>&1; then run "mypy" mypy "$file"; fi
    exit 0 ;;

  *.rs)
    [ -f Cargo.toml ] || exit 0
    command -v cargo >/dev/null 2>&1 || exit 0
    run "cargo check" cargo check --quiet ;;

  *.go)
    [ -f go.mod ] || exit 0
    command -v go >/dev/null 2>&1 || exit 0
    run "go vet" go vet ./... ;;

  *.cs)
    ls ./*.sln >/dev/null 2>&1 || ls ./*.csproj >/dev/null 2>&1 || exit 0
    command -v dotnet >/dev/null 2>&1 || exit 0
    run "dotnet build" dotnet build --nologo -v q ;;

  *) exit 0 ;;
esac
