from openapi_server.models import link
from openapi_server.models import instances
from openapi_server.models.link import Link
import connexion
import six
from flask import request
from openapi_server.models.exception import Exception  # noqa: E501
from openapi_server.models.instances import Instances  # noqa: E501
from openapi_server import util
from openapi_server.models.collections import Collections  # noqa: E501
from openapi_server.models.collection import Collection
from openapi_server.models.extent import Extent
from openapi_server.models.extent_spatial import ExtentSpatial
from openapi_server.models.extent_temporal import ExtentTemporal
from openapi_server.models.collection_data_queries import CollectionDataQueries
from openapi_server.models.collection_data_queries_position import CollectionDataQueriesPosition
from openapi_server.models.instances import Instances
import openapi_server.backend.backendConfiguration as backends

def get_collection_instances(collection_id):  # noqa: E501
    """List data instances of {collectionId}

    This will provide list of the avalable instances of the collection Use content negotiation to request HTML or JSON. # noqa: E501

    :param collection_id: local identifier of a collection
    :type collection_id: str

    :rtype: Instances
    """

    backend = backends.getDataBackendForCollection(collection_id)

    if backend is None:
        return Exception(code= "404", description="collection {0} not found".format(collection_id)), 404

    instances = backend.requestTransformer.getInstances(collectionID= collection_id)

    #links for instances metadata
    selfLink = Link(href=request.url.split('?')[0], rel="self",
                    title="description of all instances of collection " + collection_id, type="application/json")
    collectionLink = Link(href=request.url.split('?')[0][0 : request.url.rindex("/")], rel="collection",
                    title="collection "+ collection_id +" description as json", type="application/json")
    links = [selfLink, collectionLink]
    instances.links = links

    #links for each instance
    for instance in instances.instances:
        instance.data_queries = getDataQueryLinks(instance.id)
        instance.links = links

    return instances



def getDataQueryLinks(instanceId):
    radiusQuery = CollectionDataQueriesPosition(link=Link(href=request.url.split('?')[0] + "/" + instanceId + "/radius", title= "radius query"))
    areaQuery = CollectionDataQueriesPosition(link=Link(href=request.url.split('?')[0] + "/" + instanceId + "/area", title= "area query"))
    positionQuery = CollectionDataQueriesPosition(link=Link(href=request.url.split('?')[0] + "/" + instanceId + "/position", title= "position query"))

    return CollectionDataQueries(position= positionQuery, radius= radiusQuery, area= areaQuery)