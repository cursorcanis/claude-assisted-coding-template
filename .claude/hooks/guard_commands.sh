#!/bin/bash
# Launcher for guard_commands.py.
#
# Why a launcher: the interpreter is called `python3` on most Linux/macOS,
# `python` in Git Bash on Windows, and sometimes only `py -3` exists. Calling
# one name directly meant the hook silently no-opped wherever that name was
# missing -- the same fail-open trap as the `jq` hooks this replaced.
#
# If no interpreter is found we say so on the transcript and exit 0. That is
# deliberate: since v2 the real credential floor is the `permissions.deny`
# block in settings.json, which Claude Code enforces natively with no
# interpreter involved. This guard only adds the long tail on top, so losing
# it degrades coverage without opening the front door.
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
py=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then py="$cand"; break; fi
done
if [ -z "$py" ] && command -v py >/dev/null 2>&1; then py="py -3"; fi

if [ -z "$py" ]; then
  printf '%s\n' '{"systemMessage":"[guard] No Python interpreter found; the supplementary command guard is inactive. permissions.deny in .claude/settings.json is still enforced."}'
  exit 0
fi

exec $py "$here/guard_commands.py"
