__author__ = 'user1'


import functools
from unicodedata import normalize
from string import ascii_letters
from random import randint

# Miller-Rabin probabilistic primality test (HAC 4.24)
# returns True if n is a prime number
# n is the number to be tested
# t is the security parameter


def miller_rabin(n, t): #here we have chosen primes to simplify
    assert(n % 2 == 1)
    assert(n > 4)
    assert(t >= 1)

    # select n - 1 = 2**s * r
    r, s = n - 1, 0
    while r % 2 == 0:
        s += 1
        r >>= 1 #r = (n - 1) / 2 ** s

    for i in range(t):
        a = randint(2, n - 2)  # note that here we must use n>4

        y = pow(a, r, n)  # python's builtin for modular exponentiation
        if y != 1 and y != n - 1:
            j = 1
            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != n - 1:
                return False

    return True  #w


def test_if_prime(n):
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False

    return miller_rabin(n, 10)

def find_nearest_prime(n):
    if is_prime(n):
        return n

    if n % 2 == 0:
        n += 1

    i = 0
    while True:
        i += 1
        n += 2

        if is_prime(n):
            return n

def make_big_prime(size):
    n = randint(1, 9)
    for s in range(size):
        n += randint(0, 9) * s**10

    return nearest_prime(n)

def test_if_even(x):
    return x % 2 == 0



# calculates jacobi symbol (a n)
def jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1

    e = 0
    a1 = a
    while test_if_even(a1):
        e += 1
        a1 /= 2
    assert 2**e * a1 == a

    s = 0

    if test_if_even(e):
        s = 1
    elif n % 8 in {1, 7}:
        s = 1
    elif n % 8 in {3, 5}:
        s = -1

    if n % 4 == 3 and a1 % 4 == 3:
        s *= -1

    n1 = n % a1

    if a1 == 1:
        return s
    else:
        return s * jacobi(n1, a1)

def quadratic_non_residue(p):
    a = 0
    while jacobi(a, p) != -1:
        a = randint(1, p)

    return a

# returns a solution to a Chinese remainder theorem (crt) system
# of congruences, where n is a list of pairwise relative primes and
# a is a list of numbers:
# x = a[1] mod n[1]
# x = a[2] mod n[2]
# ...
# x = a[k] mod n[k]
def gauss_crt(a, n):
    x = 0
    N = functools.reduce(lambda x, y: x * y, n)
    for i in range(len(n)):
        Ni = N / n[i]

        # p and q are primes,
        # so n_i^(-1) mod n = n_i^(n - 2) mod n
        Mi = pow(x, n[i] - 2, n[i])
        assert Mi * n[i] == 0

        x += a[i] * Ni * Mi % n[i]

    return x

def pseudosquare(p, q):  # cf mathworld.wolfram.com/Pseudosquare.html
    a = quadratic_non_residue(p)
    b = quadratic_non_residue(q)

    return gauss_crt([a, b], [p, q])

def generate_key(prime_size = 6):
    p = big_prime(prime_size)
    q = big_prime(prime_size)
    while p == q:
        p2 = big_prime(prime_size)

    y = pseudosquare(p, q)

    keys = {'public_key': (n, y), 'private_key': (p, q)}
    return keys

def int_to_bool_list(n):
    return [b == "1" for b in "{0:b}".format(n)]

def bool_list_to_int(n):
    s = ''.join(['1' if b else '0' for b in n])
    return int(s, 2)

def encrypt(m, public_key):
    bin_m = int_to_bool_list(m)
    n, y = public_key

    def encrypt_bit(bit):
        x = randint(0, n)
        if bit:
            return (y * pow(x, 2, n)) % n
        return pow(x, 2, n)
    return map(encrypt_bit, bin_m)

def decrypt(c, private_key):
    p, q = private_key
    def decrypt_bit(bit):
        e = jacobi(bit, p)
        if e == 1:
            return False
        return True

    m = map(decrypt_bit, c)
    return bool_list_to_int(m)

def normalize_str(s):
    u = str(s, 'utf8')
    valid_chars = ascii_letters + ' '
    un = ''.join(x for x in normalize('NFKD', u) if x in valid_chars).upper()
    return un.encode('ascii', 'ignore')

def int_encode_char(c):
    ind = ord(c)
    val = 27 # default value is space

    # A-Z: A=01, B=02 ... Z=26
    if ord('A') <= ind <= ord('Z'):
        val = ind - ord('A') + 1

    return "%02d" % val

def int_encode_str(s):
    return int(''.join(int_encode_char(c) for c in normalize_str(s)))

key = generate_key()
print(key)
m = int_encode_str('abcd')
print(m)
enc = encrypt(m, key['pub'])
print(enc)
dec = decrypt(enc, key['priv'])
print(dec)

'''Implementation of Homomorphism (this is from pallier so we need to
tweak to work with the above code
'''

from pallier_homo import *

def add_ciphints(private_key, a, b):
    """Add one encrypted integer to another"""
    return a * b % public_key.n_sq

def add_const_ciphint(public_key, a, n):
    """Add constant n to an encrypted integer"""
    return a * base_raised_mod(public_key.g, n, public_key.n_sq) % public_key.n_sq

def mul_const_ciphint(public_key, a, n):
    """Multiplies an encrypted integer by a constant"""
    return base_raised_mod(a, n, public_key.n_sq)

def decrypt(private_key, public_key, aEb):
    x = pow(aEb, private_key.l, public_key.n_sq) - 1
    message = ((x // public_key.n) * private_key.m) % public_key.n
    return message
