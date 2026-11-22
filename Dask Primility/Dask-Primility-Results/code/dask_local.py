import random, time, os, sys, socket, statistics, logging, warnings
from dask.distributed import Client, LocalCluster, as_completed

logging.getLogger("distributed").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# ---------------- repo code, unchanged ----------------
def miller_rabin(n, k):

    if n <= 1:
        return False

    if n < 4:
        return True

    if n % 2 == 0:
        return False

    r = 0
    d = n - 1

    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):

        a = random.randint(2, n - 2)

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True


BITSIZE = 1024
LOOPNUM = 20


def generate_prime_candidate():

    while True:

        p = random.getrandbits(BITSIZE)

        # force odd and force top bit
        p |= (1 << (BITSIZE - 1)) | 1

        start = time.perf_counter()
        miller_rabin(p, 20)
        elapsed = time.perf_counter() - start

        # keep candidates that take some work
        if elapsed > 0.01:
            return p


def findprime(loopnum):

    while True:
        a = generate_prime_candidate()
        if miller_rabin(a, loopnum):
            return a

        a -= 2
# ------------------------------------------------------

def search(loopnum):
    return findprime(loopnum), socket.gethostname()

def race(workers, pure):
    cluster = LocalCluster(n_workers=workers, threads_per_worker=1,
                           processes=True, dashboard_address=None)
    client = Client(cluster)
    try:
        client.wait_for_workers(workers)
        t0 = time.perf_counter()
        futures = [client.submit(search, LOOPNUM, pure=pure) for _ in range(workers)]
        for fut in as_completed(futures):
            prime, host = fut.result()
            break
        elapsed = time.perf_counter() - t0
        for f in futures:
            f.cancel()
    finally:
        client.close()
        cluster.close()
    return prime, host, elapsed

def check(p):
    return p.bit_length() == BITSIZE and pow(2, p - 1, p) == 1 and miller_rabin(p, 40)

if __name__ == "__main__":
    workers = int(sys.argv[1])
    trials = int(sys.argv[2])
    pure = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
    label = "original submit() behaviour (pure=True)" if pure else "pure=False"
    times = []
    with open(f"winners_w{workers}_pure{int(pure)}.txt", "a") as out:
        for i in range(1, trials + 1):
            prime, host, secs = race(workers, pure)
            ok = check(prime)
            if not ok:
                raise RuntimeError(f"Candidate verification failed: trial {i}, workers={workers}")
            times.append(secs)
            out.write(f"{workers} {i} {secs:.3f} {host} {prime}\n")
            print(f"workers={workers} trial={i} time={secs:.2f}s node={host} verified={ok}", flush=True)
    print(f"SUMMARY {label}: workers={workers} trials={trials} "
          f"mean={statistics.mean(times):.2f}s median={statistics.median(times):.2f}s "
          f"min={min(times):.2f}s max={max(times):.2f}s", flush=True)
