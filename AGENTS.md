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
(`zfs-vs-ceph`, `smartwatch-platforms`) — vendor names date faster than the
question does. Inside:

- `README.md` — English, canonical.
- `README.cs.md` — the Czech original, kept alongside when the analysis
  originated in Czech.

Every published comparison has a row in the root `README.md` index table. An
analysis still in progress may be indexed with `⏳ in progress` in the verdict
column.

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
- **References** section with URLs and the date each was verified.
- Footer: the document is a dated snapshot and is not retro-updated.

Keep the option ordering identical in **every** table of a document — including
small side tables — so a reader never has to re-orient. If the main table reads
Garmin, Apple, Samsung, the price table and the health table read the same way.

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

- Every load-bearing claim gets a numbered reference `[R1]`, `[R2]`, … resolved
  in the References section with a URL and a verification date.
- Claims not yet verified are tagged inline with `[OVĚŘIT]` / `[VERIFY]`, so a
  half-researched document never reads as finished. The header states which
  parts are verified and which are not, and names any open tags.
- Distinguish **fact** from **inference** in the prose — "X is still on the
  support list (fact); by the Y pattern its support likely ends around Z
  (inference)". Never let an inference wear a fact's clothes.
- Prefer primary sources: the vendor's own spec or support page over a review
  quoting it. Where sources contradict each other, record the contradiction in
  the document and say which one is treated as authoritative and why.
- Findings from an earlier AI conversation are **hypotheses, not sources**.
  Verify them against primary sources before they enter a document, and correct
  the document plainly when they turn out to be wrong.

## Workflow for a new comparison

Work in progress lives on its own branch with a **draft PR**. Research lands in
rounds — each round is a commit plus a PR comment summarising what was verified
and what it changed. That way the reasoning survives even if the branch sits for
months.

Write the **decision rules before the research**, dated, inside the document, so
that once results arrive the rules are read rather than invented.

A comparison reaches `main` only when all of these hold:

1. It ends with a **verdict** — the option actually chosen, with the accepted
   trade-offs spelled out. A menu of options is research, not a decision.
2. Load-bearing claims carry sources and a verification date.
3. The English `README.md` exists (English is canonical).
4. The root README index has its row.

A document that fails any of these stays on its branch rather than landing
half-finished.
