## Strong scaling: same problem, 1 / 4 / 16 ranks

| Orbital (n,l,m) | Samples | Ranks | Sampling (s) | Density (s) | Total compute (s) | Norm (exact 1) | <r> estimated (exact) | Peak memory, sum of ranks (GB) | Peak memory, largest rank (GB) |
|:---|---:|---:|---:|---:|---:|:---|:---|---:|---:|
| (4,3,-3) | 25,000,000 | 1 | 1.1 | 7.1 | 9.1 | 0.99990 +/- 0.00034 | 18.0001 (18.0000) | 1.7 | 1.74 |
| (4,3,-3) | 25,000,000 | 4 | 0.4 | 2.2 | 3.1 | 1.00031 +/- 0.00034 | 18.0069 (18.0000) | 1.9 | 0.48 |
| (4,3,-3) | 25,000,000 | 16 | 0.1 | 0.5 | 0.8 | 1.00051 +/- 0.00034 | 18.0125 (18.0000) | 2.7 | 0.17 |

## Large runs: 200,000,000 samples on 16 ranks (4 nodes)

| Orbital (n,l,m) | Samples | Ranks | Sampling (s) | Density (s) | Total compute (s) | Norm (exact 1) | <r> estimated (exact) | Peak memory, sum of ranks (GB) | Peak memory, largest rank (GB) |
|:---|---:|---:|---:|---:|---:|:---|:---|---:|---:|
| (4,3,-3) | 200,000,000 | 16 | 0.7 | 4.4 | 6.1 | 0.99985 +/- 0.00012 | 17.9986 (18.0000) | 14.4 | 0.90 |
| (3,2,0) | 200,000,000 | 16 | 0.7 | 2.4 | 4.2 | 0.99999 +/- 0.00013 | 10.5005 (10.5000) | 14.4 | 0.90 |
| (4,3,0) | 200,000,000 | 16 | 0.7 | 3.1 | 4.9 | 0.99995 +/- 0.00015 | 18.0001 (18.0000) | 14.4 | 0.90 |

Norm = integral of |psi|^2 over all space, estimated by importance sampling (should be 1).
Exact <r> for hydrogen = (3n^2 - l(l+1))/2 Bohr radii.
Peak memory is the resident-memory high-water mark per MPI rank; the sum also counts the Python/NumPy overhead of every rank.
