import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
from scipy.special import assoc_laguerre, sph_harm_y
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n, l = 4,3
m = -3
a0 = 1.0
N = 200000
local_N = N // size
for i in range(l+1):
    r = np.random.exponential(scale=n**2, size=local_N)
    theta = np.arccos(1 - 2*np.random.rand(local_N))
    phi = 2 * np.pi * np.random.rand(local_N)

    X = r * np.sin(theta) * np.cos(phi)
    Y = r * np.sin(theta) * np.sin(phi)
    Z = r * np.cos(theta)

    def hydrogen_probability_density(n, l, m, X, Y, Z, a0=1.0):

        r = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
        theta = np.arccos(np.clip(Z / r, -1, 1))
        phi = np.arctan2(Y, X)

        rho = (2.0 / (n * a0)) * r

        L = assoc_laguerre(rho, n - l - 1, 2 * l + 1)

        norm_radial = np.sqrt(
            (2.0 / (n * a0))**3 *
            math.factorial(n - l - 1) /
            (2.0 * n * math.factorial(n + l))
        )

        R = norm_radial * np.exp(-rho / 2) * rho**l * L
        Ylm = sph_harm_y(l, m, theta, phi)

        psi = R * Ylm
        return np.abs(psi) ** 2

    P = hydrogen_probability_density(n, l, m, X, Y, Z)

    mask = P > 1e-3 * P.max()

    local_points = np.column_stack([X[mask], Y[mask], Z[mask], P[mask]])

    all_points = comm.gather(local_points, root=0)

    if rank == 0:

        all_points = np.vstack(all_points)

        Xp = all_points[:, 0]
        Yp = all_points[:, 1]
        Zp = all_points[:, 2]
        Cp = np.log10(all_points[:, 3] + 1e-20)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(Xp, Yp, Zp, c=Cp, s=1, cmap='inferno')

        ax.set_title(f"Hydrogen Orbital n={n}, l={l}, m={m}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        plt.show()
    m+=1