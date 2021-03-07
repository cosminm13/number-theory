import random


# http://2000clicks.com/MathHelp/NumberTh27JacobiSymbolAlgorithm.aspx
def jacobi(a, b):
    if b <= 0 or b % 2 == 0:
        return 0
    j = 1
    if a < 0:
        a = -a
        if b % 4 == 3:
            j = -j
    while a != 0:
        while a % 2 == 0:
            a = a / 2
            if b % 8 == 3 or b % 8 == 5:
                j = -j
        aux = a
        a = b
        b = aux
        if a % 4 == 3 and b % 4 == 3:
            j = -j
        a = a % b
    if b == 1:
        return j
    else:
        return 0


def congruence(a, b, n):
    # a = b mod n
    if (a - b) % n == 0:
        return True
    return False


def jacobi2(a, n):
    # return 0 -> congruence(a, 0, n) == True
    # return 1 -> congruence(a, 0, n) == False and exists x s.t. congruence(a, x ** 2, n) == True
    # return -1 -> congruence(a, 0, n) == False and there is no x s.t. congruence(a, x ** 2, n) == True
    if a == 0:
        return 0
    if a == 1:
        return 1

    e = 0
    a1 = a
    s = 0
    while a1 % 2 == 0:
        e += 1
        a1 /= 2

    if e % 2 == 0:
        s = 1
    else:
        if congruence(n, 1, 8) is True or congruence(n, 7, 8) is True:
            s = 1
        if congruence(n, 3, 8) is True or congruence(n, 5, 8) is True:
            s = -1
    if congruence(n, 3, 4) is True and congruence(a1, 3, 4) is True:
        s = -s
    n1 = n % a1
    if a1 == 1:
        return s
    else:
        return s * jacobi2(n1, a1)


def solovayStrassen(n, t):
    for i in range(t):
        a = random.randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if (r != 1) and (r != n - 1):
            return 'composite'
        s = jacobi2(a, n)
        if r != (s % n):
            return 'composite'
    return 'prime'


if __name__ == '__main__':
    n = 127
    print(solovayStrassen(n, 80))
