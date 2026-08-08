# Platformy chytrých hodinek: Garmin vs Apple vs Samsung — a co z toho plyne pro nákup iPhonu

- **Verdikt:** ⏳ zatím žádný — kostra založena 2026-08-08, rešerše neproběhla; rozhodovací pravidla sepsána předem (§2)
- **Sycené rozhodnutí:** koupě repasovaného iPhone 15 Pro vs 16 Pro (vs zatím žádný) — horizont ~září 2026
- **Fakta ověřena:** 🟡 párovací tvrzení §2 ověřena 2026-08-09 proti primárním zdrojům (reference §6); zbytek zatím ne — značky [OVĚŘIT] mimo §2 stále platí
- **Jazyk:** 🇨🇿 pracovní draft (originál); 🇬🇧 kanonická anglická verze vznikne při publikaci
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] doplnit současné telefony do kontextu (2026-08-08: Motorola s Androidem + iPhone 12 mini)
- [x] potvrdit rozhodovací pravidla (§2) — kauzální řetěz potvrzen uživatelem 2026-08-09
- [x] ověřit párovací tvrzení §2 (2026-08-09): všechna tři potvrzena → pravidla drží beze změny
- [ ] rešerše trvanlivé vrstvy (§3): každé nosné tvrzení dostane odkaz a datum ověření
- [ ] datovaný snapshot (§4): tabulka funkcí/senzorů + dostupnost v ČR + ceny, s datem ověření
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

## 3. Trvanlivá vrstva (nese verdikt)

Vlastnosti platforem, které se roky nemění — tady se rozhoduje. U každé sekce je zapsáno, co zjistit; každé tvrzení dostane odkaz.

### 3.1 Vazba na telefon (lock-in matice)
Kdo s čím páruje; co se stane při změně telefonu; migrace historie mezi platformami hodinek; co hodinky umí bez telefonu.

### 3.2 Vlastnictví a export dat; Strava
Kdo vlastní naměřená data; co jde exportovat (formáty, API, kompletnost); kvalita integrace se Stravou; co se stane s historií při odchodu z platformy.

### 3.3 Filozofie výdrže a OS
Vlastní OS + týdny výdrže (Garmin) vs watchOS/Wear OS + ~den [OVĚŘIT aktuální stav]; důsledky pro měření spánku, nabíjecí rutinu a GPS záznam dlouhých aktivit.

### 3.4 Předplatné a placené tiery
Co je zdarma a co za měsíční poplatek (Garmin Connect vs Apple Fitness+ vs Samsung Health); trend zpoplatňování dosud bezplatných funkcí.

### 3.5 Životnost, opravitelnost, horizont podpory
Jak dlouho dostávají hodinky aktualizace; opravitelnost (výměna baterie); typická fyzická životnost; sekundární/repasovaný trh.

### 3.6 Vývojářská platforma
Connect IQ vs watchOS SDK vs Wear OS — relevantní pro vývojáře: co si lze doprogramovat, otevřenost, jazyky, kvalita toolingu.

### 3.7 Zdravotní funkce — regulatorní rámec
Držet se certifikovaných tvrzení výrobců s odkazem (regulované claims; dostupnost per země, ČR/EU); dokument nedává zdravotní doporučení. Pozn.: funkce mohou i mizet (patentové spory apod.) [OVĚŘIT příklady].

## 4. Datovaná vrstva (snapshot — rychle zastarává)

Vyplnit až s datem ověření; explicitně: tato tabulka je datovaný snapshot a nebude retro-aktualizována.

| Funkce / senzor | Garmin (řada) | Apple Watch | Samsung Galaxy Watch | Pozn. / dostupnost ČR |
|---|---|---|---|---|
| _(doplnit při rešerši)_ | | | | |

Plus: cenový snapshot relevantních modelů; dostupnost certifikovaných zdravotních funkcí v ČR.

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

Pozn.: zdroje jsou US stránky výrobců; dostupnost EKG/tlaku v ČR je regulovaná per země a ověří se v §4. Nosná tvrzení §3–§4 zdroje teprve dostanou.

---

*Pracovní kostra založená 2026-08-08; rozhodovací pravidla sepsána před rešerší (pravidla před výsledky). Vzniká ve spolupráci s Claude (Anthropic).*
