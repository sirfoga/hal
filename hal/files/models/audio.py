# !/usr/bin/python3
# coding: utf-8

# Copyright 2016-2018 Stefano Fogarollo
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


""" Songs in various formats """

from mutagen.id3 import ID3
from mutagen.id3._frames import TIT2, TPE1, TALB, TRCK, TDRC, TCON
from mutagen.mp3 import MP3

from hal.files.models.system import FileSystem


class MP3Song(FileSystem):
    """ mp3 song """

    def __init__(self, path):
        """
        :param path: str
            Location of .mp3 file
        """

        FileSystem.__init__(self, path)

        self.song = MP3(self.path, ID3=ID3)
        self.tags = self.song.tags

    def set_name(self, name):
        """
        :param name: str
            Song's title
        :return: void
            Sets song's title
        """

        self.tags.add(TIT2(encoding=3, text=name.decode('utf-8')))
        self.song.save()

    def set_artist(self, artist):
        """
        :param artist: str
            Song's artist
        :return: void
            Sets song's artist
        """

        self.tags.add(TPE1(encoding=3, text=artist.decode('utf-8')))
        self.song.save()

    def set_album(self, album):
        """
        :param album: str
            Song's album
        :return: void
            Sets song's albu
        """

        self.tags.add(TALB(encoding=3, text=album.decode('utf-8')))
        self.song.save()

    def set_nr_track(self, nr_track):
        """
        :param nr_track: int
            Number of track
        :return: void
            Sets song's track number
        """

        self.tags.add(TRCK(encoding=3, text=str(nr_track)))
        self.song.save()

    def set_year(self, year):
        """
        :param year: int
            Year of song
        :return: void
            Sets song's year
        """

        self.tags.add(TDRC(encoding=3, text=str(year)))
        self.song.save()

    def set_genre(self, genre):
        """
        :param genre: str
            Genre of song
        :return: void
            Sets song's genre
        """

        self.tags.add(TCON(encoding=3, text=str(genre)))
        self.song.save()