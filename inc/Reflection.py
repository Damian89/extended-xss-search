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

from inc.Color import *


class Reflection:

    def __init__(self, attack_data, response_body, config):
        self.config = config
        self.data = attack_data
        self.body = response_body.decode("utf-8", "ignore")
        self.found = ""

    def log(self):
        if self.found != "":
            file = "{}{}.txt".format(self.config.log_folder, self.data["host"])
            f = open(file, "a")
            f.write(self.found)
            f.close()

    def log500(self, status):

        if status == 500:

            self.found = "Error {} {}\n".format(
                self.data["method"],
                self.data["url"]
            )
            if self.data["method"] == "POST":
                self.found = "{}\n\nPayload: {}\n\n".format(self.found, self.data["body"])
            if self.data["method"] == "GET":
                self.found = "{}\n\nPayload: {}\n\n".format(self.found, self.data["path"])

            file = "{}500-{}.txt".format(self.config.log_folder, self.data["host"])
            f = open(file, "a")
            f.write(self.found)
            # f.close()

    def analyze(self):

        for paramdata in self.data["payload_information"]:
            search_value = original_search_value = self.data["payload_information"][paramdata]
            test_char = self.data["test_char"]

            if '\\' in original_search_value:
                search_value = original_search_value.replace('\\', '\\\\')
                test_char = test_char.replace('\\', '')

            value_of_finding = 0

            if search_value not in self.body:
                continue

            value_of_finding = 0.5

            prepend_search_value = "{}{}".format(test_char, search_value)

            if prepend_search_value in self.body:
                value_of_finding = value_of_finding + 0.25

            append_search_value = "{}{}".format(search_value, test_char)

            if append_search_value in self.body:
                value_of_finding = value_of_finding + 0.25

            print(
                "\n{} [{}] Found parameter [{}] with reflection [{}] using payload [{}] [certainty: {}]".format(
                    Color.danger("[ ! ]"),
                    self.data["method"],
                    paramdata,
                    search_value,
                    original_search_value,
                    Color.green("{} %".format(int(value_of_finding * 100)))
                )
            )

            print("{} Payloaded url: {}?{}={}\n".format(
                Color.red("[ - ]"),
                self.data["url"],
                paramdata,
                original_search_value
            ))

            self.set_found_string(paramdata, search_value, value_of_finding)

    def set_found_string(self, paramdata, search_value, value_of_finding):
        self.found = self.found + "Found with value {} %: [{}] [{}={}]\nURL: {}".format(
            int(100 * value_of_finding),
            self.data["method"],
            paramdata,
            search_value,
            self.data["url"]
        )
        if self.data["method"] == "POST":
            self.found = "{}\n\nPayload: {}\n\n".format(self.found, self.data["body"])
        if self.data["method"] == "GET":
            self.found = "{}\n\nPayload: {}\n\n".format(self.found, self.data["path"])
