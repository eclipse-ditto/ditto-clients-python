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

from ditto.model.feature import Feature
from ditto.model.namespaced_id import NamespacedID
from ditto.model.thing import Thing
from ditto.protocol.things.events import Event

root_thing_namespace = "org.eclipse.ditto"
root_thing_name = "fancy-thing"
root_thing_thing_id = NamespacedID(root_thing_namespace, root_thing_name)

created_event = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/events/created",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/",
    "value": {
        "thingId": "org.eclipse.ditto:fancy-thing_53",
        "policyId": "org.eclipse.ditto:the_policy_id",
        "definition": "org.eclipse.ditto:SomeModel:1.0.0",
        "attributes": {
            "test-attr": {
                "my-custom-attr": "attr"
            }
        },
        "features": {
            "testFeature": {
                "properties": {
                    "a": 2,
                },
                "desiredProperties": {
                    "a": 1
                }
            }
        }
    },
    "revision": 1
}

deleted_event = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/events/deleted",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/",
    "revision": 1
}

modified_feature_event = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/events/modified",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/features/testFeature",
    "value": {
        "properties": {
            "a": 2,
        },
        "desiredProperties": {
            "a": 1
        }
    },
    "revision": 1
}

modified_feature_property_event = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/events/modified",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/features/accelerometer/properties/x",
    "value": 42,
    "revision": 1
}


def test_created_event():
    thing_created = Thing().with_id_from("org.eclipse.ditto:fancy-thing_53") \
        .with_policy_id_from("org.eclipse.ditto:the_policy_id") \
        .with_definition_from("org.eclipse.ditto:SomeModel:1.0.0") \
        .with_attribute("test-attr", {"my-custom-attr": "attr"}) \
        .with_feature("testFeature", Feature().with_properties(a=2).with_desired_properties(a=1))

    event = Event(root_thing_thing_id).created(thing_created)
    envelope = event.envelope(correlation_id="<command-correlation-id>").with_revision(1)
    assert envelope.to_ditto_dict() == created_event


def test_deleted_event():
    event = Event(root_thing_thing_id).deleted()
    envelope = event.envelope(correlation_id="<command-correlation-id>").with_revision(1)
    assert envelope.to_ditto_dict() == deleted_event


def test_modified_feature_event():
    feature_modified = Feature().with_properties(a=2).with_desired_properties(a=1)
    event = Event(root_thing_thing_id).feature("testFeature").modified(feature_modified)
    envelope = event.envelope(correlation_id="<command-correlation-id>").with_revision(1)
    assert envelope.to_ditto_dict() == modified_feature_event


def test_modified_feature_property_event():
    event = Event(root_thing_thing_id).feature_property("accelerometer", "x").modified(42)
    envelope = event.envelope(correlation_id="<command-correlation-id>").with_revision(1)
    assert envelope.to_ditto_dict() == modified_feature_property_event
