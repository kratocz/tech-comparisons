---
name: add-dated-section
description: Append a dated section to a published comparison document in this repo — writes it in both EN and CS, inserts before References, updates all five indexes (header "Facts verified" bullet, footer, References block, References intro date, root README row), normalises Czech quotes, runs the validator, then commits and pushes. Use when adding a new §N, recording a correction, or when the user says "sepiš to do dokumentu", "přidej sekci", "add a section", "write this up as §N".
---

# Add a dated section to a comparison document

Published documents in this repo grow by **appending dated sections**, never by
rewriting earlier ones — `§N` cross-references, including from sibling
documents, point at the existing numbers. See `AGENTS.md` for the rules this
skill mechanises.

## Steps

1. **Establish the current state.** Do not assume it. Read the last `## N.`
   heading in `<dir>/README.md` to get the next number, and read the
   **Facts verified** bullet in the header (its line number varies by document)
   and the footer paragraph verbatim — both accumulate across edits and
   their exact wording changes every time a section is added.

2. **Decide correction vs addition.**
   - New content → `## N. Title (added YYYY-MM-DD)`.
   - An error in an already-published section → fix it **in place** *and* append
     `## N. Correction (YYYY-MM-DD): …` saying what was wrong.
   - An error belonging to an addendum you are writing anyway → record it as a
     **sub-section of that addendum** (`### 26.4 Correction to §21.1`) rather
     than a standalone `## N. Correction`, which would only repeat its context.
   - An error in a section published **the same day** → an inline dated
     parenthetical inside that section is enough; do not append a section.

3. **Write both languages.** They must stay structurally identical: same
   `##` and `###` numbers in the same order. Quote rules:
   - Czech phrases → `„…“`
   - verbatim English quotations → ASCII `*"…"*`
   Mixing them (`„` opened, `"` closed) is the mistake that recurs; the
   validator catches it as an unbalanced-quote error.

4. **Verify before asserting.** Any claim of the form "there is no tool",
   "cannot", "never", "only via migration" gets its primary source fetched
   *before* the sentence is written. This repo has had to walk back three such
   claims in one day.

5. **Insert before `## References`** (EN) / `## Reference` (CS) — never at the
   end of the file, which would put the section after the references.

6. **Update the five indexes**, every one of which an audit has caught out of date:
   - header **Facts verified** bullet — **extend the matching date group**; the
     bullet stays short, "date groups with a phrase and a section range, never a
     title per section" (AGENTS.md). Enumerating every section bloated it to 1 474
     characters once
   - closing footer paragraph — same list, matching punctuation. **Re-read this
     sentence end to end afterwards**: it is a single long sentence that
     accumulates clauses, and dropped commas have survived two rounds of edits
   - `## References` — add the sources with the date each claim was checked
   - the References block's **intro line**, whose "verified to …" date goes stale
   - the **root `README.md` index row**, whose "Facts verified" column does too

7. **Check the date with `date`.** Do not infer it from context, from a greeting
   or from the previous section's heading. In a repository whose documents are
   dated snapshots the date is load-bearing, and it has already been wrong by a
   day for eight sections at once.

8. **Validate.** `scripts/check-comparison.py <dir>` must exit 0. Warnings are
   informational; errors are not.

9. **Commit and push.** Pre-authorised for this repo's documents. The message
   states what was verified and what changed, not just that a section was
   added.

## Traps this exists to prevent

- Nested `**bold**` inside an already-bold header span silently unbolds the
  rest of the line — use `*italics*` for a clause inside the header bullet.
- A `§N` next to a sibling document's name needs a relative link, or it
  resolves against the current file.
- Editing several files in one script: a failure on file 2 leaves files 3+
  untouched. Check every file was written, not just that the script printed
  something.
