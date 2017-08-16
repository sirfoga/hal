#!/usr/bin/env python
# coding: utf-8

# Copyright 2017 Stefano Fogarollo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" Prediction methods based on classification algorithms. """

from sklearn import naive_bayes
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, \
    AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def extra_trees_classifier():
    """
    :return: sklearn ExtraTreesClassifier
        Classical extra tree classifier
    """

    return ExtraTreesClassifier(n_estimators=10, max_depth=None,
                                min_samples_split=1, random_state=0)


def random_forest():
    """
    :return: sklearn RandomForestClassifier
        Classical random forest classifier
    """

    return RandomForestClassifier(n_estimators=10, max_depth=None,
                                  min_samples_split=1, random_state=0)


def knn():
    """
    :return: sklearn KNN
        Classical knn
    """

    return KNeighborsClassifier(n_neighbors=3, leaf_size=125)


def ada_boost():
    """
    :return: sklearn AdaBoostClassifier
        Classical Ada boost
    """

    return AdaBoostClassifier(DecisionTreeClassifier(max_depth=20),
                              algorithm="SAMME.R", n_estimators=20)


def bayes_gauss():
    """
    :return: sklearn GaussianNB
        Slower than svr but equally accurate
    """

    return naive_bayes.GaussianNB()


def bayes_bernoulli():
    """
    :return: sklearn BernoulliNB
        Bayes-Bernoulli model
    """

    return naive_bayes.BernoulliNB()
