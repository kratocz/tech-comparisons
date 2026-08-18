# Voice dictation on the Mac: Wispr Flow vs Superwhisper vs Spokenly vs macOS Dictation vs VoiceInk vs FluidVoice

- **Verdict:** ⭐ **VoiceInk** (built from source, local Parakeet v3, text enhancement via own API keys) — valid for the context described below
- **Facts verified:** 2026-08-18 (wisprflow.ai /pricing and /data-controls, superwhisper.com, spokenly.app, tryvoiceink.com + docs + GitHub Beingpax/VoiceInk, GitHub altic-dev/FluidVoice, Apple "macOS Feature Availability", NVIDIA model card parakeet-tdt-0.6b-v3)
- **Open tags:** one `[VERIFY]` — Superwhisper Pro / Lifetime pricing (§7): sources contradict each other and the site did not yield the price legibly
- **Process note:** this comparison originated in a conversation with Claude (claude.ai, 2026-08-18). Per this repository's rules, findings from an AI conversation are hypotheses, not sources — every load-bearing claim was re-verified against primary sources. Two claims did not survive verification and are already corrected here: Czech in macOS Dictation is **not** on-device (§4), and VoiceInk **does** have an iOS companion app (§7). The decision rules in §1 were written after the app was chosen — they are not pre-registered and must not be read as a prediction.
- **Language:** 🇬🇧 English (canonical) · 🇨🇿 [Czech original](README.cs.md)
- **Author:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Context: the profile this decision was made for

- **Solo developer on an Apple Silicon Mac.** Other platforms (Windows, Android) play no role; iOS is a nice bonus, not a requirement.
- **Dictation is primarily in Czech**, secondarily in English. An app whose Czech is not usable is out of the running regardless of its other qualities.
- **Dictation goes everywhere** — messages, documents, and above all prompts for Claude Code, which the author uses daily.
- **Preference for local processing.** Voice should not leave the machine; cloud is acceptable at most optionally, for already-transcribed text, via own API keys.
- **Aversion to subscriptions** for a tool of this size. A one-time payment or an open-source build is the preferred model.
- **Two apps have been tested first-hand:** Wispr Flow and VoiceInk with the Parakeet v3 model. Czech-quality ratings for the others are derived, not tested (§4).

Out of scope: transcribing recorded meetings and meeting notetakers (a different task than dictation), Windows and Linux, voice control of the system.

## Summary (TL;DR)

1. ⭐ **Recommendation: VoiceInk** — the only candidate that simultaneously transcribes locally, ranks among the best in Czech (verified by the author's own testing, §4), and thanks to its GPL-3.0 license can be legally compiled from source and run for free (§3, §8).
2. **The structural divide is not price but where transcription runs** (§2). Wispr Flow is the only one with no local mode — its own Data Controls page says *"Transcription always occurs on the cloud."* That is architecture, not a setting, and for this context it is a disqualification.
3. **Czech quality is a property of the engine, not the app** (§4). Superwhisper, Spokenly, VoiceInk and FluidVoice run the same local models (Whisper, Parakeet TDT v3 — 25 languages including Czech per NVIDIA). The same model gives practically the same Czech transcript in all four; they differ in price, UX and post-processing.
4. **Built-in macOS Dictation loses twice for Czech** (§4): Apple lists it neither among languages with on-device dictation (so even system dictation sends Czech speech to a server) nor among languages with automatic punctuation.
5. **Enhancement of dictated text differs in who controls it** (§5): Wispr Flow does it always and in its own cloud, FluidVoice automatically and locally (but via a closed-source layer), Superwhisper / Spokenly / VoiceInk via an LLM of your choosing — for VoiceInk including a fully local Ollama.

## Comparison at a glance

Symbols: ✅ strength · 🟡 works with caveats / trade-off · ❌ weakness or missing · — not applicable. Rated **for this context** (a Czech-dictating solo developer on Apple Silicon, preference for local processing, aversion to subscriptions) — not in general; for an English-speaking multi-platform user many rows would come out differently. Column order follows the original conversation and is identical in every table of this document.

| Criterion | Wispr Flow | Superwhisper | Spokenly | macOS Dictation | VoiceInk | FluidVoice |
|---|---|---|---|---|---|---|
| **▸ Processing and privacy** (§2) | | | | | | |
| Local transcription (voice never leaves the machine) | ❌ *"always … on the cloud"* | ✅ local Whisper | ✅ local Whisper / Parakeet | ❌ Czech goes via server only (§4) | ✅ local Whisper / Parakeet and more | ✅ all local (Parakeet / Nemotron / Whisper) |
| Works offline | ❌ | ✅ | ✅ | ❌ for Czech | ✅ | ✅ |
| **▸ Price and license** (detail §7) | | | | | | |
| Price for this profile | ❌ $15 / mo; free tier 2,000 words / week | 🟡 free tier with small models; Pro paid | ✅ local models + own keys free | ✅ free, part of the OS | ✅ $29 one-time / free when built from source | ✅ entirely free |
| Open source | ❌ | ❌ | ❌ | ❌ | ✅ GPL-3.0 | 🟡 GPLv3, but the Fluid-1 layer is closed-source |
| **▸ Platforms** | | | | | | |
| macOS requirements | ✅ | ✅ | ✅ | ✅ part of the OS | ✅ macOS 14.4+, Apple Silicon | 🟡 macOS 15.0+ only |
| Beyond macOS | ✅ Windows / iOS / Android | ✅ Windows / iOS | ✅ Windows / Linux / iOS | 🟡 counterpart on iOS / iPadOS | 🟡 iOS companion app | ❌ nothing yet (Windows / iOS announced) |
| **▸ Czech** (§4) | | | | | | |
| Czech supported in transcription | ✅ 100+ languages | ✅ via Whisper | ✅ Whisper + Parakeet v3 | 🟡 yes, but no on-device and no auto-punctuation | ✅ Whisper + Parakeet v3 | ✅ Whisper + Parakeet v3 |
| Czech dictation quality | ✅ excellent, but inserts ", eh, " on pauses *(tested)* | 🟡 derived from the engine, untested | 🟡 derived from the engine, untested | ❌ weakest of the comparison | ✅ with Parakeet v3 only a few % behind Wispr Flow *(tested)* | 🟡 derived from the engine, untested |
| **▸ Text enhancement** (§5) | | | | | | |
| Enhancement of dictated text | 🟡 automatic, but exclusively in their cloud | ✅ modes with custom prompts, LLM of your choice | ✅ optional, via own keys | ❌ none | ✅ optional, custom prompts, own keys incl. local Ollama | ✅ automatic, fully local (Fluid-1) |
| **▸ Integration with AI coding agents** (§6) | | | | | | |
| Voice for coding agents | — | ✅ declared support for Claude Code et al. | ✅ MCP server | — | 🟡 "Local CLI" provider for enhancement | — |
| **▸ Operational risk** | | | | | | |
| Maturity and continuity | 🟡 established service, but cloud: price hikes or shutdown outside your control | 🟡 commercial indie app | 🟡 commercial indie app | ✅ part of the OS | 🟡 solo developer; GPL → fork possible, local models survive | 🟡 young project, GPLv3 only since 2/2026 |

### How to read it

Wispr Flow wins the single row this context allows it to compete on — Czech quality — and even there with a flaw (", eh, "). Everything else it loses on architecture: cloud-only transcription conflicts with rule 2 of §1 and the subscription with rule 3. macOS Dictation is the opposite extreme: free and frictionless, but for Czech it has no on-device mode, no automatic punctuation and no enhancement of any kind — usable as a fallback, not as a daily tool. The middle four (Superwhisper, Spokenly, VoiceInk, FluidVoice) share the same local engines, so licensing and control decide the order: VoiceInk is the only fully open-source one with Czech quality documented by the author's own test; FluidVoice is free and fastest, but its text enhancement rests on a closed-source layer and the project demands the newest macOS; Spokenly offers the most interesting integration (MCP server) and a generous free tier, but is not open source; Superwhisper is the most configurable, but is paid by subscription or the priciest lifetime in the category and is not open source.

## 1. Decision rules (2026-08-18)

Written on the day this document was written, **after** the app was chosen — see the process note in the header. These are not pre-registered rules but explicit criteria against which the verdict can be re-examined:

1. **Czech must be usable for everyday dictation** — the primary language, not an edge case.
2. **Voice does not leave the machine.** Transcription runs locally; cloud is acceptable only optionally, for already-transcribed text, via own keys.
3. **No subscription.** One-time payment or free; open source with a build-from-source option is both a plus and a continuity insurance.
4. **Text enhancement under the user's own control** — own prompt and model choice, not an imposed black-box post-processor.

**Disqualifying criterion:** an app whose transcription runs exclusively in the cloud (violates rule 2). Wispr Flow falls out on this, but stays in the table deliberately — it is the only cloud reference bar the author has tested in Czech, so it serves as the quality baseline (§4).

## 2. Cloud vs local transcription — the structural divide

The most important difference in this whole comparison is not in the price lists but in the architecture. Wispr Flow's own Data Controls page states: *"Transcription always occurs on the cloud. This is the best way for us to provide accurate, low latency transcription."* The privacy on offer is retention-level, not architectural: Privacy Mode and disabled Private Cloud Sync limit what the service **keeps** (audio and transcript are then *"processed in real time and discarded after the request completes"*), but do not change where the data **flows** — Czech speech always goes to their servers. This is a durable property: the company itself describes it as the foundation of the product, not a temporary state.

The remaining four apps (and, for supported languages, macOS Dictation too) transcribe on-device. Superwhisper, Spokenly, VoiceInk and FluidVoice build on the same public models — Whisper in various sizes and NVIDIA Parakeet — running on Apple Silicon. A second durable fact follows: **local transcription outlives its developer.** A model the user has downloaded keeps working after the project dies; a cloud service dies with its operator. For rule 2 of §1 and for the continuity risk (last table row) this is a more fundamental argument than any feature.

## 3. License and ownership: subscription vs one-time vs open source

The five apps cover the whole spectrum of business models:

- **Wispr Flow** — pure SaaS subscription ($15 / mo, $12 / mo billed annually). The free tier's limit of 2,000 words per week on desktop is an order of magnitude short of daily dictation.
- **Superwhisper** — freemium: a free tier with small local models and custom prompts, paid Pro (monthly / yearly / lifetime; on prices see the contradiction in §7).
- **Spokenly** — local models and own keys free without limits; only the managed cloud is paid ($9.99 / mo).
- **VoiceInk** — open source (GPL-3.0) with paid binaries: one-time $29 / $49 / $69 by number of Macs, lifetime updates. The README says explicitly: *"As an open-source project, you can build VoiceInk yourself by following the instructions in BUILDING.md."* The paid build adds automatic updates and developer support — building from source is a legal and officially documented path, not a license workaround.
- **FluidVoice** — free with no tiers, GPLv3 (since 2026-02-23; earlier versions Apache 2.0). The catch is the Fluid Intelligence / Fluid-1 layer: *"We're keeping Fluid Intelligence private for now so we can sustainably offer the core dictation experience for free."* The dictation itself is open source, the smart text enhancement is not — it runs locally, but it is a black box with an unclear future (today's "for now" reads like future monetization; that is an inference, not a fact).

For this context the resulting order is: VoiceInk (open source + documented Czech) > FluidVoice (free, but closed-source core of the added value) > Spokenly (free in the needed scope, but closed source) > Superwhisper (paid) > Wispr Flow (subscription forever).

## 4. Czech: what actually determines it

**Facts on support.** Whisper supports ~100 languages including Czech. NVIDIA Parakeet TDT 0.6b v3 supports 25 European languages and Czech (`cs`) is explicitly in the model card's list. Apple's "macOS Feature Availability" overview lists Czech among dictation languages, but **not** in the on-device / modeless dictation section and **not** in the auto-punctuation section — Czech system dictation therefore goes through an Apple server and punctuation must be spoken. Wispr Flow declares 100+ languages; the conversation's claim that only seven languages have full parity with English could not be traced to a primary source and is therefore not used in this document.

**Facts from the author's own testing (2026-08-18):** Wispr Flow handles Czech excellently, but on a fraction-of-a-second pause in speech it inserts an unwanted ", eh, " into sentences — a hesitation artifact its post-processing does not reliably filter in Czech. VoiceInk with Parakeet v3 is only a few percent worse in Czech than Wispr Flow — with no cloud, no subscription and no inserted "eh".

**Inference (untested):** because Superwhisper, Spokenly and FluidVoice run the same models (Whisper Large, Parakeet v3), the same chosen engine should give practically the same Czech transcript as in VoiceInk. This is an expectation derived from architecture, not a measured result — and it is marked 🟡 in the table as well. Direct Czech benchmarks for these apps practically do not exist; Whisper's published WER metrics mostly concern English, and for Czech a noticeably higher error rate must be expected.

## 5. Enhancement of dictated text

A raw transcript and a text ready to send are two different things — and the apps differ in **who and where** bridges that gap:

- **Wispr Flow:** automatic, always, in their cloud, with their models. Zero configuration, zero control — and in Czech it demonstrably lets hesitations through (§4).
- **Superwhisper:** modes with custom prompts; output can be routed through the LLM of your choice (the site names GPT, Claude, Llama among others; the free tier includes *"Unlimited use of small AI models"* and *"Custom prompt control"*).
- **Spokenly:** optional AI post-processing via own keys (OpenAI, Deepgram, Groq, Anthropic, Google) for free, or managed cloud in Pro.
- **macOS Dictation:** none — for Czech not even automatic punctuation (§4).
- **VoiceInk:** optional enhancement with custom prompts; the docs list the providers Groq, Cerebras, Gemini, OpenRouter and add *"OpenAI, Anthropic, Mistral, Gemini, Ollama, Local CLI, and custom OpenAI-compatible providers can also work."* Ollama means a fully local chain transcription → enhancement without a single packet leaving the machine.
- **FluidVoice:** automatic and fully local via Fluid-1 (a local AI runtime, §3) — cleanup, per-app tone, formatting. The most convenient local solution, but closed-source (§3).

For rule 4 of §1 the best outcomes are VoiceInk (full control, a 100% local chain possible) and Superwhisper; FluidVoice is more convenient, but you can swap neither the prompt nor the model.

## 6. Voice for AI coding agents

Given daily Claude Code use, this axis carries its own weight:

- **Spokenly** has the strongest declared integration: *"MCP server for AI coding agents (Claude Code, Cursor)"* plus voice-driven *"Agentic Actions"* for macOS automation.
- **Superwhisper** mentions use with *"Cursor, Claude Code, Open Code, Amp, Codex, or any other agentic coding app"* on its site.
- **VoiceInk** declares no agent-specific integration; its docs do list "Local CLI" among enhancement providers, i.e. hooking into local CLI tools. Practically speaking: dictating into a Claude Code prompt works in every one of these apps — they are system-wide inputs — a dedicated integration only adds things like voice commands for the agent.
- **Wispr Flow, macOS Dictation, FluidVoice** declare nothing agent-specific (for FluidVoice, a young project, this may change quickly).

This axis is the only one where the verdict sacrifices something: Spokenly would be the stronger choice for voice-controlling agents. The accepted trade-off is described in §8.

## 7. Dated snapshot: prices, models, versions (2026-08-18)

The fast-aging layer — the numbers hold as of the verification date and are not load-bearing for the verdict (which rests on §2–§5):

| | Wispr Flow | Superwhisper | Spokenly | macOS Dictation | VoiceInk | FluidVoice |
|---|---|---|---|---|---|---|
| Price | Pro $15 / mo, $12 / mo billed annually; free tier 2,000 words / week (desktop), 1,000 / week (iPhone) | free tier; Pro approx. $8.49 / mo, $84.99 / yr, lifetime $249.99 `[VERIFY]` — see the contradiction below | local + own keys free; Pro $9.99 / mo | free | Solo $29 (1 Mac) / Personal $49 (2) / Extended $69 (3), one-time; free from source | free |
| Minimum macOS | not checked | not checked | not checked | current macOS (Tahoe) | 14.4, Apple Silicon | 15.0 (Sequoia) |
| Local models | none | Whisper (incl. Large) | Whisper, Parakeet | system (server-side for Czech) | whisper.cpp, Parakeet (via FluidAudio) and more | Nemotron Speech 3.5, Parakeet Flash / TDT v3 / TDT v2, Whisper Tiny–Large, Apple Speech, Cohere Transcribe |
| GitHub stars | — | — | — | — | ~6,000 | ~10,600 |

**Contradiction on Superwhisper pricing:** the site did not yield the price in machine-readable form (extraction returns "$849" with no decimal point and no month / lifetime distinction). Secondary sources from mid-2026 agree on $8.49 / mo, $84.99 / yr and $249.99 lifetime; one source claims the lifetime rose to $849 in March 2026. I treat the repeatedly agreeing lower values as authoritative, but before any purchase the price list must be checked directly — hence the tag. The contradiction does not affect the verdict: Superwhisper is not eliminated on price but on closed source and its paid model (§3).

VoiceInk's prices changed shortly before this document was written according to the conversation (earlier mentions of higher tiers effective 2026-08-01 no longer appear on the site — the price list above is the site's current state as of the verification date).

## 8. Verdict

**VoiceInk, compiled from source** — in this context it wins as the only app that satisfies all four rules of §1 at once: Czech documented by the author's own test at only a few percent behind the best cloud (§4), fully local transcription (§2), zero cost via the officially supported build from source under GPL-3.0 (§3), and text enhancement with an own prompt through any provider including a fully local Ollama (§5).

Trade-offs accepted, knowingly:

- **Building from source = no automatic updates and no developer support.** Updating means fetching and compiling new sources. Anyone who does not want that buys Solo for $29 — still a fraction of Wispr Flow's yearly price.
- **Czech a few percent worse than Wispr Flow** (own measurement, §4). Hypothesis to try: a custom enhancement prompt for cleaning hesitations may shrink the gap further — unverified.
- **Solo developer, commercial interest alongside open source.** Mitigation: GPL-3.0 allows a fork, and local models keep working without the developer (§2).
- **No agent-specific integration** (§6). Dictating into prompts works regardless; if voice control of agents ever becomes a real need, Spokenly can be tried for free alongside — the two apps do not exclude each other.

**I will change my mind if:** (a) VoiceInk stops being maintained and the build stops compiling on current macOS — then FluidVoice, provided it has opened or replaced Fluid-1 by then, otherwise Spokenly; (b) Czech starts failing in practice on technical terminology badly enough to need a cloud engine — then Spokenly with BYOK keys before any return to Wispr Flow; (c) Wispr Flow ships a fully local mode with Czech — then a re-test is warranted, because it leads on Czech quality even now.

## References

Verified 2026-08-18 unless stated otherwise per entry.

**Wispr Flow**

- Pricing and free tier: <https://wisprflow.ai/pricing>
- Cloud-only processing and retention controls (source of the quote *"Transcription always occurs on the cloud."*): <https://wisprflow.ai/data-controls>

**Superwhisper**

- Site, free tier, platforms, Claude Code mention: <https://superwhisper.com>
- Pro / Lifetime prices: secondary sources in contradiction, see the open tag in §7 (i.a. <https://spokenly.app/blog/superwhisper-pricing> — beware, a competitor's blog)

**Spokenly**

- Site, pricing, MCP server, BYOK providers: <https://spokenly.app>

**macOS Dictation**

- Apple "macOS Feature Availability" — language lists for dictation, on-device dictation and auto-punctuation: <https://www.apple.com/macos/feature-availability/>

**VoiceInk**

- Site and pricing: <https://tryvoiceink.com>
- Sources, GPL-3.0 license, building from source: <https://github.com/Beingpax/VoiceInk>
- Recommended models and enhancement providers: <https://tryvoiceink.com/docs/recommended-models>
- iOS companion app: <https://tryvoiceink.com/ios>

**FluidVoice**

- Sources, license, models, Fluid Intelligence: <https://github.com/altic-dev/FluidVoice>

**Models**

- NVIDIA Parakeet TDT 0.6b v3 — 25 languages incl. Czech: <https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3>
- OpenAI Whisper — multilingual model incl. Czech: <https://github.com/openai/whisper>

---

*This document is a dated snapshot (2026-08-18) and is not retro-updated as its facts age. The prices and model lists in §7 will expire first; the verdict rests on the durable layer §2–§5.*
