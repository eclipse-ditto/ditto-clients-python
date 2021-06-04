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
    matched_groups = __regex_hono_mqtt_topic_request.findall(hono_topic)
    if matched_groups and len(*matched_groups) == 2:
        return matched_groups[0][0]
    return ""


def _generate_hono_response_topic(request_id: str, status: int) -> str:
    return __hono_mqtt_topic_command_response_format.format(request_id, status)


def _get_envelope(mqtt_message_payload) -> Envelope:
    envelope = Envelope()
    json.loads(mqtt_message_payload, object_hook=envelope.from_ditto_dict)
    return envelope
