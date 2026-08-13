# Incremental replication between two storage clusters: ZFS send/recv vs Ceph mirroring

- **Verdict:** ⭐ **`zfs send -i`** (orchestrated by zrepl *or* syncoid — §12) — valid for the context described below
- **Facts verified:** 2026-08-13 (OpenZFS master man pages, docs.ceph.com latest, Proxmox wiki, zrepl docs, sanoid/syncoid README + issue tracker, btrfs-progs docs + btrbk issue tracker, Proxmox Backup Server docs, Red Hat/IBM Ceph docs)
- **Corrections:** §13 (2026-08-13) — the "min. 3 nodes" ratings and the §1 disqualifying criterion were wrong; a single-node Ceph cluster is supported. The verdict survives on different reasoning.
- **Adversarial verify:** run 2026-08-13 against the verdict. It did **not** overturn the mechanism (§2–§8 held), but it **did overturn the orchestrator pick**: the differentiator originally claimed for zrepl over syncoid rested on sanoid issues #304/#528, which have been closed since 2019/2020. §12 was rewritten to state the orchestration as an open, close call rather than a settled one.
- **Open tags:** none. The `[VERIFY]` on sparse handling in `cephfs-mirror` was resolved 2026-08-13 out of the source (§5).
- **Process note:** the decision rules (§1) were written on 2026-08-13 **after** the mechanism research in §2–§7 but **before** choosing the orchestration and the verdict. This is therefore not full pre-registration in the sense of `AGENTS.md`; stated here so the rules do not read as stronger than they are.
- **Language:** 🇬🇧 English (canonical) · 🇨🇿 [Čeština — original](README.cs.md)
- **Author:** Petr Kratochvíl — [krato.cz](https://krato.cz)

## Context: the profile this decision was made for

This follows on from [ZFS vs Ceph](../zfs-vs-ceph/README.md), where the verdict was ZFS on Proxmox VE. This document answers the question that fell out of it next: **how do changes get from one site to the other.** The profile:

- **Two sites**, each with its own cluster (not one cluster stretched across both) — ordinary apartments joined by a residential WAN link.
- **A hard monthly cap on transferred data** — the size of an increment is not an optimisation but a budget line. The ability to know a transfer's size **in advance** has value of its own.
- **Solo admin, no on-call.** Replication has to recover from a link outage by itself, because nobody is going to restart a transfer at 3 a.m.
- **Workload:** bulk media/photos/documents (~150 TiB target) plus a handful of VM disks. That is many files with a low change rate, plus a few large continuously-rewritten images.
- **RPO:** losing ~1 minute to ~1 hour is acceptable. Synchronous replication across a WAN is not required, and nothing on offer provides it.
- **The second site is a DR target, not an active node** — nothing writes to it.

Out of scope: replication to cloud (solved by dedup backup, not replication), synchronous RPO=0, and shared RWX volumes across sites.

## Summary (TL;DR)

1. ⭐ **Recommendation: `zfs send -i`.** It covers files and block devices with one mechanism, ships a block-level delta, resumes an interrupted transfer via a resume token, and is the only option here that can state the **exact transfer size up front** (`zfs send -nvP`, §3). With a hard data cap that is decisive (§1, §12).
2. **ZFS does not distinguish files from blocks, Ceph does — and that is the single most important structural difference** (§2). A dataset and a ZVOL are the same object to `send`/`recv`; CephFS and RBD, by contrast, have two unrelated daemons with **granularity that differs by orders of magnitude**.
3. **`cephfs-mirror` is not send/receive, it is rsync with better change detection** (§5). It copies files into the live remote directory and only then creates a snapshot there. A changed file is transferred **in full**, and hardlinks decompose into separate copies. For large continuously-modified files that is disqualifying.
4. **Atomicity is the most-overlooked difference** (§6). `zfs recv` is transactional — the destination dataset is a valid past state at every moment. With `cephfs-mirror` the consistent point is **only a completed snapshot**; the live directory during a sync is not one. That belongs in the DR runbook, not in a footnote.
5. **RBD is a full peer to ZFS at the block level** (§7), but journal mode pays with roughly doubled write latency and snapshot mode means RPO = the schedule interval. Also: `rbd-mirror` runs on the **secondary** (pull), `cephfs-mirror` on the **primary** (push) — easy to get backwards when designing firewalls.
6. **Block-level delta transfer has a real counter-case** (§8): it ships changed *blocks*, not changed *content*. In-place rewrites, recompression, or a database rewriting pages dirty an enormous number of blocks and the increment can be several times larger than rsync's. Marginal for this workload, but an accepted trade-off rather than a non-existent risk.
7. **A replica you have not scrubbed is not a replica** (§10). Two of the four historical ZFS bugs in the `send` path were silent ([zfs-vs-ceph §15](../zfs-vs-ceph/README.md)) — checksums cannot catch them, because they sit above the layer that computes them.
8. **Renaming a large directory is where the mechanisms diverge most** (§14). On ZFS it is metadata — a 100 TiB tree renamed inside a dataset moves kilobytes. `cephfs-mirror` has no rename detection: it deletes the old tree on the remote and re-copies the new one in full, which makes it **worse than the rsync baseline**, since rsync at least has `--link-dest` and partial fuzzy matching to fall back on.
9. **Btrfs is the closest rival and loses on exactly two rows** (§15): no resume for an interrupted transfer, and no way to size one up front. Both are decision rules here, so it is out — but it is the only mechanism that encodes a rename *as* a rename, and the incumbent DR box runs it today. Practical consequence: **that box should be rebuilt on ZFS**, because replication does not cross engines (§8).
10. **PBS is complementary, not competing** (§16). It wins outright on three rows — client-side AES-256-GCM so the far end never holds a key, built-in verify jobs (the discipline §10 asks for), and content-addressed chunks that make renames and in-place rewrites free. It loses the verdict because its destination is a datastore: recovery means restoring, which for ~150 TiB is days. **Run both** — a `send`/`recv` replica is not a backup, and a PBS datastore is not a failover target.

## Comparison at a glance

Symbols: ✅ strength · 🟡 works with caveats / a compromise · ❌ weakness or missing · — not applicable. Rated **for this context** (two sites, asymmetric residential WAN with a data cap, solo admin, bulk media + a handful of VM disks, a DR target that is never written to) — not in general; on a symmetric DC link with generous bandwidth several rows would come out differently. The first two columns are the two filesystem-level serialisers, the middle two the two Ceph daemons, and the last two are engine-neutral — rsync as the file-copy baseline, and Proxmox Backup Server, which answers a **different question** (point-in-time restore rather than a state you can fail over to) and is included on that understanding (§16).

| Criterion | ZFS `send`/`recv` | Btrfs `send`/`receive` | Ceph RBD mirror | CephFS mirror | rsync / rclone | Proxmox Backup Server |
|---|---|---|---|---|---|---|
| **▸ How the delta is produced** | | | | | | |
| Unit of transfer | ✅ block (`recordsize`/`volblocksize`) | ✅ extent (`WRITE`/`CLONE`) | ✅ object / extent | ❌ **the whole changed file** | 🟡 rolling-checksum delta | ✅ chunk (4 MiB fixed / rolling-hash dynamic) |
| Finds changes without walking the tree | ✅ birth time in the CoW tree | ✅ generation numbers | ✅ object-map + fast-diff | ✅ snapdiff (Reef onwards, §11) | ❌ stat every file | 🟡 VM: dirty bitmap · files: metadata walk |
| Detection cost scales with | ✅ volume of changes | ✅ volume of changes | ✅ object count (from an in-memory map) | 🟡 number of changed files | ❌ **total number of files** | ❌ **data read locally** (metadata mode: file count) |
| Serialises FS state vs copies via POSIX | ✅ FS state (holes, compression, properties) | ✅ FS-aware instruction stream | ✅ blocks (POSIX not involved) | ❌ POSIX copy → **hardlinks decompose** | ❌ POSIX copy | ❌ POSIX read → content-addressed chunks |
| Rename/move of a large tree (§14) | ✅ metadata only (within a dataset) | ✅ explicit `RENAME` command | ✅ invisible — guest-FS metadata | ❌ **delete + full re-copy** | ❌ delete + re-transfer (`--fuzzy` misses directory renames) | ✅ chunks re-referenced, not re-uploaded |
| **▸ Atomicity and consistency** (§6) | | | | | | |
| Destination is always a valid past state | ✅ transactional `recv` | 🟡 prior snapshots untouched; the in-flight subvolume is separate | ✅ delta applies wholly, or rolls back | ❌ live directory is a mix during a sync | ❌ | ✅ completed snapshots are immutable |
| Consistent point after a mid-transfer crash | ✅ last received snapshot | 🟡 last completed (read-only) subvolume; the partial one is left behind | ✅ last mirror snapshot | 🟡 last **completed** snapshot on the remote | ❌ none | ✅ last completed snapshot |
| Resume after a link outage | ✅ resume token (`recv -s`) | ❌ **none — restart from zero** | 🟡 the daemon continues; DIY `export-diff` does not | 🟡 the daemon continues (per file) | 🟡 `--partial` | 🟡 no token, but a retry sends only missing chunks |
| **▸ Link and budget** | | | | | | |
| **Transfer size known in advance** | ✅ `zfs send -nvP` (exact) | ❌ no dry-run option | ✅ `rbd diff --format json` (sum the extents) | ❌ no | ❌ `--dry-run` gives only a list | ❌ no |
| Compression on the wire | ✅ `-c` ships blocks compressed as they sit on disk | ✅ `--compressed-data` (Linux 6.0+) | 🟡 external (ssh `-C`) | 🟡 external | ✅ `-z` | ✅ zstd per chunk, client-side |
| Transfer without a key on the destination | ✅ `send -w` (raw) | ❌ no native encryption | ❌ | ❌ | ❌ | ✅ **client-side AES-256-GCM** |
| Bandwidth limiting | ✅ zrepl / `pv` / `mbuffer` | ✅ `pv` / `mbuffer` | 🟡 daemon configuration | 🟡 daemon configuration | ✅ `--bwlimit` | 🟡 traffic control — but sync jobs need their own `rate-in` (§16) |
| **▸ Operations** | | | | | | |
| Daemon required | ✅ none (or zrepl) | ✅ none (or btrbk) | ❌ `rbd-mirror` | ❌ `cephfs-mirror` | ✅ none | ❌ a PBS instance on both ends |
| Where the daemon runs / direction | ✅ push or pull | ✅ push or pull | 🟡 **secondary** (pull) | 🟡 **primary** (push) | ✅ either | 🟡 sync job: pull or push |
| Bidirectional / failback | 🟡 manual role swap | 🟡 manual role swap | ✅ promote/demote, two-way | ❌ one-way, **single peer** | 🟡 manual | ❌ **restore, not failover** (§16) |
| Min. nodes on the destination | ✅ **1** | ✅ **1** | 🟡 1 supported, not production-grade (§13) | 🟡 1, plus a kernel-client caveat (§13) | ✅ 1 | ✅ **1** |
| **▸ Fit for the workload** | | | | | | |
| Large continuously-modified files (VM, DB) | ✅ | 🟡 files only — no ZVOL equivalent (§15) | ✅ | ❌ transfers the whole file | 🟡 delta yes, but reads the whole file | ✅ dirty bitmap while the VM runs |
| Millions of small files, few changes | ✅ | ✅ | — | ✅ | ❌ the walk dominates the transfer | 🟡 metadata mode avoids re-reading |
| In-place rewrite / recompression (§8) | ❌ ships every dirtied block | ❌ ships every changed extent | ❌ ditto | ✅ ships only changed files | ✅ ships only changed content | ✅ content-addressed — identical content dedups away |
| Writable / RWX destination | ❌ destination must be `readonly` | ❌ received subvolume is read-only | ❌ | ✅ (but should not be) | ✅ | ❌ a datastore; you must restore |
| Subset of a dataset / different layout | ❌ whole dataset | ❌ whole subvolume | ❌ whole image | ✅ per directory | ✅ freely | ✅ freely |
| Transfer between different engines | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ **engine-agnostic** |

**How to read it.** Read the PBS column against §16 first: it is a backup system, so its ❌ on bidirectional failback is a category statement, not a defect — while its ✅ on client-side encryption, engine independence and rename cost are rows where it genuinely beats every replication mechanism here. Btrfs (§15) is the closest thing to ZFS in the table and the sharpest test of the verdict: same class of mechanism, comparable granularity, and the only column that represents a rename *as* a rename. It loses here on two of the four decision rules — no resume and no size estimate — which is precisely the pair that this context turns on. ZFS wins everywhere the question is "how many bytes will move and what happens when the link drops" — block granularity, an exact estimate up front, a transactional receive and a resume token. RBD is its equal at the block level and beats it on one row (native bidirectional failover with promote/demote), but pays with three nodes on the destination side and a mandatory daemon. CephFS mirror wins only where the others cannot compete at all — a shared writable filesystem and replication per directory rather than per whole dataset — and loses on granularity, atomicity and hardlinks. rsync is the last column not because it is bad, but because it is the only one that does what none of the others can: **change the engine, change the layout, take a subset** — and in one scenario (§8) it beats all of them.

## 1. Decision rules (2026-08-13)

Written before choosing a tool and before the verdict (see the process note in the header). The chosen mechanism must satisfy all four:

1. **The data budget is knowable in advance.** There must be a way to learn a transfer's size before starting it, within ~10 %. Without that you cannot run a link with a hard monthly cap, because a single dataset recompression will exhaust it.
2. **A link outage must not mean transferring from zero.** A residential WAN drops; a multi-TiB transfer that restarts from the beginning after an outage never finishes.
3. **The destination must be usable as a DR point at any moment, with no judgement call.** "Go check whether it finished" is not an operation I want to perform during an incident.
4. **One mechanism for both files and VM disks.** Two replication pipelines with two failure sets and two runbooks are, for a solo admin, a bigger risk than anything they save.

**Disqualifying criterion:** anything requiring ≥3 nodes on the destination side is out — the second site starts as a single machine. *(Read after the fact: this rule **did not fire** — a single-node Ceph cluster is supported. See the correction in §13; the rule is left as written rather than rewritten to fit the outcome.)*

## 2. The structural asymmetry: ZFS has one mechanism, Ceph has two

The most useful thing about this question shows up immediately: **the four cases do not decompose into four answers, but into two pairs.**

For ZFS, a *filesystem dataset* and a *ZVOL* are the same object. The replication layer never touches what is inside — it works with the block tree and birth times, not with files. `zfs send` on a dataset holding a million photos and `zfs send` on a ZVOL holding a VM disk is literally the same command with the same flags and the same semantics. "How do I replicate files" and "how do I replicate block devices" **are not two questions** in ZFS.

Ceph is the opposite. CephFS and RBD are two independent products over the same RADOS, with two separate mirroring daemons that share nothing but a name. They differ in direction (push vs pull), in which side runs the daemon, in transfer granularity, in atomicity, and in what happens when they crash. Learning `rbd-mirror` teaches you nothing about `cephfs-mirror`.

This difference is **durable** — it follows from architecture, not from a version. ZFS is one filesystem with one serialisation format; Ceph is a set of services over shared object storage, where each service solves replication at its own layer.

## 3. ZFS `send`/`recv` — how the delta is produced

The basic loop is identical for files and blocks:

```bash
# source
zfs snapshot -r tank/data@2026-08-13          # -r is atomic across the pool
zfs send -w -c -i @2026-08-12 tank/data@2026-08-13 \
  | ssh dr zfs recv -s -F backup/data
```

The delta is not computed by comparison — it falls out of the CoW tree. Every block carries a *birth time* (the transaction group it was created in), so "what changed since snapshot X" is a metadata question, not a content question. Cost is therefore proportional to the **volume of change**, not to the number of files or the size of the dataset. A dataset with ten million files and one changed photo sends that photo and nothing else; rsync would have to walk all of it.

The flags that matter:

- **`-i` vs `-I`** — `-i` sends the delta between two snapshots, `-I` includes all intermediate ones. `-I` preserves the whole retention chain on the destination, which for DR is usually what you want.
- **`-c`** generates a more compact stream by shipping blocks already compressed as they sit on disk. It saves CPU and bandwidth, and the data stays compressed on the receiving side.
- **`-w` / `--raw`** sends data exactly as it exists on disk — for encrypted datasets that means **the destination needs no key**. For unencrypted datasets `-w` is equivalent to `-Lec`.
- **`-s` on receive** saves partially received state instead of discarding it and exposes `receive_resume_token`. Without it an interrupted transfer is thrown away (§6).
- **`-i` also accepts a bookmark.** `zfs bookmark tank/data@old tank/data#old` creates an anchor that survives deleting the source snapshot — you reclaim space on the source without breaking the chain.

Resuming after an outage:

```bash
# destination: zfs get -H -o value receive_resume_token backup/data
# source:      zfs send -t <token> | ssh dr zfs recv -s backup/data
```

And, for decision rule 1, the important part — **the size estimate up front**:

```bash
zfs send -nvP -i @2026-08-12 tank/data@2026-08-13
```

`-n` is a dry run (generates no actual send data), `-P` gives machine-parsable output. You learn the stream size before a single byte leaves the monthly cap. None of the other mechanisms except RBD (§7) can do this.

**Operational traps.** The destination dataset's most recent snapshot must be exactly the one the increment is based on — the man page is explicit: *"the destination file system must already exist, and its most recent snapshot must match the incremental stream's source"*. Hence `readonly=on` on the destination (`zfs recv` still works, user writes do not) and `zfs hold` on the anchor snapshots so a retention script cannot sweep them away. Without that you are looking at a `recv -F` rollback, or worse, a full resend.

## 4. Files vs ZVOL: where the difference actually is

The mechanics are the same; two things differ — and neither is about replication.

**Consistency.** A ZVOL snapshot is crash-consistent: it matches what would be left on disk after a power cut. For a VM disk that is usually enough (a journalled filesystem recovers); for a database inside the VM it is not. An application-consistent snapshot requires quiescing the guest — `qemu-guest-agent` fsfreeze, which on Proxmox is handled by `qm snapshot`. The replication layer knows nothing about this and has no way to.

**Granularity.** `volblocksize` (16K by default in OpenZFS 2.2+) determines how large a block one guest write dirties. A 4 KB write into a ZVOL with a 16K volblocksize means 16 KB in the increment. For datasets `recordsize` does the same thing, but there the size adapts to the file, so the effect is smaller. For VM disks doing random writes this is a 4× multiplier on volume — and against a data cap that is a visible line item.

## 5. CephFS mirroring: rsync with better change detection

```bash
# on the secondary cluster
ceph fs snapshot mirror peer_bootstrap create backup_fs client.mirror_remote site-remote

# on the primary
ceph mgr module enable mirroring
ceph fs snapshot mirror enable cephfs
ceph fs snapshot mirror peer_bootstrap import cephfs <token>
ceph fs snapshot mirror add cephfs /d0/d1/d2

mkdir -p /d0/d1/d2/.snap/snap1     # you create the snapshot; the daemon only syncs it
```

The daemon runs on the **primary** cluster, mounts both sides through libcephfs, and **pushes**. From Reef onwards it uses the snapdiff API (§11): *"For a given snapshot pair in a directory, cephfs-mirror daemon will rely on CephFS Snapdiff Feature to identify changes in a directory tree."* So it does not walk the tree — it gets the list of changed files directly.

That is where the advantages end, because **the unit of transfer remains the file**: *"The diffs are applied to directory in the remote file system thereby only synchronizing files that have changed between two snapshots"* and *"snapshot data is synchronized by bulk copying to the remote filesystem"*. Change 4 KB in the middle of a 500 GB image and 500 GB moves. That makes CephFS mirroring a usable tool for documents and photos and an **unusable** one for anything large and continuously rewritten.

The second consequence of copying **through the POSIX API** instead of serialising filesystem state: **hardlinks are not transferred as hardlinks.** Red Hat and IBM document it identically — *"Synchronizing hard links is not supported; hard linked files get synchronized as regular files."* Three hardlinks to one 10 GB file occupy 10 GB on the source and 30 GB on the destination, and are re-transferred every time. Only regular files, directories and symlinks are mirrored at all; other types are ignored. `zfs send` cannot have this class of problem, because it ships blocks and metadata, not files.

**Sparse regions are not preserved — a sparse file transfers at its nominal size.** The documentation does not state this either way, so it was read out of the source (resolved 2026-08-13). `PeerReplayer::copy_to_remote()` walks the file with `ceph_preadv`/`ceph_pwritev` from offset 0 to the end in fixed iovec batches, with no `SEEK_HOLE`/`SEEK_DATA` step anywhere in the loop; the only size-related call is `ceph_ftruncate(m_remote_mount, r_fd, stx.stx_size)`. Holes are therefore read back as zeros and written to the remote as zeros.

This is not an oversight in the daemon, and it could not be fixed there alone: **CephFS does not track allocation at all.** Its own POSIX-differences page says *"Because CephFS does not explicitly track which parts of a file are allocated/written, the st_blocks field is always populated by the file size divided by the block size"* and *"Sparse files propagate incorrectly to the stat(2) st_blocks field."* There is nothing for a hole-skipping copy loop to query.

Practical consequence: a 1 TiB sparse image holding 1 GiB of real data moves ~1 TiB across the link — and, because granularity is per file, it moves again in full every time any part of it changes. Sparse VM images and CephFS mirroring do not belong together, for two independent reasons at once. `zfs send` is untouched by this: a hole is an absent block in the tree, so there is nothing to serialise.

Further documented limits: a **single peer**, **one-way** only (failback is manual), and a snap-schedule on the remote filesystem for mirrored directories breaks metadata (*"will cause … errors like `invalid metadata`"*).

## 6. Unit of transfer and atomicity: the most-overlooked difference

"Snapshot mirroring" sounds the same for ZFS and for CephFS, but it names two different things — and the difference surfaces at exactly the moment it matters most, when a transfer dies halfway.

**ZFS: state serialisation, transactional receive.** `zfs send` produces a **stream** — a serialised filesystem state, not a set of files. `zfs recv` applies it as a transaction. Without `-s`, partially received state is discarded; the man page says so from the other direction, but unambiguously: `-s` means *"If the receive is interrupted, save the partially received state, rather than deleting it."* The consequence: **the destination dataset is a valid past snapshot at every moment.** It is never a mixture. (`btrfs send`/`receive` belongs to the same class — FS state serialisation, not a file copy.)

**CephFS: copy into the live directory, snapshot afterwards.** The documentation states the ordering literally: *"Snapshots are synchronized by transferring snapshot data to the remote file system **and by creating a snapshot with the same name** as the snapshot being synchronized."* Files are copied into the **live** remote directory first; the snapshot is created there only once that completes. In between, the directory is a mixture of old and new files.

That is why the documentation insists on *"Treat the remote filesystem as read-only. Nothing is inherently enforced by CephFS."* It is not a hygiene recommendation — it follows from the fact that mid-sync there simply is no valid state there.

**What to put in the runbook:** on a CephFS DR site your recovery point is not what sits in the directory, but the **last completed snapshot**. On a ZFS DR site the recovery point is the dataset itself. That is the difference between "restore" and "first work out what is valid".

The daemon recovers from interruption (*"Internal blocklist/failure restarts of a mirror instance preserve omap so sync can resume"*) and remembers what was already synchronised via **snap-id** in the `SnapInfo` structure on the MDS rather than by name — so deleting and recreating a snapshot of the same name does not confuse it.

## 7. Ceph RBD: a full block-level peer

Three routes, all block-level.

**A) `rbd-mirror`, snapshot-based** (Octopus onwards, §11) — periodic mirror snapshots from which a delta is computed: *"determine any data or metadata updates between two mirror-snapshots and copy the deltas to its local copy."* No write penalty; RPO = the schedule interval.

```bash
rbd mirror pool enable <pool> image
rbd mirror pool peer bootstrap create --site-name A <pool> > token   # import on B
rbd mirror image enable <pool>/<img> snapshot
rbd mirror snapshot schedule add --pool <pool> --image <img> 15m
```

**B) `rbd-mirror`, journal-based** (Jewel onwards) — *"Every write to the RBD image is first recorded to the associated journal before modifying the actual image."* Finer RPO, but every write is written twice and **latency roughly doubles**. It requires the `journaling` feature, which depends on `exclusive-lock`. For a WAN scenario it makes no sense; it is a DC-to-DC tool with bandwidth to spare.

**C) DIY, no daemon** — the direct counterpart of `zfs send -i`:

```bash
rbd snap create pool/img@2026-08-13
rbd export-diff --from-snap 2026-08-12 pool/img@2026-08-13 - \
  | ssh dr rbd import-diff - pool/img
```

`merge-diff` splices consecutive diffs into one. Size estimate up front: `rbd diff --from-snap snap1 pool/img@snap2 --format json`, then sum the extents. **Reasonable performance requires `object-map` + `fast-diff`** — with them the delta is computed from the in-memory object map instead of querying RADOS for every object.

**Where the daemon runs.** For one-way replication *"the rbd-mirror daemon runs only on the secondary cluster"* — that is **pull**, the opposite of `cephfs-mirror`. The daemon must have simultaneous connectivity to **both** clusters, to all monitor and OSD hosts. That is a non-trivial firewall and routing requirement between sites, and worth knowing before the network is designed rather than after.

## 8. Where block-level delta transfer loses

The counter-argument this document needs in order not to read as advertising: `zfs send -i` and `rbd export-diff` both ship **changed blocks**, not **changed content**. The moment data is rewritten in place without changing its logical content — defragmentation, dataset recompression after a `compression` change, a database rewriting pages, a rebalance — an enormous number of blocks are dirtied and the increment is several times larger than what rsync with a rolling checksum would move. In this one scenario file-level replication beats block-level, and by a wide margin.

The general rule: **block-level delta transfer wins on "many files, few changes" and loses on "few files, heavy CoW churn"**.

The second boundary is harder: neither `send`/`recv` nor `rbd-mirror` can **cross engines, change the layout, or select a subset**. ZFS → Ceph, a different structure on the destination, a writable destination, replicating a single subdirectory — those still belong to rsync/rclone, or to a dedup backup (Kopia, restic, borg, PBS) instead of replication. Replication and backup are not the same thing, and this document covers only the former.

## 9. Orchestration: what actually runs the loop

`zfs send` is a primitive, not a solution — snapshots, retention, retries and resume all need a driver.

| Tool | Scope | Notes |
|---|---|---|
| **zrepl** | two separate machines | A supervised daemon — retry and status reporting are built in. Push and pull, resumable transfer, replication cursor implemented as a bookmark, pruning policies. Transports: `tcp` (**unencrypted**), `tls` (client certificates, CN = identity), `ssh+stdinserver` (less efficient, but does not expose the daemon to the internet), `local`. Cost: its own config language and, for `tls`, certificate management. |
| **syncoid** (sanoid) | two machines over SSH | A script run from cron, not a daemon. Resume is supported and enabled automatically since 1.4.18; also `--create-bookmark`, `--source-bwlimit`/`--target-bwlimit`, and destination-side pruning via `--delete-target-snapshots`. sanoid handles snapshot creation and source retention. Residual gap: when a resume attempt itself fails, it does not fall back to a non-resumed send on its own ([#672](https://github.com/jimsalterjrs/sanoid/issues/672), open since 2021). Failure detection is the operator's job — a cron script that stopped running is silent. |
| **pve-zsync** | two **separate** Proxmox hosts | Over SSH, **no cluster membership required**. Push or pull, 15-minute default interval via cron. Exactly the "two sites, two clusters" profile. |
| **pvesr** | nodes of the **same** Proxmox cluster | ❗ **Not usable here.** Minimum interval 1 minute, but it only works within a single cluster. Easily confused with `pve-zsync`. |

So for two sites with their own clusters `pvesr` is out regardless of how well it works inside a cluster — and that is the most common mistake when designing this scenario.

## 10. Verification: a replica you have not scrubbed is not a replica

This applies to all four mechanisms and is the one section it would be a mistake to skip.

From [zfs-vs-ceph §15](../zfs-vs-ceph/README.md): **two of the four historical ZFS corruption bugs in the `send` path were silent** — `hole_birth` (2016) and encryption `send`/`recv` (#12014, closed only in 2025). Checksums cannot catch them, because the bug sits above the layer that computes checksums: the receiver reports no error and yet destination ≠ source. Historically, ZFS's risks live precisely in the send paths and in freshly shipped features, never in the core write path.

The minimum that follows, whichever tool is chosen: **a regular scrub on the destination**, **test restores** (not "check the file exists", but actually booting the VM or comparing checksums), and for ZFS **do not browse `.zfs` on the receiving side while a `recv` is running** — deadlock #18073, fixed only in the 5/2026 releases.

## 11. Dated snapshot: versions and feature availability (2026-08-13)

This section is the only perishable part of the document. When it goes stale, the conclusions in §2–§10 still hold.

| Feature | Since | Note |
|---|---|---|
| `zfs send -s` / resume token | OpenZFS (`extensible_dataset`) | Requires the pool feature on both sides |
| `zfs send -w` (raw) | OpenZFS | Corruption bugs over encrypted datasets closed only in 2025 (#12014) |
| RBD journal-based mirroring | Ceph **Jewel** | Roughly doubles write latency |
| RBD snapshot-based mirroring | Ceph **Octopus (v15)** | No write penalty |
| `cephfs-mirror` | Ceph **Pacific (v16)** | Both sides must be Pacific or later |
| CephFS snapdiff | Ceph **Reef (v18)**, PR #53229 | Without it `cephfs-mirror` walks the tree |
| `cephfs-mirror` uses the snapdiff API | Ceph **Squid (v19)**, PR #58984 | i.e. full detection efficiency only from here |

**Ceph release state as of 2026-08-13:** the active releases are **Tentacle (v20.2)** — recommended for new deployments, latest v20.2.3 released 2026-08-05 — and **Squid (v19.2)**, supported until 9/2026. Reef is near end of life. For `cephfs-mirror` this means the fully efficient variant (the snapdiff API) is available across all actively supported lines.

## 12. Verdict

⭐ **The mechanism: `zfs send -i`.** This is what the analysis supports, and it supports it strongly.

Against the decision rules from §1:

1. **Budget known in advance** ✅ — `zfs send -nvP` gives the exact stream size. The only alternative with the same ability is RBD (`rbd diff`), which fails the node-count rule.
2. **An outage does not mean restarting from zero** ✅ — `recv -s` plus the resume token, and zrepl drives it without intervention.
3. **The destination is a valid DR point at any moment** ✅ — transactional `recv` (§6). `cephfs-mirror` would fail this rule.
4. **One mechanism for files and VM disks** ✅ — a direct consequence of §2; no Ceph variant satisfies it even in principle.

The **disqualifying criterion did not fire** — a single-node Ceph cluster is explicitly supported upstream, so both Ceph options had to be beaten on their merits: CephFS mirror on rules 1, 3 and 4, RBD mirror on rule 4. See §13 for the full correction and for what is genuinely true about a single-node destination.

**The orchestrator is a much closer call, and this analysis does not settle it.** An earlier draft recommended zrepl outright; the adversarial pass killed that reasoning, because the resume-robustness argument it rested on described sanoid's 2018–2020 state (issues [#304](https://github.com/jimsalterjrs/sanoid/issues/304), [#528](https://github.com/jimsalterjrs/sanoid/issues/528), both closed) rather than today's. Verified as of 2026-08-13, syncoid does resume automatically, does bookmarks, does bandwidth limits and does destination-side pruning — so on the four decision rules the two are equivalent. What actually separates them is a trade-off the context pulls in both directions at once: zrepl is a **supervised daemon**, so "did last night's replication run?" is answerable without extra plumbing — which matters with no on-call; syncoid is **a cron line**, which is less to operate and less to misconfigure — which matters for a solo admin who values simplicity. **Pick zrepl if you want failure detection included; pick syncoid if you already run monitoring that would notice a silent cron job.** Either satisfies §1. Whichever is chosen, do not use zrepl's `tcp` transport — it is unencrypted.

**Consciously accepted trade-offs:**

- **No native failback.** Swapping roles is manual, where RBD has promote/demote. For a DR site nothing writes to, that is acceptable; if it ever became an active node, this point reopens.
- **Chain fragility.** One deleted anchor snapshot = a full resend. The mitigations are cheap (bookmarks, `zfs hold`, `readonly=on` on the destination) but must be in place from the start, not after the first incident.
- **CoW churn** (§8) can spike transfer volume in one go. Marginal for bulk media; but before a planned recompression or a `recordsize` change, expect essentially everything to move again.
- **Whole dataset or nothing.** A subset cannot be replicated → **dataset design becomes replication design**. That is a decision made once and changed painfully.
- **Encryption:** with LUKS chosen (see [zfs-vs-ceph §12](../zfs-vs-ceph/README.md)), `send -w` is moot — the stream carries plaintext ZFS blocks and confidentiality on the wire rests entirely on the transport. The DR site therefore needs its own LUKS + Tang, not just a disk.

**I will change my mind if:** (a) the second site needs a shared RWX filesystem replicated across sites — ZFS has nothing to offer there and even the weaker `cephfs-mirror` beats nothing; (b) the daily change volume drops so low that the difference between file-level and block-level granularity disappears into the link's noise, which removes the main argument; (c) the DR site becomes an active writing node, turning manual failback from an inconvenience into a risk.

## 13. Correction (2026-08-13): the single-node destination

**The original §1 disqualifying criterion and the "min. 3 nodes" ratings were wrong.** They were corrected the same day the document was published, after a reader challenged them. What follows is the corrected position; the rule in §1 is left as written, because a decision rule that gets rewritten after seeing the result is no longer a decision rule (it is now read as: *the rule did not fire*).

**Fact: a single-node Ceph cluster is explicitly supported upstream.** cephadm has a dedicated flag — *"To deploy a Ceph cluster running on a single host, use the `--single-host-defaults` flag when bootstrapping."* It sets three options:

```
global/osd_crush_chooseleaf_type = 0     # failure domain drops from host to OSD
global/osd_pool_default_size     = 2
mgr/mgr_standby_modules          = False
```

Upstream attaches one caveat in the same breath: *"such clusters are generally not suitable for production."* That sentence is not a support disclaimer or a code-maturity warning — **the flag itself is the reason**, because each of the three options it sets trades away something Ceph exists to provide:

- `osd_crush_chooseleaf_type = 0` moves the failure domain from host to OSD, so both replicas may land on the same machine. The cluster no longer survives host loss — which is the single property that distinguishes Ceph from local storage.
- `osd_pool_default_size = 2` halves the default. Ceph's own pool documentation is blunt: *"setting `size` to `2` or `min_size` to `1` in production risks data loss and should only be done in certain emergency situations, and then only temporarily."* The default is 3.
- One host also means **one monitor**, and *"a single Monitor is a single-point-of-failure"*; production guidance is at least three in quorum. `mgr_standby_modules = False` similarly drops the standby manager.

So "not for production" means: on one node Ceph keeps all of its operational cost while giving up host-failure tolerance, monitor quorum and cross-host self-healing. It is supported and it runs — it just is not doing the job it exists to do. For a DR target that is a defensible trade only if something else on the far side justifies Ceph.

Both mirroring daemons are unaffected by node count — `rbd-mirror` and `cephfs-mirror` are ordinary daemons, and a 1-node → 1-node replication pair works.

**So the disqualifying criterion did not fire, and both Ceph options had to be beaten on their merits instead.** They were:

- **CephFS mirror** fails decision rule 1 (no way to size a transfer up front), rule 3 (the live remote directory is not a valid DR point mid-sync, §6) and rule 4 (files only). Three rules, none of them about node count.
- **RBD mirror** passes rules 1, 2 and 3 — it is a genuinely good mechanism — but fails rule 4: it is block-only. Covering ~150 TiB of bulk media files with it would mean either adding CephFS alongside (two mechanisms, two runbooks — exactly what rule 4 exists to prevent) or storing all media inside RBD images, which is an odd shape for a Plex/Nextcloud dataset.

**The verdict survives, on better reasoning than it originally had.** The node-count argument was not merely wrong, it was also weaker than the argument that replaced it: rule 4 is a property of what the mechanisms *are*, whereas node count was a property of the deployment I assumed.

**What is genuinely true about a 1-node destination**, and worth knowing before building one:

- **Redundancy drops to the OSD level.** With `osd_crush_chooseleaf_type = 0` and `size = 2`, both replicas can land on the same host — which is the point — so the cluster survives a disk loss but not a host loss, at 50 % capacity efficiency. ZFS RAIDZ2 on the same box survives two disk losses at ~75 %. On a single node the destination-side economics favour ZFS regardless of the replication question.
- **Do not mount CephFS with the kernel client on a node that also runs OSDs.** Under memory pressure the kernel client tries to flush to the OSD while the OSD tries to allocate memory, and the node deadlocks — reported since [#1317](https://tracker.ceph.com/issues/1317) (2011) and still tracked in [#3076](https://tracker.ceph.com/issues/3076) and [#12648](https://tracker.ceph.com/issues/12648). Red Hat's guide states it flatly: *"DO NOT mount kernel clients directly on the same node as your Ceph Storage Cluster."* Workarounds: use `ceph-fuse` (userspace memory is pageable, so the system recovers) or mount from a VM. This bites exactly the 1-node CephFS case and not the 3-node one. Note it does **not** affect `cephfs-mirror` itself, which uses libcephfs in userspace.
- **The operational cost does not scale down with the node count.** One node still means mon + mgr + OSDs + MDS, cephadm containers and ~4 GB RAM per OSD, to run a distributed system on hardware that cannot distribute anything.

*(This section is an addendum; earlier sections are left as published except for the affected table row.)*

## 14. Renaming or moving a large tree (added 2026-08-13)

Renaming a directory that holds a lot of data is the sharpest test of what a replication mechanism actually keys on, and the four answers span the whole range — including one inversion, because **here `cephfs-mirror` is worse than the rsync baseline it is supposed to improve on.**

**ZFS: effectively free, within a dataset.** A rename is a metadata operation — it rewrites the directory entry in the source parent, adds one in the destination parent, and updates the moved object's parent pointer, plus the indirect blocks above them. No file data block is touched. Since the increment is defined as "blocks whose birth time is newer than the source snapshot" (§3), renaming a directory holding 100 TiB moves a few kilobytes. The tree does not move because nothing in the tree changed.

The caveat is the one that matters for design: **this holds only within one dataset.** Across datasets `rename(2)` fails with `EXDEV` and `mv` degrades to copy-and-delete, which writes every block anew — so a "move" between datasets is a full re-transfer of everything under it. That sharpens the point already made in §12: dataset boundaries are replication boundaries, and a layout that puts a frequently-reorganised tree astride two datasets pays for it on the link.

**RBD: invisible.** Filenames live inside the guest filesystem; RBD replicates blocks and never sees a path. A rename dirties only the guest filesystem's own metadata, so at worst a handful of 4 MB objects appear in the delta. The same structural win as ZFS, for the same reason — path-agnostic replication cannot be fooled by a path change.

**CephFS mirror: delete plus a full re-copy, with no mitigation.** There is no rename detection in the daemon. `propagate_deleted_entries()` compares the two snapshots, finds entries present in the previous one but absent (or type-changed) in the current one, and purges them on the remote via `cleanup_remote_dir()` — a recursive walk issuing `ceph_unlinkat`. The new path is then synchronised as a fresh copy. The code never matches inodes across the delete/create boundary; one of its own comments notes the ordering it relies on: *"N.B.: snapdiff returns the deleted entry before the newly created one."* Rename a directory holding 100 TiB and the remote deletes 100 TiB and re-transfers 100 TiB.

**rsync: bad by default, and `--fuzzy` does not rescue this case.** The default behaviour is exactly as expected — the old path is deleted at the destination and the new one transferred in full. `--fuzzy`/`-y` exists, but read its scope carefully: *"The current algorithm looks in the same directory as the destination file for either a file that has an identical size and modified-time, or a similarly-named file."* After a **directory** rename the destination directory is newly created and empty, so there is no basis file in it to find. `--fuzzy` mitigates files renamed *within* a directory; it does nothing for a renamed directory. Repeating it only extends the scan into `--compare-dest`/`--copy-dest`/`--link-dest` trees. `--detect-renamed` is not a standard option — it does not appear in the rsync 3.4.4 manual page and lives among rsync's unapplied patches.

**Why the inversion matters.** rsync at least degrades gracefully: `--link-dest` against the previous run, or a fuzzy match, can salvage part of the work, and the failure mode is well known enough that people plan around it. `cephfs-mirror` offers no such lever — the delete-and-recopy is structural, and on a metered link one `mv` can consume a month's budget with no warning and no way to estimate it in advance (§5 already established that it cannot size a transfer up front). For a bulk media library, where reorganising directory trees is a normal thing to do rather than an exceptional one, this is a heavier objection than it first appears.

## 15. Btrfs send/receive (added 2026-08-13)

Btrfs belongs in the table for two reasons. It is the **only other mechanism in the same class as `zfs send`** — a filesystem-state serialisation rather than a file copy — which makes it the control that tests whether the verdict is really about ZFS or merely about "stream-based replication". And in this project it is not hypothetical: the incumbent single-node server runs `mdadm + LUKS + LVM + Btrfs` and, per [zfs-vs-ceph](../zfs-vs-ceph/README.md), is destined to become the DR target at the second site.

**Where it matches ZFS.** The incremental is `btrfs send -p <parent> <subvol>`, with `-c` to name additional clone sources. Change detection uses generation numbers, so like ZFS it never walks the tree and its cost tracks the volume of change. `--compressed-data` *"send[s] data that is compressed on the filesystem directly without decompressing it"* — the counterpart of `zfs send -c` — requiring stream protocol v2 and Linux 6.0 or newer. All snapshots involved must be read-only: *"All snapshots involved in one send command must be read-only, and this status cannot be changed as long as there's a running send operation that uses the snapshot."*

**Where it beats everything else, including ZFS — renames.** The send stream is a command language, and `BTRFS_SEND_C_RENAME` (9) is one of its commands, carrying a source path and a target path. A moved or renamed tree is transmitted as an explicit instruction, not as delete-plus-recopy. ZFS reaches the same outcome for a different reason (a rename dirties only metadata blocks, §14), but Btrfs is the only mechanism here that represents the rename *as such*, which also means it survives moves that cross what would be a dataset boundary in ZFS — precisely the `EXDEV` case that costs ZFS a full re-transfer (§14).

**Where it fails this context, and it is decisive.** Two of the four decision rules from §1 fail outright:

- **Rule 2 — no resume.** There is no resume capability in `btrfs send` or `btrfs receive`, and none is documented. An interrupted transfer restarts from zero. On a residential WAN moving multi-TiB increments, that alone is disqualifying — it is the exact failure mode rule 2 exists to exclude.
- **Rule 1 — no size estimate.** `btrfs send` has no dry-run option, so there is no way to price a transfer before committing it against a monthly cap. `zfs send -nvP` has no Btrfs counterpart.

Two further problems compound the first. The received subvolume is *"made read-only after the receiving process finishes successfully"*, so an interrupted receive leaves a **writable, partial subvolume behind** — which is not cleaned up automatically and, as the btrbk tracker records, is easy to mistake for a completed one ([btrbk #17](https://github.com/digint/btrbk/issues/17)). Worse, because the next incremental needs the previous *successfully received* snapshot as its parent, one failed transfer can block every subsequent one until someone intervenes ([btrbk #91](https://github.com/digint/btrbk/issues/91), [#196](https://github.com/digint/btrbk/issues/196)). For a solo admin with no on-call, a replication chain that wedges silently and stays wedged is a worse property than a slow one. The manual page also warns that the receiving path is writable while a receive is in progress: *"users who have write access to files or directories in the receiving path can add, remove, or modify files."*

**And it has no block-device story.** Btrfs has no ZVOL equivalent, so VM disks are ordinary files. That fails rule 4 the same way RBD does, from the opposite direction: RBD does blocks but not files, Btrfs does files but not blocks.

**The consequence for the DR site.** Replication does not cross engines (§8), so keeping the incumbent box on Btrfs means the ZFS primary cannot `send` to it at all — the DR link would fall back to rsync, giving up block granularity, atomicity and the size estimate in one step. **If that server is to be the DR target, it should be rebuilt on ZFS rather than kept on Btrfs.** That conclusion was implicit in the original zfs-vs-ceph migration plan; stated here it is explicit, and it is the practical reason this section exists rather than being a footnote.

**What Btrfs does not lose on.** It needs no daemon, runs push or pull, needs exactly one node on the destination, and its extent-level granularity is genuinely comparable to ZFS's. On a reliable LAN link, with a tool like btrbk handling the snapshot and retry policy, Btrfs → Btrfs replication is a reasonable design. It is this context — an unreliable metered WAN, no on-call, and VM disks in the mix — that rules it out, not the mechanism being weak in general.

## 16. Proxmox Backup Server (added 2026-08-13)

PBS is in the table on a different footing from the other five, and pretending otherwise would be the mistake. §8 already drew the line: replication and backup are not the same thing. **PBS is not a replication target you can fail over to — it is a datastore you restore from.** It earns its column anyway, because it does incrementally move changes between two sites, it is already in this project's stack per [zfs-vs-ceph](../zfs-vs-ceph/README.md), and on several rows it beats every replication mechanism here.

**How the delta is produced.** PBS splits data into content-addressed chunks: fixed 4 MiB for block images, because *"the content (disk image), is split into chunks of the same length (typically 4 MiB)"*, and variable-size for file archives, where it *"first generates a consistent file archive (pxar) and uses a rolling hash over this on-the-fly generated archive to calculate chunk boundaries."* Identical content hashes identically, so the upload step is a negotiation: *"If it detects a chunk that already exists on the server, it can send only the checksum instead of data and checksum."*

**The distinction that matters — read cost is not transfer cost.** For VMs, *"VMs in Proxmox VE can make use of 'dirty bitmaps', which can track the changed blocks of an image"*, and because bitmap granularity matches chunk boundaries, only modified chunks are uploaded. But the bitmap is fragile: it lives only while the VM runs, so a stop or a reboot (including "Reboot" from the PVE UI to apply pending changes) discards it, and it is bound to one target server, so backing the same VM up to two PBS instances invalidates it every time. Losing it does **not** cost network traffic — the known-chunks negotiation still suppresses re-upload — it costs a full local re-read of the disk. For files the analogue is `change-detection-mode=metadata`, which *"Encode[s] changed files, reuse[s] unchanged from previous snapshot, creating a split archive"*, comparing against the previous metadata archive to avoid re-reading unchanged files. Without it, a 150 TiB media set is re-read on every run.

That is why the table rates PBS ❌ on "detection cost scales with" while rating it ✅ on the transfer rows: it is the only mechanism here whose expensive resource is **local I/O rather than the link**.

**Where PBS beats every replication mechanism in this document.** Three rows, and they are not minor:

- **Client-side encryption.** AES-256-GCM, keys stay on the client, and *"Without their key, backed up files will be inaccessible."* §12 flagged that with LUKS the DR site necessarily holds a decryptable copy and therefore needs its own LUKS + Tang. PBS does not have that problem at all — the far end never holds plaintext or a key. It is a stronger guarantee than `zfs send -w`, and it is engine-independent.
- **Built-in verification.** §10 argued that a replica nobody scrubs is not a replica, and that two of the four historical ZFS `send`-path bugs were silent. PBS ships verify jobs that re-check backups against recorded checksums as a scheduled operation — the discipline §10 asks for, as a feature rather than as a cron job you remember to write.
- **Engine independence and content addressing.** It does not care what filesystem is underneath, so ZFS → anything works where `send`/`recv` cannot cross engines (§8). And because chunks are content-addressed, the two cases that punish block-level replication — an in-place rewrite that changes no logical content (§8), and a renamed tree (§14) — cost nothing: the same chunks are simply re-referenced.

**Cross-site: sync jobs.** Two independent PBS instances replicate to each other with sync jobs, *"configured for pull or push direction"*, on a schedule, transferring only what the destination lacks. This is genuinely the document's question answered by other means. One operational trap for a metered link: the general traffic-control rate limits do **not** cover them — *"Sync jobs on the server are not affected by the configured rate limits. If you want to limit the incoming traffic of pull-based or outgoing traffic of push-based sync job, you need to setup a job-specific rate-in limit."*

**Against the decision rules from §1.** PBS passes rule 3 (a completed snapshot is immutable and verifiable) and rule 4 (one mechanism for both files and VM disks — which no Ceph option manages). It fails rule 1: there is no way to price tonight's transfer before running it. On rule 2 it is partial — there is no resume token, but because chunks are content-addressed, a retry after an outage re-sends only what the server still lacks, which in practice is most of what a resume token buys.

**Why it does not take the verdict.** The destination is not a state you can serve from. Recovering means restoring, and for ~150 TiB of media that is measured in days, not minutes — so PBS cannot satisfy the purpose the DR site exists for. That is not a defect; it is a different job.

**The actual conclusion: run both, and do not make either do the other's work.** `zfs send` gives a DR replica that is already a live filesystem, with a priceable increment and a resume token. PBS gives point-in-time restore, retention, deduplication across snapshots, client-side encryption for the off-site copy, and the verification discipline of §10. The failure mode to avoid is treating either as a substitute: a `send`/`recv` replica is not a backup (it faithfully replicates a deletion), and a PBS datastore is not a failover target.

## References

External sources verified 2026-08-13:

- OpenZFS: [zfs-send(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html), [zfs-receive(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html)
- Ceph RBD: [RBD Mirroring](https://docs.ceph.com/en/latest/rbd/rbd-mirroring/), [rbd(8) — export-diff / import-diff / merge-diff / fast-diff](https://docs.ceph.com/en/latest/man/8/rbd/), [Incremental Snapshots with RBD (ceph.io)](https://ceph.io/en/news/blog/2013/incremental-snapshots-with-rbd/)
- CephFS: [CephFS Snapshot Mirroring (user)](https://docs.ceph.com/en/latest/cephfs/cephfs-mirroring/), [CephFS Mirroring (dev)](https://docs.ceph.com/en/latest/dev/cephfs-mirroring/), [the source rst on GitHub](https://github.com/ceph/ceph/blob/main/doc/dev/cephfs-mirroring.rst), [PR #37876 — cephfs-mirror: synchronize directory snapshots](https://github.com/ceph/ceph/pull/37876), [Red Hat Ceph Storage 8 — File System mirrors (hardlinks)](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/8/html/file_system_guide/ceph-file-system-mirrors), [IBM Storage Ceph — File System mirrors](https://www.ibm.com/docs/en/storage-ceph/6.1.0?topic=systems-ceph-file-system-mirrors), [croit — CephFS Snapdiff Feature](https://www.croit.io/blog/introducing-the-innovative-cephfs-snapdiff-feature)
- Ceph releases: [Ceph Releases (index)](https://docs.ceph.com/en/latest/releases/), [v20.2.0 Tentacle](https://ceph.io/en/news/blog/2025/v20-2-0-tentacle-released/), [v20.2.1 Tentacle](https://ceph.io/en/news/blog/2026/v20-2-1-tentacle-released/), [v19.2.4 Squid](https://ceph.io/en/news/blog/2026/v19-2-4-squid-released/)
- Orchestration: [zrepl — Configuration Overview](https://zrepl.github.io/configuration/overview.html), [zrepl — Transports](https://zrepl.github.io/configuration/transports.html), [sanoid/syncoid — README](https://github.com/jimsalterjrs/sanoid), [sanoid #672 — automatic fallback when resume fails (open)](https://github.com/jimsalterjrs/sanoid/issues/672), [Proxmox — Storage Replication (`pvesr`)](https://pve.proxmox.com/wiki/Storage_Replication), [Proxmox — PVE-zsync](https://pve.proxmox.com/wiki/PVE-zsync)
- PBS (§16): [Technical Overview — chunks, dedup, dirty bitmaps](https://pbs.proxmox.com/docs/technical-overview.html), [Backup Client — `change-detection-mode`, client-side encryption](https://pbs.proxmox.com/docs/backup-client.html), [Managing Remotes — sync jobs](https://pbs.proxmox.com/docs/managing-remotes.html), [Network Management — traffic control](https://pbs.proxmox.com/docs/network-management.html), [Storage — verification jobs](https://pbs.proxmox.com/docs/storage.html)
- Btrfs (§15): [btrfs-send(8)](https://btrfs.readthedocs.io/en/latest/btrfs-send.html), [btrfs-receive(8)](https://btrfs.readthedocs.io/en/latest/btrfs-receive.html), [send stream format — `BTRFS_SEND_C_RENAME`](https://btrfs.readthedocs.io/en/latest/dev/dev-send-stream.html), [btrbk #17 — partial subvolumes not deleted on error](https://github.com/digint/btrbk/issues/17), [#91](https://github.com/digint/btrbk/issues/91), [#196](https://github.com/digint/btrbk/issues/196)
- Renames (§14): [`PeerReplayer.cc` — `propagate_deleted_entries()` / `cleanup_remote_dir()`](https://github.com/ceph/ceph/blob/main/src/tools/cephfs_mirror/PeerReplayer.cc), [rsync 3.4.4 manual — `--fuzzy`](https://download.samba.org/pub/rsync/rsync.1)
- Sparse handling (§5): [`PeerReplayer.cc` — `copy_to_remote()`](https://github.com/ceph/ceph/blob/main/src/tools/cephfs_mirror/PeerReplayer.cc), [CephFS — Differences from POSIX](https://docs.ceph.com/en/latest/cephfs/posix/)
- Single-node Ceph (§13): [cephadm — `--single-host-defaults`](https://docs.ceph.com/en/latest/cephadm/install/), [Ceph — Pools (`size`/`min_size` guidance)](https://docs.ceph.com/en/latest/rados/operations/pools/), [Ceph — Monitor Config Reference](https://docs.ceph.com/en/latest/rados/configuration/mon-config-ref/), [tracker #1317 — deadlock, kclient on an OSD node](https://tracker.ceph.com/issues/1317), [#3076](https://tracker.ceph.com/issues/3076), [#12648](https://tracker.ceph.com/issues/12648), [Red Hat — Mounting and Unmounting Ceph File Systems](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/2/html/ceph_file_system_guide_technology_preview/mounting_and_unmounting_ceph_file_systems)
- Related context: [ZFS vs Ceph — this repository](../zfs-vs-ceph/README.md) (§12 encryption, §15 reliability profiles and the silent-corruption timelines)

---

*Researched and written in collaboration with Claude (Anthropic); facts verified against the sources above as of 13 August 2026. This document is a dated snapshot and is not continuously updated.*

*© 2026 Petr Kratochvíl · Licensed under [CC BY 4.0](../LICENSE)*
