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
    Note: Only one entity that the message targets can be configured to the live message - if using the methods for configuring it - only the last one applies.
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
        """
        Initializes a new Message instance with the provided thing ID, topic, subject, mailbox,
        addressed part of thing and payload according to the Ditto specification

        :param thing_id: The namespaced entity ID
        :type thing_id: NamespacedID
        :param topic: The topic for the message as a Topic instance
        :type topic: Topic
        :param subject: The subject of the message
        :type subject: str
        :param mailbox: The type of communication (inbox, outbox)
        :type mailbox: str
        :param address_part_of_thing: The target of the message (may be the whole thing or a feature of the thing)
        :type address_part_of_thing: str
        :param payload: The value that will be applied
        :type payload: typing.Any
        """
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
        """
        Sets the communication type to inbox and updates the message subject

        :param subject: The new message subject
        :type subject: str
        :returns: A new inbox Message instance for the provided subject
        :rtype: Message
        """
        self.topic.with_action(TopicAction(subject))
        self.subject = subject
        self.mailbox = Message.__inbox
        return self

    def outbox(self, subject: str) -> 'Message':
        """
        Sets the communication type to outbox and updates the message subject

        :param subject: The new message subject
        :type subject: str
        :returns: A new outbox Message instance for the provided subject
        :rtype: Message
        """
        self.topic.with_action(TopicAction(subject))
        self.subject = subject
        self.mailbox = Message.__outbox
        return self

    def with_payload(self, payload: Any) -> 'Message':
        """
        Sets the payload for the message

        :param payload: The payload for the message
        :type payload: typing.Any
        :returns: The updated Message instance with the updated payload
        :rtype: Message
        """
        self.payload = payload
        return self

    def feature(self, feature_id: str) -> 'Message':
        """
        Sets the Message to address a specific Feature

        :param feature_id: The targeted feature of the thing
        :type feature_id: str
        :returns: The updated Message instance with the updated addressed part of thing
        :rtype: Message
        """
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
        """
        Prepares the message to be sent by putting it in the Envelope

        :param content_type: The content type which describes the value of Ditto Protocol messages
        :type content_type: str
        :param correlation_id: The correlation ID header is used for linking one message with another.
            It typically links a reply message with its requesting message
        :type correlation_id: str
        :param ditto_originator: Contains the first authorization subject of the command that caused the sending
            of this message. Set by Ditto
        :type ditto_originator: str
        :param if_match: Has to conform to RFC-7232 (Conditional Requests). Common used for
            optimistic locking by specifying the ETag from a previous response and retrieving or
            modifying a resource only if it already exists
        :type if_match: str
        :param if_none_match: Has to conform to RFC-7232 (Conditional Requests). Common used for
            retrieving or modifying a resource only if it doesn't already exists
        :type if_none_match: str
        :param response_required: Whether a response to a command is required or if it may be omitted.
        :type response_required: bool
        :param requested_acks: Defining which acknowledgements ("ack") are requested for a command processed by Ditto
        :type requested_acks: List[str]
        :param ditto_weak_ack: Marks weak acknowledgements issued by Ditto.
        :type ditto_weak_ack: bool
        :param timeout: The timeout value to apply on the Ditto server side
            e.g. applied when waiting for requested acknowledgements
        :type timeout: str
        :param version: Determines the schema version of the payload
        :type version: str
        :param put_metadata: Determines which Metadata information is stored in the thing
        :type put_metadata: List[typing.Any]
        :returns: The Envelope instance containing topic, path, headers and value
        :rtype: Envelope
        """
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
