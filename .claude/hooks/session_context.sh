#!/bin/bash
# SessionStart: put the few facts Claude would otherwise burn tool calls
# discovering straight into context -- branch, working-tree state, and which
# stack markers exist.
#
# Cheap by design: no network, no installs, one git call. stdout on
# SessionStart is delivered to Claude, so this is additive context, not output
# the user has to read.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
command -v git >/dev/null 2>&1 || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
upstream=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null || echo "none")

stacks=""
[ -f package.json ]   && stacks="$stacks node"
[ -f tsconfig.json ]  && stacks="$stacks typescript"
[ -f pyproject.toml ] || [ -f requirements.txt ] && stacks="$stacks python"
[ -f Cargo.toml ]     && stacks="$stacks rust"
[ -f go.mod ]         && stacks="$stacks go"
ls ./*.sln >/dev/null 2>&1 && stacks="$stacks dotnet"
[ -n "$stacks" ] || stacks=" none detected"

echo "Repo state: branch '${branch}' | ${dirty} uncommitted file(s) | upstream: ${upstream}"
echo "Stack markers:${stacks}"
exit 0
