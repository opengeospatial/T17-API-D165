import json
from openapi_server.models.extent_spatial import ExtentSpatial
from typing import List
from openapi_server.backend.format_transformers.wfsCapabilitesToCollection_transformer import WFSCapabilitiesToCollectionTransformer
from openapi_server.backend.request_transformer import RequestTransformer
from openapi_server.backend.dataaccess.elasticsearch_client import getElasticsearchClient
from openapi_server.backend.dataaccess.aws_elasticsearchservice_auth import getAWSAuth
from openapi_server.backend.query_transformers.elasticsearch_query_transformer import ElasticsearchQueryTransformer
from elasticsearch import Elasticsearch
from openapi_server.models.collection import Collection
from openapi_server.models.exception import Exception
from flask import request


class ElasticsearchRequestTransformer(RequestTransformer):

    config = None
    elasticSearchClient = None
    queryTransformer = None

    def __init__(self, config):
        self.config = config
        
        if "awsAuth" in config:
            
            self.elasticSearchClient = getElasticsearchClient(self.config, awsauth= getAWSAuth(self.config["awsAuth"]))
        else:
           self.elasticSearchClient = getElasticsearchClient(self.config)

        self.queryTransformer = ElasticsearchQueryTransformer()

    def getFeatures(self, collectionID: str, limit=None, bbox=None, datetime=None):
        filters = []

        if bbox is not None:
            filters.append(self.queryTransformer.transformBBox(bbox))
        if datetime is not None:
            filters.append(self.queryTransformer.transformDateTime(datetime, temporalProperty=self.getTypeConfigForCollection(collectionID)["temporalProperty"])) 

        if len(filters) > 0:
            esQuery={
                    "query": {
                        "bool": {
                        "must": {
                            "match_all": {}
                        },
                        "filter": filters
                        }
                      }
                    }
        else:
            esQuery = {"query": {"match_all": {}}}

        response = None
        if limit is not None:
            response = self.elasticSearchClient.search(
                index=collectionID, body=esQuery, params=self.queryTransformer.transformLimit(limit))
        else:
            response = self.elasticSearchClient.search(
                index=collectionID, body=esQuery)

        features = self.getFeaturesFromESResponse(response, isGetFeaturesRequest= True)
        featureCollection = {
            "type": "FeatureCollection",
            "numberMatched": len(features),
            "numberReturned": len(features),
            "links": [{
                "href": request.url.split('?')[0],
                "rel": "self,"
		    }],
            "features": features
        }

        if len(features) > 0:
            featureCollection["bbox"] = self.mergeBBoxes(self.collectBBoxes(features))

        return featureCollection

    def getFeature(self, collectionID: str, featureID: str):
        filter = self.queryTransformer.transformID(featureID)
        esQuery = {"query": filter}

        response = self.elasticSearchClient.search(
            index=collectionID, body=esQuery)
        
        feature = self.getFeaturesFromESResponse(response)

        if len(feature) > 0:
            return feature[0] #id query only matches a single feature
        else:
            return Exception(code= "404", description="feature {0} not found".format(featureID)), 404

        

    def getCollection(self, collectionID: str):
        typeConfig = self.getTypeConfigForCollection(collectionID)
        bbox = typeConfig["bbox"]
        extent = ExtentSpatial(bbox=[[bbox[0], bbox[1]], [bbox[2], bbox[3]]])

        return Collection(
            id=collectionID, title=typeConfig["title"], description=typeConfig["description"], extent=extent)

    def getCollections(self, collectionsIDs: List):
        colls = []
        for collID in collectionsIDs:
            colls.append(self.getCollection(collID))
        
        return colls

    def getFeaturesFromESResponse(self, esResponse, isGetFeaturesRequest = False):
        features = []
        for hit in esResponse['hits']['hits']:
            feature = (hit['_source'])

            selfLink = { # add self link to each feature
                "href": request.url.split('?')[0],
                "rel": "self,"
		    }

            if isGetFeaturesRequest:
                selfLink["href"] = selfLink["href"] + "/" +feature["id"]

            if "links" in feature and len(feature["links"]) > 0:
                feature["links"].append(selfLink)
            else:
                feature["links"] = [selfLink]
            
            features.append(feature)

        return features

    def mergeBBoxes(self, bboxes):
        mergedBBox = bboxes[0]

        for i in range(1, len(bboxes)-1):
            if bboxes[i][0] < mergedBBox[0]:
                mergedBBox[0] = bboxes[i][0]
            if bboxes[i][1] > mergedBBox[1]:
                mergedBBox[1] = bboxes[i][1]
            if bboxes[i][2] < mergedBBox[2]:
                mergedBBox[2] = bboxes[i][2]
            if bboxes[i][3] > mergedBBox[3]:
                mergedBBox[3] = bboxes[i][3]

        return mergedBBox

    def collectBBoxes(self, features):
        bboxes = []
        for feature in features:
            if 'bbox' in feature:
                bboxes.append(feature['bbox'])

        return bboxes

    def getTypeConfigForCollection(self, collectionId):
        return self.config["types"][collectionId]
