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

class _TopicCriterion(str):
    """
    A representation of the defined by Ditto topic criterion options.
    """

    def __eq__(self, obj):
        return isinstance(obj, _TopicCriterion) and str(obj) == str(self)


class _TopicChannel(str):
    """
    A representation of the defined by Ditto topic channel options.
    """

    def __eq__(self, obj):
        return isinstance(obj, _TopicChannel) and str(obj) == str(self)


class TopicAction(str):
    """
     A representation of the defined by Ditto topic action options.
     Also, in the case of live messages handling custom instances can be defined
     for the respective custom topic actions.
    """

    def __eq__(self, obj):
        return isinstance(obj, TopicAction) and str(obj) == str(self)


class _TopicGroup(str):
    """
    A representation of the defined by Ditto topic group options.
    """

    def __eq__(self, obj):
        return isinstance(obj, _TopicGroup) and str(obj) == str(self)


class Topic(object):
    """
    Topic represents the Ditto protocol's Topic entity. It's represented in the form of:
    <namespace>/<entityID>/<group>/<channel>/<criterion>/<action>.
    Each of the components is configurable based on the Ditto's specification for the specific group and/or channel/criterion/etc.
    """

    GROUP_THINGS = _TopicGroup("things")
    """Represents the Ditto things topic group."""
    GROUP_POLICIES = _TopicGroup("policies")

    CHANNEL_TWIN = _TopicChannel("twin")
    """Represents the Ditto twin topic channel."""
    CHANNEL_LIVE = _TopicChannel("live")

    CRITERION_COMMANDS = _TopicCriterion("commands")
    """Represents the commands Ditto topic criterion."""
    CRITERION_EVENTS = _TopicCriterion("events")
    CRITERION_SEARCH = _TopicCriterion("search")
    CRITERION_MESSAGES = _TopicCriterion("messages")
    CRITERION_ERRORS = _TopicCriterion("errors")

    ACTION_CREATE = TopicAction("create")
    """Represents the Ditto create topic action."""
    ACTION_CREATED = TopicAction("created")
    ACTION_MODIFY = TopicAction("modify")
    ACTION_MODIFIED = TopicAction("modified")
    ACTION_DELETE = TopicAction("delete")
    ACTION_DELETED = TopicAction("deleted")
    ACTION_RETRIEVE = TopicAction("retrieve")
    ACTION_SUBSCRIBE = TopicAction("subscribe")
    ACTION_REQUEST = TopicAction("request")
    ACTION_CANCEL = TopicAction("cancel")
    ACTION_NEXT = TopicAction("next")
    ACTION_COMPLETE = TopicAction("complete")
    ACTION_FAILED = TopicAction("failed")

    __topic_format_prefix = "{}/{}/{}"

    def __init__(self,
                 namespace: str = None,
                 entity_id: str = None,
                 group: _TopicGroup = None,
                 channel: _TopicChannel = None,
                 criterion: _TopicCriterion = None,
                 action: TopicAction = None):
        """
        Initializes a new Topic instance with the provided properties according to the Ditto specification.

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :param entity_id: The entity's name to address.
        :type entity_id: str
        :param group: Determines whether the Protocol message references the Things Group or the Policies Group.
        :type group: Topic.GROUP_THINGS, Topic.GROUP_POLICIES
        :param channel: Specifies whether the Protocol message is addressed to the digital twin,
            to the actual live device or to none of both.
        :type channel: Topic.CHANNEL_LIVE, Topic.CHANNEL_TWIN
        :param criterion: Contains the type of action of the Protocol message in the specified
            entity group and on the defined channel.
        :type criterion: Topic.CRITERION_COMMANDS, Topic.CRITERION_EVENTS, Topic.CRITERION_SEARCH,
            Topic.CRITERION_MESSAGES, Topic.CRITERION_ERRORS
        :param action: For command, event, and messages criteria, additional actions are available,
            which further distinguish the purpose of a Protocol message.
        :type action: Topic.ACTION_CREATE, Topic.ACTION_CREATED, Topic.ACTION_MODIFY, Topic.ACTION_MODIFIED,
            Topic.ACTION_DELETE, Topic.ACTION_DELETED, Topic.ACTION_RETRIEVE, Topic.ACTION_SUBSCRIBE,
            Topic.ACTION_REQUEST, Topic.ACTION_CANCEL, Topic.ACTION_NEXT, Topic.ACTION_COMPLETE, Topic.ACTION_FAILED.

            Тhe predefined values are at hand to help for the common predefined use cases by the specification.
            Custom ones can be created using the TopicAction class and used also to fit other possible use cases.
            Custom TopicAction instances can be provided for the Live Channel only.
        """
        self.namespace = namespace
        self.entity_id = entity_id
        self.group = group
        self.channel = channel
        self.criterion = criterion
        self.action = action

    def with_namespace(self, namespace: str) -> 'Topic':
        """
        Sets the namespace of the current Topic instance to the provided string.

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :returns: The updated Topic instance with the provided namespace.
        """
        self.namespace = namespace
        return self

    def with_entity_id(self, entity_id: str) -> 'Topic':
        """
        Sets the entity_id of the current Topic instance to the provided string.
        :param entity_id: The entity's name to address.
        :type entity_id: str
        :returns: The updated Topic instance with the provided entity_id.
        :rtype: Topic
        """
        self.entity_id = entity_id
        return self

    def with_group(self, group: _TopicGroup) -> 'Topic':
        """
        Sets the group of the current Topic instance to the provided _TopicGroup instance.

        :param group: Determines whether the Protocol message references the Things Group or the Policies Group.
        :type group: Topic.GROUP_THINGS, Topic.GROUP_POLICIES
        :returns: The updated Topic instance with the provided group.
        :rtype: Topic
        """
        self.group = group
        return self

    def with_channel(self, channel: _TopicChannel) -> 'Topic':
        """
        Sets the channel of the current Topic instance to the provided _TopicChannel instance.

        :param channel: Specifies whether the Protocol message is addressed to the digital twin,
            to the actual live device or to none of both.
        :type channel: Topic.CHANNEL_LIVE, Topic.CHANNEL_TWIN
        :returns: The updated Topic instance with the provided channel.
        :rtype: Topic
        """
        self.channel = channel
        return self

    def with_criterion(self, criterion: _TopicCriterion) -> 'Topic':
        """
        Sets the criterion of the current Topic instance to the provided _TopicCriterion instance.

        :param criterion: Contains the type of action of the Protocol message in the specified
            entity group and on the defined channel.
        :type criterion: Topic.CRITERION_COMMANDS, Topic.CRITERION_EVENTS, Topic.CRITERION_SEARCH,
            Topic.CRITERION_MESSAGES, Topic.CRITERION_ERRORS
        :returns: The updated Topic instance with the provided criterion.
        :rtype: Topic
        """
        self.criterion = criterion
        return self

    def with_action(self, action: TopicAction) -> 'Topic':
        """
        Sets the action of the current Topic instance to the provided TopicAction instance.

        :param action: For command, event, and messages criteria, additional actions are available,
            which further distinguish the purpose of a Protocol message.
        :type action: Topic.ACTION_CREATE, Topic.ACTION_CREATED, Topic.ACTION_MODIFY, Topic.ACTION_MODIFIED,
            Topic.ACTION_DELETE, Topic.ACTION_DELETED, Topic.ACTION_RETRIEVE, Topic.ACTION_SUBSCRIBE,
            Topic.ACTION_REQUEST, Topic.ACTION_CANCEL, Topic.ACTION_NEXT, Topic.ACTION_COMPLETE, Topic.ACTION_FAILED.

            Тhe predefined values are at hand to help for the common predefined use cases by the specification.
            Custom ones can be created using the TopicAction class and used also to fit the other use cases
            expected in the specification.
            (See e.g. https://www.eclipse.org/ditto/2.0/protocol-specification-things-messages.html)
        :returns: The updated Topic instance with the provided action.
        :rtype: Topic
        """
        self.action = action
        return self

    def __str__(self):
        """
        Converts the current Topic instance into a string that is compliant with the Ditto specification.

        :returns: A string representation of the Topic instance compliant with the Ditto specification.
        :rtype: str
        """
        topic = Topic.__topic_format_prefix.format(self.namespace, self.entity_id, self.group)
        if self.group == Topic.GROUP_POLICIES:
            suffixes = [self.criterion, self.action]
        else:
            suffixes = [self.channel, self.criterion, self.action]

        for suffix in suffixes:
            if suffix:
                topic += "/{}".format(suffix)
        return topic

    def from_string(self, topic_string) -> 'Topic':
        """
        Sets the Topic's properties from a provided string.

        :param topic_string: A string that is compliant with the Ditto specification.
            Has the following structure: <namespace>/<entity-name>/<group>/<channel>/<criterion>/<action>
        :type topic_string: str
        :returns: The initialized Topic instance with the provided properties.
        :rtype: Topic
        """
        elements = topic_string.split(sep="/", maxsplit=5)
        self.namespace = elements[0]
        self.entity_id = elements[1]
        self.group = _TopicGroup(elements[2])

        if self.group == Topic.GROUP_THINGS:
            self.channel = _TopicChannel(elements[3])
            __index = 4
        else:
            __index = 3

        self.criterion = _TopicCriterion(elements[__index])
        __index += 1
        if __index < len(elements):  # action is optional
            self.action = TopicAction(elements[__index])
        return self
