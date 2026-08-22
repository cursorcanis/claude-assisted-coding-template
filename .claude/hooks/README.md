# Hooks

Hooks run whatever Claude decides, so they are the enforcement layer. This
directory holds three, wired in [`../settings.json`](../settings.json).

| Event | Matcher | Script | Effect |
|---|---|---|---|
| `SessionStart` | `startup\|resume` | `session_context.sh` | Injects branch, dirty-file count and detected stack |
| `PreToolUse` | `Bash\|PowerShell` | `guard_commands.sh` → `.py` | Denies credential reads/copies/uploads; asks before destructive commands |
| `PostToolUse` | `Write\|Edit` | `verify.sh` | Runs the project's own type/lint check; async, silent unless it fails |

## What changed in v2, and why

**The credential guard is no longer a hook.** It is
`permissions.deny` in `settings.json`. Claude Code enforces those rules
natively — including against `cat`, `head`, `tail` and `sed` inside Bash — with
no Python in the loop. The previous version reimplemented this in a regex and
missed `cp`, `grep`, `awk`, `printenv`, `scp`, `.env.staging`, and
`~/.ssh/id_ed25519`, all of which are now closed.

`guard_writes.py` is gone entirely: `Edit(...)` deny rules replace it and cover
strictly more.

**The guard that remains covers only what rules cannot express.** A deny rule
is all-or-nothing, so `Read(.env.*)` would also block `.env.example`. And a
read-oriented rule never sees `cp .env /tmp/x` or `curl -d @.env`, which move
the secret without printing it. Those two gaps are the whole remaining job.

**The verifier is no longer TypeScript-only.** `verify.sh` detects the stack
from marker files (`tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
`*.sln`) and runs the matching check. A repo with none of them stays silent.

**The interpreter is resolved, not assumed.** The old hooks invoked `python`.
Where only `python3` exists the hook errored and the command proceeded
unguarded — the identical fail-open trap that made the upstream `jq` hooks
useless in Git Bash. `guard_commands.sh` tries `python3`, `python`, then `py -3`,
and if none exists says so on the transcript rather than failing silently. That
degradation is acceptable now precisely because the permission rules, not this
script, are the floor.

## Honest limits

The guard is a regex over a command string. It raises the cost of a mistake; it
is not a boundary. It does not stop:

```bash
python -c "print(open('.env').read())"   # subprocess opens the file itself
```

`permissions.deny` does not stop that either — the docs are explicit that file
rules do not reach arbitrary subprocesses. For an actual boundary, enable
[the sandbox](https://code.claude.com/docs/en/sandboxing), which enforces at
the kernel.

Write guards accordingly: prefer `ask` over `deny` wherever a command has a
legitimate use. A guard that fires constantly trains you to approve without
reading, which is worse than no guard.

## Editing the rules

Patterns live in `DENY` / `ASK` in `guard_commands.py`. Path rules live in
`permissions` in `settings.json` — prefer adding there, since it needs no
interpreter and is enforced natively.

Both `.claude/settings.json` and `.claude/hooks/**` are in `permissions.ask`,
so Claude prompts before changing its own constraints. That is deliberate; the
previous version let an agent silently disable its own guards.

After any change, run the regression suite:

```bash
python3 .claude/hooks/tests/test_guard.py
```

Or spot-check by hand:

```bash
echo '{"tool_input":{"command":"cat .env"}}'    | bash guard_commands.sh   # deny
echo '{"tool_input":{"command":"cp .env /tmp"}}' | bash guard_commands.sh  # deny
echo '{"tool_input":{"command":"cat .env.example"}}' | bash guard_commands.sh  # empty
```

Empty output means no opinion, and the command proceeds under normal
permission rules.

## Plugin mode

`hooks.json` is the same wiring with `${CLAUDE_PLUGIN_ROOT}` in place of
`${CLAUDE_PROJECT_DIR}`, used when this repo is installed as a plugin rather
than cloned. Enable one path or the other — with both active the hooks run
twice, since plugin hooks are not deduplicated against settings hooks.

## Notes for Windows

- **No `jq`.** Git Bash ships without it, which is why these parse JSON with
  Python.
- **Hooks run in Git Bash**, not PowerShell. Paths arrive Windows-style
  (`c:/...`); the guard normalises separators before matching.
- **Config changes need a reload.** Open `/hooks` once, or restart the session.

Authoritative reference: `/hooks` in-session, or
<https://code.claude.com/docs/en/hooks>.
