# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.collection_data_queries import CollectionDataQueries
from openapi_server.models.extent import Extent
from openapi_server.models.link import Link
from openapi_server import util

from openapi_server.models.collection_data_queries import CollectionDataQueries  # noqa: E501
from openapi_server.models.extent import Extent  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501

class Collection(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, title=None, description=None, links=None, keywords=None, extent=None, item_type='feature', crs=["http://www.opengis.net/def/crs/OGC/1.3/CRS84"], data_queries=None, output_formats=None, parameter_names=None):  # noqa: E501
        """Collection - a model defined in OpenAPI

        :param id: The id of this Collection.  # noqa: E501
        :type id: str
        :param title: The title of this Collection.  # noqa: E501
        :type title: str
        :param description: The description of this Collection.  # noqa: E501
        :type description: str
        :param links: The links of this Collection.  # noqa: E501
        :type links: List[Link]
        :param keywords: The keywords of this Collection.  # noqa: E501
        :type keywords: List[str]
        :param extent: The extent of this Collection.  # noqa: E501
        :type extent: Extent
        :param item_type: The item_type of this Collection.  # noqa: E501
        :type item_type: str
        :param crs: The crs of this Collection.  # noqa: E501
        :type crs: List[str]
        :param data_queries: The data_queries of this Collection.  # noqa: E501
        :type data_queries: CollectionDataQueries
        :param output_formats: The output_formats of this Collection.  # noqa: E501
        :type output_formats: List[str]
        :param parameter_names: The parameter_names of this Collection.  # noqa: E501
        :type parameter_names: Dict[str, object]
        """
        self.openapi_types = {
            'id': str,
            'title': str,
            'description': str,
            'links': List[Link],
            'keywords': List[str],
            'extent': Extent,
            'item_type': str,
            'crs': List[str],
            'data_queries': CollectionDataQueries,
            'output_formats': List[str],
            'parameter_names': Dict[str, object]
        }

        self.attribute_map = {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'links': 'links',
            'keywords': 'keywords',
            'extent': 'extent',
            'item_type': 'itemType',
            'crs': 'crs',
            'data_queries': 'data_queries',
            'output_formats': 'output_formats',
            'parameter_names': 'parameter_names'
        }

        self._id = id
        self._title = title
        self._description = description
        self._links = links
        self._keywords = keywords
        self._extent = extent
        self._item_type = item_type
        self._crs = crs
        self._data_queries = data_queries
        self._output_formats = output_formats
        self._parameter_names = parameter_names

    @classmethod
    def from_dict(cls, dikt) -> 'Collection':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The collection of this Collection.  # noqa: E501
        :rtype: Collection
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Collection.

        identifier of the collection used, for example, in URIs  # noqa: E501

        :return: The id of this Collection.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Collection.

        identifier of the collection used, for example, in URIs  # noqa: E501

        :param id: The id of this Collection.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def title(self):
        """Gets the title of this Collection.

        human readable title of the collection  # noqa: E501

        :return: The title of this Collection.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Collection.

        human readable title of the collection  # noqa: E501

        :param title: The title of this Collection.
        :type title: str
        """

        self._title = title

    @property
    def description(self):
        """Gets the description of this Collection.

        a description of the features in the collection  # noqa: E501

        :return: The description of this Collection.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Collection.

        a description of the features in the collection  # noqa: E501

        :param description: The description of this Collection.
        :type description: str
        """

        self._description = description

    @property
    def links(self):
        """Gets the links of this Collection.


        :return: The links of this Collection.
        :rtype: List[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Collection.


        :param links: The links of this Collection.
        :type links: List[Link]
        """
        if links is None:
            raise ValueError("Invalid value for `links`, must not be `None`")  # noqa: E501

        self._links = links

    @property
    def keywords(self):
        """Gets the keywords of this Collection.

        List of keywords which help to describe the collection  # noqa: E501

        :return: The keywords of this Collection.
        :rtype: List[str]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """Sets the keywords of this Collection.

        List of keywords which help to describe the collection  # noqa: E501

        :param keywords: The keywords of this Collection.
        :type keywords: List[str]
        """

        self._keywords = keywords

    @property
    def extent(self):
        """Gets the extent of this Collection.


        :return: The extent of this Collection.
        :rtype: Extent
        """
        return self._extent

    @extent.setter
    def extent(self, extent):
        """Sets the extent of this Collection.


        :param extent: The extent of this Collection.
        :type extent: Extent
        """
        if extent is None:
            raise ValueError("Invalid value for `extent`, must not be `None`")  # noqa: E501

        self._extent = extent

    @property
    def item_type(self):
        """Gets the item_type of this Collection.

        indicator about the type of the items in the collection (the default value is 'feature').  # noqa: E501

        :return: The item_type of this Collection.
        :rtype: str
        """
        return self._item_type

    @item_type.setter
    def item_type(self, item_type):
        """Sets the item_type of this Collection.

        indicator about the type of the items in the collection (the default value is 'feature').  # noqa: E501

        :param item_type: The item_type of this Collection.
        :type item_type: str
        """

        self._item_type = item_type

    @property
    def crs(self):
        """Gets the crs of this Collection.

        the list of coordinate reference systems supported by the service  # noqa: E501

        :return: The crs of this Collection.
        :rtype: List[str]
        """
        return self._crs

    @crs.setter
    def crs(self, crs):
        """Sets the crs of this Collection.

        the list of coordinate reference systems supported by the service  # noqa: E501

        :param crs: The crs of this Collection.
        :type crs: List[str]
        """

        self._crs = crs

    @property
    def data_queries(self):
        """Gets the data_queries of this Collection.


        :return: The data_queries of this Collection.
        :rtype: CollectionDataQueries
        """
        return self._data_queries

    @data_queries.setter
    def data_queries(self, data_queries):
        """Sets the data_queries of this Collection.


        :param data_queries: The data_queries of this Collection.
        :type data_queries: CollectionDataQueries
        """

        self._data_queries = data_queries

    @property
    def output_formats(self):
        """Gets the output_formats of this Collection.

        list of formats the results can be presented in  # noqa: E501

        :return: The output_formats of this Collection.
        :rtype: List[str]
        """
        return self._output_formats

    @output_formats.setter
    def output_formats(self, output_formats):
        """Sets the output_formats of this Collection.

        list of formats the results can be presented in  # noqa: E501

        :param output_formats: The output_formats of this Collection.
        :type output_formats: List[str]
        """

        self._output_formats = output_formats

    @property
    def parameter_names(self):
        """Gets the parameter_names of this Collection.

        list of the data parameters available in the collection  # noqa: E501

        :return: The parameter_names of this Collection.
        :rtype: Dict[str, object]
        """
        return self._parameter_names

    @parameter_names.setter
    def parameter_names(self, parameter_names):
        """Sets the parameter_names of this Collection.

        list of the data parameters available in the collection  # noqa: E501

        :param parameter_names: The parameter_names of this Collection.
        :type parameter_names: Dict[str, object]
        """

        self._parameter_names = parameter_names
