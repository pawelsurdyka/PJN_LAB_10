import json
import requests
import numpy as np
from config import ES_URL, ES_INDEX, HEADERS

def es_search(query_body: dict) -> dict:
    url = f"{ES_URL}/{ES_INDEX}/_search"
    r = requests.post(url, headers=HEADERS, data=json.dumps(query_body))
    r.raise_for_status()
    return r.json()

def es_bm25_search(query: str, size: int = 10) -> list[dict]:
    body = {
        "size": size,
        "query": {
            "match": {
                "text": query
            }
        }
    }
    return es_search(body)["hits"]["hits"]

def es_vector_search(query_vector: np.ndarray, size: int = 10) -> list[dict]:
    body = {
        "size": size,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.q, 'embedding') + 1.0",
                    "params": {"q": query_vector.tolist()}
                }
            }
        }
    }
    return es_search(body)["hits"]["hits"]

def es_apply_filters(base_query: dict, entities=None, years=None) -> dict:
    filters = []

    if entities:
        filters.append({"terms": {"entities": entities}})
    if years:
        filters.append({"terms": {"years": years}})

    if not filters:
        return base_query

    return {
        "bool": {
            "must": base_query,
            "filter": filters
        }
    }
