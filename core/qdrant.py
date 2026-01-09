import requests
import numpy as np
from config import QDRANT_URL, QDRANT_COLLECTION

def qdrant_search(payload: dict) -> dict:
    url = f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points/search"
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

def qdrant_vector_search(
    query_vector: np.ndarray,
    limit: int = 10,
    filters: dict | None = None
) -> list[dict]:
    payload = {
        "vector": query_vector.tolist(),
        "limit": limit,
        "with_payload": True
    }
    if filters:
        payload["filter"] = filters

    return qdrant_search(payload)["result"]

def qdrant_build_filter(entities=None, years=None) -> dict | None:
    must = []

    if entities:
        must.append({"key": "entities", "match": {"any": entities}})
    if years:
        must.append({"key": "years", "match": {"any": years}})

    if not must:
        return None

    return {"must": must}
