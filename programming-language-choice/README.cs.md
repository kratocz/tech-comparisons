# Volba programovacího jazyka: jeden jazyk na dlouhá léta pro nové projekty

- **Verdikt:** ⏳ zatím žádný. Pravidla (§2) sepsána a potvrzena PŘED rešerší. Kolo 1 (§4.4, §4.5) hotové: **brána B2 vypálila proti TypeScriptu** — rozhodnutí o úpravě pravidla čeká na zadavatele a nebude provedeno tiše (§4.5).
- **Sycené rozhodnutí:** na čem stavět **nové** projekty (vlastní, firemní i cizí) v horizontu let — a čím ta volba argumentovat u někoho, kdo u úvahy nebyl.
- **Fakta ověřena:** 🟡 kolo 1 (2026-08-22): §4.4 a §4.5 — financování, governance a závazky podpory všech osmi kandidátů, reference [R1]–[R19]. Otevřené `[OVĚŘIT]`: §3, §4.1–§4.3, §4.6–§4.8, §5.
- **Adversariální průchod:** ❌ zatím neproběhl (povinný před verdiktem, §2.4 M5).
- **Jazyk:** 🇨🇿 čeština (originál); 🇬🇧 kanonická anglická verze zatím nevznikla
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] kontext (§1) — 2026-08-22
- [x] rozhodovací pravidla (§2) sepsána před rešerší — 2026-08-22
- [x] řádek v kořenovém README — 2026-08-22
- [x] **potvrdit rozhodovací pravidla (§2) uživatelem** — 2026-08-22: váhy domén doplněny (§2.3), B1 zúžena na backend (§2.2), agregace přepsána na váženou cenu; předpověď zapsána před rešerší
- [ ] tabulka vlastností (§4.8) — po §3
- [ ] regret matrix (§3) — 8 kandidátů × 4 domény
- [~] trvanlivá vrstva (§4) — hotovo §4.4 a §4.5 (kolo 1, 2026-08-22); zbývá §4.1–§4.3, §4.6, §4.7
- [ ] datovaný snapshot (§5)
- [ ] adversariální průchod (§2.4 M5), výsledek do hlavičky
- [ ] verdikt (§6)
- [ ] EN překlad (`README.md`) jako kanonická verze

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

Sloupce jsou seřazené **podle váhy domény sestupně** (4 · 3 · 2 · 1, §2.3), aby se tabulka četla zleva od toho, co rozhoduje nejvíc. Poslední sloupec je vážená cena podle §2.3 — nižší je lepší, rozsah 0 až 30.

| Jazyk | Backend a API (×4) | CLI a automatizace (×3) | Frontend v prohlížeči (×2) | Data, ML, dávky (×1) | Vážená cena |
|---|---|---|---|---|---|
| **C#** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **Go** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **Java** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **Kotlin** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **PHP** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **Python** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **Rust** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |
| **TypeScript** | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] | [OVĚŘIT] |

### 3.1 Jak tabulku číst

[OVĚŘIT] — doplní se po rešerši: kdo vyhrává kde, kdo padl na B1 a proč, a která doména se ukázala jako ta, o kterou se verdikt láme.

## 4. Trvanlivá vrstva (nese verdikt)

### 4.1 Přísnost, kterou lze zapnout a vynutit

[OVĚŘIT] — rozklad podle M2 (§2.4) na všech osm kandidátů: běh vs. kontrola, expresivita, nakažlivost neotypovaných závislostí, vynutitelnost v CI a ráčna, cena na zelené louce.

### 4.2 Výkonový strop a model souběžnosti

[OVĚŘIT] — měkká osa (§1), strop popsaný čísly, ne dojmem.

### 4.3 Čím se platí za každou ze čtyř domén

[OVĚŘIT] — podklad pro §3.

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
| **TypeScript** | **Žádná oficiální politika** — viz níže | — | — nezjišťováno v tomto kole | [R17][R18] |

**Dvě věci, které tahle tabulka odhalila a které jsem nečekal.**

**Za prvé: „podpora“ znamená u kompilátoru něco jiného než u běhového prostředí, a brána B2 ten rozdíl nerozlišuje.** U PHP, Pythonu, Javy a .NET je podpora hodinami tikající povinnost — neaktualizovaná verze je bezpečnostní dluh vystavený internetu. U Go, Rustu, Kotlinu a TypeScriptu je nosnějším závazkem **slib kompatibility**: starý kód se dál překládá a artefakt běží dál. Rustova formulace („co jednou vyjde jako stabilní, podporujeme ve všech budoucích vydáních“) je věcně silnější závazek k dekádě než kterákoli datovaná tabulka LTS, přestože žádnou tabulku nemá. Krátké podpůrné okno Go tedy **není** slabina, za jakou by ho tabulka na první pohled vydávala — jde o jiný model, kde se povyšuje často, ale levně.

**Za druhé: TypeScript jako jediný nemá žádný závazek, a je to doloženo primárním zdrojem, ne prázdným hledáním.** V issue microsoft/TypeScript #49088 („Document TypeScript version lifetime and EOL“, stav: uzavřeno) odpovídá Ryan Cavanaugh z týmu TypeScriptu: *"To my knowledge, we don't have an official policy beyond the one implied by the fact that we ship our components in Visual Studio. Security fixes are backported I believe for the last year of releases; non-security fixes are not backported."* [R18] Formulaci nechávám i s jejím zaváháním („I believe“) — zdroj si tím není jistý a dokument to nesmí ztvrdit.

Pozor ale na rozsah tohoto tvrzení: **týká se kompilátoru, ne běhového prostředí.** Kód v TypeScriptu běží na Node.js nebo v prohlížeči a životní cyklus má ten runtime — Node.js drží LTS **30 měsíců** [R19]. Tvrzení „TypeScript nemá LTS“ tedy neznamená „aplikace v TypeScriptu nemá podporovaný runtime“; znamená, že závazek nemá ten překladač, který pouštíš při buildu.

**Výsledek brány B2 (zapsáno 2026-08-22).** Pravidlo zní: chybí identifikovatelný plátce **nebo** doložitelný závazek k dlouhodobé podpoře → vyřazen. Plátce má všech osm (§4.4). Závazek k podpoře má sedm z osmi — buď datovanou tabulkou (C#, Java, PHP, Python), nebo slibem kompatibility (Go, Kotlin, Rust). **Osmý, TypeScript, jej podle vlastního vyjádření týmu nemá, a brána B2 tak vypálila proti němu.**

Rozhodnutí, co s tím, **nepatří mně a nebude provedeno tiše**: B2 se ukázala jako nástroj, který u překladačů měří něco jiného než u běhových prostředí, a to je vada v návrhu pravidla, ne ve faktech pod ním. Pravidlo proto zůstává zapsané přesně tak, jak bylo, i s poznámkou, že vypálilo. Případná úprava bude zaznamenána jako **dodatečná, s datem a důvodem** — ne jako by tam byla od začátku.

### 4.6 Náborový rybník, předatelnost, zaškolení

[OVĚŘIT] — plná váha kvůli firemní roli (§1).

### 4.7 Zralost frameworků a knihoven

[OVĚŘIT]

### 4.8 Souhrnná tabulka vlastností (důkazní materiál — nenese verdikt)

Tabulka, na kterou se čtenář ptá jako první: konkrétní vlastnosti jazyk po jazyku. **Verdikt z ní neplyne** — ten vydává §3 podle pravidla §2.3. Tahle tabulka shrnuje, co zjistily §4.1–§4.7, a slouží jako podklad pro tie-breakery. Kdyby ukazovala jinam než §3, platí §3; rozpor se zapíše, ne zamlčí.

Dvě omezení, obě záměrná:

- **Jen vedoucí kandidáti** podle vážené ceny z §3, ne všech osm — zbytek je vyřazen už cenou a šířka tabulky by šla proti čitelnosti. Kolik jich bude, se ukáže po §3.
- **Jen vlastnosti napojené na rozhodovací pravidlo nebo tie-breaker.** Vlastnost, která nezmění žádné rozhodnutí, je dekorace a do tabulky nepatří. Každá buňka podle M1 (§2.4) uvede, ve které verzi vlastnost přišla a zda ji ekosystém dohnal.

Jazyky jsou tu **ve sloupcích** (v §3 jsou v řádcích), protože patnáct vlastností jako sloupců je nečitelných. Pořadí jazyků zůstává abecední jako všude jinde v dokumentu (§2.1).

Plánované řádky — tři skupiny:

- **▸ Přísnost** (živí §4.1 a tie-breaker 1): typy vynucené za běhu vs. jen při kontrole · null safety · generika v jazyce vs. jen v anotacích pro statickou analýzu · sealed typy a vyčerpávající pattern matching · neměnnost jako výchozí stav · co jde vynutit v CI a existuje-li ráčna proti couvání
- **▸ Ergonomie** (sem patří i tři vlastnosti z původního zadání — jsou to otázky pohodlí a stylu, ne korektnosti, a míchat je s přísností by zkreslilo obojí): vyžaduje deklaraci proměnných · zakazuje globální proměnné · get/set properties
- **▸ Provoz a ekosystém** (živí §4.2 a §4.4–§4.7): model souběžnosti · GC vs. bez GC · startup čas · distribuce jedním binárkem · oficiální správce balíčků · oficiální formátovač a jazykový server

[OVĚŘIT] — tabulka se doplní po §3 a §4.1–§4.7.

## 5. Datovaná vrstva (snapshot — rychle zastarává)

[OVĚŘIT] — verze, termíny LTS, stav toolingu. Nenese verdikt.

## 6. Verdikt (zatím žádný)

Rešerše nezačala. Verdikt se doplní podle pravidla §2.3 a až po adversariálním průchodu (§2.4 M5).

## 7. Reference

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

**Jazykové vlastnosti**

- [R1] PHP Manual — Property Hooks (verze: zavedeno v PHP 8.4). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

*Nedostupné zdroje:* Oracle Java SE Support Roadmap <https://www.oracle.com/java/technologies/java-se-support-roadmap.html> vrátil 2026-08-22 HTTP 403; Java se proto opírá o [R11][R12].


---

Dokument je datovaný snímek a neaktualizuje se zpětně. Nové poznatky přibývají jako datované sekce na konci; opravy se zapisují jako datované dodatky.
