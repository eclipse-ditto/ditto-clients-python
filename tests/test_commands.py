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
from ditto.protocol.things.commands import Command

root_thing_namespace = "org.eclipse.ditto"
root_thing_name = "fancy-thing"
root_thing_thing_id = NamespacedID(root_thing_namespace, root_thing_name)

create_cmd = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/commands/create",
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
    }
}

delete_cmd = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/commands/delete",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/"
}

modify_feature_cmd = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/commands/modify",
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
    }
}

modify_feature_property_cmd = {
    "topic": "org.eclipse.ditto/fancy-thing/things/twin/commands/modify",
    "headers": {
        "correlation-id": "<command-correlation-id>"
    },
    "path": "/features/accelerometer/properties/x",
    "value": 42
}


def test_create_command():
    thing_to_create = Thing().with_id_from("org.eclipse.ditto:fancy-thing_53") \
        .with_policy_id_from("org.eclipse.ditto:the_policy_id") \
        .with_definition_from("org.eclipse.ditto:SomeModel:1.0.0") \
        .with_attribute("test-attr", {"my-custom-attr": "attr"}) \
        .with_feature("testFeature", Feature().with_properties(a=2).with_desired_properties(a=1))

    command = Command(root_thing_thing_id).create(thing_to_create)
    envelope = command.envelope(correlation_id="<command-correlation-id>")
    assert envelope.to_ditto_dict() == create_cmd


def test_delete_command():
    command = Command(root_thing_thing_id).delete()
    envelope = command.envelope(correlation_id="<command-correlation-id>")
    assert envelope.to_ditto_dict() == delete_cmd


def test_modify_feature_command():
    feature_to_modify = Feature().with_properties(a=2).with_desired_properties(a=1)
    command = Command(root_thing_thing_id).feature("testFeature").modify(feature_to_modify)
    envelope = command.envelope(correlation_id="<command-correlation-id>")
    assert envelope.to_ditto_dict() == modify_feature_cmd


def test_modify_feature_property_command():
    command = Command(root_thing_thing_id).feature_property("accelerometer", "x").modify(42)
    envelope = command.envelope(correlation_id="<command-correlation-id>")
    assert envelope.to_ditto_dict() == modify_feature_property_cmd
