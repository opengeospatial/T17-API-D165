import collections
import connexion
import six

from openapi_server.models.collection import Collection  # noqa: E501
from openapi_server.models.collections import Collections  # noqa: E501
from openapi_server.models.conf_classes import ConfClasses  # noqa: E501
from openapi_server.models.exception import Exception  # noqa: E501
from openapi_server.models.landing_page import LandingPage  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.models.extent import Extent
from openapi_server.models.extent_spatial import ExtentSpatial
from openapi_server.models.extent_temporal import ExtentTemporal
from openapi_server import util
from flask import request
import openapi_server.backendConfiguration as backends


def describe_collection(collection_id):  # noqa: E501
    """describe the feature collection with id &#x60;collectionId&#x60;

     # noqa: E501

    :param collection_id: local identifier of a collection
    :type collection_id: str

    :rtype: Collection
    """
    backend = backends.getDataBackendForCollection(collection_id)
    collection = backend.requestTransformer.getCollection(collectionID= collection_id)
    
    selfLink = Link(href=request.url, rel="self",
                    title="describition of " + collection_id + " collection", type="application/json")
    itemsLink = Link(href=request.url + "/" +"items", rel="items",
                    title="features of " + collection_id + " collection", type="application/json")
    collectionsLink = Link(href=request.url[0 : request.url.rindex("/")], rel="data",
                    title="describition of all collections", type="application/json")
    
    collection.links = [selfLink, itemsLink, collectionsLink]

    return collection


def get_collections():  # noqa: E501
    """the feature collections in the dataset

     # noqa: E501


    :rtype: Collections
    """
    allColls = []
    for backend in backends.getAvailableDataBackends():
        backendColls = backend.requestTransformer.getCollections(backend.availableCollections)
        for coll in backendColls:
            coll.links = createLinksForCollection(request.url, coll.id)

        allColls.extend(backendColls)

    selfLink = Link(href=request.url, rel="self",
                    title="describition of all collections", type="application/json")
    landingPageLink = Link(href=request.url[0 : request.url.rindex("/")], rel="landingpage",
                    title="landing page as json", type="application/json")

    links = [selfLink, landingPageLink]
    collections = Collections( links= links, collections= allColls)    

    return collections


def get_conformance_declaration():  # noqa: E501
    """information about specifications that this API conforms to

    A list of all conformance classes specified in a standard that the server conforms to. # noqa: E501


    :rtype: ConfClasses
    """
    return 'do some magic!'


def get_landing_page():  # noqa: E501
    """landing page

    The landing page provides links to the API definition, the conformance statements and to the feature collections in this dataset. # noqa: E501


    :rtype: LandingPage
    """
    collectionsLink = Link(request.url + "collections", rel="data",
                           title="describition of all collections")
    selfLink = Link(href=request.url, rel="self",
                    type="application/json", title="landing page as json")
    lp = LandingPage(backends.getBackendConfiguration()["server"]["title"],
                     backends.getBackendConfiguration()["server"]["description"], [selfLink, collectionsLink])

    return lp



def createLinksForCollection(collectionsUrl, collectionID):
    collectionsLink = Link(href=collectionsUrl, rel="data",
                    title="describition of all collections", type="application/json")
    selfLink = Link(href=collectionsUrl + "/" + collectionID, rel="self",
                    title="describition of " + collectionID + " collection", type="application/json")
    itemsLink = Link(href=collectionsUrl + "/" + collectionID + "/items", rel="items",
                    title="features of " + collectionID + " collection", type="application/json")

    return [selfLink, itemsLink, collectionsLink]
