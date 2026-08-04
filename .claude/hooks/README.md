# Claude Code hooks in this repo

What is wired, why, and how to change it.

## What is active

| Event | Matcher | Script | Effect |
|---|---|---|---|
| PreToolUse | `Bash\|PowerShell` | `guard_commands.py` | Denies secret-leaking / history-rewriting commands; asks before destructive ones |
| PreToolUse | `Write\|Edit` | `guard_writes.py` | Denies edits to credential files |
| PostToolUse | `Write\|Edit` | `verify_ts.sh` | `tsc --noEmit` after a `.ts/.tsx` edit (async; speaks only on failure) |

All three live in **`.claude/settings.json`** (committed). They are portable: the
guards only inspect strings, and the verifier resolves the project root from its
own location rather than hardcoding a path.

**`.claude/settings.local.json`** (gitignore this) holds only machine and
account preferences — model, permission mode, allowlist. No hooks.

## Why these particular rules

Generic hook advice ("block `rm -rf`, lint on save") is mostly noise. These
target what this repo can actually lose:

- **Dotenv files and key material → `deny` on read-to-stdout and on write.**
  Printing one into a transcript leaks it, and transcripts are long-lived.
  `.env.example` is deliberately *not* protected — keeping it current is normal
  work.
- **Force-push → `deny`.** Rewrites published history. Revert instead.
- **`git reset --hard`, `git clean -f`, recursive `rm` → `ask`.** All have
  legitimate uses, so they prompt rather than block.
- **`tsc` after edits.** `asyncRewake`, so it never blocks an edit and stays
  silent while the code compiles — it interrupts only when something broke.

`verify_ts.sh` no-ops until the project actually has a `tsconfig.json` and a
local `typescript` install. Until then it is silent by design, not broken.

## Editing the rules

Patterns live in the `DENY` / `ASK` lists in `guard_commands.py` and `PROTECTED`
in `guard_writes.py`. After any change, re-run the pipe tests:

```bash
echo '{"tool_input":{"command":"cat .env.local"}}' | python .claude/hooks/guard_commands.py
echo '{"tool_input":{"file_path":"src/.env"}}'     | python .claude/hooks/guard_writes.py
```

Empty output = no opinion (command proceeds under normal permission rules).
Otherwise it prints a `permissionDecision` of `deny` or `ask`.

A guard that is too aggressive is worse than none — it trains you to approve
without reading. Prefer `ask` over `deny` whenever a command has any legitimate
use in this project.

## Notes for this machine

- **No `jq`.** Git Bash here ships without it, so the jq one-liners in most hook
  documentation silently produce nothing. These hooks parse stdin with `python`
  (3.12, on PATH) instead.
- **Hooks run in Git Bash**, not PowerShell. Paths arrive Windows-style
  (`c:/...`).
- **Config changes need a reload.** The settings watcher only tracks directories
  that had a settings file at session start. If a hook edit seems inert, open
  `/hooks` once or restart the session.

Authoritative reference: `/hooks` in-session, or the hook schema in Claude Code's
settings documentation.
