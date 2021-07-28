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

from ditto.protocol.envelope import Envelope

full_dict = {
    "topic": "my.ns/my.dev/things/live/messages/testCommand",
    "headers": {
        "content-type": "application/json",
        "correlation-id": "p-pdid6j-899vvx1b69if8-1hjfb46",
        "ditto-message-direction": "TO",
        "ditto-message-feature-id": "MyFeature",
        "ditto-message-subject": "testCommand",
        "ditto-message-thing-id": "my.ns:my.dev",
        "ditto-originator": "some-ditto-originator",
        "requested-acks": [],
        "response-required": True,
        "version": 2,
        "x-things-parameter-order": "[\"arg1\",\"arg2\",\"arg3\",\"arg4\"]"
    },
    "path": "/features/MyFeature/inbox/messages/testCommand",
    "value": {
        "arg1": "docker.io/library/some:latest",
        "arg2": "test-ctr",
        "arg3": {
            "domainName": "test-domain",
            "mountPoints": [
                {
                    "source": "/some/source",
                    "destination": "/some/dest",
                    "propagationMode": "rprivate"
                }
            ],
            "devices": [
                {
                    "pathOnHost": "/dev/ttyACM0",
                    "pathInContainer": "/dev/ttyACM0",
                    "cgroupPermissions": "rwm"
                }
            ],
            "restartPolicy": {
                "maxRetryCount": 5,
                "retryTimeout": 6,
                "type": "UNLESS_STOPPED"
            },
            "extraHosts": [
                "edgehost:182.123.123.123"
            ],
            "portMappings": [
                {
                    "proto": "tcp",
                    "hostPort": 80,
                    "hostPortEnd": 80,
                    "containerPort": 80,
                    "hostIP": "0.0.0.0"
                }
            ],
            "log": {
                "type": "JSON_FILE",
                "maxFiles": 5,
                "maxSize": "512M",
                "rootDir": "/some/root/dir",
                "mode": "BLOCKING",
                "maxBufferSize": "512"
            }
        },
        "arg4": False
    }
}

full_dict_timestamped = '{"topic": "led_raspberry/myRspbLed/things/live/messages/ledColor",\
    "headers": {\
        "version": 2,\
        "accept": "*/*",\
        "accept-encoding": "gzip, deflate",\
        "timeout": "0",\
        "response-required": false,\
        "ditto-originator": "some-originator",\
        "requested-acks": [],\
        "ditto-message-direction": "TO",\
        "ditto-message-subject": "ledColor",\
        "ditto-message-thing-id": "led_raspberry:myRspbLed",\
        "ditto-message-feature-id": "ledLights",\
        "correlation-id": "2ee49e62-f8d7-44f9-b070-2be42e69c077",\
        "content-type": "text/plain; charset=UTF-8",\
        "timestamp": "2021-06-03T14:08:53.827760996+02:00"\
    },\
    "path": "/features/ledLights/inbox/messages/ledColor",\
    "value": "#7fff00"\
}'


def test_all():
    env = Envelope().from_ditto_dict(full_dict)
    assert env.headers.to_ditto_dict() == full_dict["headers"]
    assert env.topic.namespace == "my.ns"
    assert env.topic.entity_id == "my.dev"
    assert env.headers.values["x-things-parameter-order"] == full_dict["headers"]["x-things-parameter-order"]
    assert env.to_ditto_dict() == full_dict


def test_from_string_payload():
    envelope = Envelope()
    json.loads(full_dict_timestamped, object_hook=envelope.from_ditto_dict)
    as_dict = json.loads(full_dict_timestamped)
    assert envelope.to_ditto_dict() == as_dict
