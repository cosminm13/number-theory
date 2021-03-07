from Crypto.Util import number
import random
from math import gcd
from sympy import mod_inverse
from functools import reduce
from modint import chinese_remainder

def modular_inverse(a, p):
    return (a ** (p - 2)) % p

def setKeys():
    # p = number.getPrime(8)
    p = 251
    p_square = p ** 2
    # q = number.getPrime(8)
    q = 197

    n = p * p * q

    def generate_e(n):
        e = random.randrange(1, n - 1)
        if gcd(n, e) != 1:
            generate_e(n)
        return e

    # e = generate_e(n)
    e = 3

    public_key = (n, e)

    phi = (p_square - p) * (q - 1)

    # d = modular_inverse(e, phi)
    d = mod_inverse(e, phi)

    private_key = d

    primes = (p, q)

    return public_key, private_key, primes


def encrypt_message(m, pubK):
    return pow(m, pubK[1], pubK[0])  # m ** e % n

def decrypt_message_classic(m, prK, pubK):
    return pow(m, prK, pubK[0])  # m ** d % n

# https://crypto.stackexchange.com/questions/2575/chinese-remainder-theorem-and-rsa
# http://www.ijircce.com/upload/2017/march/335_Design_n.pdf
def decrypt_message_crt(m, prK, pubK, primes):
    p = primes[0]
    p_square = p ** 2
    q = primes[1]
    d = prK
    n = pubK[0]
    e = pubK[1]

    # Garner
    # https://www.di-mgt.com.au/crt_rsa.html
    dP = mod_inverse(e, p - 1)
    dQ = mod_inverse(e, q - 1)
    qInv = mod_inverse(q, p_square)
    m1 = pow(m, dP, p)
    m2 = pow(m, dQ, q)
    h = (qInv * (m1 - m2)) % p
    m = m2 + h * q
    return m


# https://www.geeksforgeeks.org/using-chinese-remainder-theorem-combine-modular-equations/
def solve_crt(m, x):
    while True:
        temp_m = mod_inverse(m[1], m[0]) * x[0] * m[1] + mod_inverse(m[0], m[1]) * x[1] * m[0]
        temp2_m = m[0] * m[1]

        x.remove(x[0])
        x.remove(x[0])
        x = [temp_m % temp2_m] + x

        m.remove(m[0])
        m.remove(m[0])
        m = [temp2_m] + m

        if len(x) == 1:
            break

    return x[0]


def decrypt_message_hensel(m, prK, pubK, primes):
    p = primes[0]
    p_square = p ** 2
    q = primes[1]
    d = prK
    n = pubK[0]
    e = pubK[1]

    # Hensel
    # https://hovav.net/ucsd/dist/survey.pdf
    # https://gdeepak.com/pubs/Improvement%20over%20Public%20Key%20Cryptographic%20algorithm.pdf
    # https://math.stackexchange.com/questions/2040200/algorithm-for-hensels-lifting
    r1 = mod_inverse(d, p - 1)
    r2 = mod_inverse(d, q - 1)
    m1 = pow(m, r1, p)
    m2 = pow(m, r2, q)
    # m1p = pow(m, r1, p)
    m1p = (m % p) ** (1 // e)

    return solve_crt([p, q], [m1p, m2])


if __name__ == '__main__':
    public_key, private_key, primes = setKeys()
    message = 12346

    print(f"Original message: {message}")
    print(f"Public key: {public_key}, Private key: {private_key}, Primes: {primes}")
    encrypted_message = encrypt_message(message, public_key)
    print(f"Encrypted message: {encrypted_message}")
    decrypted_message = decrypt_message_classic(encrypted_message, private_key, public_key)
    print(f"Decrypted message: {decrypted_message}")
    decrypted_message_crt = decrypt_message_crt(encrypted_message, private_key, public_key, primes)
    print(f"Decrypted message CRT: {decrypted_message_crt}")
    decrypted_message_hensel = decrypt_message_hensel(encrypted_message, private_key, public_key, primes)
    print(f"Decrypted message Hensel: {decrypted_message_hensel}")