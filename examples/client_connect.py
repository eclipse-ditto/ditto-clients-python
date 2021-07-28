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

import sys
import time

from ditto.client import Client
from ditto.model.feature import Feature
from ditto.model.namespaced_id import NamespacedID
from ditto.protocol.envelope import Envelope
from ditto.protocol.things.commands import Command


def connect_client_simple():
    def on_connect(cl: Client):
        print("connected!!!")

        # Test subscribe
        cl.subscribe(on_message)

    def on_disconnect(cl: Client):
        print("disconnected!!!")

    def on_message(req_id: str, message: Envelope):
        print(message.to_ditto_dict())

        # Test reply
        client.reply(req_id, message.with_status(204))

        # Test commands generation
        cmd = Command(NamespacedID().from_string("test.ns:test-name")).feature("MyFeature").modify(
            Feature().with_properties(x="y", z=1))
        envelope = cmd.envelope(correlation_id="test-cr-id", response_required=False, content_type="application/json")

        # Test send
        client.send(envelope)

        # Test unsubscribe
        client.unsubscribe(on_message)

    client = Client(on_connect=on_connect, on_disconnect=on_disconnect)
    client.connect("localhost")
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("finished")
            client.disconnect()
            sys.exit()


# Test basic client functionalities
connect_client_simple()
