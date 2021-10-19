import connexion
import six
from openapi_server.backend import data_backend

from openapi_server.models.exception import Exception  # noqa: E501
from openapi_server.models.feature_collection_geo_json import FeatureCollectionGeoJSON  # noqa: E501
from openapi_server import util
from flask import send_file
from flask import Response
import openapi_server.backend.backendConfiguration as backends



def get_instance_data_for_area(collection_id, instance_id, coords, datetime=None):  # noqa: E501
    """Query end point for area queries of instance {instanceId} of collection {collectionId} defined by a polygon

    Return the data values for the data area defined by the query parameters # noqa: E501

    :param collection_id: local identifier of a collection
    :type collection_id: str
    :param instance_id: local identifier of a collection
    :type instance_id: str
    :param coords: Only data that has a geometry that intersects the area defined by the polygon are selected. The polygon is defined using a Well Known Text string following
    :type coords: str
    :param datetime: date time
    :type datetime: str

    :rtype: application/x-netcdf
    """
    backend = backends.getDataBackendForCollection(collection_id)

    if backend is None:
        return Exception(code= "404", description="collection {0} not found".format(collection_id)), 404

    queryTransformer = backend.requestTransformer.getDataQueryTransformer()
    response = queryTransformer.transformAreaQuery(collection_id, instance_id, coords, datetime)
    
    return response


def get_instance_data_for_position(collection_id, instance_id, coords, datetime=None):  # noqa: E501
    """Query end point for position queries of instance {instanceId} of collection {collectionId}

    Query end point for position queries # noqa: E501

    :param collection_id: local identifier of a collection
    :type collection_id: str
    :param instance_id: local identifier of a collection
    :type instance_id: str
    :param coords: location(s) to return data for, the coordinates are defined by a Well Known Text (wkt) string. to retrieve a single location:POINT(x y) i.e. POINT(0 51.48) for Greenwich, London
    :type coords: str
    :param datetime: date time
    :type datetime: str

    :rtype: application/x-netcdf
    """
    backend = backends.getDataBackendForCollection(collection_id)

    if backend is None:
        return Exception(code= "404", description="collection {0} not found".format(collection_id)), 404

    queryTransformer = backend.requestTransformer.getDataQueryTransformer()
    response = queryTransformer.transformPositionQuery(collection_id, instance_id, coords, datetime)
    
    return response

def get_instance_data_for_radius(collection_id, instance_id, within, within_units, radius_coords,  datetime=None):  # noqa: E501
    """Query end point to return data within defined radius of a point for an instance {instanceId} of collection {collectionId}

    Query end point to return all data within a defined radius of the defined point location queries # noqa: E501

    :param collection_id: local identifier of a collection
    :type collection_id: str
    :param instance_id: local identifier of a collection
    :type instance_id: str
    :param within: radius
    :type within: 
    :param within_units: Distance units for the corridor-width parameter (e.g KM)
    :type within_units: str
    :param radius_coords: location(s) to return data for, the coordinates are defined by a Well Known Text (wkt) string. to retrieve a single location :  POINT(x y) i.e. POINT(0 51.48) for Greenwich, London  see http://portal.opengeospatial.org/files/?artifact_id&#x3D;25355 and  https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry  the coordinate values will depend on the CRS parameter, if this is not defined the values will be assumed to WGS84 values (i.e x&#x3D;longitude and y&#x3D;latitude) 
    :type radius_coords: str
    :type datetime: str

    :rtype: application/x-netcdf
    """
    backend = backends.getDataBackendForCollection(collection_id)

    if backend is None:
        return Exception(code= "404", description="collection {0} not found".format(collection_id)), 404

    queryTransformer = backend.requestTransformer.getDataQueryTransformer()
    response = queryTransformer.transformRadiusQuery(collection_id, instance_id, within, within_units, radius_coords, datetime)
    
    return response