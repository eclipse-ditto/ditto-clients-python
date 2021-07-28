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

from ditto.protocol.topic import Topic, TopicAction


def test_from_string():
    t = Topic().from_string("my.ns/my.dev/things/live/messages/install")
    assert t.namespace == "my.ns"
    assert t.entity_id == "my.dev"
    assert t.group == Topic.GROUP_THINGS
    assert t.channel == Topic.CHANNEL_LIVE
    assert t.criterion == Topic.CRITERION_MESSAGES
    assert t.action == TopicAction("install")


def test_from_string():
    t = Topic().from_string("my.ns/my.dev/things/twin/commands/modify")
    assert t.namespace == "my.ns"
    assert t.entity_id == "my.dev"
    assert t.group == Topic.GROUP_THINGS
    assert t.channel == Topic.CHANNEL_TWIN
    assert t.criterion == Topic.CRITERION_COMMANDS
    assert t.action == Topic.ACTION_MODIFY


def test_from_string():
    t = Topic().from_string("my.ns/my.policy/policies/commands/modify")
    assert t.namespace == "my.ns"
    assert t.entity_id == "my.policy"
    assert t.group == Topic.GROUP_POLICIES
    assert t.channel is None
    assert t.criterion == Topic.CRITERION_COMMANDS
    assert t.action == Topic.ACTION_MODIFY
