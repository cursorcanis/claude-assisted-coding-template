---
paths:
  - "**/*.sh"
  - "**/*.ps1"
  - "**/*.bat"
  - "**/*.cmd"
  - "**/Makefile"
---

# Shell scripts in this repo

This template is developed on Windows and expected to run on macOS and Linux
too, so scripts carry a portability cost that is easy to forget.

- `set -euo pipefail` at the top of every bash script, and quote every
  expansion. An unquoted path breaks the first time it contains a space,
  which on Windows is immediately.
- Do not assume an interpreter name. `python` exists in Git Bash, `python3` on
  most Linux images, and sometimes only the `py` launcher. Resolve it, or
  fail with a message that says what was missing.
- Do not assume a tool exists. `jq` in particular is absent from Git Bash,
  which is why the hooks here parse JSON with Python.
- Scripts under `.claude/hooks/` must keep LF endings; CRLF breaks the
  shebang. `.gitattributes` enforces this — do not override it.
- A hook that cannot do its job exits 0 and says so. A hook that exits
  non-zero by accident blocks the user's work.
