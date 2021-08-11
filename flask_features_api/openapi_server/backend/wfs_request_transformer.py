from typing import List
from urllib import parse
from openapi_server.backend.format_transformers.null_transformer import NullTransformer
from openapi_server.backend.format_transformers.wfsCapabilitesToCollection_transformer import WFSCapabilitiesToCollectionTransformer
from openapi_server.backend.request_transformer import RequestTransformer
from openapi_server.backend.dataaccess.http_access_layer import HTTPAccessLayer
from openapi_server.backend.query_transformers.wfs_query_transformer import WFSQueryTransformer
from xml.dom import minidom

class WFSRequestTransformer(RequestTransformer):

    def __init__(self, wfsBackendConfig: dict):
        self.wfsBackendConfig = wfsBackendConfig
        self.wfsBaseURL = wfsBackendConfig["baseURL"]
        self.http = HTTPAccessLayer()
        self.queryTransformer = WFSQueryTransformer()
        self.formatTransformer = NullTransformer() #ToDo should be converted from GML3
        self.capabilitesTransformer = WFSCapabilitiesToCollectionTransformer()

    
    def getFeatures(self, collectionID: str, limit=None, bbox=None, datetime=None):
        requestParams = {"request": "getFeature", "service" : "WFS", "version": "2.0.0", "outputFormat": "application/json", "typeNames": collectionID}
        
        if limit is not None:
            requestParams.update(self.queryTransformer.transformLimit(limit)) #merge dicts
        
        if bbox is not None:
            requestParams.update(self.queryTransformer.transformBBox(bbox)) #merge dicts

        if datetime is not None:
            temporalProperty = self.wfsBackendConfig["types"][collectionID]["temporalProperty"] #get property to filter on from config
            requestParams.update(self.queryTransformer.transformDateTime(datetime, temporalProperty)) #merge dicts

        backendResp = self.http.get(self.wfsBaseURL, requestParams)
        resp = self.formatTransformer.transform(backendResp)

        return resp

    def getFeature(self, collectionID: str, featureID: str):
        requestParams = {"request": "getFeature", "service" : "WFS", "version": "2.0.0", "outputFormat": "application/json", "typeName": collectionID}
        featureIdParams = self.queryTransformer.transformID(featureID)
        requestParams.update(featureIdParams) #merge dicts 

        backendResp = self.http.get(self.wfsBaseURL, requestParams)
        resp = self.formatTransformer.transform(backendResp)

        return resp

    def getCollection(self, collectionID: str):
        return self.getCollections([collectionID])[0] #only one collection in the list


    def getCollections(self, collectionsIDs: List):
        requestParams = {"request": "getCapabilities", "service" : "WFS", "version": "2.0.0", "outputFormat": "text/xml"}
        capabilitesXML = self.http.get(self.wfsBaseURL, requestParams)

        collections = [];
        for id in collectionsIDs:
            collection = self.parseWFSCapabilities(capabilitesXML, id)
            collections.append(collection)

        return collections



    def parseWFSCapabilities(self, capabilitiesXML: str, collectionID: str):       
        dom = minidom.parseString(capabilitiesXML)
        featureTypes = dom.getElementsByTagNameNS("*", "FeatureType") #ignore namespace

        for featureType in featureTypes:
            featureTypeID = featureType.getElementsByTagNameNS("*", "Name")
            if featureTypeID[0].firstChild.data == collectionID: #Name tag occurs only one within each FeatureType tag
                return self.capabilitesTransformer.transform(featureType.toxml("utf-8")) #as string
            
