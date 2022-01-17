from enum import Enum
from logging import error
from openapi_server.backend.netcdf_request_transformer import NetCDFRequestTransformer
from openapi_server.backend.request_transformer import RequestTransformer

class BackendType(Enum):
    NETCDF = 1

class DataBackend:
    """
     DataBackend associates backend configuration with the corresponding request transformer for the backend type
    """

    def __init__(self, id: str, backendType: BackendType, availableCollections: dict , config: dict):
        self.requestTransformer: RequestTransformer 

        self.id = id
        self.availableCollections = availableCollections
        self.backendType = backendType
        self.config = config

        if backendType is BackendType.NETCDF:
            self.requestTransformer = NetCDFRequestTransformer(config)

        else:
            print("unkown backend type")

        




