#!/usr/bin/env python3
"""PreToolUse guard for Write / Edit.

Stops edits to files that hold live credentials. These are gitignored and
machine-local: rewriting one silently breaks a running stack, and the value
that was overwritten is usually not recoverable from anywhere else.

Contract: exit 0 and print JSON. Printing nothing = no opinion.
"""
import json
import re
import sys

PROTECTED = [
    # .env.example is deliberately excluded - it holds placeholders, and
    # keeping it current is a normal part of the work.
    (r"\.env(\.local|\.development|\.production|\.test)?$",
     "Holds live credentials. Edit it by hand, or write .env.example instead."),
    (r"\.(pem|p12|pfx|key)$",
     "Private key material."),
    (r"[\\/](id_rsa|credentials\.json|service-account.*\.json)$",
     "Credential file."),
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not isinstance(path, str) or not path:
        return 0

    normalized = path.replace("\\", "/")
    for pattern, reason in PROTECTED:
        if re.search(pattern, normalized, re.IGNORECASE):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"[guard] {reason}",
                }
            }))
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
