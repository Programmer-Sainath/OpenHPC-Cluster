import numpy as np
import matplotlib.pyplot as plt
from scipy.special import assoc_laguerre, sph_harm_y
import math

def hydrogen_probability_density(n, l, m, X, Y, Z, a0=1.0):

    r = np.sqrt(X**2 + Y**2 + Z**2)


    theta = np.arccos(Z / r)

    phi = np.arctan2(Y, X)

    rho = ( 2.0 / ( n * a0 ) ) * r

    L = assoc_laguerre(rho, n-l-1, 2*l+1)

    norm_radial = np.sqrt(
        ( 2.0 / ( n*a0 ) )**3 * math.factorial( n-l-1 ) / ( 2.0 * n * math.factorial( n+l ) )
    )

    R = norm_radial * np.exp(-rho/2) * rho**l * L

    Ylm = sph_harm_y(l, m, theta, phi)

    psi = R * Ylm

    return np.abs(psi) ** 2


# 3D grid
N = 19000000
lim = 25
n, l, m = 4, 3, 0

r = np.random.exponential(scale=n**2, size=N)
theta = np.arccos(1 - 2*np.random.rand(N))
phi = 2*np.pi*np.random.rand(N)

X = r * np.sin(theta) * np.cos(phi)
Y = r * np.sin(theta) * np.sin(phi)
Z = r * np.cos(theta)


for i in range(1):
    P = hydrogen_probability_density(n, l, m, X, Y, Z)

    # Keep only high-density points
    threshold = np.percentile(P, 99.5)
    print(threshold, np.max(P))

    mask = P > threshold

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(
        X[mask],
        Y[mask],
        Z[mask],
        c=np.log10(P[mask]),
        s=1,
        cmap='inferno'
    )

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(f'3D Hydrogen Orbital (n={n}, l={l}, m={m})')

    plt.show()
    m+=1


