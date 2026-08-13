# Inkrementální replikace mezi dvěma storage clustery: ZFS send/recv vs Ceph mirroring

- **Verdikt:** ⭐ **`zfs send -i`** (orchestrace zreplem *nebo* syncoidem — §12) — platí pro kontext popsaný níže
- **Fakta ověřena:** 2026-08-13 (OpenZFS man pages master, docs.ceph.com latest, Proxmox wiki, zrepl docs, README a issue tracker sanoid/syncoid, dokumentace btrfs-progs a issue tracker btrbk, dokumentace Proxmox Backup Serveru, Red Hat/IBM Ceph docs)
- **Opravy:** §13 (2026-08-13) — hodnocení „min. 3 uzly“ a vyřazující kritérium v §1 byly chybné; jednouzlový Ceph cluster je podporován. Verdikt přežil, ale na jiné argumentaci.
- **Adversariální ověření:** provedeno 2026-08-13 proti verdiktu. Mechanismus **nevyvrátilo** (§2–§8 obstály), ale **vyvrátilo volbu orchestrace**: rozlišovací argument pro zrepl proti syncoidu stál na issues sanoid #304/#528, které jsou zavřené od 2019/2020. §12 byla přepsána tak, aby orchestraci uváděla jako otevřené, těsné rozhodnutí, ne jako uzavřené.
- **Otevřené tagy:** žádné. `[OVĚŘIT]` u sparse oblastí v `cephfs-mirror` byl 2026-08-13 vyřešen ze zdrojového kódu (§5).
- **Poznámka k procesu:** rozhodovací pravidla (§1) byla sepsána 2026-08-13 **po** sběru mechanismových faktů §2–§7, ale **před** volbou orchestrace a verdiktu. Nejde tedy o plnou pre-registraci ve smyslu `AGENTS.md`; uvádím to, aby pravidla nevypadala silněji, než jsou.
- **Jazyk:** 🇨🇿 čeština (originál) · 🇬🇧 [English version](README.md)
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Kontext: pro jaký profil se rozhodovalo

Navazuje na [ZFS vs Ceph](../zfs-vs-ceph/README.cs.md), kde padl verdikt ZFS na Proxmox VE. Tenhle dokument řeší otázku, která z toho vypadla jako další: **jak dostávat změny mezi dvě lokality.** Profil:

- **Dvě lokality**, každá s vlastním clusterem (ne jeden roztažený cluster) — běžné byty spojené rezidenční WAN linkou.
- **Tvrdý měsíční strop na přenesená data** — objem inkrementu není optimalizace, ale rozpočtová položka. Schopnost zjistit velikost přenosu **předem** má vlastní hodnotu.
- **Sólo admin, bez on-call.** Replikace se musí umět sama zvednout po výpadku linky, protože nikdo nebude ve 3 ráno restartovat přenos.
- **Workload:** bulk média/fotky/dokumenty (~150 TiB cíl) + hrst VM disků. Tedy hodně souborů s malou mírou změn, plus několik velkých průběžně přepisovaných obrazů.
- **RPO:** ztráta ~1 minuty až ~1 hodiny je přijatelná. Synchronní replikace přes WAN se nevyžaduje a nikdo ji ani nenabízí.
- **Druhá lokalita je DR cíl, ne aktivní uzel** — na cíl se nezapisuje.

Mimo rozsah: replikace do cloudu (řeší se dedup zálohou, ne replikací), synchronní RPO=0 a sdílené RWX svazky napříč lokalitami.

## Shrnutí (TL;DR)

1. ⭐ **Doporučení: `zfs send -i`.** Pokrývá soubory i bloková zařízení jedním mechanismem, posílá blokovou deltu, umí resumovat přerušený přenos přes resume token a jako jediný z porovnávaných umí říct **přesný objem přenosu předem** (`zfs send -nvP`, §3). Při stropu na data je to rozhodující (§1, §12).
2. **ZFS nerozlišuje soubory a bloky, Ceph ano — a je to ten nejdůležitější strukturální rozdíl** (§2). Dataset i ZVOL jsou pro `send`/`recv` tentýž objekt; naproti tomu CephFS a RBD mají dva nesouvisející démony s **řádově odlišnou granularitou**.
3. **`cephfs-mirror` není send/receive, je to rsync s lepší detekcí změn** (§5). Kopíruje soubory do živého vzdáleného adresáře a teprve pak tam vytvoří snapshot. Změněný soubor se přenáší **celý** a hardlinky se rozpadají na samostatné kopie. Pro velké průběžně měněné soubory je to diskvalifikace.
4. **Atomicita je nejpřehlíženější rozdíl** (§6). `zfs recv` je transakční — cílový dataset je v každém okamžiku nějaký platný minulý stav. U `cephfs-mirror` je konzistentní bod **jen dokončený snapshot**, živý adresář během syncu ne. To patří do DR runbooku, ne do poznámky pod čarou.
5. **RBD je plnohodnotný protějšek ZFS na blokové úrovni** (§7), ale journal mód platí zdvojnásobením latence zápisu a snapshot mód znamená RPO = interval plánu. Navíc: `rbd-mirror` běží na **sekundáru** (pull), `cephfs-mirror` na **primáru** (push) — snadno se to poplete při návrhu firewallu.
6. **Blokový delta přenos má reálný protipřípad** (§8): posílá změněné *bloky*, ne změněný *obsah*. Rewrite in-place, rekomprese nebo databáze přepisující stránky ušpiní obrovské množství bloků a inkrement může být násobně větší než u rsyncu. Pro tenhle workload je to okrajové, ale je to přijatý kompromis, ne neexistující riziko.
7. **Replika bez scrubu a test restore není replika** (§10). Dva ze čtyř historických ZFS bugů v `send` cestě byly tiché ([zfs-vs-ceph §15](../zfs-vs-ceph/README.cs.md)) — checksum je nechytí, protože sedí nad ním.
8. **Přejmenování velkého adresáře je místo, kde se mechanismy rozcházejí nejvíc** (§14). U ZFS jsou to metadata — 100TiB strom přejmenovaný uvnitř datasetu přenese kilobajty. `cephfs-mirror` detekci přejmenování nemá: starý strom na cíli smaže a nový překopíruje celý, čímž je **horší než rsyncová základna**, protože rsync má aspoň `--link-dest` a částečné fuzzy párování, o co se opřít.
9. **Btrfs je nejbližší konkurent a prohrává přesně na dvou řádcích** (§15): nemá resume přerušeného přenosu a neumí ho předem ocenit. Obojí je tu rozhodovací pravidlo, takže vypadává — ale je to jediný mechanismus, který kóduje přejmenování **jako** přejmenování, a stávající DR bedna na něm dnes běží. Praktický důsledek: **ta bedna by měla být přestavěna na ZFS**, protože replikace nepřechází mezi enginy (§8).
10. **PBS je doplněk, ne konkurent** (§16). Vyhrává naplno na třech řádcích — AES-256-GCM na klientu, takže druhý konec nikdy nedrží klíč, vestavěné verify joby (disciplína, kterou žádá §10) a obsahově adresované chunky, díky nimž jsou přejmenování i rewrite in-place zdarma. Verdikt nebere proto, že jeho cílem je datastore: zotavení znamená obnovu, a to je u ~150 TiB na dny. **Provozovat obojí** — replika přes `send`/`recv` není záloha a datastore PBS není failover cíl.

## Srovnání v přehledu

Symboly: ✅ silná stránka · 🟡 funguje s výhradami / kompromis · ❌ slabina nebo chybí · — nedává smysl. Hodnoceno **pro tento kontext** (dvě lokality, asymetrická rezidenční WAN se stropem na data, sólo admin, bulk média + hrst VM disků, DR cíl bez zápisu) — ne obecně; na symetrické DC lince s tučnou kapacitou by řada řádků dopadla jinak. První dva sloupce jsou dva serializátory na úrovni filesystému, prostřední dva jsou dva Ceph démoni a poslední dva jsou engine-neutrální — rsync jako základna kopírování souborů a Proxmox Backup Server, který odpovídá na **jinou otázku** (obnova do bodu v čase, ne stav, na který jde přepnout) a je zařazen s tímhle vědomím (§16).

| Kritérium | ZFS `send`/`recv` | Btrfs `send`/`receive` | Ceph RBD mirror | CephFS mirror | rsync / rclone | Proxmox Backup Server |
|---|---|---|---|---|---|---|
| **▸ Jak vzniká delta** | | | | | | |
| Jednotka přenosu | ✅ blok (`recordsize`/`volblocksize`) | ✅ extent (`WRITE`/`CLONE`) | ✅ objekt / extent | ❌ **celý změněný soubor** | 🟡 rolling-checksum delta | ✅ chunk (4 MiB fixní / dynamický rolling-hash) |
| Nalezení změn bez procházení stromu | ✅ birth time v CoW stromu | ✅ generation numbers | ✅ object-map + fast-diff | ✅ snapdiff (od Reefu, §11) | ❌ stat každého souboru | 🟡 VM: dirty bitmap · soubory: průchod metadat |
| Cena detekce roste s | ✅ objemem změn | ✅ objemem změn | ✅ počtem objektů (z in-memory mapy) | 🟡 počtem změněných souborů | ❌ **počtem souborů celkem** | ❌ **objemem čtených dat lokálně** (metadata mód: počtem souborů) |
| Serializace stavu FS vs kopie přes POSIX | ✅ stav FS (díry, komprese, properties) | ✅ instrukční stream vědomý si FS | ✅ bloky (POSIX se neúčastní) | ❌ POSIX kopie → **hardlinky se rozpadnou** | ❌ POSIX kopie | ❌ POSIX čtení → obsahově adresované chunky |
| Přejmenování/přesun velkého stromu (§14) | ✅ jen metadata (uvnitř datasetu) | ✅ explicitní příkaz `RENAME` | ✅ neviditelné — metadata hostovaného FS | ❌ **smazání + plná znovukopie** | ❌ smazání + znovupřenos (`--fuzzy` na adresáře nestačí) | ✅ chunky se jen znovu odkážou, nepřenášejí |
| **▸ Atomicita a konzistence** (§6) | | | | | | |
| Cíl je vždy platný minulý stav | ✅ transakční `recv` | 🟡 starší snapshoty netknuté; rozpracovaný subvolume je zvlášť | ✅ delta se aplikuje celá, nebo rollback | ❌ živý adresář je během syncu směs | ❌ | ✅ dokončené snapshoty jsou neměnné |
| Konzistentní bod po pádu v půlce | ✅ poslední přijatý snapshot | 🟡 poslední dokončený (read-only) subvolume; ten částečný zůstane ležet | ✅ poslední mirror-snapshot | 🟡 poslední **dokončený** snapshot na cíli | ❌ žádný | ✅ poslední dokončený snapshot |
| Resume po přerušení linky | ✅ resume token (`recv -s`) | ❌ **žádné — od nuly** | 🟡 démon pokračuje sám; DIY `export-diff` ne | 🟡 démon pokračuje sám (po souborech) | 🟡 `--partial` | 🟡 bez tokenu, ale opakování pošle jen chybějící chunky |
| **▸ Linka a rozpočet** | | | | | | |
| **Odhad objemu přenosu předem** | ✅ `zfs send -nvP` (přesně) | ❌ dry-run neexistuje | ✅ `rbd diff --format json` (součet extentů) | ❌ není | ❌ `--dry-run` dá jen seznam | ❌ ne |
| Komprese na drátě | ✅ `-c` posílá bloky komprimované z disku | ✅ `--compressed-data` (Linux 6.0+) | 🟡 externí (ssh `-C`) | 🟡 externí | ✅ `-z` | ✅ zstd po chuncích, na klientu |
| Přenos bez klíče na cílové straně | ✅ `send -w` (raw) | ❌ nemá nativní šifrování | ❌ | ❌ | ❌ | ✅ **AES-256-GCM na klientu** |
| Omezení šířky pásma | ✅ zrepl / `pv` / `mbuffer` | ✅ `pv` / `mbuffer` | 🟡 konfigurace démona | 🟡 konfigurace démona | ✅ `--bwlimit` | 🟡 traffic control — sync joby ale chtějí vlastní `rate-in` (§16) |
| **▸ Provoz** | | | | | | |
| Nutný démon | ✅ žádný (nebo zrepl) | ✅ žádný (nebo btrbk) | ❌ `rbd-mirror` | ❌ `cephfs-mirror` | ✅ žádný | ❌ instance PBS na obou stranách |
| Kde démon běží / směr | ✅ push i pull | ✅ push i pull | 🟡 **sekundár** (pull) | 🟡 **primár** (push) | ✅ oboje | 🟡 sync job: pull nebo push |
| Obousměrně / failback | 🟡 ruční prohození rolí | 🟡 ruční prohození rolí | ✅ promote/demote, two-way | ❌ jednosměrně, **jediný peer** | 🟡 ruční | ❌ **obnova, ne failover** (§16) |
| Min. počet uzlů na cíli | ✅ **1** | ✅ **1** | 🟡 1 podporován, ne pro produkci (§13) | 🟡 1, navíc caveat kernel klienta (§13) | ✅ 1 | ✅ **1** |
| **▸ Vhodnost pro workload** | | | | | | |
| Velké průběžně měněné soubory (VM, DB) | ✅ | 🟡 jen soubory — nemá ekvivalent ZVOL (§15) | ✅ | ❌ přenese celý soubor | 🟡 delta ano, ale čte celý soubor | ✅ dirty bitmap, dokud VM běží |
| Miliony malých souborů, málo změn | ✅ | ✅ | — | ✅ | ❌ walk dominuje nad přenosem | 🟡 metadata mód se vyhne opětovnému čtení |
| Rewrite in-place / rekomprese (§8) | ❌ pošle všechny ušpiněné bloky | ❌ pošle každý změněný extent | ❌ dtto | ✅ pošle jen změněné soubory | ✅ pošle jen změněný obsah | ✅ obsahově adresované — shodný obsah se zdeduplikuje |
| Zapisovatelný / RWX cíl | ❌ cíl musí být `readonly` | ❌ přijatý subvolume je read-only | ❌ | ✅ (ale nemá se) | ✅ | ❌ datastore; musíš obnovovat |
| Podmnožina datasetu / jiný layout na cíli | ❌ celý dataset | ❌ celý subvolume | ❌ celý image | ✅ per adresář | ✅ libovolně | ✅ libovolně |
| Přenos mezi různými enginy | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ **nezávislé na enginu** |

**Jak to číst.** Sloupec PBS čti nejdřív proti §16: je to zálohovací systém, takže jeho ❌ u obousměrného failbacku je konstatování kategorie, ne vada — zatímco jeho ✅ u šifrování na klientu, nezávislosti na enginu a ceny přejmenování jsou řádky, kde skutečně poráží každý replikační mechanismus tady. Btrfs (§15) je v tabulce nejblíž ZFS a je nejostřejší zkouškou verdiktu: stejná třída mechanismu, srovnatelná granularita a jediný sloupec, který reprezentuje přejmenování **jako** přejmenování. Prohrává tu na dvou ze čtyř rozhodovacích pravidel — chybí resume a chybí odhad objemu —, což je přesně ta dvojice, na které tenhle kontext stojí. ZFS vyhrává všude, kde se ptáme „kolik dat poteče a co se stane, když spadne linka“ — bloková granularita, přesný odhad předem, transakční příjem a resume token. RBD je jeho rovnocenný protějšek na blokové úrovni a v jedné věci ho poráží (nativní obousměrný failover s promote/demote), platí za to ale třemi uzly na cílové straně a povinným démonem. CephFS mirror vyhrává jen tam, kde ostatní nemohou — sdílený zapisovatelný filesystém a replikace po adresářích místo po celých datasetech — a prohrává na granularitě, atomicitě i na hardlincích. rsync je poslední sloupec ne proto, že by byl špatný, ale proto, že je jediný, který zvládne to, co ostatní neumí vůbec: **změnu enginu, změnu layoutu a podmnožinu** — a v jednom scénáři (§8) porazí všechny ostatní.

## 1. Rozhodovací pravidla (2026-08-13)

Sepsáno před volbou nástroje a verdiktu (viz poznámka k procesu v hlavičce). Vybraný mechanismus musí splnit všechny čtyři body:

1. **Rozpočet na data je zjistitelný předem.** Musí existovat způsob, jak před spuštěním přenosu zjistit jeho velikost s chybou do ~10 %. Bez toho nelze provozovat linku s tvrdým měsíčním stropem, protože jediná rekomprese datasetu ho vyčerpá.
2. **Přerušení linky nesmí znamenat přenos od nuly.** Rezidenční WAN vypadává; přenos v řádu TiB, který po výpadku začíná znovu, nikdy nedoběhne.
3. **Cílová strana má být kdykoliv použitelná jako DR bod, bez ručního posuzování.** „Podívej se, jestli to doběhlo“ není operace, kterou chci dělat v krizi.
4. **Jeden mechanismus pro soubory i VM disky.** Dvě replikační roury se dvěma sadami selhání a dvěma runbooky jsou u sólo admina větší riziko než cokoliv, co ušetří.

**Vyřazující kritérium:** cokoliv, co vyžaduje ≥3 uzly na cílové straně, je mimo — druhá lokalita startuje jako jeden stroj. *(Čteno zpětně: toto pravidlo **nezabralo** — jednouzlový Ceph cluster je podporován. Viz oprava v §13; pravidlo zůstává, jak bylo napsáno, místo aby bylo přepsáno na míru výsledku.)*

## 2. Strukturální asymetrie: ZFS má jeden mechanismus, Ceph dva

Nejužitečnější věc na téhle otázce se ukáže hned na začátku: **čtyři případy se nerozpadají na čtyři odpovědi, ale na dvě dvojice.**

Pro ZFS je *filesystem dataset* i *ZVOL* tentýž objekt. Replikační vrstva vůbec nesahá na to, co je uvnitř — pracuje se stromem bloků a jejich birth time, ne se soubory. `zfs send` na dataset s milionem fotek a `zfs send` na ZVOL s diskem virtuálu je doslova stejný příkaz se stejnými přepínači a stejnou sémantikou. Otázky „jak replikovat soubory“ a „jak replikovat bloková zařízení“ v ZFS **nejsou dvě otázky**.

Ceph je opačný případ. CephFS a RBD jsou dva nezávislé produkty nad stejným RADOS a mají dva samostatné mirroring démony, které spolu nemají nic společného kromě jména. Liší se směrem (push vs pull), stranou, na které běží, granularitou přenosu, atomicitou i tím, co se stane při pádu. Kdo si zvykne na `rbd-mirror`, nemá o `cephfs-mirror` naučeno nic.

Tenhle rozdíl je **durable** — plyne z architektury, ne z verze. ZFS je jeden filesystém s jedním serializačním formátem; Ceph je sada služeb nad sdíleným objektovým úložištěm, kde každá služba řeší replikaci na své vrstvě.

## 3. ZFS `send`/`recv` — jak vzniká delta

Základní smyčka je pro soubory i bloky identická:

```bash
# zdroj
zfs snapshot -r tank/data@2026-08-13          # -r je atomické napříč poolem
zfs send -w -c -i @2026-08-12 tank/data@2026-08-13 \
  | ssh dr zfs recv -s -F backup/data
```

Delta se nepočítá porovnáváním — vyplývá z CoW stromu. Každý blok nese *birth time* (transaction group, ve které vznikl), takže „co se změnilo od snapshotu X“ je otázka na metadata, ne na obsah. Náklad je tedy úměrný **objemu změn**, ne počtu souborů ani velikosti datasetu. Dataset s deseti miliony souborů a jednou změněnou fotkou pošle tu fotku a nic víc; rsync by ho musel celý projít.

Přepínače, na kterých záleží:

- **`-i` vs `-I`** — `-i` pošle deltu mezi dvěma snapshoty, `-I` včetně všech mezilehlých. `-I` zachová na cíli celou retenci, což je pro DR obvykle to, co chceš.
- **`-c`** generuje kompaktnější stream tím, že posílá bloky už zkomprimované tak, jak leží na disku. Šetří CPU i linku a data zůstávají komprimovaná i na příjmu.
- **`-w` / `--raw`** posílá data přesně tak, jak jsou na disku — u šifrovaných datasetů to znamená **cíl nepotřebuje klíč**. Pro nešifrované je `-w` ekvivalent `-Lec`.
- **`-s` na příjmu** ukládá částečně přijatý stav místo jeho zahození a vystaví `receive_resume_token`. Bez toho se přerušený přenos zahazuje (§6).
- **`-i` bere i bookmark.** `zfs bookmark tank/data@old tank/data#old` vytvoří kotvu, která přežije smazání zdrojového snapshotu — uvolníš místo na zdroji, aniž bys přerušil řetěz.

Resume po výpadku:

```bash
# cíl:   zfs get -H -o value receive_resume_token backup/data
# zdroj: zfs send -t <token> | ssh dr zfs recv -s backup/data
```

A pro rozhodovací pravidlo č. 1 to podstatné — **odhad objemu předem**:

```bash
zfs send -nvP -i @2026-08-12 tank/data@2026-08-13
```

`-n` je dry run (nevygeneruje žádná data), `-P` strojově čitelný výstup. Dostaneš velikost streamu dřív, než z měsíčního stropu ubude první bajt. Žádný z ostatních mechanismů kromě RBD (§7) tohle neumí.

**Provozní pasti.** Cílový dataset musí mít jako poslední snapshot přesně ten, ze kterého inkrement vychází — man page to říká jednoznačně: *"the destination file system must already exist, and its most recent snapshot must match the incremental stream's source"*. Proto na cíl patří `readonly=on` (`zfs recv` funguje dál, uživatelské zápisy ne) a na kotevní snapshoty `zfs hold`, aby je nesmetl retenční skript. Bez toho tě čeká `recv -F` rollback, nebo v horším případě full resend.

## 4. Soubory vs ZVOL: kde je rozdíl doopravdy

Mechanika je stejná, liší se dvě věci — a ani jedna z nich není o replikaci.

**Konzistence.** Snapshot ZVOLu je crash-consistent: odpovídá tomu, co by na disku zbylo po výpadku proudu. Pro VM disk to obvykle stačí (žurnálovaný FS se zvedne), pro databázi uvnitř VM ne. Aplikačně konzistentní snapshot vyžaduje quiescnutí hosta — `qemu-guest-agent` fsfreeze, což na Proxmoxu obstará `qm snapshot`. Replikační vrstva o tom neví a nemá jak.

**Granularita.** `volblocksize` (default 16K v OpenZFS 2.2+) určuje, jak velký blok ušpiní jeden zápis hosta. 4KB zápis do ZVOLu se 16K volblocksize znamená 16 KB v inkrementu. U datasetů totéž dělá `recordsize`, ale tam se velikost přizpůsobuje souboru, takže se to projeví méně. Pro VM disky, kde jde o random write, to je čtyřnásobek objemu — a při stropu na data to je viditelná položka.

## 5. CephFS mirroring: rsync s lepší detekcí změn

```bash
# na sekundárním clusteru
ceph fs snapshot mirror peer_bootstrap create backup_fs client.mirror_remote site-remote

# na primárním
ceph mgr module enable mirroring
ceph fs snapshot mirror enable cephfs
ceph fs snapshot mirror peer_bootstrap import cephfs <token>
ceph fs snapshot mirror add cephfs /d0/d1/d2

mkdir -p /d0/d1/d2/.snap/snap1     # snapshot si vytváříš sám; démon ho jen synchronizuje
```

Démon běží na **primárním** clusteru, obě strany mountuje přes libcephfs a **pushuje**. Od Reefu používá snapdiff API (§11): *"For a given snapshot pair in a directory, cephfs-mirror daemon will rely on CephFS Snapdiff Feature to identify changes in a directory tree."* Neprochází tedy strom — dostane rovnou seznam změněných souborů.

Tím ale výhody končí, protože **jednotkou přenosu zůstává soubor**: *"The diffs are applied to directory in the remote file system thereby only synchronizing files that have changed between two snapshots"* a *"snapshot data is synchronized by bulk copying to the remote filesystem"*. Změníš 4 KB uprostřed 500GB obrazu → přenese se 500 GB. To dělá z CephFS mirroringu použitelný nástroj pro dokumenty a fotky a **nepoužitelný** pro cokoliv velkého a průběžně přepisovaného.

Druhý následek toho, že se kopíruje **přes POSIX API** místo serializace stavu filesystému: **hardlinky se nepřenášejí jako hardlinky.** Red Hat i IBM to dokumentují shodně — *"Synchronizing hard links is not supported; hard linked files get synchronized as regular files."* Tři hardlinky na jeden 10GB soubor zaberou na zdroji 10 GB a na cíli 30 GB, a přenesou se pokaždé znovu. Mirrorují se navíc jen regular files, adresáře a symlinky; ostatní typy se ignorují. `zfs send` tuhle třídu problémů mít nemůže, protože neposílá soubory, ale bloky a metadata.

**Sparse oblasti se nezachovávají — řídký soubor se přenese v nominální velikosti.** Dokumentace to neříká tak ani tak, takže odpověď je vyčtená ze zdrojáku (vyřešeno 2026-08-13). `PeerReplayer::copy_to_remote()` prochází soubor přes `ceph_preadv`/`ceph_pwritev` od offsetu 0 do konce po pevných iovec dávkách a nikde ve smyčce není krok `SEEK_HOLE`/`SEEK_DATA`; jediné volání týkající se velikosti je `ceph_ftruncate(m_remote_mount, r_fd, stx.stx_size)`. Díry se tedy přečtou jako nuly a jako nuly se na cíl zapíší.

Není to opomenutí démona a samo v něm ani opravit nejde: **CephFS alokaci vůbec nesleduje.** Jeho vlastní stránka o odchylkách od POSIXu říká *"Because CephFS does not explicitly track which parts of a file are allocated/written, the st_blocks field is always populated by the file size divided by the block size"* a *"Sparse files propagate incorrectly to the stat(2) st_blocks field."* Smyčka přeskakující díry nemá koho se zeptat.

Praktický důsledek: 1TiB řídký obraz s 1 GiB skutečných dat pošle po lince ~1 TiB — a protože granularita je po souborech, pošle ho celý znovu pokaždé, když se v něm cokoliv změní. Řídké obrazy VM a CephFS mirroring k sobě nepatří, a to ze dvou nezávislých důvodů naráz. `zfs send` se to netýká: díra je nepřítomný blok ve stromu, takže není co serializovat.

Další doložená omezení: **jediný peer**, **jednosměrně** (failback je ruční) a snap-schedule na vzdáleném FS pro mirrorované adresáře rozbije metadata (*"will cause … errors like `invalid metadata`"*).

## 6. Jednotka přenosu a atomicita: nejpřehlíženější rozdíl

„Mirroring snapshotů“ zní u ZFS i u CephFS stejně, ale znamená to dvě různé věci — a rozdíl se projeví přesně v okamžiku, kdy na tom záleží nejvíc, tedy když přenos spadne v půlce.

**ZFS: serializace stavu, transakční příjem.** `zfs send` vytvoří **stream** — serializovaný stav filesystému, ne sadu souborů. `zfs recv` ho aplikuje jako transakci. Bez `-s` se částečně přijatý stav zahodí; man page to říká z opačné strany, ale jednoznačně: `-s` znamená *"If the receive is interrupted, save the partially received state, rather than deleting it."* Důsledek: **cílový dataset je v každém okamžiku nějaký platný minulý snapshot.** Nikdy není směsí. (`btrfs send`/`receive` patří do stejné třídy — serializace stavu FS, ne kopie souborů.)

**CephFS: kopie do živého adresáře, snapshot až potom.** Dokumentace popisuje pořadí doslova: *"Snapshots are synchronized by transferring snapshot data to the remote file system **and by creating a snapshot with the same name** as the snapshot being synchronized."* Nejdřív se soubory nakopírují do **živého** vzdáleného adresáře, teprve po dokončení tam vznikne snapshot. Mezi tím je adresář směsí starých a nových souborů.

Proto dokumentace trvá na *"Treat the remote filesystem as read-only. Nothing is inherently enforced by CephFS."* Není to hygienické doporučení — je to důsledek toho, že v půlce syncu tam prostě není platný stav.

**Co si z toho odnést do runbooku:** na CephFS DR lokalitě není tvým obnovovacím bodem to, co leží v adresáři, ale **poslední dokončený snapshot**. Na ZFS DR lokalitě je obnovovacím bodem sám dataset. To je rozdíl mezi „obnovím“ a „nejdřív musím zjistit, co je platné“.

Restart démona se z přerušení zvedne (*"Internal blocklist/failure restarts of a mirror instance preserve omap so sync can resume"*) a co už bylo synchronizováno si pamatuje přes **snap-id** v `SnapInfo` na MDS, ne přes jméno — takže smazání a znovuvytvoření snapshotu stejného jména démona nezmate.

## 7. Ceph RBD: plnohodnotný blokový protějšek

Tři cesty, všechny blokové.

**A) `rbd-mirror`, snapshot-based** (od Octopusu, §11) — periodické mirror-snapshoty, ze kterých se spočte delta: *"determine any data or metadata updates between two mirror-snapshots and copy the deltas to its local copy."* Bez zápisové penalizace, RPO = interval plánu.

```bash
rbd mirror pool enable <pool> image
rbd mirror pool peer bootstrap create --site-name A <pool> > token   # import na B
rbd mirror image enable <pool>/<img> snapshot
rbd mirror snapshot schedule add --pool <pool> --image <img> 15m
```

**B) `rbd-mirror`, journal-based** (od Jewel) — *"Every write to the RBD image is first recorded to the associated journal before modifying the actual image."* Jemnější RPO, ale každý zápis se zapisuje dvakrát a **latence se prakticky zdvojnásobí**. Vyžaduje feature `journaling`, která závisí na `exclusive-lock`. Pro WAN scénář to nedává smysl; je to nástroj pro DC-to-DC s tučnou linkou.

**C) DIY bez démona** — přímý protějšek `zfs send -i`:

```bash
rbd snap create pool/img@2026-08-13
rbd export-diff --from-snap 2026-08-12 pool/img@2026-08-13 - \
  | ssh dr rbd import-diff - pool/img
```

`merge-diff` umí slepit navazující diffy do jednoho. Odhad objemu předem: `rbd diff --from-snap snap1 pool/img@snap2 --format json` a sečíst extenty. **Podmínka rozumného výkonu je `object-map` + `fast-diff`** — s nimi se delta počítá z in-memory object mapy místo dotazu na RADOS pro každý objekt zvlášť.

**Kde démon běží.** Pro jednosměrnou replikaci *"the rbd-mirror daemon runs only on the secondary cluster"* — tedy **pull**, opačně než `cephfs-mirror`. Démon musí mít současně konektivitu na **oba** clustery, na všechny monitory i OSD hosty. To je netriviální požadavek na firewall a routing mezi lokalitami a je dobré ho vědět před návrhem sítě, ne po něm.

## 8. Kde blokový delta přenos prohrává

Protiargument, který dokument potřebuje, aby nebyl reklamou: `zfs send -i` i `rbd export-diff` posílají **změněné bloky**, ne **změněný obsah**. Ve chvíli, kdy se data přepisují na místě beze změny logického obsahu — defragmentace, rekomprese datasetu po změně `compression`, databáze přepisující stránky, rebalance —, ušpiní se obrovské množství bloků a inkrement je násobně větší, než co by přenesl rsync s rolling checksumem. Souborová replikace v tomhle jediném scénáři blokovou poráží, a to výrazně.

Obecné pravidlo: **blokový delta přenos vyhrává na „hodně souborů, málo změn“, prohrává na „málo souborů, hodně CoW churnu“**.

Druhá hranice je tvrdší: `send`/`recv` ani `rbd-mirror` **neumí přenášet mezi enginy, měnit layout ani vybrat podmnožinu**. ZFS → Ceph, jiná struktura na cíli, zapisovatelný cíl, replikace jen jednoho podadresáře → tam pořád patří rsync/rclone, nebo rovnou dedup záloha (Kopia, restic, borg, PBS) místo replikace. Replikace a záloha nejsou totéž a tenhle dokument řeší jen tu první.

## 9. Orchestrace: co doopravdy točí smyčku

`zfs send` je primitivum, ne řešení — snapshoty, retenci, retry a resume musí někdo řídit.

| Nástroj | Rozsah | Poznámka |
|---|---|---|
| **zrepl** | dva samostatné stroje | Dohlížený démon — retry a hlášení stavu má vestavěné. Push i pull, resumovatelný přenos, replikační kurzor jako bookmark, pruning policy. Transporty: `tcp` (**nešifrovaný**), `tls` (klientské certifikáty, CN = identita), `ssh+stdinserver` (méně efektivní, ale nevystavuje démona do internetu), `local`. Cena: vlastní konfigurační jazyk a u `tls` správa certifikátů. |
| **syncoid** (sanoid) | dva stroje přes SSH | Skript spouštěný z cronu, ne démon. Resume podporuje a zapíná automaticky od 1.4.18; dále `--create-bookmark`, `--source-bwlimit`/`--target-bwlimit` a promazávání na cíli přes `--delete-target-snapshots`. Tvorbu snapshotů a retenci na zdroji řeší sanoid. Zbytková mezera: když selže samotný pokus o resume, neumí se sám přepnout na přenos bez resume ([#672](https://github.com/jimsalterjrs/sanoid/issues/672), otevřené od 2021). Detekce selhání je na provozovateli — cron skript, který přestal běžet, mlčí. |
| **pve-zsync** | dva **samostatné** Proxmox hosty | Přes SSH, **nevyžaduje členství v clusteru**. Push i pull, default interval 15 min přes cron. Přesně profil „dvě lokality, dva clustery“. |
| **pvesr** | uzly **téhož** Proxmox clusteru | ❗ **Nepoužitelné pro tenhle případ.** Minimální interval 1 min, ale funguje jen uvnitř jednoho clusteru. Snadná záměna s `pve-zsync`. |

Pro dvě lokality s vlastními clustery tedy `pvesr` odpadá bez ohledu na to, jak dobře funguje uvnitř clusteru — a to je nejčastější omyl při návrhu tohoto scénáře.

## 10. Ověření: replika, kterou jsi neproscrubboval, není replika

Tohle platí pro všechny čtyři mechanismy a je to jediná sekce, kterou by bylo chybou přeskočit.

Z [zfs-vs-ceph §15](../zfs-vs-ceph/README.cs.md) plyne, že **dva ze čtyř historických ZFS korupčních bugů v `send` cestě byly tiché** — `hole_birth` (2016) i encryption `send`/`recv` (#12014, uzavřeno 2025). Checksum je nechytí, protože bug sedí nad vrstvou, která checksumy počítá: příjemce nehlásí chybu a přesto cíl ≠ zdroj. Rizika ZFS sedí historicky právě v `send` cestách a v čerstvě dodaných funkcích, ne v jádru zápisu.

Z toho plyne minimum bez ohledu na zvolený nástroj: **pravidelný scrub na cílové straně**, **test restore** (ne „zkontroluj, že soubor existuje“, ale skutečné nabootování VM nebo porovnání checksumů) a u ZFS **nechodit do `.zfs` na přijímací straně během běžícího `recv`** — deadlock #18073, oprava až v 5/2026.

## 11. Datovaný snímek: verze a dostupnost funkcí (2026-08-13)

Tahle sekce je jediná perishable část dokumentu. Až zestárne, závěry §2–§10 platí dál.

| Funkce | Od verze | Poznámka |
|---|---|---|
| `zfs send -s` / resume token | OpenZFS (`extensible_dataset`) | Vyžaduje pool feature na obou stranách |
| `zfs send -w` (raw) | OpenZFS | Korupční bugy nad šifrovanými datasety uzavřeny až 2025 (#12014) |
| RBD journal-based mirroring | Ceph **Jewel** | Zdvojnásobení latence zápisu |
| RBD snapshot-based mirroring | Ceph **Octopus (v15)** | Bez zápisové penalizace |
| `cephfs-mirror` | Ceph **Pacific (v16)** | Obě strany musí být Pacific nebo novější |
| CephFS snapdiff | Ceph **Reef (v18)**, PR #53229 | Bez něj `cephfs-mirror` prochází strom |
| `cephfs-mirror` používá snapdiff API | Ceph **Squid (v19)**, PR #58984 | Tj. plná efektivita detekce až tady |

**Stav vydání Ceph k 2026-08-13:** aktivní jsou **Tentacle (v20.2)** — doporučená pro nová nasazení, poslední vydání v20.2.3 z 2026-08-05 — a **Squid (v19.2)**, podpora do 9/2026. Reef je před koncem podpory. Pro `cephfs-mirror` to znamená, že plně efektivní varianta (snapdiff API) je dostupná ve všech aktivně podporovaných řadách.

## 12. Verdikt

⭐ **Mechanismus: `zfs send -i`.** To je to, co analýza podporuje — a podporuje to silně.

Proti rozhodovacím pravidlům z §1:

1. **Rozpočet předem** ✅ — `zfs send -nvP` dá přesnou velikost streamu. Jediná alternativa se stejnou schopností je RBD (`rbd diff`), která padá na pravidle o počtu uzlů.
2. **Přerušení neznamená restart od nuly** ✅ — `recv -s` + resume token, a zrepl to řídí sám bez zásahu.
3. **Cíl je kdykoliv platný DR bod** ✅ — transakční `recv` (§6). U `cephfs-mirror` by tohle pravidlo padlo.
4. **Jeden mechanismus pro soubory i VM disky** ✅ — přímý důsledek §2; žádná Ceph varianta to nesplní ani teoreticky.

**Vyřazující kritérium nezabralo** — jednouzlový Ceph cluster je upstreamem explicitně podporován, takže obě Ceph varianty bylo nutné porazit na jejich vlastních kvalitách: CephFS mirror na pravidlech 1, 3 a 4, RBD mirror na pravidle 4. Úplná oprava a to, co o jednouzlovém cíli platí doopravdy, jsou v §13.

**Volba orchestrace je mnohem těsnější a tahle analýza ji nerozhoduje.** Dřívější verze doporučovala rovnou zrepl; adversariální průchod tu úvahu zabil, protože argument o robustnosti resume popisoval stav sanoidu z let 2018–2020 (issues [#304](https://github.com/jimsalterjrs/sanoid/issues/304), [#528](https://github.com/jimsalterjrs/sanoid/issues/528), obě zavřené), ne dnešek. Ověřeno k 2026-08-13: syncoid resumuje automaticky, umí bookmarky, limity pásma i promazávání na cíli — na všech čtyřech rozhodovacích pravidlech jsou tedy rovnocenné. Skutečně je odlišuje kompromis, který kontext tahá na obě strany současně: zrepl je **dohlížený démon**, takže na otázku „proběhla dneska v noci replikace?“ se dá odpovědět bez dalšího lešení — což při absenci on-callu váží; syncoid je **řádek v cronu**, tedy míň provozu a míň příležitostí ke špatné konfiguraci — což váží u sólo admina, který cení jednoduchost. **Zvol zrepl, pokud chceš detekci selhání v ceně; zvol syncoid, pokud už provozuješ monitoring, který si mlčícího cronu všimne.** §1 splní obojí. Ať padne cokoliv, nepoužívej u zreplu transport `tcp` — je nešifrovaný.

**Vědomě přijaté kompromisy:**

- **Žádný nativní failback.** Prohození roli je ruční, zatímco RBD má promote/demote. Pro DR lokalitu, na kterou se nezapisuje, je to přijatelné; kdyby se z ní stal aktivní uzel, tenhle bod se otevírá znovu.
- **Křehkost řetězu.** Jeden smazaný kotevní snapshot = full resend. Mitigace jsou levné (bookmarky, `zfs hold`, `readonly=on` na cíli), ale musí být nasazené od začátku, ne po prvním incidentu.
- **CoW churn** (§8) může jednorázově vystřelit objem přenosu. Pro bulk média okrajové; před plánovanou rekompresí nebo změnou `recordsize` je ale nutné počítat s tím, že se přenese znovu prakticky všechno.
- **Celý dataset, nebo nic.** Nelze replikovat podmnožinu → **návrh datasetů se stává návrhem replikace**. To je rozhodnutí, které se dělá jednou a špatně se mění.
- **Šifrování:** při volbě LUKS (viz [zfs-vs-ceph §12](../zfs-vs-ceph/README.cs.md)) je `send -w` bezpředmětné — stream nese plaintextové ZFS bloky a důvěrnost na drátě stojí a padá s transportem. DR lokalita tedy potřebuje vlastní LUKS + Tang, ne jen disk.

**Změním názor, pokud:** (a) druhá lokalita bude potřebovat sdílený RWX filesystém replikovaný mezi lokalitami — tam ZFS nemá co nabídnout a i slabší `cephfs-mirror` je lepší než nic; (b) objem denní změny klesne tak nízko, že rozdíl mezi souborovou a blokovou granularitou zmizí v šumu linky, čímž zmizí hlavní argument; (c) DR lokalita se stane aktivním zapisujícím uzlem, čímž se ruční failback změní z nepohodlí v riziko.

## 13. Oprava (2026-08-13): cíl na jednom uzlu

**Původní vyřazující kritérium v §1 a hodnocení „min. 3 uzly“ byly chybné.** Opraveno tentýž den, kdy dokument vyšel, poté co je čtenář zpochybnil. Níže je opravená pozice; pravidlo v §1 zůstává, jak bylo napsáno, protože rozhodovací pravidlo přepsané po zhlédnutí výsledku už není rozhodovací pravidlo (čte se tedy nově jako: *pravidlo nezabralo*).

**Fakt: jednouzlový Ceph cluster je upstreamem explicitně podporován.** cephadm na to má vlastní přepínač — *"To deploy a Ceph cluster running on a single host, use the `--single-host-defaults` flag when bootstrapping."* Nastaví tři volby:

```
global/osd_crush_chooseleaf_type = 0     # failure domain klesá z hostu na OSD
global/osd_pool_default_size     = 2
mgr/mgr_standby_modules          = False
```

Upstream k tomu jedním dechem dodává výhradu: *"such clusters are generally not suitable for production."* Ta věta není podpůrné odmítnutí odpovědnosti ani varování před nezralostí kódu — **důvodem je sám ten přepínač**, protože každá ze tří voleb, které nastaví, odevzdává něco, kvůli čemu Ceph existuje:

- `osd_crush_chooseleaf_type = 0` přesouvá failure domain z hostu na OSD, takže obě repliky mohou přistát na témže stroji. Cluster přestává přežívat ztrátu hostu — což je jediná vlastnost, kterou se Ceph liší od lokálního úložiště.
- `osd_pool_default_size = 2` půlí default. Vlastní dokumentace poolů to říká natvrdo: *"setting `size` to `2` or `min_size` to `1` in production risks data loss and should only be done in certain emergency situations, and then only temporarily."* Default je 3.
- Jeden host znamená také **jeden monitor**, a *"a single Monitor is a single-point-of-failure"*; produkční doporučení jsou aspoň tři v kvóru. `mgr_standby_modules = False` obdobně ruší záložního managera.

„Ne pro produkci“ tedy znamená: na jednom uzlu si Ceph nechává celý svůj provozní náklad a vzdává se odolnosti proti ztrátě hostu, kvóra monitorů i samoopravy napříč stroji. Podporované to je a běží to — jen to nedělá práci, kvůli které vzniklo. Pro DR cíl je to obhajitelný kompromis jen tehdy, když Ceph na druhé straně ospravedlňuje něco jiného.

Oba mirroring démoni jsou na počtu uzlů nezávislí — `rbd-mirror` i `cephfs-mirror` jsou obyčejné démony a replikační dvojice 1 uzel → 1 uzel funguje.

**Vyřazující kritérium tedy nezabralo a obě Ceph varianty bylo nutné porazit na jejich vlastních kvalitách.** Poraženy byly:

- **CephFS mirror** padá na rozhodovacím pravidle 1 (nelze zjistit objem přenosu předem), pravidle 3 (živý vzdálený adresář není v půlce syncu platný DR bod, §6) a pravidle 4 (jen soubory). Tři pravidla, ani jedno o počtu uzlů.
- **RBD mirror** projde pravidly 1, 2 i 3 — je to skutečně dobrý mechanismus — ale padá na pravidle 4: umí jen bloky. Pokrýt jím ~150 TiB souborových médií by znamenalo buď přidat vedle CephFS (dva mechanismy, dva runbooky — přesně to, čemu pravidlo 4 předchází), nebo držet všechna média uvnitř RBD images, což je pro dataset obsluhovaný Plexem a Nextcloudem zvláštní tvar.

**Verdikt přežil, a to na lepší argumentaci, než měl původně.** Argument o počtu uzlů nebyl jen chybný, byl i slabší než ten, který ho nahradil: pravidlo 4 je vlastnost toho, **čím ty mechanismy jsou**, zatímco počet uzlů byla vlastnost nasazení, které jsem předpokládal.

**Co o jednouzlovém cíli platí doopravdy** a co je dobré vědět, než ho někdo postaví:

- **Redundance klesá na úroveň OSD.** Při `osd_crush_chooseleaf_type = 0` a `size = 2` mohou obě repliky přistát na témže hostu — o to jde —, takže cluster přežije ztrátu disku, ale ne ztrátu hostu, při 50% kapacitní efektivitě. ZFS RAIDZ2 na téže bedně přežije ztrátu dvou disků při ~75 %. Na jednom uzlu vycházejí ekonomicky lépe ZFS bez ohledu na otázku replikace.
- **Nemountuj CephFS kernel klientem na uzlu, kde běží OSD.** Při tlaku na paměť se kernel klient snaží vyprázdnit buffer do OSD, zatímco OSD se snaží alokovat paměť, a uzel se zadeadlockuje — hlášeno od [#1317](https://tracker.ceph.com/issues/1317) (2011) a stále vedeno v [#3076](https://tracker.ceph.com/issues/3076) a [#12648](https://tracker.ceph.com/issues/12648). Příručka Red Hatu to říká natvrdo: *"DO NOT mount kernel clients directly on the same node as your Ceph Storage Cluster."* Obchvaty: `ceph-fuse` (userspace paměť je stránkovatelná, takže se systém vzpamatuje) nebo mount z VM. Tohle kouše přesně jednouzlový CephFS případ a tříuzlový ne. Na samotný `cephfs-mirror` to **nedopadá** — ten používá libcephfs v userspace.
- **Provozní náklad se s počtem uzlů nezmenšuje.** Jeden uzel pořád znamená mon + mgr + OSD + MDS, cephadm kontejnery a ~4 GB RAM na OSD, aby na hardwaru, který nemá co distribuovat, běžel distribuovaný systém.

*(Tato sekce je dodatek; předchozí sekce zůstávají tak, jak vyšly, s výjimkou dotčeného řádku tabulky.)*

## 14. Přejmenování nebo přesun velkého stromu (doplněno 2026-08-13)

Přejmenování adresáře, pod kterým leží hodně dat, je nejostřejší test toho, na čem replikační mechanismus doopravdy stojí — a ty čtyři odpovědi pokrývají celé rozpětí, včetně jedné inverze, protože **tady je `cephfs-mirror` horší než rsyncová základna, kterou má vylepšovat.**

**ZFS: prakticky zdarma, uvnitř datasetu.** Přejmenování je metadatová operace — přepíše se položka ve zdrojovém rodičovském adresáři, přidá se do cílového, aktualizuje se ukazatel na rodiče přesouvaného objektu a nad tím indirect bloky. Žádný datový blok souboru se nedotkne. A protože inkrement je definovaný jako „bloky s birth time novějším než zdrojový snapshot“ (§3), přejmenování adresáře se 100 TiB pod ním přenese pár kilobajtů. Strom se nehne, protože se v něm nic nezměnilo.

Výhrada je přesně ta, na které záleží při návrhu: **platí to jen uvnitř jednoho datasetu.** Napříč datasety `rename(2)` selže s `EXDEV` a `mv` degraduje na kopírování a smazání, což zapíše všechny bloky znovu — „přesun“ mezi datasety je tedy plný přenos všeho, co pod ním leží. To zostřuje bod, který už zazněl v §12: hranice datasetů jsou hranicemi replikace a layout, který posadí často reorganizovaný strom na rozhraní dvou datasetů, to zaplatí na lince.

**RBD: neviditelné.** Jména souborů žijí uvnitř hostovaného filesystému; RBD replikuje bloky a žádnou cestu nevidí. Přejmenování ušpiní jen vlastní metadata hostovaného FS, takže se v deltě objeví nanejvýš hrstka 4MB objektů. Stejná strukturální výhra jako u ZFS a ze stejného důvodu — replikaci nezávislou na cestách nelze změnou cesty zmást.

**CephFS mirror: smazání a plná znovukopie, bez možnosti to zmírnit.** Démon žádnou detekci přejmenování nemá. `propagate_deleted_entries()` porovná dva snapshoty, najde položky přítomné v předchozím a chybějící (nebo se změněným typem) v aktuálním a smaže je na cíli přes `cleanup_remote_dir()` — rekurzivní průchod volající `ceph_unlinkat`. Nová cesta se pak synchronizuje jako čerstvá kopie. Kód nikdy nepáruje inody přes hranici delete/create; jeden z jeho vlastních komentářů poznamenává pořadí, na které spoléhá: *"N.B.: snapdiff returns the deleted entry before the newly created one."* Přejmenuj adresář se 100 TiB a cíl 100 TiB smaže a 100 TiB přenese znovu.

**rsync: ve výchozím stavu špatně a `--fuzzy` tenhle případ nezachrání.** Výchozí chování je přesně to očekávané — stará cesta se na cíli smaže a nová se přenese celá. `--fuzzy`/`-y` existuje, ale je potřeba číst jeho rozsah pozorně: *"The current algorithm looks in the same directory as the destination file for either a file that has an identical size and modified-time, or a similarly-named file."* Po přejmenování **adresáře** je cílový adresář nově vytvořený a prázdný, takže v něm není žádný basis soubor k nalezení. `--fuzzy` zmírňuje soubory přejmenované *uvnitř* adresáře; s přejmenovaným adresářem nedělá nic. Zopakování přepínače jen rozšíří sken do stromů `--compare-dest`/`--copy-dest`/`--link-dest`. `--detect-renamed` standardní volba není — v manuálové stránce rsyncu 3.4.4 se nevyskytuje a žije mezi nenaaplikovanými patchi rsyncu.

**Proč na té inverzi záleží.** rsync aspoň degraduje elegantně: `--link-dest` proti předchozímu běhu nebo fuzzy shoda dokážou část práce zachránit a ten failure mode je natolik známý, že se s ním plánuje. `cephfs-mirror` žádnou takovou páku nenabízí — smazat a překopírovat je tam strukturální, a na měřené lince může jediné `mv` spolykat měsíční rozpočet bez varování a bez možnosti to předem odhadnout (§5 už doložila, že objem přenosu dopředu zjistit neumí). U knihovny médií, kde je reorganizace adresářových stromů běžná věc a ne výjimečná, je to těžší námitka, než na první pohled vypadá.

## 15. Btrfs send/receive (doplněno 2026-08-13)

Btrfs do tabulky patří ze dvou důvodů. Je to **jediný další mechanismus ve stejné třídě jako `zfs send`** — serializace stavu filesystému, ne kopie souborů —, takže slouží jako kontrola, jestli je verdikt doopravdy o ZFS, nebo jen o „streamové replikaci“. A v tomhle projektu není hypotetický: stávající jednouzlový server běží na `mdadm + LUKS + LVM + Btrfs` a podle [zfs-vs-ceph](../zfs-vs-ceph/README.cs.md) se má stát DR cílem v druhé lokalitě.

**Kde se ZFS vyrovná.** Inkrement je `btrfs send -p <parent> <subvol>`, s `-c` pro další clone zdroje. Detekce změn stojí na generation numbers, takže stejně jako ZFS nikdy neprochází strom a cena sleduje objem změn. `--compressed-data` *"send[s] data that is compressed on the filesystem directly without decompressing it"* — protějšek `zfs send -c` — vyžaduje protokol streamu v2 a Linux 6.0 nebo novější. Všechny zúčastněné snapshoty musí být read-only: *"All snapshots involved in one send command must be read-only, and this status cannot be changed as long as there's a running send operation that uses the snapshot."*

**Kde poráží všechny ostatní včetně ZFS — přejmenování.** Send stream je příkazový jazyk a `BTRFS_SEND_C_RENAME` (9) je jedním z jeho příkazů, nesoucím zdrojovou a cílovou cestu. Přesunutý nebo přejmenovaný strom se přenáší jako explicitní instrukce, ne jako smazání a znovukopie. ZFS dojde ke stejnému výsledku jinou cestou (přejmenování ušpiní jen metadatové bloky, §14), ale Btrfs je tu jediný mechanismus, který přejmenování reprezentuje **jako takové** — což mimo jiné znamená, že přežije i přesuny přes hranici, která by v ZFS byla hranicí datasetu, tedy přesně ten `EXDEV` případ, který ZFS stojí plný přenos (§14).

**Kde v tomhle kontextu selhává, a je to rozhodující.** Dvě ze čtyř rozhodovacích pravidel z §1 padají naplno:

- **Pravidlo 2 — žádné resume.** `btrfs send` ani `btrfs receive` resume neumí a nikde není dokumentované. Přerušený přenos začíná od nuly. Na rezidenční WAN s inkrementy v jednotkách TiB je to samo o sobě diskvalifikace — je to přesně ten failure mode, kvůli kterému pravidlo 2 existuje.
- **Pravidlo 1 — žádný odhad objemu.** `btrfs send` nemá dry-run, takže neexistuje způsob, jak přenos ocenit dřív, než se odečte z měsíčního stropu. `zfs send -nvP` protějšek v Btrfs nemá.

To první zhoršují dva navazující problémy. Přijatý subvolume se *"made read-only after the receiving process finishes successfully"*, takže přerušený příjem nechá ležet **zapisovatelný, částečný subvolume** — automaticky se neuklidí a podle trackeru btrbk se snadno splete s dokončeným ([btrbk #17](https://github.com/digint/btrbk/issues/17)). Hůř: protože další inkrement potřebuje jako rodiče předchozí **úspěšně přijatý** snapshot, jediný selhaný přenos může zablokovat všechny následující, dokud někdo nezasáhne ([btrbk #91](https://github.com/digint/btrbk/issues/91), [#196](https://github.com/digint/btrbk/issues/196)). U sólo admina bez on-callu je replikační řetěz, který se tiše zasekne a zaseknutý zůstane, horší vlastnost než pomalost. Manuálová stránka navíc varuje, že cílová cesta je během příjmu zapisovatelná: *"users who have write access to files or directories in the receiving path can add, remove, or modify files."*

**A nemá odpověď na bloková zařízení.** Btrfs nemá ekvivalent ZVOLu, takže disky VM jsou obyčejné soubory. Padá tím na pravidle 4 stejně jako RBD, jen z opačné strany: RBD umí bloky a ne soubory, Btrfs soubory a ne bloky.

**Důsledek pro DR lokalitu.** Replikace nepřechází mezi enginy (§8), takže ponechat stávající bednu na Btrfs znamená, že na ni ZFS primár nemůže `send`ovat vůbec — DR linka by spadla na rsync a jedním krokem odevzdala blokovou granularitu, atomicitu i odhad objemu. **Pokud má být ten server DR cílem, měl by být přestavěn na ZFS, ne ponechán na Btrfs.** V původním migračním plánu v zfs-vs-ceph to bylo implicitní; tady je to řečeno nahlas a je to praktický důvod, proč tahle sekce existuje místo poznámky pod čarou.

**V čem Btrfs neprohrává.** Nepotřebuje démona, umí push i pull, vystačí si s jedním uzlem na cíli a jeho extentová granularita je se ZFS srovnatelná. Na spolehlivé LAN lince, s nástrojem typu btrbk řešícím snapshoty a retry politiku, je replikace Btrfs → Btrfs rozumný návrh. Vylučuje ho tenhle kontext — nespolehlivá měřená WAN, žádný on-call a disky VM ve hře —, ne slabost mechanismu obecně.

## 16. Proxmox Backup Server (doplněno 2026-08-13)

PBS je v tabulce na jiném základě než zbylých pět a předstírat opak by byla chyba. §8 už tu čáru vedla: replikace a záloha nejsou totéž. **PBS není replikační cíl, na který se dá přepnout — je to datastore, ze kterého se obnovuje.** Svůj sloupec si zaslouží stejně, protože inkrementálně přesouvá změny mezi dvěma lokalitami, protože podle [zfs-vs-ceph](../zfs-vs-ceph/README.cs.md) už v téhle stavbě je, a protože v několika řádcích poráží každý replikační mechanismus tady.

**Jak vzniká delta.** PBS dělí data na obsahově adresované chunky: fixních 4 MiB pro blokové obrazy, protože *"the content (disk image), is split into chunks of the same length (typically 4 MiB)"*, a proměnlivé pro souborové archivy, kde *"first generates a consistent file archive (pxar) and uses a rolling hash over this on-the-fly generated archive to calculate chunk boundaries."* Shodný obsah se hashuje shodně, takže upload je vyjednávání: *"If it detects a chunk that already exists on the server, it can send only the checksum instead of data and checksum."*

**Rozlišení, na kterém záleží — cena čtení není cena přenosu.** U VM platí, že *"VMs in Proxmox VE can make use of 'dirty bitmaps', which can track the changed blocks of an image"*, a protože granularita bitmapy odpovídá hranicím chunků, nahrají se jen změněné chunky. Bitmapa je ale křehká: žije jen dokud VM běží, takže zastavení nebo restart (včetně „Reboot“ z rozhraní PVE kvůli aplikaci čekajících změn) ji zahodí, a je vázaná na jeden cílový server, takže zálohování téže VM na dvě instance PBS ji zneplatňuje pokaždé. Její ztráta **nestojí** síťový provoz — vyjednávání o známých chuncích znovunahrání stejně potlačí — stojí plné lokální přečtení disku. U souborů je protějškem `change-detection-mode=metadata`, který *"Encode[s] changed files, reuse[s] unchanged from previous snapshot, creating a split archive"* a porovnává proti předchozímu metadatovému archivu, aby se nezměněné soubory nemusely číst znovu. Bez něj se 150TiB knihovna médií čte celá při každém běhu.

Proto tabulka hodnotí PBS ❌ na řádku „cena detekce roste s“ a přitom ✅ na přenosových řádcích: je to jediný mechanismus tady, jehož drahým zdrojem je **lokální I/O, ne linka.**

**Kde PBS poráží každý replikační mechanismus v tomhle dokumentu.** Tři řádky, a nejsou to drobnosti:

- **Šifrování na klientu.** AES-256-GCM, klíče zůstávají na klientu a *"Without their key, backed up files will be inaccessible."* §12 upozorňovala, že při LUKS drží DR lokalita nutně dešifrovatelnou kopii, a potřebuje proto vlastní LUKS + Tang. PBS tenhle problém nemá vůbec — druhý konec nikdy nedrží plaintext ani klíč. Je to silnější záruka než `zfs send -w` a je nezávislá na enginu.
- **Vestavěné ověřování.** §10 tvrdila, že replika, kterou nikdo nescrubuje, není replika, a že dva ze čtyř historických ZFS bugů v `send` cestě byly tiché. PBS má verify joby, které plánovaně přeověřují zálohy proti zaznamenaným checksumům — přesně ta disciplína, kterou §10 vyžaduje, jako funkce místo cronu, na který si musíš vzpomenout.
- **Nezávislost na enginu a obsahové adresování.** Je mu jedno, co je pod ním, takže ZFS → cokoliv funguje tam, kde `send`/`recv` mezi enginy nepřejde (§8). A protože jsou chunky obsahově adresované, oba případy, které trestají blokovou replikaci — rewrite in-place beze změny logického obsahu (§8) a přejmenovaný strom (§14) —, nestojí nic: tytéž chunky se prostě znovu odkážou.

**Mezi lokalitami: sync joby.** Dvě nezávislé instance PBS si replikují sync joby, *"configured for pull or push direction"*, podle plánu, a přenášejí jen to, co na cíli chybí. To je skutečně otázka tohohle dokumentu zodpovězená jinými prostředky. Jedna provozní past pro měřenou linku: obecné limity traffic controlu je **nepokrývají** — *"Sync jobs on the server are not affected by the configured rate limits. If you want to limit the incoming traffic of pull-based or outgoing traffic of push-based sync job, you need to setup a job-specific rate-in limit."*

**Proti rozhodovacím pravidlům z §1.** PBS projde pravidlem 3 (dokončený snapshot je neměnný a ověřitelný) i pravidlem 4 (jeden mechanismus pro soubory i disky VM — což nezvládne žádná Ceph varianta). Padá na pravidle 1: neexistuje způsob, jak dnešní přenos ocenit dřív, než proběhne. Na pravidle 2 je částečný — resume token nemá, ale protože jsou chunky obsahově adresované, opakování po výpadku pošle jen to, co serveru pořád chybí, což je v praxi většina toho, co resume token kupuje.

**Proč nebere verdikt.** Cíl není stav, ze kterého jde rovnou obsluhovat. Zotavení znamená obnovu a u ~150 TiB médií se to měří ve dnech, ne v minutách — PBS tedy nemůže naplnit účel, kvůli kterému DR lokalita existuje. Není to vada; je to jiná práce.

**Skutečný závěr: provozovat obojí a nenutit ani jedno dělat práci toho druhého.** `zfs send` dá DR repliku, která už je živý filesystém, s ocenitelným inkrementem a resume tokenem. PBS dá obnovu do bodu v čase, retenci, deduplikaci napříč snapshoty, šifrování na klientu pro kopii mimo lokalitu a ověřovací disciplínu z §10. Failure mode, kterému je potřeba se vyhnout, je brát jedno jako náhradu druhého: replika přes `send`/`recv` není záloha (věrně zreplikuje i smazání) a datastore PBS není failover cíl.

## Reference

Externí zdroje ověřené 2026-08-13:

- OpenZFS: [zfs-send(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html), [zfs-receive(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html)
- Ceph RBD: [RBD Mirroring](https://docs.ceph.com/en/latest/rbd/rbd-mirroring/), [rbd(8) — export-diff / import-diff / merge-diff / fast-diff](https://docs.ceph.com/en/latest/man/8/rbd/), [Incremental Snapshots with RBD (ceph.io)](https://ceph.io/en/news/blog/2013/incremental-snapshots-with-rbd/)
- CephFS: [CephFS Snapshot Mirroring (user)](https://docs.ceph.com/en/latest/cephfs/cephfs-mirroring/), [CephFS Mirroring (dev)](https://docs.ceph.com/en/latest/dev/cephfs-mirroring/), [zdrojový rst na GitHubu](https://github.com/ceph/ceph/blob/main/doc/dev/cephfs-mirroring.rst), [PR #37876 — cephfs-mirror: synchronize directory snapshots](https://github.com/ceph/ceph/pull/37876), [Red Hat Ceph Storage 8 — File System mirrors (hardlinky)](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/8/html/file_system_guide/ceph-file-system-mirrors), [IBM Storage Ceph — File System mirrors](https://www.ibm.com/docs/en/storage-ceph/6.1.0?topic=systems-ceph-file-system-mirrors), [croit — CephFS Snapdiff Feature](https://www.croit.io/blog/introducing-the-innovative-cephfs-snapdiff-feature)
- Vydání Ceph: [Ceph Releases (index)](https://docs.ceph.com/en/latest/releases/), [v20.2.0 Tentacle](https://ceph.io/en/news/blog/2025/v20-2-0-tentacle-released/), [v20.2.1 Tentacle](https://ceph.io/en/news/blog/2026/v20-2-1-tentacle-released/), [v19.2.4 Squid](https://ceph.io/en/news/blog/2026/v19-2-4-squid-released/)
- Orchestrace: [zrepl — Configuration Overview](https://zrepl.github.io/configuration/overview.html), [zrepl — Transports](https://zrepl.github.io/configuration/transports.html), [sanoid/syncoid — README](https://github.com/jimsalterjrs/sanoid), [sanoid #672 — automatický fallback při selhání resume (otevřené)](https://github.com/jimsalterjrs/sanoid/issues/672), [Proxmox — Storage Replication (`pvesr`)](https://pve.proxmox.com/wiki/Storage_Replication), [Proxmox — PVE-zsync](https://pve.proxmox.com/wiki/PVE-zsync)
- PBS (§16): [Technical Overview — chunky, dedup, dirty bitmaps](https://pbs.proxmox.com/docs/technical-overview.html), [Backup Client — `change-detection-mode`, šifrování na klientu](https://pbs.proxmox.com/docs/backup-client.html), [Managing Remotes — sync joby](https://pbs.proxmox.com/docs/managing-remotes.html), [Network Management — traffic control](https://pbs.proxmox.com/docs/network-management.html), [Storage — verify joby](https://pbs.proxmox.com/docs/storage.html)
- Btrfs (§15): [btrfs-send(8)](https://btrfs.readthedocs.io/en/latest/btrfs-send.html), [btrfs-receive(8)](https://btrfs.readthedocs.io/en/latest/btrfs-receive.html), [formát send streamu — `BTRFS_SEND_C_RENAME`](https://btrfs.readthedocs.io/en/latest/dev/dev-send-stream.html), [btrbk #17 — částečné subvolume se při chybě nemažou](https://github.com/digint/btrbk/issues/17), [#91](https://github.com/digint/btrbk/issues/91), [#196](https://github.com/digint/btrbk/issues/196)
- Přejmenování (§14): [`PeerReplayer.cc` — `propagate_deleted_entries()` / `cleanup_remote_dir()`](https://github.com/ceph/ceph/blob/main/src/tools/cephfs_mirror/PeerReplayer.cc), [manuál rsync 3.4.4 — `--fuzzy`](https://download.samba.org/pub/rsync/rsync.1)
- Sparse oblasti (§5): [`PeerReplayer.cc` — `copy_to_remote()`](https://github.com/ceph/ceph/blob/main/src/tools/cephfs_mirror/PeerReplayer.cc), [CephFS — Differences from POSIX](https://docs.ceph.com/en/latest/cephfs/posix/)
- Jednouzlový Ceph (§13): [cephadm — `--single-host-defaults`](https://docs.ceph.com/en/latest/cephadm/install/), [Ceph — Pools (doporučení `size`/`min_size`)](https://docs.ceph.com/en/latest/rados/operations/pools/), [Ceph — Monitor Config Reference](https://docs.ceph.com/en/latest/rados/configuration/mon-config-ref/), [tracker #1317 — deadlock, kernel klient na uzlu s OSD](https://tracker.ceph.com/issues/1317), [#3076](https://tracker.ceph.com/issues/3076), [#12648](https://tracker.ceph.com/issues/12648), [Red Hat — Mounting and Unmounting Ceph File Systems](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/2/html/ceph_file_system_guide_technology_preview/mounting_and_unmounting_ceph_file_systems)
- Navazující kontext: [ZFS vs Ceph — tento repozitář](../zfs-vs-ceph/README.cs.md) (§12 šifrování, §15 spolehlivostní profily a timelines tichých korupčních bugů)

---

*Zkoumáno a sepsáno ve spolupráci s Claude (Anthropic); fakta ověřena proti zdrojům výše k 13. srpnu 2026. Tento dokument je datovaný snímek a není průběžně aktualizován.*

*© 2026 Petr Kratochvíl · Licencováno pod [CC BY 4.0](../LICENSE)*
