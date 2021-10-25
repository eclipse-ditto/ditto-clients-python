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
        Initializes a new Envelope instance with the provided properties according to the Ditto specification.

        :param topic: Used for addressing an entity, defining the channel (twin/live) and specifying the intention of
            the Protocol message.
        :type topic: Topic
        :param headers: Represents all Ditto-specific headers along with additional HTTP/etc.
            See https://www.eclipse.org/ditto/protocol-specification.html
        :type headers: Headers
        :param path: References a part of a Thing which is affected by this message.
        :type path: str
        :param value: The JSON value to apply at the specified path.
        :type value: typing.Any
        :param fields: The fields that should be included in the response.
        :type fields: str
        :param extra: The extra object contains the extraFields which have optionally been selected to be
            included when using signal enrichment. (See https://www.eclipse.org/ditto/2.0/basic-enrichment.html)
        :type extra: typing.Any
        :param status: Some protocol messages (for example responses) contain a HTTP status code which is stored in this field.
        :type status: int
        :param revision: For events this field contains the revision number of the event.
        :type revision: int
        :param timestamp: For events this field contains the modification timestamp of the event.
        :type timestamp: str
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
        Sets the topic of the current Envelope instance to the provided Topic instance.

        :param topic: A path that specifies the address of the entity and the intention of the message.
        :type topic: Topic
        :returns: The updated Envelope instance with the provided topic.
        :rtype: Envelope
        """
        self.topic = topic
        return self

    def with_headers(self, headers: Headers) -> 'Envelope':
        """
        Sets the headers of the current Envelope instance to the provided Headers instance.

        :param headers: Protocol messages contain headers as JSON object with arbitrary content.
            See https://www.eclipse.org/ditto/protocol-specification.html.
        :type headers: Headers
        :returns: The updated Envelope instance with the provided headers.
        :rtype: Envelope
        """
        self.headers = headers
        return self

    def with_path(self, path: str) -> 'Envelope':
        """
        Sets the path of the current Envelope instance to the provided string.

        :param path: Contains a JSON pointer of where to apply the value of the protocol message.
            May also be / when the value contains a replacement for the complete addressed entity.
        :type path: str
        :returns: The updated Envelope instance with the provided path.
        :rtype: Envelope
        """
        self.path = path
        return self

    def with_value(self, value: Any) -> 'Envelope':
        """
        Sets the value of the current Envelope instance to the provided JSON value.

        :param value: The JSON value to apply at the message's specified path.
        :type value:typing.Any
        :returns: The updated Envelope instance with the provided value.
        :rtype: Envelope
        """
        self.value = value
        return self

    def with_fields(self, fields: str) -> 'Envelope':
        """
        Sets the fields of the current Envelope instance to the provided string.

        :param fields: The fields that should be included in the response.
        :type fields: str
        :returns: The updated Envelope instance with the provided fields.
        :rtype: Envelope
        """
        self.fields = fields
        return self

    def with_extra(self, extra: Any) -> 'Envelope':
        """
        Sets the extra field of the current Envelope instance to the provided JSON value.

        :param extra: The extra object contains the extraFields which have optionally been selected to be
            included when using signal enrichment. Events, for example, only contain the actually changed data by
            default, so it is often helpful to additionally include some extra fields as context to be included
            when subscribing.
        :type extra: typing.Any
        :returns: The updated Envelope instance with the provided extra.
        :rtype: Envelope
        """
        self.extra = extra
        return self

    def with_status(self, status: int) -> 'Envelope':
        """
        Sets the status of the current Envelope instance to the provided integer.

        :param status: Some protocol messages (for example responses) contain a HTTP status code which is stored in this field.
        :type status: int
        :returns: The updated Envelope instance with the provided status.
        :rtype: Envelope
        """
        self.status = status
        return self

    def with_revision(self, revision: int) -> 'Envelope':
        """
        Sets the revision of the current Envelope instance to the provided integer.

        :param revision: For events this field contains the revision number of the event.
        :type revision: int
        :returns: The updated Envelope instance with the provided revision.
        :rtype: Envelope
        """
        self.revision = revision
        return self

    def with_timestamp(self, timestamp: str) -> 'Envelope':
        """
        Sets the timestamp of the current Envelope instance to the provided string.

        :param timestamp: For events this field contains the modification timestamp of the event.
        :type timestamp: str
        :returns: The updated Envelope instance with the provided timestamp.
        :rtype: Envelope
        """
        self.timestamp = timestamp
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        """
        Converts the current Envelope instance into a dictionary
        that is compliant with the Ditto specification and is directly JSON serializable
        compliant with the Ditto format requirements.

        :returns: A dictionary representation of the Envelope instance compliant with the Ditto JSON format.
        :rtype: dict
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
        Enables initialization of the Envelope instance via a dictionary that is compliant with the Ditto specification.

        This method can be used in combination with the supported by Python object_hook configuration for loading JSON data.

        :param ditto_dictionary: The dictionary that is compliant with the Ditto specification.
        :type ditto_dictionary: typing.Dict
        :returns: The initialized Envelope instance if the dictionary is compliant with the Ditto specification.
            Otherwise, the input ditto_dictionary is returned.
        :rtype: Envelope
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
