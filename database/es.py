import os
from opensearchpy import OpenSearch

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "192.168.0.105")
OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", 9200)
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "admin")

def fuzzy_search(query) -> list[str]:
    opensearch = OpenSearch(
        hosts = [{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_auth = (OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

    query_body = {
        "query": {
            "fuzzy": {
                "full": {
                    "value": query,
                    "fuzziness": 200
                }
            }
        }
    }
    result = opensearch.search(index='addresses', body=query_body)
    return [hit['_source']['full'] for hit in result['hits']['hits']][:5]