# Copyright (c) 2021 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0

import threading


class _RWLock:
    def __init__(self):
        """
        Initializes read-write lock, using the default Python lock from "threading" module.
        """
        self._read_condition = threading.Condition(threading.Lock())
        self._readers = 0

    def lock_read(self):
        """
        Locks the thread for reading.
        """
        self._read_condition.acquire()
        try:
            self._readers += 1
        finally:
            self._read_condition.release()

    def unlock_read(self):
        """
        Unlocks the thread for reading.
        """
        self._read_condition.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_condition.notifyAll()
        finally:
            self._read_condition.release()

    def lock_write(self):
        """
        Locks the thread for writing.
        """
        self._read_condition.acquire()
        while self._readers > 0:
            self._read_condition.wait()

    def unlock_write(self):
        """
        Unlocks the thread for writing.
        """
        self._read_condition.release()
