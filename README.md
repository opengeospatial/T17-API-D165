# OGC Testbed 17 - API Experiments - D165 Python Server
The API Experiments Server implementation comprises separate implementations of [OGC API - Features (Features)](https://ogcapi.ogc.org/features/) and [OGC API - Environmental Data Retrieval (EDR)](https://ogcapi.ogc.org/edr/). Both server implementations are developed in Python programming language and around the Flask web framework. Flask provides the core capabilities to implement web interfaces. The basic implementation of both OGC API Standards is supported by the use of code generators. The model classes and controller classes (server stubs) are automatically generated from the respective OpenAPI specifications of Features and EDR by using the [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) project. OpenAPI Generator offers a specific code generator that produces basic Flask-based executable server applications.

This development was part of the OGC Testbed 17 API Experiments thread.

## Structure of this Repository
This repository consists of two separate server applications (one for OGC API - Features and one for OGC API EDR). For each of these applications there is a separate project in the subfolders of this repository. The subfolders readme files contain specific information about the code structure and deployment.
### OGC API Features
Click [here](https://github.com/opengeospatial/T17-API-D165/tree/main/flask_features_api) to go to OGC API - Features implementation
### OGC API Environmental Data Retrieval
Click [here](https://github.com/opengeospatial/T17-API-D165/tree/main/flask_edr_api) to go to OGC API - EDR implementation.

