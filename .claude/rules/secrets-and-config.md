---
paths:
  - "**/.env.example"
  - "**/*.config.{js,ts,json,yaml,yml}"
  - "**/docker-compose*.{yml,yaml}"
  - "**/Dockerfile*"
  - "**/*.tf"
---

# Configuration and secret handling

Loaded only when Claude opens a config file, so it costs nothing the rest of
the time.

- A secret never gets a literal value in a committed file. Reference it:
  `${DATABASE_URL}`, not the URL.
- When you add a variable anywhere, add it to `.env.example` in the same
  change, with a placeholder and a one-line comment on what it is.
- Config files that ship to production and config files used locally are
  different files. Do not make a local convenience change to the former.
- Default to the least privilege that works: read-only credentials, scoped
  tokens, single-purpose service accounts.
- If a real credential is found committed anywhere in this repo, stop and say
  so. Rotating it is the user's job; pointing it out is yours.
