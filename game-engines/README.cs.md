# Herní enginy: Unreal Engine vs Unity vs Godot

- **Typ:** neutrální přehled — bez verdiktu, končí průvodcem čtením (§3)
- **Fakta ověřena:** 🟡 2026-11-13: hodnocené verze (§1.1), všechny kategorie z §1.2 (§4–§12) a dodatečně přidaná cross-kompilace (§1.6, §11), odhady pro AI agenta rozepsané po jazycích včetně vizuálního skriptování (§6), reference v §13. Žádné místo k ověření nezůstalo otevřené, ale ne všechna jsou potvrzená: ze jedenácti šest uzavřel primární zdroj nebo vlastní test (u GDExtension zůstává pád editoru odvozený, §5), jedno jen sekundární zdroj (termín UE6, §4) a čtyři výslovné mlčení zdroje (2D fyzika v Unrealu a otevřené světy v Unity, §9; hostitelské systémy buildů v Unity a Godotu, §11). Řádky označené „odhad“ jsou odvození, ne měření (§6). 2026-11-14: termín plného vydání UE 5.9 (§2, §4)
- **Pořadí práce:** rozsah (§1) je sepsaný 2026-11-13, tedy **až po** průzkumné AI konverzaci z listopadu 2026, ne před ní. Zjištění z té konverzace se proto vedla jako hypotézy a do dokumentu vstoupila až po ověření proti zdrojům v §13
- **Jazyk:** 🇨🇿 publikovaný pracovní draft (originál); 🇬🇧 kanonická anglická verze zatím nevznikla
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] rozsah (§1) — 2026-11-13
- [x] řádek v kořenovém README (2026-11-13)
- [x] ověření všech kategorií z §1.2 proti zdrojům (§4–§12) — 2026-11-13
- [x] souhrnná tabulka „Srovnání v kostce“ (§2) a průvodce čtením (§3) — 2026-11-13
- [x] cross-kompilace (§11), přidaná změnou rozsahu v §1.6 — 2026-11-13
- [x] odhady pro AI agenta rozepsané po jazycích, včetně Blueprintů a Visual Scriptingu (§6) — 2026-11-13
- [x] uzavřít všechna otevřená místa k ověření — 2026-11-13; výsledek po jednotlivých místech je v hlavičce
- [ ] termín UE6 doložit primárním zdrojem (příspěvek Epicu odmítá automatické stažení, §4)
- [ ] EN překlad (`README.md`) jako kanonická verze

## 1. Rozsah (sepsán 2026-11-13, před ověřováním)

Rozsah je zafixovaný teď, aby se pokrytí potichu nezúžilo na to, co se bude dobře hledat. Případné změny se zapíšou jako datované poznámky (§1.6), ne jako přepis.

### 1.1 Možnosti a hodnocené verze

Pořadí sloupců jde **od nejrozsáhlejšího enginu po nejlehčí** a nic víc netvrdí — není to žebříček. Stejné pořadí platí ve všech tabulkách dokumentu.

| Engine | Stabilní verze (základ hodnocení) | Předběžná verze (hodnocená zvlášť, značka 🧪) |
|---|---|---|
| **Unreal Engine** | 5.8.4 — nejnovější hotfix řady 5.8 nalezený ve fóru Epicu k 2026-11-13 | 5.9 Preview („MegaJam“), vydaná 2026-11-09 |
| **Unity** | 6.6.8f1 (`6000.6.8f1`), vydaná 2026-11-03 | 6.7 beta 9 (`6000.7.0b9`); Unity 7 je ve veřejné alfě, ale hodnotí se jen jako plán |
| **Godot** | 4.7.2, vydaná 2026-08-18 | 4.8 beta 3 |

*Buildy připnuty 2026-11-13; doplněno do původní tabulky na místo značek k ověření, rozsah se tím nemění.*

Základ tvoří stabilní verze. Co přinášejí jen předběžné verze, je v tabulkách označené 🧪, aby šlo poznat, co ve stabilní verzi ještě není. U 🧪 řádků platí zvláštní opatrnost: Unreal 5.9 Preview vznikl podle 80.lv zhruba za týden se zkráceným testováním (§13), takže se do finální verze může hodně změnit.

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

Výchozí hypotézy pocházejí z AI konverzace z listopadu 2026 a z tabulky, která v ní vznikla. Řádek do dokumentu vstoupí až po ověření proti primárnímu zdroji: poznámkám k vydání, dokumentaci výrobce nebo zdrojovému kódu. Sekundární zdroje (blogy, agregátory zpráv a weby firem, které samy prodávají MCP servery) slouží jen jako stopa, kde hledat; kde na nich buňka přesto stojí, říká to §13.

### 1.6 Změny rozsahu (2026-11-13)

- Otázka „komunita a výukové materiály“ z kategorie Ekosystém se **vypouští**. Velikost komunity ani kvalitu výukových materiálů nejde doložit primárním zdrojem bez vlastního měření, takže by buňky byly jen dojmy.
- Do kategorie Platformy se **přidává** otázka, na kterém operačním systému jde sestavit build pro který cílový systém (cross-kompilace), pro Windows, macOS, Linux, Android a iOS/iPadOS. Výchozí hypotézy k ní pocházejí z jiné AI konverzace z 2026-11-11 a do §11 vstoupily až po ověření.

Zbytek rozsahu zůstává beze změny.

## 2. Srovnání v kostce

Popisné buňky podle §1.3, řazení sloupců podle §1.1. Buňky jsou zkrácené; zdroj a přesné znění každého řádku je v sekci uvedené v posledním sloupci. „Odhad“ odkazuje na odvození vysvětlené v té sekci, „dokumentace nezmiňuje“ na místo, kde zdroj mlčí.

| Vlastnost | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 | Detail |
|---|---|---|---|---|
| **▸ Základ** | | | | |
| Licence | Zdarma; 5 % z hrubých tržeb produktu nad 1 mil. USD (3,5 % při současném vydání na Epic Games Store) | Personal zdarma do 200 tis. USD příjmů a financování firmy; Pro 2 310 USD/rok za místo | MIT, zcela zdarma | §4 |
| Zdrojový kód | Dostupný i v bezplatné licenci, ale není open source | Jen Enterprise jako placený doplněk | Open source (MIT) | §4 |
| Nároky editoru | Doporučeno 32 GB RAM a 8 GB VRAM | Doporučeno minimálně 8 GB RAM | Minimum 4 GB RAM, editor kolem 200 MB | §4 |
| Ohlášený plán | 🧪 5.9 Preview; plné vydání 5.9 bez termínu, Epic zmiňuje „příští rok“ (2027); UE6 cílí na Early Access koncem 2027 (sekundární zdroj) | 🧪 6.7 jako LTS; Unity 7 ve veřejné alfě, plné vydání plánované na 1. čtvrtletí 2027 | 🧪 4.8 v betě, blíží se RC | §4 |
| **▸ Programování** | | | | |
| Jazyky | C++ a Blueprints; v UE6 přibude Verse | C# | GDScript, C#, C++ přes GDExtension; 🧪 4.8: C# vyžaduje .NET 10 | §5 |
| Vizuální skriptování | Blueprints; 🧪 5.9: Blueprinty jde vytvářet a upravovat i z Pythonu | Visual Scripting (balíček 1.9) | Ne — VisualScript zrušen ve 4.0; komunitní doplněk Orchestrator | §5 |
| Rychlost iterace | C++ vyžaduje kompilaci | Od 6.6 nové projekty vstupují do Play mode bez reloadu domény | GDScript bez kroku sestavení (odhad) | §5 |
| Null pointer: editor | C++: pád editoru (odvozeno). Blueprints: chyba „Accessed None“ v logu | Výjimka v konzoli, engine pokračuje dalším snímkem | Hra běží v samostatném procesu, editor nespadne | §5 |
| Null pointer: hotová hra | C++: pád hry (odvozeno). Blueprints: uzel selže | Výjimka do logu, hra pokračuje | Debug: chyba do logu, hra pokračuje. Release: bez výpisu; volání na typované proměnné s `null` hru shodí (vlastní test) | §5 |
| Nekonečná smyčka: editor | C++: zamrzne editor (odvozeno). Blueprints: přerušeno po limitu iterací | Zamrzne celý editor | Zamrzne jen hra, editor ji ukončí | §5 |
| Nekonečná smyčka: hotová hra | Hra zamrzne (odvozeno) | Hra zamrzne (odvozeno) | Hra zamrzne (odvozeno) | §5 |
| **▸ Vývoj s AI** | | | | |
| Soubory projektu | Binární `.uasset`; 🧪 5.9: GraphDsl, textový zápis grafových assetů | Scény a prefaby jako YAML (výchozí „Force Text“) | Scény `.tscn` jako čitelný text | §6 |
| MCP server | Oficiální (od 5.8 experimentální); 🧪 5.9: víc sad nástrojů včetně Blueprintů a výkonu | Oficiální, součást Unity AI | Jen komunitní | §6 |
| Cena MCP | Zdarma | Předplatné Unity AI (14 dní zdarma); počet souběžných připojení podle plánu | Komunitní servery zdarma nebo za jednorázový poplatek | §6 |
| AI asistent v editoru | 🧪 5.9: Unreal Assistant, Unreal Canvas, napojení na Claude Code | Unity AI: asistent, generátory assetů | Přehledy novinek 4.7 ani 4.8 žádný nezmiňují | §6 |
| Práce bez editoru | Python skripty editoru | `-batchmode` s `-executeMethod` | `--headless` | §6 |
| Smyčka agenta (odhad) | Nejpomalejší — kompilace C++ | Střední — rekompilace C# | Nejrychlejší — skripty bez sestavení | §6 |
| Jazyk z pohledu AI (odhad) | C++: nejvíc chyb napoprvé (makra reflexe, závislosti modulů) | C#: nejméně chyb napoprvé | GDScript: plete se syntaxe Godotu 3 a 4 | §6 |
| Napojení kódu na scénu (odhad) | Jen přes editor nebo jeho nástroje (binární `.uasset`) | Ručně v YAML přes `fileID` a `guid`, křehké | Přímo v textu `.tscn` | §6 |
| Vizuální skriptování z pohledu AI (odhad) | Blueprints bez editoru mimo dosah; 🧪 5.9: Python, MCP a GraphDsl | Visual Scripting: textový zápis ani nástroje pro AI nenalezeny | — | §6 |
| **▸ Grafika a osvětlení** | | | | |
| Dynamické GI | Lumen; 🧪 5.9: Lumen World Cache (vyžaduje HW ray tracing) | Ve stabilní verzi jen Enlighten s předvýpočtem a končící podporou; 🧪 6.7: Surface Cache GI | SDFGI (jen Forward+); 🧪 4.8: vícenásobné odrazy v ambient occlusion | §7 |
| GI s předvýpočtem | Lightmapy | Lightmapy, Adaptive Probe Volumes | LightmapGI, VoxelGI; 🧪 4.8: směrové lightmapy se spekulárem | §7 |
| Ray tracing | Hardwarový ray tracing v enginu (mj. Lumen) | V HDRP, které je v režimu údržby | Jen nízkoúrovňové API RenderingDevice | §7 |
| Hodně světel se stíny | MegaLights (od 5.8 připravené pro produkci) | Obdobu MegaLights dokumentace nezmiňuje | Obdobu MegaLights dokumentace nezmiňuje | §7 |
| Plošná světla | Rect Light, i plně dynamické | URP jen zapečená, v reálném čase jen HDRP | AreaLight3D od 4.7 | §7 |
| Virtualizovaná geometrie | Nanite; 🧪 5.9: rychlejší culling | Ne; automatické LODy (Mesh LOD od 6.2) | Ne; automatické LODy | §7 |
| HDR výstup na monitor | Ano; s D3D11 jen v exkluzivním režimu celé obrazovky | Ano, v URP; v HDRP podle dokumentace balíčku | Ano, od 4.7 | §7 |
| **▸ 2D** | | | | |
| 2D nástroje | Paper2D, jen údržba | Samostatná, aktivně vyvíjená 2D sada | Samostatný 2D engine s 2D světly, tilemapami a 2D fyzikou | §8 |
| **▸ Animace a postavy** | | | | |
| Animace | Control Rig, Motion Matching a další; 🧪 5.9: generování animací pomocí AI | Mecanim, 2D kosterní animace | AnimationPlayer, AnimationTree; IK framework od 4.6 | §8 |
| Realistické postavy | MetaHuman | Dokumentace vestavěnou obdobu nezmiňuje | Dokumentace vestavěnou obdobu nezmiňuje | §8 |
| Filmové sekvence | Sequencer, Movie Render Graph | Timeline, Cinemachine | AnimationPlayer | §8 |
| **▸ Fyzika a svět** | | | | |
| 3D fyzika | Chaos | NVIDIA PhysX | Jolt (výchozí od 4.6); 🧪 4.8: Jolt 5.6 | §9 |
| 2D fyzika | Běžná fyzika zamčená do roviny; samostatnou 2D fyziku dokumentace nezmiňuje | Box2D | Vlastní 2D fyzika | §9 |
| Terén | Landscape, Mesh Terrain | Terrain a balíček Terrain Tools | Vestavěný terén dokumentace nezmiňuje; řeší se pluginy | §9 |
| Otevřené světy | World Partition, PCG | Automatické dělení světa dokumentace nezmiňuje; streamování subscén v balíčku Entities | Bez vestavěného streamování scén; 🧪 4.8: streamování textur po mip úrovních | §9 |
| **▸ Multiplayer a UI** | | | | |
| Multiplayer | Replikace v jádru enginu | Netcode for GameObjects / for Entities | High-level multiplayer API | §10 |
| UI | UMG a Common UI | UI Toolkit a uGUI | Control uzly; editor je sám postavený v Godotu | §10 |
| **▸ Platformy** | | | | |
| Mobil | Android, iOS | Android, iOS | Android, iOS; 🧪 4.8: editor sám nastaví Android SDK | §11 |
| Web | Ve 5.8 ne; 🧪 5.9: experimentální cíl WebAssembly s WebGPU | Ano (WebGL 2.0) | Ano, jen WebGL 2.0 přes Compatibility; projekty v C# ne | §11 |
| Konzole | Po schválení výrobcem konzole, Epic si za přístup neúčtuje | Vyžaduje Unity Pro | Jen přes třetí strany (W4 Games a další) | §11 |
| XR | VR i AR | Včetně Apple Vision Pro (s Pro) | OpenXR; 🧪 4.8: visionOS jako modul | §11 |
| Build pro jiný OS | Windows → Linux oficiálním toolchainem; iOS z Windows jen vzdáleně přes Mac; jinak build na cílovém OS | S Mono z kteréhokoli desktopu; s IL2CPP z jiného OS jen Linux; iOS přes Xcode na Macu | Desktop i Android z libovolného OS díky předkompilovaným šablonám; iOS jen z macOS | §11 |
| **▸ Ekosystém** | | | | |
| Obchod s assety | Fab | Asset Store | Asset Store, nový ve 4.7 | §12 |

## 3. Jak tabulku číst

Tabulka nevybírá vítěze; říká, kde je který engine nejsilnější, a které vlastnosti kontextu volbu mezi nimi překlápějí.

- **Unreal Engine je nejsilnější tam, kde rozhoduje vestavěná 3D technologie:** dynamické GI, virtualizovaná geometrie, mnoho světel se stíny, realistické postavy a nástroje pro otevřené světy (§7–§9). Licence nic nestojí, dokud jednotlivý produkt neutrží milion dolarů (§4). Platí se za to nejtěžším editorem, nativním C++ v procesu editoru (§5) a binárními assety, které AI bez editoru nečte (§6).
- **Unity je nejsilnější v šíři cílových platforem a v nástrojích kolem nich:** mobil, web ve stabilní verzi, XR včetně Vision Pro a samostatná 2D sada (§8, §11). Scény jsou text a MCP je oficiální (§6). Licence se ale odvíjí od příjmů a financování celé firmy a konzole i Vision Pro vyžadují Pro (§4, §11); dynamické GI je zatím jen v betě (§7).
- **Godot je nejsilnější v nákladech, lehkosti a průhlednosti:** MIT bez poplatků, malý editor, hra izolovaná v samostatném procesu a scény jako čitelný text (§4–§6). Ve 2D je rovnocenný Unity (§8). Ve 3D osvětlení zaostává hlavně tam, kde Unreal a Unity mají vestavěné high-end technologie (§7), a konzole jsou jen přes třetí strany (§11).

Vlastnosti kontextu, které volbu překlápějí nejvíc:

- **Cílová platforma a build stroj.** Web ve stabilní verzi mají jen Unity a Godot; konzole nejsnáz Unreal a Unity. Kdo chce buildit pro víc systémů z jednoho počítače, má nejvíc volnosti v Godotu a nejmíň v Unrealu; pro iOS potřebují Mac všechny tři, Unity ho umí nahradit sestavením v cloudu přes Unity Build Automation (§11).
- **Výtvarný styl.** Realistické 3D s dynamickým světlem táhne k Unrealu; stylizované 3D a 2D tenhle rozdíl nepotřebují (§7–§8).
- **Peníze a financování.** U Unrealu rozhodují tržby produktu, u Unity příjmy a investice celé firmy, u Godotu nic (§4).
- **Vývoj převážně s AI.** Textové scény a izolovaný proces hry mluví pro Godot a Unity, binární assety proti Unrealu; 🧪 Unreal 5.9 ten rozdíl zmenšuje (§6). Víc než volba enginu tu váží volba jazyka: textový kód AI zvládá ve všech třech, kdežto Blueprints a Visual Scripting jsou pro ni bez nástrojů editoru mimo dosah (odhad, §6).
- **Jazyk.** C++, C# a GDScript jsou tři různé světy a znalost jednoho z nich je sama o sobě důvod (§5).

## 4. Základ

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| **▸ Licence a cena** | | | |
| Licence | Zdarma. Hry a jiné produkty s kódem enginu platí 5 % z celoživotních hrubých tržeb produktu nad 1 mil. USD, bez ohledu na to, kdo tržby inkasuje; tržby z Epic Games Store jsou bez poplatku ([licence](https://www.unrealengine.com/en-US/license)) | Unity Personal zdarma do 200 tis. USD příjmů a financování za posledních 12 měsíců, nad tím Pro za 2 310 USD/rok nebo 210 USD/měsíc za místo, nad 25 mil. USD Enterprise ([ceník 2026](https://unity.com/en/products/pricing-updates)). Licence je čistě za místa, z tržeb her se neplatí ([oznámení 2024](https://www.tipranks.com/news/the-fly/unity-ceo-says-canceling-runtime-fee-announces-pricing-changes)) | MIT, zcela zdarma, bez poplatků z tržeb ([Godot](https://godotengine.itch.io/)) |
| Výjimky a slevy | Čtvrtletí, kdy produkt utrží méně než 10 000 USD, je bez poplatku ([EULA change log](https://www.unrealengine.com/eula-change-log/unreal)). Sazba 3,5 % místo 5 % na všech platformách, když hra vyjde na Epic Games Store nejpozději současně s ostatními obchody (program Launch Everywhere with Epic, hry vydané od 2025-01-01) ([Epic](https://www.unrealengine.com/news/unreal-engines-improved-royalty-reporting-system)) | Pro a Enterprise zdražily od 2026-01-12 o 5 %; Unity ohlašuje každoroční úpravy cen ([ceník 2026](https://unity.com/en/products/pricing-updates)) | — |
| Neherní komerční použití | Firmy s tržbami nad 1 mil. USD za 12 měsíců, které nedistribuují aplikaci s kódem enginu koncovým uživatelům: 1 850 USD/rok za místo ([vlastní licence](https://www.unrealengine.com/en-US/custom-license)) | Zákazníci z kategorie Industry nemohou použít Personal ([srovnání plánů](https://unity.com/compare-plans)) | — |
| **▸ Zdrojový kód** | | | |
| Přístup | Přístup ke zdrojovému kódu je součástí bezplatné licence ([licencování](https://www.unrealengine.com/en-us/custom-licensing)); engine se distribuuje i přes GitHub ([oznámení 5.8](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274)) | Jen Enterprise, jako placený doplněk „Source Code Access (read only)“ nebo „Source Code Adapt“ ([srovnání plánů](https://unity.com/compare-plans)) | Otevřený pod licencí MIT ([Godot](https://godotengine.itch.io/)) |
| **▸ Nároky editoru** | | | |
| Hardware | Doporučeno 32 GB RAM, grafika s 8 GB VRAM, čtyřjádrový procesor od 2,5 GHz, Windows 11 ([specifikace](https://dev.epicgames.com/documentation/unreal-engine/hardware-and-software-specifications-for-unreal-engine?lang=en-US)) | Pro běh editoru na Windows, macOS i Linuxu doporučeno minimálně 8 GB RAM (dokumentace 6.3, [systémové požadavky](https://docs.unity.com/en-us/engine/6000.3/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements)) | Minimum pro nativní editor 4 GB RAM (dokumentace 4.6, [systémové požadavky](https://docs.godotengine.org/en/4.6/about/system_requirements.html)); editor kolem 200 MB, exportní šablony dalších 1,3 GB (dokumentace 4.5, [systémové požadavky](https://docs.godotengine.org/en/4.5/about/system_requirements.html)) |
| **▸ Verze a plán** | | | |
| Hodnocený build | 5.8.4 ([hotfix](https://forums.unrealengine.com/t/5-8-4-hotfix-released/2842775)) | 6000.6.8f1, vydaná 2026-11-03 ([poznámky](https://unity.com/vn/releases/editor/whats-new/6000.6.8f1)) | 4.7.2, vydaná 2026-08-18, na GitHubu vedená jako nejnovější vydání ([vydání](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable)) |
| 🧪 Předběžná verze | 5.9 Preview „MegaJam“ ([poznámky](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | 6000.7.0b9 ([beta program](https://unity.com/vn/releases/editor/beta)) | 4.8 beta 3 ([oznámení](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-3/)) |
| Ohlášený plán | 5.8 byla ohlášena jako poslední plánovaná velká verze UE5, s výhradou případných dalších oficiálních vydání ([Epic](https://www.unrealengine.com/ja/news/unreal-engine-5-8-is-now-available)) — tou se stala 5.9. Plné vydání 5.9 nemá k 2026-11-14 ohlášený termín: poznámky k vydání 5.9 Preview žádný neuvádějí a oznámení preview ve fóru Epicu (2026-11-09) píše jen o změnách sbíraných *"for an eventual 5.9 release next year"*, a to o plánu z doby před rozhodnutím vydat preview; „příští rok“ tedy znamená 2027 (odvozeno z data příspěvku). Totéž oznámení uvádí, že části webového rendereru jsou *"prototypes we plan to refactor before the full 5.9 release ships"* ([fórum Epicu](https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840)). UE6 cílí na Early Access koncem 2027: *"targeting an early access release at the end of 2027"* (sekundární zdroj: [PocketGamer.biz](https://www.pocketgamer.biz/epic-games-outlines-its-vision-for-unreal-engine-6/); příspěvek Epicu [The Road to UE6](https://www.unrealengine.com/news/the-road-to-ue-6) automatické stažení odmítá, takže ho přehled nečetl) | 6.7 má být LTS a poslední verzí na Mono ([Unity, červen 2026](https://discussions.unity.com/t/coreclr-scripting-and-serialization-update-june-2026/1723299)); Unity 7 je ve veřejné alfě ([7000.0.0a7](https://unity.com/releases/editor/alpha/7000.0.0a7)), plné vydání je naplánované na 1. čtvrtletí 2027: *"Full Release scheduled for Q1 2027"* ([Unity, červenec 2026](https://unity.com/news/unity-7-roadmap-revealed-at-unite-seoul)) | 4.8 je ve fázi bety s blížícím se RC ([beta 3](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-3/)) |

Dvě věci k tabulce, které se v buňkách nevejdou:

- **Co se počítá do limitu.** U Unrealu je limit 1 mil. USD na **produkt** a počítají se jeho hrubé tržby, tedy i podíl, který si strhne obchod (fakt podle licence). U Unity je limit 200 tis. USD na **organizaci** a počítají se příjmy i získané financování celé firmy (fakt podle ceníku). Oba limity se proto nedají srovnávat jedním číslem: malé studio s investicí přes 200 tis. USD platí Unity Pro dřív, než prodá jedinou kopii, kdežto u Unrealu by s takovou investicí neplatilo nic, dokud hra neutrží milion (inference z obou podmínek).
- **Zdrojový kód u Unrealu není open source.** Přístup ke kódu je volný, ale řídí se licencí Epicu, ne svobodnou licencí jako u Godotu (inference z toho, že přístup je popsaný jako součást licence Epicu).

## 5. Programování

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| **▸ Jazyky a skriptování** | | | |
| Jazyky | C++ a Blueprints; 🧪 5.9: nové knihovny pro Python a Blueprinty umožňují vytvářet a upravovat Blueprinty, grafy a uzly ze skriptů ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | C# | GDScript, C# a C++ přes GDExtension ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)); 🧪 4.8: build s C# vyžaduje .NET 10 ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| Vizuální skriptování | Blueprints | Visual Scripting, balíček 1.9 ([příručka 1.9](https://docs.unity3d.com/Packages/com.unity.visualscripting@1.9/manual/index.html)) | Vestavěné ne: VisualScript byl ve 4.0 odstraněn, protože ho podle ankety jako hlavní jazyk používalo jen 0,5 % uživatelů ([Godot](https://godotengine.org/article/godot-4-will-discontinue-visual-scripting)). Existuje komunitní doplněk Orchestrator ([fórum Godotu](https://forum.godotengine.org/t/heard-about-visual-scripting-but-cant-find-it/66967)) |
| Rychlost iterace | C++ vyžaduje kompilaci; Blueprinty se kompilují v editoru | Od 6.6 nové projekty ve výchozím stavu vstupují do Play mode jen s reloadem scény, bez reloadu domény ([Unity 6.6](https://discussions.unity.com/t/unity-6-6-is-now-available/1735357)) | GDScript se interpretuje bez samostatného kroku sestavení projektu (odhad z povahy jazyka) |
| **▸ Chybný kód** | | | |
| Null pointer: editor | C++: herní modul běží v procesu editoru, takže neošetřená dereference nulového ukazatele shodí editor (odvozeno z nativního kódu ve stejném procesu). Blueprints: chyba „Blueprint Runtime Error: Accessed None“ v logu, běh pokračuje | Unity výjimku zachytí, zaloguje a pokračuje dalším snímkem ([Jackson Dunstan](https://www.jacksondunstan.com/articles/5344)) | Hra vždy běží v samostatném procesu, takže její pád nepoloží editor ([dokumentace](https://docs.godotengine.org/en/stable/tutorials/editor/game_embedding.html)). Výjimkou jsou skripty `@tool`, které běží v editoru a podle dokumentace ho mohou shodit: *"the editor does not include protections for potential misuse of `@tool` scripts"* ([kód v editoru, dokumentace 4.7](https://docs.godotengine.org/en/4.7/tutorials/plugins/running_code_in_the_editor.html)). Totéž platí pro GDExtension: editor nativní knihovny načítá a po rekompilaci znovu nahrává ([příklad GDExtension v C++, zdroj dokumentace 4.7](https://raw.githubusercontent.com/godotengine/godot-docs/4.7/tutorials/scripting/cpp/gdextension_cpp_example.rst)), takže chyba v nich shodí editor (odvozeno, dokumentace pád nezmiňuje) |
| Null pointer: hotová hra | C++: pád hry (odvozeno). Blueprints: uzel selže, hra pokračuje | Výjimka do logu, hra pokračuje dalším snímkem (tentýž zdroj) | Záleží na typu buildu. V debug exportu se chyba zaloguje (`SCRIPT ERROR`), funkce skončí a hra pokračuje. V release exportu se nic nezaloguje: volání metody na netypované proměnné s `null` i přístup k vlastnosti na `null` projdou a funkce **pokračuje dalšími řádky**, kdežto volání metody na typované proměnné (`var n: Node = null`) hru **shodí** (segfault). Vlastní test na Godotu 4.7.2, export pro macOS, 2026-11-13 ([test](tests/godot-null-release/run.sh)). Zdrojový kód vysvětluje chybějící výpis: kontroly i výpis chyb ve VM GDScriptu leží uvnitř `#ifdef DEBUG_ENABLED` ([`gdscript_vm.cpp`, 4.7.2](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/modules/gdscript/gdscript_vm.cpp)), který mají jen buildy `editor` a `template_debug` ([`SConstruct`, 4.7.2](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/SConstruct)). Dokumentace o tom mlčí |
| Nekonečná smyčka: editor | C++: zamrzne editor (odvozeno). Blueprints: smyčku přeruší limit iterací, nastavitelný v Project Settings jako „Maximum Loop Iteration Count“ ([Epic](https://answers.unrealengine.com/questions/237724/view.html)) | Zamrzne celý editor; Unity takové hlášení uzavírá jako „By Design“ s vysvětlením, že šlo o nekonečnou smyčku ve skriptu projektu ([issue tracker](https://issuetracker.unity3d.com/issues/editor-freezes-occasionally-when-entering-play-mode-while-using-procedural-generation)) | Zamrzne jen hra v samostatném procesu (odvozeno z [dokumentace](https://docs.godotengine.org/en/stable/tutorials/editor/game_embedding.html)) |
| Nekonečná smyčka: hotová hra | Hra zamrzne | Hra zamrzne | Hra zamrzne |

Poslední řádek je odvození, ne zdroj: smyčka bez konce na hlavním vlákně zastaví hru v každém z enginů a žádný z nalezených zdrojů netvrdí opak. Rozdíly mezi enginy jsou proto skoro výhradně v editoru.

## 6. Vývoj s AI

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| **▸ Čitelnost projektu** | | | |
| Soubory projektu | Assety (`.uasset`) jsou binární a nejdou sloučit (sekundární zdroj: [glosář](https://usourcecontrol.com/glossary/uasset)). 🧪 5.9 přidává GraphDsl, textový jazyk pro tvorbu a úpravy grafových assetů ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Při režimu „Force Text“, výchozím pro nové projekty, se scény a prefaby ukládají jako YAML ([JetBrains Rider](https://www.jetbrains.com/help/rider/Asset-serialization-mode.html)) | Scény `.tscn` jsou podle dokumentace převážně čitelné pro lidi a snadno spravovatelné ve verzovacích systémech ([dokumentace](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)); 🧪 4.8 čistší serializace s menšími diffy ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| **▸ Napojení AI** | | | |
| MCP server | Oficiální plugin od 5.8 ([oznámení 5.8](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274)). 🧪 5.9: sady nástrojů pro Blueprinty, akce editoru, výkon, soubory, snímání scény, konzoli a další, registr nástrojů a MCP klient ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Oficiální Unity MCP v rámci Unity AI ([dokumentace](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.5/manual/integration/unity-mcp-get-started.html)) | Jen komunitní, například `godot-mcp` od Coding-Solo pod MIT nebo novější `shin2344234/godot-mcp` s režimem `--headless` ([přehled](https://ziva.sh/blogs/godot-mcp-server-claude-code-cursor) od prodejce MCP serveru, [vydání](https://github.com/shin2344234/godot-mcp/releases)) |
| Cena MCP | Zdarma, součást enginu | Unity AI vyžaduje předplatné, zkušební doba 14 dní; plány se liší počtem souběžných MCP připojení ([ceník](https://unity.com/simulation)) | Komunitní servery zdarma nebo za jednorázový poplatek (tentýž [přehled](https://ziva.sh/blogs/godot-mcp-server-claude-code-cursor)) |
| AI asistent v editoru | 🧪 5.9: Unreal Assistant, Unreal Canvas s generátory textu, obrázků, videa a meshí a napojení mj. na Claude Code ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Unity AI s nástroji pro generování kódu, tvorbu assetů a inferenci za běhu ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | Přehledy novinek 4.7 ani 4.8 vestavěného asistenta nezmiňují ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| Práce bez editoru | Python skripty editoru, 🧪 v 5.9 rozšířené ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | `-batchmode` s `-executeMethod` ([dokumentace](https://docs.unity3d.com/es//Manual/CommandLineArguments.html)) | `--headless` ([příkazová řádka](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html)) |
| **▸ Odhady** | | | |
| Smyčka agenta (odhad) | Nejpomalejší: každá změna C++ znamená kompilaci | Střední: změna C# znamená rekompilaci skriptů. Kompilaci i testy (`-runTests`) jde pustit v `-batchmode`, ale ne nad projektem, který má otevřený editor: *"You can't open a project in batch mode while the Editor has the same project open"* (dokumentace 6.3, [příkazová řádka](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor), [testy z příkazové řádky](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/test-framework-introduction/reference-command-line)) | Nejrychlejší: GDScript bez kroku sestavení, malý engine; `--check-only` se `--script` skript jen zkontroluje na chyby a skončí ([příkazová řádka](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html)) |
| Jazyk z pohledu AI (odhad) | C++ s makry reflexe enginu (`UCLASS`, `UPROPERTY`); nejvíc chyb napoprvé v makrech, v závislostech modulů v `Build.cs` a v API, které se mezi verzemi mění. Chyby ale vrací kompilátor přesně | C#: staticky typovaný jazyk se stabilním API; nejméně chyb napoprvé | GDScript; syntaxe se mezi Godotem 3 a 4 změnila ([migrace na Godot 4](https://docs.godotengine.org/en/4.7/tutorials/migrating/upgrading_to_godot_4.html)), takže AI plete tvary obou verzí. Dynamické typy ukážou část chyb až za běhu |
| Napojení kódu na scénu (odhad) | Odkazy assetů na třídy C++ a podtřídy Blueprintů leží v binárních `.uasset`, takže je AI nastaví jen přes editor nebo jeho nástroje (MCP, Python) | Pole `[SerializeField]` se nastavují v Inspectoru; v YAML scény jsou to odkazy přes `fileID` a `guid`, které AI upraví i ručně, ale chybný odkaz se ukáže až v editoru | Scéna `.tscn` odkazuje na skripty a uzly v čitelném textu, takže AI upraví skript i scénu stejným způsobem |
| Vizuální skriptování z pohledu AI (odhad) | Blueprints: bez editoru je AI nepřečte ani neupraví, protože jsou v binárních `.uasset`. 🧪 5.9: knihovny pro Python, sady nástrojů MCP pro Blueprinty a GraphDsl tuhle cestu otevírají (§5 a řádky výše); jak spolehlivě, přehled neměřil | Visual Scripting: grafy jsou assety `ScriptGraphAsset` ([API 1.9](https://docs.unity3d.com/Packages/com.unity.visualscripting@1.9/api/Unity.VisualScripting.ScriptGraphAsset.html)). Textový zápis grafů ani nástroje pro jejich úpravu z AI přehled nenašel a rozcestník příručky 1.9 způsob uložení grafů nepopisuje | — (vestavěné vizuální skriptování není, §5) |

Čtyři poslední řádky jsou **odhady, ne měření**. Odvozují se z toho, jak dlouhý krok sestavení engine vyžaduje, jak specifický je jeho jazyk a v jakém formátu ukládá scény a grafy; doplňuje je sebehodnocení AI agenta (Claude, 2026-11-13), které je hypotéza, ne zdroj. Přehled nemá benchmark, který by rychlost a spolehlivost práce AI agenta v jednotlivých enginech měřil (§1.4).

Seřazené po jazycích místo po enginech dávají ty řádky toto pořadí, od nejsnazšího pro AI agenta (odhad):

1. **GDScript** a **C# v Unity** zhruba nastejno. C# vede ve správnosti napoprvé, GDScript v rychlosti ověření a v tom, že AI upraví i scénu, na kterou kód napojuje.
2. **C++ v Unrealu.** Kód je text a kompilátor chyby vrací přesně, takže oprava konverguje, jen pomalu; napojení na assety ale vede přes editor.
3. **Blueprints.** Bez editoru mimo dosah; s nástroji z 5.9 (🧪) se mohou posunout výš, pokud se v praxi osvědčí.
4. **Visual Scripting v Unity.** Bez editoru mimo dosah a bez nalezených nástrojů, které by AI k úpravě grafů dávaly.

## 7. Grafika a osvětlení

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| **▸ Globální osvětlení** | | | |
| Dynamické GI | Lumen; 🧪 5.9: Lumen World Cache, který si cache osvětlení staví za běhu path tracingem a vyžaduje hardwarový ray tracing ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Ve stabilní verzi jen Enlighten Realtime GI, který potřebuje předvýpočet a jehož podpora podle srovnání pipeline končí po Unity 2024 LTS ([srovnání pipeline](https://docs.unity.cn/Documentation/Manual/render-pipelines-feature-comparison.html)). 🧪 6.7: Surface Cache GI ([dokumentace 6.7](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/surface-cache-gi-volume-override-reference.html)) | SDFGI, jen v rendereru Forward+ ([dokumentace](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_sdfgi.html)); 🧪 4.8: levná aproximace vícenásobných odrazů v ambient occlusion ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| GI s předvýpočtem | Lightmapy | Lightmapy a Adaptive Probe Volumes ([srovnání pipeline](https://docs.unity.cn/Documentation/Manual/render-pipelines-feature-comparison.html)) | LightmapGI a VoxelGI ([úvod do GI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/introduction_to_global_illumination.html)); 🧪 4.8: směrové lightmapy i se spekulárním světlem ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| Ray tracing | Hardwarový ray tracing v enginu, mj. pro Lumen ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | V HDRP, které od strategie z února 2026 přechází do režimu údržby ([80.lv](https://80.lv/articles/unity-unveils-2026-render-pipelines-strategy/)) | Jen nízkoúrovňové API v RenderingDevice ([Phoronix](https://phoronix.com/news/godot-4.7-dev-1-vulkan-rt)) |
| **▸ Světla a geometrie** | | | |
| Hodně světel se stíny | MegaLights, od 5.8 ve stavu připraveném pro produkci ([poznámky 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)) | Obdobu MegaLights dokumentace nezmiňuje (zdroj mlčí) | Obdobu MegaLights dokumentace nezmiňuje (zdroj mlčí) |
| Plošná světla | Rect Light; v režimu Movable plně dynamické: *"None of its direct or indirect illumination is baked by Lightmass at all."* ([Rect Light, dokumentace 5.9](https://dev.epicgames.com/documentation/unreal-engine/rectangular-area-lights-in-unreal-engine)) | V URP se plošné světlo automaticky přepne na zapečené ([dokumentace URP](https://docs.unity3d.com/Manual/urp/light-component.html)); dynamická plošná světla má jen HDRP ([převod HDRP na URP](https://docs.unity3d.com/6000.5/Documentation/Manual/urp/convert-hdrp-lighting-to-urp.html)) | AreaLight3D od 4.7 ([Phoronix](https://www.phoronix.com/news/Godot-4.7-Released)) |
| Virtualizovaná geometrie | Nanite; 🧪 5.9: rychlejší culling ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Ne; automatické generování LOD při importu od 6.2 ([Mesh LOD](https://docs.unity3d.com/6000.2/Documentation/Manual/lod/mesh-lod-generate-lods.html)) | Ne; automatické generování LOD ([dokumentace](https://docs.godotengine.org/en/4.7/tutorials/3d/mesh_lod.html)) |
| HDR výstup na monitor | Ano, přes `r.HDR.EnableHDROutput` *"on platforms that supports it"*; stránka výslovně jmenuje Windows (D3D11, D3D12) a Mac, úplný seznam platforem nemá. S D3D11 jen v exkluzivním režimu celé obrazovky ([HDR Display Output, dokumentace 5.9](https://dev.epicgames.com/documentation/en-us/unreal-engine/high-dynamic-range-display-output-in-unreal-engine)) | Ano, HDR Output. V URP na Windows (DirectX 11, DirectX 12, Vulkan), macOS (Metal), iOS 16+, Androidu (Vulkan, GLES), konzolích a XR, jen s lineárním barevným prostorem; s DirectX 11 jen v přehrávači, ne v editoru ([HDR Output v URP 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/materials-and-shaders/graphics-color/hdr/hdr-in-urp/hdr-output)). HDRP podle dokumentace balíčku 17.0 ([HDR Output v HDRP](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/HDR-Output.html)); že jde o verzi dodávanou s 6.6, přehled neověřil | Ano, od 4.7 ([Phoronix](https://www.phoronix.com/news/Godot-4.7-Released)) |

## 8. 2D, animace a postavy

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| **▸ 2D** | | | |
| 2D nástroje | Paper2D: Epic na něm aktivně nepracuje a jen ho udržuje ([fórum Epicu](https://forums.unrealengine.com/t/paper2d/95809)) | Samostatná 2D sada; 6.6 přidala rendering layers pro 2D světla a profilovací moduly pro 2D ([Unity 6.6](https://discussions.unity.com/t/unity-6-6-is-now-available/1735357)) | Samostatný 2D engine s 2D světly a stíny, tilemapami a 2D fyzikou ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)) |
| **▸ Animace a postavy** | | | |
| Animace | Control Rig, Pose Search (motion matching), IK Retargeter; 🧪 5.9: generování animací pomocí AI (UAF AnimGen) ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Mecanim, 2D kosterní animace; Cinemachine ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | AnimationPlayer, AnimationTree ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)); nový IK framework od 4.6 ([Godot 4.6](https://godotengine.org/releases/4.6/)) |
| Realistické postavy | MetaHuman ([oznámení 5.8](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274)) | Vestavěnou obdobu dokumentace nezmiňuje (zdroj mlčí) | Vestavěnou obdobu dokumentace nezmiňuje (zdroj mlčí) |
| Filmové sekvence | Sequencer a Movie Render Graph ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Timeline a Cinemachine ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | AnimationPlayer ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)) |

## 9. Fyzika a svět

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| 3D fyzika | Chaos, včetně fyzikálních assetů přes Dataflow ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Integrace NVIDIA PhysX ([dokumentace](https://docs.unity3d.com/6000.6/Documentation/Manual/physics-integrations.html)) | Jolt jako výchozí pro nové 3D projekty od 4.6 ([Godot 4.6](https://godotengine.org/releases/4.6/)); 🧪 4.8: Jolt 5.6 ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| 2D fyzika | Dokumentace popisuje 2D fyziku jako běžnou fyzikální simulaci se zamčenou polohou a rotací do roviny (*"typically to the Y axis for side scrolling games"*, [Paper 2D Physics, dokumentace 5.9](https://dev.epicgames.com/documentation/unreal-engine/paper-2d-physics-in-unreal-engine)); samostatnou 2D fyziku nezmiňuje (zdroj mlčí) | Integrace Box2D ([dokumentace](https://docs.unity3d.com/6000.6/Documentation/Manual/physics-integrations.html)) | Vlastní 2D fyzika ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)) |
| Terén | Landscape a Mesh Terrain; 🧪 5.9 vylepšuje Mesh Partition ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Terrain a balíček Terrain Tools ([dokumentace](https://docs.unity3d.com/6000.6/Documentation/Manual/PhysicsSection.html)) | Vestavěný terén dokumentace 4.7 mezi 3D nástroji nezmiňuje, uvádí CSG a GridMap (zdroj mlčí, [dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)); řeší se pluginy |
| Otevřené světy | World Partition a PCG ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Vestavěné automatické dělení světa na buňky jako World Partition dokumentace nezmiňuje (zdroj mlčí). Streamování nabízí balíček Entities přes subscény: *"Unity can dynamically load and unload scenes in seamless worlds that are larger than can fit memory"*; které části se kdy načtou, ale řídí kód projektu, ne automatické dělení (odvozeno) ([streamování v Entities 1.3](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/streaming-overview.html)); jinak aditivní scény a Addressables | Bez vestavěného streamování scén (zdroj mlčí); 🧪 4.8: streamování textur po mip úrovních ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |

## 10. Multiplayer a UI

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| Multiplayer | Replikace je součástí jádra enginu; 🧪 5.9 přidává selektivní replikaci pawnů pro Mass ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Netcode for GameObjects a Netcode for Entities ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | High-level multiplayer API se spawnováním a synchronizací uzlů ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)) |
| UI | UMG a Common UI ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | UI Toolkit a uGUI ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | Systém Control uzlů; sám editor je postavený v Godotu ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)) |

## 11. Platformy

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| Mobil | Android a iOS ([oznámení 5.8](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274)) | Android a iOS ([příručka 6.7](https://docs.unity.com/en-us/engine/6000.7/manual)) | Android a iOS ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)); 🧪 4.8: editor sám stáhne a nastaví Android a Java SDK ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |
| Web | Ve 5.8 ne; 🧪 5.9: nový experimentální cíl WebAssembly s vykreslováním přes WebGPU ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Ano, prohlížeče s podporou WebGL 2.0 ([systémové požadavky](https://docs.unity3d.com/6000.0/Documentation/Manual/system-requirements.html)) | Ano, ale jen WebGL 2.0 přes renderer Compatibility; WebGPU Godot nepodporuje a projekty v C# na web exportovat nejde ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_web.html)) |
| Konzole | Dokumentace a přístup ke konzolím bez dalších poplatků, ale jen pro vývojáře schválené výrobcem konzole a po NDA s Epicem ([PlayStation 5](https://dev.epicgames.com/documentation/en-us/unreal-engine/development-for-playstation-5-in-unreal-engine)) | Vydávání na konzole vyžaduje plán Pro ([ceník 2026](https://unity.com/en/products/pricing-updates)) | Oficiálně jen Steam Deck; na konzole přes middleware a služby třetích stran, například W4 Games ([Godot](https://godotengine.org/consoles/index.html)) |
| XR | VR i AR mají vlastní sekce platformní dokumentace ([platformy](https://dev.epicgames.com/documentation/unreal-engine/sharing-and-releasing-projects?application_version=4.27)) | Včetně Apple Vision Pro, které vyžaduje plán Pro ([ceník 2026](https://unity.com/en/products/pricing-updates)) | Podpora XR včetně XR editoru ([dokumentace 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html)); 🧪 4.8: visionOS jako modul s hand trackingem ([beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/)) |

**Build pro jiný operační systém.** Matice říká, na kterém systému jde sestavit build pro který cíl, oficiálně podporovanou cestou v hodnocené verzi. Buňky jsou popisné jako ve zbytku dokumentu (§1.3); „sám“ znamená build na stejném systému, pro který je určený.

| Engine | Build na | Windows | macOS | Linux | Android | iOS/iPadOS |
|---|---|---|---|---|---|---|
| **Unreal** | Windows | sám | ne (odvozeno) | ano, oficiální cross-compile toolchain | ano | jen vzdáleně přes Mac (Remote Build) |
| | macOS | ne (odvozeno) | sám | ne | ano | ano |
| | Linux | ne | ne (odvozeno) | sám | ano | ne (odvozeno) |
| **Unity** | Windows | sám | jen se scripting backendem Mono | ano, i s IL2CPP | ano (viz pozn.) | sestavení jen na Macu nebo přes Unity Build Automation; projekt Xcode z tohoto OS dokumentace nezmiňuje (viz pozn.) |
| | macOS | jen s Mono | sám | ano, i s IL2CPP | ano (viz pozn.) | ano, přes Xcode |
| | Linux | jen s Mono | jen s Mono | sám | ano (viz pozn.) | sestavení jen na Macu nebo přes Unity Build Automation; projekt Xcode z tohoto OS dokumentace nezmiňuje (viz pozn.) |
| **Godot** | Windows | sám | ano, jako `.app` v ZIPu, bez DMG | ano (viz pozn.) | ano (viz pozn.) | ne |
| | macOS | ano (viz pozn.) | sám | ano (viz pozn.) | ano (viz pozn.) | ano, přes Xcode |
| | Linux | ano (viz pozn.) | ano, jako `.app` v ZIPu, bez DMG | sám | ano (viz pozn.) | ne |

Poznámky k matici:

- **Unreal:** Cross-kompilace je podporovaná jen z Windows na Linux; uživatelé Macu musí kompilovat nativně ([požadavky pro Linux](https://dev.epicgames.com/documentation/unreal-engine/linux-development-requirements-for-unreal-engine)). Opačný směr z Linuxu na Windows podle komunitní wiki možný není ([Unreal Community Wiki](https://unrealcommunity.wiki/linux-support-2afdzysd), sekundární). Pro iOS z Windows se Unreal přes SSH připojí až ke dvěma Macům; Mac potřebuje jen Xcode, ne kopii projektu ani Unreal ([vzdálené buildy pro iOS](https://dev.epicgames.com/documentation/unreal-engine/creating-remote-builds-of-unreal-engine-projects-for-ios)). Android toolchain jde nastavit na Windows, macOS i Linuxu ([Android SDK](https://dev.epicgames.com/documentation/unreal-engine/manual-android-sdk-setup-with-android-studio-for-unreal-engine)). Buňky „odvozeno“ plynou z toho, že jedinou zdokumentovanou cross-kompilací desktopu je Windows → Linux.
- **Unity:** Build s IL2CPP pro konkrétní platformu se obecně musí dělat v editoru běžícím na té platformě; výjimkou je Linux ([IL2CPP](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-introduction.html)), pro který Unity dodává sysroot a toolchain balíčky pro Windows, macOS i Linux ([Linux IL2CPP](https://docs.unity.cn/Packages/com.unity.sysroot@2.0/manual/index.html)). Desktopové buildy pro jiný OS jdou se scripting backendem Mono ([Unity Discussions, odpověď Unity](https://discussions.unity.com/t/why-is-there-no-windows-il2cpp-build-module-for-macos-installations-of-unity/919172)). 🧪 Unity 7 alfa ale podporu Mono desktopových přehrávačů odstraňuje ([7000.0.0a7](https://unity.com/releases/editor/alpha/7000.0.0a7)), takže s ní tahle cesta nejspíš skončí (inference). Pro iOS Unity vygeneruje projekt Xcode a teprve Xcode z něj sestaví aplikaci; Xcode běží jen na macOS, bez Macu proto zbývá sestavení v cloudu: *"If you don't have a macOS device, you can use Unity Build Automation to build your applications in the cloud"* ([build pro iOS, dokumentace 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/iphone/ios-building-and-delivering/build-process)). Jestli projekt Xcode pro iOS vygeneruje i editor na Windows nebo Linuxu, dokumentace 6.x neříká; výslovně to uvádí jen pro visionOS ([systémové požadavky 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements)). U Androidu systémové požadavky uvádějí SDK, NDK a OpenJDK instalované přes Unity Hub a editor pro Windows, macOS i Linux, ale omezení buildu podle hostitelského systému neuvádějí; jediné takové omezení se týká konzolí, které jdou sestavit jen ve Windows verzi Unity (tentýž zdroj). Že Android build jde ze všech tří systémů, je proto odvozené z toho mlčení.
- **Godot:** Export pro macOS z Windows nebo Linuxu vyrobí `.app`, DMG jde vytvořit jen na macOS; s certifikátem Apple Developer ID jde podpis i notarizace přes rcodesign i z Linuxu a Windows, `.app` exportovaná z Windows ale nemá příznak spustitelnosti ([export pro macOS](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_macos.html)). Pro iOS se musí exportovat z macOS s nainstalovaným Xcode; C# na iOS je od 4.2 experimentální ([export pro iOS](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html)). Pro Android dokumentace popisuje nastavení na Windows, macOS i Linuxu, s OpenJDK 17 a Android SDK ([export pro Android](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_android.html)). Pro Windows omezení hostitelského systému neuvádí, jen podpis kódu jde jinde než na Windows přes osslsigncode ([export pro Windows](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_windows.html)). Pro Linux hostitelský systém neřeší (zdroj mlčí, [export pro Linux](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_linux.html)); obecná stránka o exportu matici hostitel–cíl nemá a omezení podle hostitele zmiňuje jen u DMG pro macOS ([export projektů](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_projects.html)). Export pro Windows a Linux z libovolného OS je proto odvozený z předkompilovaných exportních šablon a z toho mlčení. Platí to pro projekt v GDScriptu: nativní knihovny přes GDExtension se musí zkompilovat pro každou cílovou platformu zvlášť (odvozeno z toho, že jde o nativní kód).
- **Společné úzké hrdlo je Apple:** pro iOS/iPadOS je potřeba Mac s Xcode ve všech třech enginech, lokálně, vzdáleně nebo jako macOS runner v CI.

Oficiálně podporovanou konzolí Godotu je jen Steam Deck přes linuxové exportní šablony; to plyne z [dokumentace ke konzolím](https://docs.godotengine.org/fr/4.5/_sources/tutorials/platform/consoles.rst.txt) (verze 4.5). Důvodem je, že SDK konzolí jsou pod NDA a jejich kód nejde zveřejnit pod open source licencí ([Godot](https://godotengine.org/consoles/index.html)).

## 12. Ekosystém

| | Unreal Engine 5.8.4 | Unity 6.6.8f1 | Godot 4.7.2 |
|---|---|---|---|
| Obchod s assety | Fab; 🧪 5.9 do něj přidává generování obrázků a meshí ([poznámky 5.9](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes)) | Asset Store ([ceník](https://unity.com/products)) | Asset Store, který ve 4.7 nahradil dřívější Asset Library ([Phoronix](https://www.phoronix.com/news/Godot-4.7-Released)) |

Otázka „komunita a výukové materiály“ byla z rozsahu vypuštěna (§1.6).

## 13. Reference

Ověřeno 2026-11-12 až 2026-11-14 (2026-11-14 jen termín plného vydání UE 5.9: poznámky k vydání 5.9 Preview a oznámení ve fóru). Sekundární zdroje jsou označené.

**Unreal Engine:**
- Verze — [5.8.4 hotfix](https://forums.unrealengine.com/t/5-8-4-hotfix-released/2842775) · [oznámení 5.8](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274) · [oznámení 5.8 (JP)](https://www.unrealengine.com/ja/news/unreal-engine-5-8-is-now-available) · [poznámky k vydání 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US) · [poznámky k vydání 5.9 Preview](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes) (aktualizováno 2026-11-09) · [5.9 MegaJam Preview, fórum](https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840) · [80.lv: preview sestavený zhruba za týden](https://80.lv/articles/unreal-engine-5-9-preview-is-out-it-was-built-with-ai/) (sekundární) · [PocketGamer.biz: plán UE6](https://www.pocketgamer.biz/epic-games-outlines-its-vision-for-unreal-engine-6/) (sekundární) · [The Road to UE6](https://www.unrealengine.com/news/the-road-to-ue-6) (Epic, automatické stažení odmítá, nečteno)
- Licence — [licence](https://www.unrealengine.com/en-US/license) · [EULA change log](https://www.unrealengine.com/eula-change-log/unreal) · [Launch Everywhere with Epic](https://www.unrealengine.com/news/unreal-engines-improved-royalty-reporting-system) · [vlastní licence](https://www.unrealengine.com/en-US/custom-license) · [licencování a přístup ke kódu](https://www.unrealengine.com/en-us/custom-licensing)
- Editor a platformy — [hardwarové a softwarové specifikace](https://dev.epicgames.com/documentation/unreal-engine/hardware-and-software-specifications-for-unreal-engine?lang=en-US) · [požadavky pro Linux a cross-compile toolchain](https://dev.epicgames.com/documentation/unreal-engine/linux-development-requirements-for-unreal-engine) · [vzdálené buildy pro iOS](https://dev.epicgames.com/documentation/unreal-engine/creating-remote-builds-of-unreal-engine-projects-for-ios) · [Android SDK](https://dev.epicgames.com/documentation/unreal-engine/manual-android-sdk-setup-with-android-studio-for-unreal-engine) · [Linux Support (komunitní wiki)](https://unrealcommunity.wiki/linux-support-2afdzysd) (sekundární) · [PlayStation 5](https://dev.epicgames.com/documentation/en-us/unreal-engine/development-for-playstation-5-in-unreal-engine) · [sdílení a vydávání projektů](https://dev.epicgames.com/documentation/unreal-engine/sharing-and-releasing-projects?application_version=4.27)
- Programování — [limit iterací smyček v Blueprintech (odpověď Epicu)](https://answers.unrealengine.com/questions/237724/view.html) · [stav Paper2D (fórum Epicu)](https://forums.unrealengine.com/t/paper2d/95809) · [binární `.uasset`](https://usourcecontrol.com/glossary/uasset) (sekundární, prodejce verzovacího systému)
- Grafika a fyzika — [Rect Light](https://dev.epicgames.com/documentation/unreal-engine/rectangular-area-lights-in-unreal-engine) · [HDR Display Output](https://dev.epicgames.com/documentation/en-us/unreal-engine/high-dynamic-range-display-output-in-unreal-engine) · [Paper 2D Physics](https://dev.epicgames.com/documentation/unreal-engine/paper-2d-physics-in-unreal-engine)

**Unity:**
- Verze — [6000.6.8f1](https://unity.com/vn/releases/editor/whats-new/6000.6.8f1) · [beta program (6000.7.0b9)](https://unity.com/vn/releases/editor/beta) · [příručka 6.7 Beta](https://docs.unity.com/en-us/engine/6000.7/manual) · [Unity 7 alfa, 7000.0.0a7](https://unity.com/releases/editor/alpha/7000.0.0a7) · [Unity 6.6 je k dispozici](https://discussions.unity.com/t/unity-6-6-is-now-available/1735357) · [CoreCLR, červen 2026](https://discussions.unity.com/t/coreclr-scripting-and-serialization-update-june-2026/1723299) · [plán Unity 7 z Unite Seoul, červenec 2026](https://unity.com/news/unity-7-roadmap-revealed-at-unite-seoul)
- Licence — [ceník 2026](https://unity.com/en/products/pricing-updates) · [srovnání plánů](https://unity.com/compare-plans) · [plány a ceny](https://unity.com/products) · [plány a ceny Unity AI](https://unity.com/simulation) · [zrušení runtime fee, 2024](https://www.tipranks.com/news/the-fly/unity-ceo-says-canceling-runtime-fee-announces-pricing-changes) (sekundární)
- Editor a programování — [systémové požadavky 6.3](https://docs.unity.com/en-us/engine/6000.3/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements) · [systémové požadavky 6.0](https://docs.unity3d.com/6000.0/Documentation/Manual/system-requirements.html) · [argumenty příkazové řádky](https://docs.unity3d.com/es//Manual/CommandLineArguments.html) · [argumenty editoru 6.3 a batch mode](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor) · [testy z příkazové řádky 6.3](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/test-framework-introduction/reference-command-line) · [Visual Scripting 1.9](https://docs.unity3d.com/Packages/com.unity.visualscripting@1.9/manual/index.html) · [`ScriptGraphAsset` (API 1.9)](https://docs.unity3d.com/Packages/com.unity.visualscripting@1.9/api/Unity.VisualScripting.ScriptGraphAsset.html) · [zamrznutí editoru „By Design“](https://issuetracker.unity3d.com/issues/editor-freezes-occasionally-when-entering-play-mode-while-using-procedural-generation) · [výjimky a další snímek (Jackson Dunstan)](https://www.jacksondunstan.com/articles/5344) (sekundární) · [režim serializace assetů (JetBrains)](https://www.jetbrains.com/help/rider/Asset-serialization-mode.html) (sekundární) · [Unity MCP](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.5/manual/integration/unity-mcp-get-started.html) · [IL2CPP](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-introduction.html) · [Linux IL2CPP: sysroot a toolchainy](https://docs.unity.cn/Packages/com.unity.sysroot@2.0/manual/index.html) · [Windows IL2CPP na macOS (odpověď Unity)](https://discussions.unity.com/t/why-is-there-no-windows-il2cpp-build-module-for-macos-installations-of-unity/919172) · [systémové požadavky 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements) · [build pro iOS 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/iphone/ios-building-and-delivering/build-process)
- Grafika a fyzika — [srovnání render pipeline](https://docs.unity.cn/Documentation/Manual/render-pipelines-feature-comparison.html) · [Surface Cache GI (6.7)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/surface-cache-gi-volume-override-reference.html) · [světla v URP](https://docs.unity3d.com/Manual/urp/light-component.html) · [převod osvětlení z HDRP na URP](https://docs.unity3d.com/6000.5/Documentation/Manual/urp/convert-hdrp-lighting-to-urp.html) · [strategie render pipeline 2026 (80.lv)](https://80.lv/articles/unity-unveils-2026-render-pipelines-strategy/) (sekundární) · [Mesh LOD](https://docs.unity3d.com/6000.2/Documentation/Manual/lod/mesh-lod-generate-lods.html) · [fyzikální integrace](https://docs.unity3d.com/6000.6/Documentation/Manual/physics-integrations.html) · [fyzika a terén](https://docs.unity3d.com/6000.6/Documentation/Manual/PhysicsSection.html) · [HDR Output v URP 6.6](https://docs.unity.com/en-us/engine/6000.6/manual/materials-and-shaders/graphics-color/hdr/hdr-in-urp/hdr-output) · [HDR Output v HDRP 17.0](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/HDR-Output.html) · [streamování v Entities 1.3](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/streaming-overview.html)

**Godot:**
- Verze — [4.7.2 na GitHubu](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable) · [poznámky k 4.7.2](https://godotengine.org/article/maintenance-release-godot-4-7-2/) · [Godot 4.6](https://godotengine.org/releases/4.6/) · [Godot 4.7 (Phoronix)](https://www.phoronix.com/news/Godot-4.7-Released) (sekundární) · [4.8 beta 1](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/) · [4.8 beta 3](https://godotengine.org/article/dev-snapshot-godot-4-8-beta-3/)
- Licence a editor — [licence MIT](https://godotengine.itch.io/) · [systémové požadavky 4.6](https://docs.godotengine.org/en/4.6/about/system_requirements.html) · [systémové požadavky 4.5](https://docs.godotengine.org/en/4.5/about/system_requirements.html) · [seznam funkcí 4.7](https://docs.godotengine.org/en/4.7/about/list_of_features.html) · [vkládání hry do editoru](https://docs.godotengine.org/en/stable/tutorials/editor/game_embedding.html) · [příkazová řádka](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html) · [formát TSCN](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) · [migrace na Godot 4](https://docs.godotengine.org/en/4.7/tutorials/migrating/upgrading_to_godot_4.html)
- Programování a AI — [konec VisualScriptu](https://godotengine.org/article/godot-4-will-discontinue-visual-scripting) · [Orchestrator (fórum Godotu)](https://forum.godotengine.org/t/heard-about-visual-scripting-but-cant-find-it/66967) · [přehled MCP serverů](https://ziva.sh/blogs/godot-mcp-server-claude-code-cursor) (sekundární, prodejce MCP serveru) · [shin2344234/godot-mcp](https://github.com/shin2344234/godot-mcp/releases) · [kód v editoru (`@tool`)](https://docs.godotengine.org/en/4.7/tutorials/plugins/running_code_in_the_editor.html) · [příklad GDExtension v C++ (zdroj dokumentace 4.7)](https://raw.githubusercontent.com/godotengine/godot-docs/4.7/tutorials/scripting/cpp/gdextension_cpp_example.rst) · [`gdscript_vm.cpp` 4.7.2](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/modules/gdscript/gdscript_vm.cpp) · [`SConstruct` 4.7.2](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/SConstruct) · [vlastní test: `null` v release exportu](tests/godot-null-release/run.sh)
- Grafika a platformy — [SDFGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_sdfgi.html) · [úvod do GI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/introduction_to_global_illumination.html) · [mesh LOD](https://docs.godotengine.org/en/4.7/tutorials/3d/mesh_lod.html) · [ray tracing přes RenderingDevice (Phoronix)](https://phoronix.com/news/godot-4.7-dev-1-vulkan-rt) (sekundární) · [export na web](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_web.html) · [export pro macOS](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_macos.html) · [export pro iOS](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html) · [podpora konzolí](https://godotengine.org/consoles/index.html) · [konzole v dokumentaci 4.5](https://docs.godotengine.org/fr/4.5/_sources/tutorials/platform/consoles.rst.txt) · [export projektů](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_projects.html) · [export pro Windows](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_windows.html) · [export pro Linux](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_linux.html) · [export pro Android](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_android.html)

---

*Pracovní kostra založená 2026-11-13; rozsah sepsán před ověřováním, ale až po průzkumné AI konverzaci. Všechny kategorie, souhrnná tabulka a průvodce čtením ověřeny a doplněny 2026-11-13; cross-kompilace přidána změnou rozsahu tentýž den (§1.6, §11), stejně jako odhady pro AI agenta rozepsané po jazycích (§6) a uzavření všech míst k ověření (§4, §5, §7, §9, §11). Termín plného vydání UE 5.9 doplněn 2026-11-14 (§2, §4). Dokument je datovaný snapshot a zpětně se neaktualizuje. Vzniká ve spolupráci s Claude (Anthropic).*
