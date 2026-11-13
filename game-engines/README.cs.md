# Herní enginy: Unreal Engine vs Unity vs Godot

- **Typ:** neutrální přehled — bez verdiktu, končí průvodcem čtením (zatím nesepsán)
- **Fakta ověřena:** 🟡 zatím jen verze v §1.1 (2026-11-12 až 2026-11-13, reference v §2). Srovnávací tabulka zatím do dokumentu nevstoupila. Otevřená [OVĚŘIT] místa: přesné opravné buildy všech tří stabilních verzí a číslo bety Unity (§1.1)
- **Pořadí práce:** rozsah (§1) je sepsaný 2026-11-13, tedy **až po** průzkumné AI konverzaci z listopadu 2026, ne před ní. Zjištění z té konverzace se proto vedou jako hypotézy, ne jako fakta, a do dokumentu vstoupí až po ověření proti primárním zdrojům
- **Jazyk:** 🇨🇿 publikovaný pracovní draft (originál); 🇬🇧 kanonická anglická verze zatím nevznikla
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] rozsah (§1) — 2026-11-13
- [x] řádek v kořenovém README (2026-11-13)
- [ ] ověřovací kola po kategoriích z §1.2 proti primárním zdrojům, s připnutým buildem u každé hodnocené verze
- [ ] souhrnná tabulka „Srovnání v kostce“
- [ ] průvodce čtením: kde je který engine nejsilnější a jaký kontext volbu překlopí
- [ ] EN překlad (`README.md`) jako kanonická verze

## 1. Rozsah (sepsán 2026-11-13, před ověřováním)

Rozsah je zafixovaný teď, aby se pokrytí potichu nezúžilo na to, co se bude dobře hledat. Případné změny se zapíšou jako datované poznámky pod tuto sekci, ne jako přepis.

### 1.1 Možnosti a hodnocené verze

Pořadí sloupců jde **od nejrozsáhlejšího enginu po nejlehčí** a nic víc netvrdí — není to žebříček. Stejné pořadí platí ve všech tabulkách dokumentu.

| Engine | Stabilní verze (základ hodnocení) | Předběžná verze (hodnocená zvlášť, značka 🧪) |
|---|---|---|
| **Unreal Engine** | 5.8 [OVĚŘIT: poslední opravný build] | 5.9 Preview („MegaJam“), vydaná 2026-11-09 |
| **Unity** | 6.6 [OVĚŘIT: poslední opravný build] | 6.7 beta [OVĚŘIT: číslo bety]; Unity 7 je ve veřejné alfě, ale hodnotí se jen jako plán |
| **Godot** | 4.7.x [OVĚŘIT: poslední opravný build] | 4.8 beta 3 |

Základ tvoří stabilní verze. Co přinášejí jen předběžné verze, je v tabulkách označené 🧪, aby šlo poznat, co ve stabilní verzi ještě není. U 🧪 řádků platí zvláštní opatrnost: Unreal 5.9 Preview vznikl podle 80.lv zhruba za týden se zkráceným testováním (§2), takže se do finální verze může hodně změnit.

### 1.2 Otázky

Přehled odpovídá na tyto otázky, rozdělené do kategorií:

- **Základ:** licence a cena; přístup ke zdrojovému kódu; nároky editoru; stav verzí a ohlášený plán.
- **Programování:** jazyky; vizuální skriptování; rychlost iterace; co udělá chybný kód (null pointer a nekonečná smyčka) v editoru a v hotové hře.
- **Vývoj s AI:** jak čitelné jsou soubory projektu bez editoru; oficiální a komunitní MCP servery a jejich cena; vestavěný AI asistent a generování v editoru; rychlost smyčky „uprav, spusť, oprav“ pro agenta; jak spolehlivě AI píše jazyk enginu; práce bez otevřeného editoru.
- **Grafika a osvětlení:** dynamické globální osvětlení; GI s předvýpočtem; ray tracing; mnoho světel se stíny; plošná světla; virtualizovaná geometrie; HDR výstup.
- **2D:** vestavěné 2D nástroje.
- **Animace a postavy:** animační systémy; realistické postavy; filmové sekvence.
- **Fyzika a svět:** 3D a 2D fyzika; terén; otevřené světy.
- **Multiplayer a UI.**
- **Platformy:** PC, mobil, web, konzole, XR.
- **Ekosystém:** obchod s assety; komunita a výukové materiály.

### 1.3 Měřítko hodnocení

Tabulky budou používat **krátké popisné buňky**, ne symboly ✅/🟡/❌. Měřítkem je, **co engine umí vestavěně v hodnocené verzi**: bez placených assetů a pluginů třetích stran. Ty se zmíní zvlášť jen tam, kde podstatně mění obrázek (například dynamické GI v Unity). Buňky neváží pro žádného konkrétního čtenáře.

### 1.4 Mimo rozsah

- **Další enginy** (GameMaker, Defold, Construct, GDevelop, Bevy, O3DE, Flax, Stride a další) — aby přehled zůstal zvládnutelný.
- **Platformy uvnitř jiných her** (UEFN, Roblox Studio).
- **Vlastní výkonnostní měření.** Přehled se opírá o dokumentaci a poznámky k vydání, ne o benchmarky.
- **Ceny placených assetů a kurzů, pracovní trh.**
- **Unity 7 a Unreal Engine 6 jako hodnocené verze** — zmíní se jen jako ohlášený plán.
- **Verdikt pro konkrétní projekt.** Ten patří do samostatné rozhodovací analýzy, nebo do datované sekce připojené k tomuto přehledu s vlastním kontextem a pravidly (viz `AGENTS.md`).

### 1.5 Odkud pocházejí hypotézy

Výchozí hypotézy pocházejí z AI konverzace z listopadu 2026 a z tabulky, která v ní vznikla. Řádek do dokumentu vstoupí až po ověření proti primárnímu zdroji: poznámkám k vydání, dokumentaci výrobce nebo zdrojovému kódu. Sekundární zdroje (blogy, agregátory zpráv a weby firem, které samy prodávají MCP servery) slouží jen jako stopa, kde hledat.

## 2. Reference

Ověřeno 2026-11-12 až 2026-11-13; pokrývají zatím jen verze v §1.1.

- Unreal Engine 5.9 Preview — [poznámky k vydání](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes) (aktualizováno 2026-11-09) · [oznámení na fóru Epicu](https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840) · [80.lv: preview sestavený zhruba za týden](https://80.lv/articles/unreal-engine-5-9-preview-is-out-it-was-built-with-ai/)
- Unity 6.7 beta — [uživatelská příručka 6.7 Beta](https://docs.unity.com/en-us/engine/6000.7/manual) · [poznámky k 6000.7.0b2](https://unity.com/releases/editor/beta/6000.7.0b2)
- Unity 7 alfa — [poznámky k 7000.0.0a7](https://unity.com/releases/editor/alpha/7000.0.0a7)
- Godot 4.8 — [beta 1: přehled novinek](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/) · [beta 3](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-3/)

---

*Pracovní kostra založená 2026-11-13; rozsah sepsán před ověřováním, ale až po průzkumné AI konverzaci. Vzniká ve spolupráci s Claude (Anthropic).*
