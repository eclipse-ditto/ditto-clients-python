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

class DefinitionID(object):
    """
    DefinitionID represents an ID of a given definition entity.

    Compliant with the Ditto specification it consists of a namespace, name and a version
    in the form of <namespace>:<name>:<version>.
    The DefinitionID is used to declare a Thing's model also it is used
    in declare the different models a Feature represents via its properties.
    """

    __definition_id_template = "{}:{}:{}"

    def __init__(self,
                 namespace: str = None,
                 name: str = None,
                 version: str = None):
        """
        Initializes a new DefinitionID instance with the provided namespace, name and desired version
        according to the Ditto specification.

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :param name: The entity's name. May not be empty, contain "/" or contain control characters.
        :type name: str
        :param version: The entity's version.
        :type version: str
        """
        self.namespace = namespace
        self.name = name
        self.version = version

    def with_namespace(self, namespace: str) -> 'DefinitionID':
        """
        Sets the namespace of the current DefinitionID instance to the provided string.

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :returns: The updated DefinitionID instance with the provided namespace.
        :rtype: DefinitionID
        """
        self.namespace = namespace
        return self

    def with_name(self, name: str) -> 'DefinitionID':
        """
        Sets the name of the current DefinitionID instance to the provided string.

        :param name: The entity's name. May not be empty, contain "/" or contain control characters.
        :type name: str
        :returns: The updated DefinitionID instance with the provided name.
        :rtype: DefinitionID
        """
        self.name = name
        return self

    def with_version(self, version: str) -> 'DefinitionID':
        """
        Sets the version of the current DefinitionID instance to the provided string.

        :param version: The entity's version.
        :type version: str
        :returns: The updated DefinitionID instance with the provided version.
        :rtype: DefinitionID
        """
        self.version = version
        return self

    def from_string(self, definition_id_str: str = None) -> 'DefinitionID':
        """
        Sets the DefinitionID's properties from a provided string.

        :param definition_id_str: A string that is compliant with the Ditto specification.
            It consists of a namespace, name and a version in the form of <namespace>:<name>:<version>.
        :returns: The initialized DefinitionID instance with the provided name, namespace and version.
        :rtype: DefinitionID
        """
        if definition_id_str:
            elements = definition_id_str.split(sep=":", maxsplit=2)
            self.__init__(namespace=elements[0], name=elements[1], version=elements[2])
        return self

    def __str__(self):
        """
        Converts the current DefinitionID instance into a string that is compliant with the Ditto specification.
        :returns: A string representation of the DefinitionID instance compliant with the Ditto specification.
        :rtype: str
        """
        return self.__definition_id_template.format(self.namespace, self.name, self.version)
