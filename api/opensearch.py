from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from api.config import config
from sqlalchemy import create_engine, text
from api.config import config

host = config.OPEN_SEARCH_HOST
port = config.OPEN_SEARCH_PORT
auth = (config.OPEN_SEARCH_LOGIN, config.OPEN_SEARCH_PASSWORD)

index_name = "addresses"


def connect():
    return OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        use_ssl=True,
        http_auth=auth,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )


def create_index(index_name: str):
    client = connect()
    index_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "standard_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase"],
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "full_address": {
                    "type": "text",
                    "analyzer": "standard_analyzer",
                }
            }
        },
    }

    try:
        response = client.indices.create(index=index_name, body=index_body)
        print("Index created:", response)
    except Exception as e:
        print("Error creating index:", e)


def insert_data(documents: list[dict], index_name):
    client = connect()
    actions = [
        {
            "_op_type": "index",
            "_index": index_name,
            "_source": {
                **doc,
                "address_suggest": {
                    "input": [doc["full_address"]],
                    "weight": 1,
                },
            },
        }
        for doc in documents
    ]
    success, failed = bulk(client, actions)
    print(f"Successfully indexed {success} documents.")
    if failed:
        print(f"Failed to index {len(failed)} documents.")


def fuzzy_search(partial_name: str, limit: int = 5):
    client = connect()
    search_query = {
        "query": {
            "match": {
                "full_address": {
                    "query": partial_name,
                    "fuzziness": "5",
                }
            }
        },
        "size": limit,
        "sort": [
            {
                "_score": {"order": "desc"}
            }  # Ensure results are sorted by relevance
        ],
    }

    response = client.search(index=index_name, body=search_query)
    hits = response.get("hits", {}).get("hits", [])

    results = [
        {
            "street_name": hit["_source"].get("street_name"),
            "house_number": hit["_source"].get("house_number"),
            "city": hit["_source"].get("city"),
            "postcode": hit["_source"].get("postcode"),
            "id": hit["_source"].get("id"),
            "full_address": hit["_source"].get("full_address"),
        }
        for hit in hits
    ]

    return results


def find_address_by_partial_name(partial_name: str, limit: int = 5):

    results = fuzzy_search(partial_name, limit)

    return results


def delete_index(index_name: str):
    client = connect()
    try:
        response = client.indices.delete(index=index_name)
        print("Index deleted:", response)
    except Exception as e:
        print("Error deleting index:", e)


def get_all_addresses_from_postgres():
    db_url = config.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(db_url)
    query = text("SELECT * FROM addresses")
    dict_results = []
    with engine.connect() as connection:
        results = connection.execute(query)
    for result in results:
        dict_results.append(
            {
                "street_name": result.street_name,
                "house_number": result.house_number,
                "city": result.city,
                "postcode": result.postcode,
                "id": result.id,
                "full_address": result.full_address,
            }
        )
    return dict_results


def load_data():
    delete_index(index_name)
    create_index(index_name)
    address_data = get_all_addresses_from_postgres()
    insert_data(address_data, index_name)


if config.UPDATE_OPENSEARCH_DATA:
    load_data()
