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

import configparser
import os
import sys
from inc.Color import *
from inc.Clean import *


class Config:

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('app-settings.conf')

        self.__set_set_config()

        self.__get_urls()
        self.__get_cookies()
        self.__get_http_headers()
        self.__get_parameters()

    def __set_set_config(self):

        # Default settings
        self.http_timeout = int(self.config["default"]["HTTPTimeout"])
        self.max_threads = int(self.config["default"]["MaxThreads"])

        # Attack methods
        self.type_get = self.config.getboolean("types", "UseGet")
        self.type_post = self.config.getboolean("types", "UsePost")
        self.type_only_base_request = self.config.getboolean("types", "OnlyBaseRequest")
        self.chunk_size_get = int(self.config["type-settings"]["GetChunkSize"])
        self.chunk_size_post = int(self.config["type-settings"]["PostChunkSize"])
        self.test_single_quote = self.config.getboolean("type-settings", "SingleQuoteTest")
        self.test_double_quote = self.config.getboolean("type-settings", "DoubleQuoteTest")
        self.test_bigger_sign = self.config.getboolean("type-settings", "BiggerSignTest")
        self.extended_mode = self.config.getboolean("type-settings", "ExtendedMode")
        # Tunneling
        self.tunneling = self.config.getboolean("tunneling", "Active")
        self.tunnel = self.config["tunneling"]["Tunnel"]

        # Log
        self.log_folder = self.config["files"]["Logs"]

    def __get_cookies(self):

        file = self.config["files"]["Cookies"]

        if not os.path.exists(file):
            sys.exit("Cookie jar not found")

        cookies = open(file, "r").read().splitlines()

        cookies = ";".join([cookie.rstrip() for cookie in cookies if cookie.strip()])

        self.cookies = cookies

    def __get_parameters(self):

        file = self.config["files"]["Parameters"]

        if not os.path.exists(file):
            sys.exit("Param list not found")

        parameters = open(file, "r").read().splitlines()

        if len(parameters) == 0:
            sys.exit("Param list seems to be empty")

        parameters = [param.rstrip() for param in parameters if param.strip()]

        self.parameters = parameters

    def __get_http_headers(self):

        file = self.config["files"]["HttpHeaders"]

        if not os.path.exists(file):
            sys.exit("Header list not found")

        headers = open(file, "r").read().splitlines()

        headers = "\n".join([header.rstrip() for header in headers if header.strip()])

        if len(headers) == 0:
            sys.exit("Header list seems to be empty")

        self.headers = headers

    def __get_urls(self):

        file = self.config["files"]["Urls"]

        if not os.path.exists(file):
            sys.exit("Url list not found")

        urls = open(file, "r").read().splitlines()

        relevant_urls = []

        for url in urls:
            if url.startswith("#") or url.startswith(";"):
                continue

            relevant_urls.append(url.strip())

        if len(relevant_urls) == 0:
            sys.exit("Url list seems to be empty!")

        self.original_url_count = len(relevant_urls)

        url_cleaner = Clean(relevant_urls)
        url_cleaner.clean()
        self.urls = url_cleaner.cleaned_urls
        self.cleaned_url_count = len(self.urls)

    def show_summary(self):

        if self.type_only_base_request:
            print("{} Mode:\t\t\t{}".format(Color.red("[ ! ]"), "Only base preparation"))
        else:
            print("{} Mode:\t\t\t{}".format(Color.green("[ i ]"), "Default mode"))

        if self.type_get:
            print("{} GET:\t\t\t{} with chunk size of {}".format(Color.green("[ i ]"), "active",
                                                                 Color.green(self.chunk_size_get)))

        if self.type_post:
            print("{} POST:\t\t\t{} with chunk size of {}".format(Color.green("[ i ]"), "active",
                                                                  Color.green(self.chunk_size_post)))

        print("{} Threads:\t\t\t{}".format(Color.orange("[ i ]"), self.max_threads))
        print("{} HTTP Timeout:\t\t{}".format(Color.orange("[ i ]"), self.http_timeout))

        if self.tunneling:
            print("{} Proxy server:\t\t{}".format(
                Color.orange("[ i ]"),
                self.tunnel
            ))

        if self.cookies.strip() != "":
            print("{} Cookies used:\t\t{}".format(Color.orange("[ i ]"), self.cookies.strip()))

        if self.headers.strip() != "":
            print("{} Added headers:\t\t{}".format(
                Color.orange("[ i ]"),
                ", ".join([header for header in self.headers.splitlines()])
            ))

        print("{} Initial url count:\t{}".format(
            Color.orange("[ i ]"),
            self.original_url_count
        ))

        print("{} Cleaned url count:\t{}".format(
            Color.orange("[ i ]"),
            self.cleaned_url_count
        ))
