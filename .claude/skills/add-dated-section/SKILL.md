---
name: add-dated-section
description: Append a dated section to a published comparison document in this repo — writes it in both EN and CS, inserts before References, updates the header "Facts verified" bullet, the footer and the References block, normalises Czech quotes, runs the validator, then commits and pushes. Use when adding a new §N, recording a correction, or when the user says "sepiš to do dokumentu", "přidej sekci", "add a section", "write this up as §N".
---

# Add a dated section to a comparison document

Published documents in this repo grow by **appending dated sections**, never by
rewriting earlier ones — `§N` cross-references, including from sibling
documents, point at the existing numbers. See `AGENTS.md` for the rules this
skill mechanises.

## Steps

1. **Establish the current state.** Do not assume it. Read the last `## N.`
   heading in `<dir>/README.md` to get the next number, and read the header
   line 4 and the footer paragraph verbatim — both accumulate across edits and
   their exact wording changes every time a section is added.

2. **Decide correction vs addition.**
   - New content → `## N. Title (added YYYY-MM-DD)`.
   - An error in an already-published section → fix it **in place** *and* append
     `## N. Correction (YYYY-MM-DD): …` saying what was wrong.
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

6. **Update the three indexes**, all of which the audit has caught out of date:
   - header **Facts verified** bullet — name the new section
   - closing footer paragraph — same list, matching punctuation
   - `## References` — add the sources with their verification date

7. **Validate.** `scripts/check-comparison.py <dir>` must exit 0. Warnings are
   informational; errors are not.

8. **Commit and push.** Pre-authorised for this repo's documents. The message
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
