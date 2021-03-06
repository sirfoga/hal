# -*- coding: utf-8 -*-

""" Sampling methods """

import abc

import numpy as np
import scipy.integrate as integrate


class Pdf:
    def __init__(self, f):
        self.f = f

    def sample(self, n):
        return [
            self.f() for _ in range(n)
        ]

    def antithetics(self, n):
        samples = self.sample(n)
        antithetics = [1 - sample for sample in samples]
        return antithetics

    def sample_with_antithetics(self, n):
        n_samples = int(n / 2)
        samples = self.sample(n_samples)
        antithetics = [1 - sample for sample in samples]
        return samples + antithetics

    @abc.abstractmethod
    def expected_value(self, limits):
        return 0

    @abc.abstractmethod
    def variance(self, limits):  # E(f²) - E²(f)
        return 0


class Pdf1D(Pdf):
    def expected_value(self, limits):
        a, b = limits
        val, _ = integrate.quad(self.f, a, b)
        return val

    def variance(self, limits):
        def f_squared(x):
            return np.power(self.f(x), 2)

        expected_val = Pdf1D(self.f).expected_value(limits)  # can abstract this formula?
        expected_squared_val = Pdf1D(f_squared).expected_value(limits)
        return expected_squared_val - np.power(expected_val, 2)


class Pdf2D(Pdf):
    def expected_value(self, limits):
        x_min, x_max = limits[0]  # x-limit
        y_min, y_max = limits[1]  # y-limit
        val, _ = integrate.dblquad(self.f, x_min, x_max, lambda x: y_min, lambda x: y_max)
        return val

    def variance(self, limits):
        def f_squared(y, x):
            return np.power(self.f(y, x), 2)

        expected_val = Pdf2D(self.f).expected_value(limits)
        expected_squared_val = Pdf2D(f_squared).expected_value(limits)
        return expected_squared_val - np.power(expected_val, 2)
