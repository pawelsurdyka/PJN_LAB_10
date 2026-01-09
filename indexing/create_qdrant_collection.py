import requests
from config import QDRANT_URL, QDRANT_COLLECTION

VECTOR_SIZE = 384

def main():
    # usuń kolekcję
    # requests.delete(f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}")

    payload = {
        "vectors": {
            "size": VECTOR_SIZE,
            "distance": "Cosine"
        }
    }

    r = requests.put(
        f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}",
        json=payload
    )
    r.raise_for_status()

    print("✅ Qdrant collection created")

if __name__ == "__main__":
    main()
