from enum import Enum
from logging import error
from openapi_server.backend.wfs_request_transformer import WFSRequestTransformer
from openapi_server.backend.query_transformers.query_transformer import QueryTransformer
from openapi_server.backend.request_transformer import RequestTransformer
from openapi_server.backend.query_transformers.wfs_query_transformer import WFSQueryTransformer

class BackendType(Enum):
    WFS = 1

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
        else:
            print("unkown backend type")

        




