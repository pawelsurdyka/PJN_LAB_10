from collections import defaultdict

from core.embeddings import embed_text
from core.elastic import es_bm25_search
from core.qdrant import qdrant_vector_search, qdrant_build_filter


# ======================================================
# PUBLICZNY INTERFEJS
# ======================================================

def retrieve_documents(
    query: str,
    method: str,
    entities=None,
    years=None,
    k: int = 10
) -> list[dict]:

    if method == "bm25":
        return _retrieve_bm25(query, k)

    if method == "qdrant":
        return _retrieve_qdrant(query, entities, years, k)

    if method == "hybrid":
        return _retrieve_hybrid(query, entities, years, k)

    raise ValueError(f"Unknown retrieval method: {method}")


# ======================================================
# BM25 – ELASTICSEARCH
# ======================================================

def _retrieve_bm25(query: str, k: int) -> list[dict]:
    hits = es_bm25_search(query, k)
    return [
        {
            "id": h["_id"],
            "text": h["_source"]["text"],
            "score": h["_score"],
            "source": "es",
            "rank": i + 1
        }
        for i, h in enumerate(hits)
    ]


# ======================================================
# QDRANT – VECTOR SEARCH
# ======================================================

def _retrieve_qdrant(query: str, entities, years, k: int) -> list[dict]:
    vector = embed_text(query, prefix="query")
    flt = qdrant_build_filter(entities, years)

    results = qdrant_vector_search(
        query_vector=vector,
        limit=k,
        filters=flt
    )

    return [
        {
            "id": r["id"],
            "text": r["payload"]["text"],
            "score": r["score"],
            "source": "qdrant",
            "rank": i + 1
        }
        for i, r in enumerate(results)
    ]


# ======================================================
# HYBRYDA – RRF (RANK-BASED)
# ======================================================

def _retrieve_hybrid(query: str, entities, years, k: int) -> list[dict]:
    es_results = _retrieve_bm25(query, k)
    qd_results = _retrieve_qdrant(query, entities, years, k)

    scores = defaultdict(float)
    docs = {}

    # ES → RRF
    for r in es_results:
        scores[r["id"]] += 1.0 / r["rank"]
        docs[r["id"]] = r

    # Qdrant → RRF
    for r in qd_results:
        scores[r["id"]] += 1.0 / r["rank"]
        docs[r["id"]] = r

    # sortowanie po RRF score
    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for doc_id, score in ranked[:k]:
        d = docs[doc_id]
        results.append({
            "id": doc_id,
            "text": d["text"],
            "rrf_score": score
        })

    return results
