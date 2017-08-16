# !/usr/bin/python
# coding: utf_8

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


""" Tests files handling methods in hal """

import os
from functools import partial
from unittest import TestCase, main

from hal.files import models
from hal.tests import utils


class TestFileSystemPaths(TestCase):
    """ Tests hal.files.models.FileSystem path handlers """

    def test_fix_raw_path(self):
        """
        :return: bool
            True iff FileSystem.fix_raw_path correctly handles raw paths
        """

        tests = {
            "//a/b/c": "/a/b/c",  # double separators
            "/a/b/c.txt": "/a/b/c.txt"  # files
        }
        utils.battery_test(
            self.assertEqual, tests, models.FileSystem.fix_raw_path
        )

    def test_remove_year(self):
        """
        :return: bool
            True iff FileSystem.remove_year correctly removes years from paths
        """

        tests = {
            "Today is 1980": "Today is ",
            # year in start, middle, end position of sentence
            "Today 1980 is ": "Today  is ",
            "1980 Today is ": " Today is ",
            "19803": "3",  # composition of year
            "20012002": ""
        }
        utils.battery_test(
            self.assertEqual, tests, models.FileSystem.remove_year
        )

    def test_remove_brackets(self):
        """
        :return: bool
            True iff FileSystem.remove_bracket correctly removes brackets
            from paths
        """

        tests = {
            "(": "",  # void
            "((": "",
            "()": "",
            "([)([{}": "",
            "a(": "a",  # mixed with words
            "(a]": "",
            "}{a{b": "ab",
            "a(b[c{d}])": "a"  # with words in between
        }
        utils.battery_test(self.assertEqual, tests,
                           models.FileSystem.remove_brackets)

    def test_extract_name_max_chars(self):
        """
        :return: bool
            True iff FileSystem.extract_name_max_chars correctly extracts
            name from paths
        """

        tests = {
            "012345678a": "012345678a",  # length
            "012345678b ": "012345678b",
            "012345678c  ": "012345678c",
            " 012345678d": "012345678d",
            "  012345678e": "012345678e",
            "012345678912345678f": "0123456789"  # remove
        }
        utils.battery_test(
            self.assertEqual,
            tests,
            partial(models.FileSystem.extract_name_max_chars, max_chars=10)
        )

    def test_prettify(self):
        """
        :return: bool
            True iff FileSystem.prettify correctly prettifies bad strings
        """

        bad_string = "".join(models.BAD_CHARS)
        tests = {
            bad_string: "",
            bad_string + bad_string: "",
            bad_string + "a good string" + bad_string: "a_good_string"
        }
        utils.battery_test(self.assertEqual, tests, partial(
            models.FileSystem.prettify, r="_"))


class Test(TestCase):
    """ Tests hal.files.models.FileSystem folders/files functions """

    def __init__(self):
        TestCase.__init__(self)

        # create folder structure, at the end it will be like
        # working_folder/
        #             file1
        #             file2
        #             hidden_file
        #             inner_folder/
        #                         file11
        #                         file12
        self.working_folder = utils.random_name()
        self.file1 = os.path.join(
            self.working_folder,
            utils.random_name()
        )
        self.file2 = os.path.join(
            self.working_folder,
            utils.random_name()
        )
        self.hidden_file = os.path.join(
            self.working_folder,
            "." + utils.random_name()  # hidden requires dot before
        )
        self.inner_folder = os.path.join(
            self.working_folder,
            utils.random_name()
        )
        self.file11 = os.path.join(
            self.inner_folder,
            utils.random_name()
        )
        self.file12 = os.path.join(
            self.inner_folder,
            utils.random_name()
        )
        self.create_test_files()

    def create_test_files(self):
        """
        :return: void
            Creates files/folders structure for tests
        """

        os.makedirs(self.working_folder)  # create folders
        os.makedirs(self.inner_folder)
        for file in [self.file1, self.file2, self.hidden_file, self.file11,
                     self.file12]:
            open(file, "a").close()  # create files

    def test_ls_dir(self):
        """
        :return: bool
            True iff FileSystem.ls_dir correctly list only folders
        """

        tests = {
            self.working_folder: [self.file1, self.file2, self.inner_folder],
            self.inner_folder: [self.file11, self.file12]
        }
        utils.battery_test(self.assertEqual, tests,
                           models.FileSystem.ls_dir)

    def test_ls_recurse(self):
        """
        :return: bool
            True iff FileSystem.ls_recurse correctly list recursively
        """

        tests = {
            self.working_folder: [self.file1, self.file2, self.inner_folder,
                                  self.file11, self.file12]
        }
        utils.battery_test(self.assertEqual, tests,
                           models.FileSystem.ls_recurse)


if __name__ == '__main__':
    main()
