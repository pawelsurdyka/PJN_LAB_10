import requests, json
from tqdm import tqdm

from core.utils import load_jsonl
from core.embeddings import embed_text
from core.ner import extract_entities
from core.dates import extract_dates
from config import ES_URL, ES_INDEX, HEADERS

DATA_PATH = "data/culturax_pl_clean.jsonl"

def main():
    docs = load_jsonl(DATA_PATH)

    for doc in tqdm(docs, desc="Indexing ES"):
        text = doc["text"]

        entities = extract_entities(text)
        dates = extract_dates(text)

        payload = {
            "id": doc["id"],
            "text": text,
            "domain": doc.get("domain"),
            "embedding": embed_text(text).tolist(),
            "entities": (
                entities["persons"]
                + entities["organizations"]
                + entities["locations"]
            ),
            "years": dates["years"]
        }

        r = requests.post(
            f"{ES_URL}/{ES_INDEX}/_doc/{doc['id']}",
            headers=HEADERS,
            data=json.dumps(payload)
        )
        r.raise_for_status()

    print("✅ Elasticsearch reindexing finished")

if __name__ == "__main__":
    main()
