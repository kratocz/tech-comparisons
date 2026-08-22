# Tech Comparisons

> Dated tech comparisons that end with a verdict for a concrete context — because the honest answer is always *"it depends"*, so each analysis spells out what it depends **on**.

## What this is

Real decision analyses from real projects — not neutral feature matrices. Each document:

- **anchors to a concrete context** — a "Context" section up front; the verdict claims validity only for that profile,
- **compares honestly** — including the rows where the losing side wins,
- **ends with a verdict once complete** — the option actually chosen, with the accepted trade-offs spelled out; analyses still under way are marked ⏳ in the table below,
- **is a dated snapshot** — facts carry a verification date and the document is not retro-updated.

## Comparisons

| Topic | Verdict (for that context) | Facts verified | Read |
|---|---|---|---|
| **ZFS vs Ceph** — storage engine for a small (1–3 node) self-hosted cluster | ZFS on Proxmox VE | 2026-07 · add. ×5, last 2026-08-14 | 🇬🇧 [English](zfs-vs-ceph/README.md) · 🇨🇿 [Čeština](zfs-vs-ceph/README.cs.md) |
| **Storage replication** — incremental replication between two clusters: ZFS `send`/`recv` vs Ceph RBD and CephFS mirroring | ZFS `zfs send -i` | 2026-08-13 | 🇬🇧 [English](storage-replication/README.md) · 🇨🇿 [Čeština](storage-replication/README.cs.md) |
| **Smartwatch platforms** — Garmin vs Apple vs Samsung, as input to an iPhone 15 Pro vs 16 Pro purchase decision | ⏳ in progress | 2026-08-09 (partial) | 🇨🇿 [Čeština](smartwatch-platforms/README.cs.md) |
| **Voice dictation** — Wispr Flow vs Superwhisper vs Spokenly vs macOS Dictation vs VoiceInk vs FluidVoice, for Czech dictation on an Apple Silicon Mac | VoiceInk (built from source) | 2026-08-18 | 🇬🇧 [English](voice-dictation/README.md) · 🇨🇿 [Čeština](voice-dictation/README.cs.md) |
| **Programming language choice** — one language to build new projects on for years, across web backend, browser frontend, CLI and data/ML | ⏳ in progress | 2026-08-22 (context and decision rules only; research not started) | 🇨🇿 [Čeština](programming-language-choice/README.cs.md) |

## Languages

English is canonical. Analyses that originated in Czech keep the Czech original alongside (`README.cs.md`). Drafts still in progress may exist in Czech only until the English version is written.

## Author

**Petr Kratochvíl** — [krato.cz](https://krato.cz). Researched and written with AI assistance (Claude); facts verified against the sources referenced in each document.

## License

[CC BY 4.0](LICENSE) — share and adapt with attribution.
