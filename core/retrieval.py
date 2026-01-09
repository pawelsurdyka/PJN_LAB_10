from core.embeddings import embed_text
from core.elastic import es_bm25_search, es_vector_search
from core.qdrant import qdrant_vector_search, qdrant_build_filter

def retrieve_documents(
    query: str,
    method: str,
    entities=None,
    years=None,
    k: int = 10
) -> list[dict]:

    if method == "bm25":
        return es_bm25_search(query, k)

    if method == "es_vector":
        vec = embed_text(query, "query")
        return es_vector_search(vec, k)

    if method == "qdrant":
        vec = embed_text(query, "query")
        flt = qdrant_build_filter(entities, years)
        return qdrant_vector_search(vec, k, flt)

    raise ValueError(f"Unknown retrieval method: {method}")
