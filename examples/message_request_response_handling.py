# Copyright (c) 2022 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0

import sys
import time

from ditto.client import Client
from ditto.model.namespaced_id import NamespacedID
from ditto.protocol.envelope import Envelope


def connect_client_with_request_response_handler():
    def on_connect(cl: Client):
        print("connected!!!")

        # Test subscribe
        cl.subscribe(on_message)

    def on_disconnect(cl: Client):
        print("disconnected!!!")

    def on_message(req_id: str, message: Envelope):
        print(message.to_ditto_dict())

        # Test reply
        # Response status can be changed depending on the topic of the recieved message or
        #  on the executed actions after recieven the resuest message
        client.reply(req_id, message.with_status(204))
       

    client = Client(on_connect=on_connect, on_disconnect=on_disconnect)
    client.connect("localhost")
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("finished")
            client.disconnect()
            sys.exit()


# Test client reques-response message handling
connect_client_with_request_response_handler()
