import requests
from tqdm import tqdm

from core.utils import load_jsonl
from core.embeddings import embed_text
from core.ner import extract_entities
from core.dates import extract_dates
from config import QDRANT_URL, QDRANT_COLLECTION

DATA_PATH = "data/culturax_pl_clean.jsonl"

def main():
    docs = load_jsonl(DATA_PATH)
    points = []

    for doc in tqdm(docs, desc="Indexing Qdrant"):
        if doc["id"] % 10 != 0:
            continue

        text = doc["text"]

        entities = extract_entities(text)
        dates = extract_dates(text)

        point = {
            "id": doc["id"],
            "vector": embed_text(text).tolist(),
            "payload": {
                "text": text,
                "domain": doc.get("domain"),
                "entities": (
                    entities["persons"]
                    + entities["organizations"]
                    + entities["locations"]
                ),
                "years": dates["years"]
            }
        }
        points.append(point)

        # batch co 100
        if len(points) >= 100:
            flush(points)
            points = []

    if points:
        flush(points)

    print("✅ Qdrant reindexing finished")

def flush(points):
    r = requests.put(
        f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points",
        json={"points": points}
    )
    r.raise_for_status()

if __name__ == "__main__":
    main()
