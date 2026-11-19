import sys, time, math, random, socket, resource
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
hosts = comm.allgather(socket.gethostname())
node_names = sorted(set(hosts))

# published values: N -> (pi(N), largest prime <= N)
KNOWN = {10**6: (78498, 999983), 10**7: (664579, 9999991), 10**8: (5761455, 99999989),
         10**9: (50847534, 999999937), 10**10: (455052511, 9999999967),
         10**11: (4118054813, 99999999977), 10**12: (37607912018, 999999999989)}
BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)   # deterministic below 3.3e24

def is_prime(n):
    if n < 2:
        return False
    for p in BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def odd_base_primes(limit):
    s = np.ones(limit + 1, dtype=np.uint8)
    s[:2] = 0
    for i in range(2, math.isqrt(limit) + 1):
        if s[i]:
            s[i * i::i] = 0
    return [int(p) for p in np.flatnonzero(s) if p % 2 == 1]

def gib(x):
    return x / 1024.0 ** 3

if __name__ == "__main__":
    N = int(float(sys.argv[1]))
    M = (N + 1) // 2                       # odd numbers 1, 3, ..., <= N  (index i <-> 2i+1)
    i0 = rank * M // size
    i1 = (rank + 1) * M // size
    n_local = i1 - i0
    lo_num = 2 * i0 + 1
    bp = odd_base_primes(math.isqrt(N))

    comm.Barrier()
    t0 = time.perf_counter()
    arr = np.ones(n_local, dtype=np.uint8)  # the whole slice lives in RAM
    if i0 == 0:
        arr[0] = 0                          # 1 is not prime
    t1 = time.perf_counter()
    for p in bp:                            # mark odd multiples of p, starting at p*p
        k = max(p, -(-lo_num // p))
        if k % 2 == 0:
            k += 1
        j = (p * k - 1) // 2 - i0
        if j < n_local:
            arr[j::p] = 0
    t2 = time.perf_counter()
    cnt = int(np.count_nonzero(arr))
    t3 = time.perf_counter()
    comm.Barrier()
    wall = time.perf_counter() - t0

    last_local, last50 = 0, []
    if rank == size - 1:
        tail = arr[-1000000:] if n_local > 1000000 else arr
        nz = np.flatnonzero(tail)
        off = n_local - len(tail)
        if len(nz):
            last_local = 2 * (i0 + off + int(nz[-1])) + 1
            last50 = [2 * (i0 + off + int(x)) + 1 for x in nz[-50:]]
    last = comm.allreduce(last_local, op=MPI.MAX)
    last50 = comm.bcast(last50 if rank == size - 1 else None, root=size - 1)

    rng = random.Random(777 + rank)         # spot check against deterministic Miller-Rabin
    idx = rng.sample(range(n_local), min(20000, n_local)) + list(range(max(0, n_local - 2000), n_local))
    bad = 0
    for j in idx:
        if (arr[j] == 1) != is_prime(2 * (i0 + j) + 1):
            bad += 1
    checked = len(idx)

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    res = comm.gather((rank, hosts[rank], t1 - t0, t2 - t1, t3 - t2, cnt, n_local, arr.nbytes, rss, checked, bad), root=0)

    if rank == 0:
        pi = 1 + sum(r[5] for r in res)     # + the prime 2
        bad_t = sum(r[10] for r in res)
        chk_t = sum(r[9] for r in res)
        ref = KNOWN.get(N)
        ok = bad_t == 0 and (ref is None or (pi == ref[0] and last == ref[1]))
        verdict = ("yes (reference + spot-check)" if ref else "yes (spot-check only)") if ok else "NO"
        tot = [r[2] + r[3] + r[4] for r in res]
        per_node = ", ".join("%s %.1f" % (h, max(tot[i] for i in range(size) if hosts[i] == h)) for h in node_names)
        arr_gib = gib(sum(r[7] for r in res))
        rss_sum = sum(r[8] for r in res)
        rss_max = max(r[8] for r in res)
        for r in res:
            print("RANK | %s | %d ranks | %d | %s | %s | %.1f | %.1f | %.1f | %s |" % (
                format(N, ","), size, r[0], r[1], format(r[6], ","), r[2], r[3], r[4], format(r[5], ",")), flush=True)
        print("ROW | %s | %d | %d | %s | %s | %s | %s | %s | %d | %s |" % (
            format(N, ","), size, len(node_names), format(pi, ","),
            format(ref[0], ",") if ref else "n/a", format(last, ","),
            format(ref[1], ",") if ref else "n/a", format(chk_t, ","), bad_t, verdict), flush=True)
        print("TIME | %s | %d | %d | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %s | %.2f | %.2f | %.2f | %s | %.3f |" % (
            format(N, ","), size, len(node_names), max(r[2] for r in res), max(r[3] for r in res),
            max(r[4] for r in res), wall, max(tot), min(tot), per_node, arr_gib, rss_sum, rss_max,
            "yes" if arr_gib > 16 else "no", size * wall / 3600.0), flush=True)
        fn = "sieve_N%d_%dranks.txt" % (N, size)
        with open(fn, "w") as f:
            f.write("Distributed sieve of Eratosthenes (odd numbers only, one uint8 flag per odd number held in RAM)\n")
            f.write("N = %s   MPI ranks: %d on %d node(s)   Wall time: %.1f s\n" % (format(N, ","), size, len(node_names), wall))
            f.write("pi(N) = %s   Largest prime <= N: %s   Correct: %s\n" % (format(pi, ","), format(last, ","), verdict))
            f.write("----------------------------------------------------------------\n")
            f.write("Slice of each rank (index of odd numbers) and the primes found in it:\n")
            for r in res:
                f.write("rank %2d  %-8s  %s odd numbers  %s primes  %.1f s\n" % (
                    r[0], r[1], format(r[6], ","), format(r[5], ","), r[2] + r[3] + r[4]))
            f.write("----------------------------------------------------------------\n")
            f.write("The last 50 primes <= N:\n")
            for a in range(0, len(last50), 5):
                f.write("  ".join(str(x) for x in last50[a:a + 5]) + "\n")
        print("saved=" + fn, flush=True)
