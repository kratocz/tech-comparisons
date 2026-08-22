# Volba programovacího jazyka: jeden jazyk na dlouhá léta pro nové projekty

- **Verdikt:** ⏳ zatím žádný — rešerše nezačala. Kostra z 2026-08-22 obsahuje kontext (§1) a rozhodovací pravidla (§2), sepsaná PŘED rešerší.
- **Sycené rozhodnutí:** na čem stavět **nové** projekty (vlastní, firemní i cizí) v horizontu let — a čím ta volba argumentovat u někoho, kdo u úvahy nebyl.
- **Fakta ověřena:** ❌ zatím nic. Všechna věcná tvrzení v §3–§5 nesou `[OVĚŘIT]` a jsou zatím prázdná. Jediné ověřené tvrzení k datu založení: property hooks přišly v PHP 8.4 [R1]. Otevřené `[OVĚŘIT]`: celá §3, §4 a §5.
- **Adversariální průchod:** ❌ zatím neproběhl (povinný před verdiktem, §2.4 M5).
- **Jazyk:** 🇨🇿 čeština (originál); 🇬🇧 kanonická anglická verze zatím nevznikla
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## 0. Stav a otevřené úkoly

- [x] kontext (§1) — 2026-08-22
- [x] rozhodovací pravidla (§2) sepsána před rešerší — 2026-08-22
- [x] řádek v kořenovém README — 2026-08-22
- [ ] **potvrdit rozhodovací pravidla (§2) uživatelem** — rešerše nesmí začít dřív
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
- **Čtyři domény, všechny povinné** (§3): webový backend a API; webový frontend v prohlížeči; CLI nástroje, démoni a automatizace; data, ML a dávkové zpracování.
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
| **B1** | ❌ v kterékoli ze čtyř domén (§3) → vyřazen | Přímý důsledek zadání „jeden jazyk, čtyři domény“. Jazyk, který jednu doménu nezvládne, tuhle roli splnit nemůže, ať je jinde jakkoli dobrý. |
| **B2** | Chybí identifikovatelný plátce ekosystému **nebo** doložitelný závazek k dlouhodobé podpoře → vyřazen | Sázka na dekádu potřebuje někoho, kdo ji financuje. Ověřuje se doložitelně (§4.4, §4.5), ne pověstí. |

**Fallback k B1, sepsaný předem:** pokud B1 nepřežije **žádný** kandidát, pravidlo se **nepřepisuje** — zapíše se, že vypálilo a že premisa „jeden jazyk na všechny čtyři domény“ je pro tento kontext nesplnitelná. Verdikt pak zní: nejnižší nejhorší buňka **plus pojmenovaná úniková cesta** pro doménu, kde padl. Tahle věta je tu proto, aby se po výsledcích nevymýšlela.

### 2.3 Agregační pravidlo

Mezi kandidáty, kteří prošli B1 a B2, vyhrává ten s **nejnižší nejhorší buňkou** napříč čtyřmi doménami — ne ten s nejvíc ✅. Jeden jazyk na dlouhá léta se láme na svém nejslabším místě, ne na svém nejsilnějším.

Při shodě rozhodují v tomto **pevně daném pořadí**:

1. přísnost, kterou lze zapnout a **vynutit v CI** (§4.1),
2. velikost náborového rybníka a předatelnost (§4.6),
3. zralost frameworků a knihoven (§4.7).

### 2.4 Metodická pravidla

- **M1 — nejnovější stabilní verze, ale s datem narození.** Hodnotí se aktuální stabilní verze jazyka i frameworků. Každá buňka opřená o mladou vlastnost uvede, **ve které verzi přišla** a **zda ji ekosystém dohnal** (frameworky, ORM, statická analýza). Existence vlastnosti není totéž co její použitelnost; bez tohoto rozlišení by se z poznámek k vydání stal argument.
- **M2 — přísnost se nehodnotí zaškrtávátkem.** Otázka „řeší to typy?“ se rozpadá na pět podotázek a každá má jiného vítěze (§4.1): (a) vynucuje se to za běhu, nebo jen při kontrole; (b) co typový systém vůbec umí vyjádřit; (c) jak nakažlivá je neotypovaná závislost; (d) dá se to vynutit pro všechny v CI a existuje ráčna proti couvání; (e) jaká je cena na zelené louce, kde lze jet přísně od prvního řádku. Rozklad se pouští na **všechny** kandidáty stejně — včetně těch, o kterých se přísnost předpokládá.
- **M3 — každé nosné tvrzení nese `[R…]`.** Tvrzení o neexistenci („nejde“, „neexistuje“, „jen přes“) potřebuje primární zdroj **a** pozitivní kontrolu, že hledání vůbec funguje. Prázdný výsledek hledání není zdroj.
- **M4 — ratingy jsou vázané na tento kontext** (§1) a na nic jiného. Buňka převzatá odjinud je hypotéza, ne fakt.
- **M5 — adversariální průchod je povinný** před verdiktem: samostatný průchod, který se verdikt snaží **vyvrátit**, ne potvrdit. Výsledek se zapisuje do hlavičky.

## 3. Regret matrix: co stojí použít ten který jazyk v té které doméně

Tabulka se **neptá, jak je jazyk v doméně dobrý**. Ptá se: *kolik mě stojí, když v téhle doméně musím použít právě jeho, protože jsem si ho vybral jako svůj jeden jazyk.* Rozdíl je nosný — žebříček nemá poraženého, cena ano.

Symboly: ✅ domovská doména, cena blízko nule · 🟡 použitelné, ale s pojmenovanou cenou · ❌ cena tak vysoká, že bys pro tuhle doménu sáhl po jiném jazyce. Hodnoceno **pro kontext §1** (zelená louka, čtyři povinné domény, výkon jako měkká osa), ne obecně.

| Jazyk | Webový backend a API | Frontend v prohlížeči | CLI a automatizace | Data, ML, dávky | Nejhorší buňka |
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

## 5. Datovaná vrstva (snapshot — rychle zastarává)

[OVĚŘIT] — verze, termíny LTS, stav toolingu. Nenese verdikt.

## 6. Verdikt (zatím žádný)

Rešerše nezačala. Verdikt se doplní podle pravidla §2.3 a až po adversariálním průchodu (§2.4 M5).

## 7. Reference

Ověřeno k 2026-08-22.

- [R1] PHP Manual — Property Hooks (verze: zavedeno v PHP 8.4). Ověřeno 2026-08-22: <https://www.php.net/manual/en/language.oop5.property-hooks.php>

---

Dokument je datovaný snímek a neaktualizuje se zpětně. Nové poznatky přibývají jako datované sekce na konci; opravy se zapisují jako datované dodatky.
