from typing import List

class RequestTransformer:
    
    def getFeatures(self, collectionID: str, limit=None, bbox=None, datetime=None):
        pass

    def getFeature(self, collectionID: str, featureID: str):
        pass

    def getCollection(self, collectionID: str):
        pass

    def getCollections(self, collectionsIDs: List):
        pass