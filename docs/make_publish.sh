#!/usr/bin/env bash
# coding: utf_8

# Copyright 2016 Stefano Fogarollo
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


OUTPUT_FOLDER="epydoc/html/"
DOCS_FOLDER="docs/"
BUILD_FOLDER="build/"
COMMIT_MSG=$(git log -1 --pretty=%B)  # last commit message

echo "<<<<    CLEANING    >>>>"
rm -rf ${OUTPUT_FOLDER}  # clean
rm -rf ${BUILD_FOLDER}
mkdir ${BUILD_FOLDER}  # prepare build folder

echo "<<<<    GENERATING DOCS    >>>>"
epydoc --config epydoc/Epydoc_html  # make docs
mv ${OUTPUT_FOLDER}* ${BUILD_FOLDER}  # move to build folder

echo "<<<<    MOVING TO GH-PAGES    >>>>"
git checkout gh-pages  # change branch (to publish docs)
mv ${BUILD_FOLDER}* ../

rm -rf ${BUILD_FOLDER}  # clean

echo "<<<<    COMMITTING    >>>>"
git add --all
git commit -m "${COMMIT_MSG} (generated docs)"
git push origin gh-pages