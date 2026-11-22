from mpi4py import MPI
import numpy as np
from scipy.special import assoc_laguerre
try:
    from scipy.special import sph_harm_y
    def orbital_harmonic(l, m, polar, azimuth):
        return sph_harm_y(l, m, polar, azimuth)
except ImportError:
    # SciPy 1.13 on the recorded Rocky Linux cluster uses the legacy argument order.
    from scipy.special import sph_harm
    def orbital_harmonic(l, m, polar, azimuth):
        return sph_harm(m, l, azimuth, polar)

import math
from skimage import measure

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# parameters
N = 80
lim = 25

n, l, m = 4, 3, -3

# global grid
x = np.linspace(-lim, lim, N)
y = np.linspace(-lim, lim, N)
z = np.linspace(-lim, lim, N)

# split x-axis
x_chunks = np.array_split(np.arange(N), size)
local_x = x[x_chunks[rank]]

# local grid only
X, Y, Z = np.meshgrid(local_x, y, z, indexing='ij')
# wavefunction
def psi2(n, l, m, X, Y, Z, a0=1.0):

    r = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
    theta = np.arccos(np.clip(Z / r, -1, 1))
    phi = np.arctan2(Y, X)

    rho = (2.0 / (n * a0)) * r

    L = assoc_laguerre(rho, n - l - 1, 2 * l + 1)

    norm = np.sqrt(
        (2.0 / (n * a0))**3 *
        math.factorial(n - l - 1) /
        (2.0 * n * math.factorial(n + l))
    )

    R = norm * np.exp(-rho / 2) * rho**l * L
    Ylm = orbital_harmonic(l, m, theta, phi)

    return np.abs(R * Ylm) ** 2

# local computation
P_local = psi2(n, l, m, X, Y, Z)

# gather FULL volume (MPI step)
P_full = comm.gather(P_local, root=0)

# root builds isosurface
if rank == 0:

    P = np.concatenate(P_full, axis=0)

    # normalize
    P = P / P.max()

    # marching cubes
    level = 0.1

    verts, faces, normals, values = measure.marching_cubes(P, level=level)

    # map voxel → physical space
    verts = verts * (2 * lim / (N - 1)) - lim

    # plot
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_trisurf(
        verts[:, 0],
        verts[:, 1],
        faces,
        verts[:, 2],
        cmap='inferno',
        lw=0.2
    )

    ax.set_title(f"Hydrogen Orbital (n={n}, l={l}, m={m})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    fig.savefig(f"orbital_isosurface_n{n}_l{l}_m{m}.png", dpi=150)
    plt.close(fig)