#!/bin/bash
# PostToolUse: type-check the project after a .ts/.tsx edit.
#
# Async + asyncRewake: never blocks an edit, silent on success, wakes the model
# only when tsc actually fails.
#
# Runs natively on Windows via Git Bash -- this project is plain Node/TypeScript
# with no WSL-only native binaries. If that ever changes, this is the one place
# that needs to know.
set -uo pipefail

payload=$(cat)
file=$(printf '%s' "$payload" | python -c \
  "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    print(''); raise SystemExit
ti=d.get('tool_input') or {}
tr=d.get('tool_response') or {}
print(tr.get('filePath') or ti.get('file_path') or '')" 2>/dev/null)

case "$file" in
  *.ts|*.tsx) ;;
  *) exit 0 ;;
esac

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)

# Stay silent until the project actually has TypeScript wired up. Without these
# guards the hook fires on every edit in a fresh repo and reports a missing-tsc
# failure that has nothing to do with the code.
[ -f "$root/tsconfig.json" ] || exit 0
[ -x "$root/node_modules/.bin/tsc" ] || [ -f "$root/node_modules/typescript/bin/tsc" ] || exit 0

out=$(cd "$root" && ./node_modules/.bin/tsc --noEmit 2>&1)
status=$?

if [ $status -ne 0 ]; then
  echo "tsc FAILED after editing $(basename "$file"):"
  printf '%s\n' "$out" | head -25
  exit 2
fi
exit 0
