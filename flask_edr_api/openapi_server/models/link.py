# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Link(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, href=None, rel=None, type=None, hreflang=None, title=None, length=None):  # noqa: E501
        """Link - a model defined in OpenAPI

        :param href: The href of this Link.  # noqa: E501
        :type href: str
        :param rel: The rel of this Link.  # noqa: E501
        :type rel: str
        :param type: The type of this Link.  # noqa: E501
        :type type: str
        :param hreflang: The hreflang of this Link.  # noqa: E501
        :type hreflang: str
        :param title: The title of this Link.  # noqa: E501
        :type title: str
        :param length: The length of this Link.  # noqa: E501
        :type length: int
        """
        self.openapi_types = {
            'href': str,
            'rel': str,
            'type': str,
            'hreflang': str,
            'title': str,
            'length': int
        }

        self.attribute_map = {
            'href': 'href',
            'rel': 'rel',
            'type': 'type',
            'hreflang': 'hreflang',
            'title': 'title',
            'length': 'length'
        }

        self._href = href
        self._rel = rel
        self._type = type
        self._hreflang = hreflang
        self._title = title
        self._length = length

    @classmethod
    def from_dict(cls, dikt) -> 'Link':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The link of this Link.  # noqa: E501
        :rtype: Link
        """
        return util.deserialize_model(dikt, cls)

    @property
    def href(self):
        """Gets the href of this Link.


        :return: The href of this Link.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this Link.


        :param href: The href of this Link.
        :type href: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")  # noqa: E501

        self._href = href

    @property
    def rel(self):
        """Gets the rel of this Link.


        :return: The rel of this Link.
        :rtype: str
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this Link.


        :param rel: The rel of this Link.
        :type rel: str
        """

        self._rel = rel

    @property
    def type(self):
        """Gets the type of this Link.


        :return: The type of this Link.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Link.


        :param type: The type of this Link.
        :type type: str
        """

        self._type = type

    @property
    def hreflang(self):
        """Gets the hreflang of this Link.


        :return: The hreflang of this Link.
        :rtype: str
        """
        return self._hreflang

    @hreflang.setter
    def hreflang(self, hreflang):
        """Sets the hreflang of this Link.


        :param hreflang: The hreflang of this Link.
        :type hreflang: str
        """

        self._hreflang = hreflang

    @property
    def title(self):
        """Gets the title of this Link.


        :return: The title of this Link.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Link.


        :param title: The title of this Link.
        :type title: str
        """

        self._title = title

    @property
    def length(self):
        """Gets the length of this Link.


        :return: The length of this Link.
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Link.


        :param length: The length of this Link.
        :type length: int
        """

        self._length = length