# Platformy chytrých hodinek: Garmin vs Apple vs Samsung — a co z toho plyne pro nákup iPhonu

- **Verdikt:** ⏳ zatím žádný — kostra založena 2026-08-08, rešerše neproběhla; rozhodovací pravidla sepsána předem (§2)
- **Sycené rozhodnutí:** koupě repasovaného iPhone 15 Pro vs 16 Pro (vs zatím žádný) — horizont ~září 2026
- **Fakta ověřena:** 🟢 §2 + §3 + §4 ověřeny 2026-08-09 (reference §6); zbývá verdikt (§5), EN překlad a řádek v kořenovém README
- **Jazyk:** 🇨🇿 pracovní draft (originál); 🇬🇧 kanonická anglická verze vznikne při publikaci
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] doplnit současné telefony do kontextu (2026-08-08: Motorola s Androidem + iPhone 12 mini)
- [x] potvrdit rozhodovací pravidla (§2) — kauzální řetěz potvrzen uživatelem 2026-08-09
- [x] ověřit párovací tvrzení §2 (2026-08-09): všechna tři potvrzena → pravidla drží beze změny
- [x] rešerše trvanlivé vrstvy (§3) — 2026-08-09, reference [R8]–[R26]
- [x] datovaný snapshot (§4) — 2026-08-09: zdravotní funkce v ČR, ceny, časování trhu (reference [R27]–[R37])
- [x] souhrnná tabulka „Srovnání v kostce“ — 2026-08-09, vč. dokrývací rešerše každodenních funkcí (platby ČR, hudba, mapy, zprávy, asistent; [R38]–[R46])
- [ ] verdikt (§5) + řádek do kořenového README + EN překlad (`README.md`)

## 1. Kontext: jaké rozhodnutí se tu doopravdy dělá

Tohle není „které hodinky jsou nejlepší". Nákup hodinek je odložený (měsíce až roky) — teď se volí **směr platformy**, protože je vstupem bezprostředního rozhodnutí o telefonu:

- **Bezprostřední rozhodnutí (~do září 2026):** koupit repasovaný **iPhone 15 Pro, 16 Pro, nebo zatím žádný**.
- **Současný stav:** dva telefony — **Motorola (Android)** a **iPhone 12 mini**. Nejde tedy o vstup do Apple ekosystému, ale o to, zda a jak hluboko v něm pokračovat; Android zůstává souběžně k dispozici.
- **Profil:** full-stack vývojář; aktivní účet **Strava** → integrace, vlastnictví a exportovatelnost sportovních/zdravotních dat jsou prioritní kritéria.
- **Hodinky:** nákup v horizontu měsíců až let; konkrétní model se vybere až při nákupu podle tehdejší nabídky — tento dokument volí platformu, ne model.

## 2. Rozhodovací pravidla (sepsána 2026-08-08 — PŘED rešerší; párovací fakta ověřena 2026-08-09)

Pravidla se píší před měřením; po výsledku se čtou, ne vymýšlejí. Stav: **kauzální řetěz potvrzen uživatelem, párovací fakta ověřena — pravidla drží beze změny.**

| Výsledek volby platformy | Důsledek pro nákup iPhonu | Zdůvodnění |
|---|---|---|
| **Apple Watch** | **16 Pro** | ✅ Ověřeno: Apple Watch párují výhradně s iPhonem — Series 11 „requires iPhone 11 or later with iOS 26 or later“ [R1]; párování s Androidem neexistuje. iPhone 12 mini na seznamu iOS 26 ještě je [R2] (fakt), ale podle vzoru XR/XS (podpora ~7 hlavních verzí; vypadly s iOS 26) mu hlavní verze dojdou ~iOS 27–28, tj. 2026–2027 (inference) → v horizontu nákupu hodinek (měsíce–roky) už nové watchOS s 12 mini nejspíš nespáruješ. Směr Apple tedy reálně vyžaduje novější iPhone. |
| **Garmin** | telefon čistě podle telefonních kritérií (klidně levnější 15 Pro, nebo odklad nákupu) | ✅ Ověřeno: Garmin Connect existuje oficiálně pro iOS („Requires iOS 18.2 or later“ [R3]) i Android [R4] → hodinky na volbu telefonu nijak netlačí. |
| **Samsung** | jako Garmin — iPhone hodinky nepotřebují; párují s Motorolou | ✅ Ověřeno: Watch4 a novější „rely on Google Play services which is not supported on iOS“ [R5] → jen Android. ✅ Potvrzena i výhrada: EKG/tlak vyžadují aplikaci Samsung Health Monitor, oficiálně jen pro Galaxy telefony (distribuce výhradně přes Galaxy Store) [R6] → s Motorolou tyto funkce oficiálně nefungují (neoficiální APK obchvaty existují, ale nestavět na nich). Samsung pro tento kontext oslabuje. |

Poznámka k přímému vlivu (ověřeno 2026-08-09): práh aktuální generace je „iPhone 11 nebo novější s iOS 26“ [R1] — 15 Pro i 16 Pro jsou hluboko nad ním a oba na seznamu iOS 26 [R2]; žádný watch-specifický rozdíl mezi nimi nenalezen → vliv hodinek na volbu modelu zůstává nepřímý (délka závazku k ekosystému), ne přímý (feature gate). Evidovaný rozpor ve zdrojích: stránka Samsungu o měření tlaku [R7] zmiňuje jen „Android 12 or later“ bez požadavku na Samsung telefon; oficiální stránka aplikace SHM [R6] Galaxy telefon vyžaduje explicitně — za směrodatnou beru [R6] (stránka samotné aplikace + fakt distribuce přes Galaxy Store), rozpor nechávám zaznamenaný.

## Srovnání v kostce (pro tento kontext)

Symboly: ✅ plně / 🟡 s výhradami či podmínkou / ❌ ne či chybí. Hodnoceno **pro tento kontext** (Motorola + iPhone 12 mini, Strava, vývojář, ČR) — ne obecně; s Galaxy telefonem by sloupec Samsungu vypadal jinak. Detaily a zdroje: §3, §4 a reference §6.

| Kritérium | Garmin | Apple Watch | Samsung Galaxy Watch |
|---|---|---|---|
| **▸ Telefon a vazba** | | | |
| Podporované telefony | ✅ iOS i Android [R3][R4] | ❌ jen iPhone [R1] | ❌ jen Android [R5] |
| Plný provoz s Motorolou | ✅ | ❌ | 🟡 ano, ale bez EKG/tlaku [R6] |
| Provoz bez telefonu | ✅ plně standalone, i bez účtu (FIT po USB) [R9] | 🟡 cellular ano; aktivace jen iPhonem | 🟡 LTE ano; aktivace jen Androidem |
| Odpovídání na zprávy z hodinek | 🟡 na Androidu ano; na iPhonu ❌ (restrikce Apple, platí pro všechny cizí hodinky) [R38] | ✅ jediné plnohodnotné na iPhonu | ✅ na Androidu (plná klávesnice) |
| **▸ Data a Strava** | | | |
| Export surových dat | ✅ FIT per aktivita + bulk ZIP účtu [R9] | 🟡 úplný, ale jeden XML blob + GPX [R11] | ❌ CSV/XML bez re-importu; GPX bez tepu [R14] |
| Synchronizace do Stravy | ✅ nativní auto-sync + bulk import historie [R8] | 🟡 jen nativní Cvičení, 30 dní zpětně; nebo Strava app v hodinkách [R10] | 🟡 jen aktivity s GPS [R12][R13] |
| Přenos historie metrik při odchodu z platformy | ❌ | ❌ | ❌ (všude jen aktivity; pojistka = průběžné zrcadlení do Stravy, §3.1) |
| **▸ Výdrž a každodennost** | | | |
| Výdrž baterie | ✅ dny–týdny [R26] | ❌ ~1 den (Ultra ~2) [R26] | 🟡 ~1,5–3 dny [R26] |
| Platby hodinkami v ČR | ✅ Garmin Pay — prakticky všechny běžné banky [R39] | ✅ Apple Pay — všechny běžné banky [R40] | ✅ Google Wallet (Samsung Pay v ČR nefunguje) [R41] |
| Offline hudba (Spotify) | ✅ music modely (Premium, stahování po Wi-Fi) [R42] | ✅ (Premium) [R43] | ✅ (Wear OS) |
| Mapy / navigace v hodinkách | ✅ offline mapy vč. Venu 4 (turn-by-turn) [R44] | 🟡 Apple Maps (vázané na iPhone) | ✅ Google Maps vč. offline [R43] |
| Hlasový asistent | 🟡 pass-through Siri/Google z telefonu (jen modely s mikrofonem) [R45] | ✅ Siri přímo v hodinkách | ✅ Gemini přímo v hodinkách (Watch 9) [R46] |
| **▸ Služby a podpora** | | | |
| Předplatné — tlak na paywall | 🟡 Connect+ a potvrzený příklon nových funkcí k němu [R15][R16] | ✅ data i health zdarma; Fitness+ jen obsah | 🟡 premium tier zvažují [R17] |
| Formální závazek délky podpory | ❌ žádný (empiricky roky) | 🟡 bez příslibu; empiricky ~5–6 let [R18] | ✅ 5 let (od Watch 9, 7/2026) [R19] |
| Výměna baterie / pozáruční servis | 🟡 výměna za refurbished kus za poplatek [R20] | 🟡 placený servis [OVĚŘIT ceny ČR] | 🟡 placený servis [OVĚŘIT ceny ČR] |
| Vývojářská platforma | ✅ Monkey C, volný sideload, vývoj z libovolného OS [R21] | 🟡 vyžaduje Mac; $99/rok na distribuci [R22] | ✅ standardní Android stack, ADB sideload |
| **▸ Zdraví v ČR (k 8/2026; detail §4.1)** | | | |
| EKG | ✅ vybrané modely (Venu 3/4, FR 970, Fenix 8) [R28][R29] | ✅ [R27] | 🟡 v ČR ano, ale jen se Samsung telefonem [R6][R24] |
| Krevní tlak | ❌ | 🟡 měření ne; hypertenzní notifikace ✅ [R27][R30] | 🟡 měření ✅ (jediný), ale Samsung telefon + manžeta à 28 dní [R24] |
| Spánková apnoe | ❌ (spánek jen wellness) | ✅ [R27] | 🟡 dostupnost v ČR neověřena |
| **▸ Cena** | | | |
| Vstupní cena (nejlevnější rozumný model, 8/2026) | 🟡 od ~10 tis. Kč (Venu 4) [R35] | ✅ od ~5,6 tis. Kč (SE 3) [R32] | ✅ od ~8–10 tis. Kč (Watch 9 s cashbackem) [R34] |

### Jak tabulku číst pro tento kontext

- **Garmin vede** tam, kde jde o nezávislost: telefony, data, Strava, výdrž, sideload. Nemá ale tlak, apnoe, a asistent i zprávy řeší oklikou.
- **Apple vede** ve zdraví v ČR (nejúplnější certifikované pokrytí), vstupní ceně (SE 3) a jako jediný umí plnohodnotné zprávy na iPhonu — výměnou za nejtvrdší lock-in a ~denní výdrž.
- **Samsung vede** ve formálním závazku podpory (5 let) a každodenních Wear OS aplikacích — ale jeho unikátní karta (tlak) je s Motorolou mrtvá a sloupec zdraví se celý škrtá.
- **Platby v ČR jsou remíza** — všude ✅ (u Samsungu ironicky přes Google Wallet, ne Samsung Pay). Jinde ve světě běžný diferenciátor, tady ne.

## 3. Trvanlivá vrstva (nese verdikt)

Vlastnosti platforem, které se roky nemění — tady se rozhoduje. Rešerše 2026-08-09; nosná tvrzení mají odkazy [R8]–[R26] v §6.

### 3.1 Vazba na telefon (lock-in matice)

- **Apple Watch: výhradně iPhone** [R1]. Bez iPhonu je nelze ani aktivovat; přechod na Android = hodinky end-of-life. Výměna iPhonu za novější iPhone je podporovaná (záloha/obnova při přepárování). Cellular varianty zvládnou hovory a hudbu bez telefonu poblíž, kotvou účtu ale iPhone zůstává.
- **Garmin: iOS i Android** [R3][R4] — a navíc plnohodnotný standalone provoz: aktivity nahrávají offline a synchronizují se dodatečně (telefon/Wi-Fi/USB); v krajním případě jdou používat úplně bez účtu a aplikace, FIT soubory se dají tahat po USB [R9]. Výměna telefonu = přepárování; historie žije v cloudovém účtu Garmin Connect.
- **Samsung: jen Android** [R5]; s Motorolou fungují, ale bez certifikovaného EKG/tlaku [R6]; přechod na iPhone = hodinky end-of-life.
- **Migrace historie mezi platformami hodinek je mizerná u všech tří:** zdravotní metriky (spánek, tep, stres) se mezi ekosystémy nepřenášejí; přenositelné jsou prakticky jen aktivity (FIT/GPX) — ideálně průběžně zrcadlené do Stravy (§3.2). Skutečný lock-in tedy není v hodinkách, ale v nahromaděné historii.

**Pro tento kontext:** Garmin jako jediný nezamyká ani volbu telefonu, ani data.

### 3.2 Vlastnictví a export dat; Strava

- **Garmin — nejsilnější vlastnictví dat:** každá aktivita jde stáhnout jako surový FIT (+ TCX/GPX), celý účet jako bulk ZIP (Account Settings → Export Your Data, do ~48 h) [R9]. Nativní auto-sync do Stravy během minut po aktivitě a Strava umí i bulk import historie z Garmin Connect [R8]. Závislost na cloudu připomněl dobře zdokumentovaný výpadek Garmin Connect po ransomware útoku (7/2020) — lokální FIT + offline provoz hodinek ji ale tlumí.
- **Apple — úplný export, ale nemotorný:** Zdraví → „Exportovat všechna zdravotní data“ → ZIP s export.xml (kompletně: tep, spánek, kroky, tréninky) + GPX trasy [R11]; u dlouhodobých uživatelů stovky MB XML — úplné, ale prakticky to chce vlastní tooling (pro vývojáře OK). Strava ↔ Apple Health funguje obousměrně, s ostrými limity: do Stravy jdou jen aktivity z nativní aplikace Cvičení, jen 30 dní zpětně, a aktivity zapsané třetími aplikacemi se nepřenášejí [R10]; čistší cesta je nahrávat rovnou nativní Strava aplikací v hodinkách.
- **Samsung — nejslabší:** manuální export CSV/XML bez možnosti re-importu, GPX export bez tepové frekvence [R14]; Samsung Health → Strava přenáší jen aktivity s GPS (běžecký pás se nepřenese) [R12]; most přes Health Connect existuje (Strava posílá GPS souhrny, přijímá váhu [R13]), ale synchronizace Samsung Health ↔ Health Connect je hlášená jako neúplná [R14].

**Pro tento kontext (Strava jako priorita):** Garmin = zlatý standard; Apple = funguje s kázní (nativní Cvičení, nebo rovnou Strava app); Samsung = funguje pro GPS aktivity, zbytek dat zůstává v ohradě.

### 3.3 Filozofie výdrže a OS

- **Garmin:** vlastní úsporný OS; dny až týdny (běžné modely ~1–2 týdny; krajní případy: Enduro 2 až 46 dní, solární Instinct v úsporném režimu prakticky neomezeně) [R26]. Spánek bez nabíjecí úzkosti, vícedenní GPS akce bez powerbanky.
- **Apple:** ~1 den (Ultra ~1,5–3 dny) [R26]; denní nabíjecí rutina je nutnost, spánek se řeší rychlonabíjením „při sprše“.
- **Samsung:** mezi tím — reálně ~1,5–3 dny [R26].

Durable pointa: tohle není parametr jednoho modelu, ale důsledek architektury (RTOS + úsporný displej vs. plnotučný OS + AMOLED) — poměr drží dekádu a příští generace ho nezmění. Přesná čísla per model → §4.

### 3.4 Předplatné a placené tiery

- **Garmin Connect+** (od 3/2025; $6.99/měs. či $69.99/rok) [R15]: existující funkce zůstaly zdarma, ale vedení na earnings i veřejně potvrdilo, že nové pokročilé (AI) funkce půjdou přednostně do placeného tieru [R16] → „subscription creep“ je u Garminu oficiální strategie, ne fáma.
- **Apple:** naměřená data a zdravotní funkce bez předplatného; Fitness+ (~$9.99/měs.) je čistě obsahová služba (lekce), ne brána k datům.
- **Samsung:** dnes vše zdarma; šéf digital health veřejně potvrdil, že premium tier po vzoru Fitbit Premium / Connect+ zvažují [R17].

Durable pointa: všichni tři konvergují k předplatnému za „insights“; zatím nikdo z trojice nezpoplatňuje surová naměřená data ani nepřesunul existující funkci za paywall. To je metrika, kterou sledovat — Fitbit precedens ukazuje, že možné to je.

### 3.5 Životnost, opravitelnost, horizont podpory

- **Samsung — jediný s formálním závazkem:** Watch4+ měly slíbené 4 roky, od Watch 9 / Ultra 2 (7/2026) je to 5 let OS i security updatů [R19] — aktuálně nejdelší psaný závazek ve Wear OS světě.
- **Apple — bez formálního závazku, empiricky ~5–6 let:** watchOS 26 podporuje ještě Series 6 (2020) a letos nevypadl žádný model [R18] (inference z track recordu, ne příslib).
- **Garmin — bez formálního závazku, empiricky roky firmware updatů** i pro starší řady (inference z track recordu; psaná politika neexistuje). Pozor: baterie je smluvně „spotřební díl“ mimo záruku a oficiální pozáruční cesta je výměna celého kusu za refurbished za poplatek, ne oprava [R20].
- Fyzickou životnost u všech limituje lepená konstrukce a baterie; opravitelnost je nízká napříč trojicí. Repasovaný/sekundární trh je nejlikvidnější u Apple.

### 3.6 Vývojářská platforma

- **Garmin Connect IQ:** vlastní jazyk Monkey C, SDK zdarma (VS Code extension), typy aplikací od watch faces po plné appky; vlastní build jde nahrát na vlastní hodinky bez store, bez review a bez poplatku (podpis vlastním RSA klíčem) [R21]. Vývoj funguje z libovolného OS.
- **Apple watchOS:** Swift/SwiftUI v Xcode (vyžaduje Mac); běh na vlastním zařízení zdarma s ~7denním re-signem, distribuce přes App Store = Developer Program $99/rok + review [R22]. Nejsilnější integrace s telefonem, nejvyšší proces.
- **Samsung / Wear OS:** standardní Android stack (Kotlin/Compose for Wear OS), sideload přes ADB volně, Play Console jednorázově ~$25.

**Pro tento kontext (vývojář):** nejnižší tření pro „vlastní hračky“ mají Garmin a Wear OS; Apple to vyvažuje nejbohatším API mostem do telefonu.

### 3.7 Zdravotní funkce — regulatorní rámec

Zásada: držet se certifikovaných tvrzení výrobců s odkazem; nic v tomto dokumentu není zdravotní doporučení.

- **Apple:** EKG a notifikace nepravidelného rytmu certifikované široce vč. EU. Doložený příklad křehkosti: SpO₂ bylo na US kusech vypnuté od 1/2024 (patentový spor s Masimo), obnovené až 8/2025 obezličkou — výpočet se přesunul z hodinek do iPhonu — a spor běží dál (nové vyšetřování ITC otevřeno 11/2025) [R25]. EU/ČR kusů se to nedotklo, ale precedens „certifikovaná funkce může zmizet i po nákupu“ je založen.
- **Samsung:** EKG + krevní tlak přes Samsung Health Monitor, CE značka 12/2020, oficiálně dostupné i v ČR [R24] — ale jen se Samsung telefonem [R6] (s Motorolou nedostupné) a tlak vyžaduje kalibraci pažní manžetou každých 28 dní [R7].
- **Garmin:** dlouho pozice „wellness, ne medicína“, ale EKG App má od 1/2025 schválení pro EU a Austrálii (4/2025 + UK a Švýcarsko; celkem 50+ zemí) na Venu 3, Fenix 8 a dalších [R23]. Tlak neměří. → Předpoklad „Garmin nemá certifikované zdravotní funkce“ je od 2025 zastaralý.

Durable pointa: regulovaná funkce není vlastnost hodinek, ale trojice (hodinky, telefon/aplikace, země) — u Samsungu navíc značky telefonu. Per-model a per-země detaily → §4.

## 4. Datovaná vrstva (snapshot k 2026-08-09 — rychle zastarává)

Datovaný snapshot; nebude retro-aktualizován. Kontext trhu v okamžiku pořízení: **Galaxy Watch 9 / Ultra 2 v prodeji od 7. 8. 2026** (dva dny; plné ceny, cashback do 31. 8.) [R34][R37]; **Apple Watch Series 12 / Ultra 4 očekávány ~září 2026** (nový čip, bez redesignu, cena mírně nahoru — tj. Series 11 brzy zlevní) [R37]; **iOS 27 (~září 2026) ukáže, zda iPhone 12 mini vypadl z podpory** (inference §2).

### 4.1 Certifikované zdravotní funkce v ČR (k 2026-08-09)

| Funkce | Apple Watch | Samsung Galaxy Watch | Garmin |
|---|---|---|---|
| EKG | ✅ ČR [R27] | ✅ ČR — ale jen se Samsung telefonem [R6][R24] | ✅ ČR od 1/2025 — Venu 3/4, Forerunner 970 (sw 5.02+), Fenix 8, Enduro 3; **ne** Venu X1 [R28][R29] |
| Krevní tlak — měření na zápěstí | ❌ nemá | ✅ ČR — **jediný z trojice**; Samsung telefon + kalibrace pažní manžetou à 28 dní [R24][R7] | ❌ nemá |
| Tlak/hypertenze — trend a notifikace | ✅ hypertension notifications, ČR ✓ (Series 9+ / Ultra 2+; SE 3 ne) [R27][R30] | 🆕 Blood Pressure Trend (jen Watch 9 / Ultra 2, od 7/2026; wellness, kalibrace i Samsung telefon dál nutné; nahrazuje Vascular Load) [R31] | ❌ |
| Spánková apnoe — notifikace | ✅ ČR (Series 9+ / Ultra 2 / SE 3) [R27] | 🟡 funkce existuje (SHM), dostupnost v ČR neověřena [OVĚŘIT] | ❌ (spánek jen wellness) |
| SpO₂ | ✅ ČR (US Masimo sága se EU kusů netýká, §3.7) [R27] | ✅ (wellness) | ✅ (wellness, Pulse Ox) |

Čtení tabulky pro tento kontext: s Motorolou se celý sloupec Samsungu u EKG/tlaku škrtá (§2) — reálná volba „certifikované zdraví na zápěstí“ je tedy Apple (široké pokrytí, bez měření tlaku) vs Garmin (EKG od 1/2025, nic víc).

### 4.2 Cenový snapshot ČR (orientačně, 8/2026)

| Model (relevantní výběr) | Cena ČR k 8/2026 | Pozn. |
|---|---|---|
| Apple Watch SE 3 | od ~5 600 Kč (akce až ~4 500) [R32] | vstupní model; apnoe ✓, hypertenzní notifikace ❌ |
| Apple Watch Series 11 | od ~9 000–10 790 Kč (Al 42 mm); LTE titan ~20 500 Kč [R33] | plná zdravotní výbava; Series 12 ~za měsíc [R37] |
| Samsung Galaxy Watch 9 | 9 990–9 999 Kč (40 mm BT), 10 790 Kč (44 mm); LTE +~1 300; cashback −2 000 do 31. 8. [R34] | novinka 8/2026; Snapdragon, 5 let podpory [R19] |
| Garmin Venu 4 | od ~10 300 Kč (Heureka) / ~13 500 Kč (Alza, MSRP 13 490) [R35] | EKG ✓, výdrž ~12 dní, lifestyle řada |
| Garmin Forerunner 970 | ~15 000–15 990 Kč (MSRP 18 790) [R36] | EKG ✓, běžecký flagship |
| Garmin Fenix 8 | ~20 000–27 500 Kč dle varianty (MSRP sníženo z 29 990) [R36] | outdoor flagship, EKG ✓ |

Ceny silně kolísají akcemi (cashback, slevové kódy) — před nákupem ověřit na Heureka/Zbozi; tabulka je referenční bod, ne ceník.

### 4.3 Poznámky k časování (k 2026-08-09)

- Hodinky se teď nekupují (§1) — snapshot slouží jako budoucí referenční bod „co platilo v době rozhodnutí o telefonu“.
- Kdyby se nákup hodinek posunul jen na podzim 2026: Series 12 (~9/2026) stlačí ceny Series 11; cashback na Watch 9 končí 31. 8.; Venu 4 je rok v cyklu (nástupce ~2027, inference z dvouletého cyklu Venu 2→3→4).
- Pro rozhodnutí o telefonu je klíčové září 2026: vyjde iOS 27 a bude jasno, jestli iPhone 12 mini drží (§2 inference se ověří do měsíce).

## 5. Verdikt (zatím žádný)

Šablona: **Směřuji k platformě X → telefon Y.** Přijaté kompromisy: … **Znovu otevřít, pokud:** (revival clause — např. změna podmínek předplatného, ztráta integrace Strava, změna pravidel párování, konec podpory iPhone 12 mini dřív než …).

## 6. Reference

Ověřeno 2026-08-09 (párovací tvrzení §2):

- [R1] Apple — Apple Watch Series 11, Tech Specs: <https://support.apple.com/en-us/125093> („Requires iPhone 11 or later with iOS 26 or later“); přehledově též Apple Watch and iPhone compatibility: <https://support.apple.com/en-us/118490>
- [R2] Apple — iPhone models compatible with iOS 26: <https://support.apple.com/guide/iphone/iphone-models-compatible-with-ios-26-iphe3fa5df43/ios>
- [R3] App Store — Garmin Connect: <https://apps.apple.com/us/app/garmin-connect/id583446403> („Requires iOS 18.2 or later“)
- [R4] Google Play — Garmin Connect: <https://play.google.com/store/apps/details?id=com.garmin.android.apps.connectmobile>; Garmin — Connect App Compatibility Requirements: <https://support.garmin.com/en-US/?faq=pvL8aWsaLU2iKyvF8VrpP9>
- [R5] Samsung — Galaxy smart watch and phone compatibility: <https://www.samsung.com/us/support/answer/ANS10004668/>
- [R6] Samsung — Samsung Health Monitor (stránka aplikace): <https://www.samsung.com/us/apps/samsung-health-monitor/>
- [R7] Samsung — Check your blood pressure using a Galaxy smartwatch: <https://www.samsung.com/us/support/answer/ANS10010530/> (jen „Android 12 or later“ — rozpor s [R6], evidováno)

Ověřeno 2026-08-09 (trvanlivá vrstva §3):

- [R8] Strava — Garmin and Strava: <https://support.strava.com/hc/en-us/articles/216918057-Garmin-and-Strava>; Import Historical Data From Garmin Connect: <https://support.strava.com/en-us/articles/15401911-import-historical-data-from-garmin-connect>
- [R9] Export dat z Garmin Connect (per-aktivita FIT/TCX/GPX + bulk export účtu): <https://www.gneta.app/blog/export-garmin-data-guide>; plně offline provoz bez účtu: <https://kevinboone.me/garmin-degoogled.html>
- [R10] Strava — Apple Health and Strava (jen nativní Cvičení, 30 dní, třetí aplikace ne): <https://support.strava.com/en-us/articles/216917527-Health-App-and-Strava>
- [R11] Struktura exportu Apple Health (export.xml + GPX trasy): <https://www.healthexport.dev/blog/apple-health-export-xml-too-big>
- [R12] Strava — Samsung Health and Strava (jen GPS aktivity; konec Tizen appky): <https://support.strava.com/en-us/articles/15401747-samsung-health-and-strava>
- [R13] Strava — Health Connect and Strava: <https://support.strava.com/en-us/articles/15401554-health-connect-and-strava>
- [R14] Export ze Samsung Health a jeho limity: <https://www.dcrainmaker.com/2019/03/export-samsung-galaxy.html>; nespolehlivost synchronizace do Health Connect: <https://forum.developer.samsung.com/t/syncing-data-is-unreliable-between-samsung-health-and-health-connect/24850>
- [R15] DC Rainmaker — Garmin Connect+ walkthrough (3/2025, ceny, co zůstává zdarma): <https://www.dcrainmaker.com/2025/03/garmin-connect-plus-subscription-walkthrough.html>
- [R16] TechRadar — Garmin potvrzuje budoucí paywall nových funkcí: <https://www.techradar.com/health-fitness/smartwatches/garmin-quietly-confirms-our-worst-fears-about-garmin-connect-says-more-features-will-likely-be-paywalled-in-the-future>; the5krunner (11/2025): <https://the5krunner.com/2025/11/06/garmin-connect-plus-paywall-new-features/>
- [R17] Android Authority — Samsung zvažuje placený tier Samsung Health: <https://www.androidauthority.com/samsung-health-subscription-3568540/>
- [R18] watchOS 26 — podporované modely (Series 6+, letos nevypadl žádný): <https://www.techradar.com/health-fitness/smartwatches/does-your-apple-watch-support-watchos-26-heres-the-full-list-of-compatible-apple-watches-and-which-ones-will-have-support-ended>
- [R19] 9to5Google — 5 let updatů pro Galaxy Watch 9 / Ultra 2 (7/2026; dřív 4 roky): <https://9to5google.com/2026/07/23/samsung-galaxy-watch-9-five-years-wear-os-updates/>; přehled: <https://endoflife.date/samsung-galaxy-watch>
- [R20] Android Authority — záruka Garmin (baterie = spotřební díl; pozáruční výměna za refurbished za poplatek): <https://www.androidauthority.com/garmin-watch-warranty-3241838/>
- [R21] Garmin — Connect IQ SDK: <https://developer.garmin.com/connect-iq/>; Monkey C: <https://developer.garmin.com/connect-iq/monkey-c/>
- [R22] Apple — Developer Program ($99/rok, všechny platformy): <https://developer.apple.com/programs/whats-included/>
- [R23] Garmin — ECG App v EU a Austrálii (1/2025): <https://www.garmin.com/en-US/newsroom/press-release/wearables-health/garmin-expands-ecg-app-to-customers-in-australia-and-the-european-union/>; UK+CH (4/2025): <https://www.dcrainmaker.com/2025/04/garmin-expands-ecg-to-uk-switzerland.html>
- [R24] Samsung — EKG/tlak: CE 12/2020, seznam zemí vč. České republiky: <https://news.samsung.com/global/samsung-expands-vital-blood-pressure-and-electrocardiogram-tracking-to-galaxy-watch3-and-galaxy-watch-active2-in-31-more-countries>; FAQ se seznamem zemí: <https://www.samsung.com/ae/support/apps-services/what-countries-support-the-samsung-galaxy-watchs-ecg-feature/>
- [R25] 9to5Mac — návrat SpO₂ v USA přes workaround (8/2025): <https://9to5mac.com/2025/08/14/apple-watch-blood-oxygen-feature-returning-in-the-u-s-today/>; AppleInsider — nové vyšetřování ITC (11/2025): <https://appleinsider.com/articles/25/11/14/apple-under-investigation-again-by-usitc-over-apple-watch-blood-oxygen-sensing>
- [R26] Android Central — přehled výdrží (Garmin dny–týdny vs Apple ~den vs Samsung ~2–3 dny): <https://www.androidcentral.com/wearables/best-smartwatches-for-battery-life>

Ověřeno 2026-08-09 (datovaná vrstva §4):

- [R27] Apple — watchOS 26 Feature Availability (Czechia: ECG, Sleep Apnea, Hypertension Notifications, Blood Oxygen): <https://www.apple.com/watchos/feature-availability/>
- [R28] Garmin EKG v ČR (1/2025): <https://samsungmagazine.eu/en/2025/01/16/update-your-garmin-ekg-finally-coming-to-the-czech-republic/>; Garmin — ECG App Region Compatibility: <https://support.garmin.com/en-US/?faq=QssFZHtIOfAYNSSmzXNwY9>
- [R29] Garmin — What Garmin Watches Have the ECG App: <https://support.garmin.com/en-US/?productID=873008&faq=XW4TwGAinJ2juGDNiANMt8>; Venu 4 s EKG: <https://www.notebookcheck.net/Garmin-Venu-4-rears-its-head-again-before-release-with-ECG-support-confirmed.1113199.0.html>; Venu X1 bez EKG: <https://the5krunner.com/2025/06/12/garmin-venu-x1-all-you-need-to-know-comparison-first-look-review/>
- [R30] MacRumors — hypertension notifications spuštěny (9/2025, Series 9+/Ultra 2+): <https://www.macrumors.com/2025/09/15/apple-watch-hypertension-notifications-now-live/>; expanze na 170 zemí (1/2026): <https://www.macrumors.com/2026/01/27/hypertension-alerts-expansion-six-countries/>
- [R31] Samsung Blood Pressure Trend (7/2026, Watch 9/Ultra 2): <https://www.sammyfans.com/2026/07/01/samsung-announces-new-blood-pressure-trend-feature/>; nahrazuje Vascular Load: <https://9to5google.com/2026/07/02/samsung-galaxy-watch-vascular-load/>
- [R32] Apple Watch SE 3 ceny ČR: <https://www.appliste.cz/apple-watch-se-3-sleva/>; Alza kategorie: <https://www.alza.cz/apple-watch-se-2025/18918319.htm>
- [R33] Apple Watch Series 11 ceny ČR: <https://www.alza.cz/apple-watch-11/18918318.htm>
- [R34] Galaxy Watch 9 ceny ČR: <https://mobilizujeme.cz/clanky/samsung-galaxy-watch-9-jsou-oficialni-chytrejsi-hodinky-s-ai-stoji-od-9-999-kc>; Alza: <https://www.alza.cz/samsung-galaxy-watch-9/18923449.htm>
- [R35] Garmin Venu 4 ceny ČR: <https://chytre-hodinky.heureka.cz/garmin-venu-4-41mm_3/>; MSRP: <https://www.alza.cz/garmin-venu-4-recenze>
- [R36] Forerunner 970 / Fenix 8 ceny ČR: <https://www.zivotsgarminem.cz/hodinky-forerunner-970-spadly-pod-15-tisic-jde-o-model-s-nejlepsim-pomerem-ceny-vykonu>; <https://www.zivotsgarminem.cz/node/4408/recenze-hodinek-fenix-8-nove-prostredi-dedictvi-forerunneru-hlasove-ovladani-volani-2>
- [R37] Galaxy Watch 9 / Ultra 2 launch (22. 7. 2026, prodej 7. 8. 2026): <https://www.droid-life.com/2026/07/22/galaxy-watch-9-galaxy-watch-ultra-2-made-official/>; Apple Watch Series 12 očekávání (~9/2026): <https://www.macrumors.com/2026/07/20/apple-watch-series-12-rumored-features/>

Ověřeno 2026-08-09 (dokrývka pro tabulku „Srovnání v kostce“):

- [R38] Garmin — odpovědi na zprávy jen na Androidu (restrikce Apple): <https://www.tomsguide.com/wellness/smartwatches/finally-the-massive-garmin-update-weve-all-been-waiting-for-is-here-but-theres-a-catch>; WhatsApp na Garminu: <https://tech.yahoo.com/wearables/articles/whatsapp-now-officially-available-garmin-164156066.html>
- [R39] Garmin Pay — banky v ČR: <https://www.garmin.com/cs-CZ/garminpay/banks/>; přehled Pay služeb v ČR: <https://www.mesec.cz/clanky/apple-google-garmin-fitbit-samsung-huawei-pay-karty-banky-seznam-prehled/>
- [R40] Apple Pay v ČR: <https://www.alza.cz/apple-pay>
- [R41] Samsung Wallet v ČR bez plateb; Galaxy Watch platí přes Google Wallet: <https://www.svetandroida.cz/samsung-wallet-cesko-aplikace/>; <https://www.alza.cz/jak-platit-samsung-galaxy-watch4-classic>
- [R42] Spotify na Garminu (music modely, Premium, Wi-Fi): <https://www.wareable.com/features/how-to-use-spotify-on-garmin-watch-6590>
- [R43] Spotify na Apple Watch: <https://support.spotify.com/us/article/spotify-on-apple-watch/>; offline Google Maps na Wear OS: <https://m.gsmarena.com/google_maps_offline_support_wear_os_beta-news-64174.php>
- [R44] Garmin Venu 4 — offline mapy a navigace (manuál): <https://www8.garmin.com/manuals/webhelp/GUID-2CF5620C-E585-4E0A-9CC3-9565533EEE4D/EN-US/GUID-AE6741EA-7DCC-4A8D-BCD4-7CD12AEBABD8.html>
- [R45] Garmin — Setting Up Voice Assistant (pass-through z telefonu): <https://support.garmin.com/en-US/?faq=B0n9YwrwMg4j7yEgevIWgA>
- [R46] Galaxy Watch 9 specs (Gemini v hodinkách): <https://the5krunner.com/specs/samsung/galaxy-watch-9/>

Pozn.: zdroje [R1]–[R7] jsou US stránky výrobců. Ceny předplatných (§3.4) jsou US ceníky, ceny hodinek (§4.2) české maloobchodní k datu snapshotu — obojí orientační.

---

*Pracovní kostra založená 2026-08-08; rozhodovací pravidla sepsána před rešerší (pravidla před výsledky). Vzniká ve spolupráci s Claude (Anthropic).*
