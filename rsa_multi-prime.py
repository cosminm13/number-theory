from Crypto.Util import number
import random
from math import gcd
from sympy import mod_inverse
from functools import reduce
from modint import ChineseRemainderConstructor, chinese_remainder
# from sympy.ntheory.modular import crt


def modular_inverse(a, p):
    return (a ** (p - 2)) % p

def setKeys():
    # p = number.getPrime(8)
    p = 173
    # q = number.getPrime(8)
    q = 167
    # r = number.getPrime(8)
    r = 251
    n = p * q * r

    def generate_e(n):
        e = random.randrange(1, n - 1)
        if gcd(n, e) != 1:
            generate_e(n)
        return e

    # e = generate_e(n)
    e = 3

    public_key = (n, e)

    phi = (p - 1) * (q - 1) * (r - 1)

    # d = modular_inverse(e, phi)
    d = mod_inverse(e, phi)

    private_key = d

    primes = (p, q, r)

    return public_key, private_key, primes


def encrypt_message(m, pubK):
    return pow(m, pubK[1], pubK[0])  # m ** e % n

def decrypt_message_classic(m, prK, pubK):
    return pow(m, prK, pubK[0])  # m ** d % n


# https://crypto.stackexchange.com/questions/2575/chinese-remainder-theorem-and-rsa
def decrypt_message_crt(m, prK, pubK, primes):
    p = primes[0]
    q = primes[1]
    r = primes[2]
    d = prK
    n = pubK[0]
    e = pubK[1]

    m1 = ((m % p) ** (d % (p - 1))) % p
    m2 = ((m % q) ** (d % (q - 1))) % q
    m3 = ((m % r) ** (d % (r - 1))) % r

    return solve_crt([p, q, r], [m1, m2, m3])


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


if __name__ == '__main__':
    public_key, private_key, primes = setKeys()
    message = 1234

    print(f"Original message: {message}")
    print(f"Public key: {public_key}, Private key: {private_key}, Primes: {primes}")
    encrypted_message = encrypt_message(message, public_key)
    print(f"Encrypted message: {encrypted_message}")
    decrypted_message = decrypt_message_classic(encrypted_message, private_key, public_key)
    print(f"Decrypted message: {decrypted_message}")
    decrypted_message_crt = decrypt_message_crt(encrypted_message, private_key, public_key, primes)
    print(f"Decrypted message with CRT: {decrypted_message_crt}")
