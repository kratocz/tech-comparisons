# ZFS vs Ceph: choosing the storage engine for a small self-hosted cluster

- **Verdict:** ⭐ **ZFS on Proxmox VE** — valid for the context described below
- **Facts verified:** July 2026 · addenda 2026-08-01/06 (the Linux snapshot layer §2.5–2.6; reliability profiles incl. the Ceph and ZFS corruption-bug timelines §15) · **2026-08-13 (growing one disk at a time, EC 2+2 vs RAIDZ2 §16 — including two corrections to earlier claims)** · **2026-08-14 (the snapshot automount layer rewritten upstream but still unreleased — §17; the eight objections keeping the decision open, with a pre-registered measurement rule — §18; **correction: `zfs rewrite` exists and four claims were wrong** — §19)**
- **Language:** 🇬🇧 English (canonical) · 🇨🇿 [Čeština — original](README.cs.md)
- **Author:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Context: the profile this decision was made for

This is not a generic "which one is better" comparison. It is a real decision analysis from a real project — the verdict claims validity only for this profile, and a different profile may well flip it:

- **Personal cluster, phased start:** begins with **a single node**, growing over time to 2–3 nodes across **two sites** (ordinary apartments, connected by residential WAN links).
- **Solo admin, no on-call** — operations must be manageable by one person, including "at 3 a.m."
- **Cost-conscious 2026:** DDR4 ECC production is winding down (prices climbing), the HDD market is sold out — every extra GB of RAM and every extra drive hurts.
- **Workload:** bulk media/photos/documents (~150 TiB target) plus a handful of VMs and services (Plex, Nextcloud, monitoring à la Zabbix/Grafana/Loki); Kubernetes under consideration.
- **Starting point:** an existing single-node server running `mdadm RAID6 + dm-crypt/LUKS + LVM + Btrfs` (the third column of the comparison table). It is the migration source, and afterwards it becomes the geo DR target at the second site. Complemented by cloud storage with a hard monthly transfer cap.
- **HA requirements:** losing ~1 minute of data on node failure is acceptable (RPO ≤ 1 min); synchronous replication across the WAN is not required.

## Summary (TL;DR)

1. ⭐ **Recommendation: ZFS on Proxmox VE, not Ceph** — for the profile "1–3 nodes, solo admin, cost-conscious, bulk + a few services, phased growth", ZFS wins almost everywhere it actually matters here: **full value from a single node** (Ceph on one node is an anti-pattern), **an order of magnitude less RAM** (a direct saving amid the DDR4 crunch), simpler operations, clean DR via `send`/`recv`, better capacity efficiency at small scale (RAIDZ2 75 % vs Ceph `size=3` 33 %).
2. **Four of my six original objections to ZFS dissolved** (§2): mixed-size disks (→ add a new vdev), "slowness" (→ SMR + a full pool, not ZFS itself), shrink (→ true for the **pool**, not for **ZVOLs**), silent corruption (→ ZFS handles it natively; the existing mdadm+Btrfs stack could only catch up by adding a `dm-integrity` layer). **Two confirmed ones remain** (§2.5): browsing snapshots = a separate mount per snapshot (the design never changed) and a snapshot-automount panic bug — the upstream fix only landed 12/2025 (PR #17943) and is still missing from the 2.3.x LTS line as of 8/2026. The mitigations are simple (`snapdir=hidden` is the default, `zfs diff`/clone), but it is the weakest part of ZFS on Linux.
3. **HA depends on node count, not on the engine** (§4). With one node there is no HA with anything (not even Ceph). ZFS HA is handled by **Proxmox ZFS replication + HA manager + an arbiter** (orchestrated failover, RPO ~1 min) — sufficient for this use case. Across a WAN, no engine gives you real-time HA.
4. **Ceph keeps a real edge in only three things** (§7, §9): distributed/shared storage (live VM migration, **K8s RWX PVs**), native **S3/RGW**, and automatic self-healing across nodes. **Both relevant items were examined (§14) and neither requires Ceph** — monitoring HA (Zabbix/Grafana/Loki) is solved app-level + RWO, and Kopia backups don't need S3 → **the decision went to ZFS**.
5. **The ZFS→Ceph migration trap is real but optional** (§10): it only exists if Ceph is the destination. Staying on ZFS the whole way (1 node → +2 nodes + replication) removes it — node 1 is never wiped.
6. **The reliability deep research (§15) favours ZFS.** ZFS has the most mature integrity track record — serious bugs are rare and fixed (dirty dnode 2023; encryption send/recv closed in 2025), and **the LUKS path is untouched by them**. Ceph's risks sit exactly where this project was headed: **CephFS snapshots + multi-MDS** (incidents spanning 2021→2025), **operator error** (the main source of real-world loss; solo admin), and **practically mandatory PLP SSDs** (the planned NVMe drives are consumer-class).

## Comparison at a glance

Symbols: ✅ strength · 🟡 works with caveats / a compromise · ❌ weakness or missing · — not applicable. Rated for **this context** (1–3 nodes, homelab, solo admin, Kubernetes, bulk media + a few services) — not in general; on a large symmetric cluster many rows would come out in Ceph's favour. The last column is the **starting single-node server** (mdraid + dm-crypt/LUKS + LVM + Btrfs) being migrated away from (see Context).

| Criterion | ZFS (on Proxmox VE) | Ceph | Current (mdraid+LUKS+LVM+Btrfs) |
|---|---|---|---|
| **▸ Deployment & cost** | | | |
| Min. meaningful node count | ✅ **1** | ❌ 3 (2+arbiter is fragile) | ✅ 1 (it is single-node) |
| RAM per node | ✅ ~64 GB (ARC is flexible) | ❌ ~96–128 GB (~4 GB/OSD) | ✅ low |
| Inter-node network | ✅ 1 GbE suffices (async) | 🟡 10 GbE ~mandatory | — (single-node) |
| SSD requirements (PLP) | 🟡 PLP only for a SLOG (not planned) | ❌ practically mandatory (BlueStore fsync) — consumer NVMe won't do (§15) | ✅ no special requirements |
| Operational complexity | ✅ `zpool`/`zfs`, one layer | ❌ 5+ daemons, CRUSH, PGs | 🟡 4 layers, more tools |
| **▸ Data & integrity** | | | |
| Auto-repair of silent corruption | ✅ native (scrub/resilver) | ✅ native (BlueStore) | ❌ **detects (Btrfs), can't repair** |
| Data-loss bug history (§15) | 🟡 rare, fixed fast (dnode 2023; encryption send/recv closed 2025) | 🟡 core mature (CERN); fragile: CephFS snapshots+multi-MDS, operator error | 🟡 Btrfs RAID5/6 ❌ permanently (here on LV over mdadm ✓) |
| Capacity efficiency | ✅ RAIDZ2 75 % (grown incrementally ~67–70 % until rewritten, §2.1) | 🟡 size=3 33 % (EC realistically from ~5–6 nodes; on 3 only k=2,m=1) | ✅ RAID6 ~75 % |
| Fragmentation when full (common to all) | 🟡 yes (CoW) | 🟡 yes (BlueStore) | 🟡 yes (Btrfs CoW) + ENOSPC |
| Defrag / cleanup | ✅ `zfs rewrite` — defragmenting files and rebalancing after `zpool add` are stated purposes; loses its grip on a near-full pool (§19) | 🟡 OSD reweight / rewrite (CoW-safe, keeps snapshots) | ✅ `defragment` + `balance` (but **breaks reflinks**) |
| CoW granularity (1-byte write) | 🟡 128K record (tunable 4K–1M; ZVOL 16K) | ❌ 4 MB with a snapshot (~4K without) | ✅ 4K (`nodatacow` for DBs = 0) |
| Mixed-size disks | 🟡 across vdevs yes, wasteful within one | ✅ CRUSH weights | 🟡 mdadm smallest wins |
| Add a disk (expand) | ✅ RAIDZ expansion (2.3) — old data keeps the old parity ratio until rewritten (§2.1) | ✅ trivial | ✅ mdadm `--grow` reshape (rewrites, no parity caveat) |
| Remove a disk / shrink the pool | ❌ not for RAIDZ | ✅ `osd out` + rebalance | 🟡 mdadm reshape (possible, slow) |
| Raise redundancy (add parity) | ❌ RAIDZ2→Z3 in-place no (migration only) | ✅ `size` at runtime (EC profile no) | 🟡 mdadm RAID5→6 reshape (nothing higher exists) |
| Shrink an LV/ZVOL/RBD (VM disk) | ✅ yes (FS first) | ✅ yes (`--allow-shrink`) | ✅ `lvreduce` (FS first) |
| **▸ HA & availability** | | | |
| Auto VM failover on node loss | ✅ Proxmox HA + replication | ✅ yes | ❌ no HA |
| RPO (data loss) | 🟡 ≤ 1 min (async) | ✅ 0 (sync) | ❌ backups only |
| RTO (VM downtime) | 🟡 ~2–5 min | 🟡 ~2–5 min | ❌ manual recovery |
| Live VM migration (zero downtime) | 🟡 planned only (with replication) | ✅ any time (shared) | ❌ |
| Auto redundancy recovery after node loss | 🟡 orchestrated (failback) | ✅ automatic (needs 3+ full nodes) | ❌ (single-node) |
| Geo HA across a WAN | ❌ async DR only | ❌ async DR only (sync = showstopper) | ❌ |
| **▸ Features / workloads** | | | |
| Block device for VMs | ✅ ZVOL (local) | ✅ RBD (distributed) | ✅ LVM LV (local) |
| POSIX (UTF-8 names, ACLs, ns timestamps, xattrs) | ✅ full — POSIX ACLs (the Linux VFS cannot enforce NFSv4 ACLs, §2.6), optional UTF-8 normalization | ✅ CephFS POSIX (minor deviations from being distributed) | ✅ full native Linux |
| K8s persistent volumes | 🟡 local-PV RWO (`zfs-localpv`) | ✅ distributed RWX (`ceph-csi`) | 🟡 local-PV (LVM CSI) |
| Native S3 / object storage | ❌ (only MinIO/Garage on top) | ✅ RGW | ❌ (only MinIO on top) |
| Deduplication (auto, block-level) | 🟡 Fast Dedup, prefer PBS | 🟡 experimental / RGW batch | 🟡 Btrfs bees (batch) |
| Reflink clone (`cp --reflink`) | 🟡 block cloning (2.2+), default off, no cross-dataset | ❌ CephFS can't (server-side copy only) | ✅ native, stable |
| Compression — algorithms | ✅ lz4 (default) + zstd (tunable) | ✅ lz4/zstd/snappy/zlib (per-pool) | ✅ zstd/lzo/zlib |
| Recompressing existing data | ✅ in-place `zfs rewrite -r` (§19) | 🟡 new data only (rewrite) | ✅ in-place `defragment -c` |
| At-rest encryption | ✅ ZFS native / LUKS | ✅ LUKS under OSDs | ✅ dm-crypt/LUKS |
| Backups / DR | ✅ `send`/`recv` + PBS (clean) | 🟡 3 interfaces, fragile mirroring | 🟡 Btrfs send + snapshots |
| Browsing many snapshots (grepping history) | 🟡 one mount per snapshot (`.zfs` automount; prefer `zfs diff`/clone, §2.5) | ✅ CephFS `.snap`, no mounts (RBD ❌ manual map+mount) | ✅ subvolumes, no mounts (beware: own `st_dev`) |
| Snapshot-layer stability | ❌ automount: history of panics; fix #17943 missing from 2.3.x LTS as of 8/2026 (§2.5) | 🟡 no automount layer, but CephFS snapshots themselves = the most fragile area (MDS trims, §15) | ✅ subvolume snapshots mature |
| **▸ Scaling & phasing** | | | |
| Scaling to 10+ nodes / PB | 🟡 per-node (replication) | ✅ native | ❌ single-node |
| Phasing 1 → 3 nodes | ✅ no migration trap | ❌ migration trap (or start with 3) | ❌ not a cluster |
| Maturity / community | ✅ 20 years, huge base | ✅ mature, smaller homelab base | ✅ mature (Btrfs on LV, not its RAID5/6) |

### What this means

- **ZFS leads** in deployment, cost, simplicity, capacity, phasing and DR — everything that hurts most in the "solo, cost-conscious, phased start" position.
- **It's a tie** on the essentials: data corruption protection, VM failover, encryption, block devices.
- **Ceph leads** in distributed PVs (K8s RWX), native S3, RPO 0, auto-recovery across nodes, and scaling.
- **The current solution** (last column) has the three weaknesses driving the migration: it **cannot repair silent corruption** (Btrfs only detects it), it **has no HA**, and it is **four layers**. ZFS fixes all three in a single layer.
- 🆕 **(2026-08-01)** The weakest spot of ZFS on Linux is the **snapshot automount layer** (`.zfs/snapshot`): one mount per snapshot plus a history of panics/deadlocks, with the latest fix only landing 12/2025 and not yet in the 2.3.x LTS line (§2.5). CephFS and Btrfs solve this by design — the first row where the incumbent stack genuinely beats ZFS.
- 🆕 **(2026-08-01, reliability)** The deep research (§15) favours ZFS: this design systematically routes around ZFS's risks (fresh features, native encryption), while Ceph's risks (fragile CephFS snapshots, operator error, mandatory PLP SSDs) would hit it head-on. The elegance of CephFS snapshot *access* (row above) thus gets a counterweight — the snapshot *feature* itself is more fragile on CephFS than on ZFS.

Of Ceph's wins, only **two actually concern this project — K8s RWX PVs and native S3** (see §7, §14). I accepted RPO 0 as unnecessary (≤ 1 min is fine), and auto-recovery plus scaling target large symmetric clusters, not the planned node 1 + node 2 + arbiter setup.

---

## 1. Starting point: why question Ceph at all

The trigger was the idea of **building just one node for now** and scaling later (RAM and HDD prices high in 2026, DDR4 ECC EOL). That exposed a fundamental conflict:

- **"A 1-node Ceph cluster" is a contradiction in terms.** Ceph derives its value from distribution and self-healing *across nodes*; on a single node (`size=1`) you pay its full complexity (MON/MGR/OSD, ~4 GB RAM per OSD, tuning) and get nothing ZFS wouldn't give you more simply — the properties Ceph exists for vanish on one node.
- **ZFS, by contrast, is single-node by design** and scales out via replication → it fits phasing 1 → 2 → 3 nodes with no intermediate step.

That turned the question "how to phase Ceph" into **"do you need Ceph at all, or is it over-engineering for your context?"**

## 2. My original objections to ZFS and how they held up

| # | Objection | Verdict | Resolution |
|---|-----------|---------|------------|
| 1 | ZFS requires equally sized disks (wastes space otherwise) | 🟡 true **within a vdev**, not across the pool | Growth within a generation = same size; a generational jump (bigger disks) = **a new vdev**. RAIDZ Expansion (OpenZFS 2.3, 2025) adds disks one at a time. |
| 2 | ZFS was always "very slow" for me | ❌ not a property of ZFS | My old test ran on an **SMR disk with a nearly full pool** = worst case (§2.2). Bulk workloads on CMR with enough RAM are fast. |
| 3 | ZFS can't shrink (only expand) | 🟡 true for the **pool/RAIDZ vdev**, **not for ZVOLs** | Shrinking a RAIDZ vdev: no; shrinking a **ZVOL** (block device): yes (§6). Two different operations! |
| 4 | (current server) silent corruption is detected but never repaired | ✅ a real gap | `dm-integrity` (current stack) or ZFS natively (§3). |
| 5 | Browsing snapshots = a separate mount for each one (back then: "lots of mounted devices") | ✅ **still true today** | The design never changed: `.zfs/snapshot/<x>` = automount, N snapshots = N mounts; the only news is auto-unmount after 5 min (`zfs_expire_snapshot`). Work around it with `zfs diff`/`clone`/`send` (§2.5). |
| 6 | Kernel panic when mounting many snapshots | ✅ **real; upstream fix only 12/2025** | A long lineage (#13131, #13327), latest incarnation #17659 (hit Proxmox too); fix PR #17943 is in master, still missing from 2.3.x LTS as of 8/2026 → mitigations in §2.5. |

### 2.1 Mixed-size disks

- **Within a RAIDZ vdev:** smallest disk wins, larger ones get truncated → waste. True.
- **Across the pool:** a pool is a set of vdevs; `vdev1 = 5× 30 TB` plus a later `vdev2 = 5× 60 TB` is fine. "Bigger disks in a few years" is solved by a new vdev.
- **RAIDZ Expansion (2.3, Jan 2025):** adds a single disk to an existing RAIDZ vdev online. Caveat: old data keeps the **old data:parity ratio** until rewritten (capacity grows incrementally); it changes neither the RAID level nor ashift. It covers exactly the "grow 1+2 → 2+2 → 3+2" plan (= RAIDZ2 with a growing number of data units).

**The capacity cost of incremental growth (worked example).** If you add disks one at a time whenever the pool hits ~80 % full, each "layer" of data keeps the parity ratio it was written with — and you don't get the full efficiency of the final width until you rewrite the data. Model: RAIDZ2 growing from 4 to 7 disks of 32 TB each (80 % fill = 80 % of raw, adding at the threshold):

| Phase | Disks | Ratio | Data added | Raw used |
|---|---|---|---|---|
| Start | 4 | 2:2 (50 %) | 51.2 TB | 102.4 TB |
| +5th disk | 5 | 3:2 (60 %) | +15.4 TB | 128 TB |
| +6th disk | 6 | 4:2 (67 %) | +17.1 TB | 153.6 TB |
| +7th disk | 7 | 5:2 (71 %) | +18.3 TB | 179.2 TB |
| **Total** | 7 | mix ~57 % | **~102 TB** | 179.2 TB |

Comparison at 7 disks and 80 % fill (224 TB raw):

| Configuration | Stores |
|---|---|
| RAIDZ2 incremental (this pattern) | **~102 TB** |
| RAIDZ2 clean 7-disk / after a rewrite (all 5:2) | ~128 TB |
| Ceph `size=3` | ~60 TB |

The caveat costs you **~26 TB (~20 %)** against a clean array, but you still lead Ceph `size=3` by **~42 TB** — the caveat shrinks ZFS's lead, it doesn't cancel it. The loss is **not permanent**: one `zfs send -R` (rewrite) unifies everything at 5:2 → ~128 TB, defragmenting along the way while preserving snapshots. A large share of the loss comes from **starting at 4 disks** (2:2 = 50 %, the worst ratio); starting at 6+ disks roughly halves it. The numbers are theoretical (excluding ZFS padding/metadata overhead of a few %), the ratios hold.

### 2.2 "Slowness" — the causes

- **SMR (shingled) disks:** resilver benchmark **CMR 14.5 h vs SMR 9.5 days (16×)**; SMR random I/O is "utterly terrible", and the resilver's CoW walk makes it worse. SMR does not belong in RAID/NAS — it would sink Btrfs and Ceph too.
- **A full pool** (CoW): above ~80 % fill, fragmentation grows (ZFS has no *free-space* defragmentation — "block pointer rewrite" has been undelivered since 2015; `zfs rewrite` rewrites file data but allocates from the same free space, §19), large-block performance drops.
- **RAIDZ = the IOPS of a single disk** for random workloads (one vdev). For sequential bulk (media, photos, backups) it is fast.
- **Mitigations:** CMR disks, enough RAM for ARC, a SLOG for sync writes, pool < 80 %, and a **separate SSD/NVMe pool for VMs** (random) isolated from the HDD bulk pool.

### 2.3 Shrink — pool vs ZVOL (the key distinction)

Do not conflate two different operations:
- **Shrinking the pool / a RAIDZ vdev** (removing a physical disk): ❌ **not possible.** `zpool remove` handles only mirror/stripe/cache/log/special vdevs, **not RAIDZ**.
- **Shrinking a ZVOL** (a logical block device inside the pool): ✅ **possible** (§6). The pool stays, the ZVOL shrinks.

### 2.4 Silent corruption — see §3.

### 2.5 The snapshot layer on Linux: one mount per snapshot, and a panic bug (added 2026-08-01)

Both of my historical experiences (objections 5 and 6) turned out to be confirmed — the first as a design that never changed, the second as a long lineage of real bugs whose fix only landed recently.

**The mechanics (unchanged to this day):** `.zfs/snapshot/<name>` is an automount trigger — entering the directory mounts that snapshot as a separate filesystem with its own entry in the mount table. Searching through 200 snapshots = 200 mounts. The only news since my old experience is automatic unmounting of idle snapshots (`zfs_expire_snapshot`, default 300 s) — which brings a problem of its own (mass expiry of hundreds of mounts at once; systemd additionally re-parses mountinfo on every change).

**The panic bug (verified 2026-08-01):**

- History: [#13131](https://github.com/openzfs/zfs/issues/13131) "Kernel Panic and DoS on massive amounts of snapshot mount/umount" (2022, OpenZFS 2.1.2, reproduced via Samba + many snapshots), [#13327](https://github.com/openzfs/zfs/issues/13327) (processes stuck in the kernel, rising load).
- Latest incarnation: [#17659](https://github.com/openzfs/zfs/issues/17659) (8/2025) — `VERIFY(avl_find(...)) failed / PANIC at avl.c:625:avl_add()` in `zfsctl_snapshot_mount` ← `zpl_snapdir_automount`; Debian 13 / OpenZFS 2.3.2, and reported in-thread on **Proxmox VE 9 (OpenZFS 2.3.4)** with `snapdir=visible` and ~57 snapshots — the panic was triggered by any `ls`/`find`/`stat` over `.zfs/snapshot`. The trigger: a concurrent automount of the same snapshot (typically two mount namespaces — a systemd unit, a container). Technically not a classic kernel panic but an `spl_panic`/VERIFY assert — the thread sleeps forever, everything else touching ZFS ends up in D state, the machine slowly dies, and only a hard reboot helps.
- **The fix:** [PR #17943](https://github.com/openzfs/zfs/pull/17943) (a per-entry mutex) — **merged to master on 8 Dec 2025**. Per the changelogs, though, it has not reached the 2.3.x LTS line (checked 2.3.6–2.3.8) as of 8/2026 → on distributions shipping 2.3.x (including Proxmox VE 9), the mitigations still apply.
- Related: [#18073](https://github.com/openzfs/zfs/issues/18073) (12/2025) — a deadlock between a concurrent `zfs recv` and `du` over the receiving filesystem's `.zfs/snapshot` (`z_teardown_lock`); fix #18415 shipped in the 5/2026 releases. Relevant for `send`/`recv` DR: don't browse `.zfs` on the receiving side during replication windows.

**Mitigations:**

1. Keep `snapdir=hidden` (the default) — `.zfs` stays out of readdir; the panic scenarios required `visible` or targeted access.
2. Read history via `zfs diff` (changes with no mount), `zfs clone` (one specific snapshot) or an explicit `mount -t zfs pool/ds@snap` — not a recursive `find` across `.zfs/snapshot`.
3. No mount namespaces over `.zfs` (containers, systemd `BindReadOnlyPaths`, chroot) — the exact trigger of #17659.
4. Don't browse `.zfs` on the replication target while a receive is running (#18073).

**Compared to the alternatives:** a Btrfs snapshot = a subvolume inside an already-mounted FS, no mounts (caveat: each subvolume has its own `st_dev` → `find -xdev`/`du -x`/`rsync -x`/`tar --one-file-system` stop at the boundary). CephFS = a `.snap` directory in every directory, no mounts, recursive — the most elegant; RBD is the worst of the three (snap → map/clone → mount, manually, crash-consistent only with `fsfreeze`). **For a "grep across the whole snapshot history" workflow, ZFS is the clumsiest and historically riskiest of the three** — it works, but only with discipline.

**Impact on the verdict:** the core use case (bulk reads/writes, `send`/`recv` DR, Proxmox replication, PBS backups) never touches the automount layer and the mitigations are trivial — so this alone does not flip the verdict. It is, however, the first confirmed row where CephFS and the incumbent Btrfs stack genuinely beat ZFS — it enters the decision (§14) as a consciously carried risk with the mitigations above.

### 2.6 OpenZFS on Linux vs the "original" ZFS — parity and integration differences (added 2026-08-01)

Feature parity is complete today — since the codebase merge (OpenZFS 2.0, 2020), Linux is the de facto reference implementation and FreeBSD 13+ runs the same code; native encryption was even born in ZFS-on-Linux (0.8, 2019). The differences that remain are OS-integration ones:

- **NFSv4 ACLs are not enforceable on Linux** — the Linux VFS cannot handle them, so in practice you run POSIX ACLs (`acltype=posixacl`); `acltype=nfsv4` is a FreeBSD thing ([#4966](https://github.com/openzfs/zfs/issues/4966), WIP [PR #13186](https://github.com/openzfs/zfs/pull/13186)). The one genuine functional gap. For this project (home Samba/NFS), POSIX ACLs are enough.
- **The kernel module lives outside mainline (CDDL vs GPL)** — on plain Debian that means DKMS and the "kernel without a module" upgrade risk; **it disappears on Proxmox** (PVE ships the kernel and ZFS together, tested).
- **The ARC lives outside the page cache** → set `zfs_arc_max` manually (otherwise double caching and a memory tug-of-war under pressure).
- **Boot environments** are not built in (FreeBSD has `bectl`; on Linux you bolt on `zfsbootmenu`/`zectl`) — irrelevant for PVE.
- **Native encryption — two caveats independent of the OS:** it does not encrypt pool metadata (dataset and snapshot names, structure, sizes and timestamps stay readable), and it is the least battle-hardened part of the codebase — send/recv of encrypted datasets carried a years-long history of corruption bugs (the main issue #12014 from 2021 was closed only in 2025; fixes headed for 2.2.8/2.3.3, §15). → This reinforces the **LUKS + Tang** choice from §12 (encrypts everything including metadata); test any `send --raw` backups by restoring them.

## 3. Silent corruption: dm-integrity vs native ZFS

The main pain of my current server (`mdraid + dm-crypt/LUKS + LVM + Btrfs`): silent corruption (platter, drive firmware, controller, cabling) is **detected by Btrfs** (checksum → `EIO`) but **never repaired by mdraid** — Btrfs cannot see the parity (it sits below it), and mdraid has no per-block checksums, so it doesn't know which disk is lying.

**There are two fixes, and both require rebuilding the array:**

1. **`dm-integrity` under mdraid** (or LVM RAID with `--raidintegrity y`): gives every sector a checksum → corruption comes back as a **read error instead of bad data** → RAID6 recomputes from parity and rewrites. It turns "silent" corruption into "loud" corruption, which RAID can handle. Cost: ~10–30 % write overhead, +1 layer.
2. **ZFS** has this built in natively (checksum + redundancy + self-heal in one layer, 75 % efficiency with RAIDZ2).

**Consequence for the decision:** since fixing corruption **requires rebuilding the array either way**, the "at least I don't have to change anything" argument collapses. The rebuild happens regardless — the only question is onto what (ZFS vs mdadm/LVM+integrity).

## 4. HA: it's about node count, not the engine

- **1 node = no HA with anything** (not even single-node Ceph — there is nothing to fail over to). HA is a question of **"1 node vs 2 nodes", not "ZFS vs Ceph".**
- **ZFS HA** (Proxmox VE):
  - **Proxmox ZFS replication (`pvesr`) + HA manager** — async replica of the ZVOLs (minimum interval 1 min) + automatic VM restart on another node from the latest replica. Soft HA (RPO ~1 min, failover = restart, not live migration). Sufficient for media/photos/documents/ordinary services.
  - **DRBD-over-ZFS** — a synchronous replica of a local pair (RPO 0), hard HA for databases. More complex.
- **No real-time HA across a WAN with any engine** — synchronous writes over residential WAN links (latency, jitter, outages) are a showstopper. The geo tier is always async DR only.

### 4.1 "Orchestrated failover" (what that means)

Ceph is **shared storage** → data reachable from every node → failover = a trivial VM restart elsewhere. ZFS is **shared-nothing** → the replica on the second node is a separate, lagging, read-only pool. Failover therefore needs a layer above the storage (an orchestrator) performing: **detection → fencing → replica promotion → service start → redirection → (after recovery) failback**. The Proxmox HA manager does this **automatically** (orchestrated ≠ manual); the price is RPO > 0, a restart instead of live migration, and fencing/failback complexity.

### 4.2 The "node 1 burns down" scenario (solved without Ceph)

The target setup, all on ZFS:

| Element | Role |
|---|---|
| **node 1** (big) | VM primary + bulk media/photos/documents |
| **node 2** (small/cheap, e.g. N100) | compute + replicas of the VM ZVOLs = failover target (**no bulk storage** — carries only the VMs) |
| **RPi5 qdevice** (~free) | quorum arbiter (2 nodes without an arbiter = losing 1 kills the majority → HA won't fire) |
| **DR server** (geo, second site — the former main machine) | async DR for bulk + VMs (PBS, §5) |

Node 1 burns down → the VMs come up on node 2 (RPO ~1 min), bulk data is restored from geo DR. Node 2 stays cheap because it carries only VMs, not the storage.

### 4.3 How much HA that is — numbers, failover and failback

| Metric | Value |
|---|---|
| **RPO** (data loss) | ≤ 1 min (`pvesr` interval, 1 min minimum) |
| **RTO** (VM downtime) | ~2–5 min (detection + fencing + VM boot) |
| Failover | automatic |
| Type | crash-consistent (the VM boots as if after a power cut) |

**Failover mechanics** (node 1 dies): `pvesr` continuously replicates the VM ZVOLs to node 2 (a copy ≤ 1 min old) → corosync detects the outage → **watchdog fencing** (a node without quorum resets itself in ~60 s, the split-brain guard) → the HA manager starts the VM on node 2 from the latest replica → the VM boots. Requires: quorum (node 1 + node 2 + the **RPi qdevice**), fencing enabled (softdog), a replication job per VM.

**Failback** (returning to a repaired node 1) is *planned*, hence **zero-downtime**: set up replication node 2 → node 1 (fills it back up), then `qm migrate <vmid> node1 --online` → a **live migration** transfers only the final delta + RAM state → the VM switches over without interruption. The only unavailability window in the whole cycle is the original failover.

**How much HA to enable** — sort the VMs into three buckets:
- "Must always run" (Plex, *arr, Nextcloud, DNS…) → HA + 1-min replication.
- "Longer downtime is fine" → no HA, just PBS backups.
- "Not even a minute of loss" (DBs with active transactions) → add **app-level replication** (Patroni etc.) rather than building Ceph for it.

## 5. Deduplication: don't solve it in storage — PBS does it

- **ZFS legacy dedup** = the infamous ~5 GB RAM/TB (unrealistic for 150 TiB). **Fast Dedup (OpenZFS 2.3, 2025)** softened that (DDT log/prefetch/prune/quota, DDT on a special vdev), but it is still slower than no dedup. The consensus: "dedup is good now — and you still shouldn't use it."
- **On real data, dedup yields almost nothing:** media and photos are already compressed (ratio ~1.0), documents are a tiny volume.
- **Where dedup does pay off (VM images, backups) → PBS** (Proxmox Backup Server) handles it at the application layer: chunk-based, content-defined dedup across all backups, RAM-light (runs at backup time, not inline on the storage). Plus incremental backups (dirty-bitmap), compression, client-side encryption, retention, verify (integrity), remote sync.
- **Ceph** has no production inline dedup (RADOS inline dedup is experimental; only RGW object dedup for S3 is mature).

→ **Live data on ZFS (compression lz4/zstd only), backups in PBS (with dedup). Do not enable storage-level dedup.** PBS will run on the DR server = geo DR + versioned backups (replacing the originally considered Ceph mirroring — simpler and more faithful).

## 6. ZVOL: the block device (RBD equivalent) + resize

- **A ZVOL** = a block device carved out of the pool (`zfs create -V`), the local analogue of a Ceph RBD. It inherits snapshots, clones, compression, checksums, `send`/`recv`, encryption, thin provisioning. Proxmox uses it for VM disks.
- Difference vs RBD: a ZVOL is **local** (an RBD is **distributed/shared**). Networked via iSCSI/NVMe-oF, replicated between nodes asynchronously.
- **Expand:** `zfs set volsize=` (larger) + resize the FS inside — online, trivial.
- **Shrink:** `zfs set volsize=` (smaller) **works**, but truncates data beyond the boundary **without warning** (no safety net like RBD's `--allow-shrink`) → you must **shrink the FS inside first**. The procedure is identical to `lvreduce` over LVM+Btrfs (FS shrink first, then the volume). Safety net: `zfs snapshot` before the shrink (instant rollback).
- **Snapshots + resize:** resizing works with existing snapshots (no need to delete them). With a shrink, though, snapshots pin the old blocks → **pool space is not reclaimed while pre-shrink snapshots exist**. Recommended flow: keep the snapshot → shrink → verify → only then delete the snapshot (both safety and space reclaim).

## 7. Kubernetes and S3 — the last real reasons for Ceph

The project is considering Kubernetes. This is where Ceph holds a genuine edge that must not be waved away:

- **K8s persistent volumes:**
  - **Ceph RBD (ceph-csi)** — mature dynamic provisioning, **distributed PVs** (a pod failing over to another node sees the same PV), RWX via CephFS.
  - **ZFS (openebs `zfs-localpv`)** — dynamic provisioning of ZVOLs, but **local PVs** (the pod runs where the pool is; failover only with the data replicated elsewhere). RWO, no distributed RWX.
  - **The deciding question:** do the K8s workloads need **RWX / distributed PVs** (multiple pods sharing one volume, failover independent of placement), or is **RWO local-PV + replication/failover** enough? For most self-hosted services (Plex, photos, documents, DBs with their own replication), RWO suffices. RWX is only needed for a filesystem shared between replicas.
- **K8s control-plane HA** (etcd 3-node quorum) is **a separate layer independent of the storage engine** — solved by 3 (even small) control-plane nodes, not by the ZFS/Ceph choice.
- **S3/RGW object storage:** Ceph has it natively; ZFS doesn't (only MinIO/Garage on top of the filesystem). The question: does anything on the cluster require the S3 API?

## 8. Why ZFS wins for this context (summary)

1. **Full value from one node + no migration trap** (§10) — fits the phased plan.
2. **An order of magnitude less RAM** — in my plan a ZFS node comes out at ~64 GB vs a full Ceph node at 96–128 GB. A direct saving amid the DDR4 crunch.
3. **Simplicity** — `zpool`/`zfs`, a single layer, operable "at 3 a.m." by a solo admin with no on-call.
4. **`send`/`recv`** — the cleanest incremental, versioned, bit-exact DR (to the DR server).
5. **Capacity efficiency** — RAIDZ2 75 % vs Ceph `size=3` 33 %; at 150 TiB that is tens of drives of difference.
6. **Cheaper networking** — Ceph practically mandates 10 GbE; single-node ZFS needs no cluster network at all, and replication runs fine over 1 GbE.
7. **Integrity, snapshots, compression, encryption, ZVOLs** — all in one layer.

## 9. Where Ceph wins (honestly)

- **Distributed/shared storage** — RBD/CephFS reachable from every node → zero-downtime live VM migration + K8s RWX PVs. ZFS is shared-nothing.
- **RPO=0 HA within the cluster** (ZFS replication is async, ~1 min). Note: across a WAN you don't get RPO=0 even with Ceph.
- **Scaling to 10+ nodes / petabytes / many parallel clients** — Ceph is built for it.
- **Native S3/RGW.**
- **Automatic self-healing across nodes.**

Of these, only **distributed K8s PVs** and **S3** are actually relevant to this project (§7) — and even those would work only within a single site anyway, not across the WAN.

## 10. The ZFS→Ceph migration trap (and how to avoid it)

ZFS and Ceph are incompatible worlds — there is no conversion, only copying (losing snapshots). Enrolling node 1 (ZFS) into a Ceph cluster means reformatting it → draining it onto nodes 2+3 → running `size=2` for the duration of the window (tolerating 1 failure).

**The trap exists only if Ceph is the destination.** Avoidance:
1. **Stay on ZFS the whole way** (1 node → +2 nodes + replication) → node 1 is never wiped, no trap.
2. If Ceph is a must → **don't start with ZFS**; build 2 Ceph nodes from day one.
3. The reduced-redundancy window during a migration is covered by the **geo backup** (DR server + cloud) — even if a disk died inside the window, a DR copy exists.

## 11. Recommended target architecture (the ZFS path)

- **OS/hypervisor:** Proxmox VE 9 (built on OpenZFS 2.3 → RAIDZ Expansion and Fast Dedup), **root-on-ZFS mirror** (replaces the old mdadm OS mirror; OS snapshots / boot environments for free).
- **Storage:** ZFS — RAIDZ2 for the HDD bulk (media/photos/documents), a mirror/RAIDZ SSD pool for the VM ZVOLs (random workload isolated from bulk).
- **HA (once node 2 exists):** Proxmox ZFS replication + HA manager + the RPi5 qdevice arbiter (§4.2).
- **Backups/DR:** PBS on the DR server (§5) — versioned, deduplicated, remote sync; cloud for the most valuable subset (photos/documents) within its hard monthly transfer cap.
- **Phasing:** node 1 (ZFS, full value immediately) → + a small node 2 + the arbiter (HA, nothing gets wiped) → node 3 as finances allow.

## 12. At-rest encryption

**Threat model:** theft of a whole node → data unreadable. The key requirement: **the unlocker must not be obtainable from the stolen machine**.

**The two-key model** (both LUKS and ZFS native encryption): the *master key* encrypts the data and lives on disk, but **itself encrypted**; it is unlocked by a *wrapping key*, which must not be on the disk. `/etc/crypttab` is just configuration (what to unlock with what), not a key.

**Where to keep the wrapping key** (against node theft):

| Method | Fit |
|---|---|
| TPM alone | ❌ travels with the board → a stolen node yields the key (TPM+PIN helps, but that's interaction) |
| Passphrase + dropbear SSH | ✅ key in your head, remote unlock after reboot; the cost: manual |
| **Tang/Clevis (network-bound)** | ⭐ unlocks only inside the home network (Tang on the RPi arbiter); a carried-off node = locked; at home, auto-boot |

**Recommendation: LUKS + Clevis/Tang** (Tang on the RPi5 arbiter), ideally with an encrypted root too. On Proxmox (Debian) these are standard packages (`clevis-luks`, `clevis-initramfs`, `tang`), but the setup is manual (the installer doesn't offer root encryption). DR/backups are encrypted **client-side by PBS** independently. Alternative: ZFS native encryption + a passphrase (supports `send --raw` = encrypted replicas with no key on the DR side), but Tang unlock with it is DIY — and it also leaves pool metadata unencrypted (dataset/snapshot names, sizes, timestamps) and is the least battle-hardened part of ZFS: the years-long history of send/recv corruption bugs on encrypted datasets was closed only in 2025 (§2.6, §15). One more point for LUKS.

**The trap:** a keyfile on an **unencrypted root** = the attacker reads it off the stolen disk → the encryption is pointless. Hence an external unlocker (Tang/passphrase), not a keyfile on a plaintext disk.

**The boundary:** this protects a *powered-off* stolen machine; a running/unlocked one is a different problem. **The BMC/IPMI is its own attack surface** — out of scope for this analysis.

## 13. Fill ratio and real usable capacity

The fill ceiling is similar for both (~80 %), so **by itself it doesn't move the needle much** — the main capacity difference is replication overhead (see "Comparison at a glance", the capacity-efficiency row).

- **ZFS:** ~80 % for performance/fragmentation reasons (CoW); beyond that it slows down (no data loss), beyond ~95 % badly. Practice (45Drives) puts the real ceiling closer to ~90 %; above 90 %, though, there is even a reported case of `zpool import` failing after a power loss ([#18041](https://github.com/openzfs/zfs/issues/18041)) — the 80 % ceiling thus has a healthy margin.
- **Ceph:** thresholds `nearfull` 85 %, `backfillfull` 90 %, `full` 95 % (writes stop). Plus a **self-heal reserve** — an OSD/node failure must fit onto the survivors → practically ~75–80 %, **less on few nodes** (losing 1 of 3 = 33 % must fit somewhere). ZFS needs no such reserve.

**Actually usable out of every 100 TB of purchased disks** (usable × 80 % fill):

| Configuration | Real data |
|---|---|
| ZFS RAIDZ2 (75 % × 80 %) | ~60 TB |
| Ceph `size=3` (33 % × 80 %) | ~27 TB |

At a 150 TiB target the gap is tens of drives and easily €4,000+ in hardware — but it comes from replication, not from the fill ratio.

## 14. The decision

The four questions that opened up during the analysis resolved as follows:

1. **K8s persistent volumes — RWX not needed.** The planned applications (Zabbix, Grafana, Loki, Prometheus) do HA at the application layer (multiple replicas + a shared DB / Patroni), not via shared storage → `zfs-localpv` (RWO) + Proxmox HA is enough.
2. **S3/RGW — not needed.** The only candidate reason (backups via Kopia) doesn't require S3 — Kopia handles filesystem/SFTP repositories; the nice-to-have is covered by MinIO on top of ZFS.
3. **HA model — accepted.** Orchestrated failover (RPO ≤ 1 min, RTO ~2–5 min, failback via live migration; §4.3) is sufficient for this profile.
4. **The snapshot automount layer — a consciously carried risk (added 2026-08-01).** A confirmed weakness of ZFS on Linux (§2.5): one mount per snapshot plus a history of panics; the upstream fix (12/2025) is still outside the 2.3.x LTS line. Carried with mitigations (`snapdir=hidden`, `zfs diff`/clone, no mount namespaces over `.zfs`) — the core use case never touches it.

**→ Verdict: ZFS on Proxmox VE.** On 1–3 nodes, Ceph would add nothing this project would actually use — while charging a permanent tax in RAM, networking and operational complexity. Point 4 is the one place where CephFS objectively leads — for this profile it does not outweigh the rest; the reliability profiles (§15) further support the verdict (this design routes around ZFS's risks, while Ceph's would hit it head-on). On a large symmetric cluster with many clients the verdict could easily flip — which is exactly why this whole analysis is anchored to the context up top.

## 15. Data-loss risk: reliability profiles (added 2026-08-01)

This second addendum draws on an independent deep-research reliability analysis of ZFS/Btrfs/Ceph on Debian/Ubuntu ([the artifact](https://claude.ai/public/artifacts/49c04b36-c45d-4b73-8652-c79f39de5ad5), 319 sources) and a follow-up discussion; the load-bearing claims were verified against primary sources on 2026-08-01. The takeaway for this context: **the risk profiles favour ZFS** — this design systematically routes around ZFS's weaknesses, while Ceph's would hit it head-on.

**ZFS — the most mature integrity track record; risks concentrated and avoidable:**

**Documented (Open)ZFS-on-Linux corruption bugs — a timeline** (added 2026-08-06):

| When | What | Layer | Fix |
|---|---|---|---|
| 2016 | **hole_birth** — silent corruption of incremental `zfs send` streams: the receiver reports no error, yet destination ≠ source (old data arrives instead of zeros; [#4996](https://github.com/openzfs/zfs/issues/4996), [Debian #830824](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=830824)) | send/recv | ZoL 0.6.5.8 / 0.7.0-rc1: the sender ignores the faulty hole_birth metadata by default ([FAQ](https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ%20hole%20birth.html)) |
| 3–4/2018 | A regression in 0.7.7: "disappearing" files (lost hard links) + false ENOSPC when copying directories with many files; per [The Register](https://www.theregister.com/2018/04/10/zfs_on_linux_data_loss_fixed/) no data was actually lost | ZPL/VFS | emergency 0.7.8 within 3 days (revert) |
| 2021→2025 | Native encryption × send/recv ([#12014](https://github.com/openzfs/zfs/issues/12014) and friends): permanent errors on encrypted snapshots during backups | encryption | closed only in 2025 (PR #17340; fixes in 2.2.8/2.3.3) |
| 11/2023 | **Dirty dnode** ([#15526](https://github.com/openzfs/zfs/issues/15526)): silent corruption during copies (trigger: coreutils 9.x + block cloning), **latent since ~2013**, invisible to scrub | core (dnode check) | 2.2.2 / 2.1.14 (12/2023) |

- **Lessons:** two of the four bugs were **silent** — checksums cannot catch a bug sitting above them → backups + verifying replicas (scrub on the target, test restores); hole_birth is exactly the send/recv DR scenario. The risks sit in the send paths and freshly shipped features, never in the core RAIDZ/mirror write path → run conservative versions, let novelties mature (block cloning is off by default anyway).
- **Encryption: the LUKS + Tang path (§12) is untouched by the whole encryption saga.** Debian 13 / Ubuntu 24.04 / PVE 9 all ship versions carrying every fix above.
- Fill levels: see §13 — practice tolerates ~90 %, so the 80 % ceiling has a healthy margin (incl. [#18041](https://github.com/openzfs/zfs/issues/18041)).

**Ceph — the core is mature at massive scale, but the risks sit exactly where this project was headed:**

- **CephFS snapshots + multi-MDS = historically the most fragile area.** The official best practice as late as the Mimic era (2018) read "[use a single active MDS and do not use snapshots](https://docs.ceph.com/en/mimic/cephfs/best-practices/)"; both features are supported today, yet operational incidents span versions: [#53192](https://tracker.ceph.com/issues/53192) (11/2021, Nautilus) — with snapshots enabled, `rm -rf` dropped from ~400 to ~25 unlinks/s (`SnapRealm::split_at`, 100 % CPU on the MDS), the degradation persisted even after deleting all snapshots, and the full fix only arrived with v20.2.0 (Tentacle, 11/2025) — **four years**; [Silvenga, 7/2024](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/) — MDS journal corruption during snapshot trimming after a mass delete (multi-MDS), MDS crashes and a risky recovery; [Rook #15273](https://github.com/rook/rook/issues/15273) (1/2025, Squid 19.2.0) — group snapshots of ~20 PVCs → latency spikes and the MDS "behind on trims". For a project with snapshots as a central workflow this is a direct hit — and unlike the ZFS automount bug (§2.5, which has a merged fix), this is behaviour of the MDS architecture, not a single bug with a patch.
**Documented Ceph corruption bugs — a timeline** (added 2026-08-02, tabulated 2026-08-06):

| When | What | Layer | Fix |
|---|---|---|---|
| 11/2019 | The fastbmap allocator in 14.2.3/14.2.4 — RocksDB checksum errors; hit **only OSDs with a separate DB/WAL device** (the recommended "block.db on SSD" layout; [advisory](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/X6TNSDQK5DVKO6XFJW3DMJAJV63PLDYM/)) | BlueStore | expedited 14.2.5 |
| 5/2020 | `bluefs_preextend_wal_files` → RocksDB WAL corruption ([#45613](https://tracker.ceph.com/issues/45613)) | BlueFS | option disabled, fixed in 15.2.x |
| 9/2020 | *Edinburgh:* MDS journal corruption after a network reconfiguration → cascading MDS crashes, a week of disaster recovery on a ~40TB FS; data recovered ([postmortem](https://blogs.ed.ac.uk/mhagdorn/2020/09/09/anatomy-of-a-cephfs-disaster/)) | CephFS/MDS | — (operational disaster) |
| 2021 | BlueFS mishandling **>4GB writes from RocksDB** → potential corruption ([openSUSE advisory 5/2021](https://osv.dev/vulnerability/openSUSE-SU-2021:0672-1)) | BlueFS | 14.2.22 / 15.2.13 |
| 10–12/2021 | The Pacific **OMAP conversion** bug on upgrades: `quick_fix/repair` → malformed OMAP keys ([#53062](https://tracker.ceph.com/issues/53062), an "IMPORTANT NOTICE" advisory) | upgrade path | 16.2.7 (12/2021) |
| 7/2024 | *Silvenga:* MDS journal corruption during snapshot trimming after a mass delete; backups saved the day ([postmortem](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/)) | CephFS/MDS | — (operational disaster) |

The pattern: **the RADOS core has no documented case of losing data by itself on healthy hardware** — the pure corruption bugs cluster in 2019–2021 (BlueStore maturing: the BlueFS↔RocksDB interaction, upgrade conversions); what is fresh (2024) is the MDS/CephFS metadata layer. Yet every one of these bugs demanded a timely reaction to advisories (follow ceph-users, don't ride day-one point releases) = one more line item of the solo admin's operational tax. Compared with the ZFS table above: ZFS has fewer, but two of them were silent.
- **Most real-world Ceph data loss = operator error, not bugs:** `min_size=1` (the most common), `size=2`, touching OSDs during degradation/backfill, copy-pasted `--yes-i-really-mean-it` commands, ignored HEALTH_WARN. The risk grows for a **solo admin without a daily Ceph routine** — exactly this profile (§8).
- **Enterprise SSDs with PLP are practically mandatory** (BlueStore does frequent fsyncs; consumer SSDs without PLP = collapsing sync writes + corruption risk on power loss). The planned build uses consumer NVMe → the Ceph path would mean pricier drives. ZFS needs PLP only for a SLOG, which is not planned.
- **Debian packages have a documented history of trouble** (Reef 18.2.0 could not even be built for bookworm; dashboard PyO3 crashes) → upstream recommends cephadm in containers = one more operational layer.

**Btrfs (the incumbent stack):** the RAID5/6 write hole is officially "not for production" even in 2026 ([RAID56 status](https://btrfs.readthedocs.io/en/latest/btrfs-man5.html)) — the incumbent stack (Btrfs on LV **on top of mdadm RAID6**, not Btrfs RAID5/6) correctly avoids it; the single/RAID1/10 profiles are mature (Meta on millions of machines, default on Fedora/openSUSE desktop). The flagship ENOSPC/balance annoyance remains.

**Hardware, across the board:** ECC is recommended, not mandatory — the "scrub of death" is a myth (Ahrens: ZFS without ECC is no riskier than any other FS without ECC; priority: backups → checksumming FS → UPS → ECC). The real risk for all three: drives that lie about flushes, and QLC SSDs under write load.

## 16. Growing one disk at a time: EC 2+2 vs RAIDZ2 (added 2026-08-13)

This third addendum comes from a clarification that changes the brief: **I am not buying the target configuration in one go — I start with 3–4 disks and grow one disk at a time.** Growing by a single disk is classically Ceph territory and classically a RAIDZ weakness, so it was worth checking whether that flips the verdict. It did not — but along the way I had to **correct two of my own claims from earlier revisions of this document**, both in Ceph's favour.

### 16.1 How many disks a two-failure tolerance actually needs

`m` is directly the number of OSDs you may lose: *"The value of M defines how many OSDs can be lost simultaneously without losing any data."* Tolerating two therefore means `m=2`, spread over `k+m` failure domains.

| layout | disks | usable capacity | efficiency |
|---|---:|---:|---:|
| Ceph replica3 | 3 | 1 disk | 33 % |
| Ceph replica3 | 4 | 1.33 disks | 33 % |
| **Ceph EC 2+2** | **4** | **2 disks** | **50 %** |
| **ZFS RAIDZ2** | **4** | **2 disks** | **50 %** |
| ZFS RAIDZ1 | 3 | 2 disks | 67 %, but survives only 1 |

A `k=1, m=2` profile (3 disks, tolerance 2) is mathematically degenerate — Reed-Solomon with a single data chunk produces copies, i.e. exactly what `size=3` does at the same 33 % efficiency. Whether Ceph rejects it outright I did not verify (the documentation states no minimum for `k`), but it has no reason to exist.

**The practical consequence:** 3 disks in RAIDZ1 and 4 in RAIDZ2 both yield two disks' worth of usable capacity, because both have two data disks. The fourth disk therefore buys not capacity but an entire level of resilience. At today's ~30 TB capacities, where a resilver runs for days while reading every remaining disk, RAIDZ1 is a bad trade.

### 16.2 "Survives 2" means something different for each engine

⚠️ **A correction to an earlier claim.** Previous revisions of this document placed ZFS and Ceph failure tolerance side by side as equivalent. They are not.

Ceph defines `min_size` as *"the minimum number of active replicas (or shards) required for PGs to be active and thus for I/O operations to proceed"*, and a PG that is not `active` serves no requests. For EC the documentation recommends *"min_size be K+1 or greater to prevent loss of writes and loss of data"*.

| state | ZFS RAIDZ2 (4 disks) | Ceph EC 2+2 (4 OSDs) | Ceph replica3 (4 OSDs) |
|---|---|---|---|
| 1 disk lost | reads and writes | reads and writes | reads and writes |
| 2 disks lost | **reads and writes** | data survives, but `min_size=3` → **I/O stalls** | some PGs drop to 1 copy, below `min_size=2` → **part of the data unavailable** |
| self-heal without a replacement disk | no (needs a hot spare) | no (4 shards need 4 OSDs) | yes, if the data fits on the surviving OSDs |

With replication, **self-heal headroom** further eats into nominal capacity: for the cluster to restore three copies after losing a disk, the data must fit on the remaining OSDs. On four disks that caps you at roughly one disk's worth of user data rather than a third of four — and less still once the `nearfull`/`full` ratios are applied. On three disks, three copies cannot be placed on two survivors at all.

### 16.3 RAIDZ expansion exists — and that retires one of the historical objections

**Proxmox VE 9.0 shipped with ZFS 2.3.3**, and RAIDZ expansion is officially supported there. A disk is added with `zpool attach`, preceded by `zpool upgrade` to activate the `raidz_expansion` feature flag. Resilience is preserved: *"Fault tolerance is unchanged — a RAID-Z2 stays a RAID-Z2."*

**Earlier revisions of this document assumed a RAIDZ vdev is fixed-width forever.** That held through ZFS 2.2; from 2.3 it no longer does.

Two caveats:

- **Old data keeps its original ratio:** *"blocks written before the expansion keep their original data-to-parity ratio, just spread over more disks. Only newly written blocks use the wider ratio."*
- **The open issue [OpenZFS #17784](https://github.com/openzfs/zfs/issues/17784)** reports that after expanding a RAIDZ2 from 4 to 5 disks the physical allocation is roughly double the logical data (20.7 TiB for 10.3 TiB) with over 10 TiB of expected capacity missing; the related PR #18324 has not closed it. The reporter is running a 2.4.99 development build rather than 2.3.x LTS, so **I have not verified whether the version in Proxmox is affected**. Before relying on expansion for a production pool, rehearse it in a VM with virtual disks — it takes minutes.

Expansion reads and rewrites all allocated space, so expanding sooner costs less than expanding later. A rough order-of-magnitude estimate at ~200 MB/s sequential: 10 TB occupied ≈ 14 hours, 30 TB ≈ 1.7 days, 60 TB ≈ 3.5 days (not measured).

### 16.4 An existing pool's EC profile cannot be changed

The Ceph documentation is categorical: *"the profile cannot be modified after the pool is created"* and *"There is no way to alter the profile of a pool after the pool has been created."* Moving from 2+2 to 3+2 therefore means **a new pool**. The standard copy tool does not work on EC pools either — `rados cppool` returns `error copying pool testpool => newpool: (95) Operation not supported`. The `--force` flag on `ceph osd erasure-code-profile set` merely overwrites the named profile (and demands `--yes-i-really-mean-it`); it does not reach back into existing pools.

Two mitigations:

1. **CephFS supports multiple data pools.** New data can be directed into a wider pool through a layout (`setfattr -n ceph.dir.layout -v pool=ec42 /ceph/logs`) without copying the old data; both pools share the same OSDs.
2. **Pool Migration is in the works.** The developer documentation describes a proposal targeting the **Umbrella** release, intended to *"change the erasure code profile (and in particular the choice of K and M) non-disruptively"* as well as *"Converting between replica and erasure coded pools"*, with no outage. It is a **proposal, not a feature**: the first release will require an empty target pool, will offer no cancel or suspend, and will require every client and daemon to be upgraded.

### 16.5 Correction: on growth, capacity is a draw

⚠️ **The second and more consequential correction.** It is tempting to say "EC is locked at 50 % while RAIDZ2 grows to 67 %". That is unfair twice over: CephFS lets you add a second pool with a wider profile (§16.4), so "locked forever" is false — and, more importantly, **RAIDZ expansion has exactly the property I would be holding against Ceph**: old data keeps its original ratio, so the pool as a whole does not become more efficient under ZFS either.

The efficiency of **freshly written** data is identical for both:

| disks | RAIDZ2 width | equivalent EC profile | efficiency |
|---:|---|---|---:|
| 4 | 2+2 | EC 2+2 | 50 % |
| 5 | 3+2 | EC 3+2 | 60 % |
| 6 | 4+2 | EC 4+2 | 67 % |

The difference is therefore **operational, not capacity-related**: with ZFS it is one `zpool attach` and new data is automatically written wider; with Ceph it is creating another pool and managing per-directory layouts, with several pools of differing geometry side by side.

### 16.6 Small-write performance — this is the real difference

Ceph's developer documentation describes the `parity-delta-write` technique for `m=2` at a cost of *"just 3 read and 3 writes to perform an overwrite of less than one chunk"* — six disk operations, three of them reads on the critical path, against three parallel writes for replication. ZFS RAIDZ is copy-on-write: a small write becomes a new, narrower stripe with its own parity, so **no read-modify-write happens at all**.

Measurements confirm that `k=2` is the worst end of the spectrum. The official Fast EC benchmark in Tentacle shows that *"wider erasure codes performance improves as K increases"*, and even with Fast EC on NVMe, three-way replication retains roughly **50 % better performance** than EC on a 70/30 mix at 16K. Operational experience on spinning disks (ceph-users): *"EC pools have high throughput but low IOP/s compared with replicated pools"*, having tested `k` from 5 to 12 and concluding *"Best results in decreasing order: k=8, k=6. All other choices were poor."*

On versions: **Proxmox VE 9.2 ships Ceph Tentacle 20.2.1 as the default**, so Fast EC is available — but the benchmark gains come from a 16K `stripe_unit` rather than the 4K default, i.e. from configuration, not from the upgrade alone.

### 16.7 Conclusion for this scenario

For **a single node with four disks, growing one disk at a time**, **ZFS RAIDZ2** wins — not on capacity, which is a draw (§16.5), but because in this configuration Ceph pays the small-write overhead (§16.6), stalls on a second failure (§16.2), requires a replicated metadata pool on SSD plus enterprise SSDs with PLP (§15), and adds multi-pool administration. Its one genuine counterweight is self-healing without a replacement disk, once there are more OSDs than `k+m`.

**What would flip this:** growing by **nodes** instead of disks — then Ceph is the right choice from the start and saves a later migration (§10); or a workload dominated by **large sequential writes** (media archive, backups) rather than VM disks, where the read-modify-write overhead disappears.

## 17. Update (2026-08-14): the snapshot automount layer was rewritten — and is in no release yet

§2.5 named PR [#17943](https://github.com/openzfs/zfs/pull/17943) as the fix and recorded that it had not reached the 2.3.x LTS line. Both statements still hold. What has changed is the *shape* of the fix, and it is worth recording precisely, because the headline reads better than the practical situation.

**#17943 fixed one race, not the lineage.** Its title is exact: "Fix snapshot automount race causing AVL tree panic" (merged 2025-12-08). The two issues §2.5 treats as the lineage — [#13131](https://github.com/openzfs/zfs/issues/13131) "Kernel Panic and DoS on massive amounts of snapshot mount/umount" (2022) and [#13327](https://github.com/openzfs/zfs/issues/13327) "processes stuck in kernel forever" — stayed open through it.

**They were closed on 2026-08-06, by a rewrite.** The maintainer closed both with "Resolved by [#18847](https://github.com/openzfs/zfs/pull/18847)" — *"Linux: rewrite snapshot automount facility"*. Not a patch: commit `e8e30769` landed on master **2026-06-18**, and through July a batch of new ZTS tests followed it (snapdir detach under ongoing access, multiple automounts via multiple base-dataset mounts, shutdown behaviour when the automount is moved or bind-mounted elsewhere). Two neighbouring issues also closed: [#17659](https://github.com/openzfs/zfs/issues/17659), the systemd-triggered panic that hit Proxmox, on 2025-12-12, and [#18073](https://github.com/openzfs/zfs/issues/18073), the `recv` × `du` deadlock, on 2026-04-08.

**And none of it is released.** Verified 2026-08-14:

| | |
|---|---|
| Rewrite on master | 2026-06-18 (`e8e30769`) |
| Latest releases | 2.4.3, 2.3.8, 2.2.10 — all **2026-06-12** |
| Newest commit on `zfs-2.3-release` | 2026-06-08 |

The rewrite landed **six days after** the most recent releases and has not been backported to the 2.3.x LTS branch. On anything installable today — including what Proxmox ships — the behaviour is the pre-rewrite behaviour.

**What this changes for the verdict: nothing.** §2.5's conclusion stands unaltered: this is the weakest part of ZFS on Linux, and the mitigations are cheap (`snapdir=hidden` is the default; browse history with `zfs diff` or a clone rather than `.zfs`; do not walk `.zfs` on a receiving side during `recv`). Those mitigations remain the operative advice, not a stopgap until the next update.

**What it changes for the outlook: the class looks closed upstream.** A rewrite plus a purpose-built test suite is a stronger signal than a race fix — the maintainers treated it as a design problem rather than a bug. The thing to watch is the first release containing `e8e30769` (2.4.4 or later) and whether it is ever backported to 2.3.x. Until one of those happens, the comparison table's "snapshot-layer stability" row stands exactly as published.

*§2.5 is left as it was written. This is ageing, not an error: the section was accurate on 2026-08-01 and the world moved under it, which is what a dated snapshot is for.*

## 18. The objections keeping the decision open (added 2026-08-14)

This document reached a verdict in §14. A year on, I have not acted on it — and that gap is itself information. A comparison that records only the conclusion, and not the reasons its own author never adopted it, is less useful than one that admits both. What follows are the eight objections that keep me looking at Ceph, each with what it is actually worth and whether Ceph is the thing that answers it.

The uncomfortable summary is that **Ceph answers one of the eight**, makes two of them worse, and does not touch three.

| # | Objection | Does it hold? | Does Ceph answer it? |
|---|---|---|---|
| 1 | Serious bugs in OpenZFS on Linux | Yes — and Ceph has its own (§15) | ❌ no |
| 2 | Per-disk LUKS just to be able to send snapshots | The premise is inverted | ❌ Ceph is also per-OSD dm-crypt |
| 3 | Cannot add a larger disk later | **Yes — the strongest point** | 🟡 yes, but see #8 |
| 4 | No defragmentation | Yes | ❌ BlueStore fragments too |
| 5 | Dedup RAM you never get back | Largely yes | ❌ Ceph dedup is experimental |
| 6 | Slow reads and writes vs Btrfs/ext4 | Often — and the causes are checkable | ❌❌ **far worse at this scale** |
| 7 | ZFS corrupted file ownership years ago | Cannot assess | — |
| 8 | Cannot grow from 1-node EC to 3-node replication | **Yes, and worse than stated** | ❌ this is a cost *of* Ceph |

### 18.1 Bugs (objection 1)

True, and §15 documents them. But §15 documents Ceph's timeline symmetrically, and the useful question is not "does it have bugs" but "where do the bugs sit relative to how I will use it". ZFS's cluster in the `send` paths and in freshly shipped features; Ceph's in CephFS snapshots with multi-MDS, in non-PLP SSDs, and — §15's own conclusion — in **operator error**, which is the dominant real-world cause of loss and scales with the number of moving parts. Ceph has five-plus daemons to ZFS's one command set. §17 is a data point the other way: the automount panic class was closed by a *rewrite* with a purpose-built test suite, not a patch.

### 18.2 Encryption (objection 2)

The premise is inverted, and this is worth stating plainly because it was my own reasoning. **LUKS was never the price of replication.** ZFS native encryption supports `zfs send -w` (raw), which ships ciphertext and needs no key on the destination. §12 chose LUKS for unrelated reasons: native encryption leaves pool metadata readable (dataset and snapshot names, sizes, timestamps), and its `send`/`recv` path carried a corruption history whose main issue ([#12014](https://github.com/openzfs/zfs/issues/12014)) closed only on 2025-05-19.

And Ceph does not escape per-device encryption: *"Logical volumes can be encrypted using `dmcrypt` by specifying the `--dmcrypt` flag when creating OSDs."* Every OSD is a dm-crypt volume. The difference is that `ceph-volume` orchestrates it instead of Clevis — a real ergonomic gain, but not a change of model.

### 18.3 Larger disks (objection 3)

True, and the strongest of the eight. Inside a RAIDZ vdev, usable capacity per disk is set by the smallest member, so a 40 TB disk bought into a pool of 30 TB disks contributes 30 TB. Two ZFS answers exist before reaching for Ceph. **Mirror vdevs**: add and replace two at a time, and with `autoexpand=on` replacing both halves of one mirror yields the space immediately — at 50 % efficiency instead of RAIDZ2's 75 %, which at a 150 TiB target is a large number of extra drives. **Whole vdevs**: `raidz2` of 4×30 TB and a later `raidz2` of 4×40 TB coexist in one pool, at the cost of buying four at a time.

Ceph handles this natively through CRUSH weights, and that is a genuine, durable advantage. It is also the advantage that §18.9 mostly cancels.

### 18.4 Defragmentation (objection 4)

Partly true, and weaker than I stated — see the correction in §19. `zfs rewrite` has existed since May 2025 and ships in 2.3.x and 2.4.x; defragmenting files and rebalancing after a vdev addition are its stated purposes, so neither needs a second pool any more. What survives of the objection is that it needs contiguous free space to write into, so its effectiveness falls away on the near-full pool that motivates using it; there a `send`/`recv` rebuild remains the reliable cure. But the comparison table already rates **Ceph 🟡 on this row as well**: BlueStore fragments too. The ✅ belongs to Btrfs. And on the near-full case specifically, the failure modes differ in Ceph's disfavour: a full ZFS pool becomes slow, whereas a Ceph pool reaching its full ratio **stops accepting writes**. The real answer to "the array will often be very full" is not an engine but buying capacity earlier.

### 18.5 Dedup (objection 5)

Largely true. OpenZFS 2.3's Fast Dedup added `zpool ddtprune`, which *"prunes older unique entries from the dedup table"* — but it does not remove the DDT, so "I will never get that RAM back" survives as a fair description. The resolution is that this is a feature not to switch on: on bulk media and photos deduplication gains almost nothing, which is the conclusion of the sources §7 already cites. Ceph's own deduplication is documented as experimental. This objection is about a button that should stay unpressed in either system.

### 18.6 Performance (objection 6)

Often true, and it is the objection doing the most emotional work — which is exactly why it deserves the most precise treatment. ZFS is genuinely slower than ext4 on many workloads, and the causes are specific and checkable rather than mysterious. The dominant one is geometry: **a single RAIDZ vdev delivers the random IOPS of roughly one disk**, so an eight-disk RAIDZ2 is not eight disks' worth of IOPS; mirrors scale with vdev count. After that come `recordsize` mismatched to the workload, synchronous writes without a SLOG, an ARC starved by VMs, and `atime=on` turning reads into writes. A `special` vdev with `special_small_blocks` takes metadata IOPS off the RAIDZ vdev entirely and is often the single largest available win — at the price that it is pool storage, not cache: **lose it unmirrored and the pool is gone**.

But this objection points away from Ceph, not toward it. On one to three nodes with a single client, Ceph is far slower than ZFS and not remotely comparable to ext4: every write crosses the network and must commit durably on each replica before the client is acknowledged, which is precisely why PLP SSDs and 10 GbE are near-mandatory (§15). Ceph's speed comes from parallelism across many OSDs and many clients — none of which this profile has.

### 18.7 The ownership incident (objection 7)

Recorded, not explained away. Years-old, no details retained, so it cannot be diagnosed now. Plausible candidates from what is documented: the 0.7.7→0.7.8 "disappearing files" regression (§15), the NFSv4-versus-POSIX-ACL mismatch on Linux (§2.6, [#4966](https://github.com/openzfs/zfs/issues/4966)), or idmapping on `recv`. As evidence about a specific bug it is unusable; as a datapoint about trust it is real, and trust is not a rounding error for a solo admin at 3 a.m.

### 18.8 One node with EC to three nodes with replication (objection 8)

True, and materially worse than the objection states. The erasure code profile is immutable: *"the profile cannot be modified after the pool is created. If you find that you need an erasure-coded pool with a profile different than the one you have created, you must create a new pool … all objects from the wrongly configured pool must be moved to the newly created pool."* And the topology requirement is hard: *"Most erasure-coded pool deployments require at least `k+m` CRUSH failure domains, which in most cases means racks or hosts. There are operational advantages to planning EC profiles and cluster topology so that there are at least `k+m+1` failure domains."*

EC 2+2 therefore needs **four** failure domains, five recommended. Three nodes with host-level EC 2+2 is not slow or inefficient — it is not possible.

| Step | What you actually get |
|---|---|
| 1 node, EC 2+2, failure domain = OSD | Works, but **no tolerance of losing the machine** |
| → 3 nodes, EC 2+2 at host level | ❌ **not possible**, the fourth domain is missing |
| → 3 nodes, EC 2+1 | 67 % efficiency, **one parity only** (weaker than RAIDZ2), new pool + full data move |
| → 3 nodes, replication size=3 | 33 % efficiency, new pool + full data move |
| → EC 2+2 at host level | Only from **4–5 nodes** |

Every route off single-node EC is a new pool and a full migration, with the free space to hold both at once or the patience to do it in batches. This is §10's ZFS→Ceph migration trap reproduced **inside Ceph**, where changing engines cannot avoid it.

And it largely cancels objection 3. If changing topology means a full pool-to-pool migration anyway, that is exactly the moment at which a ZFS pool could be rebuilt with new vdev geometry. What survives of Ceph's advantage is the narrower claim that it handles heterogeneous disks better **between** topology changes.

### 18.9 What this actually selects for

Read the list for what it prefers rather than what it rejects: defragmentation, familiar performance, growth one disk at a time, no dedup trap, no per-disk encryption surprise. That describes **the incumbent `mdadm + LUKS + LVM + Btrfs` stack**, whose single documented weakness in the comparison table is one row — *detects silent corruption, cannot repair it* — and that row is closable by adding `dm-integrity` beneath it.

So the objections do not point at Ceph. They point at tuned ZFS or at staying put.

### 18.10 Decision rule, written before the measurement (2026-08-14)

Objection 6 is the only one of the eight that is cheap to test, and it carries the others emotionally. It therefore gets a rule written now, before any number exists.

**The test.** Build the layout that would actually be deployed — which forces the mirrors-versus-RAIDZ2 decision, since that is what sets IOPS — on the real hardware, with a mirrored `special` vdev if small files matter, `recordsize` matched to the workload, and ARC not starved. Measure against Btrfs on the same disks with the same workload mix: bulk sequential read and write for media, and a metadata-heavy directory walk for the photo and document tree.

**The gates**, in order of authority:

1. **Absolute.** ZFS must saturate the network link on sequential transfer and complete the photo-tree walk fast enough to be unremarkable in use. This gate decides, because the question is not whether ZFS matches Btrfs but whether it is fast enough for what the array is for.
2. **Relative.** Tuned ZFS lands within 25 % of Btrfs on sequential throughput and within 2× on the metadata walk.

**What each outcome means.** Fail gate 1 → the §14 verdict falls honestly, and the replacement is the incumbent stack plus `dm-integrity`, **not** Ceph, because §18.6 and §18.8 rule Ceph out on the same evidence. Pass gate 1 but fail gate 2 → acceptable; record the gap and move on. Pass both → objections 1, 4, 5, 6 and 7 lose most of their force at once, and only 3 and 8 remain — and those two largely cancel each other.

**What would make Ceph right after all:** growth by single heterogeneous disks over many years **and** acceptance of 10 GbE, PLP SSDs, four-plus nodes for meaningful EC, and materially worse single-client latency. That is a coherent trade. It is not a fix for anything on this list.

## 19. Correction (2026-08-14): `zfs rewrite` exists, and four claims were wrong

Four claims in this document said ZFS has no tool for rewriting existing data. That was wrong when written, not merely stale: the `zfs rewrite` subcommand landed upstream in **May 2025** ([#17246](https://github.com/openzfs/zfs/pull/17246)) and is present in both the **2.3.x and 2.4.x** release lines — that is, in what you would actually install today.

**Corrected in place:** the "Defrag / cleanup" and "Recompressing existing data" rows of the comparison table, the full-pool bullet in §2.4, and §18.4's assessment of objection 4. This section records what changed and why, per the repository's rule that an error is fixed in place *and* logged.

**What the tool does.** *"Rewrite blocks of specified file as is without modification at a new location and possibly with new properties, as if they were atomically read and written back."* It takes `-r` to recurse, `-x` to stay within one filesystem, and `-o`/`-l` for a byte range. It closes the recompression gap outright: changing `compression` or `recordsize` and then running `zfs rewrite -r` applies the new property to existing data, which previously required a `send`/`recv` cycle through another pool.

**Defragmentation is a stated purpose, not a side effect.** The submitting PR is explicit about what users had been asking for: *"an ability to re-balance pool after vdev addition, de-fragment randomly written files, change some properties for already written files"*. Rebalancing after `zpool add` matters here in particular — §16 and objection 3 (§18.3) both end at "add a wider vdev of larger disks", after which existing data stays on the old vdevs until something rewrites it. `zfs rewrite -P -r` is that something.

It also runs under load — *"protected by normal range locks, it can be done under any other load"* — is faster than a read-plus-write because *"it does not require data copying to user-space"*, and *"does not affect file's modification time or other properties"*, so mtime-based backup tools do not see the whole pool as changed.

**Where the objection survives is narrower than first stated** (this paragraph was corrected the same day, after the original overstated it). Rewriting a file frees its scattered blocks and allocates a contiguous run, so free-space fragmentation — what the `FRAG` column measures, *"As the amount of space allocated increases, it becomes more difficult to locate free space"* — does improve as a consequence. But the mechanism needs somewhere contiguous to write the new copy **before** the old blocks are freed, and that is exactly what a near-full, heavily fragmented pool does not have; there the new copy lands fragmented too and little is gained. Snapshots make it worse still (see below). So `zfs rewrite` works best on the pool that needs it least, and a `send`/`recv` rebuild into a fresh pool remains the cure that always works. It is also still not "block pointer rewrite": the pool cannot relocate blocks on its own, this is driven per file from userspace.

**Two flags that matter more than they look.**

`-P` — *"Perform physical rewrite, preserving logical birth time of blocks."* Without it, *"rewritten blocks update their logical birth time, meaning they will be included in incremental `zfs send` streams as modified data."* A naive defragmentation therefore makes the next incremental send ship the entire dataset — which, on the metered residential WAN of the sibling `storage-replication` analysis, is a month's transfer budget spent on moving data that did not change. `-P` makes the rewrite invisible to replication. It did not exist when §2.4 was written.

`-C` and `-S` skip blocks shared with clones and snapshots, and the reason is the thing to remember: *"rewriting these blocks would create separate copies and increase space usage."* On a pool that is too full — the exact situation that motivates defragmenting — rewriting snapshotted data makes the problem **worse**, because the snapshot pins the old block and the rewrite adds a new one. The order of operations is therefore: prune snapshots first, rewrite second.

**And the trade that has no tool.** When a rebuild is unavoidable, `zfs send -R` preserves every snapshot — but preserving them replays the original write history, which reproduces much of the fragmentation. Sending a single snapshot without `-R` yields a maximally compact result and discards the history. Fragmentation *is* the imprint of that history, so the two cannot both be kept.

**Net effect on objection 4 (§18.4):** it drops from "no tool exists" to "a tool exists, and it stops helping precisely when the pool is too full — which is when you reach for it". It is weaker than stated, but it does not disappear — and neither does the conclusion that Ceph is not the answer to it, since BlueStore fragments as well and a full Ceph pool stops accepting writes where a full ZFS pool merely slows down.

## References

External sources (verified July 2026; snapshot/ACL addenda verified 2026-08-01):

- RAIDZ Expansion: [The Register](https://www.theregister.com/2025/01/23/openzfs_23_raid_expansion/), [FreeBSD Foundation](https://freebsdfoundation.org/blog/raid-z-expansion-feature-for-zfs/), [the parity-ratio caveat](https://louwrentius.com/zfs-raidz-expansion-is-awesome-but-has-a-small-caveat.html)
- Device removal / shrink limits: [OpenZFS zpool-remove](https://openzfs.github.io/openzfs-docs/man/v2.0/8/zpool-remove.8.html), [cr0x.net](https://cr0x.net/en/zfs-vdev-removal-limits/)
- SMR: [xda-developers](https://www.xda-developers.com/smr-hdds-are-fine-for-your-nas-until-you-try-to-resilver/), [vermaden](https://vermaden.wordpress.com/2024/05/29/zfs-resilver-smr-drives/), [OpenZFS #18132](https://github.com/openzfs/zfs/issues/18132)
- Fragmentation / defrag: [OpenZFS #3582](https://github.com/openzfs/zfs/issues/3582), [zfs-rewrite(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-rewrite.8.html), [#17246 — introduce `zfs rewrite`](https://github.com/openzfs/zfs/pull/17246), [zpoolprops(7) — the `fragmentation` property](https://openzfs.github.io/openzfs-docs/man/master/7/zpoolprops.7.html) (verified 2026-08-14)
- Fast Dedup: [Klara Systems](https://klarasystems.com/articles/introducing-openzfs-fast-dedup/), [despairlabs](https://despairlabs.com/blog/posts/2024-10-27-openzfs-dedup-is-good-dont-use-it/)
- Ceph dedup: [Ceph docs — Deduplication (experimental)](https://docs.ceph.com/en/latest/dev/deduplication/), [RGW Object Dedup](https://docs.ceph.com/en/latest/radosgw/s3_objects_dedup/)
- ZVOL shrink: [FreeBSD Forums](https://forums.freebsd.org/threads/zfs-set-volsize-data-loss.55854/), [TrueNAS](https://www.truenas.com/community/threads/shrink-zvol-of-vm.100519/)
- Snapshot automount / panics: [#13131](https://github.com/openzfs/zfs/issues/13131), [#13327](https://github.com/openzfs/zfs/issues/13327), [#17659](https://github.com/openzfs/zfs/issues/17659), [fix PR #17943](https://github.com/openzfs/zfs/pull/17943) (master 12/2025; not in 2.3.6–2.3.8), [#18073](https://github.com/openzfs/zfs/issues/18073) (recv × du deadlock), [module parameters — `zfs_expire_snapshot`](https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Module%20Parameters.html)
- NFSv4 ACLs on Linux: [#4966](https://github.com/openzfs/zfs/issues/4966), [WIP PR #13186](https://github.com/openzfs/zfs/pull/13186)
- CephFS snapshots: [Ceph docs — CephFS Snapshots](https://docs.ceph.com/en/latest/dev/cephfs-snapshots/)
- Reliability profiles (2026-08-01): [deep-research artifact](https://claude.ai/public/artifacts/49c04b36-c45d-4b73-8652-c79f39de5ad5), [#15526 dirty dnode](https://github.com/openzfs/zfs/issues/15526), [#12014 encryption send/recv](https://github.com/openzfs/zfs/issues/12014), [#18041 import >90 % after power loss](https://github.com/openzfs/zfs/issues/18041), [tracker #53192 — MDS latency with snapshots (2021→fixed 2025)](https://tracker.ceph.com/issues/53192), [Silvenga — CephFS metadata recovery (7/2024)](https://silvenga.com/posts/notes-on-cephfs-metadata-recovery/), [Rook #15273 — MDS trims with snapshots (1/2025)](https://github.com/rook/rook/issues/15273), [CephFS best practices (Mimic)](https://docs.ceph.com/en/mimic/cephfs/best-practices/), [Btrfs RAID56 status](https://btrfs.readthedocs.io/en/latest/btrfs-man5.html)
- Ceph corruption bugs — timeline (verified 2026-08-02): [the 14.2.3/14.2.4 advisory (11/2019)](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/X6TNSDQK5DVKO6XFJW3DMJAJV63PLDYM/), [#45613 — bluefs_preextend_wal_files (5/2020)](https://tracker.ceph.com/issues/45613), [BlueFS >4GB writes (openSUSE advisory 5/2021)](https://osv.dev/vulnerability/openSUSE-SU-2021:0672-1), [#53062 — Pacific OMAP + IMPORTANT NOTICE (10/2021)](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/U4QX4E32BR5IOICOUW4FR7E56YEET3CN/), [Edinburgh — Anatomy of a CephFS disaster (9/2020)](https://blogs.ed.ac.uk/mhagdorn/2020/09/09/anatomy-of-a-cephfs-disaster/)
- ZFS corruption bugs — timeline (verified 2026-08-06): [hole_birth #4996](https://github.com/openzfs/zfs/issues/4996), [Debian #830824](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=830824), [FAQ hole birth](https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ%20hole%20birth.html), [0.7.7→0.7.8 "disappearing files" (The Register, 4/2018)](https://www.theregister.com/2018/04/10/zfs_on_linux_data_loss_fixed/)
- Growing one disk at a time, EC vs RAIDZ2 (verified 2026-08-13): [Ceph — Erasure code](https://docs.ceph.com/en/latest/rados/operations/erasure-code/), [Ceph — Erasure code profiles](https://docs.ceph.com/en/latest/rados/operations/erasure-code-profile/), [Ceph — Pools (min_size)](https://docs.ceph.com/en/latest/rados/operations/pools/), [Ceph — Create a CephFS](https://docs.ceph.com/en/latest/cephfs/createfs/), [Ceph dev — Erasure coding enhancements](https://docs.ceph.com/en/latest/dev/osd_internals/erasure_coding/enhancements/), [Ceph dev — Design of Pool Migration](https://docs.ceph.com/en/latest/dev/pool-migration-design/), [Ceph.io — Tentacle Fast EC performance](https://ceph.io/en/news/blog/2025/tentacle-fastec-performance-updates/), [ceph-users — best practice for Erasure Coding](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/QCEFF2DEGV2J6IQAIK3MKVBSX5BCQHAM/), [OpenZFS — RAIDZ](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/RAIDZ.html), [OpenZFS #17784](https://github.com/openzfs/zfs/issues/17784), [Proxmox — raidz extension for PVE 9 / ZFS 2.3.3](https://lore.proxmox.com/pve-devel/20250717133753.408101-1-d.herzig@proxmox.com/), [Proxmox — Ceph Squid to Tentacle](https://pve.proxmox.com/wiki/Ceph_Squid_to_Tentacle)

---

*Researched and written in collaboration with Claude (Anthropic); facts verified against the sources above as of July 2026, with the addenda (snapshot layer, reliability profiles, corruption-bug timelines) verified 1–6 August 2026 the growth addendum verified 13 August 2026, and the automount update, the objections section and the `zfs rewrite` correction 14 August 2026. This document is a dated snapshot and is not continuously updated.*

*© 2026 Petr Kratochvíl · Licensed under [CC BY 4.0](../LICENSE)*
