# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ExtentTemporal(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, interval=None, trs='http://www.opengis.net/def/uom/ISO-8601/0/Gregorian'):  # noqa: E501
        """ExtentTemporal - a model defined in OpenAPI

        :param interval: The interval of this ExtentTemporal.  # noqa: E501
        :type interval: List[List[datetime]]
        :param trs: The trs of this ExtentTemporal.  # noqa: E501
        :type trs: str
        """
        self.openapi_types = {
            'interval': List[List[datetime]],
            'trs': str
        }

        self.attribute_map = {
            'interval': 'interval',
            'trs': 'trs'
        }

        self._interval = interval
        self._trs = trs

    @classmethod
    def from_dict(cls, dikt) -> 'ExtentTemporal':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The extent_temporal of this ExtentTemporal.  # noqa: E501
        :rtype: ExtentTemporal
        """
        return util.deserialize_model(dikt, cls)

    @property
    def interval(self):
        """Gets the interval of this ExtentTemporal.

        One or more time intervals that describe the temporal extent of the dataset. The value `null` is supported and indicates an open time interval. In the Core only a single time interval is supported. Extensions may support multiple intervals. If multiple intervals are provided, the union of the intervals describes the temporal extent.  # noqa: E501

        :return: The interval of this ExtentTemporal.
        :rtype: List[List[datetime]]
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this ExtentTemporal.

        One or more time intervals that describe the temporal extent of the dataset. The value `null` is supported and indicates an open time interval. In the Core only a single time interval is supported. Extensions may support multiple intervals. If multiple intervals are provided, the union of the intervals describes the temporal extent.  # noqa: E501

        :param interval: The interval of this ExtentTemporal.
        :type interval: List[List[datetime]]
        """
        if interval is not None and len(interval) < 1:
            raise ValueError("Invalid value for `interval`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._interval = interval

    @property
    def trs(self):
        """Gets the trs of this ExtentTemporal.

        Coordinate reference system of the coordinates in the temporal extent (property `interval`). The default reference system is the Gregorian calendar. In the Core this is the only supported temporal coordinate reference system. Extensions may support additional temporal coordinate reference systems and add additional enum values.  # noqa: E501

        :return: The trs of this ExtentTemporal.
        :rtype: str
        """
        return self._trs

    @trs.setter
    def trs(self, trs):
        """Sets the trs of this ExtentTemporal.

        Coordinate reference system of the coordinates in the temporal extent (property `interval`). The default reference system is the Gregorian calendar. In the Core this is the only supported temporal coordinate reference system. Extensions may support additional temporal coordinate reference systems and add additional enum values.  # noqa: E501

        :param trs: The trs of this ExtentTemporal.
        :type trs: str
        """
        allowed_values = ["http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"]  # noqa: E501
        if trs not in allowed_values:
            raise ValueError(
                "Invalid value for `trs` ({0}), must be one of {1}"
                .format(trs, allowed_values)
            )

        self._trs = trs
