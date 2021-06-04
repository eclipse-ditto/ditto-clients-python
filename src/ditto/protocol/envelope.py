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

from typing import Any, Dict

from ..protocol.headers import Headers
from ..protocol.topic import Topic


class Envelope(object):
    """
    Envelope represents the Ditto's Envelope specification.
    As a Ditto's message consists of an envelope along with a Ditto-compliant payload.
    """

    # Literals needed for the conversion of the Envelope instance from and to the desired Ditto JSON format.
    __ditto_json_key_topic = "topic"
    __ditto_json_key_headers = "headers"
    __ditto_json_key_path = "path"
    __ditto_json_key_value = "value"
    __ditto_json_key_fields = "fields"
    __ditto_json_key_extra = "extra"
    __ditto_json_key_status = "status"
    __ditto_json_key_revision = "revision"
    __ditto_json_key_timestamp = "timestamp"
    __ditto_json_keys_all = [__ditto_json_key_topic,
                             __ditto_json_key_headers,
                             __ditto_json_key_path,
                             __ditto_json_key_value,
                             __ditto_json_key_fields,
                             __ditto_json_key_extra,
                             __ditto_json_key_status,
                             __ditto_json_key_revision,
                             __ditto_json_key_timestamp]

    def __init__(self,
                 topic: Topic = None,
                 headers: Headers = None,
                 path: str = None,
                 value: Any = None,
                 fields: str = None,
                 extra: Any = None,
                 status: int = None,
                 revision: int = None,
                 timestamp: str = None):
        """

        :param topic:
        :param headers:
        :param path:
        :param value:
        :param fields:
        :param extra:
        :param status:
        :param revision:
        :param timestamp:
        """
        self.topic = topic
        self.headers = headers
        if not self.headers:
            self.headers = Headers()
        self.path = path
        self.value = value
        self.fields = fields
        self.extra = extra
        self.status = status
        self.revision = revision
        self.timestamp = timestamp

    def with_topic(self, topic: Topic) -> 'Envelope':
        """
        Configures the topic of the Envelope.

        :param topic:
        :return:
        """
        self.topic = topic
        return self

    def with_headers(self, headers: Headers) -> 'Envelope':
        """
        Configures the headers of the Envelope.

        :param headers:
        :return:
        """
        self.headers = headers
        return self

    def with_path(self, path: str) -> 'Envelope':
        """
        Configures the Ditto path of the Envelope.

        :param path:
        :return:
        """
        self.path = path
        return self

    def with_value(self, value: Any) -> 'Envelope':
        """
        Configures the Ditto value of the Envelope.

        :param value:
        :return:
        """
        self.value = value
        return self

    def with_fields(self, fields: str) -> 'Envelope':
        """
        Configures the fields of the Envelope as defined by the Ditto protocol specification.

        :param fields:
        :return:
        """
        self.fields = fields
        return self

    def with_extra(self, extra: Any) -> 'Envelope':
        """
        Configures any extra Envelope configurations as defined by the Ditto protocol specification.

        :param extra:
        :return:
        """
        self.extra = extra
        return self

    def with_status(self, status: int) -> 'Envelope':
        """
        Configures the status of the Envelope based on the HTTP codes available.

        :param status:
        :return:
        """
        self.status = status
        return self

    def with_revision(self, revision: int) -> 'Envelope':
        """
        Configures the current revision number of an entity this Envelope refers to.

        :param revision:
        :return:
        """
        self.revision = revision
        return self

    def with_timestamp(self, timestamp: str) -> 'Envelope':
        """
        Configures the timestamp of the Envelope.

        :param timestamp:
        :return:
        """
        self.timestamp = timestamp
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        """

        :return:
        """
        envelope_dict = {
            Envelope.__ditto_json_key_topic: self.topic.__str__()
        }
        if self.headers is not None:
            envelope_dict[Envelope.__ditto_json_key_headers] = self.headers.to_ditto_dict()

        envelope_dict[Envelope.__ditto_json_key_path] = self.path
        envelope_dict[Envelope.__ditto_json_key_value] = self.value
        envelope_dict[Envelope.__ditto_json_key_fields] = self.fields
        envelope_dict[Envelope.__ditto_json_key_extra] = self.extra
        envelope_dict[Envelope.__ditto_json_key_status] = self.status
        envelope_dict[Envelope.__ditto_json_key_revision] = self.revision
        envelope_dict[Envelope.__ditto_json_key_timestamp] = self.timestamp

        return {k: v for k, v in envelope_dict.items() if v is not None}

    def from_ditto_dict(self, ditto_dictionary: Dict):
        """

        :param ditto_dictionary:
        :return:
        """
        if (list(set(ditto_dictionary.keys()) & set(
                Envelope.__ditto_json_keys_all))) and Envelope.__ditto_json_key_topic in ditto_dictionary.keys():
            if Envelope.__ditto_json_key_topic in ditto_dictionary:
                self.topic = Topic().from_string(ditto_dictionary[Envelope.__ditto_json_key_topic])
            if Envelope.__ditto_json_key_headers in ditto_dictionary:
                self.headers = Headers().from_ditto_dict(ditto_dictionary[Envelope.__ditto_json_key_headers])
            else:
                self.headers = Headers()
            if Envelope.__ditto_json_key_path in ditto_dictionary:
                self.path = ditto_dictionary[Envelope.__ditto_json_key_path]
            if Envelope.__ditto_json_key_value in ditto_dictionary:
                self.value = ditto_dictionary[Envelope.__ditto_json_key_value]
            if Envelope.__ditto_json_key_status in ditto_dictionary:
                self.status = ditto_dictionary[Envelope.__ditto_json_key_status]
            if Envelope.__ditto_json_key_fields in ditto_dictionary:
                self.fields = ditto_dictionary[Envelope.__ditto_json_key_fields]
            if Envelope.__ditto_json_key_extra in ditto_dictionary:
                self.extra = ditto_dictionary[Envelope.__ditto_json_key_extra]
            if Envelope.__ditto_json_key_revision in ditto_dictionary:
                self.revision = ditto_dictionary[Envelope.__ditto_json_key_revision]
            if Envelope.__ditto_json_key_timestamp in ditto_dictionary:
                self.timestamp = ditto_dictionary[Envelope.__ditto_json_key_timestamp]
            return self
        return ditto_dictionary
