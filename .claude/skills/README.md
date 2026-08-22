# Skills in this template

Claude Code discovers skills at `.claude/skills/<name>/SKILL.md` — **flat**, one
directory per skill. Nested category folders are not scanned, which is why the
imported skills below were flattened out of their upstream category tree.

## Origin

| Skill | Source |
|---|---|
| `frontend-design` | this template |
| everything else | [davidondrej/skills](https://github.com/davidondrej/skills), pinned in [`UPSTREAM.lock`](UPSTREAM.lock) |

Imported skills are MIT-licensed, © 2026 David Ondrej — full text in
[`LICENSE-davidondrej-skills`](LICENSE-davidondrej-skills). That copyright line
stays put: MIT permits modifying and redistributing the files, on the condition
that the notice travels with them. See [`../../NOTICE`](../../NOTICE) for the
split between template-authored and bundled work.

## Why the upstream is pinned

Vendored skills are a supply chain. Every model-invocable skill's description
is loaded into the prompt of every session, and its body is loaded whenever
Claude judges it relevant — so an upstream edit changes how your agent behaves,
silently, in every project that cloned this template.

[`UPSTREAM.lock`](UPSTREAM.lock) records the exact commit these came from and
the command to diff against it. Do not pull an update without reading the diff.
The bundled `config-auditor` subagent exists for exactly this review.

## Context cost, and what was done about it

A skill's description sits in context permanently once Claude can auto-invoke
it. Fifteen of these skills are things you invoke deliberately — `/short`,
`/remind`, `/handoff`, `/teach` — and they now carry
`disable-model-invocation: true`, which keeps them available as `/name` while
taking their descriptions out of the always-loaded listing.

Two skills had the flag upstream but descriptions that describe automatic
triggering (`before-building` — "fire the moment the user proposes a build";
`git-worktree` — "use when starting a task in a shared repo"). The flag
contradicted the description, so it was removed from those two.

Delete anything you will not use. Curation is the only real lever on this cost.

## Changes from upstream

- **Sanitized.** The snapshot is only partly de-personalised upstream; roughly
  twenty remaining references to the author by name were rewritten to "the user"
  so the skills read correctly for whoever clones this.
- **`launch-subagent`** — upstream mandates Cursor model names ("Fable 5 Max",
  "GPT 5.6 Sol Max Fast") and forbids Sonnet. Claude Code's Agent tool accepts
  only `sonnet` / `opus` / `haiku` / `fable`, so those rules are unfollowable.
  Rewritten to real values, with a verbatim-duplicated block removed.
- **`folder-specific-claude-and-agents-md`** — dropped a hardcoded
  `~/Documents/code/workspace/` path and a link to a file that does not exist
  here. Recommends a one-line `AGENTS.md` over a symlink, since symlinks need
  Developer Mode on Windows and do not survive `git clone`.
- **`research-prompt`, `agent-self-scheduling`, `create-readonly-db-role`** —
  removed dependencies on the upstream author's paid API and private
  infrastructure, so nothing here needs an account to work.

## Not imported, and why

- **macOS-only** — `cmux`, `anti-sleep`, `macbook-metrics-setup`,
  `nuke-cursor-app`.
- **Needs a paid key** — `deepapi`, `deep-research`, `risky-changes`,
  `online-shopping`, `youtube-transcript`, `fireflies-transcript`.
- **Other agent runtimes** — `pi-web-search`, `pi-custom-model`, `herdr`,
  `codex-subagent`, `bb-plugins`, `bb-subagents`, `corral-launch-agents`,
  `fable-review`, `gpt-review`, `total-review`.
- **The author's own infrastructure** — `read-prod-database`, `prod-push`,
  `push-skill-to-github`.
- **`save-idea`** — writes to `~/content/` for a video and podcast backlog.
  A personal content workflow, not a coding-template concern.
- **`global-agent-guardrails`** — good idea, superseded here. It maintains a
  shared regex denylist across agents; this template gets the same protection
  from `permissions.deny`, which Claude Code enforces natively and which cannot
  fail open when an interpreter is missing.
- **Upstream `hooks/`** — `deny-dangerous.sh` requires `jq` and **fails open
  when jq is absent**, which is the case in Git Bash. It also hardcodes
  `/opt/homebrew/bin`. See [`../hooks/README.md`](../hooks/README.md).

To pull in a skipped skill, copy it out of the pinned upstream into
`.claude/skills/<name>/`, dropping the category directory.
