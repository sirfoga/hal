#!/usr/bin/env python
# coding: utf-8

"""Functions to deal with matrices"""

from sklearn.preprocessing import LabelEncoder

from hal.maths.utils import divide


class Matrix:
    """Table of data"""

    def __init__(self, matrix):
        self.matrix = matrix

    def precision(self):
        """Calculates precision

        :return: Precision of matrix
        """
        true_pos = self.matrix[0][0]
        false_pos = self.matrix[1][0]
        return divide(1.0 * true_pos, true_pos + false_pos)

    def recall(self):
        """Calculates recall

        :return: Recall
        """
        true_pos = self.matrix[0][0]
        false_neg = self.matrix[0][1]
        return divide(1.0 * true_pos, true_pos + false_neg)

    def true_neg_rate(self):
        """Calculates true negative rate

        :return: true negative rate
        """
        false_pos = self.matrix[1][0]
        true_neg = self.matrix[1][1]
        return divide(1.0 * true_neg, true_neg + false_pos)

    def accuracy(self):
        """Calculates accuracy

        :return: Accuracy
        """
        true_pos = self.matrix[0][0]
        false_pos = self.matrix[1][0]
        false_neg = self.matrix[0][1]
        true_neg = self.matrix[1][1]

        num = 1.0 * (true_pos + true_neg)
        den = true_pos + true_neg + false_pos + false_neg

        return divide(num, den)

    def f1_score(self):
        """Calculates F1 score

        :return: F1 score
        """
        m_pre = self.precision()
        rec = self.recall()
        return divide(2.0, 1.0 / m_pre + 1.0 / rec)  # harmonic mean

    def get_as_list(self):
        """List of all values in matrix

        :return: list representation
        """
        return sum([
            row
            for row in self.matrix
        ], [])

    def encode(self):
        """Encodes matrix

        :return: Encoder used
        """
        encoder = LabelEncoder()  # encoder
        values = self.get_as_list()
        encoded = encoder.fit_transform(values)  # long list of encoded
        n_columns = len(self.matrix[0])
        n_rows = len(self.matrix)

        self.matrix = [
            encoded[i: i + n_columns]
            for i in range(0, n_rows * n_columns, n_columns)
        ]

        return encoder

    def decode(self, encoder):
        """Decodes matrix

        :param encoder: Encoder used to encode matrix
        :return: list: Decodes matrix
        """
        self.matrix = [
            encoder.inverse_transform(row)
            for row in self.matrix
        ]

    def get_column(self, index):
        """Gets column at given index

        :param index: index of column
        :return: Column
        """

        return [
            row[index]
            for row in self.matrix
        ]

    @staticmethod
    def from_columns(columns):
        """Parses raw columns

        :param columns: matrix divided into columns
        :return: Matrix: Merge the columns to form a matrix
        """
        data = [
            [
                column[i]
                for i in range(len(column))
            ]
            for column in columns
        ]
        return Matrix(data)
