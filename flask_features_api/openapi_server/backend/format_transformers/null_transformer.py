from openapi_server.backend.format_transformers.format_transformer import FormatTransformer

class NullTransformer(FormatTransformer):

    def transform(self, input: str):
        output = input
        return output