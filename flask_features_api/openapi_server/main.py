import openapi_server.backendConfiguration as backends
import connexion
from  openapi_server import encoder



#init backend configuration
backends.initBackendConfig("backend_configuration.json")

app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'A sample API conforming to the draft standard OGC API - Features - Part 1: Core'},
            pythonic_params=True)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(port=8080)