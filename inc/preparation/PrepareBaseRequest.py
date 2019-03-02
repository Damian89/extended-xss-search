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

from urllib.parse import urlparse
from inc.Headers import *


class PrepareBaseRequest:

    def __init__(self, config):
        self.config = config
        self.tests = []

        self.__create_request_data()

    def __create_request_data(self):

        for attacked_site in self.config.urls:
            url = self.__make_url(attacked_site)
            path = self.__get_path_and_query(url)
            hostname = self.__get_host(url)
            port = self.__get_port(url)

            self.__add_test(url, hostname, port, path)

    def __add_test(self, url, hostname, port, path):

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_user_defined_headers()

        if self.config.cookies != "":
            headers.set("Cookie", self.config.cookies)

        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")

        self.tests.append({
            'url': url,
            'port': port,
            'method': 'GET',
            'host': hostname,
            'path': path,
            'headers': headers.make(),
            'body': '',
        })

    @staticmethod
    def __make_url(attacked_site):

        url = attacked_site

        if not attacked_site.startswith("http"):
            url = "http://{}/".format(attacked_site)

        return url

    @staticmethod
    def __get_path_and_query(url):

        parser = urlparse(url)

        path = parser.path

        query = parser.query

        if query == "" or query is None:
            return path

        return "{}?{}".format(path, query)

    @staticmethod
    def __get_host(url):

        parser = urlparse(url)

        return parser.hostname

    @staticmethod
    def __get_port(url):

        parser = urlparse(url)

        return parser.port
