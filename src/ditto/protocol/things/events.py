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

from typing import Any

from ...model.namespaced_id import NamespacedID
from ...model.thing import Thing
from ...protocol.things.signal import _Signal
from ...protocol.topic import Topic


class Event(_Signal):
    """
    Represents a message entity defined by the Ditto protocol for the Things group that defines a notification for a change that happened.
    This is a special Message that is always bound to a specific Thing instance along with providing the capabilities to configure:
    - the type of the change that happened - created, modified, deleted
    - the channel used for the notification - twin, live
    - the entity that was affected - the whole Thing (the default), all features of the Thing (features),
                                  a single Feature of the Thing (feature), all attributes of the Thing (attributes) or
                                  a single attribute of the Thing (attribute), the Thing's policy (policy_id)
                                  or the Thing's definition (definition).
    Note: Only one change type can be configured to the event - if using the methods for configuring it - only the last one applies.
    Note: Only one channel can be configured to the event - if using the methods for configuring it - only the last one applies.
    Note: Only one entity that will b affected by the event can be configured - if using the methods for configuring it - only the last one applies.
    """

    def __init__(self, thing_id: NamespacedID, topic: Topic = None, path: str = None, payload: Any = None):
        """
        Initializes a new Event instance with the provided thing ID, topic, path and payload
        according to the Ditto specification

        :param thing_id: The namespaced entity ID
        :type thing_id: NamespacedID
        :param topic: The topic for the event as a Topic instance
        :type topic: Topic
        :param path: The path at which to apply the event
        :type path: str
        :param payload: The value that will be applied
        :type payload: typing.Any
        """
        if topic:
            self.topic = topic
        else:
            self.topic = Topic().with_namespace(thing_id.namespace) \
                .with_entity_id(thing_id.name) \
                .with_group(Topic.GROUP_THINGS) \
                .with_channel(Topic.CHANNEL_TWIN) \
                .with_criterion(Topic.CRITERION_EVENTS)
        if path is None:
            self.path = _Signal._path_thing
        else:
            self.path = path
        self.payload = payload

    def created(self, thing: Thing) -> 'Event':
        """
        Prepares the event to be emitted for a created
        feature, property, multiple features or properties, or the whole thing

        :param thing: The thing, that has been created
        :type thing: Thing
        :returns: An Event instance configured to be emitted for an executed create action
        :rtype: Event
        """
        self.topic.with_action(Topic.ACTION_CREATED)
        self.payload = thing.to_ditto_dict()
        self.path = _Signal._path_thing
        return self

    def modified(self, payload: Any) -> 'Event':
        """
        Prepares the event to be emitted for a modified thing or a part of the thing

        :param payload: The new value for the configured event to emit
        :type payload: typing.Any
        :returns: An Event instance configured to be emitted for an executed modify action
        :rtype: Event
        """
        self.topic.with_action(Topic.ACTION_MODIFIED)
        self.payload = payload
        return self

    def deleted(self) -> 'Event':
        """
        Prepares the event to be emitted for a deleted thing or a part of the thing

        :returns: An Event instance configured to be emitted for an executed delete action
        :rtype: Event
        """
        self.topic.with_action(Topic.ACTION_DELETED)
        return self

    def policy_id(self) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding the policy ID of the thing

        :returns: An Event instance configured to be emitted for changes in the policy ID of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_policy_id
        return self

    def definition(self) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding the definition of the thing

        :returns: An Event instance configured to be emitted for changes in the definition of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_definition
        return self

    def attributes(self) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding all the attributes of the thing

        :returns: An Event instance configured to be emitted for changes in all the attributes of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_attributes
        return self

    def attribute(self, attribute_path: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding a certain attribute of the thing

        :param attribute_path: The path to the specified attribute
        :type attribute_path: str
        :returns: An Event instance configured to be emitted for changes in a certain attribute of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_attribute_format.format(attribute_path)
        return self

    def features(self) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding all the features of the thing

        :returns: An Event instance configured to be emitted for changes in all the features of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_features
        return self

    def feature(self, feature_id: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :returns: An Event instance configured to be emitted for changes in a certain feature of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_feature_format.format(feature_id)
        return self

    def feature_definition(self, feature_id: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding the definition of a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :returns: An Event instance configured to be emitted
            for changes in the definition of a certain feature of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_feature_definition_format.format(feature_id)
        return self

    def feature_properties(self, feature_id: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding all the properties of a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :returns: An Event instance configured to be emitted
            for changes in all the properties of a certain feature of the thing
        :rtype: Event
        """
        return self

    def feature_property(self, feature_id: str, property_path: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding a certain property of a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :param property_path: The path of the specified property
        :type property_path: str
        :returns: An Event instance configured to be emitted
            for changes in a certain property of a certain feature of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_feature_property_format.format(feature_id, property_path)
        return self

    def feature_desired_properties(self, feature_id: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding all
        the desired properties of a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :returns: An Event instance configured to be emitted
            for changes in all the desired properties of a certain feature of the thing
        :rtype: Event
        """
        return self

    def feature_desired_property(self, feature_id: str, desired_property_path: str) -> 'Event':
        """
        Prepares the event to be emitted for an action regarding a
        certain desired property of a certain feature of the thing

        :param feature_id: The ID of the specified feature
        :type feature_id: str
        :param desired_property_path: The path of the specified desired property
        :type desired_property_path: str
        :returns: An Event instance configured to be emitted
            for changes in a certain desired property of a certain feature of the thing
        :rtype: Event
        """
        self.path = _Signal._path_thing_feature_desired_property_format.format(feature_id, desired_property_path)
        return self

    def live(self) -> 'Event':
        """
        Prepares the event to be sent to the live channel (towards the actual device)

        :returns: An Event instance configured to be emitted on the live channel
        :rtype: Event
        """
        self.topic.with_channel(Topic.CHANNEL_LIVE)
        return self

    def twin(self) -> 'Event':
        """
        Prepares the event to be sent to the twin channel (towards the digital twin of the device)

        :returns: An Event instance configured to be emitted on the twin channel
        :rtype: Event
        """
        self.topic.with_channel(Topic.CHANNEL_TWIN)
