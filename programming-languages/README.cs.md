# Volba programovacího jazyka: jeden jazyk na dlouhá léta pro nové projekty

- **Na co dokument odpovídá:** na **tři různé otázky**. Zadání se během práce dvakrát upřesnilo a každá nová verze se zapsala jako nové datované zadání, ne jako přepis staré (§7.1, §12.1) — dokument tedy nese tři verdikty vedle sebe. Koho zajímá jen jedna z otázek, nemusí číst zbytek.
- **Otázka 1 — který jazyk je nejprofesionálnější, tedy přehledný v malém i velmi rozsáhlém kódu? → §7.** Verdikt (§7.5): **Kotlin a Rust, dělené první místo** — jediné dva z osmi bez jediné výhrady ve všech čtyřech kritériích. Shodu pravidlo nerozhoduje a tie-breaker se po zhlédnutí výsledku nedopisuje, takže volba mezi nimi patří zadavateli.
- **Otázka 2 — který jazyk nejlíp pokryje čtyři konkrétní domény najednou? → §3 a §6.** Verdikt (§6.2): **TypeScript**, vážená cena 4 před Pythonem s 5, s vyjmenovanými kompromisy — nejdražší z nich je, že se typy za běhu nevynucují.
- **Otázka 3 — a co když se do profesionality započítá i souběžnost? → §12.** Verdikt (§12.5): **Rust** se součtem 1 před Kotlinem se 3. Tenhle verdikt **rozsekl shodu z otázky 1**, a to jedinou osou: prevencí datových závodů při překladu, kterou z osmi kandidátů tvrdí o sobě jen Rust.
- **Hlavní nález — rozpor mezi verdikty (§7.5, §12.5):** vítěz otázky 2 je v otázce 1 sedmý a v otázce 3 šestý. **Žádný jazyk není zároveň nejlepším pokrytím těch čtyř domén a nejprofesionálnějším nástrojem.** Ten obchod je vlastní obsah dokumentu, ne kterýkoli z verdiktů zvlášť.
- **Sycené rozhodnutí:** na čem stavět **nové** projekty (vlastní, firemní i cizí) v horizontu let — a čím tu volbu argumentovat u někoho, kdo u úvahy nebyl.
- **Fakta ověřena:** 🟡 2026-08-22 až 2026-08-23, osm kol, reference [R1]–[R91]. Bez otevřených `[OVĚŘIT]`. Přiznaně neúplné: §4.1 (úrovně PHPStan a Psalm), §4.2 (C# a Rust), §7.4 (kritérium P2 měří jen vlastnictví formátovače, ne množství magie).
- **Předpovědi:** dvě, obě zapsané před svou rešerší. §2.3 **nevyšla** — Go mělo stoupnout a skončilo poslední. §7.3 **vyšla** ve všech bodech; rozdíl byl v tom, že uvažovala o rozptylu uvnitř kritérií, ne o silných stránkách kandidátů.
- **Dodatky:** §9 (2026-08-26) — proč PHP zaostává za Pythonem; rozdíl drží, ale čtvrtina z něj stojí na formalistickém kritériu P2. §10 (2026-08-26) — **jaké verze byly doopravdy analyzovány**: PHP 8.5 dodatečně ověřeno (nic nemění), TypeScript 7 je nativní přepis do Go, který analýza nezohlednila, a M1 byla uplatňována nerovnoměrně. §11 (2026-08-26) — **souběžnost, kterou kritéria neměřila**: P1 nehodnotilo prevenci datových závodů při překladu, což je doložený argument pro Rust v otevřené shodě §7.5; kritérium se ale zpětně nedopisuje. §12 (2026-08-26) — **třetí zadání**: profesionalita včetně souběžnosti, pravidla sepsána před rešerší.
- **Oprava:** ⚠️ §8 (2026-08-23) — tvrzení, že TypeScript nemá závazek podpory, bylo nepravdivé; brána B2 vypálila na chybném faktu a vypálit neměla. Verdikty se nemění, jedna položka účtu je levnější.
- **Adversariální průchod:** 🟡 2026-08-23 (§6.1) — ze čtyř prověřovaných buněk jedna neobstála a byla opravena (PHP v prohlížeči); pořadí na prvních dvou místech se nezměnilo. **Omezení: průchod běžel ve stejném kontextu, který závěr vytvořil, ne v odděleném.**
- **Jazyk:** 🇨🇿 čeština (originál) · 🇬🇧 [English version](README.md) (kanonická)
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## TL;DR

*Shrnutí doplněné 2026-08-26. Nepřidává žádné tvrzení — jen sbírá dohromady výsledky §3, §6 a §7, aby se nemusely hledat.*

Dokument odpovídá na **tři otázky** a **každá má jiného vítěze**. Tabulka je seřazená podle profesionality jazyka; nižší číslo je vždy lepší. Čtyři kritéria profesionality jsou z §7.2, ceny buněk ✅ = 0 · 🟡 = 1 · ❌ = 3, takže součet jde přepočítat okem. Plné znění buněk i se zdroji je v §7.4. Poslední sloupec je **pořadí** v prvním zadání (§6.2); tam, kde je vážená cena shodná, sdílejí kandidáti jedno místo — rozdíly v doménovém skóre jsou malé a rozsah je jen 4 až 9.

| # | Jazyk | P1: kompilátor chytí chybu | P2: čitelnost pro lidi | P3: velký refaktoring bezpečný | P4: typy unesou doménový model | Součet | Se souběžností (§12.5) | Domény (§6.2) |
|---|---|---|---|---|---|---|---|---|
| 1.–2. | **Rust** | ✅ null neexistuje, `match` vyčerpávající | ✅ `rustfmt` pod `rust-lang` | ✅ `rust-analyzer` pod `rust-lang` | ✅ enumy nesou data | **0** | **1 — 1. místo** | 6. místo |
| 1.–2. | **Kotlin** | ✅ nullabilita v typech | ✅ `ktfmt` pod `Kotlin` | ✅ `kotlin-lsp` pod `Kotlin` | ✅ sealed třídy, `when` bez `else` | **0** | 3 — 2. místo | 3.–5. místo |
| 3. | C# | 🟡 nullabilita jen při překladu | ✅ `dotnet format` pod `dotnet` | ✅ statické typy + Roslyn | 🟡 součtové typy zatím jen návrh | 2 | 6 — 3. místo | 3.–5. místo |
| 4. | Go | 🟡 `nil` je nulová hodnota všeho | ✅ `gofmt` v distribuci | ✅ `gopls` pod `golang` | ❌ součtové typy vynechány záměrně | 4 | 7 — 4. místo | 8. místo |
| 5.–6. | Java | 🟡 generika se mažou, nullabilita chybí | ❌ oficiální formátovač není | 🟡 jazykový server je Eclipse | ✅ sealed + vyčerpávající `switch` | 5 | 8 — 5. místo | 3.–5. místo |
| 5.–6. | Python | ❌ runtime typy nevynucuje | ✅ `black` pod `psf` | 🟡 dynamický; `mypy` first-party | 🟡 jen ve statické kontrole | 5 | 12 — 7. místo | 2. místo |
| 7. | TypeScript | ❌ typy se při překladu mažou | ❌ oficiální formátovač není | ✅ statické typy + nástroje MS | ✅ diskriminované unie a `never` | 6 | 10 — 6. místo | **1. místo** |
| 8. | PHP | ❌ přísnost po souborech, bez generik | ❌ oficiální formátovač není | ❌ oficiální jazykový server není | ❌ enumy nesou jen skalár | 12 | 19 — 8. místo | 7. místo |

Co ta čtyři kritéria znamenají (plné znění a co se u každého měří je v §7.2):

- **P1 — kompilátor chytí chybu dřív než uživatel:** hranice vynucení typů (za běhu, nebo jen při kontrole), nullabilita v typovém systému, vyčerpávající větvení.
- **P2 — kód přečte cizí člověk bez kontextu:** existuje oficiální formátovač pod organizací samotného jazyka? *(Jen to — viz výhrada níže.)*
- **P3 — velký refaktoring je bezpečný:** statické typy plus oficiální jazykový server; najde nástroj všechna volání?
- **P4 — typový systém unese doménový model:** součtové typy nesoucí data a vyčerpávající větvení nad nimi.

- **Nejprofesionálnější jazyk (§7):** **Kotlin a Rust, dělené první místo** — jediné dva bez jediné výhrady ve všech čtyřech kritériích.
- **Se započtenou souběžností (§12.5):** **Rust sám**, se součtem 1 před Kotlinem se 3. Rozhodla prevence datových závodů při překladu, kterou z osmi tvrdí o sobě jedině Rust — a která ve čtyřech kritériích §7.2 nebyla vůbec měřena (§11.2).
- **Nejlepší pokrytí čtyř domén (§6.2):** **TypeScript** s váženou cenou 4 před Pythonem s 5 — ale platí za to tím, že se typy za běhu nevynucují.
- **Hlavní nález:** vítěz druhého sloupce je v prvním sedmý. **Žádný jazyk není zároveň nejlepším pokrytím domén a nejprofesionálnějším nástrojem** — a ten obchod je vlastní obsah dokumentu, ne kterýkoli z verdiktů zvlášť.
- **Dvě kritéria jsou měřena neúplně a dokument to přiznává:** P2 hodnotí jen to, pod čí organizací žije formátovač, ne kolik magie musíš držet v hlavě (§9.3), a P4 nehodnotí neměnnost, ačkoli ji §7.2 uvádí (§10.1). U dvojice PHP–Python stojí zhruba třetina rozdílu právě na P2.
- **Pozor na rozsah:** obě čísla platí pro profil ze §1 (nové projekty na zelené louce) a pro pravidla ze §2.3 a §7.2. Jiné váhy dávají jiného vítěze — citlivost je v §6.3 a §7.4.

## 0. Stav a otevřené úkoly

- [x] kontext (§1) — 2026-08-22
- [x] rozhodovací pravidla (§2) sepsána před rešerší — 2026-08-22
- [x] řádek v kořenovém README — 2026-08-22
- [x] **potvrdit rozhodovací pravidla (§2) uživatelem** — 2026-08-22: váhy domén doplněny (§2.3), B1 zúžena na backend (§2.2), agregace přepsána na váženou cenu; předpověď zapsána před rešerší
- [x] tabulka vlastností (§4.8) — 2026-08-22
- [x] regret matrix (§3) včetně vážené ceny a čtení tabulky (§3.1) — kola 2 až 5, 2026-08-22
- [x] trvanlivá vrstva (§4) — §4.1 až §4.7 hotové (kola 1 až 7, 2026-08-22)
- [x] datovaný snapshot (§5) — 2026-08-22
- [x] adversariální průchod (§6.1) — 2026-08-23
- [x] verdikt (§6.2) a čtení po doménách i citlivost na váhy (§6.3) — 2026-08-23
- [x] **druhé zadání: pravidla profesionality (§7.1–§7.3) sepsána 2026-08-23 PŘED rešerší** — commitnuta zvlášť, aby to šlo ověřit z historie
- [x] rešerše profesionality (§7.4) a druhý verdikt (§7.5) — 2026-08-23: **dělené první místo Kotlin a Rust**
- [x] **oprava §8 (2026-08-23): brána B2 vypálila na chybném faktu a vypálit neměla**
- [x] dodatek §9 (2026-08-26): rozbor rozdílu PHP vs. Python, doplněny úrovně PHPStan a dvě pod-doložená tvrzení
- [x] dodatek §10 (2026-08-26): audit analyzovaných verzí, PHP 8.5 ověřeno, TypeScript 7 zaznamenán
- [x] dodatek §11 (2026-08-26): souběžnost mimo kritéria; argument pro Rust zapsán, P1 nezměněno
- [x] **třetí zadání: pravidla (§12.1–§12.3) sepsána 2026-08-26 PŘED rešerší** — commitnuta zvlášť
- [x] rešerše třetího zadání (§12.4) a jeho verdikt (§12.5) — 2026-08-26: **Rust vyhrál sám, shoda ze §7.5 rozseknuta**
- [x] anglická verze (`README.md`) jako kanonická — 2026-08-26

## 1. Kontext: jaké rozhodnutí se tu doopravdy dělá

Otázka nezní „který jazyk je nejlepší“ ani „na co se který jazyk hodí“. Zní: **kdybych si měl vybrat jeden jazyk, na kterém budu roky stavět nové projekty napříč čtyřmi doménami, který to bude a co za to zaplatím?**

- **Zelená louka.** Všechny projekty v záběru jsou **nové**. Nezáleží na tom, čí — vlastní, firemní, cizí. Tenhle společný jmenovatel je podstatný: odstraňuje přepínací náklad ze stávajícího systému, který by jinak rozhodoval víc než vlastnosti jazyka.
- **Co tenhle dokument NEŘEŠÍ:** migraci existujícího systému („máme monolit v PHP, přejít na X?“). To je jiná otázka s jinou odpovědí, kde dominuje cena přechodu, ne kvalita cíle.
- **Čtyři domény, různě vážené** (§2.3, §3), v pořadí podle váhy: webový backend a API (4); CLI nástroje, démoni a automatizace (3); webový frontend v prohlížeči (2); data, ML a dávkové zpracování (1). Jazyk má pokrýt všechny čtyři — ale ne stejnou měrou, a ta nerovnost je součástí zadání, ne kompromis vzniklý cestou.
- **Výkon není tvrdý požadavek.** Zadavatel nemá konkrétní zátěž — jen nechce narazit na strop. Výkon je proto **měkká osa se stropem popsaným čísly** (§4.2), ne vyřazovací brána. Přímý důsledek: jazyk, jehož cena se platí denně a výhoda se inkasuje jen při extrémní zátěži, je v tomhle kontextu v nevýhodě.
- **Dvě role, jeden verdikt.** Volba slouží zároveň jako podklad pro doporučení ve firmách. Protože je záběr omezen na zelenou louku, obě role se sbíhají a verdikt je jeden. Firemní role se promítá jinak: zvedá laťku citací (každé nosné tvrzení nese `[R…]`) a dává plnou váhu osám náboru, financování ekosystému, LTS a historie breaking changes (§4.4–§4.6). Kdyby se během rešerše ukázalo, že osobní optimum je jiné než firemní, dokument nechá oba verdikty vedle sebe místo průměru.
- **Profil zadavatele:** full-stack vývojář, sólo nebo malý tým, ČR. Dosavadní těžiště v PHP; to je fakt kontextu, ne výchozí favorit.

## 2. Rozhodovací pravidla (sepsána 2026-08-22 — PŘED rešerší)

Pravidla se píší před měřením; po výsledku se čtou, ne vymýšlejí. **Stav: nepotvrzena zadavatelem** — dokud nejsou, rešerše nezačíná.

### 2.1 Kandidáti

Osm jazyků, řazeno **abecedně** — pořadí je záměrně neutrální, aby samo nenaznačovalo favorita, a **drží se stejné ve všech tabulkách dokumentu**:

`C#` · `Go` · `Java` · `Kotlin` · `PHP` · `Python` · `Rust` · `TypeScript`

Vyřazení kandidáta se zapisuje s důvodem a s odkazem na pravidlo, na kterém padl. Prázdná buňka není vyřazení.

### 2.2 Tvrdé brány

| # | Brána | Zdůvodnění |
|---|---|---|
| **B1** | ❌ v **backendu a API** (nejvýš vážená doména, §2.3) → vyřazen. ❌ v ostatních třech doménách **nevyřazuje** — započítá se váženou cenou (§2.3) a zapíše se do verdiktu jako explicitně přijatý náklad | Jeden jazyk se vybírá především kvůli nejvýš vážené doméně; tam ❌ ruší smysl celé volby. V níže vážené doméně je ❌ drahá, ale zaplatitelná — a poctivější je tu cenu přiznat než kandidáta tiše vyhodit. |
| **B2** | Chybí identifikovatelný plátce ekosystému **nebo** doložitelný závazek k dlouhodobé podpoře → vyřazen | Sázka na dekádu potřebuje někoho, kdo ji financuje. Ověřuje se doložitelně (§4.4, §4.5), ne pověstí. |

**Úprava B2 — DODATEČNÁ, provedená 2026-08-22 AŽ PO výsledku kola 1.** Původní znění výše se nemění a zůstává čitelné; tohle je přílepek, ne přepis, protože pravidlo upravené po zhlédnutí výsledku ztrácí přesně tu vlastnost, kvůli které se píše dopředu.

- **Co se stalo:** B2 vypálila proti TypeScriptu (§4.5). Rešerše zároveň ukázala, že pravidlo míchá dvě různé věci — u běhového prostředí je „podpora“ tikající bezpečnostní povinnost, u překladače je nosným závazkem slib kompatibility. B2 tenhle rozdíl nerozlišovala.
- **Nové znění:** závazek k dlouhodobé podpoře se uznává **buď** datovanou tabulkou podpory, **nebo** doloženým slibem zpětné kompatibility. U jazyka, který se překládá do artefaktu běžícího jinde, se navíc čte životní cyklus **toho běhového prostředí**, ne překladače.
- **Důsledek:** TypeScript bránou prochází — na Node.js s LTS 30 měsíců [R19]. Chybějící politika podpory překladače mu ale **zůstává zapsaná jako náklad** v §4.5 a promítne se do tie-breakerů, ne že by zmizela.
- **Rozhodl:** zadavatel, 2026-08-22, s vyloženou alternativou nechat pravidlo platit a TypeScript vyřadit.
- **Proč to bylo obhajitelné:** záměr B2 byl „kdo to financuje“ a ten Microsoft splňuje bez debat. Klopýtnutí bylo v návrhu měřidla, ne v riziku pod ním. Kdyby chyba byla ve faktech, pravidlo by se nechalo vypálit.

**Poznámka k síle B1 (zapsáno 2026-08-22, před rešerší):** zúžením na backend se z B1 stala spíš pojistka než čepel — je pravděpodobné, že ji projde všech osm kandidátů a že veškerou práci odvede vážená cena v §2.3. Necháváme ji tam vědomě: kdyby se ukázalo, že některý kandidát backend a API pořádně nezvládá, má to být vyřazení, ne položka v součtu.

**Fallback k B1, sepsaný předem:** pokud B1 nepřežije **žádný** kandidát, pravidlo se **nepřepisuje** — zapíše se, že vypálilo a že premisa „jeden jazyk pro tyhle domény“ je nesplnitelná. Verdikt pak zní: nejnižší vážená cena **plus pojmenovaná úniková cesta** pro doménu, kde kandidát padl. Tahle věta je tu proto, aby se po výsledcích nevymýšlela.

### 2.3 Váhy domén a agregační pravidlo

Domény neváží stejně. Váhy určil zadavatel **2026-08-22, před rešerší**:

| Doména | Váha |
|---|---|
| Webový backend a API | 4 |
| CLI, démoni, automatizace | 3 |
| Frontend v prohlížeči | 2 |
| Data, ML, dávkové zpracování | 1 |

**Cena buňky:** ✅ = 0 · 🟡 = 1 · ❌ = 3. **Vážená cena kandidáta** = součet (cena buňky × váha domény). **Vyhrává nejnižší vážená cena.** Čísla jsou tu proto, aby šel výsledek přepočítat ručně a nedal se ohnout výkladem; maximum je 30, nula znamená ✅ ve všech čtyřech.

Původní verze pravidla („vyhrává nejnižší nejhorší buňka“) padla spolu s rovnoměrnými vahami — nešlo ji udržet ve chvíli, kdy ❌ v backendu a ❌ v data/ML mají bolet různě. Nahrazena 2026-08-22, stále před rešerší.

Při shodě rozhodují v tomto **pevně daném pořadí**:

1. přísnost, kterou lze zapnout a **vynutit v CI** (§4.1),
2. velikost náborového rybníka a předatelnost (§4.6),
3. zralost frameworků a knihoven (§4.7).

**Předpověď zapsaná před rešerší.** Tyhle váhy mají důsledky, které jdou pojmenovat teď — a zapsané dopředu je po výsledcích nelze vydávat za očekávané, ani zamlčet, když nevyjdou. Jde o **inferenci, ne ověřená fakta**: Go by mělo stoupnout (backend a CLI jsou jeho domovské domény a zároveň dvě nejvýš vážené; slabiny má v těch dvou nejníž vážených). Pythonu klesla hodnota jeho největší přednosti na váhu 1, zatímco za startup a distribuci platí ve váze 3. Rust zůstává znevýhodněn tím, že výkon není tvrdý požadavek (§1). U JVM a .NET rozhodne, jak dobře dnes fungují nativní obrazy — což je přesně ten případ, kvůli kterému existuje pravidlo M1. Pokud rešerše tuhle předpověď vyvrátí, zapíše se to do dokumentu jako výsledek, ne jako oprava předpovědi.

### 2.4 Metodická pravidla

- **M1 — nejnovější stabilní verze, ale s datem narození.** Hodnotí se aktuální stabilní verze jazyka i frameworků. Každá buňka opřená o mladou vlastnost uvede, **ve které verzi přišla** a **zda ji ekosystém dohnal** (frameworky, ORM, statická analýza). Existence vlastnosti není totéž co její použitelnost; bez tohoto rozlišení by se z poznámek k vydání stal argument.
- **M2 — přísnost se nehodnotí zaškrtávátkem.** Otázka „řeší to typy?“ se rozpadá na pět podotázek a každá má jiného vítěze (§4.1): (a) vynucuje se to za běhu, nebo jen při kontrole; (b) co typový systém vůbec umí vyjádřit; (c) jak nakažlivá je neotypovaná závislost; (d) dá se to vynutit pro všechny v CI a existuje ráčna proti couvání; (e) jaká je cena na zelené louce, kde lze jet přísně od prvního řádku. Rozklad se pouští na **všechny** kandidáty stejně — včetně těch, o kterých se přísnost předpokládá.
- **M3 — každé nosné tvrzení nese `[R…]`.** Tvrzení o neexistenci („nejde“, „neexistuje“, „jen přes“) potřebuje primární zdroj **a** pozitivní kontrolu, že hledání vůbec funguje. Prázdný výsledek hledání není zdroj.
- **M4 — ratingy jsou vázané na tento kontext** (§1) a na nic jiného. Buňka převzatá odjinud je hypotéza, ne fakt.
- **M5 — adversariální průchod je povinný** před verdiktem: samostatný průchod, který se verdikt snaží **vyvrátit**, ne potvrdit. Výsledek se zapisuje do hlavičky.

## 3. Regret matrix: co stojí použít ten který jazyk v té které doméně

Tabulka se **neptá, jak je jazyk v doméně dobrý**. Ptá se: *kolik mě stojí, když v téhle doméně musím použít právě jeho, protože jsem si ho vybral jako svůj jeden jazyk.* Rozdíl je nosný — žebříček nemá poraženého, cena ano.

Symboly: ✅ domovská doména, cena blízko nule · 🟡 použitelné, ale s pojmenovanou cenou · ❌ cena tak vysoká, že bys pro tuhle doménu sáhl po jiném jazyce. Hodnoceno **pro kontext §1** (zelená louka, výkon jako měkká osa), ne obecně.

Stav vyplňování: **všechny čtyři sloupce ověřeny 2026-08-22** (kola 2 až 5, §4.3), vážená cena spočtena podle §2.3. Ceny buněk jsou ✅ = 0, 🟡 = 1, ❌ = 3; váhy 4 · 3 · 2 · 1. **Pořadí je prozatímní** — čtyři buňky čekají na adversariální průchod (M5) a trvanlivá vrstva §4.1, §4.2, §4.6 a §4.7 zatím nemá vstup do tie-breakerů.

Sloupce jsou seřazené **podle váhy domény sestupně** (4 · 3 · 2 · 1, §2.3), aby se tabulka četla zleva od toho, co rozhoduje nejvíc. Poslední sloupec je vážená cena podle §2.3 — nižší je lepší, rozsah 0 až 30.

| Jazyk | Backend a API (×4) | CLI a automatizace (×3) | Frontend v prohlížeči (×2) | Data, ML, dávky (×1) | Vážená cena |
|---|---|---|---|---|---|
| **C#** | ✅ ASP.NET Core je first-party, jeden kalendář s jazykem [R9] | 🟡 Native AOT, ale s toolchainem a zákazem dynamických rysů [R20] | 🟡 Blazor WASM: do prohlížeče jde runtime; past s heapem na iOS [R35] | 🟡 ML.NET first-party; ve Sparku ani Polars není [R43] | **6** |
| **Go** | ✅ `net/http` ve stdlib — žádné druhé okno podpory [R8] | ✅ domovská; vždy křížový překlad [R24] | ❌ ~2 MB dno, 10 MB+ běžně; obstálo v M5 s výhradou (§6.1) [R37] | ❌ chybí v seznamech Sparku i Polars [R44][R45] | **9** |
| **Java** | ✅ Spring Boot; minor ale jen ≥12 měsíců OSS [R31] | 🟡 GraalVM, ale closed-world a JSON metadata [R21] | 🟡 TeaVM (třetí strana); omezení nedoložena [R41] | 🟡 první třída ve Sparku; modelování slabší [R44] | **6** |
| **Kotlin** | ✅ táž cesta jako Java [R31] | 🟡 táž cesta a tytéž výhrady jako Java [R21] | 🟡 Kotlin/Wasm je Beta a klade podmínku na prohlížeč [R36] | 🟡 přes JVM na Java API Sparku (inference) [R44] | **6** |
| **PHP** | ✅ Symfony či Laravel; volba mění okno 4 roky vs. 2 [R28][R29] | 🟡 binárka jen přes projekt třetí strany [R25] | 🟡 `php-wasm` existuje a je živý; ❌ neobstálo v M5 (§6.1) [R42] | ❌ chybí v seznamech Sparku i Polars [R44][R45] | **8** |
| **Python** | ✅ Django, tři roky na každé vydání [R30] | 🟡 bez křížového překladu [R26] | 🟡 Pyodide zralé, plný přístup k Web API; velikost nedoložena [R38] | ✅ jediný v obou seznamech; referenční ekosystém [R44][R45] | **5** |
| **Rust** | 🟡 kalendář podpory nenalezen u Axumu ani u Actixu; posíleno v M5 (§6.1) [R34][R65] | ✅ domovská; Tier 1 napříč OS [R27] | 🟡 evidence hodnotu buňky nedokládá; zůstává jako nejméně zavazující (§6.1) [R40] | 🟡 implementuje Polars; trénování nezjišťováno [R45] | **7** |
| **TypeScript** | ✅ zralé, ale roztříštěné; Fastify ~rok, Express nenalezeno [R32][R33] | 🟡 Node SEA experimentální; `deno compile` zralé, ale jiný runtime [R22][R23] | ✅ prohlížeč je nativní cíl; jediná nula ve sloupci [R39] | 🟡 Polars přes Node.js, TensorFlow.js [R45][R46] | **4** ⬅ nejnižší |

### 3.1 Jak tabulku číst (k 2026-08-23, po adversariálním průchodu)

**Pořadí podle vážené ceny** (nižší je lepší, rozsah 0 až 30):

| # | Jazyk | Výpočet | Vážená cena |
|---|---|---|---|
| 1. | **TypeScript** | 0×4 + 1×3 + 0×2 + 1×1 | **4** |
| 2. | **Python** | 0×4 + 1×3 + 1×2 + 0×1 | **5** |
| 3.–5. | **C#**, **Java**, **Kotlin** | 0×4 + 1×3 + 1×2 + 1×1 | **6** |
| 6. | **Rust** | 1×4 + 0×3 + 1×2 + 1×1 | **7** |
| 7. | **PHP** | 0×4 + 1×3 + 1×2 + 3×1 | **8** |
| 8. | **Go** | 0×4 + 0×3 + 3×2 + 3×1 | **9** |

*Pořadí po adversariálním průchodu (§6.1, 2026-08-23). Před ním mělo PHP 12 a bylo poslední; po zrušení nedoloženého ❌ v prohlížeči má 8 a poslední je Go. Vedoucí dvojice se nezměnila.*

**Předpověď z §2.3 se nepotvrdila, a nejde o drobnost.** Psal jsem, že by mělo stoupnout Go. Skončilo sedmé z osmi. Důvod je přesně ten mechanismus, který odhalilo kolo 3: **obě nuly Go leží tam, kde nuly nic nevynášejí.** V backendu má nulu každý, takže se z ní pořadí neposune, a druhá nula je v CLI. Zato dvě ❌ v prohlížeči a v datech se do součtu propíšou plnou vahou. Předpověď selhala proto, že jsem uvažoval o silných stránkách kandidáta místo o rozptylu uvnitř sloupců. Zůstává zapsaná v §2.3 tak, jak byla napsána, a tohle je její vyhodnocení, ne oprava.

**Vyhrává zatím TypeScript, a je to jediný kandidát s nulou tam, kde ji nemá nikdo jiný** (§4.3, prohlížeč). Platí jen v CLI a v datech.

**Tři věci, které to pořadí zatím nesmí učinit verdiktem.**

1. **Vítěz je ten, proti komu v kole 1 vypálila brána B2** (§4.5). Kdyby zadavatel zvolil variantu „nechat pravidlo platit“, byl by dnešní vítěz vyřazen dřív, než se cokoli spočítalo. Citlivost verdiktu na jedno rozhodnutí o pravidle je tím doložená, ne domnělá — a patří do verdiktu jako přiznaný předpoklad.
2. **Čtyři buňky jsou označené jako nejisté** a jdou přednostně do M5: Rust v backendu, Go a PHP v prohlížeči, Rust v prohlížeči. Kdyby ❌ u Go v prohlížeči neobstálo, Go se posouvá z 9 na 7 nebo 5.
3. **Tie-breakery zatím nemají vstup.** Trojice C#, Java a Kotlin je na shodných 6 a rozhodne o ní až §4.1, §4.6 a §4.7 — tedy přísnost vynutitelná v CI, náborový rybník a zralost frameworků.

## 4. Trvanlivá vrstva (nese verdikt)

### 4.1 Přísnost, kterou lze zapnout a vynutit (ověřeno 2026-08-22)

Otázka „řeší to typy?“ nemá odpověď ano/ne. Podle pravidla M2 (§2.4) se rozpadá na pět podotázek a **každá má jiného vítěze**. Rozklad je puštěný na všech osm stejně — včetně těch, u kterých se přísnost automaticky předpokládá.

#### (a) Vynucuje se to za běhu, nebo jen při kontrole?

Nejsou dvě skupiny, jak by se čekalo, ale **tři** — a ta prostřední je ta, o které se nemluví.

| Skupina | Kdo | Doložení |
|---|---|---|
| **Vynucuje běh** | Java, Kotlin, C#, Go, Rust | Špatný typ neprojde, protože ho odmítne runtime nebo se k němu vůbec nedá dostat. **Ale každý má výjimku, viz níže.** |
| **Vynucuje běh jen po souborech** | PHP | Typy se kontrolují za běhu — *"ensure that the value is of the specified type at call time, otherwise a `TypeError` is thrown"*. Jenže přísný režim je direktiva **na soubor**: *"Strict typing only applies to function calls made within the file with strict typing enabled. Callers without strict typing will still coerce values."* Bez direktivy PHP hodnoty **koeruje** — `sum(1.5, 2.5)` vrátí `int(3)` [R49]. |
| **Nevynucuje vůbec** | Python, TypeScript | Python: *"The Python runtime does not enforce function and variable type annotations. They can be used by third party tools such as type checkers, IDEs, linters, etc."* [R47] TypeScript: typy se při překladu mažou a výstupem je prostý JavaScript [R39]. |

**Výjimky u té první skupiny jsou podstatné a u dvou z nich zásadní:**

- **Java — generika se za běhu mažou.** Type erasure nahradí typové parametry jejich mezí nebo `Object`em; `List<String>` je v bytekódu jen `List` a *"generics incur no runtime overhead"*. Typová bezpečnost generik je tedy u Javy **stejně jako u Pythonu věcí kontroly, ne běhu** [R55].
- **C# — nullabilita se za běhu nevynucuje vůbec.** Dokumentace to říká rovnou: *"The runtime behavior of your program is unchanged. Nullable reference types are entirely a compile-time feature."* [R50]
- **Kotlin — díra je Java.** Nullabilita je součástí typového systému a kompilátor ji vynucuje, ale při volání javového kódu vznikají **platform types** bez informace o nullabilitě, a to je jedna z mála cest, jak v Kotlinu dostat NPE [R52].
- **Go — nemá null safety.** `nil` je nulová hodnota ukazatelů, řezů, map, kanálů, rozhraní i funkcí, takže neinicializovaná proměnná těchto typů je `nil` a jazyk před tím nechrání [R54].
- **Rust — jediný, kdo tu díru nemá.** *"Rust doesn't have the null feature that many other languages have"*; místo toho `Option<T>`, přičemž *"the compiler won't let us use an `Option<T>` value as if it were definitely a valid value"* a hodnotu, která smí chybět, musíš **explicitně opt-in** [R53].

#### (b) Co typový systém umí vyjádřit

| Jazyk | Nullabilita v typovém systému | Generika | Poznámka |
|---|---|---|---|
| **C#** | Ano, anotacemi a analýzou toku [R50] | Ano, za běhu skutečná | Dvě doložené pasti, viz (c) |
| **Go** | Ne — `nil` je nulová hodnota [R54] | Ano, od **Go 1.18** [R54] | |
| **Java** | Ne v jazyce | Ano, ale **mazaná** [R55] | |
| **Kotlin** | Ano, vynucená kompilátorem [R52] | Ano (JVM, tedy s mazáním) | Nejsilnější nullabilita na JVM |
| **PHP** | Částečně (`?int`), za běhu | **Nemá vůbec** — v jazyce neexistují; žijí jen jako komentáře pro statickou analýzu [R49] | Největší mezera z osmi |
| **Python** | Ano v anotacích, nevynucená | Ano v anotacích, nevynucená | Vše stojí na kontrole |
| **Rust** | Nemá null; `Option<T>` [R53] | Ano | Nejsilnější z osmi |
| **TypeScript** | Ano, `strictNullChecks` [R51] | Ano, mazaná | |

#### (c) Jak nakažlivá je neotypovaná závislost a kudy vede únik

- **Python — `Any` je nakažlivé z definice.** *"A static type checker will treat every type as assignable to `Any` and `Any` as assignable to every type"*, a co je horší: *"no type checking is performed when assigning a value of type `Any` to a more precise type"* [R47]. Jedna neotypovaná knihovna tedy tiše vypne kontrolu všemu, co skrz ni protéká, a **nikde to nesvítí červeně**.
- **C# — `!` a dvě pasti.** Operátor odpuštění nullu je popsán bez příkras: *"Each occurrence is a place the compiler can no longer protect you."* K tomu dvě doložené situace, kdy nenullovatelná reference drží `null` **bez varování**: struktura vytvořená přes `default` a nové pole referenčního typu, jehož prvky jsou do přiřazení `null` [R50]. Na druhou stranu od .NET 5 jsou anotované všechny běhové knihovny .NET, takže nakažlivost z ekosystému je tu menší než u Pythonu [R50].
- **Kotlin** — únikem jsou platform types z Javy a `!!` [R52]. **PHP** — volající ze souboru bez direktivy koeruje [R49]. **TypeScript** — `any` a `@ts-expect-error`. **Java** — mazání a raw typy [R55]. **Go** — `any` a typové aserce. **Rust** — `unwrap()` a `unsafe`.

#### (d) Dá se to vynutit pro všechny v CI a existuje ráčna?

**A tady je přímá odpověď na otázku, kvůli které tenhle dokument vznikl: nakolik to mypy doopravdy řeší.**

`mypy --strict` zapíná dvanáct volitelných kontrol včetně `--disallow-untyped-defs`, `--disallow-untyped-calls`, `--disallow-any-generics` a `--warn-return-any`. Ráčna proti couvání existuje a je přímo v `--strict`: `--warn-unused-ignores` *"will make mypy report an error whenever your code uses a `# type: ignore` comment on a line that is not actually generating an error message"* [R48].

Jenže **`--strict` sám vymezuje, kde jeho záruka končí**, a stojí to v jeho vlastním popisu: *"strict will catch type errors as long as intentional methods like type ignore or casting were not used."* [R48] A ještě jedna věc, která překvapí: **`--disallow-any-explicit` v `--strict` není.** Explicitní `Any` tedy přísný režim nezakazuje; musíš ho zapnout zvlášť.

Souhrnná odpověď: **mypy řeší body (b), (d) a částečně (c). Bod (a) neřeší vůbec a řešit ho nemůže.** Hodnota, která přijde z JSONu, z databázového driveru nebo z neotypované knihovny, vstupuje jako `Any` a mypy o ní z principu mlčí. Převádí tedy „typy jsou dokumentace“ na „typy jsou kontrolované při buildu, pro kód, který vlastníš, minus explicitní úniky“ — což je hodně, ale není to „runtime odmítne špatnou hodnotu“.

**Týž rozklad na C#, jak slibuje M2.** Nullable reference types jsou *"entirely a compile-time feature"*, `!` vypíná ochranu po jednotlivých výskytech a dvě doložené pasti vyrobí `null` v nenullovatelné referenci beze slova [R50]. C# je na tom v (a) u nullability **stejně jako Python u typů** — s tím rozdílem, že zbytek typového systému mu runtime vynucuje.

**TypeScript** má `strict` jako rodinu přepínačů se *"stronger guarantees of program correctness"*, ale dokumentace k němu přidává vlastní cenu: *"Future versions of TypeScript may introduce additional stricter checking under this flag, so upgrades of TypeScript might result in new type errors in your program."* [R51] Přísnost, která ti pod rukama roste — u projektu na dekádu je to náklad, ne detail.

*Úrovně PHPStan a Psalm pro PHP v tomto kole zjišťovány nebyly; buňka PHP v tomto bodě je proto neúplná.*

#### (e) Cena na zelené louce

Klasická stížnost na postupné typování — že se dolepuje na starý kód — se **v tomhle kontextu neuplatní** (§1: všechny projekty jsou nové). Na zelené louce jde jet přísně od prvního řádku a pokrytí anotacemi je otázkou disciplíny, ne migrace. To Python a TypeScript posiluje víc, než jak se o nich obvykle mluví.

**Ale — a tohle je celý rozdíl — zelená louka opravuje pokrytí, ne hranici vynucení.** Ať je CI jakkoli přísné, bod (a) zůstává tam, kde byl: v Pythonu a TypeScriptu runtime typy nekontroluje, takže špatná hodnota z neověřené hranice projde dovnitř a spadne daleko od místa vzniku.

#### Důsledek pro tie-breaker

Tie-breaker 1 (§2.3) je právě „přísnost vynutitelná v CI“ a rozhoduje o trojici na shodné vážené ceně 6. Podle rozkladu výše vychází pořadí **Kotlin › C# › Java**: Kotlin má nullabilitu v typovém systému a vynucenou kompilátorem, C# ji má jen jako věc překladu s dokumentovanými pastmi, ale generika mu za běhu drží, a Java nemá ani jedno — nullabilita v jazyce chybí a generika se mažou.

### 4.2 Výkonový strop a model souběžnosti (ověřeno 2026-08-22)

Výkon není v tomhle kontextu brána (§1), takže se neptám „který je rychlejší“, ale **co se stane, až budeš potřebovat dělat víc věcí najednou**. To je trvanlivá vlastnost jazyka, kdežto benchmark je snímek.

| Model | Kdo | Doložení |
|---|---|---|
| **Lehká vlákna plánovaná runtimem** | Go, Java, Kotlin | Go: goroutina *"is lightweight, costing little more than the allocation of stack space"* a goroutiny jsou *"multiplexed onto multiple OS threads so if one should block, such as while waiting for I/O, others continue to run"* [R59]. Java od **JDK 21**: virtuální vlákna, kterých *"we can easily have a great many active virtual threads, even millions, running in the same Java process"* [R57]. |
| **Smyčka událostí plus výslovní workeři** | TypeScript (Node) | *"Workers (threads) are useful for performing CPU-intensive JavaScript operations. They do not help much with I/O-intensive work. The Node.js built-in asynchronous I/O operations are more efficient than Workers can be."* Stabilita 2 — Stable [R58]. |
| **Globální zámek, který se právě odstraňuje** | Python | Viz níže — nejzajímavější případ z celé osmičky. |
| **Jen kooperativní souběžnost** | PHP | Fibers od **PHP 8.1** jsou přerušitelné funkce s vlastním zásobníkem [R60]; jde o kooperativní souběžnost, ne o paralelismus. |
| *Nezjišťováno v tomto kole* | C#, Rust | `async`/`await` a `Task` u C#, `async` a vlákna u Rustu zjišťovány nebyly — buňky jsou neúplné. |

**Poctivost k Javě, protože se to snadno přežene.** Dokumentace sama varuje před tím, jak se virtuální vlákna čtou: *"Virtual threads are not faster threads; they do not run code any faster than platform threads. They exist to provide scale (higher throughput), not speed (lower latency)."* [R57] Řeší tedy propustnost při čekání na I/O, ne výpočetní strop.

**Python a GIL — učebnicový případ pravidla M1.** Volnovláknový build bez GIL existuje od **Pythonu 3.13**, ale **není výchozí** a dokumentace k němu uvádí dvě konkrétní ceny. Ekosystém: *"Some third-party packages, in particular ones with an extension module, may not be ready for use in a free-threaded build, and will re-enable the GIL."* — jedna nepřipravená C rozšíření tedy zámek **zapne zpátky**. A jednovláknový výkon: *"the average overhead ranges from about 1% on macOS aarch64 to 8% on x86-64 Linux systems"* [R56].

To je přesně to, kvůli čemu M1 existuje: vlastnost je vydaná, ale ekosystém ji nedohnal a dokument to musí říct, místo aby napsal „Python už GIL nemá“.

### 4.3 Čím se platí za každou ze čtyř domén

**▸ CLI, démoni a automatizace (váha 3) — ověřeno 2026-08-22**

Rozhoduje tu jedna otázka: **dostane se můj nástroj na cizí stroj, aniž bych tam musel nejdřív nainstalovat běhové prostředí?** Odpověď rozděluje osmičku ostřeji než cokoli jiného v tomhle dokumentu.

| Jazyk | Samostatná binárka | Křížový překlad | Cena a výhrady | Zdroj |
|---|---|---|---|---|
| **C#** | Native AOT — self-contained, bez nainstalovaného .NET | 🟡 zdroj mlčí o překladu mezi OS; dokumentace uvádí, že binárka vyrobená na Linuxu poběží na *"same or newer Linux version"* | Vyžaduje toolchain na hostiteli (clang a zlib na Linuxu, C++ workload ve Visual Studiu). Zakázáno: dynamické načítání sestav, `System.Reflection.Emit`, C++/CLI, vestavěné COM na Windows. Vynucuje trimming. `System.Linq.Expressions` běží vždy interpretovaně. *"Not all the runtime libraries are fully annotated to be Native AOT compatible."* | [R20] |
| **Go** | Ano, standardně | ✅ na libovolný cíl z libovolného hostitele | Domovská doména. Dokumentace to říká rovnou: *"In effect, you are always cross-compiling."* Cílů je přes dvacet kombinací OS a architektury. | [R24] |
| **Java** | Přes GraalVM Native Image — *"Starts in milliseconds"*, bez nainstalované JVM | 🟡 nezjišťováno v tomto kole | **Closed-world assumption.** Analýza je statická a *"does not run your application"*, takže *"cannot always exhaustively predict all usages of the Java Native Interface (JNI), Java Reflection, Dynamic Proxy objects, or class path resources"* — chybějící místa se dopisují ručně do JSON metadat. V ekosystému postaveném na reflexi je to opakovaný náklad, ne jednorázový. Bez native image potřebuje cílový stroj JVM. | [R21] |
| **Kotlin** | Táž cesta jako Java (JVM + GraalVM) | 🟡 nezjišťováno v tomto kole | Tytéž výhrady jako u Javy [R21]. Kotlin/Native jako druhá cesta v tomto kole nezjišťován. | [R21] |
| **PHP** | Přes `static-php-cli` — staticky slinkovaná binárka bez systémového PHP | 🟡 Linux, macOS a FreeBSD lokálně; Windows jen přes GitHub Actions | Zásadní rozdíl proti ostatním: **není to oficiální nástroj jazyka**, ale projekt třetí strany (MIT, autor crazywhalecc). Podporuje PHP 8.2–8.5. Zralost knihoven pro dlouhoběžící démony a systémovou automatizaci v tomto kole nezjišťována — hodnocení stojí zatím jen na distribuci. | [R25] |
| **Python** | Přes PyInstaller, režim one-file | ❌ *"PyInstaller does not support cross-compilation"* — pro každý OS a verzi Pythonu je nutné pustit build na tom OS | One-file se při každém spuštění rozbaluje do dočasné složky, což start zpomaluje oproti one-folder. Na strojích, kde Python už je, žádný z těchto nákladů nevzniká — proto je to cena za distribuci, ne za psaní. | [R26] |
| **Rust** | Ano, standardně | ✅ Tier 1 pokrývá Linux, macOS i Windows na x86-64 i ARM64, s oficiálními buildy a automatickými testy po každé změně | Domovská doména. Tier 1 znamená *"Guaranteed to work"*, Tier 2 *"Guaranteed to build"*. | [R27] |
| **TypeScript** | Dvě cesty, obě funkční, každá s jinou cenou | ✅ přes `deno compile` (Windows, macOS, Linux × x64 i ARM64) | **Node SEA** je *"Stability: 1.1 - Active development"*, `require()` a `import` ve vloženém skriptu čtou jen vestavěné moduly, křížové sestavení vyžaduje vypnout `useCodeCache` i `useSnapshot`, macOS x64 se netestuje a na Linux arm64 v Dockeru je známý pád na `process.dlopen()`. **`deno compile`** je podstatně vyzrálejší a přibaluje osekaný runtime — ale volbou Dena volíš jiný runtime než Node, tedy odbočku uvnitř téhož jazyka. | [R22][R23] |

**Co z toho plyne.** Go a Rust jsou tu jediné, kde distribuce nestojí **nic** — binárka je výchozí výstup překladu a křížový překlad je vlastnost jazyka, ne přílepek. Všichni ostatní si samostatnou binárku musí koupit: C# a Java toolchainem a omezením dynamických rysů, PHP závislostí na projektu třetí strany, Python vzdáním se křížového překladu, TypeScript volbou mezi experimentální cestou a jiným runtime.

Tím se **potvrzuje ta část předpovědi z §2.3, která se týkala Go** — ale z jiného důvodu, než jsem psal. Nepředpovídal jsem křížový překlad, předpovídal jsem obecně „domovskou doménu“. Doložilo se to konkrétněji a zároveň to platí stejně silně pro Rust, kterého jsem v téhle doméně nezmiňoval.

**▸ Webový backend a API (váha 4) — ověřeno 2026-08-22**

Tady nezáleží na tom, jestli jazyk backend „umí“ — umí ho všech osm. Rozhoduje něco jiného a je to trvanlivé: **v backendu tě neváže životní cyklus jazyka, ale frameworku, a ten je u většiny kandidátů podstatně kratší.** Sledovat tedy musíš dvě okna, ne jedno.

| Jazyk | Hlavní framework | Okno podpory frameworku | Kolik oken musíš hlídat | Zdroj |
|---|---|---|---|---|
| **C#** | ASP.NET Core — součást .NET, od téhož výrobce | Shodné s .NET: LTS 36 měsíců | **Jedno** — framework a jazyk mají jeden kalendář | [R9] |
| **Go** | `net/http` ve **standardní knihovně** | Žádné samostatné; kryje ho Go 1 compatibility promise | **Žádné navíc** — jediný z osmi, kdo druhý kalendář nemá vůbec | [R8] |
| **Java** | Spring Boot | Minor *"at least 12 months"*, major *"at least 3 years"*; nové vydání každých šest měsíců (květen a listopad) | Dvě | [R31] |
| **Kotlin** | Spring Boot (Ktor v tomto kole nezjišťován) | Tytéž hodnoty jako u Javy | Dvě | [R31] |
| **PHP** | Symfony **nebo** Laravel — a rozdíl mezi nimi je dvojnásobný | Symfony LTS: 3 roky oprav + **4 roky bezpečnosti**. Laravel: 18 měsíců oprav + **2 roky bezpečnosti** | Dvě, a volba frameworku ti okno zdvojnásobí nebo zkrátí na polovinu | [R28][R29] |
| **Python** | Django | Tři roky; od vydání 2028 dostane **každé** feature vydání týchž tři roky, ne jen LTS | Dvě | [R30] |
| **Rust** | Axum | Datovaná politika podpory **nenalezena** v kořeni repozitáře ani v adresáři crate `axum` (pozitivní kontrola prošla — `Cargo.toml` se v obou výpisech objevil) | Dvě, z toho jedno bez zveřejněného kalendáře | [R34] |
| **TypeScript** | Fastify, Express a další — vrstva je roztříštěná | Fastify: minimum šest měsíců plus dalších šest po vydání následujícího major, tedy zhruba rok. Express: politika **nenalezena** — a přiznávám, že tenhle závěr je slabý, protože pozitivní kontrola u repozitáře s dokumentací selhala (viz [R33]) | Dvě | [R32][R33] |

**Nález, který jsem nečekal a který mění čtení §2.3.** Backend má nejvyšší váhu (4), ale je to **nejméně rozlišující sloupec celého dokumentu** — sedm z osmi kandidátů je tu na stejné úrovni. A protože se vážená cena počítá jako součin ceny buňky a váhy, doména, kde jsou všichni stejní, přispívá **všem stejně**, tedy nerozhoduje o pořadí vůbec. Vysoká váha sama o sobě vliv nedělá; vliv dělá **rozptyl uvnitř sloupce**.

Prakticky z toho plyne, že verdikt nerozhodne backend s vahou 4, ale **CLI s vahou 3**, kde se buňky opravdu liší (§4.3 výše). To je proti intuici, se kterou se váhy zadávaly, a je to důsledek pravidla §2.3, ne jeho porušení — pravidlo se nemění, jen se ukazuje, jak se chová.

Jediný, koho backend odděluje, je **Rust**, a jeho 🟡 stojí zatím na jediné ose (chybějící zveřejněný kalendář podpory u Axumu). Šíře ekosystému pro autentizaci, ORM a administraci v tomto kole zjišťována nebyla, takže **tuhle buňku označuji za nejistou a posílám ji přednostně do adversariálního průchodu** (M5).

**▸ Webový frontend v prohlížeči (váha 2) — ověřeno 2026-08-22**

Jediná doména, kde má jeden kandidát výhodu, kterou mu ostatní nemohou vzít: **prohlížeč je nativní cíl TypeScriptu, ne jeho exportní trh.** Ostatních sedm se do prohlížeče dostává přes WebAssembly nebo transpilaci a každý za to platí něčím jiným.

| Jazyk | Cesta do prohlížeče | Doložená cena | Zdroj |
|---|---|---|---|
| **C#** | Blazor WebAssembly, first-party | *"The Blazor app, its dependencies, and the .NET runtime are downloaded to the browser"* — do prohlížeče tedy putuje běhové prostředí. Zmírnění jsou dokumentovaná: balení Webcil, IL trimming při každém Release buildu, statická komprese Brotli a Gzip. Konkrétní past: výchozí `EmccMaximumHeapSize` je 2 GB a na Safari v iOS ho může být nutné snížit, jinak aplikace spadne. | [R35] |
| **Go** | `GOOS=js GOARCH=wasm`, oficiální cíl | *"Go generates large Wasm files, with the smallest possible size being around ~2MB"* a *"10MB+ is common"*. Soubor `wasm_exec.js` musí pocházet z **téže hlavní verze** kompilátoru — *"Other combinations are not supported."* TinyGo se dostane na ~10 kB, ale je to jiný kompilátor s jiným podmnožinovým chováním. | [R37] |
| **Java** | TeaVM — *"an ahead-of-time compiler for Java bytecode that emits JavaScript and WebAssembly that runs in a browser"* | Projekt třetí strany, ne oficiální cesta jazyka. Konkrétní omezení a velikosti výstupu se na úvodní stránce nedokládají — **mezera v evidenci**, hodnocení proto stojí jen na tom, že cesta existuje a je aktivní. | [R41] |
| **Kotlin** | Kotlin/Wasm, first-party, plus Compose Multiplatform | **Stav Beta** podle vlastní dokumentace. Vyžaduje *"a browser version that supports WebAssembly's garbage collection and legacy exception handling proposals"* — tedy podmínku na straně návštěvníka. Kotlin/JS jako druhá cesta v tomto kole nezjišťován. | [R36] |
| **PHP** | `php-wasm` | Jednoznačně nejtenčí cesta z osmi: projekt třetí strany pod Apache-2.0, fakticky jednoho udržovatele. Pokrývá PHP 8.0–8.5, vazba na DOM jde přes samostatný balíček. Existuje a je aktivní — ale psát v tom uživatelské rozhraní je něco jiného než umět v prohlížeči spustit PHP. | [R42] |
| **Python** | Pyodide — *"a port of CPython to WebAssembly/Emscripten"* | Zralejší, než se čeká: *"Any pure Python package with a wheel available on PyPi is supported"*, včetně NumPy, pandas, SciPy a scikit-learn, plus obousměrné rozhraní na JavaScript a *"full access to the Web APIs"*. **Velikost stahovaného runtime se nepodařilo doložit** — stránka s údaji vrátila 403, takže žádné číslo netvrdím. | [R38] |
| **Rust** | `wasm32`, plus frameworky mimo standardní knihovnu | Doložený signál je nepříjemný, ale úzký: oficiální kniha pracovní skupiny Rust a WebAssembly nese oznámení *"This project and website is no longer maintained."* **Pozor na rozsah — to je o té knize a webu, ne o cílové platformě ani o frameworcích**, které zjišťovány nebyly. Buňka proto stojí na neúplné evidenci. | [R40] |
| **TypeScript** | Žádná — prohlížeč **je** cíl | *"TypeScript is JavaScript's runtime with a compile-time type checker"*; typy se při překladu mažou a výstupem je prostý JavaScript, který *"is **guaranteed** to run the same way"*. Cena nula, a je to jediná nula v tomto sloupci. | [R39] |

**Co z toho plyne.** Frontend je zrcadlovým obrazem CLI: tam měly nulovou cenu Go a Rust, tady ji má jedině TypeScript. A protože §2.3 sčítá vážené ceny, rozhodne se verdikt na tom, jestli je nula v CLI (váha 3) cennější než nula ve frontendu (váha 2) — což při zadaných vahách vychází ve prospěch CLI, ale ne o tolik, aby to bylo bez debaty.

**Tři buňky tohoto sloupce označuji za nejisté a posílám je do adversariálního průchodu (M5):** ❌ u Go (stojí na doložených velikostech, ale TinyGo je nezkoumaná úniková cesta), ❌ u PHP (stojí na tenkosti ekosystému, což je soud, ne měření) a 🟡 u Rustu (evidence je úzká a týká se dokumentace, ne platformy).

**▸ Data, ML a dávkové zpracování (váha 1) — ověřeno 2026-08-22**

Doména se ve skutečnosti skládá ze tří různých úloh a každá má jiného vítěze, což běžná zkratka „na data se používá Python“ zakrývá. Hodnotil jsem podle dvou referenčních nástrojů, u nichž je seznam podporovaných jazyků v dokumentaci **vyjmenovaný**, takže z něj lze číst i nepřítomnost.

- **Apache Spark** (dávkové zpracování): *"It provides high-level APIs in Java, Scala, Python and R"*; nativním implementačním jazykem je Scala [R44].
- **Polars** (dataframy): *"an analytical query engine for DataFrames, written in Rust"*, s vazbami pro *"Python, Rust, Node.js, R, and SQL"* [R45].

Z těch dvou seznamů plyne rozdělení: **Python je v obou. Java je ve Sparku. Rust Polars přímo implementuje. TypeScript má vazbu na Polars přes Node.js a k tomu TensorFlow.js pro prohlížeč i Node [R46]. C# má vlastní first-party ML.NET, používaný podle Microsoftu v Power BI, Defenderu, Outlooku a Bingu, ale s pozicí integrátora TensorFlow a ONNX, ne jejich náhrady [R43]. Go a PHP nejsou ani v jednom z obou seznamů.**

| Jazyk | Doložená pozice | Zdroj |
|---|---|---|
| **C#** | ML.NET, first-party a provozně prověřený; v seznamech Sparku ani Polars není | [R43][R44][R45] |
| **Go** | Není v seznamu jazyků Sparku ani Polars | [R44][R45] |
| **Java** | První třída ve Sparku pro dávkové zpracování; modelování slabší | [R44] |
| **Kotlin** | Přes JVM dosáhne na Java API Sparku *(inference — Kotlin sám v seznamu jmenován není)* | [R44] |
| **PHP** | Není v seznamu jazyků Sparku ani Polars | [R44][R45] |
| **Python** | Jediný jazyk přítomný v obou seznamech; referenční ekosystém domény | [R44][R45] |
| **Rust** | Implementuje Polars. Ekosystém pro trénování modelů v tomto kole nezjišťován | [R45] |
| **TypeScript** | Vazba na Polars přes Node.js; TensorFlow.js pro prohlížeč i Node | [R45][R46] |

**Rozsah tohoto hodnocení je úmyslně úzký.** Stojí na dvou nástrojích, ne na průzkumu celé domény, a nepřítomnost v seznamu znamená nepřítomnost **v tom seznamu** — ne, že v jazyce nejde zpracovat data. Při váze 1 je to úměrná investice; kdyby doména vážila víc, tenhle podklad by nestačil.

### 4.4 Kdo ekosystém platí (ověřeno 2026-08-22)

Otázka pro bránu B2 nezní „je to open source“, ale **kdo platí lidi, kteří to udržují**. Odpověď se u těch osmi rozpadá na tři různé modely a ten rozdíl je trvanlivější než kterákoli jazyková vlastnost.

| Jazyk | Kdo platí a řídí vývoj | Model | Zdroj |
|---|---|---|---|
| **C#** | Microsoft. .NET Foundation je výslovně organizace pro **komunitní projekty** kolem platformy, ne pro vývoj samotného .NET — ten řídí Microsoft | firemní | [R10] |
| **Go** | Google — „standardní“ kompilátor `gc` a toolchain udržuje *"the Go team at Google"* | firemní | [R7] |
| **Java** | Oracle (OpenJDK) plus pracovní skupina Eclipse Adoptium: strategičtí členové Alibaba, IBM, Microsoft; podnikoví Fujitsu, Bloomberg, Canonical, Red Hat | smíšený: firma + nadace | [R11][R12] |
| **Kotlin** | Kotlin Foundation, založená **JetBrains a Googlem**; další členové Meta, Gradle, Touchlab, Uber, Kotzilla, Block. Mezi vyhlášené úkoly patří *"Control incompatible changes to the language"* a *"Preserve the Kotlin trademarks"* | nadace, dva dominantní zakladatelé | [R13] |
| **PHP** | PHP Foundation — **smluvně platí deset vývojářů** na částečný i plný úvazek; platinoví sponzoři JetBrains, Automattic, Sovereign Tech Agency, zlatí Laravel, GoDaddy, team.blue | nadace, široká sponzorská základna | [R3] |
| **Python** | Python Software Foundation — drží duševní vlastnictví většiny vydání a ochranné známky, zaměstnává *"CPython Developer in Residence"* | nadace | [R5] |
| **Rust** | Rust Foundation — zakládající platinoví členové AWS, Google, Huawei, Meta, Microsoft, Mozilla (leden 2021), přes 50 organizací | nadace, široká firemní základna | [R15] |
| **TypeScript** | Microsoft | firemní | [R17][R18] |

**Co z toho plyne pro sázku na dekádu.** Brána B2 v části „plátce“ neodfiltrovala **nikoho** — všech osm má dohledatelného financiéra. Rozdíl je v tom, na kom to stojí: u Go, TypeScriptu a C# na jediné firmě, u Kotlinu na nadaci se dvěma dominantními zakladateli, u PHP, Pythonu, Rustu a Javy na širší základně. To není hodnocení kvality — Microsoft ani Google z těch jazyků zítra neodejdou — ale je to jiný typ rizika a patří do trvanlivé vrstvy, protože se nemění s verzí.

*Poznámka ke zdrojům: oficiální stránka Oracle Java SE Support Roadmap vrátila 2026-08-22 HTTP 403 a nepodařilo se ji načíst. Údaje o Javě proto stojí na Eclipse Adoptium [R11][R12], což je pro tento kontext stejně relevantnější — jde o bezplatnou distribuci, ne o placenou podporu Oracle.*

### 4.5 Závazky podpory a zpětná kompatibilita (ověřeno 2026-08-22)

| Jazyk | Délka podpory jedné verze | Konkrétně k 2026-08-22 | Slib zpětné kompatibility | Zdroj |
|---|---|---|---|---|
| **C#** | LTS 36 měsíců (sudá čísla), STS 24 měsíců (lichá); nové hlavní vydání každý listopad | .NET 10 (LTS) do 14. 11. 2028; .NET 8 i 9 do 10. 11. 2026 | — nezjišťováno v tomto kole | [R9] |
| **Go** | Do vydání **dvou novějších** hlavních verzí — při kadenci dvou vydání ročně zhruba rok *(inference z politiky a pozorované kadence)* | Go 1.27.0 vydáno 19. 8. 2026 | **Go 1 compatibility promise:** *"programs written to the Go 1 specification will continue to compile and run correctly, unchanged, over the lifetime of that specification"* — na úrovni zdrojáku, s deseti vyjmenovanými výjimkami; binární kompatibilita zaručena není | [R6][R7][R8] |
| **Java** | Adoptium: jedno LTS **každé dva roky** od 2021, podpora *"for at least four years"*, zdarma | JDK 25 nejméně do 9/2031 · JDK 21 nejméně do 12/2029 · JDK 17 nejméně do 10/2027 | — nezjišťováno v tomto kole | [R11] |
| **Kotlin** | Bez datované tabulky LTS. Na JVM podporuje **nejméně tři předchozí jazykové a API verze** vedle poslední stabilní | — | Novější kompilátor čte starší binárky; nekompatibilní změny přes dvoufázový deprecation cyklus; přepínače `-language-version` a `-api-version` emulují starší chování | [R14] |
| **PHP** | 2 roky aktivní podpory + 2 roky bezpečnostních oprav = **4 roky** | 8.4 bezpečnostně do 31. 12. 2028 · 8.5 do 31. 12. 2029 · 8.2 končí 31. 12. 2026 | — nezjišťováno v tomto kole | [R2] |
| **Python** | PEP 602: ~2 roky oprav chyb + ~3 roky bezpečnostních = **5 let**, *"Five years after a release, support ends"* | Nejdelší okno z celé osmičky | — nezjišťováno v tomto kole | [R4] |
| **Rust** | Bez datované tabulky LTS | — | Nejsilnější formulace z celé osmičky: *"once a feature is released through stable, contributors will continue to support that feature for all future releases"*. Nekompatibilní změny jdou do **edicí**, které jsou opt-in a **navzájem plně interoperabilní** — každý crate se stěhuje nezávisle | [R16] |
| **TypeScript** | ⚠️ opraveno v §8: politika **existuje**, ale je podmíněná dodáním v produktu Microsoftu a nedává verzím vlastní kalendář | — | — nezjišťováno v tomto kole | [R17][R18][R66] |

**Dvě věci, které tahle tabulka odhalila a které jsem nečekal.**

**Za prvé: „podpora“ znamená u kompilátoru něco jiného než u běhového prostředí, a brána B2 ten rozdíl nerozlišuje.** U PHP, Pythonu, Javy a .NET je podpora hodinami tikající povinnost — neaktualizovaná verze je bezpečnostní dluh vystavený internetu. U Go, Rustu, Kotlinu a TypeScriptu je nosnějším závazkem **slib kompatibility**: starý kód se dál překládá a artefakt běží dál. Rustova formulace („co jednou vyjde jako stabilní, podporujeme ve všech budoucích vydáních“) je věcně silnější závazek k dekádě než kterákoli datovaná tabulka LTS, přestože žádnou tabulku nemá. Krátké podpůrné okno Go tedy **není** slabina, za jakou by ho tabulka na první pohled vydávala — jde o jiný model, kde se povyšuje často, ale levně.

**Za druhé: TypeScript jako jediný nemá žádný závazek, a je to doloženo primárním zdrojem, ne prázdným hledáním.** ⚠️ **Toto tvrzení bylo 2026-08-23 opraveno jako nepravdivé — viz §8. Politika existuje, jen je podmíněná. Odstavec níže zůstává v původním znění, aby bylo vidět, co se opravovalo.** V issue microsoft/TypeScript #49088 („Document TypeScript version lifetime and EOL“, stav: uzavřeno) odpovídá Ryan Cavanaugh z týmu TypeScriptu: *"To my knowledge, we don't have an official policy beyond the one implied by the fact that we ship our components in Visual Studio. Security fixes are backported I believe for the last year of releases; non-security fixes are not backported."* [R18] Formulaci nechávám i s jejím zaváháním („I believe“) — zdroj si tím není jistý a dokument to nesmí ztvrdit.

Pozor ale na rozsah tohoto tvrzení: **týká se kompilátoru, ne běhového prostředí.** Kód v TypeScriptu běží na Node.js nebo v prohlížeči a životní cyklus má ten runtime — Node.js drží LTS **30 měsíců** [R19]. Tvrzení „TypeScript nemá LTS“ tedy neznamená „aplikace v TypeScriptu nemá podporovaný runtime“; znamená, že závazek nemá ten překladač, který pouštíš při buildu.

**Výsledek brány B2 (zapsáno 2026-08-22; ⚠️ 2026-08-23 se ukázalo, že vypálit neměla — §8).** Pravidlo zní: chybí identifikovatelný plátce **nebo** doložitelný závazek k dlouhodobé podpoře → vyřazen. Plátce má všech osm (§4.4). Závazek k podpoře má sedm z osmi — buď datovanou tabulkou (C#, Java, PHP, Python), nebo slibem kompatibility (Go, Kotlin, Rust). **Osmý, TypeScript, jej podle vlastního vyjádření týmu nemá, a brána B2 tak vypálila proti němu.**

Rozhodnutí, co s tím, **nepatří mně a nebude provedeno tiše**: B2 se ukázala jako nástroj, který u překladačů měří něco jiného než u běhových prostředí, a to je vada v návrhu pravidla, ne ve faktech pod ním. Pravidlo proto zůstává zapsané přesně tak, jak bylo, i s poznámkou, že vypálilo. Případná úprava bude zaznamenána jako **dodatečná, s datem a důvodem** — ne jako by tam byla od začátku.

### 4.6 Náborový rybník, předatelnost, zaškolení (ověřeno 2026-08-22)

Tahle osa má plnou váhu kvůli druhé roli ze §1 — doporučování ve firmách. Firma nepřebírá jazyk, přebírá jeho náborový rybník.

**Trvanlivá část** (konkrétní procenta jsou perishable a jsou v §5): rozdíly mezi těmi osmi nejsou po procentech, ale **řádové**. Ve třech pásmech: TypeScript a Python s nejširší základnou; C#, Java a PHP ve středu; Go, Rust a Kotlin nejúžeji, přičemž **Kotlin má nejmenší základnu z celé osmičky** [R61].

**A tady vzniká napětí, které musí verdikt vyřešit, ne zamlčet.** Tie-breaker 1 (přísnost, §4.1) rozhodl trojici na ceně 6 pořadím Kotlin › C# › Java. Tie-breaker 2 (nábor) ji řadí **přesně opačně** — C# a Java mají zhruba trojnásobnou základnu oproti Kotlinu. Pravidlo §2.3 má pořadí tie-breakerů pevně dané předem, takže **platí Kotlin**; ale pro firemní roli je to výsledek, který jde proti tomu, co by firma chtěla slyšet. Verdikt to musí uvést jako přiznaný důsledek pravidla, ne to schovat.

*Omezení zdroje: jde o dobrovolnou anketu jedné komunity, ne o měření trhu práce, a „používá jazyk“ není totéž co „je na něj k sehnání“. Pro ČR specificky data v tomto kole zjišťována nebyla.*

### 4.7 Zralost frameworků a knihoven (ověřeno 2026-08-22)

Podklady jsou už v §4.3, kde se zjišťovaly kvůli doménám. Shrnuto do jedné osy:

- **Nejzralejší a nejcelistvější:** C# (ASP.NET Core first-party, jeden kalendář s jazykem), Java a Kotlin (Spring Boot), PHP (Symfony a Laravel, obojí s vlastní datovanou politikou podpory), Python (Django).
- **Nejméně tříštivé:** Go — webová vrstva je ve standardní knihovně, takže „framework“ jako samostatná závislost s vlastním životním cyklem tu vůbec nevzniká [R8].
- **Nejtříštivější:** TypeScript. Vrstva frameworků je široká a bez společné politiky — Fastify má LTS zhruba na rok [R32], u Expressu se politiku nepodařilo najít [R33]. Ekosystém je největší z osmi a zároveň nejméně koordinovaný; pro sázku na dekádu je to obojí najednou.
- **Nejtenčí ve dvou ze čtyř domén:** Rust (u Axumu nenalezen datovaný kalendář [R34]) a PHP mimo web.

### 4.8 Souhrnná tabulka vlastností (důkazní materiál — nenese verdikt, ověřeno 2026-08-22)

Tabulka, na kterou se čtenář ptá jako první: konkrétní vlastnosti jazyk po jazyku. **Verdikt z ní neplyne** — ten vydává §3 podle pravidla §2.3. Tohle shrnuje, co zjistily §4.1 až §4.7, a slouží jako podklad pro tie-breakery. Kdyby ukazovala jinam než §3, platí §3 a rozpor se zapíše.

*Úprava proti záměru z kostry (2026-08-22): původně měla tabulka obsahovat jen vedoucí kandidáty, aby nebyla široká. Nakonec je tu všech osm — vyřadit PHP a Go z referenční tabulky by čtenáři vzalo právě to srovnání, kvůli kterému tuhle tabulku chtěl. Cenou je devět sloupců, které se na úzké obrazovce posouvají.*

Jazyky jsou tu **ve sloupcích** (v §3 v řádcích), pořadí abecední jako všude (§2.1).

| Vlastnost | C# | Go | Java | Kotlin | PHP | Python | Rust | TypeScript |
|---|---|---|---|---|---|---|---|---|
| **▸ Přísnost** | | | | | | | | |
| Typy vynucené za běhu | ✅ | ✅ | ✅ | ✅ | 🟡 po souborech | ❌ | ✅ | ❌ |
| Nullabilita v typovém systému | 🟡 jen při překladu | ❌ `nil` | ❌ | ✅ | 🟡 `?int` | 🟡 jen anotace | ✅ `Option<T>` | ✅ `strictNullChecks` |
| Generika skutečná za běhu | ✅ | ✅ od 1.18 | ❌ mazaná | ❌ mazaná | ❌ nemá vůbec | ❌ jen anotace | ✅ | ❌ mazaná |
| Hlavní únik z přísnosti | `!` a `default` struktury | `any`, aserce | mazání, raw typy | platform types z Javy | soubor bez direktivy | `Any` | `unwrap`, `unsafe` | `any` |
| **▸ Ergonomie** | | | | | | | | |
| Vlastnosti get/set jako jazykový rys | ✅ [R62] | — | — | ✅ [R63] | ✅ od 8.4 [R1] | ✅ `@property` [R64] | — | — |
| **▸ Provoz a ekosystém** | | | | | | | | |
| Model souběžnosti | `async`/`Task` *(nezj.)* | goroutiny | virtuální vlákna (JDK 21) | korutiny + JVM | jen kooperativní (Fibers 8.1) | GIL; build bez něj od 3.13, není výchozí | `async` + vlákna *(nezj.)* | smyčka událostí + workeři |
| Samostatná binárka bez runtime | 🟡 Native AOT | ✅ výchozí | 🟡 GraalVM | 🟡 GraalVM | 🟡 třetí strana | 🟡 PyInstaller | ✅ výchozí | 🟡 SEA / `deno compile` |
| Křížový překlad | 🟡 zdroj mlčí | ✅ | 🟡 nezj. | 🟡 nezj. | 🟡 částečně | ❌ | ✅ | ✅ přes Deno |
| Okno podpory jazyka | 36 měs. LTS | ~1 rok + slib kompatibility | ≥4 roky (Adoptium) | bez tabulky | 4 roky | 5 let | bez tabulky | žádné |
| Okno podpory frameworku | shodné s jazykem | žádný navíc | ≥12 měs. minor | ≥12 měs. minor | 2–4 roky dle volby | 3 roky | nenalezeno | ~1 rok / nenalezeno |
| Náborová základna (§5.1) | 29,9 % | 17,4 % | 29,6 % | 11,5 % | 19,1 % | 54,8 % | 14,5 % | 48,8 % |

**Ke třem sloupcům z původního zadání.** Tabulka, která tenhle dokument inspirovala, měla tři sloupce: *vyžaduje deklaraci proměnných*, *zakazuje globální proměnné* a *podporuje get/set properties*. Třetí je výše a je doložený. **První dva tu nejsou schválně** a je to důsledek pravidla, které si tahle tabulka sama uložila: patří sem jen vlastnost napojená na nějaké rozhodovací pravidlo nebo tie-breaker. Deklarace proměnných ani zákaz globálních proměnných na žádné pravidlo v §2 nenapojené nejsou — a otázka, kvůli které tam původně byly, tedy *„nakolik mi jazyk sám od sebe zabrání udělat chybu“*, má odpověď jinde a mnohem přesnější: v §4.1 bodě (a), kde se ukázalo, že rozhoduje **hranice vynucení**, ne přítomnost syntaktického pravidla.

**A ještě jedna oprava původní tabulky.** Řadila *get/set properties* mezi vlastnosti přísnosti, kde Java vycházela hůř. Jsou to ale dvě různé osy: vlastnosti jsou ergonomie, ne korektnost, a Java tím, že je nemá, není méně bezpečná — jak je vidět na řádku „Typy vynucené za běhu“, kde Java ✅ má a Python s TypeScriptem ne.

## 5. Datovaná vrstva (snapshot k 2026-08-22 — rychle zastarává)

**Nenese verdikt.** Až tahle sekce zastará, §1 až §4 platí dál.

### 5.1 Náborová základna (Stack Overflow Developer Survey 2025)

Podíl **profesionálních vývojářů**, kteří jazyk uvádějí mezi používanými [R61]. Pořadí je abecední jako ve všech tabulkách dokumentu (§2.1), ne podle podílu — nejvyšší má Python, následuje TypeScript:

| Jazyk | Podíl |
|---|---|
| **C#** | 29,9 % |
| **Go** | 17,4 % |
| **Java** | 29,6 % |
| **Kotlin** | 11,5 % |
| **PHP** | 19,1 % |
| **Python** | 54,8 % |
| **Rust** | 14,5 % |
| **TypeScript** | 48,8 % |

*(Pro kontext mimo osmičku: JavaScript 68,8 %.)* Anketa je z **ročníku 2025**, čtena v srpnu 2026 — novější ročník může existovat a nebyl ověřován. Jde o dobrovolnou anketu, ne o měření trhu práce.

### 5.2 Aktuální verze a termíny podpory

| Jazyk | Stav k 2026-08-22 | Zdroj |
|---|---|---|
| **C#** | .NET 10 (LTS) podporováno do 14. 11. 2028; .NET 8 i 9 do 10. 11. 2026 | [R9] |
| **Go** | Go 1.27.0 vydáno 19. 8. 2026; podpora vždy jen pro dvě nejnovější hlavní verze | [R6] |
| **Java** | Adoptium: JDK 25 nejméně do 9/2031, JDK 21 do 12/2029, JDK 17 do 10/2027 | [R11] |
| **Kotlin** | Bez datované tabulky podpory; na JVM nejméně tři předchozí jazykové a API verze | [R14] |
| **PHP** | 8.5 bezpečnostně do 31. 12. 2029; 8.4 do 31. 12. 2028; 8.2 končí 31. 12. 2026 | [R2] |
| **Python** | Pětileté okno na vydání; volnovláknový build od 3.13, není výchozí | [R4][R56] |
| **Rust** | Bez datované tabulky podpory; edice opt-in a vzájemně interoperabilní | [R16] |
| **TypeScript** | Bez oficiální politiky podpory; runtime Node.js drží LTS 30 měsíců | [R18][R19] |

### 5.3 Frameworky

| Framework | Okno podpory | Zdroj |
|---|---|---|
| Symfony (LTS) | 3 roky oprav + 4 roky bezpečnosti | [R28] |
| Django | 3 roky; od vydání 2028 na každé feature vydání | [R30] |
| ASP.NET Core | shodné s .NET, LTS 36 měsíců | [R9] |
| Laravel | 18 měsíců oprav + 2 roky bezpečnosti | [R29] |
| Spring Boot | minor nejméně 12 měsíců, major nejméně 3 roky | [R31] |
| Fastify | ~12 měsíců (6 + 6 po dalším major) | [R32] |

## 6. Adversariální průchod a verdikt

### 6.1 Adversariální průchod (M5, 2026-08-23)

Zadání pro tenhle průchod znělo **vyvrátit**, ne potvrdit. Šel na čtyři buňky označené jako nejisté a na samotný závěr.

**Omezení, které je nutné přiznat:** průchod proběhl **ve stejném kontextu, který závěr vytvořil**, ne v odděleném. Kodex doporučuje čerstvý kontext právě proto, že autor své vlastní argumenty vyvrací hůř než cizí člověk. Váha tohoto průchodu je tím menší a čtenář to má vědět.

| Buňka | Výsledek | Co se stalo |
|---|---|---|
| **Rust v backendu** (🟡) | **Obstála, a je líp podložená** | Námitka byla nerovné měřítko: u TypeScriptu jsem hledal politiku podpory u dvou frameworků, u Rustu jen u jednoho. Doplněno stejnou metodou — Actix-web nemá datovaný kalendář podpory v kořeni ani v `.github`, pozitivní kontrola prošla (`Cargo.toml` ve výpisu) [R65]. Dva ze dvou tedy nezveřejňují nic, kdežto u TypeScriptu jeden ze dvou ano (Fastify). Rozdíl je reálný, 🟡 platí. |
| **Go v prohlížeči** (❌) | **Obstála s výhradou** | Čísla jsou z vlastní wiki Go, to nejde zpochybnit. Ale tatáž wiki doporučuje kompresi a zmiňuje TinyGo s ~10 kB, a **ani jedno jsem nezkoumal**. ❌ tedy stojí na nekomprimovaném dnu a na neprozkoumané únikové cestě. Kdyby padlo na 🟡, Go jde z 9 na 7. |
| **PHP v prohlížeči** (❌) | **NEOBSTÁLA — sníženo na 🟡** | Argument zněl „tenké, fakticky jeden udržovatel“. To je **soud, ne měření**, a doložit se nepodařilo. `php-wasm` přitom existuje, je aktivní a pokrývá PHP 8.0–8.5 [R42]. Podle pravidla, že inference nesmí nosit kostým faktu, se ❌ ruší. **Dopad: PHP z 12 na 8, tím přeskočilo Go a poslední je nově Go.** |
| **Rust v prohlížeči** (🟡) | **Evidence hodnotu nedokládá** | Jediný doklad byl nemaintainovaný web pracovní skupiny, což nevypovídá o cílové platformě ani o frameworcích. Buňka zůstává 🟡 jako nejméně zavazující hodnota, ale **není doložená** a dokument to říká místo aby to zakryl. |

**A teď nejsilnější námitka, kterou mám — míří na vítěze a nejde ji odbýt.**

Vážená cena měří **výhradně padnutí do čtyř domén.** Trvanlivá vrstva §4.4 až §4.7 do skóre nevstupuje vůbec; dostane se ke slovu jen přes tie-breakery, a ty se spouštějí pouze při shodě. Z toho plyne nepříjemný důsledek: **největší slabina TypeScriptu — že pro překladač neexistuje žádný závazek podpory, tedy přesně to, na čem v kole 1 vypálila brána B2 — je ve skóre strukturálně neviditelná.**

Není to porušení pravidla. Pravidla byla takhle napsaná předem a po výsledku se nepřepisují. Ale znamená to, že **číslo 4 není celá pravda**, a verdikt to musí říct nahlas, ne to schovat do poznámky.

Druhá námitka téhož druhu: vedoucí dvojice, TypeScript a Python, jsou **oba ve skupině, která typy za běhu nevynucuje** (§4.1 bod a). Zvolené váhy vybírají šířku záběru, a šířka v roce 2026 znamená právě tyhle dva jazyky.

### 6.2 Verdikt (2026-08-23)

**Podle pravidla §2.3 vychází verdikt na TypeScript** s váženou cenou 4, před Pythonem s 5.

**Co za to platíš — přijaté kompromisy, vyjmenované, ne naznačené:**

1. **Žádný závazek podpory pro překladač.** Tým TypeScriptu sám uvádí, že oficiální politika neexistuje (§4.5). Životní cyklus, o který se opíráš, je životní cyklus **runtime** — Node.js s LTS 30 měsíců. Tohle je ten kompromis, kvůli kterému bys jinak neprošel bránou B2, a přijímáš ho vědomě.
2. **Typy se za běhu nevynucují.** Mažou se při překladu a výstupem je prostý JavaScript (§4.1). Ochrana končí na hranici, kde data vstupují zvenčí; validace na té hranici je tvoje práce, ne práce jazyka. Pro někoho, kdo celý dokument navrhl kolem otázky přísnosti, je to ta nejdražší položka na seznamu.
3. **Nejtříštivější vrstva frameworků z osmi** (§4.7). Největší ekosystém a zároveň nejméně koordinovaný — Fastify má okno zhruba rok, u Expressu se politiku nepodařilo najít.
4. **CLI se platí volbou** (§4.3): buď experimentální Node SEA, nebo `deno compile`, tedy jiný runtime než Node. Při váze 3 je to druhá nejdražší položka verdiktu.

**Co za to dostáváš:** jediný kandidát, který pokrývá prohlížeč bez daně (§4.3), druhá nejširší náborová základna (§5.1) a nulová cena v nejvýš vážené doméně.

**Runner-up: Python (5).** Vyhrává data, kde má TypeScript 🟡, a prohrává prohlížeč. Trpí toutéž slabinou v bodě 2 — runtime typy nevynucuje — a k tomu GIL, jehož odstranění je vydané, ale ekosystém ho nedohnal (§4.2).

**Změním názor, když** — a tohle je falzifikace, ne alibi:

- **Vynucení typů za běhu má pro tebe větší cenu než šířka záběru.** Pak nejsou špatně čísla, ale váhy: vybíraly šířku, a ta v roce 2026 vede na dva jazyky, které typy za běhu nekontrolují. S jinými vahami vychází Kotlin, C# nebo Rust. Váhy jsi zadal před rešerší a přepisovat je teď by zničilo jedinou vlastnost, kvůli které se píšou dopředu — ale rozhodnout se je změnit a **spustit výpočet znovu s datem** je legitimní, pokud se to zapíše jako nové zadání, ne jako oprava.
- **Doména prohlížeče z tvého zadání vypadne.** Nula TypeScriptu je jen tam; bez frontendu klesá na 3, ale Go padá z 9 na 3 a Rust ze 7 na 5 — pořadí se přeskládá celé.
- **❌ u Go v prohlížeči padne** (§6.1). Samo o sobě verdikt nezmění, ale zúží odstup.

### 6.3 Verdikt po doménách a citlivost na váhy (2026-08-23)

Jeden verdikt odpovídá na jednu otázku — „co když mám jiné zadání než tvoje?“ je otázka jiná a zaslouží si vlastní odpověď. Obojí níže je **čtení matice ze §3**, ne nová tvrzení: nepřibyl ani jeden zdroj.

#### Po doménách — pásma, ne pořadí

**Proč pásma a ne první, druhá a třetí volba.** Matice má tři hodnoty, ne žebříček. V backendu je sedm z osmi kandidátů na ✅, což **není** první až sedmá volba, ale sedmičlenná shoda. Seřadit je by znamenalo vymyslet si rozdíly, které dokument neměřil — a to je přesně ten žebříček bez poraženého, kterému se §3 vyhýbá.

| Doména | Platí nulu | Platí | Platí nejvíc |
|---|---|---|---|
| **Backend a API** (×4) | C#, Go, Java, Kotlin, PHP, Python, TypeScript | Rust | — |
| **CLI a automatizace** (×3) | Go, Rust | C#, Java, Kotlin, PHP, Python, TypeScript | — |
| **Frontend v prohlížeči** (×2) | TypeScript | C#, Java, Kotlin, PHP, Python, Rust | Go |
| **Data, ML, dávky** (×1) | Python | C#, Java, Kotlin, Rust, TypeScript | Go, PHP |

Čte se to takhle: **kdyby ses rozhodoval jen podle jedné domény**, v backendu bys volil skoro cokoli, v CLI Go nebo Rust, v prohlížeči TypeScript a v datech Python. Verdikt v §6.2 je odpověď na otázku, co dělat, když musíš mít **jeden jazyk na všechny čtyři najednou** — a to je jiná otázka než kterýkoli řádek téhle tabulky.

#### Citlivost na váhy — několik verdiktů, každý s vlastním zadáním

Tytéž buňky, jiné váhy. Sloupec vah je v pořadí backend · CLI · frontend · data.

| Zadání | Váhy | Vítěz | Pořadí |
|---|---|---|---|
| **Tvoje zadání (§2.3)** | 4 · 3 · 2 · 1 | **TypeScript** (4) | TS 4, Python 5, C# 6, Java 6, Kotlin 6, Rust 7, PHP 8, Go 9 |
| Všechny domény stejně | 1 · 1 · 1 · 1 | **Python + TypeScript** (2) | Python 2, TS 2, C# 3, Java 3, Kotlin 3, Rust 3, PHP 5, Go 6 |
| Bez prohlížeče | 4 · 3 · 0 · 1 | **Go + Python** (3) | Go 3, Python 3, C# 4, Java 4, Kotlin 4, TS 4, Rust 5, PHP 6 |
| Bez dat a ML | 4 · 3 · 2 · 0 | **TypeScript** (3) | TS 3, C# 5, Java 5, Kotlin 5, PHP 5, Python 5, Go 6, Rust 6 |
| Jen backend | 1 · 0 · 0 · 0 | **sedmičlenná shoda** (0) | vše kromě Rustu 0, Rust 1 |
| Prohlížeč nejvýš | 2 · 3 · 4 · 1 | **TypeScript** (4) | TS 4, Python 7, Rust 7, C# 8, Java 8, Kotlin 8, PHP 10, Go 15 |
| Data nejvýš | 2 · 1 · 3 · 4 | **Python** (4) | Python 4, TS 5, C# 8, Java 8, Kotlin 8, Rust 9, PHP 16, Go 21 |

#### Co z toho plyne

**Vítězství TypeScriptu je robustní vůči všemu kromě jedné změny.** Vyhrává ve třech ze sedmi zadání, v jednom dalším dělí první místo a nikdy neklesne pod druhé — s jedinou výjimkou: **jakmile z požadavků vypadne prohlížeč, klesá na čtvrté místo a vede Go s Pythonem.** To je celý jeho nárok a zároveň jeho jediná zranitelnost. Kdo prohlížeč nepotřebuje, má úplně jiný verdikt.

**Nejméně stabilní kandidát celého dokumentu je Go.** Kolísá mezi posledním místem (9 při zadaných vahách, 15 a 21 při dvou dalších) a **děleným prvním** (3 bez prohlížeče). Žádný jiný kandidát se nehýbe takhle. Znamená to, že tvrzení „Go je pro tenhle profil špatná volba“ platí **výhradně kvůli prohlížeči a datům** — v obou nejvýš vážených doménách je totiž na nule.

**Řádek „jen backend“ je důkaz nálezu z kola 3.** Sedmičlenná shoda na nule ukazuje černé na bílém, že nejvýš vážená doména o pořadí nerozhoduje: rozptyl uvnitř sloupce dělá vliv, ne váha sloupce.

**Python je nejodolnější kandidát.** Vyhrává nebo dělí první místo ve třech zadáních a nikdy neklesne pod páté. Kdo neví, jaké budou jeho váhy za pět let, kupuje Pythonem nejméně rizika — což je argument, který se ve verdiktu podle zadaných vah neobjeví, protože ten měří jedno konkrétní zadání, ne odolnost napříč zadáními.

**Vymezení platnosti.** Verdikt platí pro profil ze §1: **nové projekty na zelené louce**, čtyři domény s vahami 4 · 3 · 2 · 1, výkon jako měkká osa. Neplatí pro migraci existujícího systému a neplatí pro jiné váhy. A stojí na jednom rozhodnutí zadavatele z 2026-08-22 — úpravě brány B2 (§2.2) — bez něhož by byl vítěz vyřazen dřív, než se cokoli spočítalo.

## 7. Druhé zadání: profesionalita jazyka (pravidla sepsána 2026-08-23 — PŘED rešerší)

### 7.1 Proč je tu druhé zadání

Zadavatel po dodání verdiktu §6.2 upřesnil, že **největší váhu pro něj má profesionalita jazyka, konkrétně jeho syntaxe** — tedy zda v něm lze přehledně programovat malé i velmi rozsáhlé projekty — a že je to otázka v podstatě nezávislá na doméně.

**Je to oprávněná námitka a dokument se odchýlil.** V prvním zadání stálo *„malé i velké projekty… čitelnost kódu, bezchybnost v kódu“* a v původním návrhu z 8. 8. 2026 *„jak moc jsou profesionální moderní programovací jazyky“*. Tahle osa byla hlavní od začátku; §2.3 ji odsunula na **tie-breaker**, tedy na kritérium, které se spouští jen při shodě. Stalo se to proto, že z domén šel udělat mechanický verdikt — vyhrála měřitelnost nad relevancí.

**Neopravuje se to přepsáním.** §6.2 na tenhle případ pamatuje předem: změna zadání se zapisuje jako **nové zadání s datem**, ne jako oprava starého, protože pravidlo upravené po zhlédnutí výsledku ztrácí to jediné, kvůli čemu se píše dopředu. **Verdikt §6.2 tedy platí dál jako odpověď na první zadání** a tohle je odpověď na druhé. Dokument ponese oba a případný rozpor mezi nimi zapíše.

### 7.2 Rozhodovací pravidla druhého zadání

**Kandidáti:** týchž osm, v témže abecedním pořadí (§2.1). **Metodická pravidla M1 až M5 (§2.4) platí beze změny** — včetně povinného adversariálního průchodu a zákazu, aby inference nosila kostým faktu.

**Kritéria.** Zadavatel 2026-08-23 vybral **všechna čtyři** z nabídnutých čtení, bez určení pořadí:

| # | Kritérium | Co se měří (checkovatelně, ne dojmem) |
|---|---|---|
| **P1** | Kompilátor chytí chybu dřív než uživatel | Hranice vynucení (§4.1 bod a), nullabilita v typovém systému, vyčerpávající větvení |
| **P2** | Kód přečte cizí člověk bez kontextu | Existence **oficiálního** formátovače, velikost a jednoduchost jazyka, možnost měnit chování za běhu |
| **P3** | Velký refaktoring je bezpečný | Statické typy plus existence **oficiálního** jazykového serveru; zda překladač najde všechna volání |
| **P4** | Typový systém unese doménový model | Součtové typy s daty, vyčerpávající větvení nad nimi, neměnnost |

**Váhy: všechna čtyři kritéria stejně (1 · 1 · 1 · 1).** Zadavatel je vybral bez určení pořadí, takže rovnoměrné váhy jsou nejmenší domýšlení. **Je to ale volba, ne fakt** — a poučen §6.3 se k ní rovnou zavazuji doplnit citlivostní přehled, aby o výsledku nerozhodla tiše.

**Cena a agregace** jsou totožné se §2.3, aby byla čísla srovnatelná: ✅ = 0 · 🟡 = 1 · ❌ = 3, součet přes čtyři kritéria, **vyhrává nejnižší** (rozsah 0 až 12).

**Vymezení.** Tohle zadání **nemá domény ani jejich váhy** — je z podstaty nezávislé na doméně. Neruší §6.2 a nemá na něj vliv.

### 7.3 Předpověď zapsaná před rešerší

Poučen tím, že předpověď v §2.3 selhala kvůli uvažování o silných stránkách místo o rozptylu, uvažuji tentokrát o rozptylu uvnitř kritérií. **Jde o inferenci, ne o fakta.**

- **Největší rozptyl čekám u P4**, kde jsou součtové typy buď v jazyce, nebo v něm nejsou vůbec. To by mělo rozhodnout pořadí víc než ostatní tři.
- **Go je kandidát s nejprotichůdnějším profilem:** velmi silné P2 (záměrně malý jazyk, oficiální `gofmt`) a P3, ale P4 by mu mělo chybět. Jeho umístění tedy závisí na tom, zda P2 vyváží P4 — a to je při rovných vahách otevřené.
- **Kotlin a Rust čekám vpředu**, protože jako jediné by měly být slušné ve všech čtyřech.
- **Vítěz prvního zadání, TypeScript, tady podle mě nevyhraje**, protože P1 ho sráží (§4.1: typy se za běhu nevynucují). Očekávám tedy, že dokument skončí **se dvěma verdikty, které si odporují** — a ten rozpor bude užitečnější než kterýkoli z nich zvlášť.

Pokud rešerše tuhle předpověď vyvrátí, zapíše se to jako výsledek, ne jako oprava předpovědi.

### 7.4 Tabulka profesionality (ověřeno 2026-08-23)

Ceny: ✅ = 0 · 🟡 = 1 · ❌ = 3, součet přes čtyři kritéria, vyhrává nejnižší (§7.2).

| Jazyk | P1: kompilátor chytí chybu | P2: čitelnost pro lidi | P3: velký refaktoring bezpečný | P4: typy unesou doménový model | Součet |
|---|---|---|---|---|---|
| **C#** | 🟡 typy vynucuje běh, ale nullabilita jen překlad a `!` [R50] | ✅ `dotnet format` pod organizací `dotnet` [R75] | ✅ statické typy, Roslyn od Microsoftu [R75] | 🟡 součtové typy jsou zatím **návrh** `standard-unions.md` v `dotnet/csharplang` [R76] | **2** |
| **Go** | 🟡 typy vynucuje běh, ale `nil` je nulová hodnota všeho referenčního [R54] | ✅ `gofmt` je součástí distribuce, *"uncontroversial"*, a FAQ dokládá záměrné vynechávání rysů [R73][R74] | ✅ statické typy, `gopls` pod organizací `golang` [R75] | ❌ FAQ: *"We considered adding variant types to Go, but after discussion decided to leave them out"* [R73] | **4** |
| **Java** | 🟡 typy vynucuje běh, ale generika se mažou a nullabilita v jazyce chybí [R55] | ❌ oficiální formátovač neexistuje; `google-java-format` je Googlu [R75] | 🟡 statické typy, ale jazykový server je Eclipse, ne správce jazyka [R75] | ✅ sealed rozhraní (JDK 17) + vyčerpávající `switch` bez `default` (JDK 21) [R68][R69] | **5** |
| **Kotlin** | ✅ nullabilita v typovém systému, vynucená kompilátorem; díra jsou platform types z Javy [R52] | ✅ `ktfmt` pod organizací `Kotlin` [R75] | ✅ statické typy, `kotlin-lsp` pod organizací `Kotlin` [R75] | ✅ sealed třídy, *"you don't need to add an `else` clause"* [R67] | **0** |
| **PHP** | ❌ přísnost je direktiva po souborech, generika nemá [R49] | ❌ oficiální formátovač neexistuje; PHP-CS-Fixer je vlastní organizace [R75] | ❌ oficiální jazykový server nenalezen [R75] | ❌ enumy od 8.1 jsou *"backed by types of `int` or `string`"* — data nesou jen skalár [R70] | **12** |
| **Python** | ❌ *"The Python runtime does not enforce… type annotations"* [R47] | ✅ `black` pod organizací `psf` [R75] | 🟡 dynamický; `mypy` a `typeshed` jsou pod organizací `python` [R75][R80] *(upřesněno v §9.1 — původní znění uvádělo `pyright`, což Pythonu křivdilo)* | 🟡 `match` a `assert_never` fungují, ale **jen ve statické kontrole** [R77] | **5** |
| **Rust** | ✅ null neexistuje, `Option<T>`, *"Matches in Rust are exhaustive"* [R53][R72] | ✅ `rustfmt` pod organizací `rust-lang` [R75] | ✅ statické typy, `rust-analyzer` pod organizací `rust-lang` [R75] | ✅ enumy s daty + vyčerpávající `match` vynucený kompilátorem [R72] | **0** |
| **TypeScript** | ❌ typy se mažou, výstupem je prostý JavaScript [R39] | ❌ oficiální formátovač neexistuje; Prettier je samostatná organizace [R75] | ✅ statické typy a nástroje od Microsoftu [R75] | ✅ diskriminované unie + kontrola vyčerpání přes `never` [R71] | **6** |

**Co P2 měří a co ne.** Hodnotil jsem **jen vlastnictví formátovače** — tedy zda existuje pod organizací samotného jazyka, což je zjistitelné. Druhá polovina otázky, *kolik magie musíš držet v hlavě*, se mi nepodařilo převést na checkovatelné kritérium a **měřená není**. Buňka Go je jediná, kde je navíc doložená i záměrná jednoduchost, protože ji tvrdí vlastní FAQ jazyka.

**Vyhodnocení předpovědi ze §7.3 — tentokrát vyšla.** Předpověděl jsem Kotlin a Rust vpředu (**sedí, oba na nule**), že TypeScript nevyhraje (**sedí, sedmý**), největší rozptyl u P4 (**sedí** — hodnoty 0, 0, 0, 1, 1, 3, 3, 3) a že Go má nejprotichůdnější profil, kde P2 bojuje s P4 (**sedí** — ✅ ✅ v P2 a P3 proti ❌ v P4, výsledkem střed tabulky). Rozdíl proti selhavší předpovědi ze §2.3 je v tom, že tahle uvažovala o **rozptylu uvnitř kritérií**, ne o silných stránkách kandidátů.

**Citlivost na váhy, jak jsem se v §7.2 zavázal.** Zdvojnásobení kteréhokoli jednoho ze čtyř kritérií vede **pokaždé k témuž vítězi**: Kotlin a Rust na nule. Mění se jen pořadí za nimi — třeba při dvojnásobné váze P4 padá Go až na sedmé místo, při dvojnásobné P2 je čtvrté. **Výsledek druhého zadání je tedy na vahách prakticky nezávislý**, což se o prvním zadání říct nedalo.

### 7.5 Verdikt druhého zadání (2026-08-23)

**Vyhrávají Kotlin a Rust, oba s nulou — a je to plná shoda, ne těsný náskok.** Jediné dva jazyky z osmi, které jsou ✅ ve všech čtyřech kritériích.

**Pravidlo §7.2 tuhle shodu nerozhoduje.** Tie-breaker jsem pro druhé zadání nenapsal, což je mezera v mých vlastních pravidlech — a **doplnit ho teď, po zhlédnutí výsledku, je přesně to, co dokument celou dobu odmítá dělat.** Verdikt tedy zní: **dělené první místo**, a rozhodnutí mezi nimi patří zadavateli. Materiál k němu už v dokumentu je a shrnuji ho bez toho, abych z něj dělal pravidlo:

- **Kotlin** má za sebou celý ekosystém JVM a Spring Boot (§4.3), ale **nejmenší náborovou základnu z osmi** — 11,5 % proti 14,5 % Rustu (§5.1) — datovanou tabulku podpory nemá (§4.5) a jeho jediná díra v přísnosti se otevírá právě při volání Javy, tedy toho ekosystému, kvůli kterému si ho vybíráš (§4.1).
- **Rust** má nejsilnější záruky z celé osmičky a jako jediný nemá null vůbec (§4.1), ale v prvním zadání je jediný, kdo není ✅ v backendu — nejvýš vážené doméně (§3) — a datovanou tabulku podpory nemá také.

**Rozpor mezi oběma verdikty je největší výstup celého dokumentu.** Není to chyba ani jednoho z nich; obě zadání jsou legitimní a každé měří něco jiného.

| Jazyk | Pořadí: domény (§6.2) | Pořadí: profesionalita (§7.5) | Posun |
|---|---|---|---|
| **C#** | 3. | 3. | 0 |
| **Go** | 8. | 4. | +4 |
| **Java** | 4. | 5. | −1 |
| **Kotlin** | 5. | 1. | +4 |
| **PHP** | 7. | 8. | −1 |
| **Python** | 2. | 6. | −4 |
| **Rust** | 6. | 2. | +4 |
| **TypeScript** | 1. | 7. | **−6** |

**Vítěz prvního zadání je v druhém sedmý.** Vítězové druhého jsou v prvním pátý a šestý. Znamená to jedinou, ale zásadní věc: **žádný jazyk není zároveň nejlepším pokrytím tvých čtyř domén a nejprofesionálnějším nástrojem.** Ten obchod je skutečný obsah tohohle dokumentu, ne kterýkoli z obou verdiktů zvlášť.

**Pozorování, výslovně ne třetí verdikt.** Sečtu-li obě pořadí, vyjde nejlíp C# a Kotlin (shodně 6), pak Rust, Python a TypeScript (8). **C# je přitom jediný kandidát, který je v první trojici obou zadání.** Zdůrazňuji, že tohle **není verdikt**: součet pořadí je agregace, kterou jsem vymyslel **až po zhlédnutí výsledků**, a jako taková nemá váhu pravidla sepsaného předem. Kdybys chtěl skutečný kombinovaný verdikt, musí dostat vlastní pravidlo, sepsané a datované dřív, než se spustí — a to je práce na další kolo, ne na tohle.

**Vymezení platnosti.** Verdikt §7.5 platí pro čtyři kritéria ze §7.2 s rovnými vahami, pro těchže osm kandidátů. Neruší §6.2 a nemá na něj vliv. P2 je měřena neúplně (jen vlastnictví formátovače) a §8 se týká §4.5, ne tohoto zadání.

## 8. Oprava (2026-08-23): brána B2 neměla vypálit

**Co bylo špatně.** §4.5 tvrdila, že TypeScript jako jediný z osmi nemá doložitelný závazek podpory, a brána B2 na tom 2026-08-22 vypálila proti němu. **Tvrzení je nepravdivé.** V kořeni repozitáře `microsoft/TypeScript` je soubor `SUPPORT.md` se sekcí *"Microsoft Support Policy"*, která říká: *"When included with a Microsoft product, TypeScript support and servicing is offered under the [Modern Support Policy]. For Visual Studio, servicing fixes are limited to security fixes for versions of TypeScript included in under-support releases of Visual Studio."* [R66]

**Jak k tomu došlo — a je to poučnější než sama chyba.** Hledal jsem na dvou místech: na wiki stránce o vydávání [R17] a v issue #49088 z roku 2022 [R18]. Obě mlčela, a já z toho udělal závěr o nepřítomnosti. **Nezkontroloval jsem `SUPPORT.md` v kořeni repozitáře — tedy standardní místo přesně pro tenhle údaj.** U Expressu a Axumu jsem přitom kořen repozitáře prohlížel a dokonce jsem u nich hlídal pozitivní kontrolu; u TypeScriptu jsem to neudělal, protože jsem měl citát od člena týmu a považoval jsem otázku za uzavřenou. **Silně znějící zdroj mě odradil od dalšího hledání** — a to je přesně ta past, kterou pravidlo „prázdný výsledek hledání není zdroj“ popisuje. Citát navíc nebyl v rozporu s nálezem: Ryan Cavanaugh v roce 2022 řekl, že politika neexistuje *"beyond the one implied by the fact that we ship our components in Visual Studio"* — a `SUPPORT.md` je právě tahle implikovaná politika, sepsaná.

**Co platí místo toho.** TypeScript **má** doloženou politiku podpory, ale je **podmíněná**: váže se na dodání v produktu Microsoftu, u Visual Studia se omezuje na bezpečnostní opravy verzí zahrnutých v podporovaných vydáních VS, a **samostatně distribuovanému balíčku z npm nedává kalendář verzí** — nic jako datovanou tabulku EOL, jakou mají PHP, Python nebo .NET. Rozdíl proti ostatním sedmi tedy existuje, ale je to rozdíl *„podmíněná politika bez kalendáře verzí“* proti *„žádná politika“*, a to je jiné tvrzení.

**Důsledek pro rozhodovací pravidlo.** Pravidlo B2 zůstává v §2.2 zapsané přesně tak, jak bylo, a **nepřepisuje se**. Ale je nutné nahlas říct: **B2 vypálila na základě chybného faktu a při správném faktu by nejspíš nevypálila vůbec.** Úprava B2, kterou zadavatel schválil 2026-08-22, tedy byla provedena na falešném předpokladu. Byla by zbytečná, ne škodlivá — vede k témuž výsledku (TypeScript prochází), jen po správné cestě. Zadavateli patří poznámka, že rozhodoval na základě mého chybného zjištění.

**Důsledek pro verdikt (§6.2).** Verdikt se nemění — vážená cena governance nezahrnuje (§6.1). Mění se ale dvě formulace kolem něj:

1. **Kompromis č. 1 v §6.2 byl přehnaný.** Neplatí „žádný závazek podpory pro překladač“; platí „podmíněná politika bez kalendáře verzí, plus životní cyklus runtime Node.js“. Ta položka účtu je **levnější**, než jak byla vyfakturovaná.
2. **Námitka z §6.1 o strukturálně neviditelné slabině se tím oslabuje**, ne ruší. Argument, že vážená cena měří jen padnutí do domén a trvanlivá vrstva do ní nevstupuje, platí dál. Jen ta konkrétní slabina, kterou jsem jako příklad použil, je menší, než jsem tvrdil.

**Co si z toho odnést do dalších kol.** Než prohlásím něco za neexistující, prohlédnu **standardní místa** pro ten typ údaje — u repozitáře kořen, `.github`, `SUPPORT.md`, `SECURITY.md` — a udělám to i tehdy, když už mám zdroj, který zní přesvědčivě. Ověřený citát o nepřítomnosti je pořád jen tvrzení o tom, co jeho autor v tu chvíli věděl.

## 9. Dodatek (2026-08-26): proč PHP tolik zaostává za Pythonem, a co v tom nesedí

Zadavatel se zeptal, proč PHP dostalo v §7.4 skóre 12 a Python 5. Otázka si vynutila přeověření a to přineslo tři věci: doplnění mezery, kterou §4.1 sama přiznávala, potvrzení dvou tvrzení, která byla v době zápisu **pod-doložená**, a jednu přiznanou hrubost měřidla.

### 9.1 Kde rozdíl je a kde není

**P1 je u obou totožné — obě ❌.** Rozdíl mezi PHP a Pythonem tedy **není** v tom, že by jeden vynucoval typy za běhu a druhý ne. PHP je vynucuje po souborech a nemá generika, Python je nevynucuje vůbec; obojí padá na stejnou hodnotu. Kdo hledá důvod rozdílu tady, hledá ho na špatném místě.

**P4 je rozdíl skutečný a doložený.** PHP enumy nesou jen skalár — *"may be backed by types of `int` or `string`"* [R70] — a generika jazyk nemá vůbec [R49]. Python má unie, generika v anotacích, `match` i `assert_never` [R77]. Že to všechno platí jen při kontrole, sráží Python na 🟡; PHP ale ty konstrukce nemá **ani při kontrole**. Rozdíl 🟡 proti ❌ tu drží.

**P3: původní zdůvodnění bylo neúplné a nová evidence hraje pro Python.** Napsal jsem, že *„`pyright` je Microsoftu, ne PSF“* — což Pythonu křivdilo. **`mypy` i `typeshed` jsou pod organizací `python`**, tedy pod samotným správcem jazyka (pozitivní kontrola: pod toutéž organizací jsou `peps`, `typing` i `pythondotorg`) [R80]. Python tedy **first-party typovou kontrolu má**. U PHP jsem naopak tvrdil „oficiální jazykový server nenalezen“, aniž bych po něm skutečně hledal — to bylo tvrzení o neexistenci bez hledání, tedy horší než prázdný výsledek. **Doplněno:** pod organizací `php` není ani jazykový server, ani formátovač; jsou tam `php-src` a webové vlastnosti projektu (pozitivní kontrola: `php-src` přítomen) [R78]. Buňky se nemění, ale teď stojí na tom, na čem stát měly.

### 9.2 Co PHP v žádné buňce nedostalo, a mělo by to zaznít

§4.1 přiznávala, že úrovně PHPStan a Psalm zjišťovány nebyly. Doplněno: **PHPStan má jedenáct úrovní (0 až 10)**, úroveň 6 *„report missing typehints“*, úroveň 9 je striktní na explicitní `mixed` a úroveň 10 *„reports errors even for implicit mixed (missing type), not just explicit mixed“* [R79].

To je ambicióznější, než jak PHP v tabulce vypadá — a **do žádné buňky §7.4 se to nepromítlo**, protože kritéria měřila jazyk a jeho oficiální nástroje, ne sílu komunitní statické analýzy. Je to reálná přednost PHP, kterou tenhle dokument nezachytil, a čtenář by o ní měl vědět.

### 9.3 Přiznaná hrubost kritéria P2

P2 se u obou jazyků rozhoduje na jediné věci: **pod čí organizací žije formátovač.** `black` je pod `psf`, tedy pod nadací jazyka → ✅. `PHP-CS-Fixer` je pod vlastní organizací, ne pod `php` → ❌. **Rozdíl mezi nimi je tři body z dvanácti, tedy čtvrtina celého skóre**, a přitom ani jeden z těch formátovačů se s jazykem nedodává a v praxi se oba pouštějí stejně — jako krok v CI.

**Kritérium tedy měří vlastnictví, ne zážitek uživatele, a u dvojice PHP–Python je to nejslabší místo celého §7.4.** Hodnotu buňky nepřepisuji: pravidlo bylo sepsáno před rešerší (§7.2) a měnit ho po zhlédnutí výsledku je přesně to, co dokument odmítá. Zapisuji ale, že **zhruba třetina rozdílu 12 : 5 stojí na formalistickém testu**, a kdo si ho necení, má škálovat rozdíl podle toho.

### 9.4 Shrnutí

Rozdíl 12 : 5 **drží**, ale rozpadá se nerovnoměrně: P1 nepřispívá ničím, P4 je plně doložený, P3 je doložený až po tomhle dodatku a P2 stojí na měřidle, které si samo přiznává hrubost. **Pořadí se nemění** — PHP zůstává osmé i při nejpříznivějším čtení, protože sedmý TypeScript má 6.

## 10. Dodatek (2026-08-26): jaké verze byly doopravdy analyzovány

Zadavatel se zeptal, zda bylo PHP hodnoceno v nejnovější verzi, a navrhl doplnit k jazykům konkrétní analyzované verze, aby bylo i za rok jasné, co se posuzovalo. Obojí míří na pravidlo **M1** (§2.4) — a obojí odhalilo, že jsem ho uplatňoval nerovnoměrně.

### 10.1 Kontrola PHP 8.5

**Verzi jsem znal, poznámky k vydání jsem nečetl.** PHP 8.5 je v §4.5 i §5.2 s termíny podpory, ale co konkrétně přineslo, jsem nikdy neověřil — hodnotil jsem z vlastností, které znám. Doplněno [R82]: PHP 8.5 přidalo pipe operátor `|>`, `clone` s přepisem readonly vlastností, atribut `#[\NoDiscard]`, atributy na konstantách, `final` u promovaných vlastností, asymetrickou viditelnost u statických vlastností a `#[\Override]` na vlastnostech.

**Žádná buňka se nehýbe.** Generika 8.5 nepřineslo, enumy zůstávají skalární (§7.4, [R70]) a pattern matching nad součtovými typy nemá. P1 i P4 tedy zůstávají ❌ ze stejných důvodů jako předtím a součet 12 platí.

**Jednu věc to ale ukázalo v můj neprospěch.** Kritérium P4 mělo podle §7.2 měřit „součtové typy s daty, vyčerpávající větvení nad nimi, **neměnnost**“ — a tu třetí složku jsem fakticky nehodnotil u nikoho. PHP má přitom `readonly` (8.1), asymetrickou viditelnost (8.4) a nově `clone with` i `final` u promovaných vlastností (8.5), což je slušný příběh neměnnosti. Buňku to nezvedá, protože chybějící součtové typy v P4 dominují, ale **P4 je změřena neúplně u všech osmi** a dokument to má říct stejně jako u P2 (§9.3).

### 10.2 Analyzované verze

| Jazyk | Aktuální stabilní verze k 2026-08-26 | K čemu byla hodnocení ukotvena |
|---|---|---|
| **C#** | .NET 10.0.11 (2026-08-11) [R81] | .NET 10 LTS; rysy citovány z C# 14 (`field`), .NET 5 (anotované knihovny), .NET 8 a 9 |
| **Go** | 1.27.0 (2026-08-19) [R6] | specifikace včetně generik od 1.18; Go 1 compatibility promise; wiki k WebAssembly |
| **Java** | JDK 25 jako aktuální LTS [R11] | rysy citovány z JDK 17 (sealed) a JDK 21 (virtuální vlákna, pattern matching pro `switch`) |
| **Kotlin** | 2.4.10 (2026-07-14) [R81] | dokumentace **bez připnuté verze**, čtena 2026-08-23 |
| **PHP** | 8.5.9 (2026-07-30) [R81] | 8.5 ověřeno až 2026-08-26 (§10.1); rysy citovány z 8.1 (enumy, fibers) a 8.4 (property hooks) |
| **Python** | 3.14 (první vydání 2025-10-07), 3.13 rovněž v režimu oprav [R4] | volnovláknový build popsán pro 3.13; **stav v 3.14 samostatně neověřen** |
| **Rust** | 1.98.0 (2026-08-20) [R81] | kniha a dokumentace **bez připnuté verze**, čteny 2026-08-22 a 23 |
| **TypeScript** | 7.0.2 (2026-08-20) [R81][R83] | dokumentace **bez připnuté verze**; TypeScript 7 nebyl v analýze zohledněn — viz §10.3 |

### 10.3 Co audit verzí odhalil

**TypeScript 7 je jiný kompilátor, než jaký dokument analyzoval.** Vydání `v7.0.2` odkazuje na repozitář `microsoft/typescript-go` [R83], tedy na nativní přepis kompilátoru do Go. Dokument o tom nikde nemluví, protože jsem verzi nepřipnul a četl jsem prostě „aktuální dokumentaci“.

**Žádnou buňku to nemění:** typy se pořád mažou a výstupem je prostý JavaScript (P1), oficiální formátovač pořád neexistuje (P2), nástroje jsou pořád od Microsoftu (P3) a diskriminované unie fungují dál (P4). Ale je to materiální kontext, který v dokumentu chybí, a čtenář za rok má vědět, že analýza vznikla, aniž by s TypeScriptem 7 počítala.

**M1 jsem uplatňoval nerovnoměrně, a teď je to vidět černé na bílém.** U Go, Javy, .NET a Pythonu jsem ukotvil k verzím a u jednotlivých rysů uváděl, kdy přišly. U Kotlinu, Rustu a TypeScriptu jsem četl dokumentaci bez připnuté verze. U PHP jsem verzi znal a poznámky k vydání nečetl. Pravidlo přitom žádá obojí u všech — verzi i to, zda ji ekosystém dohnal.

**Praktický důsledek pro čtenáře:** tabulka v §10.2 je od teď to, podle čeho se pozná, co dokument doopravdy posuzoval. Kde je uvedeno „bez připnuté verze“, platí datum ověření u příslušné reference, ne číslo verze — a to je slabší, než by M1 chtělo.

## 11. Dodatek (2026-08-26): souběžnost, kterou kritéria neměřila

Zadavatel se zeptal, zda srovnání pokrývá podporu vláken, a zda profesionalitě Go neubírá `goto` nebo to, že je „správa paměti tak trochu na programátorovi“. Jedna premisa v té otázce neplatí, ale vede k mezeře, která je reálná a týká se otevřené shody v §7.5.

### 11.1 Co z té otázky platí a co ne

**Vlákna dokument pokrývá, ale mimo skóre.** §4.2 popisuje modely souběžnosti u šesti z osmi kandidátů; u C# a Rustu přiznaně nezjišťovala nic. Především ale **souběžnost nevstupuje do skóre profesionality vůbec** — kritéria P1 až P4 (§7.2) ji neměří ani jedním svým bodem.

**`goto` je slepá ulička.** V Go je, ale žádné kritérium §7.2 neměří konstrukce řízení toku, takže by pořadím nepohnulo. Podrobnosti o jeho omezeních v Go se v načteném úryvku specifikace nezobrazily, takže se o nich nic netvrdí.

**Se správou paměti je to naopak.** Specifikace Go říká v úvodu: *"It is strongly typed and garbage-collected."* [R54] Alokace a uvolňování paměti tedy na programátorovi **nejsou**.

**Ale obava o konzistenci paměti je oprávněná — jen jiným mechanismem.** Na programátorovi je v Go **absence datových závodů**. Go memory model definuje závod jako *"a write to a memory location happening concurrently with another read or write to that same location"* a u víceslovních struktur varuje, že závody *"can in turn lead to arbitrary memory corruption"*. Go je nechytá při překladu; detekují se až za běhu přes `go build -race`. Dokument zároveň zaznamenává, že Go je v tomhle **záměrně méně nedefinované než C a C++**, kde je *"the meaning of any program with a race is entirely undefined"* [R84].

### 11.2 Mezera v kritériu P1

Kritérium P1 se ptá, zda kompilátor chytí chybu dřív než uživatel — a měřilo hranici vynucení typů, nullabilitu a vyčerpávající větvení. **Bezpečnost souběžnosti neměřilo.**

To je mezera, ne detail, protože právě tohle je vlajkové tvrzení jednoho z kandidátů: *"By leveraging ownership and type checking, many concurrency errors are compile-time errors in Rust rather than runtime errors"* [R85]. Rust tedy chytá při překladu třídu chyb, kterou ostatní kandidáti nechávají na běh, na testy nebo na programátora — a P1 z toho nezaznamenalo nic.

### 11.3 Co by to udělalo s verdiktem, a proč to přesto nedělám

**Nejspíš by to rozseklo shodu v §7.5.** Kotlin a Rust jsou tam na dělené nule a dokument říká, že volba mezi nimi patří zadavateli. Kdyby P1 zahrnovalo prevenci datových závodů při překladu, byl by Rust v tomto bodě **jediný ✅** — Kotlin běží na JVM a datové závody mu kompilátor nehlídá stejně jako Go. Shoda by se s velkou pravděpodobností rozpadla ve prospěch Rustu.

**A přesně proto to neudělám.** Kritéria byla zafixovaná v §7.2 před rešerší. Dopsat páté kritérium teď, když už je vidět, že nadržuje jednomu ze dvou remízujících, je ten nejhorší možný okamžik — je to táž chyba jako přepsat váhy po zhlédnutí výsledku, jen hůř omluvitelná, protože tady je vidět i to, komu prospěje.

**Legitimní cesta existuje a je stejná jako u §7.1:** zadavatel může vyhlásit **třetí zadání** s vlastní, dopředu sepsanou a datovanou sadou kritérií, ve které souběžnost bude — a nechat ho proběhnout znovu. Verdikty §6.2 a §7.5 by zůstaly platit jako odpovědi na své otázky.

**Do té doby platí §7.5 tak, jak je: dělené první místo, a rozhodnutí na zadavateli.** Tenhle dodatek k tomu rozhodnutí přidává jeden doložený argument ve prospěch Rustu — nikoli změnu skóre.

## 12. Třetí zadání: profesionalita včetně souběžnosti (pravidla sepsána 2026-08-26 — PŘED rešerší)

### 12.1 Proč třetí zadání

§11.2 doložila, že kritérium P1 neměřilo bezpečnost souběžnosti, a §11.3 řekla, proč se to nedopisuje zpětně: v tu chvíli už bylo vidět, komu by to prospělo. Zadavatel proto 2026-08-26 vyhlásil **třetí zadání** s vlastní sadou kritérií, do níž souběžnost patří od začátku.

**Verdikty §6.2 a §7.5 zůstávají v platnosti** jako odpovědi na své vlastní otázky. Tohle je třetí otázka, ne oprava druhé.

### 12.2 Rozhodovací pravidla třetího zadání

**Kandidáti:** týchž osm v abecedním pořadí (§2.1). **Metodická pravidla M1 až M5 (§2.4) platí beze změny**, včetně povinného adversariálního průchodu a pravidla, že tvrzení o neexistenci potřebuje primární zdroj a pozitivní kontrolu.

**Kritéria:** čtyři převzatá z §7.2 **beze změny znění i beze změny už zjištěných hodnot** — přehodnocovat je teď by znamenalo měnit výsledek, který už znám — plus tři nová, vybraná zadavatelem 2026-08-26:

| # | Kritérium | Co se měří |
|---|---|---|
| **P1** | Kompilátor chytí chybu dřív než uživatel | Převzato z §7.2 beze změny |
| **P2** | Kód přečte cizí člověk bez kontextu | Převzato z §7.2 beze změny |
| **P3** | Velký refaktoring je bezpečný | Převzato z §7.2 beze změny |
| **P4** | Typový systém unese doménový model | Převzato z §7.2 beze změny |
| **P5** | Jazyk umí vytížit víc jader | Skutečný paralelismus nad sdílenou pamětí ve **výchozím** běhovém prostředí, ne přes rozšíření třetí strany |
| **P6** | Kompilátor chytá chyby souběžnosti | Prevence datových závodů **při překladu**; doloženo tvrzením vlastní dokumentace jazyka, ne odvozením |
| **P7** | Jedna jednotka souběžnosti je levná | Kolik souběžných úloh unese jeden proces a co stojí jejich vytvoření |

**Váhy: všech sedm stejně (1 × 7).** Zadavatel vybral všechna tři nová kritéria bez určení pořadí, takže rovné váhy jsou nejmenší domýšlení. **Je to volba, ne fakt, a má viditelný důsledek:** souběžnost tím dostává tři sedminy skóre, tedy 43 %. Poučen §6.3 a §7.4 se proto zavazuji doplnit citlivostní přehled, a v něm výslovně i variantu, kde si P5 až P7 **dělí jedno místo** (každé váhu ⅓), takže souběžnost váží jednu pětinu.

**Cena a agregace** jsou totožné se §2.3 a §7.2: ✅ = 0 · 🟡 = 1 · ❌ = 3, součet přes sedm kritérií, **vyhrává nejnižší** (rozsah 0 až 21).

**Tie-breaker, tentokrát sepsaný předem** — poučeno tím, že §7.2 ho neměla a shodu proto nešlo rozhodnout: při rovnosti součtu rozhoduje **P6**, pak **P1**, pak **P5**. Souběžnost je důvod, proč tohle zadání existuje, takže její bezpečnostní osa má při shodě přednost.

### 12.3 Předpověď zapsaná před rešerší

Uvažuji o rozptylu uvnitř kritérií, protože právě to odlišilo úspěšnou předpověď §7.3 od selhavší §2.3. **Jde o inferenci, ne o fakta.**

- **Největší rozptyl čekám u P6** — podle §11 je Rust pravděpodobně jediný, kdo prevenci datových závodů při překladu tvrdí o sobě sám. Pokud to tak dopadne, je to nejsilnější jednotlivá osa celého dokumentu.
- **P5 by mělo srazit Python, PHP a TypeScript** a nechat zbylých pět nahoře.
- **P7 by mělo nadržet Go a JVM** (goroutiny, virtuální vlákna od JDK 21) a Rust nechat uprostřed, protože bez runtime třetí strany nabízí vlákna OS.
- **Čekám, že Rust získá první místo sám** a shoda z §7.5 se rozpadne. Pokud ne, zapíše se to jako výsledek, ne jako oprava předpovědi.

### 12.4 Tabulka třetího zadání (ověřeno 2026-08-26)

P1 až P4 jsou převzaty ze §7.4 **beze změny**; sloupec „P1–P4“ je jejich součet. Nové jsou P5 až P7. Ceny: ✅ = 0 · 🟡 = 1 · ❌ = 3.

| Jazyk | P1–P4 (§7.4) | P5: vytíží víc jader | P6: kompilátor chytá závody | P7: jednotka souběžnosti je levná | Součet |
|---|---|---|---|---|---|
| **C#** | 2 | ✅ vlákna i `Task.Run` na pozadí [R86] | ❌ závody jsou na programátorovi; *"the .NET class libraries are not thread safe by default"* [R86] | 🟡 `Task` na fondu vláken, ale bez zelených vláken [R91] | **6** |
| **Go** | 4 | ✅ goroutiny multiplexované na vlákna OS [R59] | ❌ memory model je běhový; závody hlásí až `-race` [R84] | ✅ goroutina stojí *"little more than the allocation of stack space"* [R59] | **7** |
| **Java** | 5 | ✅ platformní i virtuální vlákna [R57] | ❌ *"memory consistency errors"* — programátor musí zavést happens-before [R90] | ✅ virtuálních vláken *"even millions"* v jednom procesu [R57] | **8** |
| **Kotlin** | 0 | ✅ přes JVM [R57] | ❌ dokumentace korutin nic takového netvrdí [R87] | ✅ *"running millions of them in one process"*; 50 000 korutin ≈ 500 MB proti ≈ 100 GB u vláken [R87] | **3** |
| **PHP** | 12 | ❌ Fibers jsou jen kooperativní, ne paralelní [R60] | ❌ nemá co chytat — bez paralelismu ve výchozím běhu [R60] | 🟡 Fibers jsou levné, ale nevytíží jádra [R60] | **19** |
| **Python** | 5 | ❌ *"only one thread can execute Python code at once"*; dokumentace radí `multiprocessing` [R88]. Build bez GIL od 3.13 **není výchozí** [R56] | ❌ zámky a synchronizace až za běhu [R88] | 🟡 asyncio pro I/O; vlákna jsou OS vlákna pod GIL [R88] | **12** |
| **Rust** | 0 | ✅ *"a collection of native OS threads"* [R89] | ✅ jediný z osmi: *"many concurrency errors are compile-time errors in Rust rather than runtime errors"* [R85] | 🟡 `std::thread` je 1:1 na OS, výchozí zásobník 2 MiB; `async`/`await` je v jazyce, ale exekutor je knihovna [R89] | **1** |
| **TypeScript** | 6 | 🟡 workeři jsou skutečná vlákna, ale oddělené kontexty; sdílení jen přes `SharedArrayBuffer` [R58] | ❌ nic takového netvrdí [R58] | ✅ smyčka událostí zvládne desítky tisíc souběžných I/O operací [R58] | **10** |

**Vyhodnocení předpovědi ze §12.3 — vyšla ve všech čtyřech bodech.** Největší rozptyl je opravdu u P6 (jedno ✅ proti sedmi ❌, tedy nejostřejší osa dokumentu). P5 srazilo Python, PHP i TypeScript. P7 nadrželo Go a JVM a Rust nechalo uprostřed. A **Rust získal první místo sám**, čímž se shoda ze §7.5 rozpadla.

*Že předpověď vyšla, je důvod k větší podezřívavosti, ne k menší — proto adversariální průchod v §12.5 míří přednostně právě na buňky, které o výsledku rozhodly.*

**Citlivost na váhy, jak §12.2 slíbila.** Ve variantě, kde si P5 až P7 dělí jedno místo (každé ⅓, souběžnost tedy váží pětinu místo 43 %):

| Jazyk | Rovné váhy (1×7) | P5–P7 dělí jedno místo |
|---|---|---|
| **Rust** | **1** | **0,33** |
| **Kotlin** | 3 | 1,00 |
| **C#** | 6 | 3,33 |
| **Go** | 7 | 5,00 |
| **Java** | 8 | 6,00 |
| **TypeScript** | 10 | 7,33 |
| **Python** | 12 | 7,33 |
| **PHP** | 19 | 14,33 |

**Pořadí na prvních dvou místech se nemění.** Obava ze §12.2, že tři sedminy udělají z dokumentu o profesionalitě dokument o souběžnosti, se tedy na verdiktu neprojevila — Rust vede i tehdy, když souběžnost váží pětinu.

### 12.5 Verdikt třetího zadání (2026-08-26)

**Vyhrává Rust se součtem 1**, před Kotlinem se 3. **Shoda ze §7.5 je rozseknutá**, a rozhodla ji jediná osa: P6.

**Adversariální průchod (M5), mířený na buňky, které o výsledku rozhodly:**

| Námitka | Výsledek |
|---|---|
| **Chytá Rust závody opravdu při překladu?** | **Obstálo s upřesněním.** Zdroj říká *"many concurrency errors"*, ne „všechny“, a záruka platí pro **bezpečný** Rust — `unsafe` z ní vystupuje. ✅ tedy znamená „jediný, kdo to při překladu vůbec dělá“, ne „nelze napsat závod“. |
| **Není ❌ u ostatních sedmi příliš tvrdé?** | **Obstálo.** Java má `@GuardedBy` v nástrojích třetích stran, C# analyzátory, Go `-race` — ale ani jeden z jazyků to netvrdí o sobě ve vlastní dokumentaci, což bylo znění kritéria P6 (§12.2). |
| **Rust 🟡 v P7 stojí na mém vlastním rozlišení** — knihovna versus jiný build runtime | **Přiznaná slabina.** Kdyby buňka padla na ❌, Rust má 3 a **je na shodě s Kotlinem**. Pak ale vypálí tie-breaker sepsaný v §12.2 předem: rozhoduje P6, kde má Rust ✅ a Kotlin ❌. **Verdikt drží i tak** — a je to první případ v celém dokumentu, kdy se předem sepsaný tie-breaker vyplatil. |

*Omezení stejné jako v §6.1: průchod běžel ve stejném kontextu, který závěr vytvořil.*

**Co za Rust platíš — přijaté kompromisy:**

1. **Nejmenší náborová základna z osmi po Kotlinu** — 14,5 % (§5.1).
2. **Bez datované tabulky podpory** (§4.5); nahrazuje ji slib kompatibility, který je věcně silný, ale nedá se ukázat prstem na řádek s datem.
3. **Jediný, kdo není ✅ v backendu** — nejvýš vážené doméně prvního zadání (§3).
4. **Levná souběžnost potřebuje knihovnu** — `std::thread` je 1:1 na vlákna OS s 2 MiB zásobníkem.
5. **A co dokument nikdy neměřil:** dobu překladu ani strmost učení. To jsou dvě nejčastější námitky proti Rustu a **výsledek zčásti odráží, co se měřit rozhodlo.**

**Vztah k ostatním verdiktům.** §6.2 (TypeScript, pokrytí domén) a §7.5 (dělené první místo) **platí dál** jako odpovědi na své otázky. Tenhle verdikt neruší ani jeden; přidává třetí odpověď na třetí otázku. **Rozpor mezi nimi zůstává hlavním nálezem dokumentu** — a nově je vidět ještě ostřeji: vítěz prvního zadání je tady šestý.

## Reference

Ověřeno k 2026-08-22 (kolo 1 — brána B2, §4.4 a §4.5).

**Financování a governance**

- [R3] The PHP Foundation — mise, deset smluvních vývojářů, sponzoři. Ověřeno 2026-08-22: <https://thephp.foundation/>
- [R5] Python Software Foundation — mise, duševní vlastnictví, CPython Developer in Residence. Ověřeno 2026-08-22: <https://www.python.org/psf/about/>
- [R7] Go FAQ — původ projektu, tým v Googlu, toolchain `gc`. Ověřeno 2026-08-22: <https://go.dev/doc/faq>
- [R10] .NET Foundation — rozsah působnosti (komunitní projekty), sponzoři. Ověřeno 2026-08-22: <https://dotnetfoundation.org/>
- [R12] Eclipse Adoptium — členové pracovní skupiny. Ověřeno 2026-08-22: <https://adoptium.net/en-GB/members/>
- [R13] Kotlin Foundation — zakladatelé, členové, vyhlášené úkoly. Ověřeno 2026-08-22: <https://kotlinfoundation.org/>
- [R15] Rust Foundation — zakládající platinoví členové, účel. Ověřeno 2026-08-22: <https://rustfoundation.org/>

**Závazky podpory a kompatibility**

- [R2] PHP — Supported Versions (2 roky aktivní + 2 roky bezpečnostní). Ověřeno 2026-08-22: <https://www.php.net/supported-versions.php>
- [R4] Python Developer's Guide — Status of Python versions (PEP 602, pět let). Ověřeno 2026-08-22: <https://devguide.python.org/versions/>
- [R6] Go — Release History a politika podpory (do vydání dvou novějších verzí); Go 1.27.0 vydáno 2026-08-19. Ověřeno 2026-08-22: <https://go.dev/doc/devel/release>
- [R8] Go 1 and the Future of Go Programs — slib zpětné kompatibility a jeho výjimky. Ověřeno 2026-08-22: <https://go.dev/doc/go1compat>
- [R9] .NET Support Policy — LTS 36 měsíců, STS 24 měsíců, konkrétní data. Ověřeno 2026-08-22: <https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core>
- [R11] Eclipse Adoptium — Support (LTS každé dva roky, „at least four years“, zdarma). Ověřeno 2026-08-22: <https://adoptium.net/support/>
- [R14] Kotlin — Evolution principles (binární kompatibilita, deprecation cyklus, `-language-version`). Ověřeno 2026-08-22: <https://kotlinlang.org/docs/kotlin-evolution-principles.html>
- [R16] The Rust Edition Guide — Editions (stabilita, interoperabilita edicí). Ověřeno 2026-08-22: <https://doc.rust-lang.org/edition-guide/editions/index.html>
- [R17] TypeScript's Release Process (wiki) — kadence vydání; o LTS mlčí. Ověřeno 2026-08-22: <https://github.com/microsoft/TypeScript/wiki/TypeScript%27s-Release-Process>
- [R18] microsoft/TypeScript issue #49088 „Document TypeScript version lifetime and EOL“ (uzavřeno) — vyjádření týmu, že oficiální politika neexistuje. Ověřeno 2026-08-22: <https://github.com/microsoft/TypeScript/issues/49088>
- [R19] Node.js — Previous Releases (LTS 30 měsíců). Ověřeno 2026-08-22: <https://nodejs.org/en/about/previous-releases>

**Distribuce a nasazení (kolo 2, doména CLI)**

- [R20] .NET — Native AOT deployment overview, včetně sekce Limitations. Ověřeno 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/>
- [R21] GraalVM — Native Image (closed-world assumption, omezení reflexe a JNI). Ověřeno 2026-08-22: <https://www.graalvm.org/latest/reference-manual/native-image/>
- [R22] Node.js — Single executable applications (Stability 1.1, omezení). Ověřeno 2026-08-22: <https://nodejs.org/api/single-executable-applications.html>
- [R23] Deno — `deno compile` (samostatná binárka, křížový překlad). Ověřeno 2026-08-22: <https://docs.deno.com/runtime/reference/cli/compile/>
- [R24] Go — Installing Go from source, tabulka `GOOS`/`GOARCH`. Ověřeno 2026-08-22: <https://go.dev/doc/install/source>
- [R25] static-php-cli — Guide (staticky slinkované PHP binárky, podporované platformy a verze). Ověřeno 2026-08-22: <https://static-php.dev/en/guide/>
- [R26] PyInstaller — How it works / operating mode (one-file režim, absence křížového překladu). Ověřeno 2026-08-22: <https://pyinstaller.org/en/stable/operating-mode.html>
- [R27] Rust — Platform Support (definice Tier 1 a Tier 2). Ověřeno 2026-08-22: <https://doc.rust-lang.org/rustc/platform-support.html>

**Frameworky a jejich závazky podpory (kolo 3, doména backend)**

- [R28] Symfony — Releases (standardní vydání 8 měsíců oprav a 14 měsíců bezpečnosti; LTS 3 roky oprav a 4 roky bezpečnosti). Ověřeno 2026-08-22: <https://symfony.com/releases>
- [R29] Laravel — Release Notes, sekce Support Policy (*"bug fixes are provided for 18 months and security fixes are provided for 2 years"*). Ověřeno 2026-08-22 na stránce dokumentace 12.x, která zároveň upozorňuje, že aktuální řadou je 13.x: <https://laravel.com/docs/12.x/releases>
- [R30] Django — Download, přehled podporovaných verzí a tříletého okna. Ověřeno 2026-08-22: <https://www.djangoproject.com/download/>
- [R31] Spring Boot — Supported Versions (wiki projektu): minor *"at least 12 months"*, major *"at least 3 years"*. Ověřeno 2026-08-22: <https://github.com/spring-projects/spring-boot/wiki/Supported-Versions>
- [R32] Fastify — Long Term Support. Ověřeno 2026-08-22: <https://fastify.dev/docs/latest/Reference/LTS/>
- [R33] expressjs/express — výpis repozitáře; politika podpory nenalezena v kořeni ani v `.github`. **Závěr je slabý:** pozitivní kontrola u repozitáře `expressjs/expressjs.com` selhala (cesta `en` vrátila 404), takže o struktuře dokumentace nic netvrdím. Ověřeno 2026-08-22: <https://github.com/expressjs/express>
- [R34] tokio-rs/axum — výpis repozitáře; datovaná politika podpory nenalezena v kořeni ani v adresáři crate `axum`. Pozitivní kontrola prošla (`Cargo.toml` přítomen v obou výpisech). Ověřeno 2026-08-22: <https://github.com/tokio-rs/axum>

**Cesta do prohlížeče (kolo 4, doména frontend)**

- [R35] ASP.NET Core — Host and deploy Blazor WebAssembly (stažení runtime, Webcil, trimming, komprese, `EmccMaximumHeapSize`). Ověřeno 2026-08-22: <https://learn.microsoft.com/en-us/aspnet/core/blazor/host-and-deploy/webassembly/>
- [R36] Kotlin/Wasm overview — stav Beta a požadavky na prohlížeč. Ověřeno 2026-08-22: <https://kotlinlang.org/docs/wasm-overview.html>
- [R37] Go Wiki — WebAssembly (velikost výstupu, vazba `wasm_exec.js` na verzi, TinyGo). Ověřeno 2026-08-22: <https://go.dev/wiki/WebAssembly>
- [R38] pyodide/pyodide — README (port CPythonu do WebAssembly/Emscriptenu, podpora balíčků, přístup k Web API). Ověřeno 2026-08-22: <https://github.com/pyodide/pyodide>. *Stránka s údaji o velikosti* <https://pyodide.org/en/stable/project/about.html> *vrátila 403; žádné číslo o velikosti se proto v dokumentu netvrdí.*
- [R39] TypeScript Handbook — TypeScript from Scratch (mazání typů, zachování běhového chování). Ověřeno 2026-08-22: <https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html>
- [R40] Rust and WebAssembly (kniha pracovní skupiny) — nese oznámení, že projekt a web už nejsou udržovány. Ověřeno 2026-08-22: <https://rustwasm.github.io/docs/book/>
- [R41] TeaVM — úvodní stránka (AOT překladač bytekódu Javy do JavaScriptu a WebAssembly). Ověřeno 2026-08-22: <https://teavm.org/>
- [R42] seanmorris/php-wasm — README (pokrytí PHP 8.0–8.5, balíčky, licence Apache-2.0). Ověřeno 2026-08-22: <https://github.com/seanmorris/php-wasm>

**Data, ML a dávkové zpracování (kolo 5)**

- [R43] ML.NET — přehled na dotnet.microsoft.com (first-party rámec, podporované scénáře, nasazení v produktech Microsoftu). Ověřeno 2026-08-22: <https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet>
- [R44] Apache Spark — dokumentace, seznam jazykových API a nativní implementační jazyk. Ověřeno 2026-08-22: <https://spark.apache.org/docs/latest/>
- [R45] pola-rs/polars — README (dotazovací engine psaný v Rustu, seznam jazykových vazeb). Ověřeno 2026-08-22: <https://github.com/pola-rs/polars>
- [R46] TensorFlow.js — přehled (ML v prohlížeči i v Node.js). Ověřeno 2026-08-22: <https://www.tensorflow.org/js>

**Přísnost a typové systémy (kolo 6, §4.1)**

- [R47] Python — `typing` (runtime nevynucuje anotace; chování `Any`). Ověřeno 2026-08-22: <https://docs.python.org/3/library/typing.html>
- [R48] mypy — Command line (obsah `--strict`, `--warn-unused-ignores`, vymezení záruky). Ověřeno 2026-08-22: <https://mypy.readthedocs.io/en/stable/command_line.html>
- [R49] PHP Manual — Type declarations (`TypeError` při volání, `declare(strict_types=1)` po souborech, koerce, absence generik). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.types.declarations.php>
- [R50] C# — Nullable reference types (výhradně věc překladu, operátor `!`, pasti u `default` struktur a polí, anotované knihovny od .NET 5). Ověřeno 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references>
- [R51] TypeScript — TSConfig `strict` (rodina přepínačů; upozornění na růst přísnosti mezi verzemi). Ověřeno 2026-08-22: <https://www.typescriptlang.org/tsconfig/strict.html>
- [R52] Kotlin — Null safety (nullabilita v typovém systému, platform types při interoperabilitě s Javou). Ověřeno 2026-08-22: <https://kotlinlang.org/docs/null-safety.html>
- [R53] The Rust Programming Language — Defining an Enum (`Option<T>`, absence nullu). Ověřeno 2026-08-22: <https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html>
- [R54] The Go Programming Language Specification — nulové hodnoty, `nil`, typové parametry od Go 1.18. Ověřeno 2026-08-22: <https://go.dev/ref/spec>
- [R55] The Java Tutorials — Type Erasure. Ověřeno 2026-08-22: <https://docs.oracle.com/javase/tutorial/java/generics/erasure.html>

**Souběžnost, výkon a nábor (kolo 7, §4.2 a §4.6)**

- [R56] Python — Free-threaded CPython HOWTO (build bez GIL od 3.13, znovuzapnutí GIL nepřipraveným rozšířením, režie 1–8 %). Ověřeno 2026-08-22: <https://docs.python.org/3/howto/free-threading-python.html>
- [R57] Oracle — Virtual Threads (JDK 21; miliony vláken; „not faster threads… scale, not speed“). Ověřeno 2026-08-22: <https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html>. *Primární JEP 444 na openjdk.org vrátil 403.*
- [R58] Node.js — `worker_threads` (užitečné pro CPU, ne pro I/O; Stability 2 — Stable). Ověřeno 2026-08-22: <https://nodejs.org/api/worker_threads.html>
- [R59] Effective Go — Concurrency (cena goroutiny, multiplexování na vlákna OS). Ověřeno 2026-08-22: <https://go.dev/doc/effective_go>
- [R60] PHP Manual — Fibers (od PHP 8.1). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.fibers.php>
- [R61] Stack Overflow Developer Survey 2025 — Technology, podíly u profesionálních vývojářů. Ověřeno 2026-08-22: <https://survey.stackoverflow.co/2025/technology>

**Profesionalita jazyka (§7.4)**

- [R67] Kotlin — Sealed classes and interfaces (kompilátor zná všechny podtřídy; `when` bez `else`). Ověřeno 2026-08-23: <https://kotlinlang.org/docs/sealed-classes.html>
- [R68] Oracle — Sealed Classes and Interfaces (JEP 409, povolené podtřídy). Ověřeno 2026-08-23: <https://docs.oracle.com/en/java/javase/21/language/sealed-classes-and-interfaces.html>
- [R69] Oracle — Pattern Matching for switch (JEP 441, vyčerpávající pokrytí sealed typu bez `default`). Ověřeno 2026-08-23: <https://docs.oracle.com/en/java/javase/21/language/pattern-matching-switch.html>
- [R70] PHP Manual — Backed enumerations (*"may be backed by types of `int` or `string`"*). Ověřeno 2026-08-23: <https://www.php.net/manual/en/language.enumerations.backed.php>
- [R71] TypeScript Handbook — Narrowing (diskriminované unie, kontrola vyčerpání přes `never`). Ověřeno 2026-08-23: <https://www.typescriptlang.org/docs/handbook/2/narrowing.html>
- [R72] The Rust Programming Language — The match Control Flow Construct (*"Matches in Rust are exhaustive"*). Ověřeno 2026-08-23: <https://doc.rust-lang.org/book/ch06-02-match.html>
- [R73] Go FAQ — proč Go nemá variantní typy a záměrná jednoduchost. Ověřeno 2026-08-23: <https://go.dev/doc/faq>
- [R74] The Go Blog — gofmt (součást distribuce; *"uncontroversial"*). Ověřeno 2026-08-23: <https://go.dev/blog/gofmt>
- [R75] Vlastnictví nástrojů podle organizace na GitHubu, ověřeno přes API 2026-08-23 (pozitivní kontrola: všechny dotazy vrátily metadata repozitáře): `rust-lang/rustfmt`, `rust-lang/rust-analyzer`, `golang/tools` (gopls), `Kotlin/ktfmt`, `Kotlin/kotlin-lsp`, `psf/black`, `dotnet/format`, `microsoft/pyright` — proti `prettier/prettier`, `PHP-CS-Fixer/PHP-CS-Fixer` a `google/google-java-format`, které pod organizací svého jazyka **nejsou**.
- [R76] dotnet/csharplang — `proposals/standard-unions.md`; součtové typy jsou v C# stále **návrh**, ne jazykový rys. Ověřeno 2026-08-23: <https://github.com/dotnet/csharplang/blob/main/proposals/standard-unions.md>
- [R77] Python — `typing.assert_never` (kontrola vyčerpání, ale jen ve statické kontrole). Ověřeno 2026-08-23: <https://docs.python.org/3/library/typing.html>

**Souběžnost v třetím zadání (§12.4)**

- [R86] .NET — Managed Threading Best Practices (souběhy jsou na programátorovi; knihovny .NET nejsou thread-safe implicitně). Ověřeno 2026-08-26: <https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices>
- [R87] Kotlin — Coroutines basics (miliony korutin v procesu; 50 000 korutin ≈ 500 MB proti ≈ 100 GB u vláken). Ověřeno 2026-08-26: <https://kotlinlang.org/docs/coroutines-basics.html>
- [R88] Python — `threading` (GIL, doporučení `multiprocessing` pro víc jader, zámky až za běhu). Ověřeno 2026-08-26: <https://docs.python.org/3/library/threading.html>
- [R89] Rust — `std::thread` (nativní vlákna OS, výchozí zásobník 2 MiB na platformách Tier 1). Ověřeno 2026-08-26: <https://doc.rust-lang.org/std/thread/>
- [R90] The Java Tutorials — Memory Consistency Errors (happens-before je na programátorovi). Ověřeno 2026-08-26: <https://docs.oracle.com/javase/tutorial/essential/concurrency/memconsist.html>
- [R91] C# — Asynchronous programming scenarios (`Task`, fond vláken, `Task.Run` pro výpočetní úlohy). Ověřeno 2026-08-26: <https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios>

**Souběžnost a paměťový model (§11)**

- [R84] The Go Memory Model — definice datového závodu, chování implementace, varování před poškozením paměti u víceslovních struktur, srovnání s C a C++. Ověřeno 2026-08-26: <https://go.dev/ref/mem>
- [R85] The Rust Programming Language — Fearless Concurrency (*"many concurrency errors are compile-time errors in Rust rather than runtime errors"*). Ověřeno 2026-08-26: <https://doc.rust-lang.org/book/ch16-00-concurrency.html>

**Audit verzí (§10)**

- [R81] Aktuální stabilní verze zjištěné přes GitHub API 2026-08-26 (pozitivní kontrola: všechny dotazy vrátily data vydání): `JetBrains/kotlin` v2.4.10 (2026-07-14), `rust-lang/rust` 1.98.0 (2026-08-20), `microsoft/TypeScript` v7.0.2 (2026-08-20), `dotnet/core` v10.0.11 (2026-08-11), `php/php-src` php-8.5.9 (2026-07-30).
- [R82] PHP 8.5 — nové vlastnosti (pipe operátor, `clone with`, `#[\NoDiscard]`, `final` u promovaných vlastností). Ověřeno 2026-08-26: <https://www.php.net/releases/8.5/en.php>
- [R83] microsoft/TypeScript — vydání `v7.0.2` odkazuje na `microsoft/typescript-go`, tedy na nativní přepis kompilátoru. Ověřeno 2026-08-26: <https://github.com/microsoft/typescript-go>

**Dodatek (§9)**

- [R78] Organizace `php` na GitHubu — výpis repozitářů; formátovač ani jazykový server pod ní nejsou. Pozitivní kontrola prošla (`php-src` a webové vlastnosti projektu přítomny). Ověřeno 2026-08-26: <https://github.com/orgs/php/repositories>
- [R79] PHPStan — Rule Levels (0 až 10; úroveň 6 „report missing typehints“, úroveň 10 implicitní `mixed`). Ověřeno 2026-08-26: <https://phpstan.org/user-guide/rule-levels>
- [R80] Organizace `python` na GitHubu — `mypy` a `typeshed` jsou pod ní. Pozitivní kontrola prošla (`peps`, `typing`, `pythondotorg` přítomny). Ověřeno 2026-08-26: <https://github.com/orgs/python/repositories>

**Oprava (§8)**

- [R66] microsoft/TypeScript — `SUPPORT.md`, sekce „Microsoft Support Policy“. Ověřeno 2026-08-23: <https://github.com/microsoft/TypeScript/blob/main/SUPPORT.md>

**Adversariální průchod (§6.1)**

- [R65] actix/actix-web — výpis repozitáře; datovaná politika podpory nenalezena v kořeni ani v `.github`. Pozitivní kontrola prošla (`Cargo.toml` ve výpisu). Ověřeno 2026-08-23: <https://github.com/actix/actix-web>

**Vlastnosti jako jazykový rys (kolo 8, §4.8)**

- [R62] C# — Properties (vlastnosti jako členy s přístupovými metodami `get`/`set`). Ověřeno 2026-08-22: <https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties>
- [R63] Kotlin — Properties (`val`/`var`, automaticky generované a vlastní přístupové metody). Ověřeno 2026-08-22: <https://kotlinlang.org/docs/properties.html>
- [R64] Python — vestavěná funkce `property()` a dekorátor `@property`. Ověřeno 2026-08-22: <https://docs.python.org/3/library/functions.html>

**Jazykové vlastnosti**

- [R1] PHP Manual — Property Hooks (verze: zavedeno v PHP 8.4). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

*Nedostupné zdroje:* Oracle Java SE Support Roadmap <https://www.oracle.com/java/technologies/java-se-support-roadmap.html> vrátil 2026-08-22 HTTP 403; Java se proto opírá o [R11][R12].


---

Dokument je datovaný snímek a neaktualizuje se zpětně. Nové poznatky přibývají jako datované sekce na konci; opravy se zapisují jako datované dodatky.
