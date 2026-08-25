# Choosing a programming language: one language for years, for new projects

- **What this document answers:** **two different questions**. The brief was refined during the work, and the new version was recorded as a new dated brief rather than a rewrite of the old one (§7.1) — so the document carries two verdicts side by side. If only one question interests you, the rest can be skipped.
- **Question 1 — which language is the most professional, meaning legible in small and in very large codebases? → §7.** Verdict (§7.5): **Kotlin and Rust, joint first** — the only two of eight clean on all four criteria. The rule does not settle the tie, and a tie-breaker is not written after seeing the result, so the choice between them belongs to the decider.
- **Question 2 — which language best covers four specific domains at once? → §3 and §6.** Verdict (§6.2): **TypeScript**, weighted cost 4 ahead of Python's 5, with its trade-offs itemised — the most expensive being that types are not enforced at runtime.
- **Headline finding — the two verdicts disagree (§7.5):** the winner of question 2 places seventh in question 1. **No language is simultaneously the best fit for those four domains and the most professional tool.** That trade is the document's actual content, not either verdict on its own.
- **Decision it feeds:** what to build **new** projects on over a horizon of years — mine, a company's, or someone else's — and how to argue that choice to somebody who was not part of the reasoning.
- **Facts verified:** 🟡 2026-08-22 to 2026-08-23, eight rounds, references [R1]–[R77]. No open `[VERIFY]` tags. Admittedly incomplete: §4.1 (PHPStan and Psalm levels), §4.2 (C# and Rust), §7.4 (criterion P2 measures only formatter ownership, not how much magic you must hold in your head).
- **Predictions:** two, both written before their own research. §2.3 **failed** — Go was predicted to rise and finished last. §7.3 **held** on every point; the difference was that it reasoned about variance within criteria rather than about candidates' strengths.
- **Addenda:** §9 (2026-08-26) — why PHP trails Python; the gap holds, but a quarter of it rests on the formalistic criterion P2. §10 (2026-08-26) — **which versions were actually analysed**: PHP 8.5 verified after the fact (nothing changes), TypeScript 7 is a native rewrite in Go the analysis did not account for, and M1 was applied unevenly.
- **Correction:** ⚠️ §8 (2026-08-23) — the claim that TypeScript has no support commitment was false; gate B2 fired on a wrong fact and should not have fired. The verdicts do not change; one line of the bill is cheaper.
- **Adversarial pass:** 🟡 2026-08-23 (§6.1) — of four cells examined, one did not survive and was corrected (PHP in the browser); the top two placings did not move. **Limitation: the pass ran in the same context that produced the conclusion, not a fresh one.**
- **Language:** 🇬🇧 English (canonical) · 🇨🇿 [Čeština](README.cs.md) (original)
- **Author:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## TL;DR

*Summary added 2026-08-26. It adds no claim — it only gathers the results of §3, §6 and §7 so they need not be hunted for.*

The document answers **two questions** and **each has a different winner**. The table is ordered by language professionalism; a lower number is always better. The four professionalism criteria come from §7.2, cell costs are ✅ = 0 · 🟡 = 1 · ❌ = 3, so the sum can be recomputed by eye. The full cells with their sources are in §7.4.

| # | Language | P1 compiler catches the mistake | P2 legible to people | P3 large refactors safe | P4 types carry the domain model | Sum | Domains (§6.2) |
|---|---|---|---|---|---|---|---|
| 1.–2. | **Kotlin** | ✅ nullability in the types | ✅ `ktfmt` under `Kotlin` | ✅ `kotlin-lsp` under `Kotlin` | ✅ sealed classes, `when` without `else` | **0** | 6 — 5th |
| 1.–2. | **Rust** | ✅ no null, `match` exhaustive | ✅ `rustfmt` under `rust-lang` | ✅ `rust-analyzer` under `rust-lang` | ✅ enums carry data | **0** | 7 — 6th |
| 3. | C# | 🟡 nullability compile-time only | ✅ `dotnet format` under `dotnet` | ✅ static types + Roslyn | 🟡 sum types still only a proposal | 2 | 6 — 3rd |
| 4. | Go | 🟡 `nil` is the zero value of everything | ✅ `gofmt` in the distribution | ✅ `gopls` under `golang` | ❌ variant types left out deliberately | 4 | 9 — 8th |
| 5.–6. | Java | 🟡 generics erased, no nullability | ❌ no official formatter | 🟡 language server is Eclipse's | ✅ sealed + exhaustive `switch` | 5 | 6 — 4th |
| 5.–6. | Python | ❌ runtime does not enforce types | ✅ `black` under `psf` | 🟡 dynamic; `mypy` is first-party | 🟡 static checking only | 5 | 5 — 2nd |
| 7. | TypeScript | ❌ types erased at compile time | ❌ no official formatter | ✅ static types + Microsoft tooling | ✅ discriminated unions and `never` | 6 | **4 — 1st** |
| 8. | PHP | ❌ strictness per file, no generics | ❌ no official formatter | ❌ no official language server | ❌ enums carry only a scalar | 12 | 8 — 7th |

What those four criteria mean (the full wording and what each measures is in §7.2):

- **P1 — the compiler catches the mistake before the user does:** the type-enforcement boundary (at runtime, or only at check time), nullability in the type system, exhaustive branching.
- **P2 — a stranger can read the code without context:** is there an official formatter under the language's own organisation? *(Only that — see the caveat below.)*
- **P3 — large refactors are safe:** static types plus an official language server; will the tooling find every call site?
- **P4 — the type system carries the domain model:** sum types carrying data, and exhaustive branching over them.

- **Most professional language (§7):** **Kotlin and Rust, joint first** — the only two clean on all four criteria. The rule does not settle the tie and a tie-breaker is not written after seeing the result, so the choice between them belongs to the decider.
- **Best coverage of the four domains (§6.2):** **TypeScript**, weighted cost 4 ahead of Python's 5 — but it pays for that by not enforcing types at runtime.
- **Headline finding:** the winner of the second column places seventh in the first. **No language is simultaneously the best fit for the domains and the most professional tool** — and that trade is the document's actual content, not either verdict on its own.
- **Two criteria are incompletely measured, and the document says so:** P2 rates only whose organisation owns the formatter, not how much magic you must hold in your head (§9.3), and P4 does not rate immutability although §7.2 lists it (§10.1). For the PHP–Python pair roughly a third of the gap rests on P2 alone.
- **Mind the scope:** both numbers hold for the profile in §1 (new greenfield projects) and for the rules in §2.3 and §7.2. Different weights give a different winner — the sensitivity analyses are in §6.3 and §7.4.

## 0. Status and open tasks

- [x] context (§1) — 2026-08-22
- [x] decision rules (§2) written before the research — 2026-08-22
- [x] row in the root README — 2026-08-22
- [x] **decision rules (§2) confirmed by the decider** — 2026-08-22: domain weights added (§2.3), B1 narrowed to backend (§2.2), aggregation rewritten as weighted cost; prediction recorded before the research
- [x] properties table (§4.8) — 2026-08-22
- [x] regret matrix (§3) including weighted cost and how to read it (§3.1) — rounds 2 to 5, 2026-08-22
- [x] durable layer (§4) — §4.1 to §4.7 complete (rounds 1 to 7, 2026-08-22)
- [x] dated snapshot (§5) — 2026-08-22
- [x] adversarial pass (§6.1) — 2026-08-23
- [x] verdict (§6.2) plus per-domain reading and weight sensitivity (§6.3) — 2026-08-23
- [x] **second brief: professionalism rules (§7.1–§7.3) written 2026-08-23 BEFORE its research** — committed separately so the ordering is checkable from the history
- [x] professionalism research (§7.4) and second verdict (§7.5) — 2026-08-23: **Kotlin and Rust joint first**
- [x] **correction §8 (2026-08-23): gate B2 fired on a wrong fact and should not have fired**
- [x] addendum §9 (2026-08-26): why PHP trails Python, PHPStan levels added and two under-evidenced claims repaired
- [x] addendum §10 (2026-08-26): audit of the analysed versions, PHP 8.5 verified, TypeScript 7 recorded
- [x] English version (`README.md`) as the canonical one — 2026-08-26

## 1. Context: what decision is actually being made

The question is not "which language is best" nor "what is each language good for". It is: **if I had to pick one language to build new projects on for years, across four domains, which one, and what would I pay for it?**

- **Greenfield.** Every project in scope is **new**. Whose it is does not matter — mine, a company's, someone else's. That common denominator is what makes the analysis tractable: it removes the switching cost of an existing system, which would otherwise decide more than the language's own properties.
- **What this document does NOT answer:** migrating an existing system ("we have a PHP monolith, should we move to X?"). That is a different question with a different answer, dominated by the cost of the move rather than the quality of the target.
- **Four domains, unequally weighted** (§2.3, §3), in weight order: web backend and API (4); CLI tools, daemons and automation (3); web frontend in the browser (2); data, ML and batch processing (1). The language must cover all four — but not to the same degree, and that inequality is part of the brief, not a compromise arrived at along the way.
- **Performance is not a hard requirement.** The decider has no specific workload — they simply do not want to hit a ceiling. Performance is therefore a **soft axis with the ceiling described in numbers** (§4.2), not an eliminating gate. Direct consequence: a language whose cost is paid daily and whose advantage is collected only under extreme load starts at a disadvantage here.
- **Two roles, one verdict.** The choice also serves as the basis for recommendations inside companies. Because the scope is limited to greenfield, the two roles converge and the verdict is one. The consulting role shows up differently: it raises the citation bar (every load-bearing claim carries `[R…]`) and gives full weight to hiring, ecosystem funding, LTS and breaking-change history (§4.4–§4.6). If the research had shown the personal optimum differing from the company one, the document would carry both verdicts side by side rather than an average.
- **Decider's profile:** full-stack developer, solo or small team, Czech Republic. Centre of gravity so far in PHP; that is a fact of context, not a default favourite.

## 2. Decision rules (written 2026-08-22 — BEFORE the research)

Rules are written before measuring; after the result they are read, not invented. **Status: not yet confirmed by the decider** — until they are, the research does not begin.

### 2.1 Candidates

Eight languages, ordered **alphabetically** — the ordering is deliberately neutral so it does not itself suggest a favourite, and it **stays identical in every table in this document**:

`C#` · `Go` · `Java` · `Kotlin` · `PHP` · `Python` · `Rust` · `TypeScript`

Eliminating a candidate is recorded with a reason and with the rule it fell on. An empty cell is not an elimination.

### 2.2 Hard gates

| # | Gate | Rationale |
|---|---|---|
| **B1** | ❌ in **backend and API** (the highest-weighted domain, §2.3) → eliminated. ❌ in the other three domains **does not eliminate** — it is paid for in the weighted cost (§2.3) and recorded in the verdict as an explicitly accepted cost | One language is chosen chiefly for the highest-weighted domain; a ❌ there voids the point of the choice. In a lower-weighted domain a ❌ is expensive but payable — and admitting the cost is more honest than quietly dropping a candidate. |
| **B2** | No identifiable payer for the ecosystem **or** no documented commitment to long-term support → eliminated | A decade-long bet needs somebody funding it. Verified from documents (§4.4, §4.5), not from reputation. |

**Amendment to B2 — POST-HOC, made 2026-08-22 AFTER the result of round 1.** The original wording above is unchanged and remains readable; this is an appendix, not a rewrite, because a rule edited after seeing the result loses precisely the property that makes writing it in advance worth anything.

- **What happened:** B2 fired against TypeScript (§4.5). The research also showed the rule conflates two different things — for a runtime, "support" is a ticking security obligation; for a compiler, the load-bearing commitment is a compatibility promise. B2 did not distinguish them.
- **New wording:** a long-term support commitment is recognised **either** as a dated support table **or** as a documented backwards-compatibility promise. For a language that compiles to an artifact running elsewhere, the lifecycle read is **that runtime's**, not the compiler's.
- **Consequence:** TypeScript passes the gate — on Node.js with its 30-month LTS [R19]. The missing compiler support policy **stays recorded as a cost** in §4.5 and feeds the tie-breakers rather than disappearing.
- **Decided by:** the decider, 2026-08-22, with the alternative of letting the rule stand and eliminating TypeScript laid out explicitly.
- **Why it was defensible:** B2's intent was "who funds this", and Microsoft meets that without argument. The stumble was in the design of the instrument, not in the risk underneath it. Had the error been in the facts, the rule would have been allowed to fire.

**Note on B1's strength (written 2026-08-22, before the research):** narrowing it to backend turns B1 into a safety net rather than a blade — all eight candidates will probably pass it and the weighted cost in §2.3 will do all the work. It stays deliberately: if some candidate turned out not to handle backend and API properly, that should be an elimination, not a line in a sum.

**Fallback for B1, written in advance:** if **no** candidate survives B1, the rule is **not rewritten** — it is recorded that it fired and that the premise "one language for these domains" is unsatisfiable. The verdict then reads: lowest weighted cost **plus a named escape hatch** for the domain where the candidate fell. This sentence exists so that it is not invented after the results.

### 2.3 Domain weights and the aggregation rule

Domains do not weigh the same. The weights were set by the decider **2026-08-22, before the research**:

| Domain | Weight |
|---|---|
| Web backend and API | 4 |
| CLI, daemons, automation | 3 |
| Frontend in the browser | 2 |
| Data, ML, batch processing | 1 |

**Cell cost:** ✅ = 0 · 🟡 = 1 · ❌ = 3. **A candidate's weighted cost** = sum of (cell cost × domain weight). **Lowest weighted cost wins.** The numbers are here so the result can be recomputed by hand and cannot be bent by interpretation; the maximum is 30, and zero means ✅ in all four.

The rule's original version ("lowest worst-case cell wins") fell together with equal weights — it could not survive the moment a ❌ in backend and a ❌ in data/ML had to hurt differently. Replaced 2026-08-22, still before the research.

Ties are broken in this **fixed order**:

1. strictness that can be switched on and **enforced in CI** (§4.1),
2. size of the hiring pool and handover cost (§4.6),
3. maturity of frameworks and libraries (§4.7).

**Prediction recorded before the research.** These weights have consequences that can be named now — and written in advance, they cannot afterwards be passed off as expected, nor quietly dropped if they fail. This is **inference, not verified fact**: Go should rise (backend and CLI are its home domains and also the two highest-weighted; its weaknesses are in the two lowest-weighted). Python's greatest strength has dropped in value to weight 1, while it pays at weight 3 for startup and distribution. Rust stays penalised because performance is not a hard requirement (§1). For the JVM and .NET the deciding factor will be how well native images work today — which is exactly the case rule M1 exists for. If the research refutes this prediction, that is recorded in the document as a result, not as a correction of the prediction.

### 2.4 Methodological rules

- **M1 — the newest stable version, but with a date of birth.** The current stable version of the language and of its frameworks is what is rated. Every cell resting on a young feature states **which version introduced it** and **whether the ecosystem has caught up** (frameworks, ORMs, static analysis). A feature existing is not the same as it being usable; without that distinction, release notes turn into an argument.
- **M2 — strictness is not scored with a checkmark.** The question "does it handle types?" breaks into five sub-questions, each with a different winner (§4.1): (a) is it enforced at runtime or only at check time; (b) what can the type system express at all; (c) how contagious is an untyped dependency; (d) can it be enforced for everybody in CI, and is there a ratchet against backsliding; (e) what does it cost on greenfield, where you can be strict from line one. The decomposition is applied to **every** candidate equally — including the ones strictness is simply assumed of.
- **M3 — every load-bearing claim carries `[R…]`.** A claim of non-existence ("cannot", "does not exist", "only via") needs a primary source **and** a positive control showing the search works at all. An empty search result is not a source.
- **M4 — ratings are bound to this context** (§1) and to nothing else. A cell imported from elsewhere is a hypothesis, not a fact.
- **M5 — an adversarial pass is mandatory** before the verdict: a separate pass that tries to **refute** the verdict, not to confirm it. Its outcome is recorded in the header.

## 3. Regret matrix: what it costs to use a given language in a given domain

The table does **not ask how good a language is in a domain**. It asks: *what does it cost me if I have to use this one here, because I picked it as my one language.* The difference is load-bearing — a ranking has no losing side, a cost does.

Symbols: ✅ home domain, cost near zero · 🟡 usable, but with a named cost · ❌ cost so high you would reach for another language for this domain. Rated **for the context of §1** (greenfield, performance as a soft axis), not in general.

Fill status: **all four columns verified 2026-08-22** (rounds 2 to 5, §4.3), weighted cost computed per §2.3. Cell costs are ✅ = 0, 🟡 = 1, ❌ = 3; weights 4 · 3 · 2 · 1. **The ordering is provisional** — four cells await the adversarial pass (M5) and the durable layer §4.1, §4.2, §4.6 and §4.7 has not yet fed the tie-breakers.

Columns are ordered **by domain weight, descending** (4 · 3 · 2 · 1, §2.3), so the table reads from the left with what decides most. The last column is the weighted cost per §2.3 — lower is better, range 0 to 30.

| Language | Backend and API (×4) | CLI and automation (×3) | Frontend in the browser (×2) | Data, ML, batch (×1) | Weighted cost |
|---|---|---|---|---|---|
| **C#** | ✅ ASP.NET Core is first-party, one calendar with the language [R9] | 🟡 Native AOT, but with a toolchain and a ban on dynamic features [R20] | 🟡 Blazor WASM: the runtime goes to the browser; iOS heap trap [R35] | 🟡 ML.NET first-party; absent from Spark's and Polars' lists [R43] | **6** |
| **Go** | ✅ `net/http` in the stdlib — no second support window [R8] | ✅ home domain; always cross-compiling [R24] | ❌ ~2 MB floor, 10 MB+ common; survived M5 with a caveat (§6.1) [R37] | ❌ absent from Spark's and Polars' lists [R44][R45] | **9** |
| **Java** | ✅ Spring Boot; but a minor gets only ≥12 months OSS [R31] | 🟡 GraalVM, but closed-world and JSON metadata [R21] | 🟡 TeaVM (third party); limitations undocumented [R41] | 🟡 first class in Spark; modelling weaker [R44] | **6** |
| **Kotlin** | ✅ same route as Java [R31] | 🟡 same route and same caveats as Java [R21] | 🟡 Kotlin/Wasm is Beta and imposes a browser requirement [R36] | 🟡 reaches Spark's Java API through the JVM (inference) [R44] | **6** |
| **PHP** | ✅ Symfony or Laravel; the choice moves the window between 4 years and 2 [R28][R29] | 🟡 a binary only through a third-party project [R25] | 🟡 `php-wasm` exists and is active; the ❌ did not survive M5 (§6.1) [R42] | ❌ absent from Spark's and Polars' lists [R44][R45] | **8** |
| **Python** | ✅ Django, three years per release [R30] | 🟡 no cross-compilation [R26] | 🟡 Pyodide mature, full Web API access; size undocumented [R38] | ✅ the only one in both lists; the domain's reference ecosystem [R44][R45] | **5** |
| **Rust** | 🟡 no support calendar found for Axum or Actix; strengthened in M5 (§6.1) [R34][R65] | ✅ home domain; Tier 1 across operating systems [R27] | 🟡 the evidence does not establish the cell's value; kept as the least committal one (§6.1) [R40] | 🟡 implements Polars; training ecosystem not researched [R45] | **7** |
| **TypeScript** | ✅ mature but fragmented; Fastify ~a year, Express not found [R32][R33] | 🟡 Node SEA experimental; `deno compile` mature but a different runtime [R22][R23] | ✅ the browser is the native target; the only zero in this column [R39] | 🟡 Polars through Node.js, TensorFlow.js [R45][R46] | **4** ⬅ lowest |

### 3.1 How to read the table (as of 2026-08-23, after the adversarial pass)

**Ordering by weighted cost** (lower is better, range 0 to 30):

| # | Language | Computation | Weighted cost |
|---|---|---|---|
| 1. | **TypeScript** | 0×4 + 1×3 + 0×2 + 1×1 | **4** |
| 2. | **Python** | 0×4 + 1×3 + 1×2 + 0×1 | **5** |
| 3.–5. | **C#**, **Java**, **Kotlin** | 0×4 + 1×3 + 1×2 + 1×1 | **6** |
| 6. | **Rust** | 1×4 + 0×3 + 1×2 + 1×1 | **7** |
| 7. | **PHP** | 0×4 + 1×3 + 1×2 + 3×1 | **8** |
| 8. | **Go** | 0×4 + 0×3 + 3×2 + 3×1 | **9** |

*Ordering after the adversarial pass (§6.1, 2026-08-23). Before it PHP scored 12 and was last; once the unevidenced ❌ in the browser was dropped it scores 8 and Go is last. The leading pair did not change.*

**The §2.3 prediction failed, and not marginally.** I wrote that Go should rise. It finished seventh of eight. The reason is exactly the mechanism round 3 uncovered: **both of Go's zeros sit where zeros earn nothing.** Everyone scores zero in backend, so no ordering follows from it, and the second zero is in CLI. Meanwhile its two ❌ cells in the browser and in data pay full weight into the sum. The prediction failed because I reasoned about a candidate's strengths instead of about variance within columns. It stays recorded in §2.3 exactly as written, and this is its evaluation, not a correction.

**TypeScript leads so far, and it is the only candidate with a zero where nobody else has one** (§4.3, the browser). It pays only in CLI and in data.

**Three reasons this ordering must not yet be read as a verdict.**

1. **The leader is the candidate gate B2 fired against in round 1** (§4.5). Had the decider chosen to let the rule stand, today's leader would have been eliminated before anything was computed. The verdict's sensitivity to a single decision about a rule is thereby documented rather than assumed — and belongs in the verdict as an admitted premise.
2. **Four cells are marked uncertain** and go into M5 first: Rust in backend, Go and PHP in the browser, Rust in the browser. If the ❌ on Go in the browser failed to survive, Go would move from 9 to 7 or 5.
3. **The tie-breakers have no input yet.** C#, Java and Kotlin sit on an equal 6 and will be separated only by §4.1, §4.6 and §4.7 — strictness enforceable in CI, hiring pool, framework maturity.

## 4. Durable layer (carries the verdict)

### 4.1 Strictness that can be switched on and enforced (verified 2026-08-22)

"Does it handle types?" has no yes/no answer. Under rule M2 (§2.4) it breaks into five sub-questions, and **each has a different winner**. The decomposition runs across all eight equally — including the ones strictness is automatically assumed of.

#### (a) Is it enforced at runtime, or only at check time?

There are not two groups, as one would expect, but **three** — and the middle one is the one nobody talks about.

| Group | Who | Evidence |
|---|---|---|
| **Runtime enforces** | Java, Kotlin, C#, Go, Rust | A wrong type does not get through, because the runtime rejects it or you cannot reach it at all. **But each has an exception, see below.** |
| **Runtime enforces, per file only** | PHP | Types are checked at runtime — *"ensure that the value is of the specified type at call time, otherwise a `TypeError` is thrown"*. But strict mode is a **per-file** directive: *"Strict typing only applies to function calls made within the file with strict typing enabled. Callers without strict typing will still coerce values."* Without the directive PHP **coerces** — `sum(1.5, 2.5)` returns `int(3)` [R49]. |
| **No enforcement at all** | Python, TypeScript | Python: *"The Python runtime does not enforce function and variable type annotations. They can be used by third party tools such as type checkers, IDEs, linters, etc."* [R47] TypeScript: types are erased at compile time and the output is plain JavaScript [R39]. |

**The exceptions in that first group matter, and two of them are decisive:**

- **Java — generics are erased at runtime.** Type erasure replaces type parameters with their bounds or `Object`; `List<String>` is just `List` in the bytecode and *"generics incur no runtime overhead"*. The type safety of generics in Java is therefore **a matter of checking, not of running — exactly as in Python** [R55].
- **C# — nullability is not enforced at runtime at all.** The documentation says so plainly: *"The runtime behavior of your program is unchanged. Nullable reference types are entirely a compile-time feature."* [R50]
- **Kotlin — the hole is Java.** Nullability is part of the type system and the compiler enforces it, but calling Java code produces **platform types** carrying no nullability information, and that is one of the few ways to get an NPE in Kotlin [R52].
- **Go — no null safety.** `nil` is the zero value of pointers, slices, maps, channels, interfaces and functions, so an uninitialised variable of those types is `nil` and the language does not guard against it [R54].
- **Rust — the only one without that hole.** *"Rust doesn't have the null feature that many other languages have"*; instead `Option<T>`, where *"the compiler won't let us use an `Option<T>` value as if it were definitely a valid value"*, and a value allowed to be absent must be **explicitly opted into** [R53].

#### (b) What the type system can express

| Language | Nullability in the type system | Generics | Note |
|---|---|---|---|
| **C#** | Yes, via annotations and flow analysis [R50] | Yes, real at runtime | Two documented traps, see (c) |
| **Go** | No — `nil` is the zero value [R54] | Yes, since **Go 1.18** [R54] | |
| **Java** | Not in the language | Yes, but **erased** [R55] | |
| **Kotlin** | Yes, compiler-enforced [R52] | Yes (JVM, therefore erased) | Strongest nullability on the JVM |
| **PHP** | Partly (`?int`), at runtime | **None at all** — they do not exist in the language; they live only as comments for static analysis [R49] | The largest gap of the eight |
| **Python** | Yes in annotations, unenforced | Yes in annotations, unenforced | Everything rests on checking |
| **Rust** | No null; `Option<T>` [R53] | Yes | Strongest of the eight |
| **TypeScript** | Yes, `strictNullChecks` [R51] | Yes, erased | |

#### (c) How contagious an untyped dependency is, and where the escape hatch runs

- **Python — `Any` is contagious by definition.** *"A static type checker will treat every type as assignable to `Any` and `Any` as assignable to every type"*, and worse: *"no type checking is performed when assigning a value of type `Any` to a more precise type"* [R47]. One untyped library therefore silently switches off checking for everything flowing through it, and **nothing anywhere lights up red**.
- **C# — `!` and two traps.** The null-forgiving operator is described without varnish: *"Each occurrence is a place the compiler can no longer protect you."* Alongside it, two documented situations in which a non-nullable reference holds `null` **with no warning**: a struct created via `default`, and a new array of a reference type whose elements are `null` until assigned [R50]. On the other hand, since .NET 5 all .NET runtime libraries are annotated, so contagion from the ecosystem is smaller here than in Python [R50].
- **Kotlin** — the escape hatches are platform types from Java and `!!` [R52]. **PHP** — a caller in a file without the directive coerces [R49]. **TypeScript** — `any` and `@ts-expect-error`. **Java** — erasure and raw types [R55]. **Go** — `any` and type assertions. **Rust** — `unwrap()` and `unsafe`.

#### (d) Can it be enforced for everybody in CI, and is there a ratchet?

**And here is the direct answer to the question this document was proposed for: how much does mypy actually solve?**

`mypy --strict` switches on twelve optional checks including `--disallow-untyped-defs`, `--disallow-untyped-calls`, `--disallow-any-generics` and `--warn-return-any`. A ratchet against backsliding exists and is inside `--strict` itself: `--warn-unused-ignores` *"will make mypy report an error whenever your code uses a `# type: ignore` comment on a line that is not actually generating an error message"* [R48].

But **`--strict` itself marks where its guarantee ends**, and it is in its own description: *"strict will catch type errors as long as intentional methods like type ignore or casting were not used."* [R48] And one more thing that surprises: **`--disallow-any-explicit` is not part of `--strict`.** Strict mode therefore does not ban explicit `Any`; that has to be enabled separately.

Summary answer: **mypy solves (b), (d) and part of (c). It does not solve (a) at all and cannot.** A value arriving from JSON, from a database driver or from an untyped library enters as `Any` and mypy says nothing about it by design. It converts "types are documentation" into "types are checked at build time, for the code you own, minus explicit escapes" — which is a lot, but it is not "the runtime rejects a wrong value".

**The same decomposition applied to C#, as M2 requires.** Nullable reference types are *"entirely a compile-time feature"*, `!` disables protection occurrence by occurrence, and two documented traps produce `null` in a non-nullable reference without a word [R50]. On (a), C# stands with nullability **exactly where Python stands with types** — the difference being that the rest of its type system is enforced by the runtime.

**TypeScript** has `strict` as a family of switches offering *"stronger guarantees of program correctness"*, but the documentation attaches its own price: *"Future versions of TypeScript may introduce additional stricter checking under this flag, so upgrades of TypeScript might result in new type errors in your program."* [R51] Strictness that grows under your hands — for a decade-long project that is a cost, not a detail.

*PHPStan and Psalm levels for PHP were not researched in this round; the PHP cell on this point is therefore incomplete.*

#### (e) The cost on greenfield

The classic complaint about gradual typing — that it is bolted onto old code — **does not apply in this context** (§1: every project is new). On greenfield you can be strict from line one, and annotation coverage is a matter of discipline rather than migration. That strengthens Python and TypeScript more than the received wisdom about them suggests.

**But — and this is the whole difference — greenfield fixes coverage, not the enforcement boundary.** However strict the CI, point (a) stays where it was: in Python and TypeScript the runtime does not check types, so a wrong value from an unvalidated boundary passes inside and fails far from where it originated.

#### Consequence for the tie-breaker

Tie-breaker 1 (§2.3) is precisely "strictness enforceable in CI" and it decides the trio sitting on an equal weighted cost of 6. By the decomposition above the ordering is **Kotlin › C# › Java**: Kotlin has nullability in the type system and compiler-enforced, C# has it only as a compile-time matter with documented traps but its generics hold at runtime, and Java has neither — nullability is absent from the language and generics are erased.

### 4.2 Performance ceiling and concurrency model (verified 2026-08-22)

Performance is not a gate in this context (§1), so the question is not "which is faster" but **what happens when you need to do several things at once**. That is a durable property of a language, whereas a benchmark is a snapshot.

| Model | Who | Evidence |
|---|---|---|
| **Lightweight threads scheduled by the runtime** | Go, Java, Kotlin | Go: a goroutine *"is lightweight, costing little more than the allocation of stack space"* and goroutines are *"multiplexed onto multiple OS threads so if one should block, such as while waiting for I/O, others continue to run"* [R59]. Java since **JDK 21**: virtual threads, of which *"we can easily have a great many active virtual threads, even millions, running in the same Java process"* [R57]. |
| **Event loop plus explicit workers** | TypeScript (Node) | *"Workers (threads) are useful for performing CPU-intensive JavaScript operations. They do not help much with I/O-intensive work. The Node.js built-in asynchronous I/O operations are more efficient than Workers can be."* Stability 2 — Stable [R58]. |
| **A global lock, currently being removed** | Python | See below — the most interesting case of the eight. |
| **Cooperative concurrency only** | PHP | Fibers since **PHP 8.1** are interruptible functions with their own call stack [R60]; this is cooperative concurrency, not parallelism. |
| *Not researched in this round* | C#, Rust | `async`/`await` and `Task` for C#, `async` and threads for Rust were not researched — the cells are incomplete. |

**Fairness to Java, because this is easy to overstate.** The documentation itself warns how virtual threads should be read: *"Virtual threads are not faster threads; they do not run code any faster than platform threads. They exist to provide scale (higher throughput), not speed (lower latency)."* [R57] They address throughput while waiting on I/O, not a compute ceiling.

**Python and the GIL — the textbook case for rule M1.** The free-threaded build without the GIL has existed since **Python 3.13**, but it **is not the default**, and its documentation names two concrete costs. The ecosystem: *"Some third-party packages, in particular ones with an extension module, may not be ready for use in a free-threaded build, and will re-enable the GIL."* — one unprepared C extension therefore **switches the lock back on**. And single-threaded performance: *"the average overhead ranges from about 1% on macOS aarch64 to 8% on x86-64 Linux systems"* [R56].

That is exactly what M1 exists for: the feature has shipped, the ecosystem has not caught up, and the document has to say so instead of writing "Python no longer has a GIL".

### 4.3 What each of the four domains costs

**▸ CLI, daemons and automation (weight 3) — verified 2026-08-22**

One question decides here: **does my tool reach somebody else's machine without me first installing a runtime there?** The answer splits the eight more sharply than anything else in this document.

| Language | Standalone binary | Cross-compilation | Cost and caveats | Source |
|---|---|---|---|---|
| **C#** | Native AOT — self-contained, no installed .NET | 🟡 the source is silent about compiling across operating systems; the documentation states a binary produced on Linux runs on the *"same or newer Linux version"* | Requires a toolchain on the host (clang and zlib on Linux, the C++ workload in Visual Studio). Banned: dynamic assembly loading, `System.Reflection.Emit`, C++/CLI, built-in COM on Windows. Forces trimming. `System.Linq.Expressions` always runs interpreted. *"Not all the runtime libraries are fully annotated to be Native AOT compatible."* | [R20] |
| **Go** | Yes, by default | ✅ to any target from any host | Home domain. The documentation puts it plainly: *"In effect, you are always cross-compiling."* There are over twenty OS-and-architecture combinations. | [R24] |
| **Java** | Via GraalVM Native Image — *"Starts in milliseconds"*, no installed JVM | 🟡 not researched in this round | **Closed-world assumption.** The analysis is static and *"does not run your application"*, so it *"cannot always exhaustively predict all usages of the Java Native Interface (JNI), Java Reflection, Dynamic Proxy objects, or class path resources"* — the gaps are hand-written into JSON metadata. In an ecosystem built on reflection that is a recurring cost, not a one-off. Without a native image the target machine needs a JVM. | [R21] |
| **Kotlin** | Same route as Java (JVM + GraalVM) | 🟡 not researched in this round | The same caveats as Java [R21]. Kotlin/Native as a second route was not researched in this round. | [R21] |
| **PHP** | Via `static-php-cli` — a statically linked binary with no system PHP | 🟡 Linux, macOS and FreeBSD locally; Windows only through GitHub Actions | The crucial difference from the others: **it is not an official tool of the language** but a third-party project (MIT, by crazywhalecc). Supports PHP 8.2–8.5. Library maturity for long-running daemons and system automation was not researched in this round — the rating rests on distribution alone for now. | [R25] |
| **Python** | Via PyInstaller, one-file mode | ❌ *"PyInstaller does not support cross-compilation"* — the build must be run on each target OS and Python version | One-file unpacks into a temporary folder on every start, which slows launch compared with one-folder. On machines that already have Python none of these costs arise — so this is a cost of distribution, not of writing. | [R26] |
| **Rust** | Yes, by default | ✅ Tier 1 covers Linux, macOS and Windows on x86-64 and ARM64, with official builds and automated tests after every change | Home domain. Tier 1 means *"Guaranteed to work"*, Tier 2 *"Guaranteed to build"*. | [R27] |
| **TypeScript** | Two routes, both working, each with a different price | ✅ via `deno compile` (Windows, macOS, Linux × x64 and ARM64) | **Node SEA** is *"Stability: 1.1 - Active development"*, `require()` and `import` in the injected script load only built-in modules, cross-platform builds require disabling both `useCodeCache` and `useSnapshot`, macOS x64 is not tested, and on Linux arm64 in Docker there is a known crash in `process.dlopen()`. **`deno compile`** is considerably more mature and bundles a slimmed runtime — but choosing Deno means choosing a different runtime from Node, a fork inside the same language. | [R22][R23] |

**What follows.** Go and Rust are the only ones where distribution costs **nothing** — the binary is the default build output and cross-compilation is a property of the language rather than an add-on. Everybody else has to buy the standalone binary: C# and Java with a toolchain and restrictions on dynamic features, PHP with a dependency on a third-party project, Python by giving up cross-compilation, TypeScript by choosing between an experimental route and a different runtime.

This **confirms the part of the §2.3 prediction that concerned Go** — but for a different reason than I wrote. I did not predict cross-compilation; I predicted "home domain" in general terms. The evidence is more specific than the prediction, and it supports Rust just as strongly, which the prediction did not mention in this domain at all.

**▸ Web backend and API (weight 4) — verified 2026-08-22**

Whether a language "can do" backend does not matter here — all eight can. Something else decides, and it is durable: **in this domain the lifecycle binding you is the framework's, not the language's, and for most candidates it is markedly shorter.** You therefore have two windows to track, not one.

| Language | Main framework | Framework support window | How many windows to track | Source |
|---|---|---|---|---|
| **C#** | ASP.NET Core — part of .NET, from the same vendor | Identical to .NET: LTS 36 months | **One** — framework and language share a calendar | [R9] |
| **Go** | `net/http` in the **standard library** | None separate; covered by the Go 1 compatibility promise | **None extra** — the only one of the eight with no second calendar at all | [R8] |
| **Java** | Spring Boot | Minor *"at least 12 months"*, major *"at least 3 years"*; a new release every six months (May and November) | Two | [R31] |
| **Kotlin** | Spring Boot (Ktor not researched in this round) | The same figures as Java | Two | [R31] |
| **PHP** | Symfony **or** Laravel — and the difference between them is twofold | Symfony LTS: 3 years of fixes + **4 years of security**. Laravel: 18 months of fixes + **2 years of security** | Two, and the framework choice doubles your window or halves it | [R28][R29] |
| **Python** | Django | Three years; from the 2028 release **every** feature release gets the same three years, not only LTS | Two | [R30] |
| **Rust** | Axum | A dated support policy was **not found** in the repository root nor in the `axum` crate directory (positive control passed — `Cargo.toml` appeared in both listings) | Two, one of them with no published calendar | [R34] |
| **TypeScript** | Fastify, Express and others — the layer is fragmented | Fastify: a minimum of six months plus six more after the next major, so roughly a year. Express: policy **not found** — and I admit this conclusion is weak, because the positive control on the documentation repository failed (see [R33]) | Two | [R32][R33] |

**A finding I did not expect, and it changes how §2.3 reads.** Backend carries the highest weight (4), yet it is **the least discriminating column in the whole document** — seven of eight candidates sit at the same level. And because weighted cost is cell cost times weight, a domain where everyone scores alike contributes **alike to everyone**, and therefore does not order the field at all. High weight by itself produces no influence; **variance within the column** does.

Practically, this means the verdict will not be decided by backend at weight 4 but by **CLI at weight 3**, where the cells genuinely differ (§4.3 above). That runs counter to the intuition the weights were set with, and it is a consequence of rule §2.3 rather than a breach of it — the rule does not change, it simply shows how it behaves.

The only candidate backend separates is **Rust**, and its 🟡 rests for now on a single axis (no published support calendar for Axum). Ecosystem breadth for authentication, ORM and admin was not researched in this round, so **this cell is marked uncertain and queued first for the adversarial pass** (M5).

**▸ Web frontend in the browser (weight 2) — verified 2026-08-22**

The one domain where a single candidate has an advantage the others cannot take from it: **the browser is TypeScript's native target, not its export market.** The other seven reach the browser through WebAssembly or transpilation, and each pays with something different.

| Language | Route to the browser | Documented cost | Source |
|---|---|---|---|
| **C#** | Blazor WebAssembly, first-party | *"The Blazor app, its dependencies, and the .NET runtime are downloaded to the browser"* — the runtime therefore travels to the browser. Mitigations are documented: Webcil packaging, IL trimming on every Release build, static Brotli and Gzip compression. A concrete trap: the default `EmccMaximumHeapSize` is 2 GB and on Safari on iOS it may need lowering, or the app crashes. | [R35] |
| **Go** | `GOOS=js GOARCH=wasm`, an official target | *"Go generates large Wasm files, with the smallest possible size being around ~2MB"* and *"10MB+ is common"*. The `wasm_exec.js` file must come from the **same major version** of the compiler — *"Other combinations are not supported."* TinyGo reaches ~10 kB, but it is a different compiler with different subset behaviour. | [R37] |
| **Java** | TeaVM — *"an ahead-of-time compiler for Java bytecode that emits JavaScript and WebAssembly that runs in a browser"* | A third-party project, not an official route of the language. Concrete limitations and output sizes are not documented on the landing page — **a gap in the evidence**, so the rating rests only on the route existing and being active. | [R41] |
| **Kotlin** | Kotlin/Wasm, first-party, plus Compose Multiplatform | **Beta status** per its own documentation. Requires *"a browser version that supports WebAssembly's garbage collection and legacy exception handling proposals"* — a condition on the visitor's side. Kotlin/JS as a second route was not researched in this round. | [R36] |
| **PHP** | `php-wasm` | Clearly the thinnest route of the eight: a third-party project under Apache-2.0, effectively one maintainer. Covers PHP 8.0–8.5, with DOM binding through a separate package. It exists and is active — but writing a user interface in it is not the same as being able to run PHP in a browser. | [R42] |
| **Python** | Pyodide — *"a port of CPython to WebAssembly/Emscripten"* | More mature than expected: *"Any pure Python package with a wheel available on PyPi is supported"*, including NumPy, pandas, SciPy and scikit-learn, plus a two-way interface to JavaScript and *"full access to the Web APIs"*. **The download size of the runtime could not be documented** — the page carrying the figures returned 403, so no number is claimed. | [R38] |
| **Rust** | `wasm32`, plus frameworks outside the standard library | The documented signal is unpleasant but narrow: the official Rust and WebAssembly working-group book carries the notice *"This project and website is no longer maintained."* **Mind the scope — that is about the book and the website, not about the target platform or the frameworks**, which were not researched. The cell therefore rests on incomplete evidence. | [R40] |
| **TypeScript** | None — the browser **is** the target | *"TypeScript is JavaScript's runtime with a compile-time type checker"*; types are erased at compile time and the output is plain JavaScript which *"is **guaranteed** to run the same way"*. Cost zero, and it is the only zero in this column. | [R39] |

**What follows.** The frontend is the mirror image of CLI: there Go and Rust cost nothing, here only TypeScript does. And because §2.3 sums weighted costs, the verdict turns on whether a zero in CLI (weight 3) is worth more than a zero in the browser (weight 2) — which at the given weights favours CLI, but not by enough to settle it without argument.

**Three cells in this column are marked uncertain and sent to the adversarial pass (M5):** the ❌ on Go (it rests on documented sizes, but TinyGo is an unexamined escape hatch), the ❌ on PHP (it rests on ecosystem thinness, which is a judgement rather than a measurement) and the 🟡 on Rust (the evidence is narrow and concerns documentation, not the platform).

**▸ Data, ML and batch processing (weight 1) — verified 2026-08-22**

The domain is really three different jobs, each with a different winner, which the shorthand "data means Python" conceals. I rated it against two reference tools whose supported-language lists are **enumerated** in the documentation, so absence can be read from them.

- **Apache Spark** (batch processing): *"It provides high-level APIs in Java, Scala, Python and R"*; the native implementation language is Scala [R44].
- **Polars** (dataframes): *"an analytical query engine for DataFrames, written in Rust"*, with bindings for *"Python, Rust, Node.js, R, and SQL"* [R45].

From those two lists the split follows: **Python is in both. Java is in Spark. Rust implements Polars. TypeScript reaches Polars through Node.js and adds TensorFlow.js for browser and Node [R46]. C# has its own first-party ML.NET, used according to Microsoft in Power BI, Defender, Outlook and Bing, but positioned as an integrator of TensorFlow and ONNX rather than their replacement [R43]. Go and PHP are in neither list.**

| Language | Documented position | Source |
|---|---|---|
| **C#** | ML.NET, first-party and proven in production; absent from Spark's and Polars' lists | [R43][R44][R45] |
| **Go** | Not in Spark's or Polars' language list | [R44][R45] |
| **Java** | First class in Spark for batch processing; modelling weaker | [R44] |
| **Kotlin** | Reaches Spark's Java API through the JVM *(inference — Kotlin itself is not named in the list)* | [R44] |
| **PHP** | Not in Spark's or Polars' language list | [R44][R45] |
| **Python** | The only language present in both lists; the domain's reference ecosystem | [R44][R45] |
| **Rust** | Implements Polars. The model-training ecosystem was not researched in this round | [R45] |
| **TypeScript** | Polars binding through Node.js; TensorFlow.js for browser and Node | [R45][R46] |

**The scope of this rating is deliberately narrow.** It rests on two tools rather than a survey of the domain, and absence from a list means absence **from that list** — not that data cannot be processed in the language. At weight 1 that is a proportionate investment; had the domain weighed more, this basis would not be enough.

### 4.4 Who pays for the ecosystem (verified 2026-08-22)

The question for gate B2 is not "is it open source" but **who pays the people who maintain it**. Across the eight the answer splits into three different models, and that difference is more durable than any language feature.

| Language | Who pays for and directs development | Model | Source |
|---|---|---|---|
| **C#** | Microsoft. The .NET Foundation is explicitly an organisation for **community projects** around the platform, not for developing .NET itself — Microsoft directs that | corporate | [R10] |
| **Go** | Google — the "standard" `gc` compiler and toolchain are maintained by *"the Go team at Google"* | corporate | [R7] |
| **Java** | Oracle (OpenJDK) plus the Eclipse Adoptium working group: strategic members Alibaba, IBM, Microsoft; enterprise members Fujitsu, Bloomberg, Canonical, Red Hat | mixed: company + foundation | [R11][R12] |
| **Kotlin** | The Kotlin Foundation, founded by **JetBrains and Google**; further members Meta, Gradle, Touchlab, Uber, Kotzilla, Block. Its declared tasks include *"Control incompatible changes to the language"* and *"Preserve the Kotlin trademarks"* | foundation, two dominant founders | [R13] |
| **PHP** | The PHP Foundation — it **contracts ten developers** part-time and full-time; platinum sponsors JetBrains, Automattic, Sovereign Tech Agency, gold Laravel, GoDaddy, team.blue | foundation, broad sponsor base | [R3] |
| **Python** | The Python Software Foundation — holds the intellectual property of most releases and the trademarks, employs a *"CPython Developer in Residence"* | foundation | [R5] |
| **Rust** | The Rust Foundation — founding platinum members AWS, Google, Huawei, Meta, Microsoft, Mozilla (January 2021), over 50 organisations | foundation, broad corporate base | [R15] |
| **TypeScript** | Microsoft | corporate | [R17][R18] |

**What this means for a decade-long bet.** On the "payer" half, gate B2 filtered out **nobody** — all eight have a traceable financier. The difference is what it rests on: for Go, TypeScript and C# a single company; for Kotlin a foundation with two dominant founders; for PHP, Python, Rust and Java a broader base. This is not a quality judgement — neither Microsoft nor Google is walking away from those languages tomorrow — but it is a different kind of risk, and it belongs in the durable layer because it does not change with a version.

*Note on sources: the official Oracle Java SE Support Roadmap page returned HTTP 403 on 2026-08-22 and could not be read. The Java entries therefore rest on Eclipse Adoptium [R11][R12], which is in any case more relevant for this context — a free distribution rather than Oracle's paid support.*

### 4.5 Support commitments and backwards compatibility (verified 2026-08-22)

| Language | Support length per version | Concretely as of 2026-08-22 | Backwards-compatibility promise | Source |
|---|---|---|---|---|
| **C#** | LTS 36 months (even numbers), STS 24 months (odd); a new major every November | .NET 10 (LTS) to 2028-11-14; .NET 8 and 9 to 2026-11-10 | — not researched in this round | [R9] |
| **Go** | Until **two newer** majors ship — at a cadence of two releases a year, roughly a year *(inference from the policy and the observed cadence)* | Go 1.27.0 released 2026-08-19 | **Go 1 compatibility promise:** *"programs written to the Go 1 specification will continue to compile and run correctly, unchanged, over the lifetime of that specification"* — at source level, with ten enumerated exceptions; binary compatibility is not guaranteed | [R6][R7][R8] |
| **Java** | Adoptium: one LTS **every two years** since 2021, supported *"for at least four years"*, free | JDK 25 at least to 2031-09 · JDK 21 at least to 2029-12 · JDK 17 at least to 2027-10 | — not researched in this round | [R11] |
| **Kotlin** | No dated LTS table. On the JVM it supports **at least three previous language and API versions** alongside the latest stable | — | A newer compiler reads older binaries; incompatible changes go through a two-phase deprecation cycle; the `-language-version` and `-api-version` flags emulate older behaviour | [R14] |
| **PHP** | 2 years of active support + 2 years of security fixes = **4 years** | 8.4 security to 2028-12-31 · 8.5 to 2029-12-31 · 8.2 ends 2026-12-31 | — not researched in this round | [R2] |
| **Python** | PEP 602: ~2 years of bugfixes + ~3 years of security = **5 years**, *"Five years after a release, support ends"* | The longest window of the eight | — not researched in this round | [R4] |
| **Rust** | No dated LTS table | — | The strongest wording of the eight: *"once a feature is released through stable, contributors will continue to support that feature for all future releases"*. Incompatible changes go into **editions**, which are opt-in and **fully interoperable with each other** — every crate migrates independently | [R16] |
| **TypeScript** | ⚠️ corrected in §8: a policy **does** exist, but it is conditional on being shipped inside a Microsoft product and gives versions no calendar of their own | — | — not researched in this round | [R17][R18][R66] |

**Two things this table revealed that I did not expect.**

**First: "support" means something different for a compiler than for a runtime, and gate B2 does not distinguish them.** For PHP, Python, Java and .NET, support is an obligation ticking on a clock — an unpatched version is a security debt exposed to the internet. For Go, Rust, Kotlin and TypeScript the load-bearing commitment is instead the **compatibility promise**: old code keeps compiling and the artifact keeps running. Rust's wording (a feature released as stable stays supported in all future releases) is materially a stronger decade-long commitment than any dated LTS table, despite Rust having no such table. Go's short support window is therefore **not** the weakness the table makes it look at first glance — it is the other model, where you upgrade often but cheaply.

**Second: TypeScript alone has no commitment, and this is documented by a primary source rather than an empty search.** ⚠️ **This claim was corrected as false on 2026-08-23 — see §8. A policy does exist, it is merely conditional. The paragraph below is left in its original wording so that what was corrected remains visible.** In issue microsoft/TypeScript #49088 ("Document TypeScript version lifetime and EOL", state: closed), Ryan Cavanaugh of the TypeScript team replies: *"To my knowledge, we don't have an official policy beyond the one implied by the fact that we ship our components in Visual Studio. Security fixes are backported I believe for the last year of releases; non-security fixes are not backported."* [R18] The wording is reproduced with its own hedge ("I believe") — the source is not certain and the document must not harden it.

Mind the scope of that claim, though: **it concerns the compiler, not the runtime.** TypeScript code runs on Node.js or in a browser, and the lifecycle belongs to that runtime — Node.js holds a **30-month** LTS [R19]. "TypeScript has no LTS" therefore does not mean "a TypeScript application has no supported runtime"; it means the compiler you run at build time carries no commitment.

**Outcome of gate B2 (recorded 2026-08-22; ⚠️ on 2026-08-23 it turned out it should not have fired — §8).** The rule reads: no identifiable payer **or** no documented commitment to long-term support → eliminated. All eight have a payer (§4.4). Seven of eight have a support commitment — either a dated table (C#, Java, PHP, Python) or a compatibility promise (Go, Kotlin, Rust). **The eighth, TypeScript, has none according to its own team's statement, and gate B2 therefore fired against it.**

The decision about what to do **is not mine and will not be taken quietly**: B2 turned out to be an instrument measuring something different for compilers than for runtimes, and that is a defect in the rule's design, not in the facts underneath it. The rule therefore stays recorded exactly as it was, together with the note that it fired. Any amendment will be recorded as **post-hoc, with a date and a reason** — not as if it had been there all along.

### 4.6 Hiring pool, handover, onboarding (verified 2026-08-22)

This axis carries full weight because of the second role in §1 — recommending inside companies. A company does not adopt a language, it adopts its hiring pool.

**The durable part** (the specific percentages are perishable and live in §5): the differences between the eight are not measured in percentage points but in **orders of magnitude**. In three bands: TypeScript and Python with the broadest base; C#, Java and PHP in the middle; Go, Rust and Kotlin narrowest, with **Kotlin the smallest of the eight** [R61].

**And here a tension arises that the verdict must resolve rather than conceal.** Tie-breaker 1 (strictness, §4.1) ordered the trio on cost 6 as Kotlin › C# › Java. Tie-breaker 2 (hiring) orders it **exactly the other way** — C# and Java have roughly three times Kotlin's base. Rule §2.3 fixes the tie-breaker order in advance, so **Kotlin still wins**; but for the consulting role that is a result running against what a company would want to hear. The verdict must state it as an admitted consequence of the rule, not hide it.

*Source limitation: this is a voluntary poll of one community rather than a measurement of the labour market, and "uses the language" is not the same as "can be hired for it". Data specific to the Czech Republic were not researched in this round.*

### 4.7 Maturity of frameworks and libraries (verified 2026-08-22)

The evidence is already in §4.3, where it was gathered for the domains. Condensed onto one axis:

- **Most mature and most coherent:** C# (ASP.NET Core first-party, one calendar with the language), Java and Kotlin (Spring Boot), PHP (Symfony and Laravel, both with their own dated support policy), Python (Django).
- **Least fragmented:** Go — the web layer is in the standard library, so a "framework" as a separate dependency with its own lifecycle never arises here [R8].
- **Most fragmented:** TypeScript. The framework layer is wide and has no shared policy — Fastify's LTS runs about a year [R32], and no policy could be found for Express [R33]. The ecosystem is the largest of the eight and simultaneously the least coordinated; for a decade-long bet it is both at once.
- **Thinnest in two of four domains:** Rust (no dated calendar found for Axum [R34]) and PHP outside the web.

### 4.8 Summary properties table (evidence — does not carry the verdict, verified 2026-08-22)

The table a reader asks for first: concrete properties, language by language. **The verdict does not follow from it** — §3 issues that, under rule §2.3. This summarises what §4.1 to §4.7 established and serves as input to the tie-breakers. If it pointed somewhere other than §3, §3 holds and the disagreement is recorded.

*Departure from the intent stated in the skeleton (2026-08-22): the table was originally to contain only the leading candidates so it would not be wide. In the end all eight are here — dropping PHP and Go from a reference table would remove exactly the comparison the reader wanted it for. The price is nine columns, which scroll on a narrow screen.*

Languages are **in columns** here (in §3 they are in rows); the ordering stays alphabetical as everywhere (§2.1).

| Property | C# | Go | Java | Kotlin | PHP | Python | Rust | TypeScript |
|---|---|---|---|---|---|---|---|---|
| **▸ Strictness** | | | | | | | | |
| Types enforced at runtime | ✅ | ✅ | ✅ | ✅ | 🟡 per file | ❌ | ✅ | ❌ |
| Nullability in the type system | 🟡 compile time only | ❌ `nil` | ❌ | ✅ | 🟡 `?int` | 🟡 annotations only | ✅ `Option<T>` | ✅ `strictNullChecks` |
| Generics real at runtime | ✅ | ✅ since 1.18 | ❌ erased | ❌ erased | ❌ none at all | ❌ annotations only | ✅ | ❌ erased |
| Main escape from strictness | `!` and `default` structs | `any`, assertions | erasure, raw types | platform types from Java | a file without the directive | `Any` | `unwrap`, `unsafe` | `any` |
| **▸ Ergonomics** | | | | | | | | |
| get/set properties as a language feature | ✅ [R62] | — | — | ✅ [R63] | ✅ since 8.4 [R1] | ✅ `@property` [R64] | — | — |
| **▸ Operations and ecosystem** | | | | | | | | |
| Concurrency model | `async`/`Task` *(not res.)* | goroutines | virtual threads (JDK 21) | coroutines + JVM | cooperative only (Fibers 8.1) | GIL; build without it since 3.13, not the default | `async` + threads *(not res.)* | event loop + workers |
| Standalone binary without a runtime | 🟡 Native AOT | ✅ default | 🟡 GraalVM | 🟡 GraalVM | 🟡 third party | 🟡 PyInstaller | ✅ default | 🟡 SEA / `deno compile` |
| Cross-compilation | 🟡 source silent | ✅ | 🟡 not res. | 🟡 not res. | 🟡 partly | ❌ | ✅ | ✅ via Deno |
| Language support window | 36 mo LTS | ~1 year + compatibility promise | ≥4 years (Adoptium) | no table | 4 years | 5 years | no table | none |
| Framework support window | same as language | none extra | ≥12 mo minor | ≥12 mo minor | 2–4 years by choice | 3 years | not found | ~1 year / not found |
| Hiring base (§5.1) | 29.9 % | 17.4 % | 29.6 % | 11.5 % | 19.1 % | 54.8 % | 14.5 % | 48.8 % |

**On the three columns from the original brief.** The table that inspired this document had three columns: *requires variable declaration*, *forbids global variables* and *supports get/set properties*. The third is above and is sourced. **The first two are deliberately absent**, and that follows from the rule this table imposed on itself: only a property wired to a decision rule or a tie-breaker belongs here. Neither variable declaration nor a ban on globals is wired to any rule in §2 — and the question they were originally proxying for, *"how much does the language stop me making a mistake by itself"*, is answered elsewhere and far more precisely: in §4.1 point (a), where it turned out that the **enforcement boundary** decides, not the presence of a syntactic rule.

**And one more correction to the original table.** It filed *get/set properties* among strictness properties, where Java scored badly. But those are two different axes: properties are ergonomics, not correctness, and Java is not less safe for lacking them — as the "Types enforced at runtime" row shows, where Java has ✅ and Python and TypeScript do not.

## 5. Dated layer (snapshot as of 2026-08-22 — ages quickly)

**Does not carry the verdict.** When this section goes stale, §1 to §4 still hold.

### 5.1 Hiring base (Stack Overflow Developer Survey 2025)

The share of **professional developers** listing the language among those they use [R61]. The ordering is alphabetical as in every table in this document (§2.1), not by share — the highest is Python, followed by TypeScript:

| Language | Share |
|---|---|
| **C#** | 29.9 % |
| **Go** | 17.4 % |
| **Java** | 29.6 % |
| **Kotlin** | 11.5 % |
| **PHP** | 19.1 % |
| **Python** | 54.8 % |
| **Rust** | 14.5 % |
| **TypeScript** | 48.8 % |

*(For context outside the eight: JavaScript 68.8 %.)* The survey is the **2025 edition**, read in August 2026 — a newer edition may exist and was not checked. It is a voluntary poll, not a measurement of the labour market.

### 5.2 Current versions and support dates

| Language | Status as of 2026-08-22 | Source |
|---|---|---|
| **C#** | .NET 10 (LTS) supported to 2028-11-14; .NET 8 and 9 to 2026-11-10 | [R9] |
| **Go** | Go 1.27.0 released 2026-08-19; support always covers only the two newest majors | [R6] |
| **Java** | Adoptium: JDK 25 at least to 2031-09, JDK 21 to 2029-12, JDK 17 to 2027-10 | [R11] |
| **Kotlin** | No dated support table; on the JVM at least three previous language and API versions | [R14] |
| **PHP** | 8.5 security to 2029-12-31; 8.4 to 2028-12-31; 8.2 ends 2026-12-31 | [R2] |
| **Python** | Five-year window per release; free-threaded build since 3.13, not the default | [R4][R56] |
| **Rust** | No dated support table; editions opt-in and mutually interoperable | [R16] |
| **TypeScript** | No official support policy; the Node.js runtime holds a 30-month LTS | [R18][R19] |

### 5.3 Frameworks

| Framework | Support window | Source |
|---|---|---|
| Symfony (LTS) | 3 years of fixes + 4 years of security | [R28] |
| Django | 3 years; from the 2028 release on every feature release | [R30] |
| ASP.NET Core | same as .NET, LTS 36 months | [R9] |
| Laravel | 18 months of fixes + 2 years of security | [R29] |
| Spring Boot | minor at least 12 months, major at least 3 years | [R31] |
| Fastify | ~12 months (6 + 6 after the next major) | [R32] |

## 6. Adversarial pass and verdict

### 6.1 Adversarial pass (M5, 2026-08-23)

The brief for this pass was to **refute**, not to confirm. It went at the four cells marked uncertain and at the conclusion itself.

**A limitation that must be admitted:** the pass ran **in the same context that produced the conclusion**, not a separate one. The codex recommends a fresh context precisely because an author refutes their own arguments worse than a stranger does. This pass is worth less for it, and the reader should know.

| Cell | Outcome | What happened |
|---|---|---|
| **Rust in backend** (🟡) | **Survived, and is better grounded** | The objection was an uneven yardstick: for TypeScript I searched two frameworks for a support policy, for Rust only one. Filled in by the same method — Actix-web has no dated support calendar in its root or in `.github`, positive control passed (`Cargo.toml` in the listing) [R65]. Two out of two publish nothing, whereas for TypeScript one of two does (Fastify). The difference is real; the 🟡 holds. |
| **Go in the browser** (❌) | **Survived with a caveat** | The figures are from Go's own wiki and cannot be disputed. But that same wiki recommends compression and mentions TinyGo at ~10 kB, and **I examined neither**. The ❌ therefore rests on the uncompressed floor and on an unexamined escape hatch. If it fell to 🟡, Go moves from 9 to 7. |
| **PHP in the browser** (❌) | **DID NOT SURVIVE — lowered to 🟡** | The argument was "thin, effectively one maintainer". That is a **judgement, not a measurement**, and it could not be sourced. `php-wasm` meanwhile exists, is active and covers PHP 8.0–8.5 [R42]. Under the rule that inference must not wear a fact's clothes, the ❌ is dropped. **Impact: PHP from 12 to 8, overtaking Go, and Go is now last.** |
| **Rust in the browser** (🟡) | **The evidence does not establish the value** | The only evidence was the working group's unmaintained website, which says nothing about the target platform or the frameworks. The cell stays 🟡 as the least committal value, but it **is not established** and the document says so instead of covering it up. |

**And now the strongest objection I have — it is aimed at the leader and cannot be waved away.**

Weighted cost measures **fit against the four domains and nothing else.** The durable layer §4.4 to §4.7 does not enter the score at all; it gets a word only through the tie-breakers, and those fire only on a tie. An uncomfortable consequence follows: **TypeScript's greatest weakness — that no support commitment exists for the compiler, which is exactly what gate B2 fired on in round 1 — is structurally invisible in the score.**

This is not a breach of the rule. The rules were written this way in advance and are not rewritten after the result. But it means **the number 4 is not the whole truth**, and the verdict must say so aloud rather than tuck it into a footnote.

A second objection of the same kind: the leading pair, TypeScript and Python, are **both in the group that does not enforce types at runtime** (§4.1 point a). The chosen weights select for breadth, and breadth in 2026 means precisely those two languages.

### 6.2 Verdict (2026-08-23)

**Under rule §2.3 the verdict is TypeScript** with a weighted cost of 4, ahead of Python at 5.

**What you pay for it — the accepted trade-offs, itemised rather than gestured at:**

1. **No support commitment for the compiler.** The TypeScript team itself states no official policy exists (§4.5). The lifecycle you lean on is the **runtime's** — Node.js with its 30-month LTS. This is the trade-off that would otherwise have failed you at gate B2, and you accept it knowingly.
2. **Types are not enforced at runtime.** They are erased at compile time and the output is plain JavaScript (§4.1). Protection ends at the boundary where data enters from outside; validating that boundary is your work, not the language's. For somebody who framed this whole document around strictness, it is the most expensive line on the bill.
3. **The most fragmented framework layer of the eight** (§4.7). The largest ecosystem and simultaneously the least coordinated — Fastify's window is about a year, and no policy could be found for Express.
4. **CLI is paid for with a choice** (§4.3): either the experimental Node SEA, or `deno compile`, meaning a different runtime from Node. At weight 3 it is the verdict's second most expensive line.

**What you get for it:** the only candidate covering the browser without a tax (§4.3), the second-broadest hiring base (§5.1), and zero cost in the highest-weighted domain.

**Runner-up: Python (5).** It wins data, where TypeScript has 🟡, and loses the browser. It suffers the same weakness as point 2 — the runtime does not enforce types — plus the GIL, whose removal has shipped but whose ecosystem has not caught up (§4.2).

**I will change my mind if** — and this is falsification, not an alibi:

- **Runtime type enforcement is worth more to you than breadth of coverage.** Then it is not the numbers that are wrong but the weights: they selected for breadth, and in 2026 breadth leads to two languages that do not check types at runtime. Under different weights the answer is Kotlin, C# or Rust. You set the weights before the research, and rewriting them now would destroy the only property that makes writing them in advance worth anything — but deciding to change them and **rerunning the computation with a date** is legitimate, provided it is recorded as a new brief rather than a correction.
- **The browser domain leaves your brief.** TypeScript's zero is only there; without the frontend it falls to 3, but Go drops from 9 to 3 and Rust from 7 to 5 — the whole ordering reshuffles.
- **The ❌ on Go in the browser falls** (§6.1). On its own that does not change the verdict, but it narrows the gap.

### 6.3 Verdict by domain and sensitivity to the weights (2026-08-23)

One verdict answers one question — "what if my brief differs from yours?" is a different question and deserves its own answer. Both of the below are **readings of the matrix in §3**, not new claims: not a single source was added.

#### By domain — bands, not rankings

**Why bands and not first, second and third choice.** The matrix holds three values, not an ordering. In backend, seven of eight candidates sit on ✅, which is **not** first through seventh place but a seven-way tie. Ordering them would mean inventing differences the document never measured — exactly the ranking-without-a-loser that §3 avoids.

| Domain | Pays nothing | Pays | Pays most |
|---|---|---|---|
| **Backend and API** (×4) | C#, Go, Java, Kotlin, PHP, Python, TypeScript | Rust | — |
| **CLI and automation** (×3) | Go, Rust | C#, Java, Kotlin, PHP, Python, TypeScript | — |
| **Frontend in the browser** (×2) | TypeScript | C#, Java, Kotlin, PHP, Python, Rust | Go |
| **Data, ML, batch** (×1) | Python | C#, Java, Kotlin, Rust, TypeScript | Go, PHP |

It reads like this: **if you were deciding on one domain alone**, in backend you would pick almost anything, in CLI Go or Rust, in the browser TypeScript, and in data Python. The verdict in §6.2 answers what to do when you need **one language for all four at once** — and that is a different question from any row of this table.

#### Sensitivity to the weights — several verdicts, each with its own brief

The same cells, different weights. The weights column reads backend · CLI · frontend · data.

| Brief | Weights | Winner | Ordering |
|---|---|---|---|
| **Your brief (§2.3)** | 4 · 3 · 2 · 1 | **TypeScript** (4) | TS 4, Python 5, C# 6, Java 6, Kotlin 6, Rust 7, PHP 8, Go 9 |
| All domains equal | 1 · 1 · 1 · 1 | **Python + TypeScript** (2) | Python 2, TS 2, C# 3, Java 3, Kotlin 3, Rust 3, PHP 5, Go 6 |
| Without the browser | 4 · 3 · 0 · 1 | **Go + Python** (3) | Go 3, Python 3, C# 4, Java 4, Kotlin 4, TS 4, Rust 5, PHP 6 |
| Without data and ML | 4 · 3 · 2 · 0 | **TypeScript** (3) | TS 3, C# 5, Java 5, Kotlin 5, PHP 5, Python 5, Go 6, Rust 6 |
| Backend only | 1 · 0 · 0 · 0 | **seven-way tie** (0) | everything except Rust 0, Rust 1 |
| Browser highest | 2 · 3 · 4 · 1 | **TypeScript** (4) | TS 4, Python 7, Rust 7, C# 8, Java 8, Kotlin 8, PHP 10, Go 15 |
| Data highest | 2 · 1 · 3 · 4 | **Python** (4) | Python 4, TS 5, C# 8, Java 8, Kotlin 8, Rust 9, PHP 16, Go 21 |

#### What follows

**TypeScript's win is robust to everything except one change.** It wins three of seven briefs, shares first in one more and never drops below second — with a single exception: **the moment the browser leaves the requirements it falls to fourth, behind Go and Python.** That is its entire claim and simultaneously its only vulnerability. Anyone who does not need the browser has a completely different verdict.

**The least stable candidate in the whole document is Go.** It swings between last place (9 at the given weights, 15 and 21 under two others) and **joint first** (3 without the browser). No other candidate moves like this. It means the claim "Go is a poor choice for this profile" holds **strictly because of the browser and data** — in both of the highest-weighted domains it sits on zero.

**The "backend only" row is proof of the round 3 finding.** A seven-way tie at zero shows in black and white that the highest-weighted domain does not order the field: variance within a column produces influence, not the column's weight.

**Python is the most robust candidate.** It wins or shares first in three briefs and never drops below fifth. Anyone who does not know what their weights will be in five years buys the least risk with Python — an argument that cannot appear in the verdict under the given weights, because that one scores a single specific brief rather than resilience across briefs.

**Scope of validity.** The verdict holds for the profile in §1: **new greenfield projects**, four domains weighted 4 · 3 · 2 · 1, performance as a soft axis. It does not hold for migrating an existing system and it does not hold for different weights. And it rests on one decision by the decider from 2026-08-22 — the amendment to gate B2 (§2.2) — without which the leader would have been eliminated before anything was computed.

## 7. Second brief: language professionalism (rules written 2026-08-23 — BEFORE the research)

### 7.1 Why there is a second brief

After the verdict in §6.2 was delivered, the decider clarified that **what carries most weight for them is the professionalism of the language, specifically its syntax** — whether small and very large projects can be written legibly in it — and that this is essentially independent of domain.

**The objection is justified and the document had drifted.** The original brief said *"small and large projects… code legibility, correctness in code"*, and the original proposal of 2026-08-08 said *"how professional modern programming languages are"*. That axis was the main one from the start; §2.3 demoted it to a **tie-breaker**, a criterion that fires only on a tie. It happened because a mechanical verdict could be built out of the domains — measurability beat relevance.

**This is not fixed by rewriting.** §6.2 anticipated this case in advance: a changed brief is recorded as a **new dated brief**, not as a correction of the old one, because a rule edited after seeing the result loses the one thing that made writing it in advance worth anything. **The verdict in §6.2 therefore still stands as the answer to the first brief** and this is the answer to the second. The document will carry both and record any disagreement between them.

### 7.2 Decision rules of the second brief

**Candidates:** the same eight, in the same alphabetical order (§2.1). **Methodological rules M1 to M5 (§2.4) apply unchanged** — including the mandatory adversarial pass and the ban on inference wearing a fact's clothes.

**Criteria.** On 2026-08-23 the decider selected **all four** of the readings offered, without ranking them:

| # | Criterion | What is measured (checkable, not impressionistic) |
|---|---|---|
| **P1** | The compiler catches the mistake before the user does | The enforcement boundary (§4.1 point a), nullability in the type system, exhaustive branching |
| **P2** | A stranger can read the code without context | Existence of an **official** formatter, the size and simplicity of the language, the ability to change behaviour at runtime |
| **P3** | Large refactors are safe | Static types plus the existence of an **official** language server; whether the compiler finds every call site |
| **P4** | The type system carries the domain model | Sum types with data, exhaustive branching over them, immutability |

**Weights: all four criteria equal (1 · 1 · 1 · 1).** The decider selected them without ranking, so equal weights are the least amount of guessing. **It is a choice, however, not a fact** — and, taught by §6.3, I commit up front to adding a sensitivity table so it does not decide the outcome silently.

**Cost and aggregation** are identical to §2.3 so the numbers are comparable: ✅ = 0 · 🟡 = 1 · ❌ = 3, summed across four criteria, **lowest wins** (range 0 to 12).

**Scope.** This brief **has no domains and no domain weights** — it is domain-independent by nature. It does not void §6.2 and has no effect on it.

### 7.3 Prediction recorded before the research

Taught by the §2.3 prediction failing because it reasoned about strengths rather than variance, this time I reason about variance within the criteria. **This is inference, not fact.**

- **I expect the largest variance in P4**, where sum types either exist in the language or do not exist at all. That should order the field more than the other three.
- **Go is the candidate with the most self-contradictory profile:** very strong P2 (a deliberately small language, official `gofmt`) and P3, but P4 should be missing. Its placing therefore depends on whether P2 offsets P4 — and at equal weights that is open.
- **I expect Kotlin and Rust in front**, because they should be the only two decent on all four.
- **The winner of the first brief, TypeScript, will not win here** in my view, because P1 drags it down (§4.1: types are not enforced at runtime). I therefore expect the document to end **with two verdicts that disagree** — and that disagreement will be more useful than either of them alone.

If the research refutes this prediction, that is recorded as a result, not as a correction of the prediction.

### 7.4 Professionalism table (verified 2026-08-23)

Costs: ✅ = 0 · 🟡 = 1 · ❌ = 3, summed across four criteria, lowest wins (§7.2).

| Language | P1 compiler catches the mistake | P2 legible to people | P3 large refactors safe | P4 types carry the domain model | Sum |
|---|---|---|---|---|---|
| **C#** | 🟡 the runtime enforces types, but nullability is compile-time only and `!` exists [R50] | ✅ `dotnet format` under the `dotnet` organisation [R75] | ✅ static types, Roslyn from Microsoft [R75] | 🟡 sum types are still a **proposal**, `standard-unions.md` in `dotnet/csharplang` [R76] | **2** |
| **Go** | 🟡 the runtime enforces types, but `nil` is the zero value of everything by reference [R54] | ✅ `gofmt` ships with the distribution, *"uncontroversial"*, and the FAQ documents deliberate omission of features [R73][R74] | ✅ static types, `gopls` under the `golang` organisation [R75] | ❌ the FAQ: *"We considered adding variant types to Go, but after discussion decided to leave them out"* [R73] | **4** |
| **Java** | 🟡 the runtime enforces types, but generics are erased and nullability is absent from the language [R55] | ❌ no official formatter exists; `google-java-format` is Google's [R75] | 🟡 static types, but the language server is Eclipse's, not the language steward's [R75] | ✅ sealed interfaces (JDK 17) + exhaustive `switch` without `default` (JDK 21) [R68][R69] | **5** |
| **Kotlin** | ✅ nullability in the type system, compiler-enforced; the hole is platform types from Java [R52] | ✅ `ktfmt` under the `Kotlin` organisation [R75] | ✅ static types, `kotlin-lsp` under the `Kotlin` organisation [R75] | ✅ sealed classes, *"you don't need to add an `else` clause"* [R67] | **0** |
| **PHP** | ❌ strictness is a per-file directive and there are no generics [R49] | ❌ no official formatter exists; PHP-CS-Fixer is its own organisation [R75] | ❌ no official language server found [R75] | ❌ enums since 8.1 are *"backed by types of `int` or `string`"* — cases carry only a scalar [R70] | **12** |
| **Python** | ❌ *"The Python runtime does not enforce… type annotations"* [R47] | ✅ `black` under the `psf` organisation [R75] | 🟡 dynamic; `mypy` and `typeshed` are under the `python` organisation [R75][R80] *(refined in §9.1 — the original wording cited `pyright`, which did Python an injustice)* | 🟡 `match` and `assert_never` work, but **only in static checking** [R77] | **5** |
| **Rust** | ✅ null does not exist, `Option<T>`, *"Matches in Rust are exhaustive"* [R53][R72] | ✅ `rustfmt` under the `rust-lang` organisation [R75] | ✅ static types, `rust-analyzer` under the `rust-lang` organisation [R75] | ✅ enums with data + exhaustive `match` enforced by the compiler [R72] | **0** |
| **TypeScript** | ❌ types are erased and the output is plain JavaScript [R39] | ❌ no official formatter exists; Prettier is a separate organisation [R75] | ✅ static types and tooling from Microsoft [R75] | ✅ discriminated unions + exhaustiveness checking through `never` [R71] | **6** |

**What P2 measures and what it does not.** I rated **formatter ownership only** — whether one exists under the language's own organisation, which is checkable. The other half of the question, *how much magic you must hold in your head*, I could not turn into a checkable criterion and it **is not measured**. The Go cell is the only one where deliberate simplicity is additionally documented, because the language's own FAQ asserts it.

**Evaluation of the §7.3 prediction — this time it held.** I predicted Kotlin and Rust in front (**correct, both at zero**), that TypeScript would not win (**correct, seventh**), the largest variance in P4 (**correct** — values 0, 0, 0, 1, 1, 3, 3, 3) and that Go has the most self-contradictory profile, with P2 fighting P4 (**correct** — ✅ ✅ in P2 and P3 against ❌ in P4, landing it mid-table). The difference from the failed §2.3 prediction is that this one reasoned about **variance within criteria** rather than about candidates' strengths.

**Sensitivity to the weights, as committed to in §7.2.** Doubling any one of the four criteria produces **the same winner every time**: Kotlin and Rust at zero. Only the field behind them reshuffles — at double weight on P4, for instance, Go falls to seventh; at double P2 it is fourth. **The second brief's result is therefore practically independent of the weights**, which could not be said of the first.

### 7.5 Verdict of the second brief (2026-08-23)

**Kotlin and Rust win, both at zero — and it is a full tie, not a narrow lead.** They are the only two of the eight rated ✅ on all four criteria.

**Rule §7.2 does not settle this tie.** I did not write a tie-breaker for the second brief, which is a gap in my own rules — and **adding one now, after seeing the result, is exactly what this document refuses to do everywhere else.** The verdict therefore reads: **joint first place**, and the choice between them belongs to the decider. The material for it is already in the document and I summarise it without turning it into a rule:

- **Kotlin** has the entire JVM ecosystem and Spring Boot behind it (§4.3), but **the smallest hiring base of the eight** — 11.5 % against Rust's 14.5 % (§5.1) — has no dated support table (§4.5), and its one hole in strictness opens precisely when calling Java, which is the ecosystem you chose it for (§4.1).
- **Rust** has the strongest guarantees of the eight and is the only one without null at all (§4.1), but in the first brief it is the only candidate not rated ✅ in backend — the highest-weighted domain (§3) — and it has no dated support table either.

**The disagreement between the two verdicts is the biggest output of the whole document.** It is not an error in either of them; both briefs are legitimate and each measures something different.

| Language | Placing: domains (§6.2) | Placing: professionalism (§7.5) | Shift |
|---|---|---|---|
| **C#** | 3. | 3. | 0 |
| **Go** | 8. | 4. | +4 |
| **Java** | 4. | 5. | −1 |
| **Kotlin** | 5. | 1. | +4 |
| **PHP** | 7. | 8. | −1 |
| **Python** | 2. | 6. | −4 |
| **Rust** | 6. | 2. | +4 |
| **TypeScript** | 1. | 7. | **−6** |

**The winner of the first brief places seventh in the second.** The winners of the second place fifth and sixth in the first. That means one thing, but a fundamental one: **no language is simultaneously the best fit for your four domains and the most professional tool.** That trade is the real content of this document, not either verdict on its own.

**An observation, explicitly not a third verdict.** Summing both placings puts C# and Kotlin best (both 6), then Rust, Python and TypeScript (8). **C# is moreover the only candidate in the top three of both briefs.** I stress that this **is not a verdict**: summing placings is an aggregation I invented **after seeing the results**, and as such it carries none of the weight of a rule written in advance. A genuine combined verdict would need its own rule, written and dated before it runs — and that is work for another round, not for this one.

**Scope of validity.** The verdict in §7.5 holds for the four criteria in §7.2 with equal weights, for the same eight candidates. It does not void §6.2 and has no effect on it. P2 is measured incompletely (formatter ownership only) and §8 concerns §4.5, not this brief.

## 8. Correction (2026-08-23): gate B2 should not have fired

**What was wrong.** §4.5 claimed TypeScript was the only one of the eight with no documented support commitment, and on that basis gate B2 fired against it on 2026-08-22. **The claim is false.** The root of the `microsoft/TypeScript` repository contains a `SUPPORT.md` file with a *"Microsoft Support Policy"* section which states: *"When included with a Microsoft product, TypeScript support and servicing is offered under the [Modern Support Policy]. For Visual Studio, servicing fixes are limited to security fixes for versions of TypeScript included in under-support releases of Visual Studio."* [R66]

**How it happened — and that is more instructive than the error itself.** I searched two places: the wiki page about releases [R17] and issue #49088 from 2022 [R18]. Both were silent, and I turned that into a conclusion about absence. **I did not check `SUPPORT.md` in the repository root — the standard location for exactly this information.** For Express and Axum I did list the repository root and even watched the positive control; for TypeScript I did not, because I had a quote from a team member and considered the question closed. **A strong-sounding source deterred me from searching further** — which is exactly the trap the rule "an empty search result is not a source" describes. The quote was not even in conflict with the finding: in 2022 Ryan Cavanaugh said no policy existed *"beyond the one implied by the fact that we ship our components in Visual Studio"* — and `SUPPORT.md` is precisely that implied policy, written down.

**What holds instead.** TypeScript **does** have a documented support policy, but a **conditional** one: it is tied to being shipped inside a Microsoft product, at Visual Studio it is limited to security fixes for versions included in supported VS releases, and **it gives the standalone npm package no version calendar** — nothing like the dated EOL table PHP, Python or .NET have. A difference from the other seven therefore exists, but it is the difference between *"a conditional policy with no version calendar"* and *"no policy"*, which is a different claim.

**Consequence for the decision rule.** Rule B2 stays recorded in §2.2 exactly as it was and is **not rewritten**. But it must be said aloud: **B2 fired on the basis of a wrong fact and on the right fact would probably not have fired at all.** The amendment to B2 that the decider approved on 2026-08-22 was therefore made on a false premise. It would be unnecessary rather than harmful — it leads to the same outcome (TypeScript passes), just by the right route. The decider deserves the note that they decided on the basis of my faulty finding.

**Consequence for the verdict (§6.2).** The verdict does not change — weighted cost does not include governance (§6.1). Two statements around it do change:

1. **Trade-off no. 1 in §6.2 was overstated.** "No support commitment for the compiler" does not hold; "a conditional policy with no version calendar, plus the Node.js runtime lifecycle" does. That line of the bill is **cheaper** than it was invoiced for.
2. **The objection in §6.1 about a structurally invisible weakness is weakened**, not voided. The argument that weighted cost measures only domain fit, and that the durable layer does not enter it, still holds. Only the specific weakness I used as its example is smaller than I claimed.

**What to carry into later rounds.** Before declaring something non-existent, I will inspect the **standard locations** for that kind of information — for a repository, the root, `.github`, `SUPPORT.md`, `SECURITY.md` — and will do so even when I already hold a source that sounds convincing. A verified quote about absence is still only a claim about what its author knew at the time.

## 9. Addendum (2026-08-26): why PHP trails Python so badly, and what does not hold up

The decider asked why PHP scored 12 in §7.4 and Python 5. The question forced a recheck, and that produced three things: the gap §4.1 itself admitted, confirmation of two claims that were **under-evidenced** when written, and one admitted crudeness in the instrument.

### 9.1 Where the gap is and where it is not

**P1 is identical for both — ❌ each.** The difference between PHP and Python is therefore **not** that one enforces types at runtime and the other does not. PHP enforces them per file and has no generics; Python does not enforce them at all; both land on the same value. Anyone looking for the reason here is looking in the wrong place.

**P4 is a real and sourced difference.** PHP enums carry only a scalar — *"may be backed by types of `int` or `string`"* [R70] — and the language has no generics at all [R49]. Python has unions, generics in annotations, `match` and `assert_never` [R77]. That all of it holds only at check time drags Python to 🟡; but PHP lacks those constructs **even at check time**. The 🟡 against ❌ difference holds here.

**P3: the original reasoning was incomplete and the new evidence favours Python.** I wrote that *"`pyright` is Microsoft's, not the PSF's"* — which did Python an injustice. **`mypy` and `typeshed` are under the `python` organisation**, that is, under the language's own steward (positive control: `peps`, `typing` and `pythondotorg` are under the same organisation) [R80]. Python therefore **does have a first-party type checker**. For PHP, conversely, I claimed "no official language server found" without having actually searched for one — a claim of non-existence with no search behind it, which is worse than an empty result. **Now filled in:** under the `php` organisation there is neither a language server nor a formatter; what is there is `php-src` and the project's web properties (positive control: `php-src` present) [R78]. The cells do not change, but they now rest on what they should have rested on.

### 9.2 What PHP got credit for in no cell, and should be said

§4.1 admitted that PHPStan and Psalm levels were not researched. Now filled in: **PHPStan has eleven levels (0 to 10)**, level 6 *"report missing typehints"*, level 9 is strict about explicit `mixed` and level 10 *"reports errors even for implicit mixed (missing type), not just explicit mixed"* [R79].

That is more ambitious than PHP looks in the table — and **it landed in no cell of §7.4**, because the criteria measured the language and its official tooling rather than the strength of community static analysis. It is a genuine PHP strength this document does not capture, and the reader should know about it.

### 9.3 Admitted crudeness of criterion P2

For this pair, P2 turns on a single thing: **whose organisation the formatter lives under.** `black` is under `psf`, the language's foundation → ✅. `PHP-CS-Fixer` is under its own organisation, not under `php` → ❌. **The difference between them is three points out of twelve, a quarter of the whole score**, and yet neither of those formatters ships with its language and in practice both are run the same way — as a step in CI.

**The criterion therefore measures ownership rather than the user's experience, and for the PHP–Python pair it is the weakest point in the whole of §7.4.** I am not rewriting the cell value: the rule was written before the research (§7.2) and changing it after seeing the result is what this document refuses. What I record instead is that **roughly a third of the 12 : 5 gap rests on a formalistic test**, and anyone who does not value that test should scale the gap accordingly.

### 9.4 Summary

The 12 : 5 gap **holds**, but it breaks down unevenly: P1 contributes nothing, P4 is fully sourced, P3 is sourced only after this addendum, and P2 rests on an instrument that admits its own crudeness. **The ordering does not change** — PHP stays eighth even on the most favourable reading, because seventh-placed TypeScript sits at 6.

## 10. Addendum (2026-08-26): which versions were actually analysed

The decider asked whether PHP had been rated at its newest version, and suggested recording the specific analysed versions per language so that a year from now it is clear what was assessed. Both point at rule **M1** (§2.4) — and both revealed that I applied it unevenly.

### 10.1 The PHP 8.5 check

**I knew the version and had not read its release notes.** PHP 8.5 appears in §4.5 and §5.2 with its support dates, but what it actually introduced I never verified — I rated from properties I already knew. Now filled in [R82]: PHP 8.5 added the pipe operator `|>`, `clone` with reassignment of readonly properties, the `#[\NoDiscard]` attribute, attributes on constants, `final` on promoted properties, asymmetric visibility for static properties and `#[\Override]` on properties.

**No cell moves.** 8.5 brought no generics, enums remain scalar-backed (§7.4, [R70]) and there is no pattern matching over sum types. P1 and P4 therefore stay ❌ for the same reasons as before, and the sum of 12 holds.

**One thing it did show, and not in my favour.** Criterion P4 was supposed under §7.2 to measure "sum types with data, exhaustive branching over them, **immutability**" — and that third component I effectively rated for nobody. PHP meanwhile has `readonly` (8.1), asymmetric visibility (8.4) and now `clone with` and `final` on promoted properties (8.5), which is a decent immutability story. It does not lift the cell, because the missing sum types dominate P4, but **P4 is incompletely measured for all eight** and the document should say so exactly as it does for P2 (§9.3).

### 10.2 Analysed versions

| Language | Current stable as of 2026-08-26 | What the ratings were anchored to |
|---|---|---|
| **C#** | .NET 10.0.11 (2026-08-11) [R81] | .NET 10 LTS; features cited from C# 14 (`field`), .NET 5 (annotated libraries), .NET 8 and 9 |
| **Go** | 1.27.0 (2026-08-19) [R6] | the specification including generics since 1.18; the Go 1 compatibility promise; the WebAssembly wiki |
| **Java** | JDK 25 as the current LTS [R11] | features cited from JDK 17 (sealed) and JDK 21 (virtual threads, pattern matching for `switch`) |
| **Kotlin** | 2.4.10 (2026-07-14) [R81] | documentation **with no version pinned**, read 2026-08-23 |
| **PHP** | 8.5.9 (2026-07-30) [R81] | 8.5 verified only on 2026-08-26 (§10.1); features cited from 8.1 (enums, fibers) and 8.4 (property hooks) |
| **Python** | 3.14 (first release 2025-10-07), 3.13 also in bugfix [R4] | the free-threaded build is described for 3.13; **its status in 3.14 was not separately verified** |
| **Rust** | 1.98.0 (2026-08-20) [R81] | the book and the docs **with no version pinned**, read 2026-08-22 and 23 |
| **TypeScript** | 7.0.2 (2026-08-20) [R81][R83] | documentation **with no version pinned**; TypeScript 7 was not accounted for in the analysis — see §10.3 |

### 10.3 What the version audit revealed

**TypeScript 7 is a different compiler from the one this document analysed.** The `v7.0.2` release points at the `microsoft/typescript-go` repository [R83], that is, at the native rewrite of the compiler in Go. The document nowhere mentions this, because I never pinned a version and simply read "the current documentation".

**It moves no cell:** types are still erased and the output is still plain JavaScript (P1), no official formatter still exists (P2), the tooling is still Microsoft's (P3) and discriminated unions still work (P4). But it is material context missing from the document, and a reader a year from now should know the analysis was written without accounting for TypeScript 7.

**I applied M1 unevenly, and it is now visible in black and white.** For Go, Java, .NET and Python I anchored to versions and named when individual features arrived. For Kotlin, Rust and TypeScript I read documentation with no version pinned. For PHP I knew the version and did not read the release notes. The rule asks for both, for everyone — the version and whether the ecosystem has caught up with it.

**The practical consequence for the reader:** the table in §10.2 is from now on what tells you what this document actually assessed. Where it says "with no version pinned", what holds is the verification date on the relevant reference rather than a version number — and that is weaker than M1 would want.

## References

Verified as of 2026-08-22 (round 1 — gate B2, §4.4 and §4.5).

**Funding and governance**

- [R3] The PHP Foundation — mission, ten contracted developers, sponsors. Verified 2026-08-22: <https://thephp.foundation/>
- [R5] Python Software Foundation — mission, intellectual property, CPython Developer in Residence. Verified 2026-08-22: <https://www.python.org/psf/about/>
- [R7] Go FAQ — origin of the project, the team at Google, the `gc` toolchain. Verified 2026-08-22: <https://go.dev/doc/faq>
- [R10] .NET Foundation — scope (community projects), sponsors. Verified 2026-08-22: <https://dotnetfoundation.org/>
- [R12] Eclipse Adoptium — working group members. Verified 2026-08-22: <https://adoptium.net/en-GB/members/>
- [R13] Kotlin Foundation — founders, members, declared tasks. Verified 2026-08-22: <https://kotlinfoundation.org/>
- [R15] Rust Foundation — founding platinum members, purpose. Verified 2026-08-22: <https://rustfoundation.org/>

**Support and compatibility commitments**

- [R2] PHP — Supported Versions (2 years active + 2 years security). Verified 2026-08-22: <https://www.php.net/supported-versions.php>
- [R4] Python Developer's Guide — Status of Python versions (PEP 602, five years). Verified 2026-08-22: <https://devguide.python.org/versions/>
- [R6] Go — Release History and support policy (until two newer versions ship); Go 1.27.0 released 2026-08-19. Verified 2026-08-22: <https://go.dev/doc/devel/release>
- [R8] Go 1 and the Future of Go Programs — the compatibility promise and its exceptions. Verified 2026-08-22: <https://go.dev/doc/go1compat>
- [R9] .NET Support Policy — LTS 36 months, STS 24 months, concrete dates. Verified 2026-08-22: <https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core>
- [R11] Eclipse Adoptium — Support (one LTS every two years, "at least four years", free). Verified 2026-08-22: <https://adoptium.net/support/>
- [R14] Kotlin — Evolution principles (binary compatibility, deprecation cycle, `-language-version`). Verified 2026-08-22: <https://kotlinlang.org/docs/kotlin-evolution-principles.html>
- [R16] The Rust Edition Guide — Editions (stability, interoperability of editions). Verified 2026-08-22: <https://doc.rust-lang.org/edition-guide/editions/index.html>
- [R17] TypeScript's Release Process (wiki) — release cadence; silent on LTS. Verified 2026-08-22: <https://github.com/microsoft/TypeScript/wiki/TypeScript%27s-Release-Process>
- [R18] microsoft/TypeScript issue #49088 "Document TypeScript version lifetime and EOL" (closed) — the team's statement that no official policy exists. Verified 2026-08-22: <https://github.com/microsoft/TypeScript/issues/49088>
- [R19] Node.js — Previous Releases (LTS 30 months). Verified 2026-08-22: <https://nodejs.org/en/about/previous-releases>

**Distribution and deployment (round 2, the CLI domain)**

- [R20] .NET — Native AOT deployment overview, including the Limitations section. Verified 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/>
- [R21] GraalVM — Native Image (closed-world assumption, limits on reflection and JNI). Verified 2026-08-22: <https://www.graalvm.org/latest/reference-manual/native-image/>
- [R22] Node.js — Single executable applications (Stability 1.1, limitations). Verified 2026-08-22: <https://nodejs.org/api/single-executable-applications.html>
- [R23] Deno — `deno compile` (standalone binary, cross-compilation). Verified 2026-08-22: <https://docs.deno.com/runtime/reference/cli/compile/>
- [R24] Go — Installing Go from source, the `GOOS`/`GOARCH` table. Verified 2026-08-22: <https://go.dev/doc/install/source>
- [R25] static-php-cli — Guide (statically linked PHP binaries, supported platforms and versions). Verified 2026-08-22: <https://static-php.dev/en/guide/>
- [R26] PyInstaller — How it works / operating mode (one-file mode, absence of cross-compilation). Verified 2026-08-22: <https://pyinstaller.org/en/stable/operating-mode.html>
- [R27] Rust — Platform Support (definitions of Tier 1 and Tier 2). Verified 2026-08-22: <https://doc.rust-lang.org/rustc/platform-support.html>

**Frameworks and their support commitments (round 3, the backend domain)**

- [R28] Symfony — Releases (standard releases 8 months of fixes and 14 months of security; LTS 3 years of fixes and 4 years of security). Verified 2026-08-22: <https://symfony.com/releases>
- [R29] Laravel — Release Notes, Support Policy section (*"bug fixes are provided for 18 months and security fixes are provided for 2 years"*). Verified 2026-08-22 on the 12.x documentation page, which also notes that 13.x is the current line: <https://laravel.com/docs/12.x/releases>
- [R30] Django — Download, overview of supported versions and the three-year window. Verified 2026-08-22: <https://www.djangoproject.com/download/>
- [R31] Spring Boot — Supported Versions (project wiki): minor *"at least 12 months"*, major *"at least 3 years"*. Verified 2026-08-22: <https://github.com/spring-projects/spring-boot/wiki/Supported-Versions>
- [R32] Fastify — Long Term Support. Verified 2026-08-22: <https://fastify.dev/docs/latest/Reference/LTS/>
- [R33] expressjs/express — repository listing; no support policy found in the root or in `.github`. **The conclusion is weak:** the positive control on the `expressjs/expressjs.com` repository failed (the `en` path returned 404), so nothing is claimed about the structure of the documentation. Verified 2026-08-22: <https://github.com/expressjs/express>
- [R34] tokio-rs/axum — repository listing; no dated support policy found in the root or in the `axum` crate directory. Positive control passed (`Cargo.toml` present in both listings). Verified 2026-08-22: <https://github.com/tokio-rs/axum>

**The route into the browser (round 4, the frontend domain)**

- [R35] ASP.NET Core — Host and deploy Blazor WebAssembly (runtime download, Webcil, trimming, compression, `EmccMaximumHeapSize`). Verified 2026-08-22: <https://learn.microsoft.com/en-us/aspnet/core/blazor/host-and-deploy/webassembly/>
- [R36] Kotlin/Wasm overview — Beta status and browser requirements. Verified 2026-08-22: <https://kotlinlang.org/docs/wasm-overview.html>
- [R37] Go Wiki — WebAssembly (output size, `wasm_exec.js` tied to the version, TinyGo). Verified 2026-08-22: <https://go.dev/wiki/WebAssembly>
- [R38] pyodide/pyodide — README (a port of CPython to WebAssembly/Emscripten, package support, Web API access). Verified 2026-08-22: <https://github.com/pyodide/pyodide>. *The page carrying size figures* <https://pyodide.org/en/stable/project/about.html> *returned 403; no size number is therefore claimed in this document.*
- [R39] TypeScript Handbook — TypeScript from Scratch (type erasure, preserved runtime behaviour). Verified 2026-08-22: <https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html>
- [R40] Rust and WebAssembly (the working group's book) — carries a notice that the project and website are no longer maintained. Verified 2026-08-22: <https://rustwasm.github.io/docs/book/>
- [R41] TeaVM — landing page (an AOT compiler from Java bytecode to JavaScript and WebAssembly). Verified 2026-08-22: <https://teavm.org/>
- [R42] seanmorris/php-wasm — README (coverage of PHP 8.0–8.5, packages, Apache-2.0 licence). Verified 2026-08-22: <https://github.com/seanmorris/php-wasm>

**Data, ML and batch processing (round 5)**

- [R43] ML.NET — overview on dotnet.microsoft.com (first-party framework, supported scenarios, deployment in Microsoft products). Verified 2026-08-22: <https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet>
- [R44] Apache Spark — documentation, list of language APIs and the native implementation language. Verified 2026-08-22: <https://spark.apache.org/docs/latest/>
- [R45] pola-rs/polars — README (a query engine written in Rust, list of language bindings). Verified 2026-08-22: <https://github.com/pola-rs/polars>
- [R46] TensorFlow.js — overview (ML in the browser and in Node.js). Verified 2026-08-22: <https://www.tensorflow.org/js>

**Strictness and type systems (round 6, §4.1)**

- [R47] Python — `typing` (the runtime does not enforce annotations; behaviour of `Any`). Verified 2026-08-22: <https://docs.python.org/3/library/typing.html>
- [R48] mypy — Command line (contents of `--strict`, `--warn-unused-ignores`, the limits of its guarantee). Verified 2026-08-22: <https://mypy.readthedocs.io/en/stable/command_line.html>
- [R49] PHP Manual — Type declarations (`TypeError` at call time, `declare(strict_types=1)` per file, coercion, absence of generics). Verified 2026-08-22: <https://www.php.net/manual/en/language.types.declarations.php>
- [R50] C# — Nullable reference types (entirely a compile-time feature, the `!` operator, traps with `default` structs and arrays, annotated libraries since .NET 5). Verified 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references>
- [R51] TypeScript — TSConfig `strict` (the family of switches; the warning about strictness growing between versions). Verified 2026-08-22: <https://www.typescriptlang.org/tsconfig/strict.html>
- [R52] Kotlin — Null safety (nullability in the type system, platform types when interoperating with Java). Verified 2026-08-22: <https://kotlinlang.org/docs/null-safety.html>
- [R53] The Rust Programming Language — Defining an Enum (`Option<T>`, the absence of null). Verified 2026-08-22: <https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html>
- [R54] The Go Programming Language Specification — zero values, `nil`, type parameters since Go 1.18. Verified 2026-08-22: <https://go.dev/ref/spec>
- [R55] The Java Tutorials — Type Erasure. Verified 2026-08-22: <https://docs.oracle.com/javase/tutorial/java/generics/erasure.html>

**Concurrency, performance and hiring (round 7, §4.2 and §4.6)**

- [R56] Python — Free-threaded CPython HOWTO (build without the GIL since 3.13, the GIL being re-enabled by an unprepared extension, 1–8 % overhead). Verified 2026-08-22: <https://docs.python.org/3/howto/free-threading-python.html>
- [R57] Oracle — Virtual Threads (JDK 21; millions of threads; "not faster threads… scale, not speed"). Verified 2026-08-22: <https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html>. *The primary JEP 444 on openjdk.org returned 403.*
- [R58] Node.js — `worker_threads` (useful for CPU, not for I/O; Stability 2 — Stable). Verified 2026-08-22: <https://nodejs.org/api/worker_threads.html>
- [R59] Effective Go — Concurrency (the cost of a goroutine, multiplexing onto OS threads). Verified 2026-08-22: <https://go.dev/doc/effective_go>
- [R60] PHP Manual — Fibers (since PHP 8.1). Verified 2026-08-22: <https://www.php.net/manual/en/language.fibers.php>
- [R61] Stack Overflow Developer Survey 2025 — Technology, shares among professional developers. Verified 2026-08-22: <https://survey.stackoverflow.co/2025/technology>

**Language professionalism (§7.4)**

- [R67] Kotlin — Sealed classes and interfaces (the compiler knows all subclasses; `when` without `else`). Verified 2026-08-23: <https://kotlinlang.org/docs/sealed-classes.html>
- [R68] Oracle — Sealed Classes and Interfaces (JEP 409, permitted subclasses). Verified 2026-08-23: <https://docs.oracle.com/en/java/javase/21/language/sealed-classes-and-interfaces.html>
- [R69] Oracle — Pattern Matching for switch (JEP 441, exhaustive coverage of a sealed type without `default`). Verified 2026-08-23: <https://docs.oracle.com/en/java/javase/21/language/pattern-matching-switch.html>
- [R70] PHP Manual — Backed enumerations (*"may be backed by types of `int` or `string`"*). Verified 2026-08-23: <https://www.php.net/manual/en/language.enumerations.backed.php>
- [R71] TypeScript Handbook — Narrowing (discriminated unions, exhaustiveness checking through `never`). Verified 2026-08-23: <https://www.typescriptlang.org/docs/handbook/2/narrowing.html>
- [R72] The Rust Programming Language — The match Control Flow Construct (*"Matches in Rust are exhaustive"*). Verified 2026-08-23: <https://doc.rust-lang.org/book/ch06-02-match.html>
- [R73] Go FAQ — why Go has no variant types, and deliberate simplicity. Verified 2026-08-23: <https://go.dev/doc/faq>
- [R74] The Go Blog — gofmt (part of the distribution; *"uncontroversial"*). Verified 2026-08-23: <https://go.dev/blog/gofmt>
- [R75] Tool ownership by GitHub organisation, verified through the API on 2026-08-23 (positive control: every query returned repository metadata): `rust-lang/rustfmt`, `rust-lang/rust-analyzer`, `golang/tools` (gopls), `Kotlin/ktfmt`, `Kotlin/kotlin-lsp`, `psf/black`, `dotnet/format`, `microsoft/pyright` — against `prettier/prettier`, `PHP-CS-Fixer/PHP-CS-Fixer` and `google/google-java-format`, which are **not** under their language's organisation.
- [R76] dotnet/csharplang — `proposals/standard-unions.md`; sum types in C# are still a **proposal**, not a language feature. Verified 2026-08-23: <https://github.com/dotnet/csharplang/blob/main/proposals/standard-unions.md>
- [R77] Python — `typing.assert_never` (exhaustiveness checking, but only in static checking). Verified 2026-08-23: <https://docs.python.org/3/library/typing.html>

**Version audit (§10)**

- [R81] Current stable versions looked up through the GitHub API on 2026-08-26 (positive control: every query returned release data): `JetBrains/kotlin` v2.4.10 (2026-07-14), `rust-lang/rust` 1.98.0 (2026-08-20), `microsoft/TypeScript` v7.0.2 (2026-08-20), `dotnet/core` v10.0.11 (2026-08-11), `php/php-src` php-8.5.9 (2026-07-30).
- [R82] PHP 8.5 — new features (pipe operator, `clone with`, `#[\NoDiscard]`, `final` on promoted properties). Verified 2026-08-26: <https://www.php.net/releases/8.5/en.php>
- [R83] microsoft/TypeScript — the `v7.0.2` release points at `microsoft/typescript-go`, the native rewrite of the compiler. Verified 2026-08-26: <https://github.com/microsoft/typescript-go>

**Addendum (§9)**

- [R78] The `php` organisation on GitHub — repository listing; neither a formatter nor a language server is under it. Positive control passed (`php-src` and the project's web properties present). Verified 2026-08-26: <https://github.com/orgs/php/repositories>
- [R79] PHPStan — Rule Levels (0 to 10; level 6 "report missing typehints", level 10 implicit `mixed`). Verified 2026-08-26: <https://phpstan.org/user-guide/rule-levels>
- [R80] The `python` organisation on GitHub — `mypy` and `typeshed` are under it. Positive control passed (`peps`, `typing`, `pythondotorg` present). Verified 2026-08-26: <https://github.com/orgs/python/repositories>

**Correction (§8)**

- [R66] microsoft/TypeScript — `SUPPORT.md`, the "Microsoft Support Policy" section. Verified 2026-08-23: <https://github.com/microsoft/TypeScript/blob/main/SUPPORT.md>

**Adversarial pass (§6.1)**

- [R65] actix/actix-web — repository listing; no dated support policy found in the root or in `.github`. Positive control passed (`Cargo.toml` in the listing). Verified 2026-08-23: <https://github.com/actix/actix-web>

**Properties as a language feature (round 8, §4.8)**

- [R62] C# — Properties (properties as members with `get`/`set` accessors). Verified 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties>
- [R63] Kotlin — Properties (`val`/`var`, generated and custom accessors). Verified 2026-08-22: <https://kotlinlang.org/docs/properties.html>
- [R64] Python — the built-in `property()` function and the `@property` decorator. Verified 2026-08-22: <https://docs.python.org/3/library/functions.html>

**Language features**

- [R1] PHP Manual — Property Hooks (version: introduced in PHP 8.4). Verified 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

*Unreachable sources:* the Oracle Java SE Support Roadmap <https://www.oracle.com/java/technologies/java-se-support-roadmap.html> returned HTTP 403 on 2026-08-22; Java therefore rests on [R11][R12].


---

This document is a dated snapshot and is not retro-updated. New findings arrive as dated sections at the end; corrections are recorded as dated addenda.
