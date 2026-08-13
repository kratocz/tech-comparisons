#!/usr/bin/env python3
"""Check comparison documents against the conventions in AGENTS.md.

Usage:
    scripts/check-comparison.py              # every comparison directory
    scripts/check-comparison.py zfs-vs-ceph  # only these

Exits 1 if any ERROR is reported. WARNs never fail the run — they flag things
that are legal but usually worth a look (open [OVĚŘIT]/[VERIFY] tags, a
comparison with no Czech original).

These are the checks that actually caught mistakes while writing
storage-replication: a table column inserted at the wrong index, a TL;DR item
numbered out of order, a §N reference to a section that did not exist, and a
bulk edit that would have mangled URLs.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

errors: list[str] = []
warns: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"ERROR {where}: {msg}")


def warn(where: str, msg: str) -> None:
    warns.append(f"WARN  {where}: {msg}")


def table_blocks(lines: list[str]):
    """Yield (start_line_no, [row, ...]) for each contiguous run of table rows."""
    block: list[str] = []
    start = 0
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("|"):
            if not block:
                start = i
            block.append(line)
        elif block:
            yield start, block
            block = []
    if block:
        yield start, block


def check_tables(rel: str, lines: list[str]) -> None:
    for start, block in table_blocks(lines):
        if len(block) < 2:
            continue
        widths: dict[int, list[int]] = {}
        for offset, row in enumerate(block):
            widths.setdefault(row.count("|"), []).append(start + offset)
        if len(widths) > 1:
            detail = "; ".join(
                f"{n} pipes on line(s) {', '.join(map(str, ls[:4]))}"
                for n, ls in sorted(widths.items())
            )
            err(f"{rel}:{start}", f"table rows disagree on cell count — {detail}")


def check_section_refs(rel: str, text: str) -> None:
    """Every §N must resolve to a '## N.' heading in this file.

    Cross-document references carry a relative link (`[zfs-vs-ceph §15](../…)`),
    so strip those before scanning.
    """
    local = re.sub(r"\[[^\]]*\]\((?:\.\./|\./)[^)]*\)", "", text)
    sections = {int(m.group(1)) for m in re.finditer(r"^## (\d+)\.", local, re.M)}
    refs = {int(m.group(1)) for m in re.finditer(r"§(\d+)", local)}
    for missing in sorted(refs - sections):
        err(rel, f"§{missing} referenced but no '## {missing}.' section exists")

    # Consecutive, no gaps or repeats. A draft may open with a `## 0.` status
    # section, so the run is allowed to start at 0 as well as 1.
    numbers = [int(m.group(1)) for m in re.finditer(r"^## (\d+)\.", text, re.M)]
    if numbers:
        first = numbers[0]
        if first not in (0, 1):
            err(rel, f"numbered sections start at {first}, expected 0 or 1")
        elif numbers != list(range(first, first + len(numbers))):
            err(rel, f"section numbers are not consecutive from {first}: {numbers}")


def check_ordered_lists(rel: str, lines: list[str]) -> None:
    """Top-level ordered lists must count up without gaps or repeats."""
    run: list[tuple[int, int]] = []

    def flush() -> None:
        if len(run) < 2:
            return
        got = [n for n, _ in run]
        if got != sorted(got) or len(set(got)) != len(got):
            err(f"{rel}:{run[0][1]}", f"ordered list numbered {got}")

    for i, line in enumerate(lines, 1):
        m = re.match(r"^(\d+)\. ", line)
        if m:
            run.append((int(m.group(1)), i))
        elif not line.strip():
            continue
        elif not line.startswith((" ", "\t")):
            flush()
            run = []
    flush()


def check_links(rel: str, path: str, text: str) -> None:
    base = os.path.dirname(path)
    for m in re.finditer(r"\]\(((?:\.\./|\./)[^)#\s]+)", text):
        target = os.path.normpath(os.path.join(base, m.group(1)))
        if not os.path.exists(target):
            err(rel, f"relative link does not resolve: {m.group(1)}")
    for url in re.findall(r"https?://\S*?[)\s]", text):
        if " / " in url:
            err(rel, f"URL contains ' / ' — probably mangled by a bulk edit: {url}")


def check_header(rel: str, lines: list[str]) -> None:
    head = lines[:12]
    if not any(l.startswith("- **") for l in head):
        err(rel, "header metadata is not a bullet list (CommonMark merges plain lines)")
    tags = len(re.findall(r"\[OVĚŘIT\]|\[VERIFY\]", "\n".join(lines[12:])))
    if tags:
        warn(rel, f"{tags} open [OVĚŘIT]/[VERIFY] tag(s) in the body — the header must name them")


def check_czech_quotes(rel: str, text: str) -> None:
    lo, hi = text.count("„"), text.count("“")
    if lo != hi:
        err(rel, f"Czech quotes unbalanced: {lo}× „ vs {hi}× “ (ASCII \" used to close?)")


def check_parity(directory: str, en: str, cs: str) -> None:
    def shape(path: str) -> tuple[int, int]:
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        rows = sum(len(b) for _, b in table_blocks(lines))
        return len(re.findall(r"^## ", text, re.M)), rows

    en_sec, en_rows = shape(en)
    cs_sec, cs_rows = shape(cs)
    if en_sec != cs_sec:
        err(directory, f"language versions disagree on section count: EN {en_sec}, CS {cs_sec}")
    if en_rows != cs_rows:
        err(directory, f"language versions disagree on table row count: EN {en_rows}, CS {cs_rows}")


def check_index_row(directory: str) -> None:
    index = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    if f"]({directory}/README" not in index:
        err(directory, "no row in the root README index table")


def check_document(path: str) -> None:
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    check_tables(rel, lines)
    check_section_refs(rel, text)
    check_ordered_lists(rel, lines)
    check_links(rel, path, text)
    check_header(rel, lines)
    if path.endswith(".cs.md"):
        check_czech_quotes(rel, text)


def main() -> int:
    names = sys.argv[1:]
    if not names:
        names = sorted(
            d for d in os.listdir(ROOT)
            if os.path.isdir(os.path.join(ROOT, d))
            and not d.startswith(".")
            and os.path.exists(os.path.join(ROOT, d, "README.md"))
            or (os.path.isdir(os.path.join(ROOT, d))
                and not d.startswith(".")
                and os.path.exists(os.path.join(ROOT, d, "README.cs.md")))
        )
    if not names:
        print("no comparison directories found")
        return 1

    for name in names:
        directory = os.path.join(ROOT, name.rstrip("/"))
        en = os.path.join(directory, "README.md")
        cs = os.path.join(directory, "README.cs.md")
        found = [p for p in (en, cs) if os.path.exists(p)]
        if not found:
            err(name, "directory has neither README.md nor README.cs.md")
            continue
        for path in found:
            check_document(path)
        if os.path.exists(en) and os.path.exists(cs):
            check_parity(name, en, cs)
        elif not os.path.exists(en):
            warn(name, "no English README.md — English is canonical, so this cannot leave ⏳")
        check_index_row(name)

    for line in warns:
        print(line)
    for line in errors:
        print(line)
    print(f"\nchecked {len(names)} comparison(s): {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
