import sys, time
from decimal import Decimal, getcontext

def chudnovsky_pi(digits):
    getcontext().prec = digits + 20
    C = 426880 * Decimal(10005).sqrt()
    M = 1
    L = 13591409
    X = 1
    K = 6
    S = Decimal(L)
    for i in range(1, digits // 14 + 1):
        M = (M * (K**3 - 16*K)) // (i**3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    return C / S

if __name__ == "__main__":
    n = int(sys.argv[1])
    t = time.time()
    s = str(chudnovsky_pi(n))[:n + 2]
    secs = time.time() - t
    with open(f"pi_{n}.txt", "w") as f:
        f.write(s + "\n")
    ok = s[:52] == "3.14159265358979323846264338327950288419716939937510"
    print(f"digits={n} time={secs:.1f}s first50_correct={ok}")
