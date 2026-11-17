import sys, time, math, socket, resource
import numpy as np
from mpi4py import MPI
from scipy.special import assoc_laguerre
try:
    from scipy.special import sph_harm_y
    def Ylm(l, m, polar, azim):
        return sph_harm_y(l, m, polar, azim)
except ImportError:
    from scipy.special import sph_harm
    def Ylm(l, m, polar, azim):
        return sph_harm(m, l, azim, polar)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n, l, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
N = int(float(sys.argv[4]))
keep = float(sys.argv[5]) if len(sys.argv) > 5 else 0.001
a0 = 1.0
local_N = N // size
Ntot = local_N * size
s = float(n * n)

def density(n, l, m, r, theta, phi):
    rho = (2.0 / (n * a0)) * r
    norm_radial = math.sqrt((2.0 / (n * a0))**3 * math.factorial(n - l - 1)
                            / (2.0 * n * math.factorial(n + l)))
    R = norm_radial * np.exp(-rho / 2) * rho**l * assoc_laguerre(rho, n - l - 1, 2 * l + 1)
    psi = R * Ylm(l, m, theta, phi)
    return psi.real**2 + psi.imag**2

comm.Barrier()
t0 = time.time()
rng = np.random.default_rng([42, rank])
r = rng.exponential(scale=s, size=local_N)
theta = np.arccos(1.0 - 2.0 * rng.random(local_N))
phi = 2.0 * np.pi * rng.random(local_N)
t1 = time.time()
P = density(n, l, m, r, theta, phi)
t2 = time.time()

# importance-sampling check: sampling density in r is exp(-r/s)/s
w = P * r
w *= r
w *= np.exp(r / s)
w *= 4.0 * np.pi * s
S0 = float(w.sum()); S1 = float((w * r).sum()); S2 = float((w * w).sum())
S0, S1, S2 = comm.allreduce(S0), comm.allreduce(S1), comm.allreduce(S2)
del w
norm = S0 / Ntot
rmean = S1 / Ntot
se = math.sqrt(max(S2 / Ntot - norm**2, 0.0) / Ntot)
r_exact = (3 * n * n - l * (l + 1)) / 2.0 * a0

thr = np.quantile(P, 1.0 - keep)
mask = P > thr
rk, tk, pk, Pk = r[mask], theta[mask], phi[mask], P[mask]
pts = np.column_stack([rk * np.sin(tk) * np.cos(pk), rk * np.sin(tk) * np.sin(pk), rk * np.cos(tk), Pk])
del r, theta, phi, P
allp = comm.gather(pts, root=0)
hosts = comm.gather(socket.gethostname(), root=0)
comm.Barrier()
t3 = time.time()

peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
peak_sum = comm.allreduce(peak)
peak_max = comm.allreduce(peak, op=MPI.MAX)
t_sample = comm.allreduce(t1 - t0, op=MPI.MAX)
t_dens = comm.allreduce(t2 - t1, op=MPI.MAX)
t_total = t3 - t0

if rank == 0:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pts = np.vstack(allp)
    kept = len(pts)
    if kept > 200000:
        pts = pts[rng.choice(kept, 200000, replace=False)]
    C = np.log10(pts[:, 3] + 1e-30)
    lim = np.abs(pts[:, :3]).max()
    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(131, projection="3d")
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=C, s=0.5, cmap="inferno")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax2 = fig.add_subplot(132)
    ax2.scatter(pts[:, 0], pts[:, 2], c=C, s=0.5, cmap="inferno")
    ax2.set_aspect("equal"); ax2.set_title("side view (x-z)")
    ax3 = fig.add_subplot(133)
    ax3.scatter(pts[:, 0], pts[:, 1], c=C, s=0.5, cmap="inferno")
    ax3.set_aspect("equal"); ax3.set_title("top view (x-y)")
    fig.suptitle(f"Hydrogen orbital n={n}, l={l}, m={m}  |  {Ntot:,} samples on {size} ranks")
    out = f"orbital_n{n}_l{l}_m{m}_N{Ntot}_{size}ranks.png"
    fig.savefig(out, dpi=130)
    counts = {h: hosts.count(h) for h in sorted(set(hosts))}
    print(f"ranks={size} hosts={counts}")
    print(f"saved={out} kept={kept}")
    print(f"ROW | ({n},{l},{m}) | {Ntot:,} | {size} | {t_sample:.1f} | {t_dens:.1f} | {t_total:.1f} | "
          f"{norm:.5f} +/- {se:.5f} | {rmean:.4f} ({r_exact:.4f}) | {peak_sum:.1f} | {peak_max:.2f} |")
