#!/usr/bin/env python3
"""Warn when a Bash command changes directory relatively.

The Bash tool's working directory persists between calls, so `cd <relative>`
means "wherever the last command happened to leave me" rather than "the repo
root". Two failure modes follow, both of which have actually happened here:

  * the `cd` fails because the shell is already inside that directory, and the
    `&&` chain silently skips everything after it — while a later command in
    the same block still runs and prints reassuring output;
  * a multi-file script uses repo-relative paths from the wrong place, dies
    part-way, and leaves the remaining files silently unedited.

This does not block anything. It prints a reminder, because the fix is one
character: make the path absolute.
"""

import json
import re
import sys

# `cd` to something that is not absolute, not $HOME, not a variable and not a
# bare `cd` (which goes home and is unambiguous).
RELATIVE_CD = re.compile(r"(?:^|[;&|]\s*|\&\&\s*)cd\s+(?!/|~|\$|-)(\S+)")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    targets = RELATIVE_CD.findall(command)
    if not targets:
        return 0

    shown = ", ".join(sorted(set(targets))[:3])
    print(
        f"Relative `cd {shown}` — the Bash working directory persists between "
        f"calls, so this depends on where the previous command left off. If it "
        f"fails, everything after `&&` is skipped without an error you will "
        f"notice. Prefer an absolute path.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
