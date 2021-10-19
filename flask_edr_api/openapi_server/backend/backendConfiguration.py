import json
from logging import error
from openapi_server.backend.data_backend import BackendType, DataBackend


_backendConfiguration = None
_availableDataBackends = []

def initBackendConfig(backendConfigJsonPath: str):
    global _backendConfiguration
    global _availableDataBackends

    # Parse JSON into an object with attributes corresponding to dict keys.
    with open(backendConfigJsonPath) as f:
        configDict = json.load(f)
        _backendConfiguration = configDict

    for backend in _backendConfiguration["backends"]:
        _availableDataBackends.append(DataBackend(id = backend["id"], backendType = getBackendTypeFromString(backend["type"]), availableCollections = backend["collections"], config= backend["config"]))


def getBackendConfiguration():
    if _backendConfiguration is not None:
        return _backendConfiguration
    else:
        raise ValueError("backend configuration is not initialized")


def getAvailableDataBackends():
    return _availableDataBackends


def getBackendTypeFromString(backendTypeStr: str):
    if backendTypeStr.lower() == "netcdf":
        return BackendType.NETCDF
    else:
        raise error("unknown backend type " + backendTypeStr)


def getDataBackendForCollection(collectionID: str):
    for backend in _availableDataBackends:
        if collectionID in backend.availableCollections:
            return backend

    return None