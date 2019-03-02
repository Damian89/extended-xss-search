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

import threading
from inc.Color import *
from inc.Connection import Connection as OwnConnection
from inc.Reflection import *

stopSet = True


class WorkOnTestRequest(threading.Thread):

    def __init__(self, config, queue, tid):
        threading.Thread.__init__(self)

        self.config = config
        self.queue = queue
        self.tid = tid

    def run(self):

        global stopSet

        while stopSet:

            try:
                data = self.queue.get(timeout=1)
            except Exception as e:
                stopSet = False
                break

            try:
                conn = OwnConnection(self.config, data)
                conn.connect()
                response = conn.response
                response_body = conn.body

                state = self.__make_color_state(response)

                print("{} [Proc: {}] {} [{}]".format(
                    state,
                    self.tid,
                    data["url"],
                    response.status,
                ))

                reflection = Reflection(data, response_body, self.config)
                reflection.analyze()
                reflection.log()


            except Exception as e:
                print("{} [Proc: {}] {} [{}]".format(
                    Color.danger("[ x ]"),
                    self.tid,
                    data["url"],
                    e
                ))

            self.queue.task_done()

    @staticmethod
    def __make_color_state(response):
        if response.status == 200:
            state = Color.green("[ R ]")
        elif 200 < response.status <= 500:
            state = Color.orange("[ R ]")
        else:
            state = Color.red("[ R ]")
        return state
