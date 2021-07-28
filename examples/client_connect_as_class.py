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
from ditto.protocol.things.messages import Message


# import logging


class MyClient(Client):
    def on_connect(self, ditto_client: Client):
        print("Ditto client connected")
        self.subscribe(self.on_message)
        print("subscribed")

    def on_disconnect(self, ditto_client: Client):
        print("Ditto client disconnected")
        self.unsubscribe(self.on_message)
        print("unsubscribed")

    def on_message(self, request_id: str, message: Envelope):
        print("request_id: {}, envelope: {}".format(request_id, message.to_ditto_dict()))

        incoming_thing_id = NamespacedID(message.topic.namespace, message.topic.entity_id)

        # create an example outbox message and reply
        live_message = Message(incoming_thing_id).outbox("testCommand").with_payload(
            dict(a="b", x=2))
        # generate the respective Envelope
        response_envelope = live_message.envelope(correlation_id=message.headers.correlation_id, response_required=False).with_status(204)
        # send the reply
        self.reply(request_id, response_envelope)

        # create an an example feature and send
        # create the Feature instance
        feature_to_add = Feature().with_properties(x="y", z=1)
        # create the modify command with the feature as a Ditto payload
        cmd = Command(incoming_thing_id).feature("MyFeature").modify(feature_to_add)
        # generate the respective Envelope
        cmd_envelope = cmd.envelope(correlation_id="test-cr-id", response_required=False, content_type="application/json")
        # send the command
        self.send(cmd_envelope)

    def on_log(self, ditto_client: Client, level, string):
        print("[{}] {}".format(level, string))

    def run(self):
        # Using the default logger
        self.enable_logger(True)

        # optionally an external logger can also be provided
        # logging.basicConfig(level=logging.DEBUG)
        # logger = logging.getLogger(__name__)
        # self.enable_logger(True, logger)

        self.connect("localhost", 1883)
        while True:
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print("finished")
                self.disconnect()
                sys.exit()


ditto_client = MyClient()
ditto_client.run()
