"# T17-API-D165" 
# Deployment
This section contains information on how to deploy the python server implementation(s).
## OGC API - Features
### Docker
There is a docker image available that deploys the OGC API - Features server (python flask app) with _uwsgi_ and _nginx_ in a single container.  
The docker image can be pulled from Docker Hub.  
`docker pull arnevogt/tb17_apiexperiments_featuresserver_python` (location will be changed in the near future)  
Port _8080_ is exposed.  
To start a docker container run the following command:  
`docker run -p 8080:8080 arnevogt/tb17_apiexperiments_featuresserver_python`
#### Configuration
The default backend configuration can be overridden by binding a local configuration file to the docker container. This can be done by adding a volume binding to the above run command.  
`-v /path/to/backend_configuration.json:/usr/src/app/backend_configuration.json`  
The default configuration is equal to the example configuration file below.  

##### OGC WFS backend
The OGC API - Feature implementation currently uses OGC WFS implementations as data backends. The data backends are defined in a configuration (JSON) file.  
- _type_ attribute must be "WFS" for OGC WFS backends
- _collections_ attribute contains a list of WFS feature types that should be served through OGC API Features
  - feature type name equals collection name
- the _type_ attribute contains feature type/collection specific configuration
  - _temporalProperty_ specifies the property that is considered for datetime filter requests
##### Elasticsearch backend
The OGC API - Feature implementation is able to serve geojson features that are indexed in an elasticsearch index.  The Elasticsearch backend is primarily made to serve OGC API records features. Though generic geojson features could be served, datetime format must be the same as in OGC API - Records.  
- _type_ attribute must be "Elasticsearch" for elasticsearch backends
- collections attribute contains a list of elasticsearch indexes that should be made available through OGC API Features
  - index name equals collection name
- the type attribute contains index/collection specific configuration
  - _temporalProperty_ specifies the property that is considered for datetime filter requests
  - _description_, _title_ and _bbox_ attributes define collection metadata that is provided through the _/collections_ endpoint of OGC API - Features

###### AWSAuth
_awsAuth_ property must be defined if the elasticsearch instances is actually an AWS Elasticsearch Service instance.  
Authentication is handled by boto3 (AWS client libbray for python). Credentials can be either provided in a [credentials file](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file) or as [environment variables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#environment-variables) (inside the docker container).  
  
In order to use a credentials file the file can be mounted into the docker container:  
`-v path/to/.aws/credentials:/root/.aws/credentials:ro`  
The host path depends on the operating system of the host system and user specific settings.  
  
Alternatively, credentials can be passed as [environment variables in the docker run command](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file). At least _AWS_ACCESS_KEY_ID_ and _AWS_SECRET_ACCESS_KEY_ environment variables must be passed in the run command.  
  
- _region_ attribute specifies the AWS region in which the elasticsearch service instance is hosted
- (optional) _profile_ attribute: only needed if credentials are provided by credentials file an profile is not _default_.
  
**Example Backend Configuration**
<details>
<summary>backend_configuration.json</summary>
<p>

```json
{
	"server": {
		"title": "TB-17 Experiments API Python Server",
		"description": "TB-17 Experiments API Python Server"
	},
	"backends": [
		{
	    "id": "cuberworxWFS_Foundation",
            "type": "WFS",
	    "config": {
				"baseURL": "https://test.cubewerx.com/cubewerx/cubeserv/demo?datastore=Foundation",
				"types": {
					"cw:coastl_1m": {
						"temporalProperty": null
					}
				}
			},
			"collections": [
				"cw:coastl_1m"
			]
		},
		{
	    "id": "api_records_collection",
            "type": "Elasticsearch",
			"config": {
				"baseURL": "my-es-service.eu-west-2.es.amazonaws.com",
				"port": 443,
				"useSSL": true,
				"types": {
					"record-index": {
						"temporalProperty": "extents.temporal.interval",
						"description": "a collection of api records items",
						"title": "api records",
						"bbox": [-180.0,-90.0,180.0,90.0]
					}
				},
				"awsAuth": {
					"region": "eu-west-2"
				}
			},
			"collections": [
				"record-index"
			]
		}
	]
}
```

</p>
</details>

## OGC API - Environmental Data Retrieval (EDR) 
### Docker
There is a docker image available that deploys the OGC API - EDR server (python flask app) with _uwsgi_ and _nginx_ in a single container.  
The docker image can be pulled from Docker Hub.  
`docker pull arnevogt/tb17_apiexperiments_edrsserver_python` (location will be changed in the near future)  
Port _8080_ is exposed.  
To start a docker container run the following command:  
`docker run -p 8080:8080 arnevogt/tb17_apiexperiments_edrsserver_python`
#### Configuration
The default backend configuration can be overridden by binding a local configuration file to the docker container. This can be done by adding a volume binding to the above run command.  
`-v /path/to/backend_configuration.json:/usr/src/app/backend_configuration.json`  
The default configuration is equal to the example configuration file below.  

##### NetCDF Backend
The OGC API - EDRimplementation currently uses netCDF files as data backends. The data backends are defined in a configuration (JSON) file.  
- _type_ attribute must be "NETCDF" for netCDF backends
- in EDR each collection consists of multiple instances (which are again collections)
- for NetCDF backend each instance represents a netCDF file
  - every netCDF file must consist of a singe data array which has the dimensions _x_,_y_ and _time_.

The netCDF file that is configured in the example configuration (see below) is contained in the docker image and can be used as demo data. In order to add other data it is necessary to mount a data directory of the host system to the docker container.  
The _filepath_ parameter in the instance configuration (relative or absolute) always refers to the container (not to the host system).


  
**Example Backend Configuration**
<details>
<summary>backend_configuration.json</summary>
<p>

```json
{
	"server": {
		"title": "TB-17 Experiments API Python Server",
		"description": "TB-17 Experiments API Python Server"
	},
	"backends": [
		{
			"id": "example_netcdf_backend",
			"type": "NETCDF",
			"config": {
				"collections": {
					"netcdf_collection": {
						"title": "Sample NetCDF Collection",
						"description": "this is a sample NetCDF collection",
						"instances": {
							"instanceA": {
								"title": "Sample NetCDF Instance A",
								"description": "this is a sample instance of a sample NetCDF collection ",
								"bbox": [
									-180.0,
									-90.0,
									180.0,
									90.0
								],
								"timeinterval": [
									"2000-01-01",
									"2021-01-01"
								],
								"filePath": "./openapi_server/data/20191115T102219-20201214T101151_classification.nc"
							}
						}
					}
				}
			},
			"collections": [
				"netcdf_collection"
			]
		}
	]
}
```

</p>
</details>

### Data Queries
The EDR server implementation supports radius, position and area data queries.
#### radius query
- _/radius_ endpoint
- within: radius
- within_units: unit of the radius, either M (meter) or KM (kilometer)
- radius_coords: center of the circle (WKT Point geometry), WGS84)
- datetime: either a single datetime or a interval (_start/end_), use _.._ for open intervals (_../end_, _start/.._)
  
example:  
`http://localhost:8080/collections/netcdf_collection/instances/instanceA/radius?within=10&within-units=KM&radiusCoords=POINT(37.64830%20-1.65650)&datetime=2020-12-14%2000:00:00`
#### position query 
- _/position_ endpoint
- coords: coords of the position (WKT Point geometry), WGS84)
- datetime: see above

#### area query 
- _/area_ endpoint
- coords: coords of the area geometry(WKT Polygon geometry), WGS84)
- datetime: see above
