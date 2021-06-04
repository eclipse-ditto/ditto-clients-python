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
        self.namespace = namespace
        self.entity_id = entity_id
        self.group = group
        self.channel = channel
        self.criterion = criterion
        self.action = action

    def with_namespace(self, namespace: str) -> 'Topic':
        """
        Configures the namespace of the Topic.

        :param namespace:
        :return:
        """
        self.namespace = namespace
        return self

    def with_entity_id(self, entity_id: str) -> 'Topic':
        """
        Configures the namespace of the Topic.

        :param entity_id:
        :return:
        """
        self.entity_id = entity_id
        return self

    def with_group(self, group: _TopicGroup) -> 'Topic':
        """
        Configures the group of the Topic.

        :param group:
        :return:
        """
        self.group = group
        return self

    def with_channel(self, channel: _TopicChannel) -> 'Topic':
        """
        Configures the channel of the Topic.

        :param channel:
        :return:
        """
        self.channel = channel
        return self

    def with_criterion(self, criterion: _TopicCriterion) -> 'Topic':
        """
        Configures the criterion of the Topic.

        :param criterion:
        :return:
        """
        self.criterion = criterion
        return self

    def with_action(self, action: TopicAction) -> 'Topic':
        """
        Configures the action of the Topic.

        :param action:
        :return:
        """
        self.action = action
        return self

    def __str__(self):
        """
        Provides the string representation of a Topic entity.

        :return:
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

        :param topic_string:
        :return:
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

