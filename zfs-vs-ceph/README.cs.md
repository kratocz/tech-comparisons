# ZFS vs Ceph — volba storage enginu pro malý self-hosted cluster

- **Verdikt:** ⭐ **ZFS na Proxmox VE** — platí pro kontext popsaný níže
- **Fakta ověřena:** červenec 2026 · doplňky 2026-08-01/06 (snapshot vrstva §2.5–2.6; spolehlivostní profily vč. timelines korupčních bugů Ceph i ZFS §15) · **2026-08-13 (růst po jednom disku, EC 2+2 vs RAIDZ2 §16 — vč. dvou oprav dřívějších tvrzení)** · **2026-08-14 (přepis snapshot automount vrstvy upstreamem, zatím nevydaný — §17; osm námitek držících rozhodnutí otevřené, s předem sepsaným měřicím pravidlem — §18; *oprava: `zfs rewrite` existuje a čtyři tvrzení byla chybná* — §19; kódování je v ZFS vázané na vdev a v Cephu na pool — §20; co ZFS zafixuje napevno při vytvoření a jak o tom rozhodnout — §21; objektový model, který obě předpokládají — §22; změna velikosti ZVOLu pod Proxmox VM a proč je skutečnou odpovědí obvykle discard — §23) · **2026-08-15 (oprava: block cloning je defaultně zapnutý a cross-dataset funguje — §24; kolik doopravdy stojí malý soubor a proč to není řádek tabulky o zápisu 1 bajtu — §25; volba `ashift` a oprava k §21.1 — §26; zbytek §21 projetý stejným sítem, včetně jednoho vymyšleného čísla — §27; `zfs rewrite` neaplikuje `recordsize` a jak ho tedy měnit — §28; slovník pojmů, které tabulky používají, pro všechny tři sloupce — §29; jak se kompromis liší při jednom uzlu a při třech, s opravou rozsahu — §30; proč roztažení Ceph clusteru přes internet selže, na konkrétním tvaru — §31)**
- **Jazyk:** 🇨🇿 čeština (originál) · 🇬🇧 [English version](README.md)
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Kontext: pro jaký profil se rozhodovalo

Tohle není obecné srovnání „co je lepší“. Je to reálná rozhodovací analýza z konkrétního projektu — verdikt si nárokuje platnost jen pro tenhle profil a s jiným profilem může klidně vyjít opačně:

- **Osobní cluster, fázovaný start:** začíná se **1 uzlem**, časem růst na 2–3 uzly ve **2 lokalitách** (běžné byty, mezi nimi rezidenční WAN).
- **Solo admin bez on-call** — provoz musí zvládnout jeden člověk, i „ve 3 ráno“.
- **Cost-conscious rok 2026:** DDR4 ECC v doběhu výroby (ceny rostou), HDD trh vyprodaný — každý GB RAM a každý disk navíc bolí.
- **Workload:** bulk média/foto/dokumenty (cíl ~150 TiB) + hrstka VM a služeb (Plex, Nextcloud, monitoring typu Zabbix/Grafana/Loki); zvažovaný Kubernetes.
- **Výchozí stav:** stávající single-node server `mdadm RAID6 + dm-crypt/LUKS + LVM + Btrfs` (třetí sloupec srovnávací tabulky). Z něj se migruje; po migraci poslouží jako geo DR cíl ve druhé lokalitě. Doplněk: cloudové úložiště s tvrdým měsíčním transfer stropem.
- **HA nároky:** ztráta ~1 minuty dat při pádu uzlu je přijatelná (RPO ≤ 1 min); synchronní replikace přes WAN se nepožaduje.

## Shrnutí (TL;DR)

1. ⭐ **Doporučení: ZFS na Proxmox VE, ne Ceph** — pro profil „1–3 uzly, solo admin, cost-conscious, bulk + pár služeb, fázování“ vyhrává ZFS téměř ve všem, co reálně pálí: **dává plnou hodnotu už od 1 uzlu** (Ceph je na 1 uzlu anti-pattern), **řádově méně RAM** (přímá úspora v DDR4 krizi), jednodušší provoz, čisté DR přes `send`/`recv`, lepší kapacitní efektivita na malé škále (RAIDZ2 75 % vs Ceph `size=3` 33 %).
2. **Čtyři z mých šesti původních výhrad ke ZFS se rozpustily** (§2): mixed-size (→ nový vdev), „pomalost“ (→ SMR + plný pool, ne ZFS samo), shrink (→ platí jen pro **pool**, ne pro **ZVOL**), tichá korupce (→ ZFS to řeší nativně; stávající mdadm+Btrfs stack by to dohnal jen vrstvou `dm-integrity`). **Dvě potvrzené trvají** (§2.5): procházení snapshotů = mount každého zvlášť (design nezměněn) a panic bug snapshot automountu — upstream fix až 12/2025 (PR #17943), v LTS řadě 2.3.x k 8/2026 chybí. Mitigace jsou jednoduché (`snapdir=hidden` je default, `zfs diff`/clone), ale je to nejslabší kus ZFS na Linuxu.
3. **HA nezávisí na volbě engine, ale na počtu uzlů** (§4). Na 1 uzlu není HA s ničím (ani s Ceph). ZFS HA řeší **Proxmox ZFS replikace + HA manager + arbitr** (orchestrovaný failover, RPO ~1 min) — pro daný use-case dostatečné. Přes WAN neexistuje real-time HA s žádným enginem.
4. **Ceph si drží reálnou výhodu jen ve třech věcech** (§7, §9): distribuované/shared storage (živá migrace VM, **K8s RWX PV**), nativní **S3/RGW** a automatický self-heal přes uzly. **Oba relevantní body prověřeny (§14) a ani jeden Ceph nevyžaduje** — monitoring HA (Zabbix/Grafana/Loki) se řeší app-level + RWO, Kopia zálohy S3 nepotřebují → **volba padla na ZFS**.
5. **Migrační past ZFS→Ceph je reálná, ale volitelná** (§10): existuje jen tehdy, když je cílem Ceph. Zůstat u ZFS celou cestu (1 uzel → +2 uzly + replikace) past ruší — uzel 1 se nikdy nemaže.
6. **Spolehlivostní deep research (§15) hraje pro ZFS.** ZFS má nejzralejší integrity historii — vážné bugy vzácné a opravené (dirty dnode 2023; encryption send/recv uzavřeno 2025) a **LUKS cesty se netýkají**. Ceph má rizika přesně tam, kam tenhle projekt mířil: **CephFS snapshoty + multi-MDS** (incidenty 2021→2025), **operátorské chyby** (hlavní zdroj reálných ztrát; solo admin) a **prakticky povinné PLP SSD** (plánované NVMe jsou consumer třídy).

## Srovnání v přehledu

Symboly: ✅ silná stránka · 🟡 jde s výhradou / kompromis · ❌ slabina nebo chybí · — neaplikovatelné. Hodnoceno pro **tento kontext** (1–3 uzly, homelab, solo admin, Kubernetes, bulk média + pár služeb) — ne obecně; na velkém symetrickém clusteru by řada řádků vyšla ve prospěch Ceph. Poslední sloupec = **výchozí single-node server** (mdraid + dm-crypt/LUKS + LVM + Btrfs), odkud se migruje (viz Kontext).

| Kritérium | ZFS (na Proxmox VE) | Ceph | Výchozí (mdraid+LUKS+LVM+Btrfs) |
|---|---|---|---|
| **▸ Nasazení & náklady** | | | |
| Min. smysluplný počet uzlů | ✅ **1** | ❌ 3 (2+arbitr křehké) | ✅ 1 (je single-node) |
| RAM na uzel | ✅ ~64 GB (ARC flexibilní) | ❌ ~96–128 GB (~4 GB/OSD) | ✅ nízká |
| Síť mezi uzly | ✅ 1 GbE stačí (async) | 🟡 10 GbE ~povinnost | — (single-node) |
| Nároky na SSD (PLP) | 🟡 PLP jen pro SLOG (neplánuje se) | ❌ prakticky povinné (BlueStore fsync) — consumer NVMe nestačí (§15) | ✅ bez zvláštních nároků |
| Komplexita provozu | ✅ `zpool`/`zfs`, 1 vrstva | ❌ 5+ démonů, CRUSH, PG | 🟡 4 vrstvy, víc nástrojů |
| **▸ Data & integrita** | | | |
| Auto oprava tiché korupce | ✅ nativní (scrub/resilver) | ✅ nativní (BlueStore) | ❌ **detekuje (Btrfs), neopraví** |
| Historie data-loss bugů (§15) | 🟡 vzácné, rychle opravené (dnode 2023; encryption send/recv uzavřeno 2025) | 🟡 core zralý (CERN); křehké: CephFS snapshoty+multi-MDS, operátorské chyby | 🟡 Btrfs RAID5/6 ❌ trvale (zde na LV nad mdadm ✓) |
| Kapacitní efektivita | ✅ RAIDZ2 75 % (inkrementálně rostlé ~67–70 % do rewritu, §2.1) | 🟡 size=3 33 % (EC reálně až od ~5–6 uzlů; na 3 jen k=2,m=1) | ✅ RAID6 ~75 % |
| Fragmentace při plnosti (společná všem) | 🟡 ano (CoW) | 🟡 ano (BlueStore) | 🟡 ano (Btrfs CoW) + ENOSPC |
| Defrag / úklid fragmentace | 🟡 `zfs rewrite` — defragmentace souborů i rebalance po `zpool add` jsou deklarované účely, ale bere jen operandy typu soubor a adresář, takže **ZVOLy jsou mimo**; a na téměř plném poolu navíc ztrácí účinnost (§19) | 🟡 reweight OSD / rewrite (CoW-safe, zachová snapshoty) | ✅ `defragment` + `balance` (ale **ničí reflinky**) |
| CoW granularita (1-byte write) | 🟡 128K record (laditelné 4K–1M; ZVOL 16K) | ❌ 4 MB se snapshotem (bez něj ~4K) | ✅ 4K (`nodatacow` pro DB = 0) |
| Mixed-size disky | 🟡 napříč vdev ano, uvnitř plýtvá | ✅ CRUSH weights | 🟡 mdadm smallest wins |
| Přidat disk (expand) | ✅ RAIDZ expansion (2.3) — stará data drží starý parity poměr do rewritu (§2.1) | ✅ triviální | ✅ mdadm `--grow` reshape (přepíše, bez parity caveatu) |
| Odebrat disk / shrink poolu | ❌ RAIDZ ne | ✅ `osd out` + rebalance | 🟡 mdadm reshape (jde, pomalé) |
| Zvýšení redundance (přidat paritu) | ❌ RAIDZ2→Z3 in-place ne (jen migrace) | ✅ `size` za běhu (EC profil ne) | 🟡 mdadm RAID5→6 reshape (výš neexistuje) |
| Shrink LV/ZVOL/RBD (VM disk) | ✅ ano (FS napřed) | ✅ ano (`--allow-shrink`) | ✅ `lvreduce` (FS napřed) |
| **▸ HA & dostupnost** | | | |
| Auto VM failover při pádu uzlu | ✅ Proxmox HA + replikace | ✅ ano | ❌ žádné HA |
| RPO (ztráta dat) | 🟡 ≤ 1 min (async) | ✅ 0 (sync) | ❌ jen ze zálohy |
| RTO (výpadek VM) | 🟡 ~2–5 min | 🟡 ~2–5 min | ❌ ruční obnova |
| Živá migrace VM (bez výpadku) | 🟡 jen plánovaně (s replikací) | ✅ kdykoli (shared) | ❌ |
| Auto obnova redundance po pádu uzlu | 🟡 orchestrované (failback) | ✅ auto (chce 3+ plné uzly) | ❌ (single-node) |
| Geo HA přes WAN | ❌ jen async DR | ❌ jen async DR (sync = showstopper) | ❌ |
| **▸ Funkce / workloady** | | | |
| Blokové zařízení pro VM | ✅ ZVOL (lokální) | ✅ RBD (distribuované) | ✅ LVM LV (lokální) |
| POSIX (UTF-8 názvy, ACL, nanosec časy, xattr) | ✅ plný — POSIX ACL (NFSv4 ACL na Linuxu VFS nevynutí, §2.6), volitelná UTF-8 normalizace | ✅ CephFS POSIX (drobné odchylky z distribuce) | ✅ plný nativní Linux |
| K8s persistent volumes | 🟡 local-PV RWO (`zfs-localpv`) | ✅ distribuované RWX (`ceph-csi`) | 🟡 local-PV (LVM CSI) |
| Nativní S3 / object storage | ❌ (jen MinIO/Garage navrch) | ✅ RGW | ❌ (jen MinIO navrch) |
| Deduplikace (auto, block-level) | 🟡 Fast Dedup, radši PBS | 🟡 experimentální / RGW batch | 🟡 Btrfs bees (batch) |
| Reflink klon (`cp --reflink`) | 🟡 block cloning (2.2+), defaultně zapnutý, cross-dataset podmíněně; pořád ze sebe setřásá chyby (§24) | ❌ nemá `FICLONE`; `copy_file_range` kopíruje server-side, ale alokuje nové objekty (§24) | ✅ nativní, stabilní |
| Komprese — algoritmy | ✅ lz4 (default) + zstd (laditelný) | ✅ lz4/zstd/snappy/zlib (per-pool) | ✅ zstd/lzo/zlib |
| Změna komprese u existujících dat | ✅ in-place `zfs rewrite -r` (§19) | 🟡 jen nová data (rewrite) | ✅ in-place `defragment -c` |
| Šifrování at-rest | ✅ ZFS native / LUKS | ✅ LUKS pod OSD | ✅ dm-crypt/LUKS |
| Zálohy / DR | ✅ `send`/`recv` + PBS (čisté) | 🟡 3 rozhraní, mirroring křehký | 🟡 Btrfs send + snapshoty |
| Procházení mnoha snapshotů (grep historie) | 🟡 mount per snapshot (automount `.zfs`; radši `zfs diff`/clone, §2.5) | ✅ CephFS `.snap` bez mountů (RBD ❌ map+mount ručně) | ✅ subvolume bez mountů (pozor: vlastní `st_dev`) |
| Stabilita snapshot vrstvy | ❌ automount: historie paniců; fix #17943 v LTS 2.3.x k 8/2026 chybí (§2.5) | 🟡 automount nemá, ale CephFS snapshoty samy = nejkřehčí oblast (MDS trim, §15) | ✅ subvolume snapshoty zralé |
| **▸ Škálování & fázování** | | | |
| Škálování na 10+ uzlů / PB | 🟡 per-node (replikace) | ✅ nativní | ❌ single-node |
| Fázování 1 → 3 uzly | ✅ bez migrační pasti | ❌ migrační past (nebo start 3 uzly) | ❌ není cluster |
| Zralost / komunita | ✅ 20 let, obří base | ✅ zralý, menší homelab base | ✅ zralé (Btrfs na LV, ne RAID5/6) |

### Co z toho plyne

- **ZFS vede** v nasazení, nákladech, jednoduchosti, kapacitě, fázování a DR — ve všem, co v pozici „solo, cost-conscious, fázovaný start“ pálí nejvíc.
- **Vyrovnané** je to v podstatném: ochrana dat proti korupci, VM failover, šifrování, blokové zařízení.
- **Ceph vede** v distribuovaném PV (K8s RWX), nativním S3, RPO 0, auto-recovery přes uzly a škálování.
- **Výchozí řešení** (poslední sloupec) má tři slabiny, kvůli kterým se migruje: **neopravuje tichou korupci** (jen ji detekuje přes Btrfs), **nemá HA** a jsou to **čtyři vrstvy**. ZFS všechny tři řeší v jedné vrstvě.
- 🆕 **(2026-08-01)** Nejslabší místo ZFS na Linuxu je **snapshot automount vrstva** (`.zfs/snapshot`): mount per snapshot + historie paniců/deadlocků, poslední oprava teprve 12/2025 a v LTS 2.3.x zatím není (§2.5). CephFS i Btrfs tohle řeší z principu — je to první bod, kde výchozí stack ZFS reálně poráží.
- 🆕 **(2026-08-01, spolehlivost)** Deep research (§15) hraje pro ZFS: jeho rizika (čerstvé featury, native encryption) tento návrh systematicky obchází, Cephova rizika (křehké CephFS snapshoty, operátorské chyby, povinné PLP SSD) by ho trefila přímo. Elegance snapshot *přístupu* CephFS (řádek výše) tím dostává protiváhu — snapshot *funkce* sama je u CephFS křehčí než u ZFS.

Z Ceph výher se tohoto projektu reálně týkají jen **dvě — K8s RWX PV a nativní S3** (viz §7, §14). RPO 0 jsem přijal jako nepotřebné (≤ 1 min stačí), auto-recovery i škálování míří na velké symetrické clustery, ne na plánovanou sestavu uzel 1 + uzel 2 + arbitr.

---

## 1. Východisko: proč vůbec přehodnocovat Ceph

Spouštěč byl nápad **postavit zatím jen 1 uzel** a škálovat časem (ceny RAM a HDD v roce 2026 vysoké, DDR4 ECC EOL). To odhalilo zásadní konflikt:

- **„1-node Ceph cluster“ je protimluv.** Ceph dává hodnotu z distribuce a self-healu *přes uzly*; na jednom uzlu (`size=1`) platíš celou jeho komplexitu (MON/MGR/OSD, RAM ~4 GB/OSD, ladění) a nedostaneš nic, co by ZFS nedalo jednodušeji — vlastnosti, kvůli kterým Ceph existuje, na jednom uzlu mizí.
- Naopak **ZFS je od návrhu single-node** a škáluje replikací → sedí na fázování 1 → 2 → 3 uzly bez mezikroku.

Tím se otázka „jak dělat Ceph fázovaně“ změnila na **„potřebuješ vůbec Ceph, nebo je to over-engineering pro tvůj kontext?“**

## 2. Moje původní výhrady ke ZFS a jak dopadly

| # | Výhrada | Verdikt | Řešení |
|---|---------|---------|--------|
| 1 | ZFS vyžaduje stejně velké disky (jinak plýtvá) | 🟡 platí **uvnitř vdev**, ne napříč poolem | Růst uvnitř generace = stejná velikost; generační skok (větší disky) = **nový vdev**. RAIDZ Expansion (OpenZFS 2.3, 2025) přidá disk po jednom. |
| 2 | ZFS byl vždy „velmi pomalý“ | ❌ není vlastnost ZFS | Můj dřívější test běžel na **SMR disku s téměř plným poolem** = worst case (viz §2.2). Bulk workload na CMR + dost RAM je rychlý. |
| 3 | ZFS neumí shrink (jen expand) | 🟡 platí pro **pool/RAIDZ vdev**, **ne pro ZVOL** | Shrink RAIDZ vdev nejde; shrink **ZVOL** (blokové zařízení) jde (§6). Dvě různé operace! |
| 4 | (výchozí server) tichá korupce se detekuje, ale neopraví | ✅ reálná díra | `dm-integrity` (stávající stack) nebo ZFS nativně (§3). |
| 5 | Procházení snapshotů = mount každého zvlášť (tehdy „hodně přimountovaných zařízení“) | ✅ **platí dodnes** | Design nezměněn: `.zfs/snapshot/<x>` = automount, N snapshotů = N mountů; novinka je jen auto-odpojení po 5 min (`zfs_expire_snapshot`). Obcházet přes `zfs diff`/`clone`/`send` (§2.5). |
| 6 | Kernel panic při mountu mnoha snapshotů | ✅ **reálné; upstream fix až 12/2025** | Dlouhá historie (#13131, #13327), poslední inkarnace #17659 (i na Proxmoxu); oprava PR #17943 v master, v LTS 2.3.x k 8/2026 chybí → mitigace v §2.5. |

### 2.1 Mixed-size disky

- **Uvnitř RAIDZ vdev:** smallest disk wins, větší se ořízne → plýtvání. Pravda.
- **Napříč poolem:** pool = sada vdevů; `vdev1 = 5× 30 TB` + později `vdev2 = 5× 60 TB` je v pořádku. „Za pár let větší disky“ se řeší novým vdev.
- **RAIDZ Expansion (2.3, led. 2025):** přidání jednoho disku do existujícího RAIDZ vdev online. Caveat: stará data drží **starý data:parity poměr**, dokud nejsou přepsána (kapacita roste inkrementálně); nemění RAID level ani ashift. Přesně pokrývá plán „růst 1+2 → 2+2 → 3+2“ (= RAIDZ2 s rostoucím počtem datových jednotek).

**Kapacitní cena inkrementálního růstu (příklad).** Pokud disky přidáváš po jednom vždy při ~80 % zaplnění, drží každá „vrstva“ dat parity poměr z doby zápisu — a plnou efektivitu cílové šířky nedostaneš, dokud data nepřepíšeš. Modelový růst RAIDZ2 ze 4 na 7 disků po 32 TB (80 % fill = 80 % raw, přidání při dosažení):

| Fáze | Disků | Poměr | Přidáno dat | Raw obsazeno |
|---|---|---|---|---|
| Start | 4 | 2:2 (50 %) | 51,2 TB | 102,4 TB |
| +5. disk | 5 | 3:2 (60 %) | +15,4 TB | 128 TB |
| +6. disk | 6 | 4:2 (67 %) | +17,1 TB | 153,6 TB |
| +7. disk | 7 | 5:2 (71 %) | +18,3 TB | 179,2 TB |
| **Celkem** | 7 | mix ~57 % | **~102 TB** | 179,2 TB |

Srovnání při 7 discích a 80 % fill (224 TB raw):

| Konfigurace | Uloží dat |
|---|---|
| RAIDZ2 inkrementální (tento vzorec) | **~102 TB** |
| RAIDZ2 čisté 7-disk / po rewritu (vše 5:2) | ~128 TB |
| Ceph `size=3` | ~60 TB |

Caveatem přijdeš o **~26 TB (~20 %)** proti čistému poli, ale proti Ceph `size=3` pořád vedeš o **~42 TB** — caveat náskok ZFS zmenší, neruší. Ztráta **není trvalá**: jeden `zfs send -R` (rewrite) sjednotí vše na 5:2 → ~128 TB, a při tom defragmentuje i zachová snapshoty. Velký podíl ztráty jde za **startem na 4 discích** (2:2 = 50 %, nejhorší poměr); start na 6+ discích ji zhruba půlí. Čísla jsou teoretická (bez ZFS padding/metadata overheadu ~pár %), poměry drží.

### 2.2 „Pomalost“ — příčiny

- **SMR disky** (shingled): resilver benchmark **CMR 14,5 h vs SMR 9,5 dne (16×)**; random I/O SMR je „utterly terrible“, CoW walk resilveru to zhoršuje. SMR do RAID/NAS nepatří — potopí i Btrfs a Ceph.
- **Plný pool** (CoW): nad ~80 % fillu roste fragmentace (ZFS nemá defragmentaci *volného místa* — „block pointer rewrite“ je nedodaný od 2015; `zfs rewrite` přepíše souborová data, ale alokuje z téhož volného prostoru, §19), výkon velkých bloků padá.
- **RAIDZ = IOPS jednoho disku** pro random workload (1 vdev). Pro sekvenční bulk (média, foto, backup) je rychlé.
- **Mitigace:** CMR disky, dost RAM pro ARC, SLOG pro sync writes, pool < 80 %, a **separátní SSD/NVMe pool pro VM** (random) oddělený od HDD bulk poolu.

### 2.3 Shrink — pool vs ZVOL (klíčové rozlišení)

Nezaměňovat dvě různé operace:
- **Shrink poolu / RAIDZ vdev** (ubrat fyzický disk): ❌ **nejde.** `zpool remove` umí jen mirror/stripe/cache/log/special vdev, **ne RAIDZ**.
- **Shrink ZVOL** (logické blokové zařízení uvnitř poolu): ✅ **jde** (§6). Pool zůstává, ZVOL se zmenší.

### 2.4 Tichá korupce — viz §3.

### 2.5 Snapshot vrstva na Linuxu: mount-per-snapshot a panic bug (doplněno 2026-08-01)

Obě moje historické zkušenosti (výhrady 5 a 6) se potvrdily — první jako trvalý design, druhá jako dlouhá řada reálných bugů s teprve nedávno dodanou opravou.

**Mechanika (nezměněná dodnes):** `.zfs/snapshot/<jméno>` je automount trigger — vstup do adresáře připojí snapshot jako samostatný filesystem s vlastním záznamem v mount tabulce. Prohledávání 200 snapshotů = 200 mountů. Novinka od mé tehdejší zkušenosti je jen automatické odpojování nečinných snapshotů (`zfs_expire_snapshot`, default 300 s) — které ale umí vyrobit vlastní problém (hromadná expirace stovek mountů naráz; systemd navíc při každé změně re-parsuje mountinfo).

**Panic bug (ověřeno 2026-08-01):**

- Historie: [#13131](https://github.com/openzfs/zfs/issues/13131) „Kernel Panic and DoS on massive amounts of snapshot mount/umount“ (2022, OpenZFS 2.1.2, repro Samba + hodně snapshotů), [#13327](https://github.com/openzfs/zfs/issues/13327) (procesy zaseklé v kernelu, rostoucí load).
- Poslední inkarnace: [#17659](https://github.com/openzfs/zfs/issues/17659) (8/2025) — `VERIFY(avl_find(...)) failed / PANIC at avl.c:625:avl_add()` v `zfsctl_snapshot_mount` ← `zpl_snapdir_automount`; Debian 13 / OpenZFS 2.3.2, v threadu hlášeno i na **Proxmox VE 9 (OpenZFS 2.3.4)** se `snapdir=visible` a ~57 snapshoty — panic spouštěl jakýkoli `ls`/`find`/`stat` nad `.zfs/snapshot`. Spouštěč: souběžný automount téhož snapshotu (typicky dva mount namespacy — systemd unit, kontejner). Technicky nejde o klasický kernel panic, ale `spl_panic`/VERIFY assert — vlákno usne navždy, vše další nad ZFS uvízne v D stavu, stroj postupně umře, pomůže jen tvrdý reboot.
- **Oprava:** [PR #17943](https://github.com/openzfs/zfs/pull/17943) (per-entry mutex) — **merged do master 8. 12. 2025**. Podle changelogů se ale do LTS řady 2.3.x (ověřeno 2.3.6–2.3.8) k 8/2026 nedostala → na distribucích s 2.3.x (vč. Proxmox VE 9) mitigace stále platí.
- Příbuzné: [#18073](https://github.com/openzfs/zfs/issues/18073) (12/2025) — deadlock souběžného `zfs recv` × `du` nad `.zfs/snapshot` přijímaného FS (`z_teardown_lock`); oprava #18415 vyšla v releasech 5/2026. Relevantní pro DR přes `send`/`recv`: na přijímací straně nebrouzdat `.zfs` během replikačních oken.

**Mitigace:**

1. `snapdir=hidden` (default) nechat — `.zfs` není v readdir; panic scénáře vyžadovaly `visible` nebo cílený přístup.
2. Historii číst přes `zfs diff` (změny bez mountu), `zfs clone` (jeden konkrétní snapshot) nebo explicitní `mount -t zfs pool/ds@snap`, ne rekurzivním `find` přes `.zfs/snapshot`.
3. Žádné mount namespacy nad `.zfs` (kontejnery, systemd `BindReadOnlyPaths`, chroot) — přesný trigger #17659.
4. Na přijímací straně replikace nebrouzdat `.zfs` během příjmu (#18073).

**Srovnání s alternativami:** Btrfs snapshot = subvolume uvnitř už připojeného FS, žádné mounty (caveat: každý subvolume má vlastní `st_dev` → `find -xdev`/`du -x`/`rsync -x`/`tar --one-file-system` se na hranici zastaví). CephFS = `.snap` adresář v každém adresáři, bez mountů, rekurzivní — nejelegantnější; RBD naopak nejhorší (snap → map/clone → mount ručně, crash-consistency bez `fsfreeze`). **Pro workflow „grep přes celou historii snapshotů“ je ZFS z trojice nejtěžkopádnější a historicky nejrizikovější** — jde to, ale jen disciplinovaně.

**Dopad na verdikt:** jádra use-case (bulk zápisy/čtení, `send`/`recv` DR, Proxmox replikace, PBS zálohy) se automount vrstvy nedotýkají a mitigace jsou triviální — samo o sobě to verdikt nepřeklápí. Je to ale první potvrzený bod, kde CephFS i výchozí Btrfs stack ZFS reálně porážejí — do rozhodnutí (§14) vstupuje jako vědomě nesené riziko s mitigacemi výše.

### 2.6 OpenZFS na Linuxu vs „původní ZFS“ — parita a integrační rozdíly (doplněno 2026-08-01)

Feature parita je dnes plná — od sloučení kódových bází (OpenZFS 2.0, 2020) je Linux de facto referenční implementace a FreeBSD 13+ jede tentýž kód; nativní šifrování dokonce vzniklo v ZFS-on-Linux (0.8, 2019). Rozdíly zůstaly v integraci s OS:

- **NFSv4 ACL na Linuxu nejsou vynutitelné** — linuxový VFS je neumí, reálně se jede POSIX ACL (`acltype=posixacl`); `acltype=nfsv4` je věc FreeBSD ([#4966](https://github.com/openzfs/zfs/issues/4966), WIP [PR #13186](https://github.com/openzfs/zfs/pull/13186)). Jediná skutečná funkční mezera. Pro tento projekt (domácí Samba/NFS) POSIX ACL stačí.
- **Kernel modul mimo mainline (CDDL vs GPL)** — na čistém Debianu DKMS a riziko „kernel bez modulu“ po upgrade; **na Proxmoxu odpadá** (PVE dodává kernel a ZFS společně otestované).
- **ARC žije mimo page cache** → `zfs_arc_max` nastavit ručně (jinak dvojité kešování a tahanice o RAM pod tlakem).
- **Boot environments** nejsou v základu (FreeBSD má `bectl`; na Linuxu `zfsbootmenu`/`zectl`) — pro PVE nepodstatné.
- **Nativní šifrování — dvě výhrady nezávislé na OS:** nešifruje metadata poolu (názvy datasetů a snapshotů, struktura, velikosti, časy zůstávají čitelné) a jde o nejméně prověřenou část kódu — send/recv šifrovaných datasetů neslo dlouholetou historii korupčních bugů (hlavní issue #12014 z 2021 uzavřen až 2025; opravy míří do 2.2.8/2.3.3, §15). → Potvrzuje volbu **LUKS + Tang** z §12 (šifruje vše včetně metadat); případné `send --raw` zálohy testovat obnovou.

## 3. Tichá korupce: dm-integrity vs ZFS nativně

Hlavní bolest mého stávajícího serveru (`mdraid + dm-crypt/LUKS + LVM + Btrfs`): tichou korupci (plotna, firmware disku, řadič, kabel) **Btrfs detekuje** (checksum → `EIO`), ale **mdraid neopraví** — Btrfs nevidí na paritu (je pod ním), mdraid nemá per-blok checksumy a neví, který disk lže.

**Řešení jsou dvě, obě vyžadují rebuild pole:**

1. **`dm-integrity` pod mdraid** (nebo LVM RAID s `--raidintegrity y`): dá každému sektoru checksum → při korupci vrátí **chybu čtení místo špatných dat** → RAID6 dopočítá z parity a přepíše. Převádí „tichou“ korupci na „hlasitou“, kterou RAID umí. Cena: ~10–30 % write overhead, +1 vrstva.
2. **ZFS** to má vestavěné nativně (checksum + redundance + self-heal v jedné vrstvě, 75 % efektivita u RAIDZ2).

**Důsledek pro rozhodnutí:** protože oprava korupce **stejně vyžaduje rebuild pole**, padá argument „aspoň nemusím nic měnit“. Rebuild bude tak jako tak — otázka je jen na co (ZFS vs mdadm/LVM+integrity).

## 4. HA: nezávisí na engine, ale na počtu uzlů

- **1 uzel = žádné HA s ničím** (ani single-node Ceph — není na co failovat). HA je otázka **„1 uzel vs 2 uzly“, ne „ZFS vs Ceph“.**
- **ZFS HA** (Proxmox VE):
  - **Proxmox ZFS replikace (`pvesr`) + HA manager** — async replika zvolů (interval min. 1 min) + automatický restart VM na jiném uzlu z poslední repliky. Měkké HA (RPO ~1 min, failover = restart, ne živá migrace). Pro média/foto/dokumenty/běžné služby dostatečné.
  - **DRBD-over-ZFS** — sync replika lokálního páru (RPO 0), tvrdé HA pro DB. Komplexnější.
- **Přes WAN žádné real-time HA s žádným enginem** — synchronní zápisy přes rezidenční WAN (latence, jitter, výpadky) jsou showstopper. Geo úroveň je vždy jen async DR.

### 4.1 „Orchestrovaný failover“ (co to znamená)

Ceph je **shared storage** → data dostupná ze všech uzlů → failover = triviální restart VM jinde. ZFS je **shared-nothing** → replika na druhém uzlu je samostatný, zpožděný, read-only pool. Failover proto vyžaduje vrstvu nad storage (orchestrátor), která provede: **detekci → fencing → promotion repliky → start služby → přesměrování → (po návratu) failback**. Proxmox HA manager to zvládne **automaticky** (orchestrovaný ≠ ruční), daň je RPO > 0, restart místo živé migrace, a fencing/failback komplexita.

### 4.2 Scénář „uzel 1 shoří“ (řešení bez Ceph)

Cílová sestava celá na ZFS:

| Prvek | Role |
|---|---|
| **uzel 1** (velký) | VM primár + bulk media/foto/dokumenty |
| **uzel 2** (malý/levný, např. N100) | compute + repliky VM zvolů = failover cíl (**bez bulk storage** — nese jen VM) |
| **RPi5 qdevice** (~0 Kč) | quorum arbitr (2 uzly bez arbitru = při výpadku 1 ztráta majority → HA se nespustí) |
| **DR server** (geo, druhá lokalita — bývalý hlavní stroj) | async DR pro bulk + VM (PBS, §5) |

Uzel 1 shoří → VM naskočí na uzel 2 (RPO ~1 min), bulk se obnoví z geo DR. Uzel 2 je levný, protože nese jen VM, ne úložiště.

### 4.3 Kolik HA to je — kvantifikace, failover a failback

| Metrika | Hodnota |
|---|---|
| **RPO** (ztráta dat) | ≤ 1 min (interval `pvesr`, minimum 1 min) |
| **RTO** (výpadek VM) | ~2–5 min (detekce + fencing + boot VM) |
| Failover | automatický |
| Typ | crash-consistent (VM naběhne jako po pádu) |

**Mechanika failoveru** (uzel 1 umře): `pvesr` průběžně replikuje VM zvoly na uzel 2 (≤ 1 min stará kopie) → corosync detekuje výpadek → **watchdog fencing** (uzel bez quora se sám resetuje ~60 s, ochrana proti split-brainu) → HA manager spustí VM na uzlu 2 z poslední repliky → VM nabootuje. Vyžaduje: quorum (uzel 1 + uzel 2 + **RPi qdevice**), zapnutý fencing (softdog), replikační job per VM.

**Failback** (návrat na opravený uzel 1) je *plánovaný*, proto **bez výpadku**: nastaví se replikace uzel 2 → uzel 1 (naplní ho), po doběhnutí `qm migrate <vmid> node1 --online` → **živá migrace** přenese jen finální delta + stav RAM → VM se přepne bez přerušení. Jediné okno nedostupnosti v celém cyklu je původní failover.

**Kolik HA zapnout** — rozděl VM do tří kbelíků:
- „Musí běžet pořád“ (Plex, *arr, Nextcloud, DNS…) → HA + replikace 1 min.
- „Nevadí delší výpadek“ → bez HA, jen zálohy do PBS.
- „Ani minuta ztráty“ (DB s aktivními transakcemi) → doplnit **app-level replikací** (Patroni ap.), ne kvůli tomu stavět Ceph.

## 5. Deduplikace: neřešit na storage, řeší ji PBS

- **ZFS legacy dedup** = pověstných ~5 GB RAM/TB (pro 150 TiB nereálné). **Fast Dedup (OpenZFS 2.3, 2025)** to zmírnil (DDT log/prefetch/prune/quota, DDT na special vdev), ale i tak je pomalejší než žádná dedup. Konsenzus: „dedup je teď dobrá — a stejně ji nepoužívej.“
- **Pro reálná data dedup skoro nic nedá:** média i foto jsou už komprimovaná (ratio ~1.0), dokumenty jsou malý objem.
- **Kde dedup dává smysl (VM images, zálohy) → řeší ji PBS** (Proxmox Backup Server) na aplikační vrstvě: chunk-based content-defined dedup napříč všemi zálohami, RAM-nenáročný (běží při záloze, ne inline na storage). Plus inkrementální zálohy (dirty-bitmap), komprese, client-side šifrování, retence, verify (integrity), remote sync.
- **Ceph** nemá produkční inline dedup (RADOS inline dedup je experimentální; zralé je jen RGW object dedup pro S3).

→ **Živá data na ZFS (jen komprese lz4/zstd), zálohy v PBS (s dedup). Storage-level dedup nezapínat.** PBS poběží na DR serveru = geo DR + verzované zálohy (nahrazuje původně zvažovaný Ceph mirroring — jednodušeji a věrněji).

## 6. ZVOL: blokové zařízení (RBD ekvivalent) + resize

- **ZVOL** = blokové zařízení vytesané z poolu (`zfs create -V`), lokální analog Ceph RBD. Dědí snapshoty, klony, kompresi, checksumy, `send`/`recv`, šifrování, thin provisioning. Proxmox ho používá pro VM disky.
- Rozdíl vs RBD: ZVOL je **lokální** (RBD **distribuovaný/shared**). Síťově přes iSCSI/NVMe-oF, replikace mezi uzly async.
- **Expand:** `zfs set volsize=` (větší) + resize FS uvnitř — online, triviální.
- **Shrink:** `zfs set volsize=` (menší) **jde**, ale usekne data za hranicí **bez varování** (žádná pojistka jako RBD `--allow-shrink`) → nutné **napřed zmenšit FS uvnitř**. Postup je identický s `lvreduce` nad LVM+Btrfs (FS shrink first, pak volume). Pojistka: `zfs snapshot` před shrinkem (instantní rollback).
- **Snapshoty + resize:** resize funguje s existujícími snapshoty (netřeba je mazat). U shrinku ale snapshoty drží staré bloky → **místo v poolu se nevrátí, dokud pre-shrink snapshoty existují**. Doporučený postup: snapshot nech → shrink → ověř → teprve pak snapshot smaž (bezpečnost i uvolnění místa).

## 7. Kubernetes a S3 — poslední reálné důvody pro Ceph

Projekt zvažuje Kubernetes. To je oblast, kde Ceph má reálnou výhodu a kterou nelze odbýt:

- **K8s persistent volumes:**
  - **Ceph RBD (ceph-csi)** — zralé dynamic provisioning, **distribuované PV** (pod failover na jiný uzel vidí totéž PV), RWX přes CephFS.
  - **ZFS (openebs `zfs-localpv`)** — dynamic provisioning zvolů, ale **local PV** (pod běží tam, kde je pool; failover jen s daty replikovanými jinam). RWO, ne distribuované RWX.
  - **Rozhodovací otázka:** potřebuješ pro K8s workloady **RWX / distribuované PV** (víc podů sdílí totéž volume, failover bez závislosti na umístění), nebo stačí **RWO local-PV + replikace/failover**? Pro většinu self-hosted služeb (Plex, foto, dokumenty, DB s vlastní replikací) stačí RWO. RWX potřebuje jen sdílený filesystem mezi replikami.
- **K8s control plane HA** (etcd 3-node quorum) je **samostatná vrstva nezávislá na storage enginu** — řeší se 3 (i malými) control-plane uzly, ne volbou ZFS/Ceph.
- **S3/RGW object storage:** Ceph má nativně; ZFS ne (jen přes MinIO/Garage nad filesystémem). Otázka: běží na clusteru něco, co vyžaduje S3 API?

## 8. Výhody ZFS pro tento kontext (souhrn)

1. **Plná hodnota od 1 uzlu + žádná migrační past** (§10) — sedí na fázování.
2. **Řádově méně RAM** — v mém návrhu vychází ZFS uzel na ~64 GB, plný Ceph uzel na 96–128 GB. Přímá úspora v DDR4 krizi.
3. **Jednoduchost** — `zpool`/`zfs`, jedna vrstva, provoz „ve 3 ráno“ pro solo admina bez on-call.
4. **`send`/`recv`** — nejčistší inkrementální, verzované, bit-exact DR (na DR server).
5. **Kapacitní efektivita** — RAIDZ2 75 % vs Ceph `size=3` 33 %; u 150 TiB desítky disků rozdílu.
6. **Levnější síť** — Ceph chce 10 GbE povinně; ZFS single-node žádnou cluster síť, replikace i na 1 GbE.
7. **Integrita, snapshoty, komprese, šifrování, ZVOL** — vše v jedné vrstvě.

## 9. Kde Ceph vyhrává (poctivě)

- **Distribuované/shared storage** — RBD/CephFS ze všech uzlů → živá migrace VM bez výpadku + K8s RWX PV. ZFS je shared-nothing.
- **RPO=0 HA přes cluster** (ZFS replikace je async ~1 min). Pozn.: přes WAN nedostaneš RPO=0 ani s Ceph.
- **Škálování na 10+ uzlů / petabajty / mnoho paralelních klientů** — Ceph je pro to stavěný.
- **Nativní S3/RGW.**
- **Automatický self-heal přes uzly.**

Z toho jsou pro tento projekt reálně relevantní jen **distribuované K8s PV** a **S3** (§7) — a obojí by přes WAN stejně fungovalo jen lokálně, ne mezi lokalitami.

## 10. Migrační past ZFS→Ceph (a jak se jí vyhnout)

ZFS a Ceph jsou nekompatibilní světy — nejde konvertovat, jen kopírovat (ztráta snapshotů). Zapojení uzlu 1 (ZFS) do Ceph clusteru vyžaduje ho přeformátovat → vyprázdnit na uzly 2+3 → po dobu okna běží `size=2` (tolerance 1 selhání).

**Past existuje jen tehdy, když je cílem Ceph.** Vyhnutí:
1. **Zůstat u ZFS celou cestu** (1 uzel → +2 uzly + replikace) → uzel 1 se nikdy nemaže, žádná past.
2. Jestli Ceph musí být → **nezačínat ZFS**, postavit rovnou 2 uzly Ceph od začátku.
3. Okno snížené redundance při migraci kryje **geo záloha** (DR server + cloud) — i kdyby v okně umřel disk, existuje DR kopie.

## 11. Doporučená cílová architektura (ZFS cesta)

- **OS/hypervisor:** Proxmox VE 9 (staví na OpenZFS 2.3 → RAIDZ Expansion i Fast Dedup), **root-on-ZFS mirror** (nahradí dosavadní mdadm OS mirror; snapshoty OS / boot environments zdarma).
- **Storage:** ZFS — RAIDZ2 pro HDD bulk (media/foto/dokumenty), mirror/RAIDZ SSD pool pro VM zvoly (random workload oddělený od bulk).
- **HA (až 2. uzel):** Proxmox ZFS replikace + HA manager + RPi5 qdevice arbitr (§4.2).
- **Zálohy/DR:** PBS na DR serveru (§5) — verzované, dedup, remote sync; cloud pro nejcennější subset (fotky/dokumenty) v rámci jeho tvrdého měsíčního transfer stropu.
- **Fázování:** uzel 1 (ZFS, plná hodnota hned) → +uzel 2 malý + arbitr (HA, bez smazání) → případně uzel 3 dle financí.

## 12. Šifrování at-rest

**Threat model:** krádež celého uzlu → data nedostupná. Klíčové je, aby se **odemykač klíče nedal získat z ukradeného stroje**.

**Model dvou klíčů** (LUKS i ZFS native encryption): *master key* šifruje data a leží na disku, ale **sám zašifrovaný**; odemyká ho *wrapping key*, který na disku být nesmí. `/etc/crypttab` je jen konfigurace (co čím odemknout), ne klíč.

**Kde vzít wrapping key** (proti krádeži uzlu):

| Metoda | Vhodnost |
|---|---|
| TPM samotný | ❌ jede s deskou → ukradený uzel klíč vydá (TPM+PIN pomůže, ale je to interakce) |
| Passphrase + dropbear SSH | ✅ klíč v hlavě, remote unlock po rebootu; daň: ruční |
| **Tang/Clevis (network-bound)** | ⭐ odemkne se jen v domácí síti (Tang na RPi arbitru); vynesený uzel = zamčeno; doma auto-boot |

**Doporučení: LUKS + Clevis/Tang** (Tang na RPi5 arbitru), ideálně i encrypted root. Na Proxmoxu (Debian) jsou to standardní balíčky (`clevis-luks`, `clevis-initramfs`, `tang`), ale setup je ruční (instalátor šifrování root nenabízí). DR/zálohy šifruje **PBS client-side** nezávisle. Alternativa: ZFS native encryption + passphrase (umí `send --raw` = šifrované repliky bez klíče na DR straně), ale Tang unlock je s ním DIY — a navíc nešifruje metadata poolu (názvy datasetů/snapshotů, velikosti, časy) a jde o nejméně prověřenou část ZFS: dlouholetá historie send/recv korupčních bugů na šifrovaných datasetech byla uzavřena až v roce 2025 (§2.6, §15). Další bod pro LUKS.

**Past:** klíč (keyfile) na **nešifrovaném rootu** = útočník ho z ukradeného disku přečte → šifrování k ničemu. Proto odemykač zvenčí (Tang/passphrase), ne keyfile na plaintext disku.

**Hranice:** chrání *vypnutý* ukradený stroj; běžící/odemčený je jiná věc. **BMC/IPMI je samostatný attack surface** — mimo rozsah této analýzy.

## 13. Fill ratio a reálně použitelná kapacita

Fill strop je u obou podobný (~80 %), takže **sám o sobě velký rozdíl nedělá** — hlavní kapacitní rozdíl je replikační overhead (viz „Srovnání v přehledu“, řádek Kapacitní efektivita).

- **ZFS:** ~80 % kvůli výkonu/fragmentaci (CoW); nad to zpomaluje (ne ztráta dat), nad ~95 % vážně. Praxe (45Drives) uvádí reálný strop spíš ~90 %; nad 90 % ale existuje i hlášený případ selhání `zpool import` po výpadku napájení ([#18041](https://github.com/openzfs/zfs/issues/18041)) — strop 80 % má tedy zdravou rezervu.
- **Ceph:** thresholdy `nearfull` 85 %, `backfillfull` 90 %, `full` 95 % (zápisy stop). Navíc **rezerva na self-heal** — výpadek OSD/uzlu se musí vejít na zbývající → prakticky ~75–80 %, **na málo uzlech míň** (výpadek 1 ze 3 = 33 % musí mít kam). ZFS tuto rezervu nepotřebuje.

**Reálně použitelné z každých 100 TB nakoupených disků** (usable × 80 % fill):

| Konfigurace | Reálně data |
|---|---|
| ZFS RAIDZ2 (75 % × 80 %) | ~60 TB |
| Ceph `size=3` (33 % × 80 %) | ~27 TB |

U 150 TiB cíle je ten rozdíl desítky disků a klidně 100 000+ Kč v železe — ale pochází z replikace, ne z fill ratio.

## 14. Rozhodnutí

Čtyři otázky, které se v průběhu analýzy otevřely, dopadly takhle:

1. **K8s persistent volumes — RWX není potřeba.** Plánované aplikace (Zabbix, Grafana, Loki, Prometheus) dělají HA na aplikační vrstvě (víc replik + sdílená DB / Patroni), ne přes sdílený storage → `zfs-localpv` (RWO) + Proxmox HA stačí.
2. **S3/RGW — není potřeba.** Jediný zvažovaný důvod (zálohy přes Kopia) S3 nevyžaduje — Kopia umí filesystem/SFTP repozitář; nice-to-have pokryje MinIO nad ZFS.
3. **HA model — přijat.** Orchestrovaný failover (RPO ≤ 1 min, RTO ~2–5 min, failback živou migrací; §4.3) je pro tento profil dostatečný.
4. **Snapshot automount vrstva — vědomě nesené riziko (doplněno 2026-08-01).** Potvrzená slabina ZFS na Linuxu (§2.5): mount-per-snapshot + historie paniců; upstream fix (12/2025) je zatím mimo LTS řadu 2.3.x. Nese se s mitigacemi (`snapdir=hidden`, `zfs diff`/clone, žádné mount namespacy nad `.zfs`) — jádra use-case se nedotýká.

**→ Verdikt: ZFS na Proxmox VE.** Ceph by na 1–3 uzlech nepřidal nic, co by tenhle projekt reálně využil — platil by se trvalou daní v RAM, síti a provozní komplexitě. Bod 4 je jediné místo, kde CephFS objektivně vede — pro tento profil ale nepřeváží zbytek; spolehlivostní profily (§15) verdikt navíc dále podpírají (rizika ZFS tento návrh obchází, rizika Ceph by ho trefila přímo). Na velkém symetrickém clusteru s mnoha klienty by verdikt klidně vyšel opačně — přesně proto je celá analýza ukotvená ke kontextu v úvodu.

## 15. Riziko ztráty dat: spolehlivostní profily (doplněno 2026-08-01)

Druhý doplněk vychází z nezávislé deep-research analýzy spolehlivosti ZFS/Btrfs/Ceph na Debianu/Ubuntu ([artefakt](https://claude.ai/public/artifacts/49c04b36-c45d-4b73-8652-c79f39de5ad5), 319 zdrojů) a navazující diskuse; nosná tvrzení ověřena proti primárním zdrojům 2026-08-01. Závěr pro tento kontext: **profily rizik hrají pro ZFS** — jeho slabiny tento návrh systematicky obchází, Cephovy by ho trefily přímo.

**ZFS — nejzralejší integrity historie; rizika koncentrovaná a obejitelná:**

**Doložené korupční bugy (Open)ZFS na Linuxu — timeline** (doplněno 2026-08-06):

| Kdy | Co | Vrstva | Oprava |
|---|---|---|---|
| 2016 | **hole_birth** — tichá korupce inkrementálních `zfs send` streamů: příjemce nehlásí chybu, ale cíl ≠ zdroj (místo nul dorazí stará data; [#4996](https://github.com/openzfs/zfs/issues/4996), [Debian #830824](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=830824)) | send/recv | ZoL 0.6.5.8 / 0.7.0-rc1: sender defaultně ignoruje vadná hole_birth metadata ([FAQ](https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ%20hole%20birth.html)) |
| 3–4/2018 | Regrese v 0.7.7: „mizející“ soubory (ztracené hardlinky) + falešné ENOSPC při kopírování adresářů s mnoha soubory; reálná ztráta dat dle [The Register](https://www.theregister.com/2018/04/10/zfs_on_linux_data_loss_fixed/) nulová | ZPL/VFS | urgentní 0.7.8 za 3 dny (revert) |
| 2021→2025 | Native encryption × send/recv ([#12014](https://github.com/openzfs/zfs/issues/12014) a příbuzné): permanent errors šifrovaných snapshotů při zálohách | šifrování | uzavřeno až 2025 (PR #17340; opravy 2.2.8/2.3.3) |
| 11/2023 | **Dirty dnode** ([#15526](https://github.com/openzfs/zfs/issues/15526)): tichá korupce při kopírování (trigger coreutils 9.x + block cloning), **latentní ~od 2013**, scrub ji neviděl | core (dnode check) | 2.2.2 / 2.1.14 (12/2023) |

- **Lekce:** dva ze čtyř bugů byly **tiché** — checksumy nechytí bug, který sedí nad nimi → zálohy + ověřování replik (scrub na cíli, testovací restore); hole_birth je přesně scénář send/recv DR. Rizika sedí v send cestách a čerstvých featurách, ne v základní RAIDZ/mirror zápisové cestě → konzervativní verze, novinky nechat uležet (block cloning je defaultně zapnutý a pořád se opravuje, §24).
- **Šifrování: cesty LUKS + Tang (§12) se celá encryption saga netýká.** Debian 13 / Ubuntu 24.04 / PVE 9 dnes vozí verze se všemi uvedenými fixy.
- Plnost: viz §13 — praxe snese ~90 %, ale strop 80 % má zdravou rezervu (vč. [#18041](https://github.com/openzfs/zfs/issues/18041)).

**Ceph — core zralý na obří škále, ale rizika přesně tam, kam tento projekt mířil:**

- **CephFS snapshoty + multi-MDS = historicky nejkřehčí oblast.** Oficiální best practice ještě v éře Mimic (2018) zněla „[use a single active MDS and do not use snapshots](https://docs.ceph.com/en/mimic/cephfs/best-practices/)“; dnes jsou obě featury podporované, ale provozní incidenty se táhnou napříč verzemi: [#53192](https://tracker.ceph.com/issues/53192) (11/2021, Nautilus) — se snapshoty propad `rm -rf` ze ~400 na ~25 unlinků/s (`SnapRealm::split_at`, 100 % CPU MDS), degradace přetrvala i po smazání všech snapshotů a plné dořešení přišlo až s v20.2.0 (Tentacle, 11/2025) — **4 roky**; [Silvenga 7/2024](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/) — korupce MDS journalu při snapshot trimmingu po hromadném mazání (multi-MDS), pády MDS a riskantní recovery; [Rook #15273](https://github.com/rook/rook/issues/15273) (1/2025, Squid 19.2.0) — skupinové snapshoty ~20 PVC → latenční špičky a MDS „behind on trims“. Pro projekt se snapshoty jako centrálním workflow přímý zásah — a na rozdíl od ZFS automount bugu (§2.5, má merged fix) jde o chování architektury MDS, ne o jeden bug s opravou.
**Doložené korupční bugy Ceph — timeline** (doplněno 2026-08-02, jako tabulka 2026-08-06):

| Kdy | Co | Vrstva | Oprava |
|---|---|---|---|
| 11/2019 | Fastbmap alokátor v 14.2.3/14.2.4 — RocksDB checksum errors; trefoval **jen OSD s odděleným DB/WAL zařízením** (doporučenou konfiguraci „block.db na SSD“; [advisory](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/X6TNSDQK5DVKO6XFJW3DMJAJV63PLDYM/)) | BlueStore | expedovaná 14.2.5 |
| 5/2020 | `bluefs_preextend_wal_files` → korupce RocksDB WAL ([#45613](https://tracker.ceph.com/issues/45613)) | BlueFS | volba vypnuta, fix 15.2.x |
| 9/2020 | *Edinburgh:* korupce MDS journalu po síťové rekonfiguraci → kaskáda pádů MDS, týden disaster recovery na ~40TB FS; data zachráněna ([postmortem](https://blogs.ed.ac.uk/mhagdorn/2020/09/09/anatomy-of-a-cephfs-disaster/)) | CephFS/MDS | — (provozní havárie) |
| 2021 | BlueFS špatně zvládal **>4GB zápisy z RocksDB** → potenciální korupce ([openSUSE advisory 5/2021](https://osv.dev/vulnerability/openSUSE-SU-2021:0672-1)) | BlueFS | 14.2.22 / 15.2.13 |
| 10–12/2021 | Pacific **OMAP konverze** při upgradu: `quick_fix/repair` → poškozené OMAP klíče ([#53062](https://tracker.ceph.com/issues/53062), „IMPORTANT NOTICE“) | upgrade cesta | 16.2.7 (12/2021) |
| 7/2024 | *Silvenga:* korupce MDS journalu při snapshot trimmingu po hromadném mazání; zachránily zálohy ([postmortem](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/)) | CephFS/MDS | — (provozní havárie) |

Vzorec: **RADOS core na zdravém HW doložený případ „sám ztratil data“ nemá** — čisté korupční bugy se koncentrují do 2019–2021 (zrání BlueStore: BlueFS↔RocksDB interakce, upgrade konverze); co je čerstvé (2024), je MDS/CephFS metadata vrstva. Každý z bugů ale vyžadoval včasnou reakci na advisory (sledovat ceph-users, nejezdit na point-release první den) = další položka provozní daně solo admina. Srovnání s tabulkou ZFS výše: ZFS jich má méně, ale dva tiché.
- **Většina reálných ztrát dat v Ceph = operátorské chyby, ne bugy:** `min_size=1` (nejčastější), `size=2`, zásahy do OSD během degradace/backfillu, kopírované `--yes-i-really-mean-it` příkazy, ignorovaný HEALTH_WARN. Riziko roste u **solo admina bez každodenní Ceph rutiny** — přesně tento profil (§8).
- **Enterprise SSD s PLP prakticky povinné** (BlueStore dělá časté fsync; consumer SSD bez PLP = propad sync zápisů + riziko korupce při výpadku napájení). Plánovaná sestava stojí na consumer NVMe → Ceph cesta by znamenala dražší disky. ZFS potřebuje PLP jen pro SLOG, který se neplánuje.
- **Debian balíčky mají doloženou historii problémů** (Reef 18.2.0 pro bookworm vůbec nešel sestavit; dashboard PyO3 pády) → upstream doporučuje cephadm v kontejnerech = další provozní vrstva navíc.

**Btrfs (výchozí stack):** RAID5/6 write hole je oficiálně „not for production“ i v roce 2026 ([RAID56 status](https://btrfs.readthedocs.io/en/latest/btrfs-man5.html)) — výchozí stack (Btrfs na LV **nad mdadm RAID6**, ne Btrfs RAID5/6) se mu správně vyhýbá; profily single/RAID1/10 jsou zralé (Meta na milionech strojů, default Fedora/openSUSE). Vlajková otrava ENOSPC/balance trvá.

**Hardware napříč:** ECC doporučené, ne povinné — „scrub of death“ je mýtus (Ahrens: ZFS bez ECC není rizikovější než jiný FS bez ECC; priorita: zálohy → checksumující FS → UPS → ECC). Skutečné riziko všech tří: disky lžoucí o flushi a QLC SSD pod zápisovou zátěží.

## 16. Růst po jednom disku: EC 2+2 vs RAIDZ2 (doplněno 2026-08-13)

Třetí doplněk vznikl z upřesnění, které mění zadání: **nekupuju cílovou sestavu najednou, ale začínám 3–4 disky a rozšiřuju po jednom.** Rozšiřitelnost po jednom disku je klasicky doména Cephu a klasická slabina RAIDZ, takže stálo za to ověřit, jestli to verdikt neotáčí. Neotočilo — ale cestou jsem musel **opravit dvě vlastní tvrzení z předchozích verzí tohoto dokumentu**, obě ve prospěch Cephu.

### 16.1 Kolik disků potřebuje tolerance dvou výpadků

`m` je přímo počet ztratitelných OSD: *„The value of M defines how many OSDs can be lost simultaneously without losing any data.“* Pro toleranci 2 tedy `m=2` a celkem `k+m` failure domén.

| varianta | disků | použitelná kapacita | efektivita |
|---|---:|---:|---:|
| Ceph replica3 | 3 | 1 disk | 33 % |
| Ceph replica3 | 4 | 1,33 disku | 33 % |
| **Ceph EC 2+2** | **4** | **2 disky** | **50 %** |
| **ZFS RAIDZ2** | **4** | **2 disky** | **50 %** |
| ZFS RAIDZ1 | 3 | 2 disky | 67 %, ale snese jen 1 |

Profil `k=1, m=2` (3 disky, tolerance 2) je matematicky degenerovaný — Reed-Solomon s jediným datovým chunkem produkuje kopie, tedy totéž co `size=3` při stejné 33% efektivitě. Jestli ho Ceph rovnou odmítne, jsem neověřil (dokumentace minimum `k` neuvádí), ale nemá důvod existovat.

**Praktický důsledek:** 3 disky v RAIDZ1 a 4 v RAIDZ2 dají shodně dva disky užitečné kapacity, protože v obou případech jsou to dva datové disky. Čtvrtý disk tedy nekupuje kapacitu, ale celou úroveň odolnosti. U dnešních kapacit kolem 30 TB, kde resilver trvá dny a čte přitom všechny ostatní disky, je RAIDZ1 špatný obchod.

### 16.2 „Snese 2“ znamená u každého enginu něco jiného

⚠️ **Oprava dřívějšího tvrzení.** V předchozích verzích tohoto dokumentu jsem toleranci výpadků u ZFS a Cephu stavěl vedle sebe jako rovnocennou. Není.

Ceph definuje `min_size` jako *„the minimum number of active replicas (or shards) required for PGs to be active and thus for I/O operations to proceed“* a PG bez stavu `active` neobsluhuje požadavky. Pro EC dokumentace doporučuje *„min_size be K+1 or greater to prevent loss of writes and loss of data“*.

| stav | ZFS RAIDZ2 (4 disky) | Ceph EC 2+2 (4 OSD) | Ceph replica3 (4 OSD) |
|---|---|---|---|
| ztráta 1 disku | čte i zapisuje | čte i zapisuje | čte i zapisuje |
| ztráta 2 disků | **čte i zapisuje** | data přežijí, ale `min_size=3` → **I/O stojí** | část PG má 1 kopii pod `min_size=2` → **část dat nedostupná** |
| self-heal bez náhradního disku | ne (potřebuje hot spare) | ne (4 shardy chtějí 4 OSD) | ano, pokud se data vejdou na zbylé OSD |

U replikace navíc **rezerva na self-heal** ukrajuje z nominální kapacity: aby se cluster po ztrátě disku dorovnal zpět na tři kopie, musí se data vejít na zbývající OSD. Na čtyřech discích to znamená strop kolem jednoho disku užitečných dat místo nominální třetiny ze čtyř, a po započtení `nearfull`/`full` poměrů ještě míň. Na třech discích nelze tři kopie umístit na dva přeživší vůbec.

### 16.3 RAIDZ expansion existuje — a tím padá jedna z historických výhrad

**Proxmox VE 9.0 přišel se ZFS 2.3.3** a rozšiřování RAIDZ je v něm oficiálně podporované. Disk se přidá přes `zpool attach`, předtím je nutný `zpool upgrade` kvůli feature flagu `raidz_expansion`. Odolnost zůstává: *„Fault tolerance is unchanged — a RAID-Z2 stays a RAID-Z2.“*

**Starší verze tohoto dokumentu počítaly s tím, že RAIDZ vdev má navždy pevnou šířku.** To platilo do ZFS 2.2; od 2.3 už ne.

Dvě výhrady:

- **Stará data si nesou původní poměr:** *„blocks written before the expansion keep their original data-to-parity ratio, just spread over more disks. Only newly written blocks use the wider ratio.“*
- **Otevřené [OpenZFS #17784](https://github.com/openzfs/zfs/issues/17784)** hlásí po expanzi RAIDZ2 ze 4 na 5 disků zhruba dvojnásobnou fyzickou alokaci proti logickým datům (20,7 TiB na 10,3 TiB) a ztrátu přes 10 TiB očekávané kapacity; související PR #18324 ho nezavřel. Reportér ale jede vývojový build 2.4.99, ne 2.3.x LTS — **dopad na verzi v Proxmoxu jsem neověřil**. Před nasazením expanze na ostrý pool ji vyzkoušet ve VM s virtuálními disky; trvá to minuty.

Expanze přečte a přepíše všechen alokovaný prostor, takže se vyplatí rozšiřovat dřív než později. Hrubý odhad při ~200 MB/s sekvenčně: 10 TB obsazených ≈ 14 hodin, 30 TB ≈ 1,7 dne, 60 TB ≈ 3,5 dne (nenaměřeno, jen řádová orientace).

### 16.4 EC profil existujícího poolu změnit nelze

Dokumentace Cephu je kategorická: *„the profile cannot be modified after the pool is created“* a *„There is no way to alter the profile of a pool after the pool has been created.“* Přechod z 2+2 na 3+2 tedy znamená **nový pool**. Standardní kopírovací nástroj přitom na EC poolech nefunguje — `rados cppool` vrací `error copying pool testpool => newpool: (95) Operation not supported`. Flag `--force` u `ceph osd erasure-code-profile set` jen přepíše pojmenovaný profil (a chce k tomu `--yes-i-really-mean-it`); na existující pooly zpětně nesáhne.

Dvě zmírnění:

1. **CephFS umí víc datových poolů.** Nová data lze nasměrovat do širšího poolu přes layout (`setfattr -n ceph.dir.layout -v pool=ec42 /ceph/logs`) bez kopírování těch starých; oba pooly sdílejí tytéž OSD.
2. **Pool Migration je v přípravě.** Vývojová dokumentace popisuje návrh cílený na release **Umbrella**, který má umožnit *„change the erasure code profile (and in particular the choice of K and M) non-disruptively“* i *„Converting between replica and erasure coded pools“*, a to bez výpadku. Zatím je to **návrh, ne funkce**: první verze bude vyžadovat prázdný cílový pool, nepůjde ji zrušit ani pozastavit a bude chtít upgradované všechny klienty i démony.

### 16.5 Oprava (2026-08-13): kapacitně jsou při růstu na remíze

⚠️ **Druhá a podstatnější oprava.** Nabízelo se říct „EC je zamčené na 50 %, zatímco RAIDZ2 roste na 67 %“. To je nefér ve dvou směrech: u CephFS lze přidat druhý pool se širším profilem (§16.4), takže „zamčeno navždy“ neplatí — a hlavně **RAIDZ expansion má úplně tutéž vlastnost, kterou bych Cephu vyčítal**: stará data si nesou původní poměr, takže ani u ZFS se pool jako celek na vyšší efektivitu nepřepočítá.

Efektivita **čerstvě zapsaných** dat je u obou stejná:

| disků | šířka RAIDZ2 | odpovídající EC profil | efektivita |
|---:|---|---|---:|
| 4 | 2+2 | EC 2+2 | 50 % |
| 5 | 3+2 | EC 3+2 | 60 % |
| 6 | 4+2 | EC 4+2 | 67 % |

Rozdíl tedy **není kapacitní, ale provozní**: u ZFS je to jeden `zpool attach` a nová data se automaticky píšou širší; u Cephu je to založení dalšího poolu a správa layoutů po adresářích, s několika pooly různé geometrie vedle sebe.

### 16.6 Výkon malých zápisů — tady je ten skutečný rozdíl

Vývojová dokumentace Cephu popisuje pro `m=2` techniku `parity-delta-write` s nákladem *„just 3 read and 3 writes to perform an overwrite of less than one chunk“* — tedy šest diskových operací, z toho tři čtení na kritické cestě, proti třem paralelním zápisům u replikace. ZFS RAIDZ je copy-on-write: malý zápis se stane novým užším stripem s vlastní paritou, tedy **bez read-modify-write vůbec**.

Měření potvrzují, že `k=2` je nejhorší konec spektra. Oficiální benchmark Fast EC v Tentacle ukazuje, že *„wider erasure codes performance improves as K increases“*, a i s Fast EC na NVMe si trojnásobná replikace drží u mixu 70/30 na 16K zhruba **o 50 % lepší výkon** než EC. Provozní zkušenost s rotačními disky (ceph-users): *„EC pools have high throughput but low IOP/s compared with replicated pools“*, s testovanými `k` = 5 až 12 a závěrem *„Best results in decreasing order: k=8, k=6. All other choices were poor.“*

K verzím: **Proxmox VE 9.2 vede jako výchozí Ceph Tentacle 20.2.1**, takže Fast EC je dostupná — ale zisky v benchmarku plynou z `stripe_unit` 16K proti výchozím 4K, tedy z konfigurace, ne ze samotného upgradu.

### 16.7 Závěr pro tenhle scénář

Pro **jeden uzel se čtyřmi disky, rostoucí po jednom** vychází **ZFS RAIDZ2** — ne kvůli kapacitě, tam je remíza (§16.5), ale proto, že Ceph v téhle konfiguraci platí režii malých zápisů (§16.6), zastaví se při dvou výpadcích (§16.2), vyžaduje replikovaný metadata pool na SSD a k němu enterprise SSD s PLP (§15), a přidává správu více poolů. Jedinou reálnou protihodnotou je self-heal bez náhradního disku, jakmile je OSD víc než `k+m`.

**Co by závěr otočilo:** růst po **uzlech** místo po discích — pak je Ceph správná volba od začátku a ušetří pozdější migraci (§10); nebo workload převážně **velké sekvenční zápisy** (archiv médií, zálohy) místo VM disků, kde režie read-modify-write mizí.

## 17. Aktualizace (2026-08-14): snapshot automount vrstva byla přepsána — a není v žádném vydání

§2.5 označila za opravu PR [#17943](https://github.com/openzfs/zfs/pull/17943) a zaznamenala, že se nedostala do 2.3.x LTS řady. Obě tvrzení dál platí. Změnil se **tvar** té opravy, a stojí za to ho zapsat přesně, protože titulek zní líp než praktická situace.

**#17943 opravil jednu race condition, ne celou linii.** Jeho název je přesný: *"Fix snapshot automount race causing AVL tree panic"* (slito 2025-12-08). Dvě issues, které §2.5 bere jako tu linii — [#13131](https://github.com/openzfs/zfs/issues/13131) *"Kernel Panic and DoS on massive amounts of snapshot mount/umount"* (2022) a [#13327](https://github.com/openzfs/zfs/issues/13327) *"processes stuck in kernel forever"* —, zůstaly přes něj otevřené.

**Zavřely se 2026-08-06, a to přepisem.** Maintainer obě uzavřel s poznámkou *"Resolved by* [#18847](https://github.com/openzfs/zfs/pull/18847)*"* — *"Linux: rewrite snapshot automount facility"*. Není to záplata: commit `e8e30769` přistál v masteru **2026-06-18** a v průběhu července ho následovala dávka nových ZTS testů (odpojení snapdiru za probíhajícího přístupu, více automountů přes více mountů základního datasetu, chování při shutdownu, když je automount přesunutý nebo bind-mountnutý jinam). Zavřely se i dvě sousední issues: [#17659](https://github.com/openzfs/zfs/issues/17659), panic vyvolaný systemd, který potkal i Proxmox, 2025-12-12, a [#18073](https://github.com/openzfs/zfs/issues/18073), deadlock `recv` × `du`, 2026-04-08.

**A nic z toho není vydané.** Ověřeno 2026-08-14:

| | |
|---|---|
| Přepis v masteru | 2026-06-18 (`e8e30769`) |
| Poslední vydání | 2.4.3, 2.3.8, 2.2.10 — všechna **2026-06-12** |
| Nejnovější commit ve `zfs-2.3-release` | 2026-06-08 |

Přepis přistál **šest dní po** posledních vydáních a do 2.3.x LTS větve backportovaný není. Na čemkoli, co dnes jde nainstalovat — včetně toho, co dodává Proxmox —, platí chování před přepisem.

**Co to mění pro verdikt: nic.** Závěr §2.5 zůstává beze změny: je to nejslabší část ZFS na Linuxu a zmírnění jsou levná (`snapdir=hidden` je default; historii procházet přes `zfs diff` nebo klon místo `.zfs`; nechodit do `.zfs` na přijímací straně během `recv`). Ta zmírnění zůstávají platnou radou, ne provizoriem do příští aktualizace.

**Co to mění pro výhled: ta třída problémů vypadá upstreamem uzavřeně.** Přepis plus účelově psaná sada testů je silnější signál než oprava jedné race — vývojáři to vzali jako návrhový problém, ne jako bug. Sledovat je potřeba první vydání obsahující `e8e30769` (2.4.4 nebo novější) a jestli vůbec někdy přijde backport do 2.3.x. Dokud nenastane jedno z toho, řádek „stabilita snapshot vrstvy“ ve srovnávací tabulce platí přesně tak, jak vyšel.

*§2.5 zůstává tak, jak byla napsána. Tohle je stárnutí, ne chyba: sekce byla k 2026-08-01 přesná a svět se pod ní pohnul, což je přesně to, na co datovaný snímek je.*

## 18. Námitky, které drží rozhodnutí otevřené (doplněno 2026-08-14)

Tenhle dokument došel v §14 k verdiktu. Rok nato jsem podle něj nejednal — a ta mezera je sama o sobě informace. Srovnání, které zaznamená jen závěr a už ne důvody, proč ho vlastní autor nepřijal, je méně užitečné než takové, které přizná obojí. Následuje osm námitek, kvůli kterým se pořád dívám po Cephu, u každé to, co doopravdy platí, a jestli je Ceph tím, co ji řeší.

Nepříjemné shrnutí zní, že **Ceph řeší jednu z osmi**, dvě zhoršuje a tří se netýká.

| # | Námitka | Platí? | Řeší to Ceph? |
|---|---|---|---|
| 1 | Zásadní bugy v OpenZFS na Linuxu | Ano — a Ceph má vlastní (§15) | ❌ ne |
| 2 | LUKS na každý disk jen kvůli posílání snapshotů | Premisa je obrácená | ❌ Ceph je taky per-OSD dm-crypt |
| 3 | Nelze později přidat větší disk | **Ano — nejsilnější bod** | 🟡 ano, ale viz #8 |
| 4 | Chybí defragmentace | Ano | ❌ BlueStore fragmentuje taky |
| 5 | RAM po dedupu se nevrátí | Z velké části ano | ❌ Ceph dedup je experimentální |
| 6 | Pomalé čtení a zápisy proti Btrfs/ext4 | Často — a příčiny jsou ověřitelné | ❌❌ **v tomhle měřítku výrazně horší** |
| 7 | ZFS kdysi pokazilo vlastníky souborů | Neumím posoudit | — |
| 8 | Nelze růst z 1 uzlu s EC na 3 uzly s replikací | **Ano, a hůř, než zní** | ❌ tohle je cena **za** Ceph |

### 18.1 Bugy (námitka 1)

Platí a §15 je dokumentuje. Jenže §15 dokumentuje symetricky i timeline Cephu a užitečná otázka nezní „má to bugy“, ale „kde ty bugy sedí vzhledem k tomu, jak to budu používat“. ZFS je má nahloučené v `send` cestách a v čerstvě dodaných funkcích; Ceph v CephFS snapshotech s multi-MDS, ve spotřebních SSD bez PLP a — což je vlastní závěr §15 — v **chybě obsluhy**, která je dominantní příčinou reálných ztrát a roste s počtem pohyblivých částí. Ceph má pět a víc démonů proti jedné sadě příkazů u ZFS. §17 je datový bod opačným směrem: třída automount paniců se zavřela **přepisem** s účelově psanou sadou testů, ne záplatou.

### 18.2 Šifrování (námitka 2)

Premisa je obrácená, a stojí za to to říct nahlas, protože to byla moje vlastní úvaha. **LUKS nikdy nebyl cenou za replikaci.** Nativní šifrování ZFS umí `zfs send -w` (raw), který posílá šifrovaná data a klíč na cíli nepotřebuje. §12 zvolila LUKS z nesouvisejících důvodů: nativní šifrování nechává čitelná metadata poolu (jména datasetů a snapshotů, velikosti, časy) a jeho `send`/`recv` cesta měla korupční historii, jejíž hlavní issue ([#12014](https://github.com/openzfs/zfs/issues/12014)) se zavřelo až 2025-05-19.

A Ceph šifrování po zařízeních neuteče: *"Logical volumes can be encrypted using `dmcrypt` by specifying the `--dmcrypt` flag when creating OSDs."* Každý OSD je dm-crypt svazek. Rozdíl je v tom, že to orchestruje `ceph-volume` místo Clevisu — reálný ergonomický zisk, ale ne změna modelu.

### 18.3 Větší disky (námitka 3)

Platí a je to nejsilnější z osmi. Uvnitř RAIDZ vdevu je využitelná kapacita na disk daná nejmenším členem, takže 40TB disk koupený do pole z 30TB disků přispěje 30 TB. Než sáhneš po Cephu, existují dvě odpovědi v ZFS. **Mirror vdevy**: přidáváš a měníš po dvou a s `autoexpand=on` výměna obou půlek jednoho zrcadla dá prostor okamžitě — za 50 % efektivity místo 75 % u RAIDZ2, což při cíli 150 TiB znamená hodně disků navíc. **Celé vdevy**: `raidz2` ze 4×30 TB a pozdější `raidz2` ze 4×40 TB koexistují v jednom poolu, za cenu nákupu po čtyřech.

Ceph to řeší nativně přes CRUSH váhy a je to skutečná, durable výhoda. Je to zároveň ta výhoda, kterou §18.8 z větší části ruší.

### 18.4 Defragmentace (námitka 4)

Zčásti platí, a je slabší, než jak jsem to napsal — viz oprava v §19. `zfs rewrite` existuje od května 2025 a je v 2.3.x i 2.4.x; defragmentace souborů i rebalance po přidání vdevu jsou jeho deklarované účely, takže ani jedno už nepotřebuje druhý pool. Z námitky přežívá to, že potřebuje kam souvisle zapsat, takže jeho účinnost padá právě na téměř plném poolu, který k jeho použití vede; tam zůstává spolehlivým lékem přestavba přes `send`/`recv`. Jenže srovnávací tabulka dává **na tomhle řádku 🟡 i Cephu**: BlueStore fragmentuje také. ✅ tam patří Btrfs. A konkrétně u téměř zaplněného pole se způsoby selhání liší v Cephův neprospěch: plný ZFS pool zpomalí, zatímco Ceph pool při dosažení full ratio **přestane přijímat zápisy**. Skutečnou odpovědí na „pole bude často hodně plné“ není engine, ale kupovat kapacitu dřív.

### 18.5 Deduplikace (námitka 5)

Z velké části platí. Fast Dedup v OpenZFS 2.3 přinesl `zpool ddtprune`, který *"prunes older unique entries from the dedup table"* — ale DDT neodstraní, takže „tu RAM už nikdy nedostanu zpátky“ zůstává férovým popisem. Řešením je, že tohle je funkce, která se nemá zapínat: na bulk médiích a fotkách deduplikace nezíská skoro nic, což je závěr zdrojů, které §7 už cituje. Vlastní deduplikace Cephu je dokumentovaná jako experimentální. Tahle námitka je o tlačítku, které nemá zmáčknout ani jeden systém.

### 18.6 Výkon (námitka 6)

Často platí a je to námitka, která odvádí nejvíc emoční práce — právě proto si zaslouží nejpřesnější zacházení. ZFS je na řadě workloadů opravdu pomalejší než ext4 a příčiny jsou konkrétní a ověřitelné, ne záhadné. Ta hlavní je geometrie: **jeden RAIDZ vdev dodá náhodné IOPS zhruba jednoho disku**, takže osmidiskové RAIDZ2 nemá IOPS osmi disků; mirrory škálují s počtem vdevů. Pak následuje `recordsize` neodpovídající workloadu, synchronní zápisy bez SLOGu, ARC vyhladovělý virtuály a `atime=on`, který mění čtení na zápisy. `special` vdev se `special_small_blocks` sundá metadatové IOPS z RAIDZ vdevu úplně a bývá největší dostupnou výhrou — za tu cenu, že to není cache, ale úložiště poolu: **ztratíš ho bez zrcadla a pool je pryč**.

Tahle námitka ale míří od Cephu, ne k němu. Na jednom až třech uzlech s jedním klientem je Ceph výrazně pomalejší než ZFS a s ext4 nesrovnatelný: každý zápis jde po síti a musí se trvanlivě potvrdit na každé replice, než dostane klient odpověď — přesně proto jsou PLP SSD a 10GbE prakticky povinné (§15). Rychlost Cephu pochází z paralelismu přes mnoho OSD a mnoho klientů, a nic z toho tenhle profil nemá.

### 18.7 Incident s vlastníky (námitka 7)

Zaznamenáno, ne vymluveno. Roky staré, detaily se nedochovaly, takže to teď nejde diagnostikovat. Věrohodní kandidáti z toho, co je zdokumentované: regrese 0.7.7→0.7.8 s mizejícími soubory (§15), nesoulad NFSv4 a POSIX ACL na Linuxu (§2.6, [#4966](https://github.com/openzfs/zfs/issues/4966)), nebo idmapping při `recv`. Jako důkaz o konkrétním bugu je to nepoužitelné; jako datový bod o důvěře je to reálné, a důvěra není zaokrouhlovací chyba, když je člověk ve tři ráno na všechno sám.

### 18.8 Z jednoho uzlu s EC na tři s replikací (námitka 8)

Platí, a podstatně hůř, než jak námitka zní. EC profil je neměnný: *"the profile cannot be modified after the pool is created. If you find that you need an erasure-coded pool with a profile different than the one you have created, you must create a new pool … all objects from the wrongly configured pool must be moved to the newly created pool."* A topologický požadavek je tvrdý: *"Most erasure-coded pool deployments require at least `k+m` CRUSH failure domains, which in most cases means racks or hosts. There are operational advantages to planning EC profiles and cluster topology so that there are at least `k+m+1` failure domains."*

EC 2+2 tedy potřebuje **čtyři** failure domény, doporučeně pět. Tři uzly s EC 2+2 na úrovni hostů nejsou pomalé ani neefektivní — nejsou možné.

| Krok | Co reálně dostaneš |
|---|---|
| 1 uzel, EC 2+2, doména = OSD | Funguje, ale **žádná odolnost proti ztrátě stroje** |
| → 3 uzly, EC 2+2 na hostech | ❌ **nelze**, chybí čtvrtá doména |
| → 3 uzly, EC 2+1 | 67 % efektivity, **jen jedna parita** (slabší než RAIDZ2), nový pool + přesun všech dat |
| → 3 uzly, replikace size=3 | 33 % efektivity, nový pool + přesun všech dat |
| → EC 2+2 na hostech | Až od **4–5 uzlů** |

Každá cesta pryč z jednouzlového EC znamená nový pool a plnou migraci, k tomu volné místo na obojí naráz nebo trpělivost dělat to po dávkách. Je to migrační past ZFS→Ceph z §10 zopakovaná **uvnitř Cephu**, kde se jí změnou enginu vyhnout nelze.

A z velké části ruší námitku 3. Když změna topologie stejně znamená plnou migraci pool→pool, je to přesně okamžik, kdy by šel ZFS pool přestavět s novou geometrií vdevů. Z Cephovy výhody zbývá užší tvrzení, že heterogenní disky zvládá líp **mezi** změnami topologie.

### 18.9 Co ten seznam doopravdy vybírá

Přečti ho podle toho, co preferuje, ne co odmítá: defragmentaci, známý výkon, růst po jednom disku, žádnou dedup past, žádné překvapení se šifrováním po discích. To popisuje **stávající stack `mdadm + LUKS + LVM + Btrfs`**, jehož jediná zdokumentovaná slabina ve srovnávací tabulce je jeden řádek — *tichou korupci detekuje, opravit ji neumí* — a ten řádek jde zavřít přidáním `dm-integrity` pod něj.

Ty námitky tedy neukazují na Ceph. Ukazují na vyladěné ZFS, nebo na zůstat.

### 18.10 Rozhodovací pravidlo, sepsané před měřením (2026-08-14)

Námitka 6 je jediná z osmi, kterou jde levně otestovat, a emočně nese ostatní. Dostává proto pravidlo sepsané teď, dřív než existuje jakékoli číslo.

**Test.** Postavit layout, který by se reálně nasadil — což vynutí rozhodnutí mirrory versus RAIDZ2, protože právě to určuje IOPS — na skutečném hardwaru, se zrcadleným `special` vdevem, pokud jsou malé soubory ve hře, s `recordsize` odpovídajícím workloadu a s ARC, který nehladoví. Změřit proti Btrfs na týchž discích se stejnou skladbou zátěže: sekvenční čtení a zápis pro média a metadatově náročný průchod stromem u fotek a dokumentů.

**Brány**, v pořadí závaznosti:

1. **Absolutní.** ZFS musí při sekvenčním přenosu nasytit síťovou linku a průchod stromem fotek zvládnout tak rychle, aby to při používání nestálo za řeč. Tahle brána rozhoduje, protože otázka nezní, jestli se ZFS vyrovná Btrfs, ale jestli je dost rychlé na to, k čemu to pole je.
2. **Relativní.** Vyladěné ZFS se vejde do 25 % od Btrfs v sekvenční propustnosti a do dvojnásobku v metadatovém průchodu.

**Co který výsledek znamená.** Propadne brána 1 → verdikt z §14 padá poctivě a náhradou je stávající stack plus `dm-integrity`, **ne** Ceph, protože §18.6 a §18.8 ho vylučují na základě téhož měření. Projde brána 1 a propadne 2 → přijatelné; zaznamenat rozdíl a jít dál. Projdou obě → námitky 1, 4, 5, 6 a 7 naráz ztrácejí většinu síly a zbývají jen 3 a 8 — které se navzájem z velké části ruší.

**Co by z Cephu přece jen udělalo správnou volbu:** růst po jednotlivých různě velkých discích po mnoho let **a** přijetí 10GbE, PLP SSD, čtyř a více uzlů kvůli smysluplnému EC a podstatně horší latence pro jednoho klienta. To je konzistentní obchod. Není to oprava ničeho z tohoto seznamu.

## 19. Oprava (2026-08-14): `zfs rewrite` existuje a čtyři tvrzení byla chybná

Čtyři tvrzení v tomhle dokumentu říkala, že ZFS nemá nástroj na přepis existujících dat. To bylo chybné už v době psaní, ne jen zastaralé: subcommand `zfs rewrite` přistál upstreamem v **květnu 2025** ([#17246](https://github.com/openzfs/zfs/pull/17246)) a je v řadách **2.3.x i 2.4.x** — tedy v tom, co si dnes reálně nainstaluješ.

**Opraveno na místě:** řádky „Defrag / úklid fragmentace“ a „Změna komprese u existujících dat“ ve srovnávací tabulce, odrážka o plném poolu v §2.4 a hodnocení námitky 4 v §18.4. Tahle sekce zaznamenává, co se změnilo a proč, podle pravidla repozitáře, že chyba se opravuje na místě **a** zapisuje.

**Co ten nástroj dělá.** *"Rewrite blocks of specified file as is without modification at a new location and possibly with new properties, as if they were atomically read and written back."* Bere `-r` pro rekurzi, `-x` pro setrvání v jednom filesystému a `-o`/`-l` pro rozsah v bajtech. **Funguje ale jen na filesystémových datasetech** — *opraveno týž den: synopse zní `zfs rewrite [-CPSrvx] [-l length] [-o offset] file|directory…`, takže ZVOL, který je zařízením a ne souborem, mu předat nelze. Všechno, co tahle sekce tvrdí, platí pro filesystémové datasety; u ZVOLu zůstává jedinou cestou k rekompresi či defragmentaci `send`/`recv` do nového svazku (§23.4).* Pro filesystémové datasety mezeru v rekompresi zavírá úplně: změníš `compression` nebo `recordsize`, pustíš `zfs rewrite -r` a nová property se aplikuje na existující data — což dřív vyžadovalo cyklus `send`/`recv` přes jiný pool.

**Defragmentace je deklarovaný účel, ne vedlejší efekt.** Zakládající PR přímo jmenuje, co uživatelé roky chtěli: *"an ability to re-balance pool after vdev addition, de-fragment randomly written files, change some properties for already written files"*. Rebalance po `zpool add` je tu podstatná zvlášť — §16 i námitka 3 (§18.3) obě končí u „přidej širší vdev z větších disků“, načež existující data zůstanou na starých vdevech, dokud je něco nepřepíše. `zfs rewrite -P -r` je to něco.

Běží navíc za provozu — *"protected by normal range locks, it can be done under any other load"* —, je rychlejší než čtení plus zápis, protože *"it does not require data copying to user-space"*, a *"does not affect file's modification time or other properties"*, takže zálohovací nástroje řídící se podle mtime neuvidí celý pool jako změněný.

**Kde námitka přežívá, je užší, než jsem napsal poprvé** (tenhle odstavec byl opraven týž den, protože původní znění přehánělo). Přepis souboru uvolní jeho rozházené bloky a alokuje souvislý úsek, takže fragmentace volného místa — kterou měří `FRAG`, *"As the amount of space allocated increases, it becomes more difficult to locate free space"* — se tím **zlepšuje**. Jenže ten mechanismus potřebuje kam souvisle zapsat novou kopii **dřív**, než se staré bloky uvolní, a to je přesně to, co téměř plný a silně fragmentovaný pool nemá; tam nová kopie přistane taky rozházená a získáš málo. Snapshoty to zhoršují ještě víc (viz níže). `zfs rewrite` tedy funguje nejlíp na poolu, který ho potřebuje nejmíň, a přestavba přes `send`/`recv` do čerstvého poolu zůstává lékem, který zabere vždycky. Pořád to také není „block pointer rewrite“: pool si bloky přemisťovat sám neumí, tohle se řídí po souborech z userspace.

**Dva přepínače, na kterých záleží víc, než vypadá.**

`-P` — *"Perform physical rewrite, preserving logical birth time of blocks."* Bez něj platí, že *"rewritten blocks update their logical birth time, meaning they will be included in incremental `zfs send` streams as modified data."* Naivní defragmentace tedy způsobí, že příští inkrementální `send` pošle celý dataset — což na měřené rezidenční WAN ze sourozenecké analýzy `storage-replication` znamená měsíční rozpočet na přenos utracený za přesouvání dat, která se nezměnila. `-P` udělá přepis pro replikaci neviditelný. V době psaní §2.4 neexistoval.

`-C` a `-S` přeskakují bloky sdílené s klony a snapshoty, a důvod je to podstatné: *"rewriting these blocks would create separate copies and increase space usage."* Na poolu, který je příliš plný — tedy přesně v situaci, která k defragmentaci vede —, přepis snapshotovaných dat problém **zhorší**, protože snapshot drží starý blok a přepis přidá nový. Pořadí operací je proto: nejdřív promazat snapshoty, teprve pak přepisovat.

**A kompromis, na který nástroj není.** Když se přestavbě vyhnout nedá, `zfs send -R` zachová všechny snapshoty — jenže zachovat je znamená přehrát původní historii zápisů, což velkou část fragmentace zreprodukuje. Poslání jediného snapshotu bez `-R` dá maximálně kompaktní výsledek a historii zahodí. Mezi tím stojí `-i`, které nese jednu deltu místo všech mezilehlých snapshotů, takže ten kompromis je škála, ne přepínač. Fragmentace **je** otiskem té historie — dovozeno z mechanismu, ne doložený výrok —, takže oba konce té škály naráz mít nelze.

**Čistý dopad na námitku 4 (§18.4):** klesá z „nástroj neexistuje“ na „nástroj existuje a přestává pomáhat právě ve chvíli, kdy je pool moc plný — tedy když po něm sáhneš“. Je slabší, než jak byla formulovaná, ale nemizí — a nemizí ani závěr, že odpovědí na ni není Ceph, protože BlueStore fragmentuje také a plný Ceph pool přestane přijímat zápisy tam, kde plný ZFS pool jen zpomalí.

## 20. Kódování žije ve vdevu: co ZFS svazuje a Ceph odděluje (doplněno 2026-08-14)

§18 uzavřela, že Ceph odpovídá na jednu z osmi námitek. Tahle sekce přidává strukturální bod v jeho prospěch, který §18 nedala, protože nepřišel na řadu: **granularitu, ve které jde měnit schéma redundance**, a kolik volného místa ta změna stojí.

**V ZFS cesta po částech neexistuje.** Uzavírají ji dvě nezávislá omezení, obě zdokumentovaná. Rozšíření RAIDZ vdevu se parity nedotkne: *"Expansion does not change the number of failures that can be tolerated without data loss (e.g. a RAID-Z2 is still a RAID-Z2 even after expansion)."* A RAIDZ vdev nejde vyřadit, protože odstranění top-level vdevu vyžaduje, aby *"the primary pool storage does not contain a top-level raidz or draid vdev"*. Takže ani nasnadě ležící obejití — přidat vedle RAIDZ3 vdev, přelít data a starý odebrat — k dispozici není. Jednovdevový pool je nutné vyprázdnit **celý**, než ho lze zničit a postavit znovu, protože ten vdev **je** to úložiště.

**Cephova obdobná operace je po poolech.** EC profil je stejně neměnný (§18.8), ale pooly jsou logické objekty sdílející tytéž OSD, takže jeden pool jde přemigrovat na nový profil, zatímco zbytek clusteru zůstane stát. Potřebné volné místo je velikost největšího poolu, ne všeho.

| | Ceph | ZFS |
|---|---|---|
| Kde žije kódování | v **poolu** (logický objekt) | ve **vdevu** (fyzická skupina disků) |
| Sdílejí ty jednotky disky? | ✅ ano, všechny pooly nad týmiž OSD | ❌ ne, každý pool má vlastní disky |
| Granularita migrace | jeden pool | celý pool |
| Potřebné volné místo | největší pool | všechna použitá data |

Je to táž architektonická vlastnost, ze které plyne Cephova výhoda u heterogenních disků (§18.3): **Ceph odděluje logický layout od fyzického, ZFS je svazuje.** Je to durable, není to detail implementace a je to nejsilnější jednotlivý strukturální bod, který Ceph v tomhle srovnání má.

### 20.1 Granularitu si v ZFS koupit lze, a je levnější, než vypadá

Nic nenutí mít jeden pool. Postavené jako `tank-media-1`, `tank-media-2`, `tank-vms` na oddělených skupinách disků dá ZFS přesně ten model, který se na Cephu chválí: migrovat po jednom a vystačit s volným místem velikosti největšího poolu.

Překvapení je v ceně. Jeden pool se třemi osmidiskovými RAIDZ2 vdevy použije 24 disků a šest z nich na paritu. Tři pooly s jedním osmidiskovým RAIDZ2 vdevem každý použijí rovněž 24 disků a šest na paritu. **Rozdělení nestojí kapacitu vůbec.** Stojí něco jiného: volné místo se rozdělí do silos — jeden pool může být plný, zatímco druhý prázdný — a zápisy už se nestripují napříč všemi vdevy, takže celková propustnost klesne. U knihovny médií, kde převládá sekvenční přístup k jednomu velkému souboru, je ta druhá ztráta menší, než se na první pohled zdá.

### 20.2 Dvě věci, které váhy vracejí zpátky

**Tou volnou kapacitou je DR replika.** Tahle architektura už druhou kopii v druhé lokalitě drží (§4 a sourozenecká analýza `storage-replication`). Změna geometrie tedy nepotřebuje nový hardware: zrušit pool, postavit ho se zamýšleným rozvržením, poslat data zpátky. Háček je v propustnosti — protlačit celý dataset zpět přes měřenou rezidenční WAN není reálné, takže tahle cesta funguje na LAN nebo fyzickým převozem disků, ne po lince.

**A Cephova elegance při tomhle počtu uzlů není k dispozici.** EC 2+3 vyžaduje `k+m` = pět CRUSH failure domén, podle vlastního doporučení dokumentace šest (§18.8). Na jednom až třech uzlech cílový pool prostě nevytvoříš. Výhoda migrace po poolech je reálná a je skutečně Cephova — jen neexistuje zhruba pod pěti uzly, což je počet, na kterém tenhle profil bude roky sedět.

### 20.3 Obecný tvar té námitky

Parita je jen ten případ, který napadne první. Táž tuhost platí pro **jakoukoli** budoucí změnu geometrie: špatně zvolený `ashift` při vytvoření, širší vdev kvůli efektivitě, nebo útěk ze SMR disků. Ve všech případech je odpověď ZFS stejná — vyprázdnit pool a postavit znovu —, zatímco Cephova je přemigrovat dotčený pool. V tomhle obecném tvaru je námitka silnější než její paritní verze a je to verze, kterou stojí za to si pamatovat.

**Co to nemění:** verdikt ani skóre z §18. Tohle není jedna z osmi námitek, je to devátá úvaha — a odpovědí na ni není Ceph, ale **rozhodnout rozvržení poolů vědomě při stavbě**, dokud je to zadarmo. Návrh poolů je návrhem migrace, stejně jako §12 sourozenecké analýzy pozoruje, že návrh datasetů je návrhem replikace.

## 21. Rozhodnutí, která ZFS zafixuje při vytvoření (doplněno 2026-08-14)

§20 doložila, že ZFS pool nejde překódovat po částech. Tím se množina voleb zafixovaných při vytvoření stává neobvykle nosnou: každá z nich je buď zadarmo teď, nebo drahá navždy. Tahle sekce je vypisuje i s tím, co o každé rozhoduje.

### 21.1 Pool a vdev — napevno na celou životnost poolu

| Rozhodnutí | Proč je trvalé | Jak se rozhodnout |
|---|---|---|
| **`ashift`** | Property na poolu řídí následné `add`/`attach`/`replace`, ale *"Changing this value will not modify any existing vdev, not even on disk replacement"* (§26) | **Použij 12 (4 KiB), pokud neumíš doložit opak.** Příliš nízká hodnota na 4Kn disku znamená trvalý read-modify-write při každém malém zápisu; příliš vysoká jen mrhá trochou místa u malých souborů. Nikdy nespoléhej na autodetekci u poolu, který přežije své první disky — disky o velikosti sektoru lžou |
| **Úroveň parity** (raidz1/2/3) | *"Expansion does not change the number of failures that can be tolerated without data loss"* | RAIDZ2 do zhruba deseti disků; RAIDZ3 nad to, nebo tam, kde se okno resilveru protahuje na týdny (SMR, hodně plné pooly). §16 i výpočet kolem resilveru říkají, že pro tenhle profil vyhrává RAIDZ2 s měsíčním scrubem |
| **Typ vdevu** (mirror / raidz / draid) | Konverze neexistuje ani jedním směrem — a rozhoduje o tom, jestli *rozvržení* poolu vůbec zůstane vyjednatelné (§21.4) | Mirrory kupují IOPS škálující s počtem vdevů, růst po dvou discích a odebratelný vdev, za 50 % efektivity. RAIDZ kupuje kapacitu kolem 75 %, ale jeden vdev dodá náhodné IOPS zhruba jednoho disku — IOPS škálují s redundančními skupinami, ne s vřeteny (§27.3) — a nikdy ho nedostaneš ven |
| **Přidání RAIDZ vdevu** | Nikdy ho nejde odebrat: odstranění vyžaduje, aby *"the primary pool storage does not contain a top-level raidz or draid vdev"* | Ber každé `zpool add` raidz vdevu jako nevratné. Undo neexistuje, jen přestavba |
| **`special` / `dedup` vdev na RAIDZ poolu** | Blokuje ho totéž omezení — je-li v poolu raidz, nejde odebrat nic | Rozhodni při stavbě, jestli ti záleží na IOPS metadat a malých souborů. A **zrcadli ho**: je to úložiště poolu, ne cache, takže jeho ztráta bere pool |
| **Feature flagy poolu** | *"Features cannot be disabled once they have been enabled"* | Zapínej vědomě. Pozor na stavy: pouhé *enabled* pool starším softwarem naimportovat pořád nechá; podporu vyžaduje až *active*, a i tehdy read-only kompatibilní featura dovolí read-only import (§27.1) |
| **Geometrie draid** (data / parita / spare / skupiny) | Fixní při vytvoření stejně jako raidz | Kupuje sekvenční resilver a distribuované spare disky za cenu pevné šířky stripu dopadané nulami — dobré pro velká sekvenční data, špatné pro množství malých souborů (§25, §27.2) |

### 21.2 Dataset — napevno na celou životnost datasetu

| Property | Znění dokumentace | Jak se rozhodnout |
|---|---|---|
| **`encryption`** | *"encryption must be specified at dataset creation time and it cannot be changed afterwards"* | Nativní šifrování dodatečně nezapneš; LUKS pod tím lze přidávat disk po disku při jejich výměně a šifruje i metadata poolu (§12). Jdeš-li nativně, rozvrhni encryption roots při vytvoření, protože definují, co jeden klíč odemyká |
| **`casesensitivity`** | *"This property cannot be changed after the file system is created."* | Pro Linux default `sensitive`. `insensitive` jen pro dataset vyhrazený SMB klientům, kteří to potřebují |
| **`normalization`** | *"This property cannot be changed after the file system is created."* | `formD`, pokud sem kdy budou zapisovat klienti macOS přes SMB nebo NFS — macOS rozkládá diakritiku a bez normalizace může tentýž název souboru existovat dvakrát. Později se to neopraví |
| **`utf8only`** | *"This property cannot be changed after the file system is created."* | Vyplývá z nastavení `normalization`. Odmítat nevalidní UTF-8 je obvykle to, co chceš; občasný dědičný název souboru to odmítne |
| **`volblocksize`** (ZVOLy) | *"The blocksize cannot be changed once the volume has been written."* | Přizpůsob zápisovému vzoru hosta. Příliš malý stojí režii metadat; příliš velký násobí každý malý zápis hosta nejen na disku, ale i v inkrementu (§4 sourozenecké analýzy replikace) |

### 21.3 Změnitelné, ale stará data nejdou s nimi

Tyhle trvalé nejsou a u `compression`, `checksum`, `dedup` a `copies` jde stará data dorovnat i bez druhého poolu pomocí `zfs rewrite -P -r` (§19). **`recordsize` je výjimka** — *"Changes to properties that affect the size of a logical block, like recordsize, will have no effect"* — takže u něj je seznam níže opravdu jen pro nová data (§28). **U ZVOLu to nejde**: příkaz bere operandy typu soubor a adresář, takže u svazku jsou tyhle properties opravdu jen pro nová data, dokud se svazek nepostaví znovu přes `send`/`recv` (§23.4). Uvádím je proto, že i tak se vyplatí trefit je hned napoprvé: přepis plného poolu zabere čas, který nemusíš mít.

- **`recordsize`** — 1 MiB pro knihovnu médií, 128 KiB default, 16 KiB pro databázový dataset. Přepis ho neaplikuje; existující soubory si drží velikost, se kterou vznikly (§28).
- **`compression`** — `zstd` pro studená bulk data, `lz4` tam, kde jde o latenci.
- **`copies`** — na redundantním poolu málokdy užitečné; násobí místo, aniž chrání proti ztrátě zařízení.
- **`dedup`** — výjimka: vypnutí neuvolní DDT a `zpool ddtprune` prořezává, neodstraňuje (§18.5). Ber zapnutí jako trvalé.

### 21.4 Na papíře vratné, v praxi ne

- **Jeden pool, nebo víc** (§20). *Opraveno týž den, protože tahle sekce to nejprve přehnala:* **přidat** pool později jde vždycky — potřebuje to jen nové disky a nic tomu nebrání. Co nejde, je **rozdělit** existující pool, protože uvolnit z něj disky znamená odebrat vdev, a RAIDZ vdev odebrat nelze nikdy. U **mirror** vdevů to jde: *"A mirrored top-level device (log or data) can be removed"* a *"the specified device will be evacuated by copying all allocated space from it to the other devices in the pool"* — za cenu trvalé mapovací tabulky v RAM, jejíž velikost napřed odhadne `zpool remove -n`.

  Typ vdevu a počet poolů jsou tedy jedno rozhodnutí, ne dvě: RAIDZ zalije rozvržení do betonu, mirrory ho nechají vyjednatelné. A nedělá se jednou — opakuje se při každém rozšíření, protože každá nová dávka disků může buď rozšířit stávající pool, nebo založit další. Rozdělení nestojí kapacitu tak jako tak: tři osmidiskové RAIDZ2 pooly použijí týchž 24 disků a šest parity jako jeden pool se třemi takovými vdevy. Kupuje granularitu migrace; stojí volné místo v silech a chybějící striping mezi pooly.
- **Hranice datasetů.** `send`/`recv` replikuje celé datasety, takže rozvržení datasetů **je** rozvržením replikace — přesně ten bod, který dělá [storage-replication §12](../storage-replication/README.cs.md). Strom, který se bude replikovat jinak často nebo vůbec, musí být vlastním datasetem od začátku.

### 21.5 Zkrácená verze

Pokud jich má před prvním `zpool create` dostat skutečnou pozornost jen čtvero, ať jsou to: **`ashift`** (12), **typ vdevu a parita**, **jestli chceš `special` vdev** a **model šifrování**. Tyhle čtyři nejde vzít zpět bez vyprázdnění poolu. Počet poolů *páté* není — rozhoduje se znovu při každém rozšíření (§21.4) a jak volně, to určuje zvolený typ vdevu, což je důvod, proč ten váží víc, než vypadá. Všechno z §21.3 jde později opravit přes `zfs rewrite` a všechno z §21.2 jde aspoň u jednoho datasetu spravit tím, že znovu vytvoříš ten dataset, ne celý pool.

## 22. Objektový model, který §20 a §21 předpokládají (doplněno 2026-08-14)

Není to tutoriál. §20 tvrdí, že kódování je vázané na vdev, a §21 vypisuje, co tím zůstane natrvalo; obě předpokládají strukturu, kterou zbytek dokumentu nikde nevypisuje. Čtyři fakta v ní jsou nosná a u každého je označeno, kde se používá.

### 22.1 Fyzická vrstva

```
zpool "tank"  ← alokační prostor, přes který se všechno stripuje
 │
 ├── top-level vdev 1  ─┐
 ├── top-level vdev 2  ─┤  data se rozprostírají přes všechny
 └── top-level vdev 3  ─┘  ztráta KTERÉHOKOLI z nich = ztráta celého poolu
      │
      └── redundance žije uvnitř vdevu, nikdy mezi vdevy:
          mirror / raidz1,2,3 / draid / holé zařízení
           └── fyzická zařízení (celé disky nebo partitiony)
```

**Nosné fakt 1: mezi top-level vdevy není žádná redundance.** Každý si ji zajišťuje sám uvnitř. Ztratíš-li jeden celý, pool je pryč, ať jsou ostatní jakkoli zdravé. Proto se typy vdevů nemíchají, proto je přidání vdevu vážný akt (§21.1) a proto široký pool není automaticky bezpečnější pool.

Vedle datových vdevů se na pool věší pomocné třídy:

| Třída | Drží | Ztráta znamená |
|---|---|---|
| `special` | metadata a volitelně malé bloky | ❌ **pool je pryč** |
| `dedup` | dedup tabulku | ❌ **pool je pryč** |
| `log` (SLOG) | oddělený intent log pro sync zápisy | ✅ prakticky nic |
| `cache` (L2ARC) | čtecí cache druhé úrovně | ✅ nic |
| `spare` | hot spare disky | ✅ nic |

**Nosné fakt 2: `special` a `dedup` jsou úložiště, ne cache.** První dva řádky jsou to, v čem se chybuje, protože zbylé tři cache jsou a název svádí k tomu myslet si, že jsou takové všechny. `special` vdev drží skutečná metadata poolu, takže musí být zrcadlený na stejné úrovni jako datové vdevy — man page si o to říká přesně: *"The redundancy of this device should match the redundancy of the other normal devices in the pool."* Proto §21.1 bere jeho přidání na RAIDZ poolu jako trvalé rozhodnutí.

### 22.2 Logická vrstva

```
tank                              ← pool je zároveň kořenový dataset
 ├── tank/media                     filesystem  (mountovatelný, POSIX)
 │    └── tank/media/photos         vnořený, dědí properties
 ├── tank/vms
 │    └── tank/vms/disk0            ZVOL  → /dev/zvol/tank/vms/disk0
 └── tank/docs
      ├── tank/docs@2026-08-14      snapshot (read-only bod v čase)
      │    └── tank/docs-test       clone (zapisovatelný, sdílí bloky)
      └── tank/docs#kotva           bookmark (značka, stačí pro send)
```

Pět typů datasetů, všechny čerpají z téhož volného místa:

- **filesystem** — mountovatelný POSIX filesystém, výchozí typ.
- **volume (ZVOL)** — bloková zařízení vystavené pod `/dev/zvol/…`, s `volsize` a s `volblocksize` daným při vytvoření (§21.2).
- **snapshot** — `dataset@jméno`, read-only, stojí jen ty bloky, které se od té doby rozešly.
- **clone** — zapisovatelný dataset vytvořený ze snapshotu, sdílí s ním bloky, dokud se do nich nezapíše.
- **bookmark** — `dataset#jméno`, ještě lehčí: drží jen tolik, aby posloužil jako zdroj inkrementálního `send`, což je právě to, co umožní smazat podkladový snapshot a nepřetrhnout replikační řetěz.

**Nosné fakt 3: filesystémy se nedimenzují.** Nevytváříš `tank/media` o velikosti 50 TB. Vytvoříš ho a on si bere ze společného volného místa poolu. Omezení jsou volitelná a nasazují se až potom — `quota` je strop datasetu, `reservation` mu místo garantuje. Je to obrácený model proti LVM, kde se velikost logického svazku určí předem a měnit ji je operace. A je to zároveň důvod, proč je strom datasetů návrhové rozhodnutí a ne účetnictví: properties se po něm **dědí**, takže `zfs set compression=zstd tank` dosáhne na všechno pod tím, dokud to někde nepřebiješ, a hranice datasetů jsou zároveň hranicemi replikace (§21.4).

Výjimkou z „nedimenzují se“ jsou ZVOLy: ty `volsize` deklarují, ve výchozím stavu ale thin — garantované místo z nich udělá až `refreservation`.

### 22.3 Má pool pevnou velikost?

**Nosné fakt 4: umí jen růst.** Třemi cestami:

1. **`zpool add`** — nový top-level vdev. Okamžité a u RAIDZ nevratné (§21.1).
2. **`zpool attach` na raidz vdev** — RAIDZ expansion, od 2.3. Rozšíří vdev, aniž by sáhl na úroveň parity, a existující bloky si drží starý poměr dat k paritě, dokud se nepřepíšou (§2.1).
3. **Výměna všech disků ve vdevu za větší**, po jednom a s resilverem u každého. Nové místo se objeví, až když je hotový poslední — *"device replacement within mirror/raidz groups requires all devices to be expanded before new space becomes available"* —, s `autoexpand=on` automaticky, protože *"the pool will be resized according to the size of the expanded device"*, jinak přes `zpool online -e`. Kolik čeká, ukáže property `expandsize`: *"Amount of uninitialized space within the pool or device that can be used to increase the total capacity of the pool."*

Zmenšování je ta část, která v podstatě neexistuje. Jediným mechanismem je odebrání top-level vdevu, což funguje u mirroru a holého zařízení, ale nikdy tam, kde je přítomný RAIDZ vdev (§21.4). **RAIDZ pool je jednosměrka** — a právě o téhle jediné asymetrii jsou §20 i §21 nakonec obě.

## 23. Změna velikosti ZVOLu pod Proxmox VM (doplněno 2026-08-14)

Srovnávací tabulka dává ZFS, Cephu i LVM u zmenšení VM disku ✅ a jako tvrzení o schopnosti je to správně. V praxi se ale ty dva směry nechovají ani vzdáleně stejně a nástroje jeden z nich odmítají. Tahle sekce je provozní detail za tím řádkem. **Ratingy neposouvá**, protože omezení, na kterém záleží, se ukazuje být Proxmoxovo, ne kteréhokoli backendu.

### 23.1 Zvětšení: za běhu a přes `qm resize`

```bash
qm resize 101 scsi0 +500G
```

Používej `qm resize`, ne `zfs set volsize`. ZVOL zvětší obojí, ale jen `qm resize` o tom zároveň řekne QEMU, takže běžící host uvidí novou velikost okamžitě. Nastavení `volsize` za zády Proxmoxu nechá QEMU hlásit hostu starou velikost až do vypnutí VM — ZVOL je větší a host se to nedozví.

Dvě omezení plynou ze samotné property. *"The volsize can only be set to a multiple of volblocksize, and cannot be zero."* A *"Any changes to volsize are reflected in an equivalent change to the reservation (or refreservation)"* — u thick ZVOLu tedy zvětšení ukousne místo v poolu okamžitě, dřív než host cokoli zapíše.

### 23.2 Zmenšení: možné, odmítané a za běhu nebezpečné

`zfs set volsize=` menší hodnotu přijme. Proxmox ne: *"Shrinking disk size is not supported."* To odmítnutí je **nezávislé na backendu** — `qm resize` odmítne zmenšit stejně tak RBD image nebo LVM svazek —, a proto tohle ZFS od Cephu v tabulce výše nerozlišuje.

Důvod, proč to odmítnutí respektovat, je, že **ZFS netuší, co je uvnitř**. ZVOL jsou pro něj syrové bloky; uřízne pod posledním použitým extentem filesystému bez reptání. Výstraha v man page míří přesně na zařízení v provozu: *"These effects can also occur when the volume size is changed while it is in use (particularly when shrinking the size). Extreme care should be used when adjusting the volume size."*

Zmenšovat disk **běžící** VM je nebezpečné i tehdy, když je filesystém uvnitř už správně zmenšený: jádro hosta má starou velikost zařízení nacachovanou, jeho page cache může držet data za novou hranicí a QEMU velikost směrem dolů nerenegociuje. Zvětšení je událost, kterou host vstřebá; zmenšení není jeho zrcadlovým obrazem.

**Když to udělat musíš:**

1. Zmenšit filesystém uvnitř hosta, pohodlně pod cílovou velikost.
2. Ověřit, kde doopravdy leží poslední použitý blok — krok, který se vynechává nejčastěji.
3. **Vypnout VM.** Není to volitelné.
4. `zfs snapshot tank/vms/disk0@pred-zmensenim` — skutečná záchranná síť.
5. `zfs set volsize=…` na hostiteli.
6. Nabootovat a ověřit, teprve pak sahat na snapshot z kroku 4.

Pozor na interakci v kroku 4: dokud ten snapshot existuje, drží staré bloky, takže uvolňované místo se neobjeví, dokud ho nezničíš. Což je stejně správné pořadí — nejdřív ověřit, pak uvolňovat.

### 23.3 Co se obvykle chce místo toho: discard

U **sparse** ZVOLu zmenšení `volsize` samo o sobě neuvolní nic. Spotřebované místo je to, co je zapsané, ne to, co je deklarované, takže snížením deklarace se neuvolní žádné bloky. Co poolu skutečně vrací místo po smazaných souborech uvnitř hosta, je discard:

```
# Proxmox: u disku zapnout Discard (a použít virtio-scsi)
# v hostu:
fstrim -av
```

Běží to za provozu, geometrii to nijak neohrožuje a dá se to opakovat podle plánu. U thin provisioned VM disku je to jediný mechanismus, který vůbec něco vrací, a je to skoro vždycky to, co „chci zmenšit ten disk“ doopravdy znamená.

Zmenšení `volsize` si své riziko zaslouží jen u **thick** ZVOLu, kde jde o uvolnění rezervace, ne dat — a tam platí postup z §23.2 v plném rozsahu.

### 23.4 Co `zfs rewrite` v tomhle kontextu neumí

§19 zaznamenává, že `zfs rewrite` zavírá mezeru v rekompresi a defragmentaci. Zavírá ji pro **filesystémové datasety**. Synopse zní `zfs rewrite [-CPSrvx] [-l length] [-o offset] file|directory…` — soubory a adresáře — a ZVOL je zařízení pod `/dev/zvol`, ne soubor uvnitř ZFS filesystému. Předat mu ho nelze.

U disku VM na ZVOLu jsou tedy tři věci, které §19 a §21.3 nabízejí, nedostupné, a jedinou cestou ke kterékoli z nich je přestavba přes `send`/`recv` do nového svazku:

- **Rekomprese.** `compression` se měnit dá, ale *"Changing this property affects only newly-written data"* je u svazku celý příběh — nic to zpětně nedorovná.
- **Defragmentace** obsahu svazku.
- **Rebalance** na nově přidaný vdev.

Dvě menší fakta o ZVOLech, která se k tomu hodí mít: snapshot svazku vznikne jako každý jiný (`zfs snapshot tank/vms/disk0@jmeno`), ale jeho zařízení se neobjeví, dokud si o to neřekneš — *"Controls whether the volume snapshot devices under /dev/zvol/⟨pool⟩ are hidden or visible. The default value is hidden."* A žádný smysluplný strop velikosti neexistuje, takže 20TB ZVOL možný je; jestli je moudrý, je jiná otázka, protože takhle velký svazek udělá ZFS slepým vůči svému obsahu — žádné snapshoty po souborech, žádný `zfs rewrite` a granularita retence replikace je celý svazek. Pro bulk data si filesystémový dataset sdílený přes SMB nebo NFS zachová všechno tři; ZVOLy si své místo zaslouží u skutečných systémových disků virtuálů.

## 24. Oprava (2026-08-15): block cloning je defaultně zapnutý a cross-dataset funguje

Srovnávací tabulka hodnotila `cp --reflink` u ZFS jako *„block cloning (2.2+), default off, cross-dataset ne“*. Dvě ze tří těch částí byly chybné, a chybné už v době psaní, ne jen zastaralé — popisují krátké okno po korupčním incidentu ve 2.2.0, ne jakoukoli verzi, kterou bys reálně nainstaloval.

**`zfs_bclone_enabled` má default 1.** Ověřeno proti `man/man4/zfs.4` ve větvích `zfs-2.2-release`, `zfs-2.3-release` i `master`: všechny tři nesou `Ns = Ns Sy 1`, takže block cloning je v každé dnes dodávané řadě dostupný rovnou. Úloha toho parametru je opačná, než tabulka naznačovala — *"If this setting is 0, then even if `feature@block_cloning` is enabled, using functions and system calls that attempt to clone blocks will act as though the feature is disabled."* A přestal se označovat za experimentální v 11/2024.

**Cross-dataset klonování podporované je, s podmínkami.** Dokumentace featury to říká přímo: *"Blocks can be cloned across datasets under some conditions (like equal recordsize, the same master encryption key, etc.)"* a *"ZFS tries its best to clone across datasets including encrypted ones"*, byť připouští, že je to *"limited for various (nontrivial) reasons depending on the OS and/or ZFS internals"*. „Cross-dataset ne“ bylo příliš silné; přesné slovo je „podmíněně“.

**Co udělat opravdu je potřeba, je pool feature.** `block_cloning` je vlastnost poolu, takže pool vytvořený před 2.2 ji má `disabled`, dokud nepřijde `zpool upgrade`. Pak už nic dalšího netřeba — *"becomes active when first block is cloned"* sama od sebe.

**Hodnocení zůstává 🟡, ale z jiného důvodu, než jaký byl uveden.** Ne „defaultně vypnuté“, ale „defaultně zapnuté a pořád ze sebe setřásající chyby správnosti“. Jen commit log roku 2026 nese *Fix read corruption after block clone after truncate* (04/2026), *Fix double free for blocks cloned after DDT prune* (05/2026) a *Fix reads for blocks freed after being cloned* (07/2026). To jsou tři opravy ve čtecí a uvolňovací cestě za čtyři měsíce, u featury dodávané od roku 2023. Pravidlo z §15 — nechat novinky uležet, jet konzervativní verze — na ni platí přesně jako dřív; nepravdivá byla jen ta věta, že je defaultně netečná.

**Opraveno na místě:** reflink řádek srovnávací tabulky a závěrečné poučení v §15, které používalo „block cloning je beztak default off“ jako uklidnění, které poskytnout nemohlo.

**Sloupec CephFS byl 2026-08-15 přeověřen, tentokrát pořádně.** Včerejší ❌ stálo na jediném prázdném code searchi, což důkaz není. Teď stojí na třech: `FICLONE`, `FICLONERANGE` i `reflink` vracejí napříč celým stromem `ceph/ceph` **nula** výskytů, zatímco `copy_file_range` jich má pět; dokumentace CephFS v jádře nezmiňuje reflink, `FICLONE` ani sdílení bloků vůbec; a co dokumentuje, je mount volba `nocopyfrom` — *"Don't use the RADOS 'copy-from' operation to perform remote object copies. Currently, it's only used in `copy_file_range`…"*

A právě ten rozdíl je smyslem celého řádku. RADOS `copy-from` přesune kopírování z klienta a ušetří síťové kolečko, ale **alokuje nové objekty**: žádné sdílené bloky, žádná úspora místa. Na CephFS tedy `cp --reflink=always` rovnou selže a `--reflink=auto` tiše degraduje na plnou kopii — tedy přesně na výsledek, kterému se reflink snaží předejít. Btrfs reflinky zůstávají zralým referenčním případem, a proto je `cp --reflink` kanonickým příkladem té funkce.

## 25. Kolik doopravdy stojí malý soubor (doplněno 2026-08-15)

Srovnávací tabulka má řádek **granularita CoW (zápis 1 bajtu)** a snadno se čte, jako by odpovídal na otázku, kterou neklade. Pletou se tu dvě různé věci a rozdíl mezi nimi je třicetinásobek:

- **Zápis jednoho bajtu do existujícího souboru.** Copy-on-write znamená přepis celého recordu, takže při výchozím `recordsize` je to 128 KiB zápisu za jeden změněný bajt. Tohle měří ten řádek tabulky a pro ZFS to platí.
- **Jednobajtový soubor.** To 128 KiB není. `recordsize` je dokumentovaný jako *"a **suggested** block size for files in the file system"* — strop, ne pevná jednotka. Soubor menší než on dostane blok podle svého obsahu, zaokrouhlený nahoru na jeden sektor.

Doložení je v popisu featury `embedded_data`, který říká, co se vložením ušetří: *"the space of the block (**one sector, typically 512 B or 4 KiB**) is saved"*. Kdyby drobný soubor zabíral celý record, stálo by tam 128 KiB.

### 25.1 S kompresí možná žádný datový blok

*"Blocks whose contents can compress to 112 bytes or smaller can take advantage of this feature. … The contents of highly-compressible blocks are stored in the block 'pointer' itself (a misnomer in this case, as it contains the compressed data, rather than a pointer to its location on disk). Thus the space of the block … is saved, and no additional I/O is needed to read and write the data block."*

Jednobajtový soubor se pod 112 bajtů vejde s velkou rezervou, takže se uloží přímo do block pointeru a **žádný datový blok se nealokuje**. Btrfs dělá totéž pod jiným jménem — `max_inline` má default `min(2048, page size)` a při 4KiB sectorsize je *"maximum size of inline data is about 3900 bytes"*. To ✅ ve sloupci Btrfs u zmíněného řádku tedy není jen o jeho 4KiB bloku: malé soubory inlinuje také.

### 25.2 Datový blok nikdy nebyl celý účet

Ať data souboru stojí cokoli, pořád je potřeba dnode, položka v adresáři a nadřazená struktura — a ZFS ukládá metadata v **ditto blocích**, tedy ve víc kopiích, takže se metadata násobí ještě dřív, než se uplatní geometrie vdevu.

Ta pak násobí všechno, co se alokovalo:

| vdev, `ashift=12` | jeden 4KiB sektor stojí | režie |
|---|---|---|
| mirror (2-way) | 8 KiB | 100 % |
| RAIDZ2 | 12 KiB — jeden datový + **dva paritní** sektory | 200 % |

Nominální režie RAIDZ2 na širokém stripu je 25 %; na jednosektorovém bloku je 200 %, protože parita je na stripe a jednosektorový stripe potřebuje svou plnou paritu. RAIDZ navíc alokuje v násobcích *parita + 1* sektorů — to je chování alokátoru, ne citovaná věta, ale je to důvod, proč se efektivní cena nikdy nezaokrouhluje dolů.

### 25.3 Co z toho plyne

Nevyčítej si z téhle sekce celkové číslo. Závisí na počtu ditto kopií dotčených metadat a na geometrii vdevu, a vymyslet si ho by bylo přesně to, čemu má §24 a pravidla o zdrojích předcházet. Podstatný je tvar: **u velmi malého souboru dominují metadata nad daty a na RAIDZ dominuje geometrie nad obojím.**

Mění to dvě páky a obě jsou rozhodnutí z §21, ne věci k pozdějšímu doladění:

- **`ashift`.** Při `ashift=9` je sektor 512 B místo 4 KiB, takže všechna čísla výše se dělí osmi. §21.1 pořád doporučuje 12 z důvodů, které tohle převažují — ale dataset s miliony drobných souborů je ten jediný případ, který mluví opačně, a zpátky se ta volba vzít nedá.
- **`special_small_blocks` se zrcadleným `special` vdevem** (§21.1, §22.1). Odklonění malých bloků a metadat na zrcadlené SSD změní oba násobitele naráz: geometrie mirroru místo parity RAIDZ, a metadatové IOPS z RAIDZ vdevu zmizí úplně. U stromu s mnoha malými soubory to přestává být výkonová optimalizace a stává se kapacitní.

Což je ten praktický závěr: **pokud dataset ponese miliony malých souborů, patří ta informace do návrhu poolu, ne do property, kterou nastavíš potom.**

## 26. Volba `ashift` (doplněno 2026-08-15)

§21 uvádí `ashift` jako první z rozhodnutí, která pool nevezme zpět, a §25 dodává jediný argument, který táhne opačně. Tahle sekce je úvaha za tím doporučením — a opravuje, jak §21 popsala mechanismus.

### 26.1 Default je autodetekce a její vlastní implementace přiznává, že spolehlivá není

*"Pool sector size exponent, to the power of 2 (internally referred to as ashift). Values from 9 to 16, inclusive, are valid; also, the value 0 (the default) means to auto-detect using the kernel's block layer and a ZFS internal exception list."*

Ta výjimková listina je celý argument v kostce. Existuje proto, že disky o velikosti svého sektoru lžou, takže si ZFS vede vlastní registr zařízení, jejichž odpovědím se nevěří. Autodetekce je default a její vlastní návrh připouští, že se dá obelstít.

### 26.2 Doporučení stojí na tom, že chyba je asymetrická

Ne na tom, že by 12 byla optimální, ale na tom, že ty dva způsoby, jak se splést, stojí nesrovnatelně různě.

**Příliš nízko** na disku se 4KiB fyzickými sektory promění každý podsektorový zápis v read-modify-write uvnitř disku, a to na celou životnost vdevu. Dokumentace doporučuje `ashift=12` právě pro tenhle případ — disky, které používají 4KiB sektory, ale operačnímu systému hlásí 512 B.

**Příliš vysoko** na skutečně 512bajtovém zařízení stojí nějaké místo u malých bloků. To je cena, kterou vyčísluje §25, a je to cena, ne selhání.

**A argument, který převažuje nad obojím: náhradní disky.** Pool postavený s `ashift=9` narazí ve chvíli, kdy vadný disk nahradíš 4Kn kusem, a nové disky jsou čím dál častěji 4Kn. Poznámka man page o nekompatibilních zařízeních je k tomu kompromisu suchá: *"this will probably result in bad performance but at the same time could prevent loss of data"*. Pool přežije svou první sadu disků; `ashift` druhou šanci na volbu nedostane.

### 26.3 Kdy je obhajitelné něco jiného

**`ashift=9`** jen na opravdu 512bajtových zařízeních, která nikdy nenahradí 4Kn disk — okno, které se každým rokem zužuje. Jediné, co pro to mluví, je malosouborová aritmetika z §25, kde se všechna čísla dělí osmi. U datasetu s miliony drobných souborů na hardwaru, který je jistě 512n a jistě nahraditelný stejným, je to reálný kompromis; jinde je to past.

**`ashift=13`** (8 KiB) se často navrhuje pro NVMe s vnitřní stránkou větší než 4 KiB. Zaznamenáno tu jako **komunitní praxe, ne doporučení dokumentace**: man page uvádí platný rozsah 9–16 a doporučuje pouze dvanáctku. Kdo se po té cestě vydá, měl by to brát jako neověřenou optimalizaci — a počítat s tím, že to malosouborovou režii z §25 znovu zdvojnásobí.

### 26.4 Oprava k §21.1

§21.1 tvrdila, že `ashift` se *„nastavuje se per top-level vdev při `zpool create` / `add`; property na pozdější změnu neexistuje“*. Druhá polovina je chybná. Property na poolu existuje a řídí následné operace — `add`, `attach` i `replace` ji berou. Co neumí, je sáhnout zpětně: *"Changing this value will not modify any existing vdev, not even on disk replacement."*

Praktický závěr §21 to nemění — `ashift` existujícího vdevu je daný na celou jeho životnost, a právě proto ta property patří na seznam nevratných. Chybný byl jen popis mechanismu a je opraven na místě.

## 27. Zbytek §21, přeověřený (doplněno 2026-08-15)

§26 vznikla proto, že jednověté odůvodnění v §21 nesneslo dotaz. To je špatný důvod, proč by ostatní jednověté položky měly zůstat nezkontrolované, takže prošly stejným sítem: každé úsečné „proč je to trvalé“ dohledáno k primárnímu zdroji. Tři bylo potřeba změnit a jedna z těch tří byla vymyšlená, ne jen nepřesná.

### 27.1 Feature flagy poolu — tvrzení bylo příliš silné

§21.1 tvrdila, že zapnutí featury *"může udělat pool neimportovatelným pro starší ZFS"*. První polovina řádku platila — *"Features cannot be disabled once they have been enabled."* Druhá slila dva stavy, které dokumentace drží odděleně:

- **Enabled**: *"Administrator has marked it active, but on-disk format changes haven't yet taken effect; **older software can still import the pool**"*.
- **Active**: změny na disku jsou v platnosti a read-write podpora se stává povinnou — *"and read-only support is required unless the feature is read-only compatible"*.

Zapnutí featury tedy importovatelnost nestojí vůbec; stojí ji **aktivace**, a i tehdy read-only kompatibilní featura pořád dovolí read-only import implementaci, která ji nezná. `block_cloning` je například jako read-only kompatibilní označený.

Praktická rada přežívá — zapínej vědomě, protože zpátky to nejde —, ale důvod k ní byl chybný a záchranný scénář, který naznačovala (starší ZFS pool odmítne), je užší, než jak stál.

### 27.2 Geometrie draid — ten práh byl vymyšlený

§21.1 tvrdila, že dRAID je *"relevantní až nad zhruba dvaceti disky"*. **Žádné takové číslo v dokumentaci není a nikdy ověřované nebylo.** Bylo to věrohodně znějící číslo napsané, jako by mělo zdroj — což je přesně to selhání, kterému mají pravidla o zdrojích předcházet, a je horší než přehnané tvrzení, protože čtenář nemá jak poznat, že nestojí na ničem.

Co dokumentace nabízí, je jiné a užitečnější. dRAID je *"a variant of raidz that provides integrated distributed hot spares, allowing for faster resilvering, while retaining the benefits of raidz"*, postavený z *"multiple internal raidz groups, each with D data devices and P parity devices"* rozprostřených přes všechny členy, s `data` defaultně 8 a pevnou šířkou stripu *"(padding as necessary with zeros) to allow fully sequential resilvering"*. Nejbližší věcí k pravidlu na velikost je obecné doporučení pro raidz skupiny *"between 3 and 9"* disků *"to help increase performance"*.

Poctivá přeformulace je tedy o tvaru, ne o počtu: dRAID kupuje **sekvenční resilver a distribuované spare disky** za cenu pevné šířky stripu, která malé bloky dopadá nulami — což ve světle §25 z něj dělá špatnou volbu pro množství malých souborů a dobrou pro velká sekvenční data, kde je hlavní starostí doba resilveru.

### 27.3 Tvrzení o IOPS potřebovalo citaci, ne opravu

§21.1 uvádí, že jeden RAIDZ vdev *"dodá náhodné IOPS zhruba jednoho disku"*. Dokumentace o IOPS raidz přímo nemluví — ale uvádí je pro dRAID a ten vzorec mechanismus zviditelňuje: *"floor((N-S)/(D+P))*single_drive_IOPS"*. IOPS škálují s počtem **redundančních skupin**, ne s počtem disků. Jeden raidz vdev je jedna skupina, proto se chová jako jeden disk — a proto mirrory, každý jako vlastní skupina, škálují s počtem vdevů.

To je ta citace, která tvrzení chyběla. Platí a teď ukazuje na větu, která ho činí čitelným.

### 27.4 Co obstálo

- **Úroveň parity** — doslova: *"Expansion does not change the number of failures that can be tolerated without data loss."*
- **Přidání RAIDZ vdevu** — doslova: odstranění vyžaduje, aby *"the primary pool storage does not contain a top-level raidz or draid vdev"*.
- **`special` / `dedup` vdev na RAIDZ poolu** — dovození, ale správné: tyhle typy v seznamu odstranitelných jsou a raidz omezení výše hradí veškeré odstraňování, takže jejich přítomnost v RAIDZ poolu je trvalá.
- **Konverze typu vdevu** — absence, doložená dvěma způsoby místo předpokládaná: seznam subcommandů `zpool` neobsahuje žádnou konverzi ani reshape a rozšíření je dokumentované jako zachovávající úroveň parity. Ověřeno s pozitivní kontrolou, protože prázdné hledání není zdroj.
- **Všech pět datasetových properties z §21.2** — každá už nesla doloženou formulaci; žádná se nehnula.

## 28. Změna `recordsize` v praxi — a co `zfs rewrite` neumí (doplněno 2026-08-15)

§21.3 řadila `recordsize` mezi vlastnosti, které *"trvalé nejsou a od `zfs rewrite` (§19) jde stará data dorovnat i bez druhého poolu"*. U `recordsize` to neplatí a man page to říká jednou větou: *"Changes to properties that affect the size of a logical block, like **recordsize**, will have no effect."*

### 28.1 Co přepis doopravdy aplikuje

*"Changed dataset properties that operate on the data or metadata without changing the logical size will be applied. These include **checksum**, **compression**, **dedup** and **copies**."*

Čtyři vlastnosti, a hranicí je přesně to spojení *"without changing the logical size"*. Přepis bloky přesouvá; soubor nepřeblokuje. Tvrzení §19, že zavírá mezeru v **rekompresi**, tedy platí — komprese v tom seznamu je —, ale tatáž věta `recordsize` nikdy nepokrývala a §21.3 ji rozšířila na něco, co ten nástroj nikdy neuměl.

Dokumentace té property to ostatně říkala celou dobu a je to věta, kterou jsem měl přečíst první: *"Changing the file system's recordsize affects only files created afterward; existing files are unaffected."*

### 28.2 Jak tedy existující soubor dostane nový record size?

Jen tím, že se doopravdy přepíše — obsah se přečte a zapíše znovu jako nová data, takže se nový `recordsize` uplatní při alokaci. Prakticky:

- **Zkopírovat soubory** uvnitř datasetu nebo do něj (`cp`, `rsync`) a originály vyměnit. Hrubé, ale je to jediná cesta po jednotlivých souborech.
- **`send`/`recv` celého datasetu** do čerstvého s novou hodnotou. Právě tuhle cestu chtěla §19 nástrojem `zfs rewrite` odstranit — a u `recordsize` ji pořád neodstraňuje.

Obojí přečte a zapíše každý bajt, takže ani jedno není ta levná operace na místě, kterou `zfs rewrite` je pro `compression`.

### 28.3 Volba hodnoty, když je `recordsize` strop

Zvýšení se nedotkne souborů menších, než je nová hodnota — proč, řeší §25, a znamená to, že u smíšeného stromu se efekt rozředí. Hodnota je *"a power of two greater than or equal to 512 B and less than or equal to 128 KiB. If the large_blocks feature is enabled on the pool, the size may be up to 16 MiB."*

Přizpůsob ji tomu, jak se data doopravdy čtou a zapisují:

- **Velká sekvenční data** (knihovna médií) velký record snesou a těží z něj: méně bloků, méně metadat a lepší kompresní poměry, protože komprese pracuje po celých recordech.
- **Malé náhodné zápisy** (databáze) chtějí record blízko stránce aplikace. 16KiB zápis do 1MiB recordu ušpiní celý megabajt, což je řádek o write amplification ve srovnávací tabulce a důvod, proč man page tu property popisuje jako *"designed solely for use with database workloads that access files in fixed-size records"*.

Protože se uplatňuje při vzniku souboru, vyplatí se hodnotu nastavit na datasetu **dřív**, než se naplní, ne potom — a proto ji §21 drží ve skupině „vyplatí se trefit hned napoprvé“, i když je technicky změnitelná.

### 28.4 Pasti, které pro měnitelné vlastnosti platí dál

U `compression`, `checksum`, `dedup` a `copies` je `zfs rewrite` tou cestou na místě — se dvěma podmínkami, které §19 už zaznamenává a které se snadno splní ve špatném pořadí:

- **`-P` není volitelné, pokud dataset replikuješ.** Bez něj dostane každý přepsaný blok nový logical birth time, takže příští inkrementální `send` pošle celý dataset.
- **Nejdřív promazat snapshoty.** Přepis bloků sdílených se snapshotem vytvoří druhé kopie místo aby nahradil originály, takže místo napřed naroste, než se zmenší.
- A na **ZVOL** nedosáhne nic z toho (§23.4).

## 29. Slovník, který tabulky používají (doplněno 2026-08-15)

§22 vysvětluje objektový model ZFS, protože na něm §20 a §21 stojí. Srovnávací tabulky mají týž problém u zbylých dvou sloupců a ten zůstal nedořešený: `MDS` se v dokumentu vyskytuje dvacetkrát, `OSD` desetkrát, `RADOS` devětkrát, `BlueStore` devětkrát, `RGW` osmkrát, `CRUSH` pětkrát — a ani jeden není nikde vysvětlený. Řádek hodnotící Ceph na „MDS trims with snapshots“ je pro čtenáře, který neví, co je MDS, nečitelný, čímž ztrácí smysl ho psát.

Tohle je slovník pojmů, které **dokument opravdu používá**, ne úvod do tří systémů. Kde definice není zřejmá, je citovaná, ne parafrázovaná.

### 29.1 Ceph

| Pojem | Co to je |
|---|---|
| **RADOS** | Objektové úložiště, na kterém stojí všechno ostatní: *"a reliable, distributed storage service that uses the intelligence in each of its nodes to secure the data it stores and to provide that data to clients"* |
| **OSD** | Démon vlastnící jedno úložné zařízení. *"A Ceph OSD Daemon checks its own state and the state of other OSDs and reports back to monitors."* Zhruba „jeden disk, jeden OSD“, proto se RAM počítá na OSD (§15) |
| **MON** | *"Ceph Monitors maintain the master copy of the cluster map, which they provide to Ceph clients."* Tady žije kvórum — jeden monitor je single point of failure (§13) |
| **MGR** | *"A Ceph Manager serves as an endpoint for monitoring, orchestration, and plug-in modules."* |
| **MDS** | *"A Ceph Metadata Server (MDS) manages file metadata when CephFS is used to provide file services."* Potřebuje ho jen CephFS — a je to místo, kde žije jeho křehkost se snapshoty (§15) |
| **RGW** | *"The Ceph Object Storage daemon, `radosgw`, is a FastCGI service that provides a RESTful HTTP API to store objects and metadata."* S3 endpoint z §7 |
| **RBD** | Blokové zařízení rozprostřené *"over multiple objects in the Ceph Storage Cluster"* — vrstva disků VM a protějšek ZVOLu |
| **CephFS** | *"a POSIX-compliant filesystem as a service that is layered on top of the object-based Ceph Storage Cluster"* |
| **BlueStore** | Úložný backend OSD: *"stores objects in a monolithic, database-like fashion"*, přímo na syrovém zařízení. Jeho časté fsyncy jsou důvod, proč jsou PLP SSD prakticky povinné (§15) |
| **CRUSH** | Algoritmus umístění, který z vah a topologie failure domén rozhoduje, které OSD drží která data. Ty váhy jsou to, co Cephu dovolí strávit různě velké disky (§18.3) |
| **Failure domain** | Úroveň, na které CRUSH drží repliky od sebe — OSD, host, rack. Erasure coding jich potřebuje `k+m` (§18.8), a to je omezení vynucující počty uzlů |
| **Placement group (PG)** | Jednotka, kterou CRUSH doopravdy mapuje: objekty jdou do PG, PG na OSD. Mezivrstva, díky které zůstává mapa malá |
| **EC profil** | Nastavení `k`/`m` a failure domény erasure-coded poolu, fixní od vytvoření (§20) |
| **Pool** | Logický oddíl RADOSu s vlastním nastavením replikace či EC. Na rozdíl od ZFS poolu **nevlastní disky** — všechny pooly sdílejí OSD, což je celý smysl §20 |

### 29.2 Pojmy ZFS, které §22 nepokrývá

§22 pokrývá pool, vdev, dataset, filesystem, ZVOL, snapshot, clone, bookmark a pomocné třídy vdevů. V dokumentu se objevují i tyhle:

| Pojem | Co to je |
|---|---|
| **ARC** | Čtecí cache v RAM — Adaptive Replacement Cache, vyvažující nedávno a často používané bloky místo prostého LRU. Proto ZFS vypadá, že spotřebuje všechnu paměť, a proto vyhladovělý ARC dělá ZFS pomalým (§18.6) |
| **L2ARC** | `cache` vdev: čtecí cache druhé úrovně na SSD. Její index stojí RAM, takže velký L2ARC na stroji s málo pamětí situaci zhorší |
| **SLOG** | `log` vdev: samostatné zařízení pro ZFS Intent Log, obsluhující jen *synchronní* zápisy. Jediné místo, kde u ZFS na PLP opravdu záleží |
| **DDT** | Deduplikační tabulka. `zpool ddtprune` ji prořezává, odstranit ji neumí nic (§18.5) |
| **BRT** | Block reference table za block cloningem (§24) |
| **dnode** | Obdoba inode v ZFS — metadatová struktura jednoho objektu |
| **Ditto bloky** | Kopie metadat navíc, zapsané na oddělená místa, nezávisle na redundanci vdevu. Proto metadata stojí víc, než je jejich nominální velikost (§25) |
| **txg** | Transaction group: zápisy se hromadí a commitují po dávkách, což je důvod, proč je většina zápisů ZFS asynchronní a PLP tu není problém jako u Cephu |

### 29.3 Btrfs

| Pojem | Co to je |
|---|---|
| **Subvolume** | Samostatně snapshotovatelný strom uvnitř jednoho filesystému — nejbližší obdoba ZFS datasetu, jen sdílí prostor filesystému, ne poolu |
| **Reflink** | Kopie sdílející extenty originálu, dokud se do ní nezapíše; to, co vytváří `cp --reflink`. Block cloning v ZFS je ekvivalent (§24) |
| **Extent** | Alokační jednotka Btrfs proměnné délky, na místě pevného recordu v ZFS |
| **Inline extent** | Obsah malého souboru uložený uvnitř metadatového b-stromu místo v datovém bloku, omezený `max_inline` (§25) |
| **Profil** | Nastavení redundance po chuncích (`single`, `dup`, `raid1`, `raid10`, `raid5/6`), volené zvlášť pro data a metadata — tak stávající stack jede metadata v `dup` nad mdadm |

## 30. Kompromis při jednom uzlu a při třech (doplněno 2026-08-15)

Srovnávací tabulka je hodnocená pro „1–3 uzly“ jako jeden profil, což zakrývá, že kompromis mezi těmi dvěma konci mění tvar. Tahle sekce je odděluje. Nic tu není nově ověřované; jsou to vlastní nálezy dokumentu setříděné podle počtu uzlů.

### 30.1 Co dá Ceph při jednom uzlu

Víc, než §13 naznačuje, protože při jednom uzlu je CRUSH failure doména **OSD**, ne host (`osd_crush_chooseleaf_type = 0`). Všechno, co potřebuje *několik failure domén*, je tedy splnitelné několika disky v jedné bedně:

- **Různě velké disky** strávené CRUSH vahami, kde RAIDZ rozdíl zahodí (§18.3).
- **Samooprava bez náhradního disku** — data z `out` OSD se dopočítají na zbývající, pokud je kam. ZFS degraduje a čeká, pokud nemáš hot spare.
- **Odebrání kapacity** — `osd out` a rebalance. RAIDZ vdev odebrat nelze nikdy (§21.1).
- **Zvýšení redundance za běhu** — `size=2→3` u replikovaného poolu. RAIDZ2→RAIDZ3 chce přestavbu (§20).
- **Granularita migrace po poolech** (§20), dokud je dost OSD na `k+m` cílového profilu.
- **Nativní S3 přes RGW** a **RWX pro Kubernetes** přes CephFS bez re-exportu po NFS.
- **Prohlížení snapshotů** bez mountu na každý snapshot, což je nejslabší oblast ZFS na Linuxu (§2.5, §17).

**A věta, která ten seznam přerámuje celý: nic z toho nepřežije ztrátu toho stroje.** Při jednom uzlu je failure doménou disk, takže Ceph chrání přesně proti tomu, proti čemu už chrání RAIDZ2. Všechno výše je pružnost **uvnitř** jedné bedny, koupená za cenu, kterou vypisuje §13 — žádná odolnost proti ztrátě hostu, `size=2` proti vlastnímu *"risks data loss … only temporarily"* Cephu, jediný monitor jako single point of failure, pět a víc démonů, ~4 GB RAM na OSD a CephFS, který na uzlu s OSD nesmíš mountovat kernel klientem.

Jen dvě Cephovy výhody opravdu vyžadují víc uzlů: živá migrace VM a škálování.

### 30.2 Co stojí tři uzly

Tři uzly jsou bod, kde Ceph konečně dodá to, kvůli čemu existuje — přežití ztráty stroje. Účet je nejdelší přesně na témže místě.

**Kapacita a hardware**

- `size=3` dá **33 %** proti 75 % u RAIDZ2. Při cíli 150 TiB to jsou desítky disků.
- **EC 2+2 na třech uzlech nejde** — potřebuje `k+m` = čtyři domény na úrovni hostů. Zbývá k=2,m=1: 67 %, ale **jediná parita**, tedy slabší redundance než dnešní RAIDZ2.
- **Self-heal headroom**: obnova tří kopií po ztrátě uzlu vyžaduje, aby se data vešla na zbylé dva, takže pole nejde doplnit.
- **PLP SSD prakticky povinné** (fsync vzor BlueStore), **10GbE prakticky povinná**, **~4 GB RAM na OSD**.

**Výkon**

- Pro jednoho klienta podstatně pomalejší než lokální ZFS: každý zápis jde po síti a musí se trvanlivě potvrdit na každé replice, než dostane klient odpověď.
- Read-modify-write režie u malých zápisů na EC (§16.6).

**Provoz a spolehlivost**

- Pět a víc démonů, cephadm kontejnery, CRUSH a PG proti `zpool` a `zfs`.
- Vlastní závěr §15: **chyba obsluhy je dominantní reálnou příčinou ztrát** a roste s počtem pohyblivých částí. U sólo admina bez on-callu to převáží většinu technických řádků.
- **CephFS snapshoty s multi-MDS zůstávají křehkou oblastí**, s incidenty 2021→2025 — přímý zásah pro architekturu, která snapshoty bere jako centrální workflow.

**Tuhost, kterou ZFS nemá**

- EC profil je neměnný, stejná třída pasti jako parita RAIDZ (§20).
- Odchod z jednouzlového EC poolu znamená nový pool a plnou migraci dat (§18.8).

**Replikace mezi lokalitami** (ze sourozenecké analýzy [storage-replication](../storage-replication/README.cs.md))

- CephFS mirroring posílá **celé změněné soubory**, ne blokové delty.
- **Neumí říct objem přenosu předem** — na měřené lince rozhodující.
- Přejmenování adresáře je **smazání a plná znovukopie**, na téhle operaci horší než rsync.
- Hardlinky se rozpadnou na samostatné kopie.
- Živý adresář na cíli je uprostřed syncu nekonzistentní; DR bodem je jen poslední dokončený snapshot.
- `rbd-mirror` potřebuje současnou konektivitu na oba clustery, každý monitor i OSD.
- CephFS nemá reflink (§24).

### 30.3 Oprava: „Ceph potřebuje uzly“ bylo použito tam, kde neplatí

Dřívější čtení tohoto materiálu označilo pět Cephových výhod za nedostupné při jednom až třech uzlech — migraci po poolech, odebrání kapacity, samoopravu, živou migraci a škálování. Dvě z toho platily. Tři byly chybné, a chybné ze známého důvodu: omezením vynucujícím počty uzlů je `k+m` **failure domén**, a předpoklad, že doména znamená host, se přenesl do konfigurace, kde znamená OSD. Obecné pravidlo platilo; jeho rozsah ne, což je vzor, na který má `AGENTS.md` nově pravidlo.

### 30.4 Co z toho je pro tenhle kontext blocker

Z §30.1 by mohly něco rozhodnout jen tři, a všechny tři jsou otázkou budoucího use case, ne dnešního provozu: **sdílený RWX**, kdyby ho Kubernetes potřeboval (§14 to zkoumala a našla, že ne), **různě velké disky** (§18.3, nejsilnější z osmi námitek) a **S3**, kdyby si ho nějaký workload vyžádal.

Z §30.2 jsou tři dost vážné samy o sobě: **kapacitní matematika**, kde jediná tříuzlová alternativa k 33 % dá slabší redundanci, než pole má dnes; **CephFS snapshoty**, tedy křehká oblast systému, o kterou se tahle architektura opírá nejvíc; a **replikace mezi lokalitami**, kde se souborová granularita bez odhadu objemu potká s tvrdým měsíčním stropem.

## 31. Roztažení Ceph clusteru přes internet (doplněno 2026-08-15)

§4 odbývá geo-HA přes WAN jednou buňkou — *jen asynchronní DR, synchronní je showstopper*. Je to správný závěr a příliš krátký na to, aby byl užitečný, protože „dát jeden ze tří uzlů do druhé lokality“ je nápad, který se vrací. Tahle sekce je o tom, proč nefunguje, na konkrétním tvaru: dva nebo tři uzly, aspoň jeden za `[ISP, internet, ISP]`, zhruba 250 Mbps, s občasnými výpadky linky i uzlů.

### 31.1 Problémem je model, ne propustnost

Ceph potvrdí zápis až po trvanlivém commitu na replikách. WAN kolečko tedy sedí na **každém zápisu** a propustnost je vedlejší: při 20 ms RTT dostane synchronní zátěž desítky IOPS bez ohledu na to, jak je linka široká.

Upstream stránka o stretch mode žádné latenční číslo neuvádí. Dodavatelé, kteří tu konfiguraci podporují, ano: **maximálně 10 ms RTT mezi datovými lokalitami**, se 100 ms tolerovanými jen u tiebreakeru. Rezidenční cesta ISP → internet → ISP je realisticky 10–40 ms, tedy na stropě nebo za ním ještě před započtením výkyvů. Táž dokumentace jmenuje, co se při výkyvech latence děje: *"OSD flapping, loss of Monitor quorum, and slow (blocked) requests"* — všechny tři failure mody popsané níže.

### 31.2 Podporovaná konfigurace na dva až tři uzly nesedí

Odpovědí Cephu na dvě lokality je **stretch mode** a jeho požadavky jsou explicitní: *"Two Monitors must be run in each data center, plus a tiebreaker in a third (possibly in the cloud) for a total of five Monitors."* Pět monitorů, tři lokality. Mění i pooly: *"Pools will increase in size from the default `3` to `4`, and two replicas will be placed at each zone"* — **25 % kapacitní efektivity** proti 75 % u RAIDZ2.

Dva nebo tři uzly ve dvou lokalitách tedy pojedou **bez** stretch mode: bez tiebreakeru a bez automatického řízení `min_size` při netsplitu.

### 31.3 Kvórum vychází špatně v obou variantách

- **Dva uzly**: dva monitory, takže většina ztrátu kteréhokoli nepřežije. Nepoužitelné bez třetího monitoru jinde.
- **Tři uzly, jeden vzdálený**: výpadek linky je rozdělení 2–1. Dva lokální monitory drží kvórum, **vypadne ten vzdálený uzel**. Vzdálená lokalita tedy není nikdy přeživší stranou — přispívá replikami, ale sama fungovat nemůže, což je pravý opak toho, k čemu druhá lokalita je.

### 31.4 Spirála re-replikace, ta zákeřná

`mon_osd_down_out_interval` má default **10 minut**: po nich se nedostupné OSD označí `out` a Ceph začne přesouvat jeho data na přeživší uzly. Každý výpadek internetu delší než deset minut tedy rozjede přesun dat celého uzlu — a až se linka vrátí, uzel se připojí a všechno se musí backfillovat zpátky.

Rozhodne to aritmetika. 250 Mbps je 31,25 MB/s, tedy **≈2,7 TB za den** při plném nasycení a nulovém provozu klientů. Vzdálený uzel s 50 TB se re-replikuje za **≈18 dní**; při cíli 150 TiB je každá reálná zotavovací událost otázkou týdnů strávených v degradovaném stavu. Oba předpoklady — nasycená linka a nečinný cluster — jsou optimistické, takže skutečné číslo je horší.

Při dvou až třech uzlech často není **kam** re-replikovat, takže cluster místo toho sedí degradovaný po celou dobu. Je to méně destruktivní a stejně nepříjemné: znamená to, že každý výpadek nechá data jednu poruchu od ztráty.

### 31.5 Zbytek

- **Past `min_size`.** Při `size=3`/`min_size=2` na třech uzlech ztráta vzdáleného nechá dva a zápisy jedou. Ztrať během téhož výpadku *lokální* disk a jsi na jedné — **zápisy se zastaví**. Každý výpadek internetu staví cluster jeden disk od zastavení zápisů.
- **Recovery provoz vyhladoví klienty.** Backfill defaulty jsou laděné na LAN a spotřebují celou linku. `osd_max_backfills`, `osd_recovery_sleep` a mclock QoS existují, ale udržovat je správně je trvalá práce.
- **Ochrana proti falešným poplachům je tenká.** `mon_osd_min_down_reporters` má default 2 a `mon_osd_reporter_subtree_level` je `host`, což má bránit tomu, aby izolovaný síťový problém shodil uzel. Při dvou až třech hostech je ta většina triviálně malá.
- **Bezpečnost.** Porty monitorů a OSD na veřejném internetu chtějí VPN, která přidá latenci do rozpočtu z §31.1 a ubere MTU.
- **CephFS zvlášť.** Každá metadatová operace jde na MDS, takže klienti na druhé straně platí WAN za každý `stat`, `open` i `readdir`. Souborové zátěže se stanou nepoužitelnými dřív než blokové.

### 31.6 Co místo toho

Dva **nezávislé** clustery s asynchronní replikací mezi nimi — což už uzavírá §4 a čemu se celá sourozenecká analýza [storage-replication](../storage-replication/README.cs.md) věnuje. Ten rozdíl není konfigurační detail: roztažený cluster dělá z WAN součást **zápisové** cesty, kdežto asynchronní replikace z ní dělá součást cesty **zotavovací**. Jen to druhé přežije linku, která tam občas není.

Jediné, co z původního nápadu stojí za zachování, je instinkt za ním — že druhá lokalita má držet data, ne jen zálohy. Asynchronní replikace přesně to dělá; jen odmítá udělat z internetu podmínku toho, aby první lokalita dál fungovala.

## Reference

Externí zdroje (blok ověřen k 2026-08-14; dílčí data uvedena tam, kde se liší):

- RAIDZ Expansion: [The Register](https://www.theregister.com/2025/01/23/openzfs_23_raid_expansion/), [FreeBSD Foundation](https://freebsdfoundation.org/blog/raid-z-expansion-feature-for-zfs/), [caveat parity ratio](https://louwrentius.com/zfs-raidz-expansion-is-awesome-but-has-a-small-caveat.html)
- Granularita kódování (§20): [zpool-attach(8) — rozšíření RAIDZ zachovává úroveň parity](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-attach.8.html), [zpool-remove(8) — s top-level raidz nelze odstraňovat](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-remove.8.html), [Ceph — EC profily jsou neměnné](https://docs.ceph.com/en/latest/rados/operations/erasure-code/) (ověřeno 2026-08-14)
- Device removal / shrink limity: [OpenZFS zpool-remove](https://openzfs.github.io/openzfs-docs/man/v2.0/8/zpool-remove.8.html), [cr0x.net](https://cr0x.net/en/zfs-vdev-removal-limits/)
- SMR: [xda-developers](https://www.xda-developers.com/smr-hdds-are-fine-for-your-nas-until-you-try-to-resilver/), [vermaden](https://vermaden.wordpress.com/2024/05/29/zfs-resilver-smr-drives/), [OpenZFS #18132](https://github.com/openzfs/zfs/issues/18132)
- Fragmentace / defrag: [OpenZFS #3582](https://github.com/openzfs/zfs/issues/3582), [zfs-rewrite(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-rewrite.8.html), [#17246 — zavedení `zfs rewrite`](https://github.com/openzfs/zfs/pull/17246), [zpoolprops(7) — property `fragmentation`](https://openzfs.github.io/openzfs-docs/man/master/7/zpoolprops.7.html) (ověřeno 2026-08-14)
- Roztažené clustery (§31): [Ceph — Stretch Mode](https://docs.ceph.com/en/latest/rados/operations/stretch-mode/), [Ceph — Monitor/OSD interaction](https://docs.ceph.com/en/latest/rados/configuration/mon-osd-interaction/), [Red Hat Ceph Storage 8 — Stretch clusters](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/8/html/administration_guide/stretch-clusters-for-ceph-storage), [IBM Storage Ceph — Stretch clusters](https://www.ibm.com/docs/en/storage-ceph/8.0.0?topic=administration-stretch-clusters-ceph-storage) (ověřeno 2026-08-15; údaj 10 ms RTT je dodavatelský, upstream žádný neuvádí)
- Slovník (§29): [Ceph — Architecture](https://docs.ceph.com/en/latest/architecture/) (ověřeno 2026-08-15)
- `ashift` (§26): [zpoolprops(7) — property `ashift`](https://openzfs.github.io/openzfs-docs/man/master/7/zpoolprops.7.html) (ověřeno 2026-08-15)
- Malé soubory (§25): [zfsprops(7) — `recordsize`](https://openzfs.github.io/openzfs-docs/man/master/7/zfsprops.7.html), [zpool-features(7) — `embedded_data`](https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html), [Btrfs — `max_inline`](https://btrfs.readthedocs.io/en/latest/Administration.html) (ověřeno 2026-08-15)
- Block cloning (§24): [zfs(4) — `zfs_bclone_enabled`](https://openzfs.github.io/openzfs-docs/man/master/4/zfs.4.html), [zpool-features(7) — `block_cloning`](https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html) (ověřeno 2026-08-15 proti větvím 2.2, 2.3 a master)
- Fast Dedup: [Klara Systems](https://klarasystems.com/articles/introducing-openzfs-fast-dedup/), [despairlabs](https://despairlabs.com/blog/posts/2024-10-27-openzfs-dedup-is-good-dont-use-it/)
- Ceph dedup: [Ceph docs — Deduplication (experimental)](https://docs.ceph.com/en/latest/dev/deduplication/), [RGW Object Dedup](https://docs.ceph.com/en/latest/radosgw/s3_objects_dedup/)
- Změna velikosti ZVOLu (§23): [zfsprops(7) — `volsize`](https://openzfs.github.io/openzfs-docs/man/master/7/zfsprops.7.html), [Proxmox `qm(1)` — resize neumí zmenšit](https://pve.proxmox.com/pve-docs/qm.1.html) (ověřeno 2026-08-14)
- ZVOL shrink: [FreeBSD Forums](https://forums.freebsd.org/threads/zfs-set-volsize-data-loss.55854/), [TrueNAS](https://www.truenas.com/community/threads/shrink-zvol-of-vm.100519/)
- Snapshot automount / panic: [#13131](https://github.com/openzfs/zfs/issues/13131), [#13327](https://github.com/openzfs/zfs/issues/13327), [#17659](https://github.com/openzfs/zfs/issues/17659), [fix PR #17943](https://github.com/openzfs/zfs/pull/17943) (master 12/2025; mimo 2.3.6–2.3.8), [#18073](https://github.com/openzfs/zfs/issues/18073) (recv × du deadlock), [module params — `zfs_expire_snapshot`](https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Module%20Parameters.html)
- NFSv4 ACL na Linuxu: [#4966](https://github.com/openzfs/zfs/issues/4966), [WIP PR #13186](https://github.com/openzfs/zfs/pull/13186)
- CephFS snapshoty: [Ceph docs — CephFS Snapshots](https://docs.ceph.com/en/latest/dev/cephfs-snapshots/)
- Spolehlivostní profily (2026-08-01): [deep-research artefakt](https://claude.ai/public/artifacts/49c04b36-c45d-4b73-8652-c79f39de5ad5), [#15526 dirty dnode](https://github.com/openzfs/zfs/issues/15526), [#12014 encryption send/recv](https://github.com/openzfs/zfs/issues/12014), [#18041 import >90 % po výpadku](https://github.com/openzfs/zfs/issues/18041), [tracker #53192 — MDS latence se snapshoty (2021→fix 2025)](https://tracker.ceph.com/issues/53192), [Silvenga — CephFS metadata recovery (7/2024)](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/), [Rook #15273 — MDS trims při snapshotech (1/2025)](https://github.com/rook/rook/issues/15273), [CephFS best practices (Mimic)](https://docs.ceph.com/en/mimic/cephfs/best-practices/), [Btrfs RAID56 status](https://btrfs.readthedocs.io/en/latest/btrfs-man5.html)
- Ceph korupční bugy — timeline (ověřeno 2026-08-02): [advisory 14.2.3/14.2.4 (11/2019)](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/X6TNSDQK5DVKO6XFJW3DMJAJV63PLDYM/), [#45613 — bluefs_preextend_wal_files (5/2020)](https://tracker.ceph.com/issues/45613), [BlueFS >4GB writes (openSUSE advisory 5/2021)](https://osv.dev/vulnerability/openSUSE-SU-2021:0672-1), [#53062 — Pacific OMAP + IMPORTANT NOTICE (10/2021)](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/U4QX4E32BR5IOICOUW4FR7E56YEET3CN/), [Edinburgh — Anatomy of a CephFS disaster (9/2020)](https://blogs.ed.ac.uk/mhagdorn/2020/09/09/anatomy-of-a-cephfs-disaster/)
- ZFS korupční bugy — timeline (ověřeno 2026-08-06): [hole_birth #4996](https://github.com/openzfs/zfs/issues/4996), [Debian #830824](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=830824), [FAQ hole birth](https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ%20hole%20birth.html), [0.7.7→0.7.8 „mizející soubory“ (The Register, 4/2018)](https://www.theregister.com/2018/04/10/zfs_on_linux_data_loss_fixed/)
- Růst po jednom disku, EC vs RAIDZ2 (ověřeno 2026-08-13): [Ceph — Erasure code](https://docs.ceph.com/en/latest/rados/operations/erasure-code/), [Ceph — Erasure code profiles](https://docs.ceph.com/en/latest/rados/operations/erasure-code-profile/), [Ceph — Pools (min_size)](https://docs.ceph.com/en/latest/rados/operations/pools/), [Ceph — Create a CephFS](https://docs.ceph.com/en/latest/cephfs/createfs/), [Ceph dev — Erasure coding enhancements](https://docs.ceph.com/en/latest/dev/osd_internals/erasure_coding/enhancements/), [Ceph dev — Design of Pool Migration](https://docs.ceph.com/en/latest/dev/pool-migration-design/), [Ceph.io — Tentacle Fast EC performance](https://ceph.io/en/news/blog/2025/tentacle-fastec-performance-updates/), [ceph-users — best practice for Erasure Coding](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/QCEFF2DEGV2J6IQAIK3MKVBSX5BCQHAM/), [OpenZFS — RAIDZ](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/RAIDZ.html), [OpenZFS #17784](https://github.com/openzfs/zfs/issues/17784), [Proxmox — raidz extension pro PVE 9 / ZFS 2.3.3](https://lore.proxmox.com/pve-devel/20250717133753.408101-1-d.herzig@proxmox.com/), [Proxmox — Ceph Squid to Tentacle](https://pve.proxmox.com/wiki/Ceph_Squid_to_Tentacle)

---

*Vzniklo ve spolupráci s Claude (Anthropic); fakta ověřena proti uvedeným zdrojům k červenci 2026, doplňky (snapshot vrstva, spolehlivostní profily, timelines korupčních bugů) k 1.–6. srpnu 2026, doplněk o růstu po jednom disku k 13. srpnu 2026, a aktualizace automount vrstvy, sekce o námitkách, oprava k `zfs rewrite`, sekce o granularitě kódování, checklist rozhodnutí při vytvoření, sekce o objektovém modelu i sekce o změně velikosti ZVOLu k 14. srpnu 2026 a oprava k block cloningu sekce o malých souborech, sekce o `ashift` prohlídka §21, oprava k `recordsize`, slovník, sekce o počtu uzlů i sekce o roztaženém clusteru k 15. srpnu 2026. Dokument je datovaný snapshot a průběžně se neaktualizuje.*

*© 2026 Petr Kratochvíl · Licence [CC BY 4.0](../LICENSE)*
