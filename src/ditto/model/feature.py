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


class Feature(object):
    """
    Feature represents the Feature entity defined by the Ditto's Things specification.

    It is used to manage all data and functionality of a Thing that can be clustered in an outlined technical context.
    """

    # Literals needed for the conversion of the Feature instance from and to the desired Ditto JSON format.
    __ditto_json_key_definition = "definition"
    __ditto_json_key_properties = "properties"
    __ditto_json_key_desired_properties = "desiredProperties"
    __ditto_json_keys_all = [__ditto_json_key_definition,
                             __ditto_json_key_properties,
                             __ditto_json_key_desired_properties]

    def __init__(self,
                 definition: [DefinitionID] = None,
                 properties: Dict[str, Any] = None,
                 desired_properties: Dict[str, Any] = None):
        """
        Initializes a new Feature instance with the provided properties according to the Ditto specification.

        :param definition: The list of DefinitionIDs that this Feature implementation will provide the support for.
        :type definition: DefinitionID
        :param properties: The dictionary of properties related to the DefinitionIDs and additional if needed.
        :type properties: typing.Dict[str, Any]
        :param desired_properties: The dictionary of desired properties that are to be configured
            as the currently desired state of the Feature.
        :type desired_properties: typing.Dict[str, Any]
        """
        self.definition = definition
        self.properties = properties
        if self.properties is None:
            self.properties = {}
        self.desired_properties = desired_properties
        if self.desired_properties is None:
            self.desired_properties = {}

    def with_definition_from(self, *args: str) -> 'Feature':
        """
        An auxiliary method to set the Feature's definition.

        It is generated from an array of strings converted into the proper DefinitionID instances.

        :param args: the string DefinitionID representations to generate the objects from in the format
            <namespace>:<name>:<version>
        :type args: str
        :returns: The Feature object initialized with the provided list of definition IDs set as definition.
        :rtype: Feature
        """
        self.definition = [DefinitionID().from_string(arg) for arg in args]
        return self

    def with_definition(self, *args: DefinitionID) -> 'Feature':
        """
        Sets the definition of the current Feature instance to the provided set of DefinitionIDs.

        :param args: The list of DefinitionIDs to set.
        :type args: DefinitionID
        :returns: The Feature object initialized with the provided list of DefinitionIDs.
        :rtype: Feature
        """
        self.definition = args
        return self

    #

    def with_properties(self, **kwargs: Any) -> 'Feature':
        """
        Sets all properties of the current Feature instance.

        It's important that the properties must be provided in a dictionary
        that consists of object types that are supported by Python by default:
        dict, list, tuple, str, int, float, bool, None.

        The provided properties are merged with the already existing ones:
        - the values for already existing keys are updated
        - new keys and their values are added directly

        :param kwargs: The dictionary of properties to be included in the current Feature instance.
        :type kwargs: typing.Any
        :returns: The updated Feature instance with the provided properties.
        :rtype: Feature
        """
        self.properties.update(**kwargs)
        return self

    # with_property

    def with_property(self, property_id: str, value: Any) -> 'Feature':
        """
        Sets/adds a property to the current Feature instance.

        This method supports only adding/setting top-level properties in the Feature instance.

        It's important that the property's value must be provided as an object
        of one of the types that are supported by Python for JSON representation by default:
        dict, list, tuple, str, int, float, bool, None.

        :param property_id: The ID of the top-level property to add/set.
        :type property_id: str
        :param value: The vale of the property to add/set.
        :type value: typing.Any
        :returns: The updated Feature instance with the provided property.
        :rtype: Feature
        """
        self.properties[property_id] = value
        return self

    # with_desired_properties

    def with_desired_properties(self, **kwargs: Any) -> 'Feature':
        """
        Sets all desired properties of the current Feature instance.

        It's important that the desired properties must be provided in a dictionary
        that consists of object types that are supported by Python by default:
        dict, list, tuple, str, int, float, bool, None.

        The provided properties are merged with the already existing ones:
        - the values for already existing keys are updated
        - new keys and their values are added directly

        :param kwargs: The dictionary of desired properties to be included in the current Feature instance.
        :type kwargs: typing.Any
        :returns: The updated Feature instance with the provided desired properties.
        :rtype: Feature
        """
        self.desired_properties.update(**kwargs)
        return self

    def with_desired_property(self, desired_property_id: str, value: Any) -> 'Feature':
        """
        Sets/adds a desired property to the current Feature instance.

        This method supports only adding/setting top-level desired properties in the Feature instance.

        It's important that the property's value must be provided as an object
        of one of the types that are supported by Python for JSON representation by default:
        dict, list, tuple, str, int, float, bool, None.

        :param desired_property_id: The ID of the top-level desired property to add/set.
        :type desired_property_id: str
        :param value: The value of the desired property to add/set.
        :type value: typing.Any
        :returns: The updated Feature instance with the provided desired property.
        :rtype: Feature
        """
        self.desired_properties[desired_property_id] = value
        return self

    def to_ditto_dict(self) -> Dict[str, Any]:
        """
        Converts the current Feature instance into a dictionary
        that is compliant with the Ditto specification and is directly JSON serializable
        compliant with the Ditto format requirements.

        This method is intended to be used in the cases where a Feature is needed to be provided
        as a payload of a Ditto message (i.e. Envelope's value), e.g.:
        - creating a new Feature
        - modifying an existing Feature

        :returns: A dictionary representation of the Feature instance compliant with the Ditto JSON format.
        :rtype: typing.Dict
        """
        feature_dict = {}
        if self.definition:
            feature_dict[Feature.__ditto_json_key_definition] = [d.__str__() for d in self.definition]
        feature_dict[Feature.__ditto_json_key_properties] = self.properties
        feature_dict[Feature.__ditto_json_key_desired_properties] = self.desired_properties
        return {k: v for k, v in feature_dict.items() if v != {} and v != []}

    def from_ditto_dict(self, ditto_dictionary: Dict[str, Any]):
        """
        Enables initialization of the Feature instance via a dictionary that is compliant with the Ditto specification.

        This method can be used in combination with the supported by Python object_hook configuration for loading JSON data.

        :param ditto_dictionary: The dictionary that is compliant with the Ditto specification.
        :type ditto_dictionary: typing.Dict
        :returns: The initialized Feature instance if the dictionary is compliant with the Ditto specification.
            Otherwise, the input ditto_dictionary is returned.
        :rtype: Feature
        """
        if list(set(ditto_dictionary.keys()) & set(Feature.__ditto_json_keys_all)):
            if Feature.__ditto_json_key_definition in ditto_dictionary:
                self.with_definition_from(*ditto_dictionary[Feature.__ditto_json_key_definition])
            if Feature.__ditto_json_key_properties in ditto_dictionary:
                self.with_properties(**ditto_dictionary[Feature.__ditto_json_key_properties])
            if Feature.__ditto_json_key_desired_properties in ditto_dictionary:
                self.with_desired_properties(**ditto_dictionary[Feature.__ditto_json_key_desired_properties])
            return self
        return ditto_dictionary
