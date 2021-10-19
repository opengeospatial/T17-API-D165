from enum import Enum
from logging import error
from openapi_server.backend.wfs_request_transformer import WFSRequestTransformer
from openapi_server.backend.elasticsearch_request_transformer import ElasticsearchRequestTransformer
from openapi_server.backend.request_transformer import RequestTransformer


class BackendType(Enum):
    WFS = 1
    ELASTICSEARCH =2

class DataBackend:

    def __init__(self, id: str, backendType: BackendType, availableCollections: list , config: dict):
        self.requestTransformer: RequestTransformer 

        self.id = id
        self.availableCollections = availableCollections
        self.backendType = backendType
        self.config = config

        if backendType is BackendType.WFS:
            if "baseURL" not in config:
                raise ValueError("parameter baseURL is missing in config")

            self.requestTransformer = WFSRequestTransformer(config)
        elif backendType is BackendType.ELASTICSEARCH:
            if "baseURL" not in config:
                raise ValueError("parameter baseURL is missing in config")
            self.requestTransformer = ElasticsearchRequestTransformer(config)
        else:
            print("unkown backend type")

        




