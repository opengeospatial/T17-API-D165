import connexion
from  openapi_server import encoder
import openapi_server.backend.backendConfiguration as backends


#init backend configuration
backends.initBackendConfig("backend_configuration.json")

app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'A sample API conforming to the candidate standard OGC API - Environmental Data Retrieval'},
            pythonic_params=True)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(port=8080)