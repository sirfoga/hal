#!/usr/bin/env python
# coding: utf-8

""" Functions to deal with matrices """

from sklearn.preprocessing import LabelEncoder


class Matrix:
    """Table of data"""

    def __init__(self, matrix):
        self.matrix = matrix

    def precision(self):
        """
        Calculates precision

        Returns: precision
        """
        true_pos = self.matrix[0][0]
        false_pos = self.matrix[1][0]

        try:
            return 1.0 * true_pos / (true_pos + false_pos)
        except:  # division by 0
            return 0

    def recall(self):
        """
        Calculates recall

        Returns: recall
        """
        true_pos = self.matrix[0][0]
        false_neg = self.matrix[0][1]

        try:
            return 1.0 * true_pos / (true_pos + false_neg)
        except:  # division by 0
            return 0

    def true_neg_rate(self):
        """
        Calculates true negative rate

        Returns: true negative rate
        """
        false_pos = self.matrix[1][0]
        true_neg = self.matrix[1][1]

        try:
            return 1.0 * true_neg / (true_neg + false_pos)
        except:  # division by 0
            return 0

    def accuracy(self):
        """
        Calculates accuracy

        Returns:
            accuracy
        """
        true_pos = self.matrix[0][0]
        false_pos = self.matrix[1][0]
        false_neg = self.matrix[0][1]
        true_neg = self.matrix[1][1]

        num = 1.0 * (true_pos + true_neg)
        den = true_pos + true_neg + false_pos + false_neg

        try:
            return num / den
        except:  # division by 0
            return 0

    def f1_score(self):
        """
        Calculates F1 score

        Returns: F1 score
        """
        m_pre = self.precision()
        rec = self.recall()

        try:
            return 2.0 / (1.0 / m_pre + 1.0 / rec)  # harmonic mean
        except:  # division by 0
            return 0

    def get_as_list(self):
        """
        List of all values in matrix

        Returns: list representation
        """
        return sum([
            row
            for row in self.matrix
        ], [])

    def encode(self):
        """
        Encodes matrix

        Returns: Encoder used
        """
        lb = LabelEncoder()  # encoder
        values = self.get_as_list()
        encoded = lb.fit_transform(values)  # long list of encoded
        n_columns = len(self.matrix[0])
        n_rows = len(self.matrix)

        self.matrix = [
            encoded[i: i + n_columns]
            for i in range(0, n_rows * n_columns, n_columns)
        ]

        return lb

    def decode(self, lb):
        """
        Decodes matrix

        Args:
          lb: Encoder used to encode matrix

        Returns: Decodes matrix
        """
        self.matrix = [
            lb.inverse_transform(row)
            for row in self.matrix
        ]

    @staticmethod
    def from_columns(columns):
        """
        Parses raw columns

        Args:
          columns:  atrix divided into columns

        Returns: Merge the columns to form a matrix
        """
        data = [
            [
                column[i]
                for i in range(len(column))
            ]
            for column in columns
        ]
        return Matrix(data)
