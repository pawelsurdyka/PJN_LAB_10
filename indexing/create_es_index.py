import requests, json
from config import ES_URL, ES_INDEX, HEADERS

MAPPING_PATH = "indexing/es_mapping.json"

def main():
    # usuń jeśli istnieje
    requests.delete(f"{ES_URL}/{ES_INDEX}")

    with open(MAPPING_PATH, "r") as f:
        mapping = json.load(f)

    r = requests.put(
        f"{ES_URL}/{ES_INDEX}",
        headers=HEADERS,
        data=json.dumps(mapping)
    )
    r.raise_for_status()
    print("✅ Elasticsearch index created")

if __name__ == "__main__":
    main()
