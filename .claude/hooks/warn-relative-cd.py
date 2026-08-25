#!/usr/bin/env python3
"""Warn about Bash commands whose meaning depends on the working directory.

The Bash tool's working directory persists between calls, so `cd <relative>`
means "wherever the last command happened to leave me" rather than "the repo
root". Two failure modes follow, both of which have actually happened here:

  * the `cd` fails because the shell is already inside that directory, and the
    `&&` chain silently skips everything after it — while a later command in
    the same block still runs and prints reassuring output;
  * a multi-file script uses repo-relative paths from the wrong place, dies
    part-way, and leaves the remaining files silently unedited.

A third variant, added 2026-08-26 after it bit twice in one session: an
**absolute** `cd` that succeeds is not safe either, because it persists. The
next, separate tool call then uses a repo-relative path — `scripts/…`,
`some-comparison/README.md` — which now resolves inside whatever directory the
previous call left the shell in. Once that silently skipped half of a two-file
edit and left a document's two language versions out of sync. So this hook also
warns when a command references a top-level entry of the project directory
without a leading slash and does not itself `cd` somewhere absolute first.

This does not block anything. It prints a reminder, because the fix is one
character: make the path absolute.
"""

import json
import os
import re
import sys

# `cd` to something that is not absolute, not $HOME, not a variable and not a
# bare `cd` (which goes home and is unambiguous).
RELATIVE_CD = re.compile(r"(?:^|[;&|]\s*|\&\&\s*)cd\s+(?!/|~|\$|-)(\S+)")


def repo_relative_paths(command: str) -> list[str]:
    """Repo-relative uses of a top-level project entry, e.g. `scripts/foo.py`.

    The entries are read from the project directory rather than hard-coded, so
    a new comparison directory is covered the day it is created.
    """
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    if not root or not os.path.isdir(root):
        return []
    # An absolute `cd` at the start makes the rest of THIS command well-defined.
    if re.match(r"\s*cd\s+(/|~|\$)", command):
        return []
    try:
        entries = [e for e in os.listdir(root) if not e.startswith(".")]
    except OSError:
        return []
    hits = []
    for entry in entries:
        if re.search(rf"(?<![\w./-]){re.escape(entry)}/", command):
            hits.append(entry + "/")
    return hits


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")

    targets = RELATIVE_CD.findall(command)
    if targets:
        shown = ", ".join(sorted(set(targets))[:3])
        print(
            f"Relative `cd {shown}` — the Bash working directory persists "
            f"between calls, so this depends on where the previous command left "
            f"off. If it fails, everything after `&&` is skipped without an "
            f"error you will notice. Prefer an absolute path.",
            file=sys.stderr,
        )
        return 0

    relative = repo_relative_paths(command)
    if relative:
        shown = ", ".join(sorted(set(relative))[:3])
        print(
            f"Repo-relative path ({shown}) with no absolute `cd` in this "
            f"command — the working directory persists between calls, so this "
            f"resolves wherever the previous command left the shell, not at the "
            f"repo root. A multi-file script that misses this way dies part-way "
            f"and leaves the rest silently unedited. Prefer an absolute path.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
