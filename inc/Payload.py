# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Damian Schwyrz
import hashlib
import urllib.parse


class Payload:

    def __init__(self):
        self.string = ""
        self.payload_information = {}

    def generate_get_string(self, parameters, test_char):

        for param in parameters:
            identifier = hashlib.md5(param.encode('utf-16be')).hexdigest()
            value = "{}{}{}".format(identifier[0:5], test_char, identifier[0:2])


            self.payload_information[param] = value

        string = []

        for data in self.payload_information:
            string.append("{}={}".format(data,  urllib.parse.quote_plus(self.payload_information[data])))

        self.string = "&".join(string)
