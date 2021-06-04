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

json_full = {
    "definition": ["org.eclipse.ditto:complex-type:1.0.0"],
    "properties": {
        "status": {
            "connected": True,
            "complexProperty": {
                "street": "my street",
                "house no": 42
            }
        }
    }
}

json_no_properties = {
    "definition": ["org.eclipse.ditto:complex-type:1.0.0"]
}

json_no_definition = {
    "properties": {
        "status": {
            "connected": True,
            "complexProperty": {
                "street": "my street",
                "house no": 42
            }
        }
    }
}

json_multiple_definitions = {
    "definition": ["org.eclipse.ditto:complex-type:1.0.0", "org.eclipse.ditto:test-type:1.0.1"],
    "properties": {
        "status": {
            "connected": True,
            "complexProperty": {
                "street": "my street",
                "house no": 42
            }
        }
    }
}

json_multiple_properties = {
    "definition": ["org.eclipse.ditto:complex-type:1.0.0"],
    "properties": {
        "status": {
            "connected": True,
            "complexProperty": {
                "street": "my street",
                "house no": 42
            }
        },
        "lightbulb": {
            "color": "pink",
            "saturation": 100
        }
    }
}


def test_full_definition():
    feature = Feature().from_ditto_dict(json_full)

    assert feature.definition[0].__str__() == 'org.eclipse.ditto:complex-type:1.0.0'


def test_full_properties():
    feature = Feature().from_ditto_dict(json_full)

    assert feature.properties.__str__() == "{'status': {'connected': True, 'complexProperty': {'street': 'my street', 'house no': 42}}}"


def test_no_properties():
    feature = Feature().from_ditto_dict(json_no_properties)

    assert feature.definition[0].__str__() == "org.eclipse.ditto:complex-type:1.0.0"


def test_no_definition():
    feature = Feature().from_ditto_dict(json_no_definition)

    assert feature.properties.__str__() == "{'status': {'connected': True, 'complexProperty': {'street': 'my street', 'house no': 42}}}"


def test_multiple_definitions():
    feature = Feature().from_ditto_dict(json_multiple_definitions)

    assert feature.definition[1].__str__() == 'org.eclipse.ditto:test-type:1.0.1'


def test_multiple_properties():
    feature = Feature().from_ditto_dict(json_multiple_properties)

    assert feature.properties.__str__() == "{'status': {'connected': True, 'complexProperty': {'street': 'my street', 'house no': 42}}, 'lightbulb': {'color': 'pink', 'saturation': 100}}"
