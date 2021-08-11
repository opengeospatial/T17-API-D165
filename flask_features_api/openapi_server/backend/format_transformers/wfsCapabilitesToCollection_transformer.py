from openapi_server.backend.format_transformers.format_transformer import FormatTransformer
from openapi_server.models.collection import Collection
from openapi_server.models.extent_spatial import ExtentSpatial
from xml.dom import minidom, expatbuilder

class WFSCapabilitiesToCollectionTransformer(FormatTransformer):

    def transform(self, input: str):
        """
            expects FeatureType xml node as String from WFS capabilites document as input
        """

        featureTypeDOM = expatbuilder.parseString(input, False)
        collection = self.parseFeatureType(featureTypeDOM)

        return collection


    
    def parseFeatureType(self, featureTypeXML):
        id = self.getElementValue(featureTypeXML, "Name")
        title = self.getElementValue(featureTypeXML, "Title")
        description = self.getElementValue(featureTypeXML, "Abstract")

        extent = self.parseBBox(featureTypeXML.getElementsByTagNameNS("*", "WGS84BoundingBox")[0]) #bbox occurs only once

        return Collection(id=id, title=title, description=description, extent= extent)

    def parseBBox(self, bboxXML):
        lower = self.getElementValue(bboxXML, "LowerCorner")
        upper = self.getElementValue(bboxXML, "UpperCorner")

        lowerSplit = lower.split(" ");
        upperSplit = upper.split(" ");
        lowerSplit.extend(upperSplit)

        return ExtentSpatial(bbox= [lowerSplit])

    def getElementValue(self, dom, elementName):
        elements = dom.getElementsByTagNameNS("*", elementName) #ignore namespace
        if len(elements) > 0:
            return elements[0].firstChild.nodeValue #only first occurence
        else:
            return None

