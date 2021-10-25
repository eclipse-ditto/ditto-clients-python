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

class NamespacedID(object):
    """
    Represents the namespaced entity ID defined by the Ditto specification.
    It is a unique identifier representing a Thing compliant with the Ditto requirements:
    - namespace and name separated by a : (colon)
    - have a maximum length of 256 characters.
    """
    __namespaced_id_template = "{}:{}"

    def __init__(self,
                 namespace=None,
                 name=None):
        """

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :param name: The entity's name. May not be empty, contain "/" or contain control characters.
        :type name: str
        """
        self.namespace = namespace
        self.name = name

    def with_namespace(self, namespace: str) -> 'NamespacedID':
        """

        :param namespace: The entity’s namespace in which the entity is located.
        :type namespace: str
        :returns: The updated NamespacedID instance with the provided namespace.
        :rtype: NamespacedID
        """
        self.namespace = namespace
        return self

    def with_name(self, name: str) -> 'NamespacedID':
        """

        :param name: The entity's name. May not be empty, contain "/" or contain control characters.
        :type name: str
        :returns: The updated NamespacedID instance with the provided name.
        :rtype: NamespacedID
        """
        self.name = name
        return self

    def from_string(self, namespaced_id_str: str = None) -> 'NamespacedID':
        """
        Sets the NamespacedID's properties from a provided string.

        :param namespaced_id_str: A string that is compliant with the Ditto specification.
            It consists of a namespace and a name in the form of <namespace>:<name>.
        :returns: The initialized NamespacedID instance with the provided name and namespace.
        :rtype: NamespacedID
        """
        if namespaced_id_str:
            elements = namespaced_id_str.split(sep=":", maxsplit=1)
            self.__init__(namespace=elements[0], name=elements[1])
        return self

    def __str__(self):
        """
        Converts the current NamespacedID instance into a string that is compliant with the Ditto specification.
        :returns: A string representation of the NamespacedID instance compliant with the Ditto specification.
        :rtype: str
        """
        return self.__namespaced_id_template.format(self.namespace, self.name)
