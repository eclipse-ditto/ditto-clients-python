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
import logging
import threading
import time
import typing
import uuid
from typing import Callable

import paho.mqtt.client as mqtt

from .protocol.envelope import Envelope
from .rw_lock import _RWLock
# Log levels
from .utils import _generate_hono_response_topic, _get_envelope, _extract_hono_req_id

LOG_LEVEL_INFO = 0x01
LOG_LEVEL_NOTICE = 0x02
LOG_LEVEL_WARNING = 0x04
LOG_LEVEL_ERROR = 0x08
LOG_LEVEL_DEBUG = 0x10
STANDARD_PY_LOGGING_LEVEL = {
    LOG_LEVEL_DEBUG: logging.DEBUG,
    LOG_LEVEL_INFO: logging.INFO,
    LOG_LEVEL_NOTICE: logging.INFO,
    LOG_LEVEL_WARNING: logging.WARNING,
    LOG_LEVEL_ERROR: logging.ERROR,
}


class Client:
    """
    Represents the key entry and usage point of the library.

    The client has connect/disconnect capabilities along with the options to subscribe/unsubscribe
    for receiving all Ditto messages
    """
    _default_keep_alive = 30
    __hono_mqtt_topic_subscribe_commands = "command///req/#"
    __hono_mqtt_topic_publish_telemetry = "t"
    __hono_mqtt_topic_publish_events = "e"

    def __init__(
            self,
            on_connect: typing.Callable = None,
            on_disconnect: typing.Callable = None,
            on_log: typing.Callable = None,
            paho_client: mqtt.Client = None):
        """
        Initializes a Client instance with the provided on_connect, on_disconnect and on_log callback
        functions as well as an optional external paho client.

        The MQTT client may be internal or external. If using internal MQTT client, than on_connect,
        on_disconnect and on_log callback functions may be given for notifying upon certain events.
        A MQTT client is created and used in this Client instance.
        If using external MQTT client, than it must be connected prior to initializing a Client instance.

        :param on_connect: func(client:Client) - notified when the client is connected. Optional.
        :type on_connect: typing.Callable
        :param on_disconnect: func(client:Client) - notified when the client is disconnected.  Optional.
        :type on_disconnect: typing.Callable
        :param on_log: func(client:Client, log_level, log_msg:str) - notified each time there is a log entry in the
            Client. Optional. Can be enabled, switched and disabled via the Client#enable_logger() function.
        :type on_log: typing.Callable
        :param paho_client: An optional externally provided Paho MQTT client.
        :type paho_client: mqtt.Client
        """
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._on_log = on_log
        self._logger = None
        self._paho_client = paho_client
        self._handlers = []
        self._handlers_lock = _RWLock()
        self._external_mqtt_client = self._paho_client is not None
        if self._external_mqtt_client:
            if not self._paho_client.is_connected():
                raise RuntimeError("MQTT client is not connected!")
        else:
            self._paho_client = mqtt.Client(uuid.uuid1().__str__(), clean_session=True)
            self._paho_client.on_connect = self._on_paho_connect
            self._paho_client.on_disconnect = self._on_paho_disconnect
            self._paho_client.on_message = self._on_paho_message

    @property
    def on_connect(self) -> typing.Callable:
        """
        If set, called when a successful connection to the configured Ditto endpoint is established and all
        Client's internal preparations are done

        :returns: Callback function, invoked when the Client is fully initialized
        :rtype: typing.Callable
        """
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func: typing.Callable):
        """
        Defines the connect callback implementation.

        Expected signature is:
            connect_callback(client)

        client (Client): The client instance for this callback

        :param func: The connect callback implementation
        :type func: typing.Callable
        """
        self._on_connect = func

    @property
    def on_disconnect(self) -> typing.Callable:
        """
        If set, called when a disconnection from the configured Ditto endpoint has occurred and all
        Client's resources have been cleaned up.

        :returns: Callback function, invoked when the Client's resources are fully cleaned up
        :rtype: typing.Callable
        """
        return self._on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, func: typing.Callable):
        """
        Defines the disconnect callback implementation.

        Expected signature is:
            disconnect_callback(client)

        client (Client): The client instance for this callback

        :param func: The disconnect callback implementation
        :type func: typing.Callable
        """
        self._on_disconnect = func

    @property
    def on_log(self) -> typing.Callable:
        """
        If set, called when the client has log information.

        :returns: Callback function, invoked when the client logs a message
        :rtype: typing.Callable
        """
        return self._on_log

    @on_log.setter
    def on_log(self, func: typing.Callable):
        """
        Defines the logging callback implementation.

        Expected signature is:
            log_callback(client, log_level, log_message)

        client (Client): the client instance for this callback
        log_level (int): gives the severity of the message (one of INFO, NOTICE, WARNING, ERROR, and DEBUG)
        log_message (str): the message of the log

        :param func: The logging callback implementation
        :type func: typing.Callable
        """
        self._on_log = func

    def enable_logger(self, enable: bool, logger=None):
        """
        Enables or disables the logger for the client. If a logger is not passed, when the operation is "enable",
        then the default logger is used.

        :param enable: True or False, depending on whether the desired operation is enable or disable.
        :type enable: bool
        :param logger: Logger to be set, if logger is None, then the default logger object is used.
        :type logger: Logger
        """
        if not enable:
            self._logger = None
            return
        if logger is None:
            if self._logger is None:
                logger = logging.getLogger(__name__)
            else:
                return
        self._logger = logger

    def configure_credentials(self, username: str, password: str = None):
        """
        Sets a username and optionally a password for broker authentication.

        Must be called before connect() to have any effect.
        Requires a broker that supports MQTT v3.1.

        :param username: Username for authentication used by the underlying connection (e.g. MQTT)
        :type username: str
        :param password: Password for authentication used by the underlying connection (e.g. MQTT)
        :type password: str
        """
        self._paho_client.username_pw_set(username=username, password=password)

    def configure_tls(self, ca_certs: str = None, certfile: str = None, keyfile: str = None, cert_reqs: int = None,
                      tls_version: int = None, ciphers: str = None):
        """
        Configures network encryption and authentication options. Enables SSL/TLS support.

        Must be called before connect()!

        :param ca_certs: Path to CA certificates
        :type ca_certs: str
        :param certfile: Path to server certificate
        :type certfile: str
        :param keyfile: Path to server key
        :type keyfile: str
        :param cert_reqs: Enum value for certificate requirement (NONE, OPTIONAL, REQUIRED)
        :type cert_reqs: int
        :param tls_version: Version of TLS
        :type tls_version: int
        :param ciphers: The encryption cipher
        :type ciphers: str
        """
        self._paho_client.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile, cert_reqs=cert_reqs,
                                  tls_version=tls_version, ciphers=ciphers)

    def connect(self, host: typing.Any = None, port: int = 1883, keep_alive: int = _default_keep_alive):
        """
        Connects the initialized Client instance.

        Can be called multiple times without reinitializing the other configurations done at creation time.

        :param host: The MQTT host to connect to.
        :type host: typing.Any
        :param port: The MQTT port to connect to (the default is 1883).
        :type port: int
        :param keep_alive: The connection keep alive notifications interval (default is 30 seconds).
        :type keep_alive: int
        """
        if self._external_mqtt_client:
            self.__log(LOG_LEVEL_WARNING,
                       "any default or provided connect parameters will be ignored "
                       "as an external Paho client is used: host={}, port={}, keep_alive={}",
                       host, port, keep_alive)
            self._paho_client.message_callback_add(Client.__hono_mqtt_topic_subscribe_commands, self._on_paho_message)
            self._paho_client.subscribe(Client.__hono_mqtt_topic_subscribe_commands, qos=1)
            notify_thread = threading.Thread(target=self.__notify_client_on_connect())
            notify_thread.start()
        else:
            self._paho_client.connect(host, port, keep_alive)
            self._paho_client.loop_start()

    def disconnect(self):
        """
        Disconnects the initialized Client instance.
        """
        try:
            self._paho_client.unsubscribe(Client.__hono_mqtt_topic_subscribe_commands)
            if self._external_mqtt_client:
                self.__notify_client_on_disconnect(0)
            else:
                self._paho_client.loop_stop()
                self._paho_client.disconnect()
        except Exception as err:
            self.__log(LOG_LEVEL_ERROR, "error while disconnecting client: {}", err)

    def reply(self, request_id: str, message: Envelope):
        """
        Publishes a message as a response, whose topic is generated using the given request id.

        :param request_id: The id of the request
        :type request_id: str
        :param message: The response message object using Envelope class
        :type message: Envelope
        """
        self._publish(_generate_hono_response_topic(request_id, message.status), message)

    def send(self, message: Envelope):
        """
        Publishes a message for an event.

        :param message: The message object using Envelope class
        :type message: Envelope
        """
        self._publish(Client.__hono_mqtt_topic_publish_events, message)

    def subscribe(self, *args: Callable):
        """
        Adds one or more handler functions to the list of client's handlers.

        :param args: Iterable of handlers or comma-separated handlers that are invoked when a message is received.
        :type args: typing.Callable
        """
        try:
            self._handlers_lock.lock_write()
            if self._handlers is None:
                self._handlers = []
            if args:
                for func in args:
                    self._handlers.append(func)
                    self.__log(LOG_LEVEL_DEBUG, "added new message handler {}", func)
        except Exception as err:
            self.__log(LOG_LEVEL_ERROR, "error adding new messages handler: err: {}", err)
        finally:
            self._handlers_lock.unlock_write()

    def unsubscribe(self, *args: Callable):
        """
        Removes a certain, some or all handler functions from the list of client's handlers.

        :param args: Optional. Iterable of handlers or comma-separated handlers, that will be removed from the client's
            handlers list. If args is not given, then all handlers will be removed.
        :type args: typing.Callable
        """
        try:
            self._handlers_lock.lock_write()
            funcs_to_remove = self._handlers if args is None else args
            for func in funcs_to_remove:
                self._handlers.remove(func)
                self.__log(LOG_LEVEL_DEBUG, "removed message handler {}", func)
        except Exception as err:
            self.__log(LOG_LEVEL_ERROR, "error removing messages handler: err: {}", err)
        finally:
            self._handlers_lock.unlock_write()

    def _on_paho_connect(self, client, userdata, flags, rc):
        try:
            self._paho_client.subscribe(Client.__hono_mqtt_topic_subscribe_commands, qos=1)
        except ValueError as err:
            self.__log(LOG_LEVEL_ERROR, "error subscribing: {}", err)
        self.__notify_client_on_connect()

    def _on_paho_disconnect(self, client, userdata, rc):
        self.__notify_client_on_disconnect(rc)

    def _on_paho_message(self, client, userdata, msg: mqtt.MQTTMessage):
        self.__log(LOG_LEVEL_DEBUG, "received MQTT message: topic : {}, payload: {}", msg.topic, msg.payload)
        try:
            self._handlers_lock.lock_read()
            if self._handlers is None or len(self._handlers) == 0:
                self.__log(LOG_LEVEL_DEBUG, "no handlers available to transfer the message to")
                return
            envelope = _get_envelope(msg.payload)
            request_id = _extract_hono_req_id(msg.topic)

            if not request_id:
                self.__log(LOG_LEVEL_DEBUG, "the received MQTT message is one-way - it does not have a request ID in "
                                            "topic {}", msg.topic)
            else:
                self.__log(LOG_LEVEL_DEBUG, "received MQTT message with request ID = {}", request_id)

            for handler_func in self._handlers:
                message_thread = threading.Thread(target=handler_func, args=(request_id, envelope,))
                message_thread.start()
        except Exception as err:
            self.__log(LOG_LEVEL_ERROR, "error handling received MQTT message: err: {}", err)
        finally:
            self._handlers_lock.unlock_read()

    def _publish(self, topic: str, message: Envelope, qos: int = 1, retained: bool = False):
        ditto_dict = message.to_ditto_dict()
        try:
            json_buf = json.dumps(ditto_dict)
            self._paho_client.publish(topic, json_buf, qos, retained)
        except Exception as err:
            self.__log(LOG_LEVEL_ERROR, "could not send the provided message {} err: {}", ditto_dict, err)
            raise err

    def __notify_client_on_connect(self):
        if self.on_connect is None:
            return
        notify_thread = threading.Thread(target=self.on_connect, args=(self,))
        notify_thread.start()
        start_time = time.time()
        notify_thread.join(60)
        if notify_thread.is_alive() and time.time() - start_time > 60 * 1000:
            self.__log(LOG_LEVEL_ERROR, "timed out waiting for on_connect notification to be handled")
        else:
            self.__log(LOG_LEVEL_DEBUG, "successfully notified client for on_connect")

    def __notify_client_on_disconnect(self, rc):
        if self.on_disconnect is None:
            return
        notify_thread = threading.Thread(target=self.on_disconnect, args=(self,))
        notify_thread.start()
        start_time = time.time()
        notify_thread.join(60)
        if notify_thread.is_alive() and time.time() - start_time > 60 * 1000:
            self.__log(LOG_LEVEL_ERROR, "timed out waiting for on_disconnect notification to be handled")
        else:
            self.__log(LOG_LEVEL_DEBUG, "successfully notified client for on_disconnect")

    def __log(self, level, log_msg_formatter, *args):
        if self.on_log is not None:
            log_msg = log_msg_formatter.format(*args)
            try:
                self.on_log(self, level, log_msg)
            except Exception:
                pass
        if self._logger is not None:
            to_standard_lvl = STANDARD_PY_LOGGING_LEVEL[level]
            self._logger.log(to_standard_lvl, log_msg_formatter.format(*args))
