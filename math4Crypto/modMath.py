import random
import math

# ----------------------------
# GCD (Greatest Common Divisor)
# ----------------------------
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


# ----------------------------
# Extended Euclidean Algorithm
# returns (g, x, y) such that ax + by = g = gcd(a, b)
# ----------------------------
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


# ----------------------------
# Modular inverse (helper)
# ----------------------------
def modInv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


# ----------------------------
# Modular sqrt (using Tonelli Shanks)
# ----------------------------
def modSqrt(a, p):
    # Solve x^2 ≡ a (mod p), p prime
    if a == 0:
        return 0

    # Check if solution exists: a^((p-1)//2) ≡ 1 (mod p)
    if pow(a, (p - 1) // 2, p) != 1:
        return None

    # Case p ≡ 3 mod 4 (fast path)
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Factor p-1 = q * 2^s with q odd
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # Find quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 1:
        i = 1
        temp = pow(t, 2, p)
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1

        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p

    return r


# ----------------------------
# Legendre symbol (a | p), p prime
# ----------------------------
def legendre_symbol(a, p):
    a %= p
    if a == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


# ----------------------------
# Quadratic residue test (mod p, p prime)
# ----------------------------
def is_quadratic_residue(a, p):
    return legendre_symbol(a, p) != -1


# ----------------------------
# Jacobi symbol (a | n), n odd positive integer
# ----------------------------
def jacobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")

    a %= n
    result = 1

    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result

        a, n = n, a  # quadratic reciprocity
        if a % 4 == 3 and n % 4 == 3:
            result = -result

        a %= n

    return result if n == 1 else 0


# ----------------------------
# Chinese Remainder Theorem (CRT)
# x ≡ a_i (mod n_i), assuming n_i pairwise coprime
# ----------------------------
def crt(remainders, moduli):
    if len(remainders) != len(moduli):
        raise ValueError("lists must have same length")

    N = 1
    for n in moduli:
        N *= n

    x = 0

    for a_i, n_i in zip(remainders, moduli):
        N_i = N // n_i
        inv = modInv(N_i, n_i)
        if inv is None:
            raise ValueError("moduli must be coprime")
        x += a_i * N_i * inv

    return x % N


# ----------------------------
# Montgomery Reduction
# Computes: a * r^-1 mod n (internal reduction step)
# Requires: n odd, R = 2^k > n, gcd(R, n) = 1
# ----------------------------
def montgomery_reduce(T, n, n_inv, R):
    m = ((T & (R - 1)) * n_inv) & (R - 1)
    t = (T + m * n) >> (R.bit_length() - 1)
    if t >= n:
        t -= n
    return t


# ----------------------------
# Barrett Reduction
# Computes a mod n efficiently using precomputed mu
# ----------------------------
def barrett_precompute(n):
    k = n.bit_length()
    mu = (1 << (2 * k)) // n
    return mu


def barrett_reduce(a, n, mu):
    k = n.bit_length()
    q = (a * mu) >> (2 * k)
    r = a - q * n
    while r >= n:
        r -= n
    while r < 0:
        r += n
    return r


# ----------------------------
# Fermat Primality Test
# ----------------------------
def fermat_primality_test(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True


# ----------------------------
# Miller–Rabin Primality Test
# ----------------------------
def miller_rabin(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

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


# ----------------------------
# Euler's Totient Function φ(n)
# ----------------------------
def euler_totient(n):
    result = n
    i = 2

    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1

    if n > 1:
        result -= result // n

    return result


# ----------------------------
# Carmichael Function λ(n)
# ----------------------------
def carmichael_lambda(n):
    def lcm(a, b):
        return a // math.gcd(a, b) * b

    def prime_powers(n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i == 0:
                count = 0
                while n % i == 0:
                    n //= i
                    count += 1
                factors.append((i, count))
            i += 1
        if n > 1:
            factors.append((n, 1))
        return factors

    def lambda_prime_power(p, k):
        if p == 2 and k >= 3:
            return 2 ** (k - 2)
        return (p - 1) * (p ** (k - 1))

    factors = prime_powers(n)

    lam = 1
    for p, k in factors:
        lam = lcm(lam, lambda_prime_power(p, k))

    return lam