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

import re


class Parameters:

    def __init__(self, data, response_body):
        self.data = data
        self.response_body = response_body.decode("utf-8")
        self.parameters = []

    def extract_parameters_from_body(self):
        params = list(set(
            [] +
            re.findall('[name|id|for]=["|\']([a-zA-Z0-9-_]+)["|\']', self.response_body) +
            re.findall('data-([a-zA-Z0-9-_]+)', self.response_body) +
            re.findall('const ([a-zA-Z0-9-_]+)', self.response_body) +
            re.findall('var ([a-zA-Z0-9-_]+)', self.response_body) +
            re.findall('let ([a-zA-Z0-9-_]+)', self.response_body) +
            re.findall('([a-zA-Z0-9-_]+) :', self.response_body) +
            re.findall('["|\']([a-zA-Z0-9-_]+)["|\']:', self.response_body) +
            re.findall('["|\']([a-zA-Z0-9-_]+)["|\'] :', self.response_body) +
            re.findall('\[([a-zA-Z0-9_]+)\]', self.response_body) +
            re.findall('\[["|\']([a-zA-Z0-9-_]+)["|\']\]', self.response_body) +
            re.findall('<script.*>[\n\r\s]+([a-zA-Z0-9-_]+)\.[a-zA-Z0-9-_]+', self.response_body) +
            re.findall('\.([a-zA-Z0-9-_]+)=', self.response_body)+
            re.findall('[a-zA-Z0-9_]+\.([a-zA-Z0-9_]+)', self.response_body) +
            re.findall('\.[a-zA-Z0-9_]+\.([a-zA-Z0-9_]+)', self.response_body) +
            re.findall('\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.([a-zA-Z0-9_]+)', self.response_body) +
            []
        ))
        params.sort()

        self.parameters = params
