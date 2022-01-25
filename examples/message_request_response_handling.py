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
import json
import sys
import threading
import time

import paho.mqtt.client as mqtt
from ditto.client import Client
from ditto.model.namespaced_id import NamespacedID
from ditto.protocol.envelope import Envelope
from ditto.protocol.things.messages import Message
from ditto.model.feature import Feature
from ditto.model.definition_id import DefinitionID

thing_id = NamespacedID().from_string("test.ns:test-name")

feature_id = "MyFeatureID"
property_id = "myProperty"
definition_id = DefinitionID().from_string("my.model.namespace:FeatureModel:1.0.0")
my_feature = Feature().with_definition(definition_id).with_property(property_id, "myValue")
req_topic = "command///req/" + str(thing_id) + "/"
message_subject = "some-command"


def send_inbox_message():
    live_message = Message(thing_id).inbox(subject=message_subject).with_payload("some_payload")
    live_message_envelope = live_message.envelope(response_required=True)
    live_message_dict = live_message_envelope.to_ditto_dict()
    live_message_json = json.dumps(live_message_dict)
    # wait before sending the message to make sure the client's on connect has been executed
    time.sleep(5)
    paho_client.publish(topic=req_topic + message_subject, payload=live_message_json)


class MyClient(Client):
    def on_connect(self, ditto_client: Client):
        print("Ditto client connected")
        self.subscribe(self.on_message)
        print("subscribed")
        inbox_message_thread = threading.Thread(target=send_inbox_message)
        inbox_message_thread.start()

    def on_disconnect(self, ditto_client: Client):
        print("Ditto client disconnected")
        self.unsubscribe(self.on_message)
        print("unsubscribed")

    def on_message(self, request_id: str, message: Envelope):
        print("request_id: {}, envelope: {}".format(request_id, message.to_ditto_dict()))
        print(message.topic.__str__())
        incoming_thing_id = NamespacedID(message.topic.namespace, message.topic.entity_id)

        # create an example outbox message and reply
        live_message = Message(incoming_thing_id).outbox(message_subject).with_payload(
            dict(a="b", x=2))
        # generate the respective Envelope
        response_envelope = live_message.envelope(correlation_id=message.headers.correlation_id,
                                                  response_required=False).with_status(200)
        # send the reply
        self.reply(request_id, response_envelope)

    def on_log(self, ditto_client: Client, level, string):
        print("[{}] {}".format(level, string))


ditto_client: Client = None


def paho_on_connect(client, userdata, flags, rc):
    global ditto_client
    ditto_client = MyClient(paho_client=client)
    ditto_client.enable_logger(True)
    ditto_client.connect()


try:
    paho_client = mqtt.Client()
    paho_client.on_connect = paho_on_connect
    paho_client.connect("localhost")
    paho_client.loop_forever()
except KeyboardInterrupt:
    print("finished")
    ditto_client.disconnect()
    paho_client.disconnect()

    sys.exit()
