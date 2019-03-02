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

import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x\n")
    sys.exit(1)

import ssl
import queue
from inc.Config import *
from inc.preparation.PrepareBaseRequest import *
from inc.preparation.PrepareAttackRequest import *
from inc.worker.WorkOnBaseRequest import *
from inc.worker.WorkOnTestRequest import *

ssl._create_default_https_context = ssl._create_unverified_context


def main():
    config = Config()
    config.show_summary()

    base_tests = PrepareBaseRequest(config).tests

    print("{} Executing {} base requests...".format(
        Color.green("[ i ]"),
        len(base_tests)
    ))

    queue_base_requests = queue.Queue()
    threads = []

    host_params = {}

    for workerIterator in range(0, config.max_threads):
        print("{} Worker {} started...".format(
            Color.green("[ i ]"),
            workerIterator
        ))

        worker = WorkOnBaseRequest(config, queue_base_requests, workerIterator, host_params)

        worker.setDaemon(True)

        worker.start()

        threads.append(worker)

    for data in base_tests:
        queue_base_requests.put(data)

    for item in threads:
        item.join()

    print("{} Finished with {} base requests...".format(
        Color.green("[ i ]"),
        len(base_tests)
    ))

    if config.type_only_base_request:

        attack_base_tests = PrepareAttackRequest(config, host_params).tests

        queue_base_p_requests = queue.Queue()
        threads = []

        for workerIterator in range(0, config.max_threads):
            print("{} Worker {} started...".format(
                Color.green("[ i ]"),
                workerIterator
            ))

            worker = WorkOnTestRequest(config, queue_base_p_requests, workerIterator)

            worker.setDaemon(True)

            worker.start()

            threads.append(worker)

        for data in attack_base_tests:
            queue_base_p_requests.put(data)

        for item in threads:
            item.join()

    if config.type_only_base_request:
        print("{} Stopping because only base requests are allowed...".format(
            Color.red("[ i ]")
        ))

        sys.exit()
    print("{} Preparing finale attack requests...".format(
        Color.green("[ i ]")
    ))

    attack_requests = PrepareAttackRequest(config, host_params).tests

    print("{} Executing {} attacks/tests... could take a while!". format(
        Color.red("[ i ]"),
        len(attack_requests)
    ))
    queue_test_requests = queue.Queue()
    threads = []

    for workerIterator in range(0, config.max_threads):
        print("{} Worker {} started...".format(
            Color.green("[ i ]"),
            workerIterator
        ))

        worker = WorkOnTestRequest(config, queue_test_requests, workerIterator)

        worker.setDaemon(True)

        worker.start()

        threads.append(worker)

    for data in attack_requests:
        queue_test_requests.put(data)

    for item in threads:
        item.join()


if __name__ == "__main__":
    main()
