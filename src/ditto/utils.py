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

import json
import re

from .protocol.envelope import Envelope

__hono_mqtt_topic_command_response_format = "command///res/{}/{}"
__regex_hono_mqtt_topic_request = re.compile("^command///req/([^/]*)/([^/]+)$")


def _extract_hono_req_id(hono_topic: str) -> str:
    """
    Extracts the Hono request id from the topic, using the Hono MQTT request topic regex

    :param hono_topic: The Hono request topic
    :type hono_topic: str
    :returns: The Hono request id if found, else ""
    :rtype: str
    """
    matched_groups = __regex_hono_mqtt_topic_request.findall(hono_topic)
    if matched_groups and len(*matched_groups) == 2:
        return matched_groups[0][0]
    return ""


def _generate_hono_response_topic(request_id: str, status: int) -> str:
    """
    Generates Hono response topic, using the Hono MQTT topic format for sending command responses.

    :param request_id: The request id, pointing to the sender of the request
    :type request_id: str
    :param status: The status code (using http status codes), representing the outcome of the operation,
        requested by the command
    :type status: int
    :returns: Formatted Hono MQTT topic for responding to a command
    :rtype: str
    """
    return __hono_mqtt_topic_command_response_format.format(request_id, status)


def _get_envelope(mqtt_message_payload) -> Envelope:
    """
    Loads the json from MQTT message payload into an instance of Envelope class

    :param mqtt_message_payload: The MQTT message payload
    :type mqtt_message_payload: str
    :returns: An instance of Envelope class containing the MQTT message
    :rtype: Envelope
    """
    envelope = Envelope()
    json.loads(mqtt_message_payload, object_hook=envelope.from_ditto_dict)
    return envelope
