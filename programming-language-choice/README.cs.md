# Volba programovacího jazyka: jeden jazyk na dlouhá léta pro nové projekty

- **Verdikt:** ⏳ zatím žádný — rešerše nezačala. Kostra z 2026-08-22 obsahuje kontext (§1) a rozhodovací pravidla (§2) včetně vah domén a agregace, vše sepsané a potvrzené PŘED rešerší.
- **Sycené rozhodnutí:** na čem stavět **nové** projekty (vlastní, firemní i cizí) v horizontu let — a čím ta volba argumentovat u někoho, kdo u úvahy nebyl.
- **Fakta ověřena:** ❌ zatím nic. Všechna věcná tvrzení v §3–§5 nesou `[OVĚŘIT]` a jsou zatím prázdná. Jediné ověřené tvrzení k datu založení: property hooks přišly v PHP 8.4 [R1]. Otevřené `[OVĚŘIT]`: celá §3, §4 a §5.
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
- [ ] trvanlivá vrstva (§4)
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

### 4.4 Kdo ekosystém platí, licence a governance

[OVĚŘIT] — podklad pro bránu B2.

### 4.5 Historie breaking changes a závazky LTS

[OVĚŘIT] — podklad pro bránu B2.

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

Ověřeno k 2026-08-22.

- [R1] PHP Manual — Property Hooks (verze: zavedeno v PHP 8.4). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

---

Dokument je datovaný snímek a neaktualizuje se zpětně. Nové poznatky přibývají jako datované sekce na konci; opravy se zapisují jako datované dodatky.
