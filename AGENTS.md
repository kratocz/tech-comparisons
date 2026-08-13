# AGENTS.md

Working notes for anyone — human or agent — adding to this repository.

## What this repo is

Dated decision analyses, each anchored to a concrete context and ending in a
verdict. Not neutral feature matrices: the point of every document is a real
decision someone actually made, with the accepted trade-offs spelled out. The
root `README.md` states the four editorial principles; this file covers how to
apply them in practice.

## Repository layout

One directory per comparison, named after the **topic** rather than the vendors
(`storage-replication`, `smartwatch-platforms`) — vendor names date faster than
the question does. `zfs-vs-ceph` predates the rule and breaks it: leave it be,
but do not copy it. Inside:

- `README.md` — English, canonical.
- `README.cs.md` — the Czech original, kept alongside when the analysis
  originated in Czech.

Every comparison directory on `main` has a row in the root `README.md` index
table — including one still being researched, which carries `⏳ in progress` in
the verdict column until it is done. The ⏳ is what lets unfinished work sit in
the open instead of hiding on a branch nobody reads; what clears it is the
second bar in the workflow section below.

## Anatomy of a comparison

- **Header metadata** as a bullet list (`- **Verdict:** …`, `- **Facts
  verified:** …`, `- **Language:** …`, `- **Author:** …`). The bullets are
  required, not cosmetic: CommonMark merges adjacent plain lines into a single
  paragraph.
- **Context** section first — the concrete profile the verdict claims validity
  for, and nothing beyond it.
- **Comparison at a glance** — a symbol table (✅ strength · 🟡 works with
  caveats · ❌ weakness · — not applicable) rated **for that context**, with the
  rating basis stated explicitly in the table's intro. Group rows under
  `**▸ …**` sub-headers, and follow the table with a short "how to read it"
  section naming who wins where.
- Numbered `##` sections for the argument, cross-referenced inline as §N.
- **References** section with URLs and a verification date for the block, with
  per-entry dates where they differ.
- Footer: the document is a dated snapshot and is not retro-updated.

Keep the option ordering identical in **every** table of a document — including
small side tables — so a reader never has to re-orient. If the main table reads
Garmin, Apple, Samsung, the price table and the health table read the same way.
The same holds **across sibling documents**: where two comparisons rate the same
options, they list them in the same order, so a reader moving between them keeps
one axis. `storage-replication` puts Btrfs after the Ceph columns because
`zfs-vs-ceph` does.

Two formatting details that are easy to get wrong and tedious to fix later.
Czech text uses Czech quotation marks (`„…“`) — not a Czech opening quote closed
with an ASCII one, which is what you get by default and which nothing warns you
about. And inside table cells, put spaces around a slash separating two values
(`` `recordsize` / `volblocksize` ``): without them the cell has no break
opportunity and holds the whole column wider than its content needs.

## Durable layer vs dated layer

Structure a comparison so the **verdict rests on properties that do not
change**: architecture, platform philosophy, lock-in, data ownership, licensing,
support commitments. Perishable facts — prices, per-model specs, per-country
feature availability — belong in a **separate, explicitly dated snapshot
section** that is not load-bearing for the verdict.

The point is graceful ageing: when the snapshot is stale a year later, the
analysis still holds and the reader can see exactly which part expired.

Use the same ratio to judge whether a topic is worth writing up at all. A
subject that is mostly perishable detail (a shopping shortlist, a current price
comparison) gives a reader far less than one whose durable layer carries the
conclusion.

## Sourcing and verification

- Every load-bearing claim is traceable to a source. Two citation styles are in
  use and both are acceptable: numbered tags `[R1]`, `[R2]`, … resolved in the
  References section (`smartwatch-platforms`), or inline links with the
  References section grouping URLs by topic (`zfs-vs-ceph`,
  `storage-replication`). Pick one per document and hold it throughout.
- Claims not yet verified are tagged inline with `[OVĚŘIT]` / `[VERIFY]`, so a
  half-researched document never reads as finished. The header states which
  parts are verified and which are not, and names any open tags — as its own
  bullet or folded into the verification bullet, either is fine as long as a
  reader meets it in the header.
- Distinguish **fact** from **inference** in the prose — "X is still on the
  support list (fact); by the Y pattern its support likely ends around Z
  (inference)". Never let an inference wear a fact's clothes.
- Prefer primary sources: the vendor's own spec or support page over a review
  quoting it. Where sources contradict each other, record the contradiction in
  the document and say which one is treated as authoritative and why.
- Findings from an earlier AI conversation are **hypotheses, not sources**.
  Verify them against primary sources before they enter a document, and correct
  the document plainly when they turn out to be wrong.
- **Ratings are context-bound, including your own.** A ✅/🟡/❌ in a sibling
  comparison answers *that* document's question, not this one's. Treat an
  imported cell exactly like an AI-conversation finding: a hypothesis, to be
  re-derived against a primary source. `storage-replication` inherited "min. 3
  nodes" for Ceph from `zfs-vs-ceph`, where the question was what to build
  production storage on; here the question was what must exist on the far side
  to receive a replica, and a single-node cluster turns out to be supported.
  The cost was not one wrong cell — an entire disqualifying criterion rested
  on it.

## Workflow for a new comparison

Work in progress lives on its own branch. Research lands in **rounds** — one
commit per round, its message summarising what was verified and what it changed
— so the reasoning survives even if the branch sits for months.

Whether a PR is involved follows from how long the work runs. An analysis
spanning sessions or months gets one, so the rounds have somewhere to be read
(`smartwatch-platforms`, PR #1). One finished inside a single session does not
need it: branch, then `git merge --no-ff` so the rounds stay legible in the log,
then push (`storage-replication`). Corrections after landing go straight to
`main` as their own commits.

Write the **decision rules before the research**, dated, inside the document, so
that once results arrive the rules are read rather than invented. When that
ordering was not achieved — the research ran first — say so in the header
instead of letting the rules read as pre-registered. A rule presented as
pre-written when it was not is a false claim in a document whose whole value is
that its claims can be trusted.

There are **two bars**, and collapsing them into one is what makes an index
full of ⏳ rows look like a mess rather than a work log.

**To land on `main` at all**, carrying `⏳ in progress`:

1. The **Context** section is written, so a reader knows what question the
   document answers and for whom. A draft without it is not an early analysis,
   it is notes.
2. The header states what is verified and what is not, and names any open
   `[OVĚŘIT]` / `[VERIFY]` tags — so nobody mistakes a draft for a finding.
3. The root README index has its row, with `⏳ in progress` in the verdict
   column.

**To drop the ⏳** and count as finished:

1. It ends with a **verdict** — the option actually chosen, with the accepted
   trade-offs spelled out. A menu of options is research, not a decision.
2. Load-bearing claims carry sources and a verification date.
3. The English `README.md` exists (English is canonical).
4. The index row states that verdict and its verification date.

Work that does not clear the first bar stays on its branch. Work that clears the
first but not the second lives on `main` under a ⏳ — `smartwatch-platforms` is
there now — which is the point of the marker: an analysis that stalls stays
visible, and a reader is told exactly how far it got.

Most of the mechanical conventions above are checkable, so check them instead of
re-reading for them:

```
scripts/check-comparison.py                  # every comparison
scripts/check-comparison.py storage-replication
```

It verifies that every row of a table has the same cell count, that each `§N`
resolves to a section that exists, that numbered sections and ordered lists run
consecutively, that relative links resolve, that no URL was mangled by a bulk
edit, that the two language versions agree on section and table-row counts, and
that Czech quotes are balanced. It warns about open `[OVĚŘIT]` / `[VERIFY]` tags
rather than failing on them. Run it before every commit that touches a
comparison — writing `storage-replication` it caught a table column inserted at
the wrong index and two ordered lists numbered out of sequence, none of which
survived a reading.

## Corrections after publication

A document is a dated snapshot and is not retro-updated as its facts age — but
an **error is not ageing**. When one surfaces, fix the wrong cell or sentence in
place *and* record the correction as a dated addendum section at the end
(`## 13. Correction (2026-08-13): …`), saying what was wrong and what it changed.
Always append, never renumber: `§N` cross-references — including ones in sibling
documents — point at the existing numbers.

If the error sat underneath a decision rule, leave the rule exactly as written
and report that it **did not fire**. Rewriting a rule once you have seen the
outcome destroys the only property that made it worth writing in advance.
