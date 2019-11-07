#!/usr/bin/env python
# coding: utf-8


import abc

from hal.maths.la.matrix import LinearSystemMatrix

DEFAULT_TOLL = 1e-16


class LinearSystemSolver:
    def __init__(self, A, b):
        self.A = LinearSystemMatrix(A) if not isinstance(A, LinearSystemMatrix) else A
        self.b = LinearSystemMatrix(b) if not isinstance(b, LinearSystemMatrix) else b
        self.b = self.b.transpose()  # column vector

        self.x = None

    @staticmethod
    def get_error(x, x_real):
        return (x - x_real).linear_norm()

    def check(self, x, x_real, abs_toll, rel_toll):
        if x is None:
            return False

        if x_real is None:
            return False

        diff = self.get_error(x, x_real)
        return diff < (x_real * rel_toll).linear_norm() + abs_toll

    def get_solution(self):
        return self.x

    def check_solution(self, abs_toll=DEFAULT_TOLL, rel_toll=0):
        return self.check(self.A * self.x, self.b, abs_toll, rel_toll)

    def get_solution_error(self):
        return self.get_error(self.A * self.x, self.b)


class IterativeLinearSystemSolver(LinearSystemSolver):
    def set_tolls(self, abs_toll, rel_toll):
        self.abs_toll = abs_toll
        self.rel_toll = rel_toll

    @abc.abstractmethod
    def solve(self, x, abs_toll, rel_toll):
        self.x = LinearSystemMatrix(x).transpose() if not isinstance(x, LinearSystemMatrix) else x
        self.set_tolls(abs_toll, rel_toll)

    def is_toll_enough(self, x_new, x):
        return self.check(x_new, x, self.abs_toll, self.rel_toll)


class PureIterativeLinearSystemSolver(IterativeLinearSystemSolver):
    @abc.abstractmethod
    def iteration(self, x):
        pass

    def solve(self, x, abs_toll, rel_toll):
        super().solve(x, abs_toll, rel_toll)
        x = self.x

        enough_toll = False
        it_counter = 0

        while not enough_toll:
            x_new = self.iteration(x)
            enough_toll = self.is_toll_enough(x_new, x)

            it_counter += 1
            x = x_new

        self.x = x
        return it_counter


class DLUIterativeLinearSystemSolver(IterativeLinearSystemSolver):
    @abc.abstractmethod
    def iteration(self, x, D, L, U):
        pass

    def solve(self, x, abs_toll, rel_toll):
        super().solve(x, abs_toll, rel_toll)
        x = self.x

        D, L, U = self.A.dlu_decompose()
        enough_toll = False
        it_counter = 0

        while not enough_toll:
            x_new = self.iteration(x, D, L, U)
            enough_toll = self.is_toll_enough(x_new, x)

            it_counter += 1
            x = x_new

        self.x = x
        return it_counter


class JacobiSolver(DLUIterativeLinearSystemSolver):
    def iteration(self, x, D, L, U):
        S = (L + U) * -1
        x_new = D.inverse() * ((S * x) + self.b)
        return x_new


class GaussSiedelSolver(DLUIterativeLinearSystemSolver):
    def iteration(self, x, D, L, U):
        a = (D + L).inverse()
        x_new = (a * -1 * U * x) + (a * self.b)
        return x_new


class SORSolver(DLUIterativeLinearSystemSolver):
    def __init__(self, A, b, w):
        super().__init__(A, b)

        self.w = w

    def iteration(self, x, D, L, U):
        a = (D + L * self.w).inverse()
        T_sor = a * (U * (-self.w) + D * (1 - self.w))
        C_sor = a * self.w
        x_new = T_sor * x + C_sor * self.b
        return x_new

    # todo good choice for w


class GradientMethodSolver(PureIterativeLinearSystemSolver):
    def __init__(self, A, b, step_size):
        super().__init__(A, b)

        self.step_size = step_size

    def iteration(self, x):
        return x - (self.A * x + self.b) * self.step_size


class ConjugateGradientMethodSolver(PureIterativeLinearSystemSolver):
    pass  # todo
