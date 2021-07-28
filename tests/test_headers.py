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

from ditto.protocol.headers import *

expected_content_type = "application/json"
expected_correlation_id = "p-pdid6m-d0g4iuy765f8-33gyeld"
expected_ditto_originator = "test-ditto-originator"
expected_if_match = "test-if-match-string"
expected_if_none_match = "test-if-none-match-string"
expected_response_required = True
expected_requested_acks = ["twin-persisted"]
expected_ditto_weak_ack = False
expected_timeout = "42s"
expected_version = 2
expected_put_metadata = [{"some": "data"}, {"other": "data"}]
expected_custom = "my-custom"

expected_values = {
    "content-type": expected_content_type,
    "correlation-id": expected_correlation_id,
    "ditto-originator": expected_ditto_originator,
    "If-Match": expected_if_match,
    "If-None-Match": expected_if_none_match,
    "response-required": expected_response_required,
    "requested-acks": expected_requested_acks,
    "ditto-weak-ack": expected_ditto_weak_ack,
    "timeout": expected_timeout,
    "version": expected_version,
    "put-metadata": expected_put_metadata,
    "custom": expected_custom
}


def test_json_full_headers():
    headers = Headers()
    headers.from_ditto_dict(expected_values)

    assert headers.content_type == expected_content_type
    assert headers.correlation_id == expected_correlation_id
    assert headers.ditto_originator == expected_ditto_originator
    assert headers.if_match == expected_if_match
    assert headers.if_none_match == expected_if_none_match
    assert headers.response_required == expected_response_required
    assert headers.requested_acks == expected_requested_acks
    assert headers.ditto_weak_ack == expected_ditto_weak_ack
    assert headers.timeout == expected_timeout
    assert headers.version == expected_version
    assert headers.put_metadata == expected_put_metadata
    assert headers.values["custom"] == expected_custom
    assert headers.values == expected_values


def test_json_marshal_full():
    headers = Headers()
    headers.values = expected_values.copy()
    actual_dict = headers.to_ditto_dict()

    assert headers.content_type == expected_content_type
    assert headers.correlation_id == expected_correlation_id
    assert headers.ditto_originator == expected_ditto_originator
    assert headers.if_match == expected_if_match
    assert headers.if_none_match == expected_if_none_match
    assert headers.response_required == expected_response_required
    assert headers.requested_acks == expected_requested_acks
    assert headers.ditto_weak_ack == expected_ditto_weak_ack
    assert headers.timeout == expected_timeout
    assert headers.version == expected_version
    assert headers.put_metadata == expected_put_metadata
    assert headers.values["custom"] == expected_custom
    assert actual_dict == expected_values


def test_builder_methods():
    headers = Headers(). \
        with_content_type(expected_content_type). \
        with_correlation_id(expected_correlation_id). \
        with_ditto_originator(expected_ditto_originator). \
        with_if_match(expected_if_match). \
        with_if_none_match(expected_if_none_match). \
        with_response_required(expected_response_required). \
        with_requested_acks(expected_requested_acks[0]). \
        with_ditto_weak_ack(expected_ditto_weak_ack). \
        with_timeout(expected_timeout). \
        with_version(expected_version). \
        with_put_metadata(expected_put_metadata[0], expected_put_metadata[1]). \
        with_custom("custom", expected_custom)

    assert headers.values == expected_values


def test_setters():
    headers = Headers()
    headers.content_type = expected_content_type
    headers.correlation_id = expected_correlation_id
    headers.ditto_originator = expected_ditto_originator
    headers.if_match = expected_if_match
    headers.if_none_match = expected_if_none_match
    headers.response_required = expected_response_required
    headers.requested_acks = expected_requested_acks
    headers.ditto_weak_ack = expected_ditto_weak_ack
    headers.timeout = expected_timeout
    headers.version = expected_version
    headers.put_metadata = expected_put_metadata
    headers.values["custom"] = expected_custom

    assert headers.values == expected_values
    assert headers.to_ditto_dict() == expected_values
