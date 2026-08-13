# Incremental replication between two storage clusters: ZFS send/recv vs Ceph mirroring

- **Verdict:** ⭐ **`zfs send -i`** (orchestrated by zrepl *or* syncoid — §12) — valid for the context described below
- **Facts verified:** 2026-08-13 (OpenZFS master man pages, docs.ceph.com latest, Proxmox wiki, zrepl docs, sanoid/syncoid README + issue tracker, Red Hat/IBM Ceph docs)
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

## Comparison at a glance

Symbols: ✅ strength · 🟡 works with caveats / a compromise · ❌ weakness or missing · — not applicable. Rated **for this context** (two sites, asymmetric residential WAN with a data cap, solo admin, bulk media + a handful of VM disks, a DR target that is never written to) — not in general; on a symmetric DC link with generous bandwidth several rows would come out differently. The last column is the engine-neutral baseline the others are measured against.

| Criterion | ZFS `send`/`recv` | Ceph RBD mirror | CephFS mirror | rsync / rclone |
|---|---|---|---|---|
| **▸ How the delta is produced** | | | | |
| Unit of transfer | ✅ block (`recordsize`/`volblocksize`) | ✅ object / extent | ❌ **the whole changed file** | 🟡 rolling-checksum delta |
| Finds changes without walking the tree | ✅ birth time in the CoW tree | ✅ object-map + fast-diff | ✅ snapdiff (Reef onwards, §11) | ❌ stat every file |
| Detection cost scales with | ✅ volume of changes | ✅ object count (from an in-memory map) | 🟡 number of changed files | ❌ **total number of files** |
| Serialises FS state vs copies via POSIX | ✅ FS state (holes, compression, properties) | ✅ blocks (POSIX not involved) | ❌ POSIX copy → **hardlinks decompose** | ❌ POSIX copy |
| **▸ Atomicity and consistency** (§6) | | | | |
| Destination is always a valid past state | ✅ transactional `recv` | ✅ delta applies wholly, or rolls back | ❌ live directory is a mix during a sync | ❌ |
| Consistent point after a mid-transfer crash | ✅ last received snapshot | ✅ last mirror snapshot | 🟡 last **completed** snapshot on the remote | ❌ none |
| Resume after a link outage | ✅ resume token (`recv -s`) | 🟡 the daemon continues; DIY `export-diff` does not | 🟡 the daemon continues (per file) | 🟡 `--partial` |
| **▸ Link and budget** | | | | |
| **Transfer size known in advance** | ✅ `zfs send -nvP` (exact) | ✅ `rbd diff --format json` (sum the extents) | ❌ no | ❌ `--dry-run` gives only a list |
| Compression on the wire | ✅ `-c` ships blocks compressed as they sit on disk | 🟡 external (ssh `-C`) | 🟡 external | ✅ `-z` |
| Transfer without a key on the destination | ✅ `send -w` (raw) | ❌ | ❌ | ❌ |
| Bandwidth limiting | ✅ zrepl / `pv` / `mbuffer` | 🟡 daemon configuration | 🟡 daemon configuration | ✅ `--bwlimit` |
| **▸ Operations** | | | | |
| Daemon required | ✅ none (or zrepl) | ❌ `rbd-mirror` | ❌ `cephfs-mirror` | ✅ none |
| Where the daemon runs / direction | ✅ push or pull | 🟡 **secondary** (pull) | 🟡 **primary** (push) | ✅ either |
| Bidirectional / failback | 🟡 manual role swap | ✅ promote/demote, two-way | ❌ one-way, **single peer** | 🟡 manual |
| Min. nodes on the destination | ✅ **1** | 🟡 1 supported, not production-grade (§13) | 🟡 1, plus a kernel-client caveat (§13) | ✅ 1 |
| **▸ Fit for the workload** | | | | |
| Large continuously-modified files (VM, DB) | ✅ | ✅ | ❌ transfers the whole file | 🟡 delta yes, but reads the whole file |
| Millions of small files, few changes | ✅ | — | ✅ | ❌ the walk dominates the transfer |
| In-place rewrite / recompression (§8) | ❌ ships every dirtied block | ❌ ditto | ✅ ships only changed files | ✅ ships only changed content |
| Writable / RWX destination | ❌ destination must be `readonly` | ❌ | ✅ (but should not be) | ✅ |
| Subset of a dataset / different layout | ❌ whole dataset | ❌ whole image | ✅ per directory | ✅ freely |
| Transfer between different engines | ❌ | ❌ | ❌ | ✅ |

**How to read it.** ZFS wins everywhere the question is "how many bytes will move and what happens when the link drops" — block granularity, an exact estimate up front, a transactional receive and a resume token. RBD is its equal at the block level and beats it on one row (native bidirectional failover with promote/demote), but pays with three nodes on the destination side and a mandatory daemon. CephFS mirror wins only where the others cannot compete at all — a shared writable filesystem and replication per directory rather than per whole dataset — and loses on granularity, atomicity and hardlinks. rsync is the last column not because it is bad, but because it is the only one that does what none of the others can: **change the engine, change the layout, take a subset** — and in one scenario (§8) it beats all of them.

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

## References

External sources verified 2026-08-13:

- OpenZFS: [zfs-send(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html), [zfs-receive(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html)
- Ceph RBD: [RBD Mirroring](https://docs.ceph.com/en/latest/rbd/rbd-mirroring/), [rbd(8) — export-diff / import-diff / merge-diff / fast-diff](https://docs.ceph.com/en/latest/man/8/rbd/), [Incremental Snapshots with RBD (ceph.io)](https://ceph.io/en/news/blog/2013/incremental-snapshots-with-rbd/)
- CephFS: [CephFS Snapshot Mirroring (user)](https://docs.ceph.com/en/latest/cephfs/cephfs-mirroring/), [CephFS Mirroring (dev)](https://docs.ceph.com/en/latest/dev/cephfs-mirroring/), [the source rst on GitHub](https://github.com/ceph/ceph/blob/main/doc/dev/cephfs-mirroring.rst), [PR #37876 — cephfs-mirror: synchronize directory snapshots](https://github.com/ceph/ceph/pull/37876), [Red Hat Ceph Storage 8 — File System mirrors (hardlinks)](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/8/html/file_system_guide/ceph-file-system-mirrors), [IBM Storage Ceph — File System mirrors](https://www.ibm.com/docs/en/storage-ceph/6.1.0?topic=systems-ceph-file-system-mirrors), [croit — CephFS Snapdiff Feature](https://www.croit.io/blog/introducing-the-innovative-cephfs-snapdiff-feature)
- Ceph releases: [Ceph Releases (index)](https://docs.ceph.com/en/latest/releases/), [v20.2.0 Tentacle](https://ceph.io/en/news/blog/2025/v20-2-0-tentacle-released/), [v20.2.1 Tentacle](https://ceph.io/en/news/blog/2026/v20-2-1-tentacle-released/), [v19.2.4 Squid](https://ceph.io/en/news/blog/2026/v19-2-4-squid-released/)
- Orchestration: [zrepl — Configuration Overview](https://zrepl.github.io/configuration/overview.html), [zrepl — Transports](https://zrepl.github.io/configuration/transports.html), [sanoid/syncoid — README](https://github.com/jimsalterjrs/sanoid), [sanoid #672 — automatic fallback when resume fails (open)](https://github.com/jimsalterjrs/sanoid/issues/672), [Proxmox — Storage Replication (`pvesr`)](https://pve.proxmox.com/wiki/Storage_Replication), [Proxmox — PVE-zsync](https://pve.proxmox.com/wiki/PVE-zsync)
- Sparse handling (§5): [`PeerReplayer.cc` — `copy_to_remote()`](https://github.com/ceph/ceph/blob/main/src/tools/cephfs_mirror/PeerReplayer.cc), [CephFS — Differences from POSIX](https://docs.ceph.com/en/latest/cephfs/posix/)
- Single-node Ceph (§13): [cephadm — `--single-host-defaults`](https://docs.ceph.com/en/latest/cephadm/install/), [Ceph — Pools (`size`/`min_size` guidance)](https://docs.ceph.com/en/latest/rados/operations/pools/), [Ceph — Monitor Config Reference](https://docs.ceph.com/en/latest/rados/configuration/mon-config-ref/), [tracker #1317 — deadlock, kclient on an OSD node](https://tracker.ceph.com/issues/1317), [#3076](https://tracker.ceph.com/issues/3076), [#12648](https://tracker.ceph.com/issues/12648), [Red Hat — Mounting and Unmounting Ceph File Systems](https://docs.redhat.com/en/documentation/red_hat_ceph_storage/2/html/ceph_file_system_guide_technology_preview/mounting_and_unmounting_ceph_file_systems)
- Related context: [ZFS vs Ceph — this repository](../zfs-vs-ceph/README.md) (§12 encryption, §15 reliability profiles and the silent-corruption timelines)

---

*Researched and written in collaboration with Claude (Anthropic); facts verified against the sources above as of 13 August 2026. This document is a dated snapshot and is not continuously updated.*

*© 2026 Petr Kratochvíl · Licensed under [CC BY 4.0](../LICENSE)*
