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

        :param thing_id:
        :return:
        """
        self.thing_id = thing_id
        return self

    def with_id_from(self, thing_id_str: str) -> 'Thing':
        """
        An auxiliary method that sets the ID value of the current Thing instance based on the provided string n the form of 'namespace:name'.

        :param thing_id_str:
        :return:
        """
        self.thing_id = NamespacedID().from_string(thing_id_str)
        return self

    def with_policy_id(self, policy_id: NamespacedID) -> 'Thing':
        """
        Sets the provided Policy ID to the current Thing instance.

        :param policy_id:
        :return:
        """
        self.policy_id = policy_id
        return self

    def with_policy_id_from(self, policy_id_str: str) -> 'Thing':
        """
        An auxiliary method that sets the Policy ID of the current Thing instance.

        :param policy_id_str:
        :return:
        """
        self.policy_id = NamespacedID.from_string(policy_id_str)
        return self

    def with_definition(self, definition_id: DefinitionID) -> 'Thing':
        """
        Sets the current Thing instance's definition to the provided value.

        :param definition_id:
        :return:
        """
        self.definition = definition_id
        return self

    def with_definition_from(self, definition_id_str: str) -> 'Thing':
        """
        An auxiliary method to set the current Thing instance's definition to the provided one in the form of 'namespace:name:version'.

        :param definition_id_str:
        :return:
        """
        self.definition = DefinitionID().from_string(definition_id_str)
        return self

    def with_attributes(self, **kwargs: Any) -> 'Thing':
        """
        Sets all attributes to the current Thing instance.

        :param kwargs:
        :return:
        """
        self.attributes.update(**kwargs)
        return self

    def with_attribute(self, attribute_id: str, attribute_value: Any) -> 'Thing':
        """
        Sets/add an attribute to the current Thing instance.

        :param attribute_id:
        :param attribute_value:
        :return:
        """
        self.attributes[attribute_id] = attribute_value
        return self

    def with_features(self, **kwargs: Feature) -> 'Thing':
        """
        Sets all features to the current Thing instance.

        :param kwargs:
        :return:
        """
        self.features.update(**kwargs)
        return self

    def with_feature(self, feature_id: str, feature: Feature) -> 'Thing':
        """
        Sets/adds a Feature to the current features set of the Thing instance.

        :param feature_id:
        :param feature:
        :return:
        """
        self.features[feature_id] = feature
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        """

        :return:
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

        :param ditto_dictionary:
        :return:
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
