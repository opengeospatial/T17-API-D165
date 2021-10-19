from elasticsearch import Elasticsearch, RequestsHttpConnection


useSSL = True


def getElasticsearchClient(config, awsauth = None):
    searchClient = Elasticsearch(
        hosts = [{'host': config["baseURL"], 'port': config["port"]}],
        http_auth = awsauth,
        use_ssl = config["useSSL"],
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    return searchClient
