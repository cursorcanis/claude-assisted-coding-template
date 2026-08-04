#!/usr/bin/env python3
"""PreToolUse guard for Bash / PowerShell commands.

Reads the hook payload on stdin and answers with a permission decision.
Written in Python because `jq` is not installed in this machine's Git Bash,
so the usual jq one-liners would silently no-op.

Decisions:
  deny  - no legitimate use in this repo; the command is almost certainly a
          mistake or would leak a secret.
  ask   - destructive, but has real uses here; surface it for confirmation
          instead of blocking real work.
  allow - stay silent. Returning no decision lets normal permission rules
          apply, which is what we want for everything else.

Contract: exit 0 and print JSON. Printing nothing = no opinion.
"""
import json
import re
import sys


def _payload():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


# Dangerous verbs only count at a command position — start of the string, or
# after a separator. Without this, prose that merely *mentions* a command
# matches: a commit message listing "git push --force" as a blocked pattern was
# itself blocked, which is how this anchor came to exist. Heredoc body lines
# start with their own text, so they no longer trip the verb patterns.
CMD_START = r"(?:^|[\n;&|]|\$\(|`)\s*(?:sudo\s+)?"

# (regex, reason). Matched case-insensitively against the command string.
DENY = [
    (CMD_START + r"rm\s+-[rRfd]*[rf][rRfd]*\s+(/|~|\$HOME|/mnt/c/?\s*$)",
     "Recursive delete of a filesystem root or home directory."),
    (CMD_START + r"git\s+push\b[^|;\n]*(--force\b|(?<!-)-f\b)(?![-\w])",
     "Force-push rewrites published history. Push a normal commit, or revert."),
    # Dotenv files and key material hold live credentials. Printing one into
    # the transcript leaks it, and transcripts are long-lived. The lookahead
    # spares .env.example / .sample / .template, which hold only placeholders
    # and are read constantly during setup.
    (r"(cat|type|less|more|head|tail|strings)\s+[^|;]*"
     r"(\.env(?!\.(example|sample|template))(\.[\w.]+)?\b|\.pem\b|\.p12\b|id_rsa\b|credentials\.json\b)",
     "That file holds credentials. Read .env.example instead, or ask the user for the value."),
    (r"echo\s+[^|;]*\$\{?(ANTHROPIC_API_KEY|OPENAI_API_KEY|[A-Z0-9_]*(API_KEY|SECRET|TOKEN|PASSWORD))",
     "Prints a secret into the transcript."),
]

ASK = [
    (CMD_START + r"git\s+(reset\s+--hard|clean\s+-[a-z]*f)",
     "Discards uncommitted work irreversibly."),
    (CMD_START + r"rm\s+-[rRfd]*[rf]",
     "Recursive delete."),
]


def decide(command: str):
    for pattern, reason in DENY:
        if re.search(pattern, command, re.IGNORECASE):
            return "deny", reason
    for pattern, reason in ASK:
        if re.search(pattern, command, re.IGNORECASE):
            return "ask", reason
    return None, None


def main() -> int:
    data = _payload()
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
