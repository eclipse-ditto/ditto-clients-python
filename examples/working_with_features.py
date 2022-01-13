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

from base64 import encode
import time, sys

from ditto.client import Client
from ditto.model.feature import Feature
from ditto.model.namespaced_id import NamespacedID
from ditto.model.thing import Thing
from ditto.protocol.envelope import Envelope
from ditto.protocol.things.commands import Command


client = Client()
client.connect("localhost")

def create_or_modify_feature(client):
       
    # Define the feature to be created or how you want it to be after modification
    # You can provide a semantic definition of your feature
    myFeature = Feature().with_definition_from("my.model.namespace:FeatureModel:1.0.0").with_property("myProperty", "myValue")
    
    # Create your Ditto command. Modify acts as an upsert - it either updates or creates features.
    command = Command(NamespacedID().from_string("test.ns:test-name")).feature("myFeatureID").twin().modify(myFeature)

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)
    
def create_or_modify_feature_property(client):

    # Create your Ditto command. Modify acts as an upsert - it either updates or creates feature properties.
    command = Command(NamespacedID().from_string("test.ns:test-name")).feature_property("myFeatureID", "myProperty").twin().modify("myModifiedValue")

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)    

def delete_feature(client):

    # Create your Ditto command. Delete can be used to delete either a feature's properties or the feature itself.
    command = Command(NamespacedID().from_string("test.ns:test-name")).feature("myFeatureID").twin().delete()

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)  

def delete_feature_property(client):

    # Create your Ditto command. Delete can be used to delete either a feature's properties or the feature itself.
    command = Command(NamespacedID().from_string("test.ns:test-name")).feature_property("myFeatureID", "myProperty").twin().delete()

    # Send the Ditto command.
    envelope = command.envelope(response_required=False)

    client.send(envelope)  

# Test feature modifiation actions
create_or_modify_feature(client)
create_or_modify_feature_property(client)
delete_feature(client)
delete_feature_property(client)

client.disconnect()
