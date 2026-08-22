#!/usr/bin/env python3
"""PreToolUse guard for Bash / PowerShell -- the layer above permissions.deny.

WHAT THIS IS NOT
    This is not the credential boundary. `permissions.deny` in
    .claude/settings.json is, and Claude Code enforces it natively: it covers
    the file tools *and* the file-reading commands it recognises in Bash
    (cat, head, tail, sed, ...), with no interpreter in the loop.

WHAT THIS ADDS
    Two things permission rules cannot express:

    1. The dotenv long tail. A deny rule is all-or-nothing -- `Read(.env.*)`
       would also block `.env.example`, which is read constantly during setup
       and holds only placeholders. Rules therefore enumerate the live
       variants; this catches any *other* `.env.<something>` while still
       letting the placeholder files through.

    2. Copy and upload shapes. `permissions.deny` blocks *reading* a secret.
       It does not stop `cp .env /tmp/x`, `curl -d @.env ...`, or `scp`, which
       move the file without ever printing it. Those are matched here.

    Neither layer stops a subprocess that opens the file itself
    (`python -c "print(open('.env').read())"`). Nothing short of
    `sandbox.enabled` does. See .claude/hooks/README.md.

Contract: exit 0 and print JSON. Printing nothing = no opinion.
"""
import json
import re
import sys

# Dangerous verbs only count at a command position -- start of string, or after
# a separator. Without this, prose that merely *mentions* a command matches: a
# commit message listing "git push --force" as a blocked pattern was itself
# blocked, which is how this anchor came to exist.
CMD_START = r"(?:^|[\n;&|]|\$\(|`)\s*(?:sudo\s+)?"

# Files whose contents are credentials. `.env.example`, `.env.sample` and
# `.env.template` are excluded by the lookahead -- placeholders, read often.
SECRET_FILE = (
    r"(?:\.env(?!\.(?:example|sample|template)\b)(?:\.[\w.-]+)?"
    r"|[\w./\\-]*\.(?:pem|p12|pfx|key)"
    r"|id_rsa|id_ed25519|credentials\.json|service-account[\w-]*\.json"
    r"|\.aws/credentials|\.ssh/[\w.-]+)"
)

DENY = [
    (CMD_START + r"rm\s+-[rRfd]*[rf][rRfd]*\s+(/|~|\$HOME|/mnt/[a-z]/?\s*$)",
     "Recursive delete of a filesystem root or home directory."),

    # Read-to-stdout. permissions.deny already covers the tools Claude Code
    # parses; this catches the readers it does not (awk, grep, xxd, od, ...).
    (r"(?:^|[\n;&|]|\$\(|`)\s*(?:cat|type|less|more|head|tail|strings|awk|grep|"
     r"sed|xxd|od|base64|nl|tac|rev)\b[^|;\n]*" + SECRET_FILE,
     "That file holds credentials. Read .env.example instead, or ask the user for the value."),

    # Copy / move / upload -- moves the secret without printing it, so a
    # read-oriented deny rule never sees it.
    (r"(?:^|[\n;&|]|\$\(|`)\s*(?:cp|mv|rsync|scp|install|tee)\b[^|;\n]*" + SECRET_FILE,
     "Copying a credential file moves the secret somewhere unprotected."),
    (r"(?:curl|wget|http|https|nc|ncat|socat)\b[^|;\n]*" + SECRET_FILE,
     "That looks like uploading a credential file."),
    (r"@" + SECRET_FILE,
     "Passing a credential file as a request body (`@file`) uploads it."),

    # Environment-variable secrets.
    (r"(?:^|[\n;&|]|\$\(|`)\s*(?:echo|printf|printenv|env)\b[^|;\n]*"
     r"\$?\{?[A-Z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)",
     "Prints a secret into the transcript."),

    # Piping the network straight into a shell.
    (r"(?:curl|wget)\b[^|;\n]*\|\s*(?:sudo\s+)?(?:ba|z|k|)sh\b",
     "Piping a download into a shell runs unreviewed remote code."),
]

ASK = [
    (r"(?:^|[\n;&|]|\$\(|`)\s*env\s*(?:\||$)",
     "Dumps the whole environment, which may include secrets."),
    (CMD_START + r"git\s+(reset\s+--hard|clean\s+-[a-z]*f)",
     "Discards uncommitted work irreversibly."),
    (CMD_START + r"rm\s+-[rRfd]*[rf]",
     "Recursive delete."),
    (CMD_START + r"find\b[^|;\n]*\s-(delete|exec\b)",
     "`find -delete` / `-exec` can remove or run over many files at once."),
    (CMD_START + r"git\s+push\b[^|;\n]*--force-with-lease",
     "Still rewrites remote history, just more safely. Confirm the branch."),
]


def decide(command):
    # On Windows, paths reach the hook with backslashes (`.ssh\id_rsa`). Match
    # against both forms so one separator style cannot walk past the patterns.
    variants = [command]
    if "\\" in command:
        variants.append(command.replace("\\", "/"))

    for pattern, reason in DENY:
        if any(re.search(pattern, v, re.IGNORECASE) for v in variants):
            return "deny", reason
    for pattern, reason in ASK:
        if any(re.search(pattern, v, re.IGNORECASE) for v in variants):
            return "ask", reason
    return None, None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = data.get("tool_input") or {}
    command = tool_input.get("command") or ""
    if not isinstance(command, str) or not command.strip():
        return 0

    decision, reason = decide(command)
    if decision is None:
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": f"[guard] {reason}",
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
