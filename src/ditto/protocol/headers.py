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

from typing import Any, List, Dict


class Headers(object):
    """
    Represents all Ditto-specific headers along with additional HTTP/etc. headers
    that can be applied depending on the transport used.
    See https://www.eclipse.org/ditto/protocol-specification.html
    """
    CONTENT_TYPE = "content-type"
    CORRELATION_ID = "correlation-id"
    DITTO_ORIGINATOR = "ditto-originator"
    IF_MATCH = "If-Match"
    IF_NONE_MATCH = "If-None-Match"
    RESPONSE_REQUIRED = "response-required"
    REQUESTED_ACKS = "requested-acks"
    DITTO_WEAK_ACK = "ditto-weak-ack"
    TIMEOUT = "timeout"
    SCHEMA_VERSION = "version"
    PUT_METADATA = "put-metadata"

    def __init__(self, content_type: str = None,
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
                 **kwargs):
        self.values = {}
        if content_type:
            self.content_type = content_type
        if correlation_id:
            self.correlation_id = correlation_id
        if ditto_originator:
            self.ditto_originator = ditto_originator
        if if_match:
            self.if_match = if_match
        if if_none_match:
            self.if_none_match = if_none_match
        if response_required is not None:
            self.response_required = response_required
        if requested_acks:
            self.requested_acks = requested_acks.copy()
        if ditto_weak_ack is not None:
            self.ditto_weak_ack = ditto_weak_ack
        if timeout:
            self.timeout = timeout
        if version is not None:
            self.version = version
        if put_metadata:
            self.put_metadata = put_metadata.copy()
        if kwargs:
            self.values.update(**kwargs.copy())

    @property
    def content_type(self) -> str:
        try:
            return self.values[Headers.CONTENT_TYPE]
        except KeyError:
            pass

    @content_type.setter
    def content_type(self, content_type: str):
        self.values[Headers.CONTENT_TYPE] = content_type

    def with_content_type(self, content_type: str) -> 'Headers':
        self.content_type = content_type
        return self

    @property
    def correlation_id(self) -> str:
        try:
            return self.values[Headers.CORRELATION_ID]
        except KeyError:
            pass

    @correlation_id.setter
    def correlation_id(self, correlation_id: str):
        self.values[Headers.CORRELATION_ID] = correlation_id

    def with_correlation_id(self, c: str) -> 'Headers':
        self.correlation_id = c
        return self

    @property
    def ditto_originator(self) -> str:
        try:
            return self.values[Headers.DITTO_ORIGINATOR]
        except KeyError:
            pass

    @ditto_originator.setter
    def ditto_originator(self, ditto_originator: str):
        self.values[Headers.DITTO_ORIGINATOR] = ditto_originator

    def with_ditto_originator(self, ditto_originator: str) -> 'Headers':
        self.ditto_originator = ditto_originator
        return self

    @property
    def if_match(self) -> str:
        try:
            return self.values[Headers.IF_MATCH]
        except KeyError:
            pass

    @if_match.setter
    def if_match(self, if_match: str):
        self.values[Headers.IF_MATCH] = if_match

    def with_if_match(self, if_match: str) -> 'Headers':
        self.if_match = if_match
        return self

    @property
    def if_none_match(self) -> str:
        try:
            return self.values[Headers.IF_NONE_MATCH]
        except KeyError:
            pass

    @if_none_match.setter
    def if_none_match(self, if_none_match: str):
        self.values[Headers.IF_NONE_MATCH] = if_none_match

    def with_if_none_match(self, if_none_match: str) -> 'Headers':
        self.if_none_match = if_none_match
        return self

    @property
    def response_required(self) -> bool:
        try:
            return self.values[Headers.RESPONSE_REQUIRED]
        except KeyError:
            pass

    @response_required.setter
    def response_required(self, response_required: bool):
        self.values[Headers.RESPONSE_REQUIRED] = response_required

    def with_response_required(self, response_required: bool) -> 'Headers':
        self.response_required = response_required
        return self

    @property
    def requested_acks(self) -> List[str]:
        try:
            return self.values[Headers.REQUESTED_ACKS]
        except KeyError:
            pass

    @requested_acks.setter
    def requested_acks(self, requested_acks: List[str]):
        self.values[Headers.REQUESTED_ACKS] = requested_acks

    def with_requested_acks(self, *args: str) -> 'Headers':
        self.requested_acks = list(args)
        return self

    @property
    def ditto_weak_ack(self) -> bool:
        try:
            return self.values[Headers.DITTO_WEAK_ACK]
        except KeyError:
            pass

    @ditto_weak_ack.setter
    def ditto_weak_ack(self, ditto_weak_ack: bool):
        self.values[Headers.DITTO_WEAK_ACK] = ditto_weak_ack

    def with_ditto_weak_ack(self, ditto_weak_ack: bool) -> 'Headers':
        self.ditto_weak_ack = ditto_weak_ack
        return self

    @property
    def timeout(self) -> str:
        try:
            return self.values[Headers.TIMEOUT]
        except KeyError:
            pass

    @timeout.setter
    def timeout(self, timeout: str):
        self.values[Headers.TIMEOUT] = timeout

    def with_timeout(self, timeout: str) -> 'Headers':
        self.timeout = timeout
        return self

    @property
    def version(self) -> str:
        try:
            return self.values[Headers.SCHEMA_VERSION]
        except KeyError:
            pass

    @version.setter
    def version(self, version: str):
        self.values[Headers.SCHEMA_VERSION] = version

    def with_version(self, version: int) -> 'Headers':
        self.version = version
        return self

    @property
    def put_metadata(self) -> List[Any]:
        try:
            return self.values[Headers.PUT_METADATA]
        except KeyError:
            pass

    @put_metadata.setter
    def put_metadata(self, put_metadata: List[Any]):
        self.values[Headers.PUT_METADATA] = put_metadata

    def with_put_metadata(self, *args: Any) -> 'Headers':
        self.put_metadata = list(args)
        return self

    def with_custom(self, key: str, value: Any) -> 'Headers':
        self.values[key] = value
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.values.items() if v is not None}

    def from_ditto_dict(self, ditto_dictionary: Dict):
        if isinstance(ditto_dictionary, Dict):
            self.values = ditto_dictionary.copy()
            return self
        return ditto_dictionary
