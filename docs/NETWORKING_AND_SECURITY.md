# Networking and security assessment

This is a **factual security review**, not a firewall replacement script. Changes to a school-managed network require approval and a rollback plan.

## Interfaces and logical isolation

| Interface | Role | Observation |
|---|---|---|
| `enp3s0` | Private cluster LAN | `192.168.10.2/24`, `trusted` firewalld zone, switch to 4 nodes |
| `enp2s0` | School/campus uplink | On the `public` firewalld zone; exact address omitted here |
| `tailscale0` | Remote administrative overlay | Present; ACL and SSH policy were not audited |

Private addressing is not proof of physical isolation. The TP-Link LS1016G is unmanaged; no VLAN or switch-level segmentation was verified.

## Observed firewall posture

The **runtime** `public` zone includes services `cockpit, dhcp, dhcpv6-client, nfs, ssh, tftp` and ports `9873/tcp`, `6817-6818/tcp`. That zone is associated with campus-facing `enp2s0`. This increases the set of services potentially reachable from the campus network; actual reachability depends on upstream filtering and routing, which were not tested. **Ask the school IT/supervisor to review** whether DHCP, PXE, NFS, Slurm and Warewulf should be permitted on that interface. Avoid disrupting active provisioning while reviewing.

The `trusted` zone accepts incoming traffic on the private switch-facing `enp3s0`; verify that this interface connects only to intended cluster nodes. Runtime `public` showed `enp2s0`, while permanent `public` showed no explicitly bound interface; this can be explained by NetworkManager/default-zone assignments and does not alone prove a persistence fault.

## Warewulf and Munge

- `warewulf:secure: false` was recorded on the admin. This is an observed deployment setting, **not** a recommendation. Runtime overlay security deserves review, especially with a site-defined `rootkey` overlay.
- The Munge key was not published and its live distribution mechanism was not verified. Never commit any key bytes, private SSH key, or unsanitized overlay dump.
- Warewulf lists `dsa` among configured SSH host key types; legacy algorithms merit review, but the observed list is not proof that DSA keys were generated or actually used.
- NFS `/home` effective exports use `root_squash`; `/opt` is `ro,no_root_squash` to the private subnet. Review the latter policy.
- Slurm cgroup `ConstrainCores=no` and `ConstrainRAMSpace=no`; for a multi-user cluster, CPU/RAM containment should be assessed before relying on resource isolation guarantees.

## Risk register

| Priority | Item | Suggested *review*, not an automated fix |
|---|---|---|
| High | Cluster services in campus-facing public zone | School IT to review scope, ingress sources and necessity |
| High | Runtime overlay server `secure:false` with `rootkey` assigned | Review exposure, provisioning compatibility and controlled migration options |
| Medium | No cgroup CPU/RAM containment flags | Assess overcommit behavior and safe testing plan |
| Medium | NFS `/opt` `no_root_squash` | Confirm requirement and assess alternative with supervisor |
| Medium | No demonstrated reboot/failover test | Schedule supervised maintenance validation |
| Medium | Unverified campus uplink/firewall persistence and Tailscale ACLs | Review with network administrator |

No evidence here establishes compromise, abuse, Internet exposure, or a failed running cluster. **No security change was performed.**

Official references: [Warewulf security](https://warewulf.org/docs/main/server/security.html) · [Warewulf config](https://warewulf.org/docs/main/reference/man5/warewulf.conf.html) · [Slurm cgroup settings](https://slurm.schedmd.com/cgroup.conf.html).
