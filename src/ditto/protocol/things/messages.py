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

from typing import Any, List

from ...model.namespaced_id import NamespacedID
from ..envelope import Envelope
from ..headers import Headers
from ..things.signal import _Signal
from ..topic import Topic, TopicAction


class Message(object):
    """
    Represents a message entity defined by the Ditto protocol for the Things group that defines an instant communication with the underlying device/implementation.
    This is a special Message that is always bound to a specific Thing instance, it's always exchanged vie the
    Live communication channel and it provides the capabilities to configure:
    - the type of the communication - inbox, outbox
    - the entity that was affected - the whole Thing (the default) or a single Feature of the Thing (feature).
    Note: Only one communication type can be configured to the live message - if using the methods for configuring it - only the last one applies.
    Note: Only one entity that the message targts can be configured to the live message - if using the methods for configuring it - only the last one applies.
    """
    __inbox = "inbox"
    __outbox = "outbox"
    __path_messages_format = "{}/{}/messages/{}"

    def __init__(self, thing_id: NamespacedID,
                 topic: Topic = None,
                 subject: str = None,
                 mailbox: str = None,
                 address_part_of_thing: str = None,
                 payload: Any = None):
        if topic:
            self.topic = topic
        else:
            self.topic = Topic().with_namespace(thing_id.namespace) \
                .with_entity_id(thing_id.name) \
                .with_group(Topic.GROUP_THINGS) \
                .with_channel(Topic.CHANNEL_LIVE) \
                .with_criterion(Topic.CRITERION_MESSAGES)
        self.subject = subject
        self.mailbox = mailbox
        self.address_part_of_thing = address_part_of_thing
        if self.address_part_of_thing is None:
            self.address_part_of_thing = ""
        self.payload = payload

    def inbox(self, subject: str) -> 'Message':
        self.topic.with_action(TopicAction(subject))
        self.subject = subject
        self.mailbox = Message.__inbox
        return self

    def outbox(self, subject: str) -> 'Message':
        self.topic.with_action(TopicAction(subject))
        self.subject = subject
        self.mailbox = Message.__outbox
        return self

    def with_payload(self, payload: Any) -> 'Message':
        self.payload = payload
        return self

    def feature(self, feature_id: str) -> 'Message':
        self.address_part_of_thing = _Signal._path_thing_feature_format.format(feature_id)
        return self

    def envelope(self,
                 content_type: str = None,
                 correlation_id: str = None,
                 ditto_originator: str = None,
                 if_match: str = None,
                 if_none_match: str = None,
                 response_required: bool = None,
                 requested_acks: List[str] = None,
                 ditto_weak_ack: bool = None,
                 timeout: str = None,
                 version: str = None,
                 put_metadata: List[Any] = None,
                 **kwargs) -> Envelope:

        payload = self.payload if not hasattr(self.payload, _Signal._payload_converter_func_name) else self.payload.to_ditto_dict()

        msg = Envelope().with_topic(self.topic) \
            .with_path(Message.__path_messages_format.format(self.address_part_of_thing, self.mailbox, self.subject)) \
            .with_value(payload) \
            .with_headers(Headers(content_type=content_type,
                                  correlation_id=correlation_id,
                                  ditto_originator=ditto_originator,
                                  if_match=if_match,
                                  if_none_match=if_none_match,
                                  response_required=response_required,
                                  requested_acks=requested_acks,
                                  ditto_weak_ack=ditto_weak_ack,
                                  timeout=timeout,
                                  version=version,
                                  put_metadata=put_metadata,
                                  **kwargs))

        return msg
