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

from ditto.model.namespaced_id import NamespacedID
from ditto.protocol.things.messages import Message

root_thing_namespace = "org.eclipse.ditto"
root_thing_name = "smartcoffee"
root_thing_id = NamespacedID(root_thing_namespace, root_thing_name)
message_to_thing = {
    "topic": "org.eclipse.ditto/smartcoffee/things/live/messages/ask",
    "headers": {
        "content-type": "text/plain",
        "correlation-id": "a-unique-string-for-this-message"
    },
    "path": "/inbox/messages/ask",
    "value": "Hey, how are you?"
}

message_to_feature = {
    "topic": "org.eclipse.ditto/smartcoffee/things/live/messages/heatUp",
    "headers": {
        "content-type": "text/plain",
        "correlation-id": "a-unique-string-for-this-message"
    },
    "path": "/features/water-tank/inbox/messages/heatUp",
    "value": "47"
}

message_from_thing = {
    "topic": "org.eclipse.ditto/smartcoffee/things/live/messages/ask",
    "headers": {
        "correlation-id": "demo-6qaal9l",
        "auth-subjects": ["ditto", "nginx:ditto"],
        "content-type": "text/plain",
        "version": 1
    },
    "path": "/outbox/messages/ask",
    "status": 418,
    "value": "I don't know since i am only a coffee machine"
}

message_from_feature = {
    "topic": "org.eclipse.ditto/smartcoffee/things/live/messages/heatUp",
    "headers": {
        "content-type": "text/plain",
        "correlation-id": "a-unique-string-for-this-message"
    },
    "path": "/features/water-tank/outbox/messages/heatUp",
    "status": 204
}


def test_message_to_thing():
    msg = Message(root_thing_id).inbox("ask").with_payload("Hey, how are you?")
    envelope = msg.envelope(correlation_id="a-unique-string-for-this-message", content_type="text/plain")
    assert envelope.to_ditto_dict() == message_to_thing


def test_message_to_feature():
    msg = Message(root_thing_id).feature("water-tank").inbox("heatUp").with_payload("47")
    envelope = msg.envelope(correlation_id="a-unique-string-for-this-message", content_type="text/plain")
    assert envelope.to_ditto_dict() == message_to_feature


def test_message_from_thing():
    msg = Message(root_thing_id).outbox("ask").with_payload("I don't know since i am only a coffee machine")
    envelope = msg.envelope(correlation_id="demo-6qaal9l", content_type="text/plain", version=1).with_status(418)
    envelope.headers.with_custom("auth-subjects", ["ditto", "nginx:ditto"])
    assert envelope.to_ditto_dict() == message_from_thing


def test_message_from_feature():
    msg = Message(root_thing_id).feature("water-tank").outbox("heatUp")
    envelope = msg.envelope(correlation_id="a-unique-string-for-this-message", content_type="text/plain").with_status(204)
    assert envelope.to_ditto_dict() == message_from_feature
