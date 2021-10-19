from openapi_server.backend.dataquery_transformers.netcdf_dataquery_transformer import NetCDFDataQueryTransformer
from openapi_server.backend.request_transformer import RequestTransformer
from typing import List
from openapi_server.models.collection import Collection
from openapi_server.models.extent_spatial import ExtentSpatial
from openapi_server.models.extent_temporal import ExtentTemporal
from openapi_server.models.instances import Instances
from openapi_server.models.extent import Extent
from dateutil.parser import parse

class NetCDFRequestTransformer(RequestTransformer):

    def __init__(self, netCDFConfig: dict):
        self.netCDFConfig = netCDFConfig
        self.dataQueryTransformer = NetCDFDataQueryTransformer(netCDFConfig)


    def getCollection(self, collectionID: str):
        collConfig = self.getCollectionConfig(collectionID)
        mergedBbox = self.mergeBBoxes(self.collectBBoxes(collectionID))
        mergedInterval = self.mergeTempIntervals(self.collectTempIntervals(collectionID))
        extent = Extent(spatial= ExtentSpatial(bbox=[[mergedBbox[0],mergedBbox[1]],[mergedBbox[2],mergedBbox[3]]]), temporal=ExtentTemporal(interval=[mergedInterval]))

        params = collConfig["parameter_names"] if "parameter_names" in collConfig else None

        return Collection(
            id=collectionID, title=collConfig["title"], description=collConfig["description"], extent=extent, parameter_names= params, output_formats=["application/x-netcdf"], item_type="coverage")


    def getCollections(self, collectionsIDs: List):
        colls = []

        for coll in collectionsIDs:
            colls.append(self.getCollection(coll))

        return colls

    def getInstances(self, collectionID: str):
        instConfigs = self.getCollectionConfig(collectionID)["instances"]
        instances = []
        for instanceId in instConfigs.keys():
            instConfig = self.getInstanceConfig(collectionID, instanceId)
            params = instConfig["parameter_names"] if "parameter_names" in instConfig else None
            extent = Extent(spatial = ExtentSpatial(bbox=[[instConfig["bbox"][0],instConfig["bbox"][1]],[instConfig["bbox"][2],instConfig["bbox"][3]]]), temporal=ExtentTemporal(interval = [[parse(instConfig["timeinterval"][0]), parse(instConfig["timeinterval"][1])]]))

            instances.append(Collection(id = instanceId, title= instConfig["title"], description=instConfig["description"], item_type="coverage", output_formats=["application/x-netcdf"], parameter_names=params, extent= extent))

        return Instances(instances=instances)

    def getDataQueryTransformer(self):
        return self.dataQueryTransformer


    def getCollectionConfig(self, collectionId):
        return self.netCDFConfig["collections"][collectionId]

    def getInstanceConfig(self, collectionId, instanceId):
        return self.getCollectionConfig(collectionId=collectionId)["instances"][instanceId]


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

    def collectBBoxes(self, collectionId):
        bboxes = []
        for instanceId in self.getCollectionConfig(collectionId)["instances"].keys():
            instConfig = self.getInstanceConfig(collectionId, instanceId)
            if 'bbox' in instConfig:
                bboxes.append(instConfig['bbox'])

        return bboxes


    def mergeTempIntervals(self, tempIntervals):
        mergedInterval = [parse(tempIntervals[0][0]), parse(tempIntervals[0][1])]

        for i in range(1, len(tempIntervals)-1):
            dtStart = parse(tempIntervals[i][0])
            dtEnd = parse(tempIntervals[i][1])

            if dtStart < mergedInterval[0]:
                mergedInterval[0] = dtStart
            if dtEnd > mergedInterval[1]:
                mergedInterval[1] = dtEnd

        return mergedInterval

    def collectTempIntervals(self, collectionId):
        tempIntervals = []
        for instanceId in self.getCollectionConfig(collectionId)["instances"].keys():
            instConfig = self.getInstanceConfig(collectionId, instanceId)
            if 'timeinterval' in instConfig:
                tempIntervals.append(instConfig['timeinterval'])

        return tempIntervals