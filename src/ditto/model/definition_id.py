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
    in the form of 'namespace:name:version'.
    The DefinitionID is used to declare a Thing's model also it is used
    in declare the different models a Feature represents via its properties.
    """

    __definition_id_template = "{}:{}:{}"

    def __init__(self,
                 namespace=None,
                 name=None,
                 version=None):
        """

        :param namespace:
        :param name:
        :param version:
        """
        self.namespace = namespace
        self.name = name
        self.version = version

    def with_namespace(self, namespace: str) -> 'DefinitionID':
        """

        :param namespace:
        :return:
        """
        self.namespace = namespace
        return self

    def with_name(self, name: str) -> 'DefinitionID':
        """

        :param name:
        :return:
        """
        self.name = name
        return self

    def with_version(self, version: str) -> 'DefinitionID':
        """

        :param version:
        :return:
        """
        self.version = version
        return self

    def from_string(self, definition_id_str: str = None) -> 'DefinitionID':
        """

        :param definition_id_str:
        :return:
        """
        if definition_id_str:
            elements = definition_id_str.split(sep=":", maxsplit=2)
            self.__init__(namespace=elements[0], name=elements[1], version=elements[2])
        return self

    def __str__(self):
        """

        :return:
        """
        return self.__definition_id_template.format(self.namespace, self.name, self.version)
