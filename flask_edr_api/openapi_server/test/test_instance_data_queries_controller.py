# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.exception import Exception  # noqa: E501
from openapi_server.models.feature_collection_geo_json import FeatureCollectionGeoJSON  # noqa: E501
from openapi_server.test import BaseTestCase


class TestInstanceDataQueriesController(BaseTestCase):
    """InstanceDataQueriesController integration test stubs"""

    def test_get_instance_data_for_radius(self):
        """Test case for get_instance_data_for_radius

        Query end point to return data within defined radius of a point for an instance {instanceId} of collection {collectionId}
        """
        query_string = [('within', 3.4),
                        ('within-units', 'within_units_example'),
                        ('radiusCoords', 'radius_coords_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/collections/{collection_id}/instances/{instance_id}/radius'.format(collection_id='collection_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
