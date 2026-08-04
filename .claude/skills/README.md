# Skills in this template

Claude Code discovers skills at `.claude/skills/<name>/SKILL.md` — **flat**, one
folder per skill. Nested category folders are not scanned, which is why the
imported skills below were flattened out of their upstream category tree.

## Origin

| Skill | Source |
|---|---|
| `frontend-design` | this template |
| everything else | [davidondrej/skills](https://github.com/davidondrej/skills) |

The imported skills are MIT-licensed, © 2026 David Ondrej — full text in
[`LICENSE-davidondrej-skills`](LICENSE-davidondrej-skills). Several were edited
for this template; see *Local edits* below.

## What was imported, and what was not

Imported: the subset that runs as-is on Windows + Claude Code with no external
account.

    agent-self-scheduling   before-building     brain-to-docs
    create-readonly-db-role decisions           effective-agent-skills
    folder-specific-claude-and-agents-md        git-worktree
    goal-loop               google-safe-browsing  handoff
    launch-subagent         level-up            next-decision
    prompt-me               read-all-adrs       remind
    research-prompt         save-idea           setup-help
    short                   teach

Deliberately skipped, and why:

- **macOS-only** — `cmux`, `anti-sleep` (`caffeinate`), `macbook-metrics-setup`,
  `nuke-cursor-app`, `cyber-audit`.
- **Needs a paid DeepAPI key** — `deepapi` (76KB, the largest file in the repo),
  `deep-research`, `online-shopping`, `youtube-transcript`.
- **Built for other agent runtimes** — `pi-web-search` ("ONLY for Pi Agents"),
  `pi-custom-model`, `herdr`, `codex-subagent`, `distribute-skill-to-all-agents`.
- **Hardcoded to the author's own infrastructure** — `read-prod-database` (his
  Supabase role, cites "ADR 0175"), `prod-push` (his CI + Vercel project),
  `push-skill-to-github` (his private repo at `~/.agents`),
  `fireflies-transcript` (his API key).
- **Upstream `hooks/`** — `deny-dangerous.sh` requires `jq` and **fails open when
  jq is absent**, which is the case in Git Bash here (see
  [`../hooks/README.md`](../hooks/README.md)). It also hardcodes
  `/opt/homebrew/bin`. This template's own Python guards cover the same ground
  and actually execute on Windows.

To pull in any skipped skill later, copy it out of the upstream repo into
`.claude/skills/<name>/` — dropping the category folder.

## Local edits

- **`launch-subagent`** — upstream mandates Cursor model names ("Fable 5 Max",
  "GPT 5.6 Sol Max Fast") and forbids Sonnet 5. Claude Code's Agent tool accepts
  only `sonnet`/`opus`/`haiku`/`fable`, so those rules were unfollowable.
  Rewritten to real values; also deduplicated a verbatim-repeated block and
  dropped a reference to the un-imported `deepapi` skill.
- **`folder-specific-claude-and-agents-md`** — dropped a hardcoded
  `~/Documents/code/workspace/` path and a link to a `library/` file that does
  not exist here. Recommends a one-line `AGENTS.md` over a symlink, since
  symlinks need Developer Mode on Windows and do not survive `git clone`.
- **`save-idea`** — removed an assumption that `VIDEO-IDEAS.md` continues the
  numbering of the author's private Google Doc; both files now start at 1 and are
  created on first use. Still writes to `~/content/`.

## Known rough edges

`goal-loop` and `agent-self-scheduling` each mention `cmux`, a macOS-only
terminal, in one passing section. Harmless, left as-is.
