# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.exception import Exception  # noqa: E501
from openapi_server.models.instances import Instances  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCollectionMetadataController(BaseTestCase):
    """CollectionMetadataController integration test stubs"""

    def test_get_collection_instances(self):
        """Test case for get_collection_instances

        List data instances of {collectionId}
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/collections/{collection_id}/instances'.format(collection_id='collection_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
