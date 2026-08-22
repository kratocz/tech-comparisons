# Volba programovacího jazyka: jeden jazyk na dlouhá léta pro nové projekty

- **Verdikt:** ⏳ zatím žádný. Regret matrix je kompletní a **prozatímní pořadí vede TypeScript s váženou cenou 4** před Pythonem (5), viz §3.1 — pořadí ale zatím nesmí být verdiktem ze tří doložených důvodů uvedených tamtéž. **Předpověď zapsaná v §2.3 se nepotvrdila:** Go skončilo sedmé z osmi.
- **Sycené rozhodnutí:** na čem stavět **nové** projekty (vlastní, firemní i cizí) v horizontu let — a čím ta volba argumentovat u někoho, kdo u úvahy nebyl.
- **Fakta ověřena:** 🟡 2026-08-22, pět kol, reference [R1]–[R46]: financování, governance a závazky podpory (§4.4, §4.5); všechny čtyři domény (§4.3) a kompletní regret matrix včetně vážené ceny (§3, §3.1). Otevřené `[OVĚŘIT]`: §4.1, §4.2, §4.6–§4.8, §5. **Čtyři buňky označeny jako nejisté** a přednostně poslány do adversariálního průchodu: Rust v backendu, Go a PHP v prohlížeči (obě ❌), Rust v prohlížeči.
- **Adversariální průchod:** ❌ zatím neproběhl (povinný před verdiktem, §2.4 M5).
- **Jazyk:** 🇨🇿 čeština (originál); 🇬🇧 kanonická anglická verze zatím nevznikla
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] kontext (§1) — 2026-08-22
- [x] rozhodovací pravidla (§2) sepsána před rešerší — 2026-08-22
- [x] řádek v kořenovém README — 2026-08-22
- [x] **potvrdit rozhodovací pravidla (§2) uživatelem** — 2026-08-22: váhy domén doplněny (§2.3), B1 zúžena na backend (§2.2), agregace přepsána na váženou cenu; předpověď zapsána před rešerší
- [ ] tabulka vlastností (§4.8) — po §3
- [x] regret matrix (§3) včetně vážené ceny a čtení tabulky (§3.1) — kola 2 až 5, 2026-08-22
- [~] trvanlivá vrstva (§4) — hotovo §4.3, §4.4 a §4.5 (kola 1 až 5, 2026-08-22); zbývá §4.1 (přísnost podle M2), §4.2, §4.6, §4.7
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
| **Go** | ✅ `net/http` ve stdlib — žádné druhé okno podpory [R8] | ✅ domovská; vždy křížový překlad [R24] | ❌ ~2 MB dno, 10 MB+ běžně; `wasm_exec.js` vázán na verzi — **nejistá, do M5** [R37] | ❌ chybí v seznamech Sparku i Polars [R44][R45] | **9** |
| **Java** | ✅ Spring Boot; minor ale jen ≥12 měsíců OSS [R31] | 🟡 GraalVM, ale closed-world a JSON metadata [R21] | 🟡 TeaVM (třetí strana); omezení nedoložena [R41] | 🟡 první třída ve Sparku; modelování slabší [R44] | **6** |
| **Kotlin** | ✅ táž cesta jako Java [R31] | 🟡 táž cesta a tytéž výhrady jako Java [R21] | 🟡 Kotlin/Wasm je Beta a klade podmínku na prohlížeč [R36] | 🟡 přes JVM na Java API Sparku (inference) [R44] | **6** |
| **PHP** | ✅ Symfony či Laravel; volba mění okno 4 roky vs. 2 [R28][R29] | 🟡 binárka jen přes projekt třetí strany [R25] | ❌ jen `php-wasm`, fakticky jeden udržovatel — **nejistá, do M5** [R42] | ❌ chybí v seznamech Sparku i Polars [R44][R45] | **12** |
| **Python** | ✅ Django, tři roky na každé vydání [R30] | 🟡 bez křížového překladu [R26] | 🟡 Pyodide zralé, plný přístup k Web API; velikost nedoložena [R38] | ✅ jediný v obou seznamech; referenční ekosystém [R44][R45] | **5** |
| **Rust** | 🟡 u Axumu nenalezen datovaný kalendář podpory; **buňka nejistá**, jde do M5 [R34] | ✅ domovská; Tier 1 napříč OS [R27] | 🟡 evidence úzká (nemaintainovaná kniha WG) — **nejistá, do M5** [R40] | 🟡 implementuje Polars; trénování nezjišťováno [R45] | **7** |
| **TypeScript** | ✅ zralé, ale roztříštěné; Fastify ~rok, Express nenalezeno [R32][R33] | 🟡 Node SEA experimentální; `deno compile` zralé, ale jiný runtime [R22][R23] | ✅ prohlížeč je nativní cíl; jediná nula ve sloupci [R39] | 🟡 Polars přes Node.js, TensorFlow.js [R45][R46] | **4** ⬅ nejnižší |

### 3.1 Jak tabulku číst (k 2026-08-22, prozatímní)

**Prozatímní pořadí podle vážené ceny** (nižší je lepší, rozsah 0 až 30):

| # | Jazyk | Výpočet | Vážená cena |
|---|---|---|---|
| 1. | **TypeScript** | 0×4 + 1×3 + 0×2 + 1×1 | **4** |
| 2. | **Python** | 0×4 + 1×3 + 1×2 + 0×1 | **5** |
| 3.–5. | **C#**, **Java**, **Kotlin** | 0×4 + 1×3 + 1×2 + 1×1 | **6** |
| 6. | **Rust** | 1×4 + 0×3 + 1×2 + 1×1 | **7** |
| 7. | **Go** | 0×4 + 0×3 + 3×2 + 3×1 | **9** |
| 8. | **PHP** | 0×4 + 1×3 + 3×2 + 3×1 | **12** |

**Předpověď z §2.3 se nepotvrdila, a nejde o drobnost.** Psal jsem, že by mělo stoupnout Go. Skončilo sedmé z osmi. Důvod je přesně ten mechanismus, který odhalilo kolo 3: **obě nuly Go leží tam, kde nuly nic nevynášejí.** V backendu má nulu každý, takže se z ní pořadí neposune, a druhá nula je v CLI. Zato dvě ❌ v prohlížeči a v datech se do součtu propíšou plnou vahou. Předpověď selhala proto, že jsem uvažoval o silných stránkách kandidáta místo o rozptylu uvnitř sloupců. Zůstává zapsaná v §2.3 tak, jak byla napsána, a tohle je její vyhodnocení, ne oprava.

**Vyhrává zatím TypeScript, a je to jediný kandidát s nulou tam, kde ji nemá nikdo jiný** (§4.3, prohlížeč). Platí jen v CLI a v datech.

**Tři věci, které to pořadí zatím nesmí učinit verdiktem.**

1. **Vítěz je ten, proti komu v kole 1 vypálila brána B2** (§4.5). Kdyby zadavatel zvolil variantu „nechat pravidlo platit“, byl by dnešní vítěz vyřazen dřív, než se cokoli spočítalo. Citlivost verdiktu na jedno rozhodnutí o pravidle je tím doložená, ne domnělá — a patří do verdiktu jako přiznaný předpoklad.
2. **Čtyři buňky jsou označené jako nejisté** a jdou přednostně do M5: Rust v backendu, Go a PHP v prohlížeči, Rust v prohlížeči. Kdyby ❌ u Go v prohlížeči neobstálo, Go se posouvá z 9 na 7 nebo 5.
3. **Tie-breakery zatím nemají vstup.** Trojice C#, Java a Kotlin je na shodných 6 a rozhodne o ní až §4.1, §4.6 a §4.7 — tedy přísnost vynutitelná v CI, náborový rybník a zralost frameworků.

## 4. Trvanlivá vrstva (nese verdikt)

### 4.1 Přísnost, kterou lze zapnout a vynutit

[OVĚŘIT] — rozklad podle M2 (§2.4) na všech osm kandidátů: běh vs. kontrola, expresivita, nakažlivost neotypovaných závislostí, vynutitelnost v CI a ráčna, cena na zelené louce.

### 4.2 Výkonový strop a model souběžnosti

[OVĚŘIT] — měkká osa (§1), strop popsaný čísly, ne dojmem.

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

**Jazykové vlastnosti**

- [R1] PHP Manual — Property Hooks (verze: zavedeno v PHP 8.4). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

*Nedostupné zdroje:* Oracle Java SE Support Roadmap <https://www.oracle.com/java/technologies/java-se-support-roadmap.html> vrátil 2026-08-22 HTTP 403; Java se proto opírá o [R11][R12].


---

Dokument je datovaný snímek a neaktualizuje se zpětně. Nové poznatky přibývají jako datované sekce na konci; opravy se zapisují jako datované dodatky.
