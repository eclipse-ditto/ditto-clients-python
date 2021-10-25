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

from ..model.definition_id import DefinitionID
from ..model.feature import Feature
from ..model.namespaced_id import NamespacedID


class Thing(object):
    """
    Thing represents the Thing entity model form the Ditto's specification.
    Things are very generic entities and are mostly used as a “handle” for multiple features belonging to this Thing.
    """

    # Literals needed for the conversion of the Thing instance from and to the desired Ditto JSON format.
    __ditto_json_key_thing_id = "thingId"
    __ditto_json_key_policy_id = "policyId"
    __ditto_json_key_definition_id = "definition"
    __ditto_json_key_attributes = "attributes"
    __ditto_json_key_features = "features"
    __ditto_json_key__namespace = "_namespace"
    __ditto_json_key__revision = "_revision"
    __ditto_json_key__created = "_created"
    __ditto_json_key__modified = "_modified"
    __ditto_json_key__metadata = "_metadata"
    __ditto_json_keys_all = [__ditto_json_key_thing_id,
                             __ditto_json_key_policy_id,
                             __ditto_json_key_definition_id,
                             __ditto_json_key_attributes,
                             __ditto_json_key_features,
                             __ditto_json_key__namespace,
                             __ditto_json_key__revision,
                             __ditto_json_key__created,
                             __ditto_json_key__modified,
                             __ditto_json_key__metadata]

    def __init__(self,
                 thing_id: NamespacedID = None,
                 policy_id: NamespacedID = None,
                 definition: DefinitionID = None,
                 attributes: Dict[str, Any] = None,
                 features: Dict[str, Feature] = None,
                 revision: int = None,
                 created: str = None,
                 modified: str = None,
                 metadata: Any = None):
        """
        Initializes a new Thing instance with the provided properties according to the Ditto specification.

        :param thing_id: Unique identifier of a Thing. For choosing custom Thing IDs when creating a Thing.
            The rules for namespaced IDs apply.
        :type thing_id: NamespacedID
        :param policy_id: Links to the ID of an existing Policy which contains the authorization information applied for this Thing.
            The policy ID has to conform to the namespaced entity ID notation.
        :type policy_id: NamespacedID
        :param definition: The definition of this Thing declaring its model in the form 'namespace:name:version'.
        :type definition: DefinitionID
        :param attributes: The Attributes that describe this Thing in more detail. Can be an arbitrary JSON object.
            Attributes are typically used to model rather static properties at the Thing level.
            Static means that the values do not change as frequently as property values of Features.
        :type attributes: typing.Dict[str, typing.Any]
        :param features: The Features belonging to this Thing. A Thing can handle any number of Features.
            The key of this object represents the Feature's ID. Due to the fact that a Feature's ID often needs to be set
            in the path of a HTTP request, it is strongly recommended to use a restricted set of characters.
        :type features: typing.Dict[str, Feature]
        :param revision: The revision is a counter which is incremented on each modification of a Thing.
        :type revision: int
        :param created: The created timestamp of the Thing in ISO-8601 UTC format. The timestamp is set on creation.
        :type created: str
        :param modified: The modified timestamp of the Thing in ISO-8601 UTC format.
            The timestamp is set on each modification.
        :type modified: str
        :param metadata: The Metadata of the Thing. This field is not returned by default but must be selected explicitly.
            The content is a JSON object having the Thing's JSON structure with the difference that the JSON leaves
            of the Thing are JSON objects containing the metadata.
        :type metadata: typing.Any
        
        """
        self.thing_id = thing_id
        self.policy_id = policy_id
        self.definition = definition
        self.attributes = attributes
        if self.attributes is None:
            self.attributes = {}
        self.features = features
        if self.features is None:
            self.features = {}
        if thing_id:
            self.namespace = thing_id.namespace
        else:
            self.namespace = None
        self.revision = revision
        self.created = created
        self.modified = modified
        self.metadata = metadata

    def with_id(self, thing_id: NamespacedID) -> 'Thing':
        """
        Sets the provided NamespacedID as the current Thing's instance ID value.

        :param thing_id: Unique identifier of a Thing. For choosing custom Thing IDs when creating a Thing.
            The rules for namespaced IDs apply.
        :type thing_id: NamespacedID
        :returns: The updated Thing instance with the provided thing_id.
        :rtype: Thing
        """
        self.thing_id = thing_id
        return self

    def with_id_from(self, thing_id_str: str) -> 'Thing':
        """
        An auxiliary method that sets the ID value of the current Thing instance based on the provided string n the form of 'namespace:name'.

        :param thing_id_str: Unique identifier of a Thing. For choosing custom Thing IDs when creating a Thing.
            The rules for namespaced IDs apply.
        :type thing_id_str: str
        :returns: The updated Thing instance with the provided thing_id.
        :rtype: Thing
        """
        self.thing_id = NamespacedID().from_string(thing_id_str)
        return self

    def with_policy_id(self, policy_id: NamespacedID) -> 'Thing':
        """
        Sets the provided Policy ID to the current Thing instance.

        :param policy_id: Links to the ID of an existing Policy which contains the authorization information applied for this Thing.
            The policy ID has to conform to the namespaced entity ID notation.
        :type policy_id: NamespacedID
        :returns: The updated Thing instance with the provided policy_id.
        :rtype: Thing
        """
        self.policy_id = policy_id
        return self

    def with_policy_id_from(self, policy_id_str: str) -> 'Thing':
        """
        An auxiliary method that sets the Policy ID of the current Thing instance.

        :param policy_id_str: Links to the ID of an existing Policy which contains the authorization information applied for this Thing.
            The policy ID has to conform to the namespaced entity ID notation.
        :type policy_id_str: str
        :returns: The updated Thing instance with the provided policy_id.
        :rtype: Thing
        """
        self.policy_id = NamespacedID.from_string(policy_id_str)
        return self

    def with_definition(self, definition_id: DefinitionID) -> 'Thing':
        """
        Sets the current Thing instance's definition to the provided value.

        :param definition_id: The definition of this Thing declaring its model in the form 'namespace:name:version'.
        :type definition_id: DefinitionID
        :returns: The updated Thing instance with the provided definition.
        :rtype: Thing
        """
        self.definition = definition_id
        return self

    def with_definition_from(self, definition_id_str: str) -> 'Thing':
        """
        An auxiliary method to set the current Thing instance's definition to the provided one in the form of 'namespace:name:version'.

        :param definition_id_str: The definition of this Thing declaring its model in the form 'namespace:name:version'.
        :type definition_id_str: str
        :returns: The updated Thing instance with the provided definition.
        :rtype: Thing
        """
        self.definition = DefinitionID().from_string(definition_id_str)
        return self

    def with_attributes(self, **kwargs: Any) -> 'Thing':
        """
        Sets all attributes to the current Thing instance.

        :param kwargs: The Attributes that describe this Thing in more detail. Can be an arbitrary JSON object.
            Attributes are typically used to model rather static properties at the Thing level.
            Static means that the values do not change as frequently as property values of Features.
        :type kwargs: typing.Any
        :returns: The updated Thing instance with the provided attributes.
        :rtype: Thing
        """
        self.attributes.update(**kwargs)
        return self

    def with_attribute(self, attribute_id: str, attribute_value: Any) -> 'Thing':
        """
        Sets/add an attribute to the current Thing instance.

        :param attribute_id: The ID of the desired attribute to add/set.
        :type attribute_id: str
        :param attribute_value: The value of the desired attribute to add/set.
        :type attribute_value: typing.Any
        :returns: The updated Thing instance with the provided desired attribute.
        :rtype: Thing
        """
        self.attributes[attribute_id] = attribute_value
        return self

    def with_features(self, **kwargs: Feature) -> 'Thing':
        """
        Sets all features to the current Thing instance.

        :param features: The Features belonging to this Thing. A Thing can handle any number of Features.
            The key of this object represents the Feature's ID. Due to the fact that a Feature's ID often needs to be set
            in the path of a HTTP request, it is strongly recommended to use a restricted set of characters.
        :type kwargs: Feature
        :returns: The updated Thing instance with the provided features.
        :rtype: Thing
        """
        self.features.update(**kwargs)
        return self

    def with_feature(self, feature_id: str, feature: Feature) -> 'Thing':
        """
        Sets/adds a Feature to the current features set of the Thing instance.

        :param feature_id: The ID of the desired feature to add/set.
        :type feature_id: str
        :param feature: The value of the desired feature to add/set.
        :type feature: Feature
        :returns: The updated Thing instance with the provided features.
        :rtype: Thing
        """
        self.features[feature_id] = feature
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        """
        Converts the current Thing instance into a dictionary
        that is compliant with the Ditto specification and is directly JSON serializable
        compliant with the Ditto format requirements.

        This method is intended to be used in the cases where a Thing is needed to be provided
        as a payload of a Ditto message (i.e. Envelope's value), e.g.:
        - creating a new Thing
        - modifying an existing Thing

        :returns: A dictionary representation of the Thing instance compliant with the Ditto JSON format.
        :rtype: typing.Dict
        """
        thing_dict = {}
        if self.thing_id:
            thing_dict[Thing.__ditto_json_key_thing_id] = self.thing_id.__str__()
        if self.policy_id:
            thing_dict[Thing.__ditto_json_key_policy_id] = self.policy_id.__str__()
        if self.definition:
            thing_dict[Thing.__ditto_json_key_definition_id] = self.definition.__str__()
        thing_dict[Thing.__ditto_json_key_attributes] = self.attributes
        if self.features:
            thing_dict[Thing.__ditto_json_key_features] = {k: v.to_ditto_dict() for k, v in self.features.items()}
        thing_dict[Thing.__ditto_json_key__namespace] = self.namespace
        thing_dict[Thing.__ditto_json_key__created] = self.created
        thing_dict[Thing.__ditto_json_key__modified] = self.modified
        thing_dict[Thing.__ditto_json_key__revision] = self.revision
        thing_dict[Thing.__ditto_json_key__metadata] = self.metadata

        return {k: v for k, v in thing_dict.items() if v is not None and v != "None" and v != {}}

    def from_ditto_dict(self, ditto_dictionary: Dict[str, Any]):
        """
        Enables initialization of the Thing instance via a dictionary that is compliant with the Ditto specification.

        This method can be used in combination with the supported by Python object_hook configuration for loading JSON data.

        :param ditto_dictionary: The dictionary that is compliant with the Ditto specification.
        :type ditto_dictionary: typing.Dict
        :returns: The initialized Thing instance if the dictionary is compliant with the Ditto specification.
            Otherwise, the input ditto_dictionary is returned.
        :rtype: Thing
        """
        if list(set(ditto_dictionary.keys()) & set(Thing.__ditto_json_keys_all)):
            if Thing.__ditto_json_key_thing_id in ditto_dictionary:
                self.with_id_from(ditto_dictionary[Thing.__ditto_json_key_thing_id])
            if Thing.__ditto_json_key_policy_id in ditto_dictionary:
                self.with_policy_id_from(ditto_dictionary[Thing.__ditto_json_key_policy_id])
            if Thing.__ditto_json_key_definition_id in ditto_dictionary:
                self.with_definition_from(ditto_dictionary[Thing.__ditto_json_key_definition_id])
            if Thing.__ditto_json_key_attributes in ditto_dictionary:
                self.with_attributes(**ditto_dictionary[Thing.__ditto_json_key_attributes])
            if Thing.__ditto_json_key__revision in ditto_dictionary:
                self.revision = ditto_dictionary[Thing.__ditto_json_key__revision]
            if Thing.__ditto_json_key__namespace in ditto_dictionary:
                self.namespace = ditto_dictionary[Thing.__ditto_json_key__namespace]
            if Thing.__ditto_json_key__created in ditto_dictionary:
                self.created = ditto_dictionary[Thing.__ditto_json_key__created]
            if Thing.__ditto_json_key__modified in ditto_dictionary:
                self.modified = ditto_dictionary[Thing.__ditto_json_key__modified]
            if Thing.__ditto_json_key__metadata in ditto_dictionary:
                self.metadata = ditto_dictionary[Thing.__ditto_json_key__metadata]
            if Thing.__ditto_json_key_features in ditto_dictionary:
                for feature_id, feature in ditto_dictionary[Thing.__ditto_json_key_features].items():
                    self.with_feature(feature_id, Feature().from_ditto_dict(feature))
            return self
        return ditto_dictionary
