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

from ...protocol.envelope import Envelope
from ...protocol.headers import Headers
from ...protocol.topic import Topic


class _Signal(object):
    _path_thing = "/"
    _path_thing_definition = "/definition"
    _path_thing_policy_id = "/policyId"
    _path_thing_features = "/features"
    _path_thing_attributes = "/attributes"
    _path_thing_attribute_format = _path_thing_attributes + "/{}"
    _path_thing_feature_format = _path_thing_features + "/{}"
    _path_thing_feature_definition_format = _path_thing_feature_format + "/definition"
    _path_thing_feature_properties_format = _path_thing_feature_format + "/properties"
    _path_thing_feature_property_format = _path_thing_feature_properties_format + "/{}"
    _path_thing_feature_desired_properties_format = _path_thing_feature_format + "/desiredProperties"
    _path_thing_feature_desired_property_format = _path_thing_feature_desired_properties_format + "/{}"

    _payload_converter_func_name = "to_ditto_dict"

    def __init__(self,
                 topic: Topic = None,
                 path: str = None,
                 payload: Any = None):
        self.topic = topic
        self.path = path
        self.payload = payload

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
            .with_path(self.path) \
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
