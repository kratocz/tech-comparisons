# Inkrementální replikace mezi dvěma storage clustery: ZFS send/recv vs Ceph mirroring

- **Verdikt:** ⭐ **`zfs send -i`** (orchestrace zreplem *nebo* syncoidem — §12) — platí pro kontext popsaný níže
- **Fakta ověřena:** 2026-08-13 (OpenZFS man pages master, docs.ceph.com latest, Proxmox wiki, zrepl docs, README a issue tracker sanoid/syncoid, Red Hat/IBM Ceph docs)
- **Opravy:** §13 (2026-08-13) — hodnocení „min. 3 uzly" a vyřazující kritérium v §1 byly chybné; jednouzlový Ceph cluster je podporován. Verdikt přežil, ale na jiné argumentaci.
- **Adversariální ověření:** provedeno 2026-08-13 proti verdiktu. Mechanismus **nevyvrátilo** (§2–§8 obstály), ale **vyvrátilo volbu orchestrace**: rozlišovací argument pro zrepl proti syncoidu stál na issues sanoid #304/#528, které jsou zavřené od 2019/2020. §12 byla přepsána tak, aby orchestraci uváděla jako otevřené, těsné rozhodnutí, ne jako uzavřené.
- **Otevřené tagy:** `[OVĚŘIT]` — zachování sparse oblastí u `cephfs-mirror` (§5)
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

## Srovnání v přehledu

Symboly: ✅ silná stránka · 🟡 funguje s výhradami / kompromis · ❌ slabina nebo chybí · — nedává smysl. Hodnoceno **pro tento kontext** (dvě lokality, asymetrická rezidenční WAN se stropem na data, sólo admin, bulk média + hrst VM disků, DR cíl bez zápisu) — ne obecně; na symetrické DC lince s tučnou kapacitou by řada řádků dopadla jinak. Poslední sloupec je engine-neutrální základna, proti které se ostatní měří.

| Kritérium | ZFS `send`/`recv` | Ceph RBD mirror | CephFS mirror | rsync / rclone |
|---|---|---|---|---|
| **▸ Jak vzniká delta** | | | | |
| Jednotka přenosu | ✅ blok (`recordsize`/`volblocksize`) | ✅ objekt / extent | ❌ **celý změněný soubor** | 🟡 rolling-checksum delta |
| Nalezení změn bez procházení stromu | ✅ birth time v CoW stromu | ✅ object-map + fast-diff | ✅ snapdiff (od Reefu, §11) | ❌ stat každého souboru |
| Cena detekce roste s | ✅ objemem změn | ✅ počtem objektů (z in-memory mapy) | 🟡 počtem změněných souborů | ❌ **počtem souborů celkem** |
| Serializace stavu FS vs kopie přes POSIX | ✅ stav FS (díry, komprese, properties) | ✅ bloky (POSIX se neúčastní) | ❌ POSIX kopie → **hardlinky se rozpadnou** | ❌ POSIX kopie |
| **▸ Atomicita a konzistence** (§6) | | | | |
| Cíl je vždy platný minulý stav | ✅ transakční `recv` | ✅ delta se aplikuje celá, nebo rollback | ❌ živý adresář je během syncu směs | ❌ |
| Konzistentní bod po pádu v půlce | ✅ poslední přijatý snapshot | ✅ poslední mirror-snapshot | 🟡 poslední **dokončený** snapshot na cíli | ❌ žádný |
| Resume po přerušení linky | ✅ resume token (`recv -s`) | 🟡 démon pokračuje sám; DIY `export-diff` ne | 🟡 démon pokračuje sám (po souborech) | 🟡 `--partial` |
| **▸ Linka a rozpočet** | | | | |
| **Odhad objemu přenosu předem** | ✅ `zfs send -nvP` (přesně) | ✅ `rbd diff --format json` (součet extentů) | ❌ není | ❌ `--dry-run` dá jen seznam |
| Komprese na drátě | ✅ `-c` posílá bloky komprimované z disku | 🟡 externí (ssh `-C`) | 🟡 externí | ✅ `-z` |
| Přenos bez klíče na cílové straně | ✅ `send -w` (raw) | ❌ | ❌ | ❌ |
| Omezení šířky pásma | ✅ zrepl / `pv` / `mbuffer` | 🟡 konfigurace démona | 🟡 konfigurace démona | ✅ `--bwlimit` |
| **▸ Provoz** | | | | |
| Nutný démon | ✅ žádný (nebo zrepl) | ❌ `rbd-mirror` | ❌ `cephfs-mirror` | ✅ žádný |
| Kde démon běží / směr | ✅ push i pull | 🟡 **sekundár** (pull) | 🟡 **primár** (push) | ✅ oboje |
| Obousměrně / failback | 🟡 ruční prohození rolí | ✅ promote/demote, two-way | ❌ jednosměrně, **jediný peer** | 🟡 ruční |
| Min. počet uzlů na cíli | ✅ **1** | 🟡 1 podporován, ne pro produkci (§13) | 🟡 1, navíc caveat kernel klienta (§13) | ✅ 1 |
| **▸ Vhodnost pro workload** | | | | |
| Velké průběžně měněné soubory (VM, DB) | ✅ | ✅ | ❌ přenese celý soubor | 🟡 delta ano, ale čte celý soubor |
| Miliony malých souborů, málo změn | ✅ | — | ✅ | ❌ walk dominuje nad přenosem |
| Rewrite in-place / rekomprese (§8) | ❌ pošle všechny ušpiněné bloky | ❌ dtto | ✅ pošle jen změněné soubory | ✅ pošle jen změněný obsah |
| Zapisovatelný / RWX cíl | ❌ cíl musí být `readonly` | ❌ | ✅ (ale nemá se) | ✅ |
| Podmnožina datasetu / jiný layout na cíli | ❌ celý dataset | ❌ celý image | ✅ per adresář | ✅ libovolně |
| Přenos mezi různými enginy | ❌ | ❌ | ❌ | ✅ |

**Jak to číst.** ZFS vyhrává všude, kde se ptáme „kolik dat poteče a co se stane, když spadne linka" — bloková granularita, přesný odhad předem, transakční příjem a resume token. RBD je jeho rovnocenný protějšek na blokové úrovni a v jedné věci ho poráží (nativní obousměrný failover s promote/demote), platí za to ale třemi uzly na cílové straně a povinným démonem. CephFS mirror vyhrává jen tam, kde ostatní nemohou — sdílený zapisovatelný filesystém a replikace po adresářích místo po celých datasetech — a prohrává na granularitě, atomicitě i na hardlincích. rsync je poslední sloupec ne proto, že by byl špatný, ale proto, že je jediný, který zvládne to, co ostatní neumí vůbec: **změnu enginu, změnu layoutu a podmnožinu** — a v jednom scénáři (§8) porazí všechny ostatní.

## 1. Rozhodovací pravidla (2026-08-13)

Sepsáno před volbou nástroje a verdiktu (viz poznámka k procesu v hlavičce). Vybraný mechanismus musí splnit všechny čtyři body:

1. **Rozpočet na data je zjistitelný předem.** Musí existovat způsob, jak před spuštěním přenosu zjistit jeho velikost s chybou do ~10 %. Bez toho nelze provozovat linku s tvrdým měsíčním stropem, protože jediná rekomprese datasetu ho vyčerpá.
2. **Přerušení linky nesmí znamenat přenos od nuly.** Rezidenční WAN vypadává; přenos v řádu TiB, který po výpadku začíná znovu, nikdy nedoběhne.
3. **Cílová strana má být kdykoliv použitelná jako DR bod, bez ručního posuzování.** „Podívej se, jestli to doběhlo" není operace, kterou chci dělat v krizi.
4. **Jeden mechanismus pro soubory i VM disky.** Dvě replikační roury se dvěma sadami selhání a dvěma runbooky jsou u sólo admina větší riziko než cokoliv, co ušetří.

**Vyřazující kritérium:** cokoliv, co vyžaduje ≥3 uzly na cílové straně, je mimo — druhá lokalita startuje jako jeden stroj. *(Čteno zpětně: toto pravidlo **nezabralo** — jednouzlový Ceph cluster je podporován. Viz oprava v §13; pravidlo zůstává, jak bylo napsáno, místo aby bylo přepsáno na míru výsledku.)*

## 2. Strukturální asymetrie: ZFS má jeden mechanismus, Ceph dva

Nejužitečnější věc na téhle otázce se ukáže hned na začátku: **čtyři případy se nerozpadají na čtyři odpovědi, ale na dvě dvojice.**

Pro ZFS je *filesystem dataset* i *ZVOL* tentýž objekt. Replikační vrstva vůbec nesahá na to, co je uvnitř — pracuje se stromem bloků a jejich birth time, ne se soubory. `zfs send` na dataset s milionem fotek a `zfs send` na ZVOL s diskem virtuálu je doslova stejný příkaz se stejnými přepínači a stejnou sémantikou. Otázky „jak replikovat soubory" a „jak replikovat bloková zařízení" v ZFS **nejsou dvě otázky**.

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

Delta se nepočítá porovnáváním — vyplývá z CoW stromu. Každý blok nese *birth time* (transaction group, ve které vznikl), takže „co se změnilo od snapshotu X" je otázka na metadata, ne na obsah. Náklad je tedy úměrný **objemu změn**, ne počtu souborů ani velikosti datasetu. Dataset s deseti miliony souborů a jednou změněnou fotkou pošle tu fotku a nic víc; rsync by ho musel celý projít.

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

`[OVĚŘIT]` Zda bulk copy zachovává **sparse** oblasti, jsem v dokumentaci nenašel. U řídkých souborů je to rozdíl mezi „přenese se pár GB" a „přenese se nominální velikost".

Další doložená omezení: **jediný peer**, **jednosměrně** (failback je ruční) a snap-schedule na vzdáleném FS pro mirrorované adresáře rozbije metadata (*"will cause … errors like `invalid metadata`"*).

## 6. Jednotka přenosu a atomicita: nejpřehlíženější rozdíl

„Mirroring snapshotů" zní u ZFS i u CephFS stejně, ale znamená to dvě různé věci — a rozdíl se projeví přesně v okamžiku, kdy na tom záleží nejvíc, tedy když přenos spadne v půlce.

**ZFS: serializace stavu, transakční příjem.** `zfs send` vytvoří **stream** — serializovaný stav filesystému, ne sadu souborů. `zfs recv` ho aplikuje jako transakci. Bez `-s` se částečně přijatý stav zahodí; man page to říká z opačné strany, ale jednoznačně: `-s` znamená *"If the receive is interrupted, save the partially received state, rather than deleting it."* Důsledek: **cílový dataset je v každém okamžiku nějaký platný minulý snapshot.** Nikdy není směsí. (`btrfs send`/`receive` patří do stejné třídy — serializace stavu FS, ne kopie souborů.)

**CephFS: kopie do živého adresáře, snapshot až potom.** Dokumentace popisuje pořadí doslova: *"Snapshots are synchronized by transferring snapshot data to the remote file system **and by creating a snapshot with the same name** as the snapshot being synchronized."* Nejdřív se soubory nakopírují do **živého** vzdáleného adresáře, teprve po dokončení tam vznikne snapshot. Mezi tím je adresář směsí starých a nových souborů.

Proto dokumentace trvá na *"Treat the remote filesystem as read-only. Nothing is inherently enforced by CephFS."* Není to hygienické doporučení — je to důsledek toho, že v půlce syncu tam prostě není platný stav.

**Co si z toho odnést do runbooku:** na CephFS DR lokalitě není tvým obnovovacím bodem to, co leží v adresáři, ale **poslední dokončený snapshot**. Na ZFS DR lokalitě je obnovovacím bodem sám dataset. To je rozdíl mezi „obnovím" a „nejdřív musím zjistit, co je platné".

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

Obecné pravidlo: **blokový delta přenos vyhrává na „hodně souborů, málo změn", prohrává na „málo souborů, hodně CoW churnu"**.

Druhá hranice je tvrdší: `send`/`recv` ani `rbd-mirror` **neumí přenášet mezi enginy, měnit layout ani vybrat podmnožinu**. ZFS → Ceph, jiná struktura na cíli, zapisovatelný cíl, replikace jen jednoho podadresáře → tam pořád patří rsync/rclone, nebo rovnou dedup záloha (Kopia, restic, borg, PBS) místo replikace. Replikace a záloha nejsou totéž a tenhle dokument řeší jen tu první.

## 9. Orchestrace: co doopravdy točí smyčku

`zfs send` je primitivum, ne řešení — snapshoty, retenci, retry a resume musí někdo řídit.

| Nástroj | Rozsah | Poznámka |
|---|---|---|
| **zrepl** | dva samostatné stroje | Dohlížený démon — retry a hlášení stavu má vestavěné. Push i pull, resumovatelný přenos, replikační kurzor jako bookmark, pruning policy. Transporty: `tcp` (**nešifrovaný**), `tls` (klientské certifikáty, CN = identita), `ssh+stdinserver` (méně efektivní, ale nevystavuje démona do internetu), `local`. Cena: vlastní konfigurační jazyk a u `tls` správa certifikátů. |
| **syncoid** (sanoid) | dva stroje přes SSH | Skript spouštěný z cronu, ne démon. Resume podporuje a zapíná automaticky od 1.4.18; dále `--create-bookmark`, `--source-bwlimit`/`--target-bwlimit` a promazávání na cíli přes `--delete-target-snapshots`. Tvorbu snapshotů a retenci na zdroji řeší sanoid. Zbytková mezera: když selže samotný pokus o resume, neumí se sám přepnout na přenos bez resume ([#672](https://github.com/jimsalterjrs/sanoid/issues/672), otevřené od 2021). Detekce selhání je na provozovateli — cron skript, který přestal běžet, mlčí. |
| **pve-zsync** | dva **samostatné** Proxmox hosty | Přes SSH, **nevyžaduje členství v clusteru**. Push i pull, default interval 15 min přes cron. Přesně profil „dvě lokality, dva clustery". |
| **pvesr** | uzly **téhož** Proxmox clusteru | ❗ **Nepoužitelné pro tenhle případ.** Minimální interval 1 min, ale funguje jen uvnitř jednoho clusteru. Snadná záměna s `pve-zsync`. |

Pro dvě lokality s vlastními clustery tedy `pvesr` odpadá bez ohledu na to, jak dobře funguje uvnitř clusteru — a to je nejčastější omyl při návrhu tohoto scénáře.

## 10. Ověření: replika, kterou jsi neproscrubboval, není replika

Tohle platí pro všechny čtyři mechanismy a je to jediná sekce, kterou by bylo chybou přeskočit.

Z [zfs-vs-ceph §15](../zfs-vs-ceph/README.cs.md) plyne, že **dva ze čtyř historických ZFS korupčních bugů v `send` cestě byly tiché** — `hole_birth` (2016) i encryption `send`/`recv` (#12014, uzavřeno 2025). Checksum je nechytí, protože bug sedí nad vrstvou, která checksumy počítá: příjemce nehlásí chybu a přesto cíl ≠ zdroj. Rizika ZFS sedí historicky právě v `send` cestách a v čerstvě dodaných funkcích, ne v jádru zápisu.

Z toho plyne minimum bez ohledu na zvolený nástroj: **pravidelný scrub na cílové straně**, **test restore** (ne „zkontroluj, že soubor existuje", ale skutečné nabootování VM nebo porovnání checksumů) a u ZFS **nechodit do `.zfs` na přijímací straně během běžícího `recv`** — deadlock #18073, oprava až v 5/2026.

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

**Volba orchestrace je mnohem těsnější a tahle analýza ji nerozhoduje.** Dřívější verze doporučovala rovnou zrepl; adversariální průchod tu úvahu zabil, protože argument o robustnosti resume popisoval stav sanoidu z let 2018–2020 (issues [#304](https://github.com/jimsalterjrs/sanoid/issues/304), [#528](https://github.com/jimsalterjrs/sanoid/issues/528), obě zavřené), ne dnešek. Ověřeno k 2026-08-13: syncoid resumuje automaticky, umí bookmarky, limity pásma i promazávání na cíli — na všech čtyřech rozhodovacích pravidlech jsou tedy rovnocenné. Skutečně je odlišuje kompromis, který kontext tahá na obě strany současně: zrepl je **dohlížený démon**, takže na otázku „proběhla dneska v noci replikace?" se dá odpovědět bez dalšího lešení — což při absenci on-callu váží; syncoid je **řádek v cronu**, tedy míň provozu a míň příležitostí ke špatné konfiguraci — což váží u sólo admina, který cení jednoduchost. **Zvol zrepl, pokud chceš detekci selhání v ceně; zvol syncoid, pokud už provozuješ monitoring, který si mlčícího cronu všimne.** §1 splní obojí. Ať padne cokoliv, nepoužívej u zreplu transport `tcp` — je nešifrovaný.

**Vědomě přijaté kompromisy:**

- **Žádný nativní failback.** Prohození roli je ruční, zatímco RBD má promote/demote. Pro DR lokalitu, na kterou se nezapisuje, je to přijatelné; kdyby se z ní stal aktivní uzel, tenhle bod se otevírá znovu.
- **Křehkost řetězu.** Jeden smazaný kotevní snapshot = full resend. Mitigace jsou levné (bookmarky, `zfs hold`, `readonly=on` na cíli), ale musí být nasazené od začátku, ne po prvním incidentu.
- **CoW churn** (§8) může jednorázově vystřelit objem přenosu. Pro bulk média okrajové; před plánovanou rekompresí nebo změnou `recordsize` je ale nutné počítat s tím, že se přenese znovu prakticky všechno.
- **Celý dataset, nebo nic.** Nelze replikovat podmnožinu → **návrh datasetů se stává návrhem replikace**. To je rozhodnutí, které se dělá jednou a špatně se mění.
- **Šifrování:** při volbě LUKS (viz [zfs-vs-ceph §12](../zfs-vs-ceph/README.cs.md)) je `send -w` bezpředmětné — stream nese plaintextové ZFS bloky a důvěrnost na drátě stojí a padá s transportem. DR lokalita tedy potřebuje vlastní LUKS + Tang, ne jen disk.

**Změním názor, pokud:** (a) druhá lokalita bude potřebovat sdílený RWX filesystém replikovaný mezi lokalitami — tam ZFS nemá co nabídnout a i slabší `cephfs-mirror` je lepší než nic; (b) objem denní změny klesne tak nízko, že rozdíl mezi souborovou a blokovou granularitou zmizí v šumu linky, čímž zmizí hlavní argument; (c) DR lokalita se stane aktivním zapisujícím uzlem, čímž se ruční failback změní z nepohodlí v riziko.

## 13. Oprava (2026-08-13): cíl na jednom uzlu

**Původní vyřazující kritérium v §1 a hodnocení „min. 3 uzly" byly chybné.** Opraveno tentýž den, kdy dokument vyšel, poté co je čtenář zpochybnil. Níže je opravená pozice; pravidlo v §1 zůstává, jak bylo napsáno, protože rozhodovací pravidlo přepsané po zhlédnutí výsledku už není rozhodovací pravidlo (čte se tedy nově jako: *pravidlo nezabralo*).

**Fakt: jednouzlový Ceph cluster je upstreamem explicitně podporován.** cephadm na to má vlastní přepínač — *"To deploy a Ceph cluster running on a single host, use the `--single-host-defaults` flag when bootstrapping."* Nastaví tři volby:

```
global/osd_crush_chooseleaf_type = 0     # failure domain klesá z hostu na OSD
global/osd_pool_default_size     = 2
mgr/mgr_standby_modules          = False
```

Upstream k tomu jedním dechem dodává výhradu: *"such clusters are generally not suitable for production."* Oba mirroring démoni jsou na počtu uzlů nezávislí — `rbd-mirror` i `cephfs-mirror` jsou obyčejné démony a replikační dvojice 1 uzel → 1 uzel funguje.

**Vyřazující kritérium tedy nezabralo a obě Ceph varianty bylo nutné porazit na jejich vlastních kvalitách.** Poraženy byly:

- **CephFS mirror** padá na rozhodovacím pravidle 1 (nelze zjistit objem přenosu předem), pravidle 3 (živý vzdálený adresář není v půlce syncu platný DR bod, §6) a pravidle 4 (jen soubory). Tři pravidla, ani jedno o počtu uzlů.
- **RBD mirror** projde pravidly 1, 2 i 3 — je to skutečně dobrý mechanismus — ale padá na pravidle 4: umí jen bloky. Pokrýt jím ~150 TiB souborových médií by znamenalo buď přidat vedle CephFS (dva mechanismy, dva runbooky — přesně to, čemu pravidlo 4 předchází), nebo držet všechna média uvnitř RBD images, což je pro dataset obsluhovaný Plexem a Nextcloudem zvláštní tvar.

**Verdikt přežil, a to na lepší argumentaci, než měl původně.** Argument o počtu uzlů nebyl jen chybný, byl i slabší než ten, který ho nahradil: pravidlo 4 je vlastnost toho, **čím ty mechanismy jsou**, zatímco počet uzlů byla vlastnost nasazení, které jsem předpokládal.

**Co o jednouzlovém cíli platí doopravdy** a co je dobré vědět, než ho někdo postaví:

- **Redundance klesá na úroveň OSD.** Při `osd_crush_chooseleaf_type = 0` a `size = 2` mohou obě repliky přistát na témže hostu — o to jde —, takže cluster přežije ztrátu disku, ale ne ztrátu hostu, při 50% kapacitní efektivitě. ZFS RAIDZ2 na téže bedně přežije ztrátu dvou disků při ~75 %. Na jednom uzlu vycházejí ekonomicky lépe ZFS bez ohledu na otázku replikace.
- **Nemountuj CephFS kernel klientem na uzlu, kde běží OSD.** Při tlaku na paměť se kernel klient snaží vyprázdnit buffer do OSD, zatímco OSD se snaží alokovat paměť, a uzel se zadeadlockuje — hlášeno od [#1317](https://tracker.ceph.com/issues/1317) (2011) a stále vedeno v [#3076](https://tracker.ceph.com/issues/3076) a [#12648](https://tracker.ceph.com/issues/12648). Příručka Red Hatu to říká natvrdo: *"DO NOT mount kernel clients directly on the same node as your Ceph Storage Cluster."* Obchvaty: `ceph-fuse` (userspace paměť je stránkovatelná, takže se systém vzpamatuje) nebo mount z VM. Tohle kouše přesně jednouzlový CephFS případ a tříuzlový ne. Na samotný `cephfs-mirror` to **nedopadá** — ten používá libcephfs v userspace.
- **Provozní náklad se s počtem uzlů nezmenšuje.** Jeden uzel pořád znamená mon + mgr + OSD + MDS, cephadm kontejnery a ~4 GB RAM na OSD, aby na hardwaru, který nemá co distribuovat, běžel distribuovaný systém.

*(Tato sekce je dodatek; předchozí sekce zůstávají tak, jak vyšly, s výjimkou dotčeného řádku tabulky.)*

## Reference

Externí zdroje ověřené 2026-08-13:

- OpenZFS: [zfs-send(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html), [zfs-receive(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html)
- Ceph RBD: [RBD Mirroring](https://docs.ceph.com/en/latest/rbd/rbd-mirroring/), [rbd(8) — export-diff / import-diff / merge-diff / fast-diff](https://docs.ceph.com/en/latest/man/8/rbd/), [Incremental Snapshots with RBD (ceph.io)](https://ceph.io/en/news/blog/2013/incremental-snapshots-with-rbd/)
- CephFS: [CephFS Snapshot Mirroring (user)](https://docs.ceph.com/en/latest/cephfs/cephfs-mirroring/), [CephFS Mirroring (dev)](https://docs.ceph.com/en/latest/dev/cephfs-mirroring/), [zdrojový rst na GitHubu](https://github.com/ceph/ceph/blob/main/doc/dev/cephfs-mirroring.rst), [PR #37876 — cephfs-mirror: synchronize directory snapshots](https://github.com/ceph/ceph/pull/37876), [Red Hat Ceph Storage 8 — File System mirrors (hardlinky)](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/8/html/file_system_guide/ceph-file-system-mirrors), [IBM Storage Ceph — File System mirrors](https://www.ibm.com/docs/en/storage-ceph/6.1.0?topic=systems-ceph-file-system-mirrors), [croit — CephFS Snapdiff Feature](https://www.croit.io/blog/introducing-the-innovative-cephfs-snapdiff-feature)
- Vydání Ceph: [Ceph Releases (index)](https://docs.ceph.com/en/latest/releases/), [v20.2.0 Tentacle](https://ceph.io/en/news/blog/2025/v20-2-0-tentacle-released/), [v20.2.1 Tentacle](https://ceph.io/en/news/blog/2026/v20-2-1-tentacle-released/), [v19.2.4 Squid](https://ceph.io/en/news/blog/2026/v19-2-4-squid-released/)
- Orchestrace: [zrepl — Configuration Overview](https://zrepl.github.io/configuration/overview.html), [zrepl — Transports](https://zrepl.github.io/configuration/transports.html), [sanoid/syncoid — README](https://github.com/jimsalterjrs/sanoid), [sanoid #672 — automatický fallback při selhání resume (otevřené)](https://github.com/jimsalterjrs/sanoid/issues/672), [Proxmox — Storage Replication (`pvesr`)](https://pve.proxmox.com/wiki/Storage_Replication), [Proxmox — PVE-zsync](https://pve.proxmox.com/wiki/PVE-zsync)
- Jednouzlový Ceph (§13): [cephadm — `--single-host-defaults`](https://docs.ceph.com/en/latest/cephadm/install/), [tracker #1317 — deadlock, kernel klient na uzlu s OSD](https://tracker.ceph.com/issues/1317), [#3076](https://tracker.ceph.com/issues/3076), [#12648](https://tracker.ceph.com/issues/12648), [Red Hat — Mounting and Unmounting Ceph File Systems](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/2/html/ceph_file_system_guide_technology_preview/mounting_and_unmounting_ceph_file_systems)
- Navazující kontext: [ZFS vs Ceph — tento repozitář](../zfs-vs-ceph/README.cs.md) (§12 šifrování, §15 spolehlivostní profily a timelines tichých korupčních bugů)

---

*Zkoumáno a sepsáno ve spolupráci s Claude (Anthropic); fakta ověřena proti zdrojům výše k 13. srpnu 2026. Tento dokument je datovaný snímek a není průběžně aktualizován.*

*© 2026 Petr Kratochvíl · Licencováno pod [CC BY 4.0](../LICENSE)*
