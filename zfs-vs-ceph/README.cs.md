# ZFS vs Ceph — volba storage enginu pro malý self-hosted cluster

- **Verdikt:** ⭐ **ZFS na Proxmox VE** — platí pro kontext popsaný níže
- **Fakta ověřena:** červenec 2026 (datovaný snapshot; dokument se zpětně neaktualizuje)
- **Jazyk:** český originál · [English version](README.md)
- **Autor:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Kontext: pro jaký profil se rozhodovalo

Tohle není obecné srovnání „co je lepší". Je to reálná rozhodovací analýza z konkrétního projektu — verdikt si nárokuje platnost jen pro tenhle profil a s jiným profilem může klidně vyjít opačně:

- **Osobní cluster, fázovaný start:** začíná se **1 uzlem**, časem růst na 2–3 uzly ve **2 lokalitách** (běžné byty, mezi nimi rezidenční WAN).
- **Solo admin bez on-call** — provoz musí zvládnout jeden člověk, i „ve 3 ráno".
- **Cost-conscious rok 2026:** DDR4 ECC v doběhu výroby (ceny rostou), HDD trh vyprodaný — každý GB RAM a každý disk navíc bolí.
- **Workload:** bulk média/foto/dokumenty (cíl ~150 TiB) + hrstka VM a služeb (Plex, Nextcloud, monitoring typu Zabbix/Grafana/Loki); zvažovaný Kubernetes.
- **Výchozí stav:** stávající single-node server `mdadm RAID6 + dm-crypt/LUKS + LVM + Btrfs` (třetí sloupec srovnávací tabulky). Z něj se migruje; po migraci poslouží jako geo DR cíl ve druhé lokalitě. Doplněk: cloudové úložiště s tvrdým měsíčním transfer stropem.
- **HA nároky:** ztráta ~1 minuty dat při pádu uzlu je přijatelná (RPO ≤ 1 min); synchronní replikace přes WAN se nepožaduje.

## Shrnutí (TL;DR)

1. ⭐ **Doporučení: ZFS na Proxmox VE, ne Ceph** — pro profil „1–3 uzly, solo admin, cost-conscious, bulk + pár služeb, fázování" vyhrává ZFS téměř ve všem, co reálně pálí: **dává plnou hodnotu už od 1 uzlu** (Ceph je na 1 uzlu anti-pattern), **řádově méně RAM** (přímá úspora v DDR4 krizi), jednodušší provoz, čisté DR přes `send`/`recv`, lepší kapacitní efektivita na malé škále (RAIDZ2 75 % vs Ceph `size=3` 33 %).
2. **Všechny čtyři moje původní výhrady ke ZFS se rozpustily** (§2): mixed-size (→ nový vdev), „pomalost" (→ SMR + plný pool, ne ZFS samo), shrink (→ platí jen pro **pool**, ne pro **ZVOL**), tichá korupce (→ ZFS to řeší nativně; stávající mdadm+Btrfs stack by to dohnal jen vrstvou `dm-integrity`).
3. **HA nezávisí na volbě engine, ale na počtu uzlů** (§4). Na 1 uzlu není HA s ničím (ani s Ceph). ZFS HA řeší **Proxmox ZFS replikace + HA manager + arbitr** (orchestrovaný failover, RPO ~1 min) — pro daný use-case dostatečné. Přes WAN neexistuje real-time HA s žádným enginem.
4. **Ceph si drží reálnou výhodu jen ve třech věcech** (§7, §9): distribuované/shared storage (živá migrace VM, **K8s RWX PV**), nativní **S3/RGW** a automatický self-heal přes uzly. **Oba relevantní body prověřeny (§14) a ani jeden Ceph nevyžaduje** — monitoring HA (Zabbix/Grafana/Loki) se řeší app-level + RWO, Kopia zálohy S3 nepotřebují → **volba padla na ZFS**.
5. **Migrační past ZFS→Ceph je reálná, ale volitelná** (§10): existuje jen tehdy, když je cílem Ceph. Zůstat u ZFS celou cestu (1 uzel → +2 uzly + replikace) past ruší — uzel 1 se nikdy nemaže.

## Srovnání v přehledu

Symboly: ✅ silná stránka · 🟡 jde s výhradou / kompromis · ❌ slabina nebo chybí · — neaplikovatelné. Hodnoceno pro **tento kontext** (1–3 uzly, homelab, solo admin, Kubernetes, bulk média + pár služeb) — ne obecně; na velkém symetrickém clusteru by řada řádků vyšla ve prospěch Ceph. Poslední sloupec = **výchozí single-node server** (mdraid + dm-crypt/LUKS + LVM + Btrfs), odkud se migruje (viz Kontext).

| Kritérium | ZFS (na Proxmox VE) | Ceph | Výchozí (mdraid+LUKS+LVM+Btrfs) |
|---|---|---|---|
| **▸ Nasazení & náklady** | | | |
| Min. smysluplný počet uzlů | ✅ **1** | ❌ 3 (2+arbitr křehké) | ✅ 1 (je single-node) |
| RAM na uzel | ✅ ~64 GB (ARC flexibilní) | ❌ ~96–128 GB (~4 GB/OSD) | ✅ nízká |
| Síť mezi uzly | ✅ 1 GbE stačí (async) | 🟡 10 GbE ~povinnost | — (single-node) |
| Komplexita provozu | ✅ `zpool`/`zfs`, 1 vrstva | ❌ 5+ démonů, CRUSH, PG | 🟡 4 vrstvy, víc nástrojů |
| **▸ Data & integrita** | | | |
| Auto oprava tiché korupce | ✅ nativní (scrub/resilver) | ✅ nativní (BlueStore) | ❌ **detekuje (Btrfs), neopraví** |
| Kapacitní efektivita | ✅ RAIDZ2 75 % (inkrementálně rostlé ~67–70 % do rewritu, §2.1) | 🟡 size=3 33 % (EC lepší, chce uzly) | ✅ RAID6 ~75 % |
| Fragmentace při plnosti (společná všem) | 🟡 ano (CoW) | 🟡 ano (BlueStore) | 🟡 ano (Btrfs CoW) + ENOSPC |
| Defrag / úklid fragmentace | 🟡 rewrite `send/recv` (bez nástroje, CoW-safe) | 🟡 reweight OSD / rewrite (CoW-safe, zachová snapshoty) | ✅ `defragment` + `balance` (ale **ničí reflinky**) |
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
| POSIX (UTF-8 názvy, ACL, nanosec časy, xattr) | ✅ plný + NFSv4 ACL, volitelná UTF-8 normalizace | ✅ CephFS POSIX (drobné odchylky z distribuce) | ✅ plný nativní Linux |
| K8s persistent volumes | 🟡 local-PV RWO (`zfs-localpv`) | ✅ distribuované RWX (`ceph-csi`) | 🟡 local-PV (LVM CSI) |
| Nativní S3 / object storage | ❌ (jen MinIO/Garage navrch) | ✅ RGW | ❌ (jen MinIO navrch) |
| Deduplikace (auto, block-level) | 🟡 Fast Dedup, radši PBS | 🟡 experimentální / RGW batch | 🟡 Btrfs bees (batch) |
| Reflink klon (`cp --reflink`) | 🟡 block cloning (2.2+), default off, cross-dataset ne | ❌ CephFS neumí (jen server-side copy) | ✅ nativní, stabilní |
| Komprese — algoritmy | ✅ lz4 (default) + zstd (laditelný) | ✅ lz4/zstd/snappy/zlib (per-pool) | ✅ zstd/lzo/zlib |
| Změna komprese u existujících dat | 🟡 jen nová data (rewrite `send/recv`) | 🟡 jen nová data (rewrite) | ✅ in-place `defragment -c` |
| Šifrování at-rest | ✅ ZFS native / LUKS | ✅ LUKS pod OSD | ✅ dm-crypt/LUKS |
| Zálohy / DR | ✅ `send`/`recv` + PBS (čisté) | 🟡 3 rozhraní, mirroring křehký | 🟡 Btrfs send + snapshoty |
| **▸ Škálování & fázování** | | | |
| Škálování na 10+ uzlů / PB | 🟡 per-node (replikace) | ✅ nativní | ❌ single-node |
| Fázování 1 → 3 uzly | ✅ bez migrační pasti | ❌ migrační past (nebo start 3 uzly) | ❌ není cluster |
| Zralost / komunita | ✅ 20 let, obří base | ✅ zralý, menší homelab base | ✅ zralé (Btrfs na LV, ne RAID5/6) |

### Co z toho plyne

- **ZFS vede** v nasazení, nákladech, jednoduchosti, kapacitě, fázování a DR — ve všem, co v pozici „solo, cost-conscious, fázovaný start" pálí nejvíc.
- **Vyrovnané** je to v podstatném: ochrana dat proti korupci, VM failover, šifrování, blokové zařízení.
- **Ceph vede** v distribuovaném PV (K8s RWX), nativním S3, RPO 0, auto-recovery přes uzly a škálování.
- **Výchozí řešení** (poslední sloupec) má tři slabiny, kvůli kterým se migruje: **neopravuje tichou korupci** (jen ji detekuje přes Btrfs), **nemá HA** a jsou to **čtyři vrstvy**. ZFS všechny tři řeší v jedné vrstvě.

Z Ceph výher se tohoto projektu reálně týkají jen **dvě — K8s RWX PV a nativní S3** (viz §7, §14). RPO 0 jsem přijal jako nepotřebné (≤ 1 min stačí), auto-recovery i škálování míří na velké symetrické clustery, ne na plánovanou sestavu uzel 1 + uzel 2 + arbitr.

---

## 1. Východisko: proč vůbec přehodnocovat Ceph

Spouštěč byl nápad **postavit zatím jen 1 uzel** a škálovat časem (ceny RAM a HDD v roce 2026 vysoké, DDR4 ECC EOL). To odhalilo zásadní konflikt:

- **„1-node Ceph cluster" je protimluv.** Ceph dává hodnotu z distribuce a self-healu *přes uzly*; na jednom uzlu (`size=1`) platíš celou jeho komplexitu (MON/MGR/OSD, RAM ~4 GB/OSD, ladění) a nedostaneš nic, co by ZFS nedalo jednodušeji — vlastnosti, kvůli kterým Ceph existuje, na jednom uzlu mizí.
- Naopak **ZFS je od návrhu single-node** a škáluje replikací → sedí na fázování 1 → 2 → 3 uzly bez mezikroku.

Tím se otázka „jak dělat Ceph fázovaně" změnila na **„potřebuješ vůbec Ceph, nebo je to over-engineering pro tvůj kontext?"**

## 2. Moje původní výhrady ke ZFS a jak dopadly

| # | Výhrada | Verdikt | Řešení |
|---|---------|---------|--------|
| 1 | ZFS vyžaduje stejně velké disky (jinak plýtvá) | 🟡 platí **uvnitř vdev**, ne napříč poolem | Růst uvnitř generace = stejná velikost; generační skok (větší disky) = **nový vdev**. RAIDZ Expansion (OpenZFS 2.3, 2025) přidá disk po jednom. |
| 2 | ZFS byl vždy „velmi pomalý" | ❌ není vlastnost ZFS | Můj dřívější test běžel na **SMR disku s téměř plným poolem** = worst case (viz §2.2). Bulk workload na CMR + dost RAM je rychlý. |
| 3 | ZFS neumí shrink (jen expand) | 🟡 platí pro **pool/RAIDZ vdev**, **ne pro ZVOL** | Shrink RAIDZ vdev nejde; shrink **ZVOL** (blokové zařízení) jde (§6). Dvě různé operace! |
| 4 | (výchozí server) tichá korupce se detekuje, ale neopraví | ✅ reálná díra | `dm-integrity` (stávající stack) nebo ZFS nativně (§3). |

### 2.1 Mixed-size disky

- **Uvnitř RAIDZ vdev:** smallest disk wins, větší se ořízne → plýtvání. Pravda.
- **Napříč poolem:** pool = sada vdevů; `vdev1 = 5× 30 TB` + později `vdev2 = 5× 60 TB` je v pořádku. „Za pár let větší disky" se řeší novým vdev.
- **RAIDZ Expansion (2.3, led. 2025):** přidání jednoho disku do existujícího RAIDZ vdev online. Caveat: stará data drží **starý data:parity poměr**, dokud nejsou přepsána (kapacita roste inkrementálně); nemění RAID level ani ashift. Přesně pokrývá plán „růst 1+2 → 2+2 → 3+2" (= RAIDZ2 s rostoucím počtem datových jednotek).

**Kapacitní cena inkrementálního růstu (příklad).** Pokud disky přidáváš po jednom vždy při ~80 % zaplnění, drží každá „vrstva" dat parity poměr z doby zápisu — a plnou efektivitu cílové šířky nedostaneš, dokud data nepřepíšeš. Modelový růst RAIDZ2 ze 4 na 7 disků po 32 TB (80 % fill = 80 % raw, přidání při dosažení):

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

### 2.2 „Pomalost" — příčiny

- **SMR disky** (shingled): resilver benchmark **CMR 14,5 h vs SMR 9,5 dne (16×)**; random I/O SMR je „utterly terrible", CoW walk resilveru to zhoršuje. SMR do RAID/NAS nepatří — potopí i Btrfs a Ceph.
- **Plný pool** (CoW): nad ~80 % fillu roste fragmentace (ZFS nemá defragmentaci — „block pointer rewrite" je nedodaný od 2015), výkon velkých bloků padá.
- **RAIDZ = IOPS jednoho disku** pro random workload (1 vdev). Pro sekvenční bulk (média, foto, backup) je rychlé.
- **Mitigace:** CMR disky, dost RAM pro ARC, SLOG pro sync writes, pool < 80 %, a **separátní SSD/NVMe pool pro VM** (random) oddělený od HDD bulk poolu.

### 2.3 Shrink — pool vs ZVOL (klíčové rozlišení)

Nezaměňovat dvě různé operace:
- **Shrink poolu / RAIDZ vdev** (ubrat fyzický disk): ❌ **nejde.** `zpool remove` umí jen mirror/stripe/cache/log/special vdev, **ne RAIDZ**.
- **Shrink ZVOL** (logické blokové zařízení uvnitř poolu): ✅ **jde** (§6). Pool zůstává, ZVOL se zmenší.

### 2.4 Tichá korupce — viz §3.

## 3. Tichá korupce: dm-integrity vs ZFS nativně

Hlavní bolest mého stávajícího serveru (`mdraid + dm-crypt/LUKS + LVM + Btrfs`): tichou korupci (plotna, firmware disku, řadič, kabel) **Btrfs detekuje** (checksum → `EIO`), ale **mdraid neopraví** — Btrfs nevidí na paritu (je pod ním), mdraid nemá per-blok checksumy a neví, který disk lže.

**Řešení jsou dvě, obě vyžadují rebuild pole:**

1. **`dm-integrity` pod mdraid** (nebo LVM RAID s `--raidintegrity y`): dá každému sektoru checksum → při korupci vrátí **chybu čtení místo špatných dat** → RAID6 dopočítá z parity a přepíše. Převádí „tichou" korupci na „hlasitou", kterou RAID umí. Cena: ~10–30 % write overhead, +1 vrstva.
2. **ZFS** to má vestavěné nativně (checksum + redundance + self-heal v jedné vrstvě, 75 % efektivita u RAIDZ2).

**Důsledek pro rozhodnutí:** protože oprava korupce **stejně vyžaduje rebuild pole**, padá argument „aspoň nemusím nic měnit". Rebuild bude tak jako tak — otázka je jen na co (ZFS vs mdadm/LVM+integrity).

## 4. HA: nezávisí na engine, ale na počtu uzlů

- **1 uzel = žádné HA s ničím** (ani single-node Ceph — není na co failovat). HA je otázka **„1 uzel vs 2 uzly", ne „ZFS vs Ceph".**
- **ZFS HA** (Proxmox VE):
  - **Proxmox ZFS replikace (`pvesr`) + HA manager** — async replika zvolů (interval min. 1 min) + automatický restart VM na jiném uzlu z poslední repliky. Měkké HA (RPO ~1 min, failover = restart, ne živá migrace). Pro média/foto/dokumenty/běžné služby dostatečné.
  - **DRBD-over-ZFS** — sync replika lokálního páru (RPO 0), tvrdé HA pro DB. Komplexnější.
- **Přes WAN žádné real-time HA s žádným enginem** — synchronní zápisy přes rezidenční WAN (latence, jitter, výpadky) jsou showstopper. Geo úroveň je vždy jen async DR.

### 4.1 „Orchestrovaný failover" (co to znamená)

Ceph je **shared storage** → data dostupná ze všech uzlů → failover = triviální restart VM jinde. ZFS je **shared-nothing** → replika na druhém uzlu je samostatný, zpožděný, read-only pool. Failover proto vyžaduje vrstvu nad storage (orchestrátor), která provede: **detekci → fencing → promotion repliky → start služby → přesměrování → (po návratu) failback**. Proxmox HA manager to zvládne **automaticky** (orchestrovaný ≠ ruční), daň je RPO > 0, restart místo živé migrace, a fencing/failback komplexita.

### 4.2 Scénář „uzel 1 shoří" (řešení bez Ceph)

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
- „Musí běžet pořád" (Plex, *arr, Nextcloud, DNS…) → HA + replikace 1 min.
- „Nevadí delší výpadek" → bez HA, jen zálohy do PBS.
- „Ani minuta ztráty" (DB s aktivními transakcemi) → doplnit **app-level replikací** (Patroni ap.), ne kvůli tomu stavět Ceph.

## 5. Deduplikace: neřešit na storage, řeší ji PBS

- **ZFS legacy dedup** = pověstných ~5 GB RAM/TB (pro 150 TiB nereálné). **Fast Dedup (OpenZFS 2.3, 2025)** to zmírnil (DDT log/prefetch/prune/quota, DDT na special vdev), ale i tak je pomalejší než žádná dedup. Konsenzus: „dedup je teď dobrá — a stejně ji nepoužívej."
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
3. **Jednoduchost** — `zpool`/`zfs`, jedna vrstva, provoz „ve 3 ráno" pro solo admina bez on-call.
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

**Doporučení: LUKS + Clevis/Tang** (Tang na RPi5 arbitru), ideálně i encrypted root. Na Proxmoxu (Debian) jsou to standardní balíčky (`clevis-luks`, `clevis-initramfs`, `tang`), ale setup je ruční (instalátor šifrování root nenabízí). DR/zálohy šifruje **PBS client-side** nezávisle. Alternativa: ZFS native encryption + passphrase (umí `send --raw` = šifrované repliky bez klíče na DR straně), ale Tang unlock je s ním DIY.

**Past:** klíč (keyfile) na **nešifrovaném rootu** = útočník ho z ukradeného disku přečte → šifrování k ničemu. Proto odemykač zvenčí (Tang/passphrase), ne keyfile na plaintext disku.

**Hranice:** chrání *vypnutý* ukradený stroj; běžící/odemčený je jiná věc. **BMC/IPMI je samostatný attack surface** — mimo rozsah této analýzy.

## 13. Fill ratio a reálně použitelná kapacita

Fill strop je u obou podobný (~80 %), takže **sám o sobě velký rozdíl nedělá** — hlavní kapacitní rozdíl je replikační overhead (viz „Srovnání v přehledu", řádek Kapacitní efektivita).

- **ZFS:** ~80 % kvůli výkonu/fragmentaci (CoW); nad to zpomaluje (ne ztráta dat), nad ~95 % vážně.
- **Ceph:** thresholdy `nearfull` 85 %, `backfillfull` 90 %, `full` 95 % (zápisy stop). Navíc **rezerva na self-heal** — výpadek OSD/uzlu se musí vejít na zbývající → prakticky ~75–80 %, **na málo uzlech míň** (výpadek 1 ze 3 = 33 % musí mít kam). ZFS tuto rezervu nepotřebuje.

**Reálně použitelné z každých 100 TB nakoupených disků** (usable × 80 % fill):

| Konfigurace | Reálně data |
|---|---|
| ZFS RAIDZ2 (75 % × 80 %) | ~60 TB |
| Ceph `size=3` (33 % × 80 %) | ~27 TB |

U 150 TiB cíle je ten rozdíl desítky disků a klidně 100 000+ Kč v železe — ale pochází z replikace, ne z fill ratio.

## 14. Rozhodnutí

Tři otázky, které v průběhu analýzy zbývaly otevřené, dopadly takhle:

1. **K8s persistent volumes — RWX není potřeba.** Plánované aplikace (Zabbix, Grafana, Loki, Prometheus) dělají HA na aplikační vrstvě (víc replik + sdílená DB / Patroni), ne přes sdílený storage → `zfs-localpv` (RWO) + Proxmox HA stačí.
2. **S3/RGW — není potřeba.** Jediný zvažovaný důvod (zálohy přes Kopia) S3 nevyžaduje — Kopia umí filesystem/SFTP repozitář; nice-to-have pokryje MinIO nad ZFS.
3. **HA model — přijat.** Orchestrovaný failover (RPO ≤ 1 min, RTO ~2–5 min, failback živou migrací; §4.3) je pro tento profil dostatečný.

**→ Verdikt: ZFS na Proxmox VE.** Ceph by na 1–3 uzlech nepřidal nic, co by tenhle projekt reálně využil — platil by se trvalou daní v RAM, síti a provozní komplexitě. Na velkém symetrickém clusteru s mnoha klienty by verdikt klidně vyšel opačně — přesně proto je celá analýza ukotvená ke kontextu v úvodu.

## Reference

Externí zdroje (ověřeno 2026-07):

- RAIDZ Expansion: [The Register](https://www.theregister.com/2025/01/23/openzfs_23_raid_expansion/), [FreeBSD Foundation](https://freebsdfoundation.org/blog/raid-z-expansion-feature-for-zfs/), [caveat parity ratio](https://louwrentius.com/zfs-raidz-expansion-is-awesome-but-has-a-small-caveat.html)
- Device removal / shrink limity: [OpenZFS zpool-remove](https://openzfs.github.io/openzfs-docs/man/v2.0/8/zpool-remove.8.html), [cr0x.net](https://cr0x.net/en/zfs-vdev-removal-limits/)
- SMR: [xda-developers](https://www.xda-developers.com/smr-hdds-are-fine-for-your-nas-until-you-try-to-resilver/), [vermaden](https://vermaden.wordpress.com/2024/05/29/zfs-resilver-smr-drives/), [OpenZFS #18132](https://github.com/openzfs/zfs/issues/18132)
- Fragmentace / defrag: [OpenZFS #3582](https://github.com/openzfs/zfs/issues/3582)
- Fast Dedup: [Klara Systems](https://klarasystems.com/articles/introducing-openzfs-fast-dedup/), [despairlabs](https://despairlabs.com/blog/posts/2024-10-27-openzfs-dedup-is-good-dont-use-it/)
- Ceph dedup: [Ceph docs — Deduplication (experimental)](https://docs.ceph.com/en/latest/dev/deduplication/), [RGW Object Dedup](https://docs.ceph.com/en/latest/radosgw/s3_objects_dedup/)
- ZVOL shrink: [FreeBSD Forums](https://forums.freebsd.org/threads/zfs-set-volsize-data-loss.55854/), [TrueNAS](https://www.truenas.com/community/threads/shrink-zvol-of-vm.100519/)

---

*Vzniklo ve spolupráci s Claude (Anthropic); fakta ověřena proti uvedeným zdrojům k červenci 2026. Dokument je datovaný snapshot a zpětně se neaktualizuje.*

*© 2026 Petr Kratochvíl · Licence [CC BY 4.0](../LICENSE)*
