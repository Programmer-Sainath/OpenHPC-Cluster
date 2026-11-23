# Munge authentication — historical configuration

Munge provides local authentication used by Slurm services. On 2026-11-23, `munge` was active on the admin and all four compute nodes. The compute-node Slurm configuration checksum and account identifiers also matched the admin system. **The live mechanism that places the Munge key into the nodes was not verified.**

- `munge.conf` records **commented historical shell commands**, not a live setup script.
- `munge.key.example` contains a warning, **not** a real key.
- No real `/etc/munge/munge.key` or secret-bearing overlay content belongs in a public Git repository.
- Do not regenerate the active key on a running cluster. Coordinate any key rotation with authorized administrators and a maintenance window.

See [Security](../docs/NETWORKING_AND_SECURITY.md) and [Configuration catalog](../docs/CONFIG_CATALOG.md).
