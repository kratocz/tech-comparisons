# Hlasové diktování na Macu: Wispr Flow vs Superwhisper vs Spokenly vs macOS diktování vs VoiceInk vs FluidVoice

- **Verdikt:** ⭐ **VoiceInk** (build ze zdrojáků, lokální Parakeet v3, vylepšování textu přes vlastní klíče) — platí pro kontext popsaný níže
- **Fakta ověřena:** 2026-08-18 (wisprflow.ai /pricing a /data-controls, superwhisper.com, spokenly.app, tryvoiceink.com + dokumentace + GitHub Beingpax/VoiceInk, GitHub altic-dev/FluidVoice, Apple „macOS Feature Availability“, NVIDIA model card parakeet-tdt-0.6b-v3)
- **Otevřené tagy:** jeden `[OVĚŘIT]` — cena Superwhisper Pro / Lifetime (§7): zdroje si protiřečí a web cenu nevydal čitelně
- **Adversariální ověření:** provedeno 2026-08-18 v čistém kontextu se zadáním „vyvrátit“. Žádné tvrzení nepadlo — včetně všech tvrzení o nemožnosti; jedno bylo oslabeno a je zapracováno: build VoiceInk ze zdrojáků odemyká aplikaci jen oficiální cestou `make local` a kromě aktualizací ztrácí i iCloud synchronizaci slovníku (§3, §8).
- **Poznámka k procesu:** srovnání vzniklo z konverzace s Claude (claude.ai, 2026-08-18). Podle pravidel repozitáře jsou nálezy z AI konverzace hypotézy, ne zdroje — všechna nosná tvrzení byla přeověřena proti primárním zdrojům. Dvě ověření nepřežila a jsou tu už opravená: čeština v macOS diktování **není** on-device (§4) a VoiceInk **má** iOS companion aplikaci (§7). Rozhodovací pravidla v §1 byla sepsána až po volbě aplikace — nejsou pre-registrovaná a nelze je číst jako predikci.
- **Jazyk:** 🇨🇿 čeština (originál) · 🇬🇧 [English version](README.md)
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Kontext: pro jaký profil se rozhodovalo

- **Sólo vývojář na Apple Silicon Macu.** Jiné platformy (Windows, Android) nehrají roli; iOS je příjemný bonus, ne požadavek.
- **Diktuje se primárně česky**, sekundárně anglicky. Aplikace, která češtinu neumí použitelně, je mimo hru bez ohledu na ostatní kvality.
- **Diktování míří do všeho** — zprávy, dokumenty, a hlavně prompty pro Claude Code, který autor používá denně.
- **Preference lokálního zpracování.** Hlas nemá opouštět stroj; cloud je přijatelný nanejvýš volitelně, pro už přepsaný text, přes vlastní API klíče.
- **Averze k předplatnému** za nástroj této velikosti. Jednorázová platba nebo open source build je preferovaný model.
- **Dvě aplikace jsou odzkoušené z první ruky:** Wispr Flow a VoiceInk s modelem Parakeet v3. Hodnocení kvality češtiny u ostatních je odvozené, ne testované (§4).

Mimo rozsah: přepis nahraných schůzek a meeting notetakery (jiná úloha než diktování), Windows a Linux, hlasové ovládání systému.

## Shrnutí (TL;DR)

1. ⭐ **Doporučení: VoiceInk** — jediný kandidát, který zároveň přepisuje lokálně, patří k nejlepším v češtině (ověřeno vlastním testováním, §4) a díky licenci GPL-3.0 jde legálně zkompilovat ze zdrojáků a provozovat zdarma (§3, §8).
2. **Strukturální dělítko není cena, ale kde běží přepis** (§2). Wispr Flow je jediný bez lokálního režimu — jeho vlastní stránka Data Controls říká *"Transcription always occurs on the cloud."* To je architektura, ne nastavení, a pro tento kontext je to diskvalifikace.
3. **Kvalita češtiny je vlastnost enginu, ne aplikace** (§4). Superwhisper, Spokenly, VoiceInk i FluidVoice pouštějí tytéž lokální modely (Whisper, Parakeet TDT v3 — 25 jazyků včetně češtiny dle NVIDIA). Stejný model dá ve všech čtyřech prakticky stejný český přepis; liší se cena, UX a post-processing.
4. **Vestavěné macOS diktování pro češtinu ztrácí dvakrát** (§4): Apple ji nevede mezi jazyky s on-device diktováním (takže i systémové diktování posílá českou řeč na server) ani mezi jazyky s automatickou interpunkcí.
5. **Vylepšování nadiktovaného textu se liší v tom, kdo ho kontroluje** (§5): Wispr Flow ho dělá vždy a ve svém cloudu, FluidVoice automaticky a lokálně (ale closed-source vrstvou), Superwhisper / Spokenly / VoiceInk přes LLM dle vlastní volby — u VoiceInk včetně plně lokální Ollamy.

## Srovnání v přehledu

Symboly: ✅ silná stránka · 🟡 funguje s výhradami / kompromis · ❌ slabina nebo chybí · — nedává smysl / netýká se. Hodnoceno **pro tento kontext** (česky diktující sólo vývojář na Apple Silicon, preference lokálního zpracování, averze k předplatnému) — ne obecně; pro anglicky mluvícího uživatele s více platformami by řada řádků dopadla jinak. Pořadí sloupců drží pořadí z původní konverzace a je stejné ve všech tabulkách dokumentu.

| Kritérium | Wispr Flow | Superwhisper | Spokenly | macOS diktování | VoiceInk | FluidVoice |
|---|---|---|---|---|---|---|
| **▸ Zpracování a soukromí** (§2) | | | | | | |
| Lokální přepis (hlas neopouští stroj) | ❌ *"always … on the cloud"* | ✅ lokální Whisper | ✅ lokální Whisper / Parakeet | ❌ čeština jen přes server (§4) | ✅ lokální Whisper / Parakeet a další | ✅ vše lokálně (Parakeet / Nemotron / Whisper) |
| Funguje offline | ❌ | ✅ | ✅ | ❌ pro češtinu | ✅ | ✅ |
| **▸ Cena a licence** (detail §7) | | | | | | |
| Cena pro tento profil | ❌ $15 / měs; free tier 2 000 slov / týden | 🟡 free tier s malými modely; Pro placené | ✅ lokální modely + vlastní klíče zdarma | ✅ zdarma, součást systému | ✅ $29 jednorázově / build ze zdrojáků zdarma | ✅ zcela zdarma |
| Open source | ❌ | ❌ | ❌ | ❌ | ✅ GPL-3.0 | 🟡 GPLv3, ale vrstva Fluid-1 closed-source |
| **▸ Platformy** | | | | | | |
| Nároky na macOS | ✅ | ✅ | ✅ | ✅ součást OS | ✅ macOS 14.4+, Apple Silicon | 🟡 až macOS 15.0+ |
| Mimo macOS | ✅ Windows / iOS / Android | ✅ Windows / iOS | ✅ Windows / Linux / iOS | 🟡 obdoba v iOS / iPadOS | 🟡 iOS companion aplikace | ❌ zatím nic (Windows / iOS ohlášeny) |
| **▸ Čeština** (§4) | | | | | | |
| Podpora češtiny v přepisu | ✅ 100+ jazyků | ✅ přes Whisper | ✅ Whisper + Parakeet v3 | 🟡 ano, ale bez on-device a bez auto-interpunkce | ✅ Whisper + Parakeet v3 | ✅ Whisper + Parakeet v3 |
| Kvalita české diktace | ✅ skvělá, ale při pauze vkládá „, eh, “ *(testováno)* | 🟡 odvozeno od enginu, netestováno | 🟡 odvozeno od enginu, netestováno | ❌ nejslabší ze srovnání | ✅ s Parakeet v3 jen o pár % za Wispr Flow *(testováno)* | 🟡 odvozeno od enginu, netestováno |
| **▸ Vylepšení textu** (§5) | | | | | | |
| Vylepšení nadiktovaného textu | 🟡 automatické, ale výhradně v jejich cloudu | ✅ módy s vlastními prompty, LLM dle výběru | ✅ volitelné, přes vlastní klíče | ❌ žádné | ✅ volitelné, vlastní prompty, vlastní klíče vč. lokální Ollamy | ✅ automatické, plně lokální (Fluid-1) |
| **▸ Integrace s AI coding agenty** (§6) | | | | | | |
| Hlas pro coding agenty | — | ✅ deklarovaná podpora Claude Code aj. | ✅ MCP server | — | 🟡 „Local CLI“ provider pro enhancement | — |
| **▸ Provozní riziko** | | | | | | |
| Zralost a kontinuita | 🟡 etablovaná služba, ale cloud: zdražení či zánik mimo tvou kontrolu | 🟡 komerční aplikace malého nezávislého vývojáře | 🟡 komerční aplikace malého nezávislého vývojáře | ✅ součást OS | 🟡 sólo vývojář; GPL → fork možný, lokální modely přežijí | 🟡 mladý projekt, GPLv3 až od 2/2026 |

### Jak to číst

Wispr Flow vyhrává jediný řádek, na kterém mu tenhle kontext dovolí soutěžit — kvalitu češtiny — a i tam s kazem („, eh, “). Všechno ostatní prohrává na architektuře: cloud-only přepis je v rozporu s pravidlem 2 v §1 a předplatné s pravidlem 3. macOS diktování je opačný extrém: zdarma a bez tření, ale pro češtinu bez on-device režimu, bez automatické interpunkce a bez jakéhokoli vylepšování — použitelné jako nouzovka, ne jako denní nástroj. Prostřední čtveřice (Superwhisper, Spokenly, VoiceInk, FluidVoice) sdílí tytéž lokální enginy, takže o pořadí rozhodují licence a kontrola: VoiceInk je jediný plně open source s doloženě dobrou češtinou z vlastního testu; FluidVoice je zdarma a nejrychlejší, ale vylepšování textu stojí na closed-source vrstvě a projekt chce nejnovější macOS; Spokenly nabízí nejzajímavější integraci (MCP server) a štědrý free tier, ale není open source; Superwhisper je nejkonfigurovatelnější, ale platí se předplatným či nejdražším lifetime v kategorii a není open source.

## 1. Rozhodovací pravidla (2026-08-18)

Sepsáno v den psaní dokumentu, **po** volbě aplikace — viz poznámka k procesu v hlavičce. Nejsou to pre-registrovaná pravidla, ale explicitní kritéria, proti kterým lze verdikt zpětně přezkoušet:

1. **Čeština musí být použitelná pro každodenní diktování** — primární jazyk, ne okrajový případ.
2. **Hlas neopouští stroj.** Přepis běží lokálně; cloud je přijatelný jen volitelně, pro už přepsaný text, přes vlastní klíče.
3. **Bez předplatného.** Jednorázová platba nebo zdarma; open source s možností buildu ze zdrojáků je plus i pojistka kontinuity.
4. **Vylepšování textu pod vlastní kontrolou** — vlastní prompt a volba modelu, ne vnucený černoskříňkový post-processing.

**Vyřazující kritérium:** aplikace, jejíž přepis běží výhradně v cloudu (porušuje pravidlo 2). Wispr Flow tím vypadává, v tabulce ale zůstává záměrně — je to jediná cloudová referenční laťka, kterou má autor v češtině odzkoušenou, takže slouží jako baseline kvality (§4).

## 2. Cloud vs lokální přepis — strukturální dělítko

Nejdůležitější rozdíl celého srovnání není v cenících, ale v architektuře. Wispr Flow na vlastní stránce Data Controls píše: *"Transcription always occurs on the cloud. This is the best way for us to provide accurate, low latency transcription."* Nabízené soukromí je retenční, ne architektonické: Privacy Mode a vypnutý Private Cloud Sync omezí, co si služba **nechá** (audio i přepis se pak *"processed in real time and discarded after the request completes"*), ale nemění, kudy data **tečou** — česká řeč jde vždy na jejich servery. To je durable vlastnost: firma ji sama popisuje jako základ produktu, ne jako dočasný stav.

Zbylé čtyři aplikace (a pro podporované jazyky i macOS diktování) přepisují on-device. Superwhisper, Spokenly, VoiceInk i FluidVoice stavějí na týchž veřejných modelech — Whisper v různých velikostech a NVIDIA Parakeet — běžících na Apple Siliconu. Z toho plyne druhý durable fakt: **lokální přepis přežije svého vývojáře.** Model, který má uživatel stažený, funguje i po zániku projektu; cloudová služba zaniká se svým provozovatelem. Pro pravidlo 2 v §1 i pro riziko kontinuity (poslední řádek tabulky) je to zásadnější argument než kterákoli funkce.

## 3. Licence a vlastnictví: předplatné vs jednorázově vs open source

Pět aplikací pokrývá celé spektrum obchodních modelů:

- **Wispr Flow** — čisté SaaS předplatné ($15 / měs, ročně $12 / měs). Free tier s limitem 2 000 slov týdně na desktopu je na denní diktování řádově málo.
- **Superwhisper** — freemium: free tier s malými lokálními modely a vlastními prompty, placené Pro (měsíčně / ročně / lifetime; k cenám viz rozpor v §7).
- **Spokenly** — lokální modely a vlastní klíče zdarma bez limitů; platí se jen spravovaný cloud ($9,99 / měs).
- **VoiceInk** — open source (GPL-3.0) s placenými binárkami: jednorázově $29 / $49 / $69 podle počtu Maců, doživotní aktualizace. README výslovně říká: *"As an open-source project, you can build VoiceInk yourself by following the instructions in BUILDING.md."* Placený build přidává automatické aktualizace a podporu vývojáře — build ze zdrojáků je legální a oficiálně popsaná cesta, ne obcházení licence. Nuance z ověření zdrojáků: v kódu je plnohodnotná licenční brána se 7denní zkušební lhůtou a oficiální build cesta `make local` ji záměrně vypíná (compile flag `LOCAL_BUILD`) — kdo si aplikaci přeloží přímo v Xcode bez tohoto flagu, dostane trial verzi a mohl by mylně usoudit, že „zdarma ze zdrojáků“ neplatí. Lokální build zároveň podle BUILDING.md nemá automatické aktualizace ani iCloud synchronizaci slovníku.
- **FluidVoice** — zdarma bez tierů, GPLv3 (od 2026-02-23; předchozí verze Apache 2.0). Háček je ve vrstvě Fluid Intelligence / Fluid-1: *"We're keeping Fluid Intelligence private for now so we can sustainably offer the core dictation experience for free."* Samotné diktování je open source, chytré vylepšování textu ne — běží sice lokálně, ale je to černá skříňka s nejasnou budoucností (dnešní zdůvodnění „for now“ zní jako budoucí monetizace; to je inference, ne fakt).

Pro tento kontext z toho plyne pořadí: VoiceInk (open source + doložená čeština) > FluidVoice (zdarma, ale closed-source jádro přidané hodnoty) > Spokenly (zdarma v potřebném rozsahu, ale closed source) > Superwhisper (platí se) > Wispr Flow (předplatné navždy).

## 4. Čeština: co ji reálně určuje

**Fakta o podpoře.** Whisper podporuje ~100 jazyků včetně češtiny. NVIDIA Parakeet TDT 0.6b v3 podporuje 25 evropských jazyků a čeština (`cs`) je výslovně v seznamu model card. Apple v přehledu „macOS Feature Availability“ vede češtinu mezi jazyky diktování, ale **ne** v sekci on-device / modeless diktování a **ne** v sekci automatické interpunkce — česká systémová diktace tedy běží přes Apple server a interpunkci je nutné vyslovovat. Wispr Flow deklaruje 100+ jazyků; tvrzení z konverzace, že plnou paritu s angličtinou má jen sedm jazyků, se nepodařilo doložit primárním zdrojem, a proto se v tomto dokumentu nepoužívá.

**Fakta z vlastního testování (autor, 2026-08-18):** Wispr Flow zvládá češtinu skvěle, ale při zlomkové pauze v řeči vkládá do vět nežádoucí „, eh, “ — hezitační artefakt, který post-processing v češtině nespolehlivě filtruje. VoiceInk s Parakeet v3 je v češtině jen o jednotky procent horší než Wispr Flow — bez cloudu, bez předplatného a bez vkládaného „eh“.

**Inference (netestováno):** protože Superwhisper, Spokenly a FluidVoice pouštějí tytéž modely (Whisper Large, Parakeet v3), měl by stejný zvolený engine dát prakticky stejný český přepis jako ve VoiceInk. Je to očekávání odvozené z architektury, ne změřený výsledek — a je označeno 🟡 i v tabulce. Přímé benchmarky češtiny pro tyto aplikace prakticky neexistují; publikované WER metriky Whisperu se týkají hlavně angličtiny a pro češtinu je třeba počítat s citelně vyšší chybovostí.

## 5. Vylepšení nadiktovaného textu

Surový přepis a text, který jde poslat, jsou dvě různé věci — a aplikace se liší v tom, **kdo a kde** ten rozdíl obstarává:

- **Wispr Flow:** automaticky, vždy, v jejich cloudu, jejich modely. Nulová konfigurace, nulová kontrola — a v češtině prokazatelně propouští hezitace (§4).
- **Superwhisper:** módy s vlastními prompty; výstup lze routovat přes zvolený LLM (web jmenuje mj. GPT, Claude, Llama; free tier zahrnuje *"Unlimited use of small AI models"* a *"Custom prompt control"*).
- **Spokenly:** volitelný AI post-processing přes vlastní klíče (OpenAI, Deepgram, Groq, Anthropic, Google) zdarma, nebo spravovaný cloud v Pro.
- **macOS diktování:** žádné — pro češtinu ani automatická interpunkce (§4).
- **VoiceInk:** volitelný enhancement s vlastními prompty; dokumentace vede providery Groq, Cerebras, Gemini, OpenRouter a dodává *"OpenAI, Anthropic, Mistral, Gemini, Ollama, Local CLI, and custom OpenAI-compatible providers can also work."* Ollama znamená plně lokální řetěz přepis → vylepšení bez jediného paketu ven.
- **FluidVoice:** automaticky a plně lokálně přes Fluid-1 (~lokální AI runtime, §3) — čištění, tón dle aplikace, formátování. Nejpohodlnější lokální řešení, ale closed-source (§3).

Pro pravidlo 4 v §1 z toho vychází nejlépe VoiceInk (plná kontrola, možnost 100% lokálního řetězu) a Superwhisper; FluidVoice je pohodlnější, ale prompt ani model nevyměníš.

## 6. Hlas pro AI coding agenty

Vzhledem k dennímu používání Claude Code má tahle osa vlastní váhu:

- **Spokenly** má nejsilnější deklarovanou integraci: *"MCP server for AI coding agents (Claude Code, Cursor)"* plus hlasem řízené *"Agentic Actions"* pro automatizaci macOS.
- **Superwhisper** na webu uvádí použití s *"Cursor, Claude Code, Open Code, Amp, Codex, or any other agentic coding app"*.
- **VoiceInk** specifickou agentní integraci nedeklaruje; dokumentace ale mezi providery enhancementu uvádí „Local CLI“, tedy napojení na lokální CLI nástroje. Prakticky vzato: diktovat do promptu Claude Code umí každá z těchto aplikací — jsou to systémové vstupy — specifická integrace přidává až věci typu hlasové příkazy pro agenta.
- **Wispr Flow, macOS diktování, FluidVoice** nic specifického pro agenty nedeklarují (u FluidVoice jde o mladý projekt, kde se to může rychle změnit).

Tahle osa je jediná, kde verdikt něco obětuje: Spokenly by pro hlasové ovládání agentů byl silnější volba. Přijatý kompromis je popsán v §8.

## 7. Datovaný snapshot: ceny, modely, verze (2026-08-18)

Rychle stárnoucí vrstva — čísla platí k datu ověření a nejsou nosná pro verdikt (ten stojí na §2–§5):

| | Wispr Flow | Superwhisper | Spokenly | macOS diktování | VoiceInk | FluidVoice |
|---|---|---|---|---|---|---|
| Cena | Pro $15 / měs, ročně $12 / měs; free tier 2 000 slov / týden (desktop), 1 000 / týden (iPhone) | free tier; Pro cca $8,49 / měs, $84,99 / rok, lifetime $249,99 `[OVĚŘIT]` — viz rozpor níže | lokální + vlastní klíče zdarma; Pro $9,99 / měs | zdarma | Solo $29 (1 Mac) / Personal $49 (2) / Extended $69 (3), jednorázově; ze zdrojáků zdarma | zdarma |
| Minimální macOS | neověřováno | neověřováno | neověřováno | aktuální macOS (Tahoe) | 14.4, Apple Silicon | 15.0 (Sequoia) |
| Lokální modely | žádné | Whisper (vč. Large) | Whisper, Parakeet | systémový (pro češtinu serverový) | whisper.cpp, Parakeet (přes FluidAudio) a další | Nemotron Speech 3.5, Parakeet Flash / TDT v3 / TDT v2, Whisper Tiny–Large, Apple Speech, Cohere Transcribe |
| GitHub hvězdy | — | — | — | — | ~6 000 | ~10 600 |

**Rozpor u ceny Superwhisper:** web cenu nevydal ve strojově čitelné podobě (extrakce vrací „$849“ bez desetinné čárky a bez rozlišení měsíc / lifetime). Sekundární zdroje z poloviny 2026 se shodují na $8,49 / měs, $84,99 / rok a $249,99 lifetime; jeden zdroj tvrdí zdražení lifetime na $849 v březnu 2026. Za směrodatné beru opakovaně se shodující nižší hodnoty, ale před případným nákupem je nutné ověřit ceník přímo — proto tag. Na verdikt rozpor vliv nemá: Superwhisper nevypadává kvůli ceně, ale kvůli closed source a placenému modelu (§3).

Ceny VoiceInk se podle konverzace měnily krátce před vznikem dokumentu (dřívější zmínky o vyšších tierech od 1. 8. 2026 se na webu už nevyskytují — ceník výše je aktuální stav webu k datu ověření).

## 8. Verdikt

**VoiceInk, kompilovaný ze zdrojáků** — v tomto kontextu vyhrává jako jediná aplikace, která současně splní všechna čtyři pravidla §1: čeština doložená vlastním testem jen o pár procent za nejlepším cloudem (§4), přepis plně lokální (§2), cena nula při oficiálně podporovaném buildu ze zdrojáků pod GPL-3.0 (§3) a vylepšování textu s vlastním promptem přes libovolného providera včetně plně lokální Ollamy (§5).

Přijaté kompromisy, vědomě:

- **Build ze zdrojáků = žádné automatické aktualizace, žádná iCloud synchronizace slovníku, žádná podpora vývojáře.** Aktualizace znamená stáhnout a přeložit nové zdrojáky — oficiální cestou `make local`, ne přímo v Xcode, jinak se aktivuje trial brána (§3). Kdo to nechce, koupí Solo za $29 — pořád zlomek roční ceny Wispr Flow.
- **Čeština o jednotky procent horší než Wispr Flow** (vlastní měření, §4). Hypotéza k vyzkoušení: vlastní enhancement prompt na čištění hezitací může rozdíl dál smazat — neověřeno.
- **Sólo vývojář, komerční zájem vedle open source.** Mitigace: GPL-3.0 umožňuje fork a lokální modely fungují i bez vývojáře (§2).
- **Žádná specifická integrace pro coding agenty** (§6). Diktování do promptů funguje i tak; kdyby začalo chybět hlasové ovládání agentů, je Spokenly bezplatně vyzkoušitelné vedle — obě aplikace se nevylučují.

**Změním názor, pokud:** (a) VoiceInk přestane být udržován a build přestane jít přeložit na aktuálním macOS — pak FluidVoice, pokud do té doby otevře nebo nahradí Fluid-1, jinak Spokenly; (b) čeština začne v praxi selhávat na odborné terminologii tak, že bude potřeba cloudový engine — pak Spokenly s BYOK klíči dřív než návrat k Wispr Flow; (c) Wispr Flow nabídne plně lokální režim s češtinou — pak má smysl re-test, protože kvalitou češtiny vede i teď.

## Reference

Ověřeno 2026-08-18, není-li u položky uvedeno jinak.

**Wispr Flow**

- Ceník a free tier: <https://wisprflow.ai/pricing>
- Cloud-only zpracování a retenční kontroly (zdroj citace *"Transcription always occurs on the cloud."*): <https://wisprflow.ai/data-controls>

**Superwhisper**

- Web, free tier, platformy, zmínka o Claude Code: <https://superwhisper.com>
- Ceny Pro / Lifetime: sekundární zdroje v rozporu, viz otevřený tag v §7 (mj. <https://spokenly.app/blog/superwhisper-pricing> — pozor, blog konkurenta)

**Spokenly**

- Web, ceník, MCP server, BYOK providery: <https://spokenly.app>

**macOS diktování**

- Apple „macOS Feature Availability“ — seznamy jazyků pro diktování, on-device diktování a auto-interpunkci: <https://www.apple.com/macos/feature-availability/>

**VoiceInk**

- Web a ceník: <https://tryvoiceink.com>
- Zdrojáky, licence GPL-3.0, build ze zdrojáků: <https://github.com/Beingpax/VoiceInk>
- Doporučené modely a provideři enhancementu: <https://tryvoiceink.com/docs/recommended-models>
- iOS companion aplikace: <https://tryvoiceink.com/ios>

**FluidVoice**

- Zdrojáky, licence, modely, Fluid Intelligence: <https://github.com/altic-dev/FluidVoice>

**Modely**

- NVIDIA Parakeet TDT 0.6b v3 — 25 jazyků vč. češtiny: <https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3>
- OpenAI Whisper — vícejazyčný model vč. češtiny: <https://github.com/openai/whisper>

---

*Tento dokument je datovaný snapshot (2026-08-18) a neaktualizuje se zpětně s tím, jak fakta stárnou. Ceny a seznamy modelů v §7 zastarají jako první; verdikt stojí na durable vrstvě §2–§5.*
