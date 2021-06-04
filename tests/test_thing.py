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

from ditto.model.thing import Thing

# Tests for thing deserialization from json

json_full = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "attributes": {
        "room": "kitchen"
    },
    "features": {
        "lightbulb": {
            "properties": {
                "state": 1,
                "color": "white"
            },
            "desiredProperties": {
                "state": 1,
                "color": "black"
            }
        }
    },
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}

json_no_features = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "attributes": {
        "room": "kitchen"
    },
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}

json_no_attributes = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "features": {
        "lightbulb": {
            "properties": {
                "state": 1,
                "color": "white"
            }
        }
    },
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}

json_multiple_features = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "attributes": {
        "room": "kitchen"
    },
    "features": {
        "lightbulb": {
            "properties": {
                "state": 1,
                "color": "white"
            }
        },
        "lightbulb_2": {
            "properties": {
                "color": "red"
            }
        }
    },
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}

json_multiple_attributes = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "attributes": {
        "room": "kitchen",
        "house_number": 31
    },
    "features": {
        "lightbulb": {
            "properties": {
                "state": 1,
                "color": "white"
            }
        }
    },
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}

json_no_features_no_attributes = {
    "thingId": "org.example.intern.dmp:lamp",
    "policyId": "org.example.intern.dmp:internship",
    "definition": "org.example.intern.dmp:lamp:1.0.0",
    "_revision": 29,
    "_modified": "2020-08-21T12:19:15.773119884Z"
}


def test_json_full_thing_id():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_full_policy_id():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_full_definition_id():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_full_attributes_room():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.attributes["room"] == "kitchen"


def test_json_full_features_state():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.features["lightbulb"].properties["state"] == 1


def test_json_full_features_desired_state():
    thing = Thing().from_ditto_dict(json_full)
    assert thing.features["lightbulb"].desired_properties["state"] == 1


def test_json_full_features_desired_color():
    thing = Thing().from_ditto_dict(json_full)
    assert thing.features["lightbulb"].desired_properties["color"] == "black"


def test_json_full_features_color():
    thing = Thing().from_ditto_dict(json_full)

    assert thing.features["lightbulb"].properties["color"] == "white"


def test_json_no_features_thing_id():
    thing = Thing().from_ditto_dict(json_no_features)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_no_features_policy_id():
    thing = Thing().from_ditto_dict(json_no_features)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_no_features_definition_id():
    thing = Thing().from_ditto_dict(json_no_features)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_no_features_attributes_room():
    thing = Thing().from_ditto_dict(json_no_features)

    assert thing.attributes["room"] == "kitchen"


def test_json_no_attributes_thing_id():
    thing = Thing().from_ditto_dict(json_no_attributes)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_no_attributes_policy_id():
    thing = Thing().from_ditto_dict(json_no_attributes)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_no_attributes_definition_id():
    thing = Thing().from_ditto_dict(json_no_attributes)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_no_attributes_features_state():
    thing = Thing().from_ditto_dict(json_no_attributes)

    assert thing.features["lightbulb"].properties["state"] == 1


def test_json_no_attributes_features_color():
    thing = Thing().from_ditto_dict(json_no_attributes)

    assert thing.features["lightbulb"].properties["color"] == "white"


def test_json_multiple_features_thing_id():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_multiple_features_policy_id():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_multiple_features_definition_id():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_multiple_features_attributes_room():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.attributes["room"] == "kitchen"


def test_json_multiple_features_features_lightbulb_state():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.features["lightbulb"].properties["state"] == 1


def test_json_multiple_features_features_lightbulb_color():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.features["lightbulb"].properties["color"] == "white"


def test_json_multiple_features_features_lightbulb_2_color():
    thing = Thing().from_ditto_dict(json_multiple_features)

    assert thing.features["lightbulb_2"].properties["color"] == "red"


def test_json_multiple_attributes_thing_id():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_multiple_attributes_policy_id():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_multiple_attributes_definition_id():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_multiple_attributes_attributes_room():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.attributes["room"] == "kitchen"


def test_json_multiple_attributes_attributes_house_number():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.attributes["house_number"] == 31


def test_json_multiple_attributes_features_state():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.features["lightbulb"].properties["state"] == 1


def test_json_multiple_attributes_features_color():
    thing = Thing().from_ditto_dict(json_multiple_attributes)

    assert thing.features["lightbulb"].properties["color"] == "white"


def test_json_no_features_no_attributes_thing_id():
    thing = Thing().from_ditto_dict(json_no_features_no_attributes)

    assert thing.thing_id.__str__() == "org.example.intern.dmp:lamp"


def test_json_no_features_no_attributes_policy_id():
    thing = Thing().from_ditto_dict(json_no_features_no_attributes)

    assert thing.policy_id.__str__() == "org.example.intern.dmp:internship"


def test_json_no_features_no_attributes_definition_id():
    thing = Thing().from_ditto_dict(json_no_features_no_attributes)

    assert thing.definition.__str__() == "org.example.intern.dmp:lamp:1.0.0"


def test_json_no_features_no_attributes_revision():
    thing = Thing().from_ditto_dict(json_no_features_no_attributes)

    assert thing.revision == 29
