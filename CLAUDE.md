# Project conventions

<!-- Template note for humans: replace the Commands and Stack sections with
     this project's real values on day one. Everything under Working
     agreement and Guardrails is stack-independent and worth keeping. -->

## Commands

<!-- Fill these in. Claude reads them instead of guessing or running `ls`. -->
- Build: `TODO`
- Test: `TODO`
- Lint: `TODO`
- Run one test: `TODO`

## Stack

- `TODO` — language, framework, version constraints that actually bind

## Working agreement

- Prefer editing an existing file over creating a new one.
- Match the conventions already in the file you are editing; the surrounding
  code outranks any general style preference.
- When a change spans more than about three files, say what you are going to
  do before doing it.
- Do not add dependencies without saying which problem the dependency solves
  and what the alternative was.
- Tests live next to the code they cover unless this project already does it
  another way.

## Guardrails

- Never read or write `.env` or credential files. `.claude/settings.json`
  blocks this at the tool level; if a value is needed, ask for it.
- Never force-push, and never rewrite published history. Revert instead.
- `.env.example` is the one dotenv file that is safe to read and expected to
  stay current.
- Destructive git operations (`reset --hard`, `clean -f`, `rebase`) prompt
  before running. That prompt is not a formality.

## Where things live

- `.claude/rules/` — instructions scoped to particular file types; they load
  only when Claude touches a matching file.
- `.claude/skills/` — procedures invoked with `/name`, or loaded by Claude
  when relevant. Long reference material belongs here, not in this file.
- `.claude/agents/` — subagents with their own context window.
- `.claude/hooks/` — what runs automatically, regardless of what Claude decides.

Keep this file under 200 lines. If a section grows into a procedure, move it
to a skill; if it only matters for one part of the tree, move it to a rule.
