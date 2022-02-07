# Eclipse Ditto Client SDK for Python

[![Join the chat at https://gitter.im/eclipse/ditto](https://badges.gitter.im/eclipse/ditto.svg)](https://gitter.im/eclipse/ditto?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/badge/License-EPL%202.0-green.svg)](https://opensource.org/licenses/EPL-2.0)

This repository contains the Python client SDK for [Eclipse Ditto](https://eclipse.org/ditto/).

## Table of Contents
* [Installation](#Installation)
* [Creating and connecting a client](#Creating-and-connecting-a-client)
  * [Creating a client instance as a class](#Creating-a-client-instance-as-a-class)
  * [Connecting an external paho client](#Connecting-an-external-paho-client)
* [Working with features](#Working-with-features)
  * [Creating a new feature instance](#Creating-a-new-feature-instance)
  * [Modifying a feature's property](#Modifying-a-feature's-property)
  * [Deleting a feature's property](#Deleting-a-feature's-property)
  * [Deleting a feature](#Deleting-a-feature)
* [Subscribing and handling messages](#Subscribing-and-handling-messages)
* [Logging](#Logging)

## Installation

Install the sources and execute the following command:

```commandline
make install
```

## Creating and connecting a client

It is a good practice to have a defined behaviour after connecting or disconnecting the client.

```python    
def on_connect(ditto_client: Client):
    print("Ditto client connected")

def on_disconnect(ditto_client: Client):
    print("Ditto client disconnected")
```

With these configurations a client instance can be created.

```python
client = Client(on_connect=on_connect, on_disconnect=on_disconnect)
```

After the client is created, it's ready to be connected.

```python
client.connect("localhost")
```

The client can be also connected with custom connection configurations.

```python
client.connect("localhost", port=1883, keepalive=60)
```

Full example of the basic client connection can be found [here](examples/client_connect.py).

### Creating a client instance as a class

It is possible to create a client instance by inheriting the Client class. The `on_connect` and `on_disconnect` callback methods should be overridden in order to be configured. A separate method can be created in order to connect the client. This allows the client to be connected with custom configurations.

```python
class MyClient(Client):
    def on_connect(self, ditto_client: Client):
        print("Ditto client connected")
        
    def on_disconnect(self, ditto_client: Client):
        print("Ditto client disconnected")
        
    def run(self):
        self.connect("localhost", port=1883, keepalive=60)
```

Full example of the client connection as a class can be found [here](examples/client_connect_as_class.py).

### Connecting an external paho client

It is also possible to create a client instance using external paho client, which allows adding custom topics and messages that are not supported in Ditto.

Firstly, a custom `MyClient` class is created by inheriting the Client class.

Then a custom paho `on_connect()` callback method is created. It will create an instance of `MyClient`, providing the connected external paho client.

```python
ditto_client: Client = None

def paho_on_connect(client, userdata, flags, rc):
    global ditto_client
    ditto_client = MyClient(paho_client=client)
    ditto_client.enable_logger(True)
    ditto_client.connect()
```

Finally, the paho client can be connected. 

```python
try:
    paho_client = mqtt.Client()
    paho_client.on_connect = paho_on_connect
    paho_client.connect("localhost")
    paho_client.loop_forever()
except KeyboardInterrupt:
    print("finished")
    ditto_client.disconnect()
    paho_client.disconnect()
    sys.exit()
```

**_NOTE:_** Both the Ditto client and the external paho client must be disconnected before terminating the program.

Full example of the client connection using an external paho client can be found [here](examples/client_connect_as_class_external_paho.py).

## Working with features

Before sending any commands regarding features, there must be a client connected.

### Creating a new feature instance

A feature instance can be created with definition ID, properties, and/or desired properties.

```python
myFeature = Feature()
    .with_definition_from("my.model.namespace:FeatureModel:1.0.0")
    .with_property("myProperty", "myValue")
```

Then a Ditto command can be created. Modify acts as an upsert - it either creates a feature or updates it if it already exists.
The ID provided in `feature()` is used to recognize the feature which will be created/updated. 

```python
command = Command(NamespacedID().from_string("test.ns:test-name"))
    .feature("myFeatureID")
    .twin()
    .modify(myFeature)
```

The command can be now wrapped in an envelope and sent.

```python
envelope = command.envelope(response_required=False)
client.send(envelope)
```

### Modifying a feature's property

Modify overrides the current feature's property.

```python
command = Command(NamespacedID().from_string("test.ns:test-name"))
    .feature_property("myFeatureID", "myProperty")
    .twin()
    .modify("myModifiedValue")
```

The command can be now wrapped in an envelope and sent.

```python
envelope = command.envelope(response_required=False)
client.send(envelope) 
```

### Deleting a feature's property

Delete command is created using the feature's ID and the property's name.

```python
command = Command(NamespacedID().from_string("test.ns:test-name"))
    .feature_property("myFeatureID", "myProperty")
    .twin()
    .delete()
```

The command can now be wrapped in an envelope and sent.
```python
envelope = command.envelope(response_required=False)
client.send(envelope) 
```

### Deleting a feature

A feature can be deleted with a command with the appropriate feature's ID.

```python
command = Command(NamespacedID().from_string("test.ns:test-name"))
    .feature("myFeatureID")
    .twin()
    .delete()
```

The command can now be wrapped in an envelope and sent.
```python
envelope = command.envelope(response_required=False)
client.send(envelope) 
```

Full example of working with features can be found [here](examples/working_with_features.py).

## Subscribing and handling messages

Every client instance can subscribe for incoming Ditto messages. This usually happens right after the client is connected.

```python
def on_connect(ditto_client: Client):
    print("Ditto client connected")

    # Subscribe for incoming messages
    ditto_client.subscribe(on_message)
```

**_NOTE:_** Multiple handlers can be added for Ditto messages processing.

It is a good practice to clear all subscriptions before disconnecting the client.

```python
def disconnect(ditto_client: Client):
    client.unsubscribe()
    client.disconnect()
```

**_NOTE:_** If no message handlers are provided to `unsubscribe()` then all will be removed.

Now when a message is received it can be handled and replied to.

```python
def on_message(request_id: str, message: Envelope):
    # get the thing id from the topic of the incoming message
    incoming_thing_id = NamespacedID(message.topic.namespace, message.topic.entity_id)

    # create an example outbox message and reply
    live_message = Message(incoming_thing_id).outbox(message_subject).with_payload(
        dict(a="b", x=2))
    
    # generate the respective Envelope
    response_envelope = live_message.envelope(correlation_id=message.headers.correlation_id,
                                              response_required=False).with_status(200)
    # send the reply
    self.reply(request_id, response_envelope)
```

Full example of the subscribing and handling messages can be found [here](examples/message_request_response_handling.py).

## Logging

The default logger can be used in order to log events, regarding the client.

```python
client.enable_logger(True)
```

Alternatively, an external logger can be also provided.

```python
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
client.enable_logger(True, logger)
```

**_NOTE:_** The logger must be enabled before connecting the client.
