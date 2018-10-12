# -*- coding: utf-8 -*-

"""Primes functions """

import random

LOW_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
              103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
              167, 173, 179, 181, 191, 193, 197, 199,
              211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
              277, 281, 283, 293, 307, 311, 313, 317,
              331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
              401, 409, 419, 421, 431, 433, 439, 443,
              449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521,
              523, 541, 547, 557, 563, 569, 571, 577,
              587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
              653, 659, 661, 673, 677, 683, 691, 701,
              709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
              797, 809, 811, 821, 823, 827, 829, 839,
              853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
              937, 941, 947, 953, 967, 971, 977, 983,
              991, 997]  # primes until 1000


class Integer:
    """Big int std python won't recognize"""

    def __init__(self, string):
        self.to_int = int(string)
        self.to_string = string

    def is_naive_prime(self):
        """Checks if prime in very naive way
        :return: True iff prime
        """
        if self.to_int < 2:
            return False
        elif self.to_int % 2 == 0:
            return False

        return self.to_int in LOW_PRIMES

    def is_probably_prime(self):
        """Tests with miller-rabin
        :return: True iff prime
        """

        if self.is_naive_prime():
            return True

        # check if multiple pf low primes
        for prime in LOW_PRIMES:
            if self.to_int % prime == 0:
                return False

        # if all else fails, call rabin to determine if to_int is prime
        return self.test_miller_rabin(5)

    def test_miller_rabin(self, precision):
        """Tests prime with miller-rabin algorithm

        :param precision: number of rounds to perform
        :return: True iff probably prime
        """

        if not self.is_naive_prime():
            if precision < 0:
                raise ValueError('precision must be positive')

            # true -> probably prime
            # false -> composite

            # write n = d*2^s, d odd
            s = self.to_int - 1
            t = 0
            while s % 2 == 0:
                s /= 2
                t += 1

            # let a = random in the range 2, n-1
            # v = a^d mod n
            # if v = +-1 mod n:
            #     repeat this s-1 times:
            #     v = v^2 mod n
            #     if v = 1 -> composite
            # -> prime
            for _ in range(precision):
                a = random.randrange(2, self.to_int - 1)
                v = pow(int(a), int(s), self.to_int)
                if v != 1:
                    i = 0
                    while v != (self.to_int - 1):
                        if i == t - 1:
                            return False
                        else:
                            i += 1
                            v = (v ** 2) % self.to_int
            return True

        return True


def get_prime(bits):
    """Creates (probable) prime number of given size

    :param bits: size of number to generate
    :return: prime number of given size
    """
    if bits < 0:
        raise ValueError('\'bits\' field cannot be negative')
    while True:
        num = random.randrange(2 ** (bits - 1), 2 ** bits)
        if Integer(str(num)).is_probably_prime():
            return num


def blum_blum_shub(seed, amount, prime0, prime1):
    """Creates pseudo-number generator

    :param seed: seeder
    :param amount: amount of number to generate
    :param prime0: one prime number
    :param prime1: the second prime number
    :return: pseudo-number generator
    """
    assert amount >= 0  # amount cannot be negative
    if amount == 0:
        return []

    assert (seed > 0 and
            prime0 > 0 and prime1 > 0)  # seed and primes cannot be negative
    assert (prime0 % 4 == 3 and
            prime1 % 4 == 3)  # primes must be congruent 3 mod 4

    mod = prime0 * prime1
    rand = [seed]

    for _ in range(amount):
        last_num = rand[len(rand) - 1]
        next_num = (last_num * last_num) % mod
        rand.append(next_num)

    return rand
