# Shared storage and mounts

## Verified topology

Admin `/home` is an XFS/LVM filesystem (approximately 39.8 GiB). The admin NFS server exports `/home` read-write and `/opt` read-only to the private `192.168.10.0/24` network. `exportfs -v` showed **effective** `/home` `root_squash` and `/opt` `no_root_squash`, even though the generated `/etc/exports` only explicitly sets the latter. Preserve the distinction between the source file and effective options.

Each of `node01`–`node04` had:

| Path | Source | Type | Mode / status |
|---|---|---|---|
| `/home` | `warewulf:/home` (`192.168.10.2`) | NFSv4.2 | mounted `rw`, `hard`, TCP |
| `/opt` | Local RAM rootfs (`/`) | rootfs | No active NFS mount; profile says `noauto,ro` |
| `/` | Per-node RAM-based `rootfs` | rootfs | ≈7.1 GiB apparent size, nonpersistent |

`df -h` on every node reported the same **~40G** `/home` shared filesystem. This is **one shared volume**, not four independent volumes. A read-only `findmnt -T /opt` returned `/` because `/opt` was not separately mounted at test time; that is consistent with `noauto` and must not be misreported as an NFS failure.

## Safe observational checks

```bash
sudo exportfs -v
findmnt -T /home -o TARGET,SOURCE,FSTYPE,OPTIONS
findmnt -T /opt -o TARGET,SOURCE,FSTYPE,OPTIONS
df -h /home /opt
```

NFS write-permission checks, client remounts, and root-squash policy changes were **not performed** in this audit. The `/opt` export's `no_root_squash` is a remaining review item, despite the fact that it is read-only. Do not place passwords or private keys in shared directories merely because they are reachable only from the private LAN.
