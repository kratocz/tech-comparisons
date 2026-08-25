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
the question does. The name is a **plain noun phrase for the subject, not the
activity**: `smartwatch-platforms`, not `smartwatch-platform-choice`. Every
document here is a decision, so a `-choice` or `-comparison` suffix restates the
repository instead of the topic — `programming-language-choice` was renamed to
`programming-languages` for exactly that reason. `zfs-vs-ceph` predates the rule
and breaks it: leave it be, but do not copy it. Inside:

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
  paragraph. **Read every date from the clock, never infer it** — not from the
  time of day, not from a greeting, not from the section above. Dates here are
  the document's whole claim to being checkable, and eight sections once
  shipped dated a day into the future because "good morning" arrived shortly
  before midnight.
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
about. The exception is a **verbatim quotation from an English source**: those
keep ASCII quotes, normally inside italics (`*"…"*`), because they are being
reproduced rather than written. Mixing the two — opening with `„` and closing a
piece of English with `"` — is the mistake that actually happens, repeatedly;
`scripts/check-comparison.py` catches it as an unbalanced-quote error. And inside table cells, put spaces around a slash separating two values
(`` `recordsize` / `volblocksize` ``): without them the cell has no break
opportunity and holds the whole column wider than its content needs.

Write for a reader outside the bubble. English-derived scene slang — *indie*,
*boilerplate*, *vendor lock-in* — costs comprehension without buying precision,
and in Czech it can be actively misread (`indie aplikace` was taken for
Indian). Prefer the plain multi-word phrasing, or gloss the term on first use.
Established technical vocabulary is fine; slang is not.

When a table's ratings are aggregated with weights, remember what a weight can
and cannot do: **influence comes from variance within a criterion, not from the
weight on it**. A column where every option scores alike contributes alike to
everyone and cannot order the field however heavily it is weighted, which is
counter-intuitive to whoever set the weights and worth saying out loud in the
document. The same applies to any prediction written before the research —
predict from where the spread is, not from a candidate's strengths.
`programming-languages` has one prediction of each kind, and only the one
reasoning about variance survived contact with the results.

## Durable layer vs dated layer

Structure a comparison so the **verdict rests on properties that do not
change**: architecture, platform philosophy, lock-in, data ownership, licensing,
support commitments. Perishable facts — prices, per-model specs, per-country
feature availability — belong in a **separate, explicitly dated snapshot
section** that is not load-bearing for the verdict.

The point is graceful ageing: when the snapshot is stale a year later, the
analysis still holds and the reader can see exactly which part expired.

For that to work the snapshot has to say **which version of each option the
ratings were anchored to** — the release actually assessed, not merely the one
current at the time. Without it a reader a year on cannot tell what expired
from what was never checked. `programming-languages` ran nine rounds before
noticing it had never recorded this; writing the table out was what exposed
that three of eight languages had been read as "the current documentation" with
no version pinned at all, and that one of them had since been rewritten in
another language.

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
- **An impossibility claim needs a primary source before it is written**, not
  after someone questions it. "There is no tool", "it cannot be changed", "never",
  "only via migration" — these are the claims a reader cannot check and the ones
  this repo has had to walk back repeatedly — `zfs rewrite` existed, then did more
  than the first correction allowed, then did less than the second claimed; the
  pool count was not irreversible; the dRAID threshold was invented outright.
  Nearly every time the trigger was a reader's question rather than a
  verification pass, which is the part worth fixing. Fetch the man page or the docs page *first*, then write the
  sentence — and if the source is silent, say that instead of inferring the
  stronger claim. `scripts/check-comparison.py` warns about the subset of these
  that appear in comparison tables, which is a net, not a substitute.
- **An empty search result is not a source.** It shows that one query, against
  one index, returned nothing — which is also what a misspelt term, the wrong
  repository or branch, an index that never covered the thing, or a feature
  living under another name all look like. Absence of evidence has to be argued
  for; it does not arrive for free. When a claim rests on something *not*
  existing, do two things: search several ways, and run a **positive control** —
  search for something you are certain is there. If the control also comes back
  empty, the search is broken, not the world. `zfs-vs-ceph`'s "CephFS cannot
  reflink" was right, but for a day it rested on a single empty code
  search; the evidence that actually supports it is three terms returning zero
  across the whole tree *plus* `copy_file_range` returning five, which is what
  proves the search worked at all. And keep "the source is silent" distinct from
  "the source says no" — silence goes into the document as silence.

  Two ways this rule gets broken that are worth naming, because both happened in
  one document. The first is asserting absence with **no search at all** — "no
  official language server exists for PHP" was written without a single query
  behind it, which is worse than an empty result because there is not even a
  broken search to distrust. The second is subtler: **a convincing source stops
  you searching**. A quote from the TypeScript team saying no support policy
  existed felt conclusive, so the repository root was never listed — and
  `SUPPORT.md` was sitting in it, which made a decision rule fire against the
  eventual winner on a false fact. So: before writing that something does not
  exist, check the **standard locations** for that kind of fact — for a
  repository, the root, `.github`, `SUPPORT.md`, `SECURITY.md` — and check them
  even when you already hold a source that sounds final. A verified quote about
  absence is only a claim about what its author knew when they wrote it.
- **A verified statement does not extend to cases the source never named.** This
  one is harder to catch than the two above, because a source *was* fetched — it
  simply answered a neighbouring question. In one day `zfs rewrite` was verified
  to defragment and recompress, and that was then written as covering ZVOLs (the
  synopsis takes `file|directory`), as repairing free-space fragmentation (it
  allocates from the same free space), and as applying `recordsize` (*"Changes
  to properties that affect the size of a logical block, like recordsize, will
  have no effect"*). Three wrong claims from one correct one.

  The tell is that sources state their own scope and it is easy to read as
  incidental: the operand types in a SYNOPSIS, an enumeration like *"These
  include checksum, compression, dedup and copies"*, a qualifier like "for
  filesystem datasets". Those lists are usually exhaustive, not illustrative.
  So before carrying a verified fact to a case the source did not mention,
  treat the extension as a **new claim** and go back for its own scope line.
  The question is not "is this true?" but "did the sentence I read say
  anything about *this*?".

  For Ceph specifically the scope variable is almost always the same one, and
  it is worth naming because it went missing three times in two days: **which
  failure domain the claim assumes**. Re-replication after a loss, self-heal
  headroom, EC's `k+m` requirement and what a node going away actually costs
  all behave differently under an OSD-level domain than a host-level one, and
  the single-node configuration silently uses the former
  (`osd_crush_chooseleaf_type = 0`). Every claim about Ceph's behaviour on
  failure should therefore say, at least to yourself, which domain it assumes —
  a claim that does not survive being asked "at how many hosts?" was written
  about a different cluster than the one being described.
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

**When the brief itself changes mid-analysis, record it as a new dated brief —
never as a rewrite of the old one.** Give it its own section, its own rules
written before its own research, and leave the first verdict standing as the
answer to the first question. Editing the original criteria after seeing results
destroys the one property that made writing them in advance worth anything, and
the disagreement between two honest verdicts is usually more informative than
either alone: in `programming-languages` the winner of the first brief placed
seventh in the second, which is the document's most useful single finding.

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

**Errors** (these fail the run): a table whose rows disagree on cell count; a
`§N` or `§N.M` that resolves to no section or sub-section in that file; numbered
sections that do not start at 0 or 1 (a `## 0.` status section is allowed) or
that are not consecutive; sub-sections that do not count up from `N.1`
within their parent in document order (a block pasted into the wrong place
renders fine, so nothing else catches it); or an ordered list whose numbers are
out of order or repeated (a gap such as 1, 2, 4 passes); a relative link that does not
resolve; a URL mangled by a bulk edit; the two language versions disagreeing on
section count, table-row count, section numbers or sub-section numbers;
unbalanced Czech quotes (checked in `README.cs.md` only — a mixed quote in the
English file is not caught); a comparison directory with no row in the root
README index; a comparison directory holding neither `README.md` nor
`README.cs.md`; header metadata that is not a bullet list.

**Warnings** (reported, never fatal): open `[OVĚŘIT]` / `[VERIFY]` tags, with or
without text inside the brackets; a comparison directory with no English version;
a `§`-reference sitting next to a sibling document's name without a relative link,
which would otherwise resolve against the wrong file; and a table row asserting
an impossibility with no citation, `§`-reference or quoted wording behind it.

What it does **not** check is prose. Every convention above that lives in a
sentence rather than in structure is still on the writer. Run it before every commit that touches a
comparison — writing `storage-replication` it caught a table column inserted at
the wrong index and two ordered lists numbered out of sequence, none of which
survived a reading.

## Corrections after publication

A document is a dated snapshot and is not retro-updated as its facts age — but
an **error is not ageing**. When one surfaces, fix the wrong cell or sentence in
place *and* record the correction as a dated addendum section at the end
(`## 13. Correction (2026-08-13): …`), saying what was wrong and what it changed.
The project skill `add-dated-section` mechanises the whole append — both
languages, the header bullet, the footer and the References block — so reach for
it instead of doing this by hand.
Always append, never renumber: `§N` cross-references — including ones in sibling
documents — point at the existing numbers.

**New content lands the same way.** A published document grows by appending
dated sections (`## 20. … (added 2026-08-14)`), never by rewriting earlier ones,
for the same reason. The new section must then be named in the places listed
under "Three places index an addendum" below — the header's **Facts verified**
bullet, the closing footer, and the References block. They are the document's index
of what was added when, and a section missing from either is invisible to a
reader who starts at the top.

A correction may also ride **inside a new addendum as its own sub-section**
(`### 26.4 Correction to §21.1`) when the addendum is being written anyway and
the correction belongs to its subject. That is how §26.4, §27.1–27.3 and §30.3
were recorded, and it beats a standalone `## N. Correction` that would repeat
the addendum's context.

Three places index an addendum, not two: the header's **Facts verified** bullet,
the closing **footer**, and the **References** block, whose intro date and
per-entry dates both go stale if only the first two are updated.

Keep the header bullet **short**: date groups with a phrase and a section range,
never a title per section. Each heading already carries its own date and the
footer already enumerates them, so the header only has to say what was verified
when and roughly what it covered. Enumerating instead produced a 1 474-character
line at sixteen addenda — a header nobody reads, which is a rule failing rather
than a document growing.

**Exception — a correction to a section published the same day** may be recorded
inline, as a dated parenthetical inside that section, rather than as its own
addendum. Appending `## 24. Correction …` to fix `## 23.` written an hour
earlier adds numbering without adding information. The cut-off is publication
date, not convenience: once a section has been out for a day, it gets a proper
addendum.

If the error sat underneath a decision rule, leave the rule exactly as written
and report that it **did not fire**. Rewriting a rule once you have seen the
outcome destroys the only property that made it worth writing in advance.
