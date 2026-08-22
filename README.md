# claude-assisted-coding-template

A starting point for Claude Code projects: guardrails that are enforced rather
than suggested, a memory layer, a few subagents, and a curated skill set.

Two ways to use it.

**As a template** — clone it, `rm -rf .git`, start your project inside it. You
get `.claude/` fully wired plus a `CLAUDE.md` to fill in.

**As a plugin** — install it into a repo you already have, and the skills,
subagents and hooks come along without copying files:

```
/plugin marketplace add cursorcanis/claude-assisted-coding-template
/plugin install claude-assisted-coding-template@cursorcanis-tools
```

## Layout

```
CLAUDE.md                  Project instructions, loaded every session
.mcp.json.example          MCP servers; copy to .mcp.json to enable
.worktreeinclude           Gitignored files copied into new worktrees
.claude/
  settings.json            Permissions and hook wiring
  rules/                   Instructions scoped to file paths, loaded on demand
  agents/                  Subagents with their own context window
  hooks/                   What runs automatically
  skills/                  Procedures invoked with /name
.claude-plugin/            Manifests for plugin-mode install
```

## What enforces what

The distinction that matters: **`CLAUDE.md` and rules are context, hooks and
permissions are enforcement.** Claude reads the first two and usually complies.
It cannot get past the last two, because they are applied by Claude Code
before the tool runs.

| Layer | Where | Enforced by | Survives a confused model |
|---|---|---|---|
| Conventions | `CLAUDE.md`, `.claude/rules/` | nothing | no |
| Permission rules | `.claude/settings.json` | Claude Code | yes |
| Hooks | `.claude/hooks/` | Claude Code | yes |
| OS sandbox | `sandbox.enabled` | the kernel | yes |

Put anything that must not happen in the bottom half of that table.

### Credentials

`permissions.deny` blocks the file tools from touching `.env`, key material,
`~/.ssh` and friends, and Claude Code applies the same rules to the file
commands it recognises in Bash — `cat`, `head`, `tail`, `sed`. That is the
floor, and it holds with no interpreter in the loop.

`.claude/hooks/guard_commands.py` adds the two things a permission rule cannot
express: the `.env.<variant>` long tail, which a deny rule cannot match without
also blocking `.env.example`; and the copy-and-upload shapes — `cp`, `scp`,
`curl -d @file` — that move a secret without ever reading it.

Neither layer stops a subprocess that opens the file itself:

```
python -c "print(open('.env').read())"
```

Only [`sandbox.enabled`](https://code.claude.com/docs/en/sandboxing) stops that,
because only the kernel is below the subprocess. Turn it on for real isolation.
Everything here is a seatbelt against a confused agent, not a cage around a
hostile one.

## Day one

1. Fill in the Commands and Stack sections of `CLAUDE.md`. Or run `/init` and
   let Claude draft them from the code, then trim.
2. Delete the rules in `.claude/rules/` that do not apply, and add ones that do.
3. Run `/doctor` to check the hooks fire and nothing is misconfigured.
4. Skim `.claude/skills/README.md` and delete the skills you will not use —
   every model-invocable skill's description sits in context permanently.

## Verifying it works

```bash
python3 .claude/hooks/tests/test_guard.py
```

34 cases, each one either a bypass found in a real audit of the previous
version or a false positive an earlier pattern caused. Add a case before you
add a pattern.

## Provenance

Most skills are vendored from a third party at a pinned commit — see
[`.claude/skills/README.md`](.claude/skills/README.md). Vendored instructions
are a supply chain: they are read into the prompt of every session. Diff before
you update, and use the bundled `config-auditor` subagent when adopting
someone else's skills or plugin.

## Licence

MIT — see [LICENSE](LICENSE) and [NOTICE](NOTICE) for the split between
template-authored and bundled work.
