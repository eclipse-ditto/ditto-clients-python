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

from ditto.client import Client
from ditto.model.definition_id import DefinitionID
from ditto.model.feature import Feature
from ditto.model.namespaced_id import NamespacedID
from ditto.protocol.things.commands import Command

thing_id = NamespacedID().from_string("test.ns:test-name")
feature_id = "MyFeatureID"
property_id = "myProperty"
definition_id = DefinitionID().from_string("my.model.namespace:FeatureModel:1.0.0")


def create_or_modify_feature(client):
    # Define the feature to be created or how you want it to be after modification
    # You can provide a semantic definition of your feature
    my_feature = Feature().with_definition(definition_id).with_property(property_id, "myValue")

    # Create your Ditto command. Modify acts as an upsert - it either updates or creates features.
    command = Command(thing_id).feature(feature_id).twin().modify(my_feature)

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)


def create_or_modify_feature_property(client):
    # Create your Ditto command. Modify acts as an upsert - it either updates or creates feature properties.
    command = Command(thing_id).feature_property(feature_id, property_id).twin().modify("myModifiedValue")

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)


def delete_feature(client):
    # Create your Ditto command. Delete can be used to delete either a feature's properties or the feature itself.
    command = Command(thing_id).feature(feature_id).twin().delete()

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)


def delete_feature_property(client):
    # Create your Ditto command. Delete can be used to delete either a feature's properties or the feature itself.
    command = Command(thing_id).feature_property(feature_id, property_id).twin().delete()

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)


def on_connect(cl: Client):
    create_or_modify_feature(cl)
    create_or_modify_feature_property(cl)
    delete_feature_property(cl)
    delete_feature(cl)


# Test feature modification actions
ditto_client = Client(on_connect=on_connect)
ditto_client.connect("localhost")
ditto_client.disconnect()
