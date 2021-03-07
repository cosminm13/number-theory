# https://en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test
# https://en.wikipedia.org/wiki/Mersenne_prime
def lucasLehmer(n, s):
    if n <= 1:
        return 'composite'
    if n <= 3:
        return 'prime'
    if n % 2 == 0:
        return 'composite'
    for i in range(3, int(n ** (1 / 2) + 1), 2):
        if n % i == 0:
            return 'composite'
    u = 4
    for k in range(1, s - 1):
        u = (u ** 2 - 2) % n
    if u == 0:
        return 'prime'
    return 'composite'


def generate_number(n):
    return pow(2, n) - 1


if __name__ == '__main__':
    for i in range(0, 10):
        print(f"Number {generate_number(i)} is {lucasLehmer(generate_number(i), i)}")