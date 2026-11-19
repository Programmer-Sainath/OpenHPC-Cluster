import sys, time, random, socket, resource, textwrap
from mpi4py import MPI
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
hosts = comm.allgather(socket.gethostname())
node_names = sorted(set(hosts))

# ---------------- repo code, unchanged ----------------
def miller_rabin(n, k):
    if n <= 1:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
# ------------------------------------------------------

def parse(name):
    if name.startswith("M"):
        return (1 << int(name[1:])) - 1, True
    if name.startswith("C"):
        a, b = name[1:].split("x")
        return ((1 << int(a)) - 1) * ((1 << int(b)) - 1), False
    raise ValueError(name)

def run_mersenne(k, names):
    k_local = max(1, k // size)
    for name in names:
        n, expect = parse(name)
        comm.Barrier()
        t0 = time.perf_counter()
        ok = miller_rabin(n, k_local)
        t = time.perf_counter() - t0
        oks = comm.allgather(ok)
        ts = comm.allgather(t)
        comm.Barrier()
        wall = time.perf_counter() - t0
        verdict = all(oks)
        if rank == 0:
            per_node = ", ".join("%s %.1f" % (h, max(ts[i] for i in range(size) if hosts[i] == h)) for h in node_names)
            print("ROW | %s | %d | %s | %s | %s | %d | %d | %d | %.2f | %.2f | %.2f | %s |" % (
                name, n.bit_length(), "prime" if expect else "composite",
                "probably prime" if verdict else "composite",
                "yes" if verdict == expect else "NO", size, len(node_names),
                k_local * size, wall, max(ts), min(ts), per_node), flush=True)

SMALL = [p for p in range(3, 2000, 2) if all(p % q for q in range(3, int(p ** 0.5) + 1, 2))]

def run_search(bits, seconds):
    comm.Barrier()
    t0 = time.perf_counter()
    deadline = t0 + seconds
    found, tested = [], 0
    while time.perf_counter() < deadline:
        c = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if any(c % p == 0 for p in SMALL):
            continue
        tested += 1
        if miller_rabin(c, 20):
            found.append(c)
    t = time.perf_counter() - t0
    good = sum(1 for p in found if p.bit_length() == bits and pow(2, p - 1, p) == 1 and miller_rabin(p, 10))
    res = comm.gather((rank, hosts[rank], t, tested, len(found), good), root=0)
    allp = comm.gather(found, root=0)
    comm.Barrier()
    if rank == 0:
        wall = max(r[2] for r in res)
        tot_t = sum(r[3] for r in res)
        tot_f = sum(r[4] for r in res)
        tot_g = sum(r[5] for r in res)
        rate = tot_f / wall * 60.0
        per_node = ", ".join("%s %d" % (h, sum(r[4] for r in res if r[1] == h)) for h in node_names)
        for r in res:
            print("RANK | %d-bit search | %d ranks | %d | %s | %.1f | %d | %d |" % (bits, size, r[0], r[1], r[2], r[3], r[4]), flush=True)
        print("ROW | search %d-bit | %g s budget | %d | %d | %d | %d (%d verified) | %.1f | %.1f | %s |" % (
            bits, seconds, size, len(node_names), tot_t, tot_f, tot_g, wall, rate, per_node), flush=True)
        fn = "primes_%dbit_%dranks.txt" % (bits, size)
        with open(fn, "w") as f:
            f.write("Miller-Rabin prime search: %d-bit probable primes (repo miller_rabin, 20 rounds per candidate; each prime re-checked)\n" % bits)
            f.write("MPI ranks: %d on %d node(s)   Time budget: %g s   Wall time: %.1f s\n" % (size, len(node_names), seconds, wall))
            f.write("Primes found: %d (%d verified)   Rate: %.1f primes/min\n" % (tot_f, tot_g, rate))
            f.write("Digits wrapped at 100 characters per line.\n")
            f.write("----------------------------------------------------------------\n")
            for i, p in enumerate(sorted(x for ps in allp for x in ps), 1):
                f.write("Prime %d (%d bits):\n" % (i, p.bit_length()))
                f.write(textwrap.fill(str(p), 100) + "\n")
        print("saved=" + fn, flush=True)

if __name__ == "__main__":
    random.seed(1000003 * (rank + 1))
    mode = sys.argv[1]
    if mode == "mersenne":
        run_mersenne(int(sys.argv[2]), sys.argv[3].split(","))
    elif mode == "search":
        run_search(int(sys.argv[2]), float(sys.argv[3]))
    peak = comm.allreduce(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, op=MPI.MAX)
    if rank == 0:
        print("PEAKMEM | largest per-rank resident memory: %.0f MB" % peak, flush=True)
