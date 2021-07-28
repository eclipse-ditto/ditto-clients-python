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

        :param namespace:
        :param name:
        """
        self.namespace = namespace
        self.name = name

    def with_namespace(self, namespace: str) -> 'NamespacedID':
        """

        :param namespace:
        :return:
        """
        self.namespace = namespace
        return self

    def with_name(self, name: str) -> 'NamespacedID':
        """

        :param name:
        :return:
        """
        self.name = name
        return self

    def from_string(self, namespaced_id_str: str = None) -> 'NamespacedID':
        """

        :param namespaced_id_str:
        :return:
        """
        if namespaced_id_str:
            elements = namespaced_id_str.split(sep=":", maxsplit=1)
            self.__init__(namespace=elements[0], name=elements[1])
        return self

    def __str__(self):
        return self.__namespaced_id_template.format(self.namespace, self.name)
