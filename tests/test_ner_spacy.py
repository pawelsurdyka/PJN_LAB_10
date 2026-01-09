import random
from core.utils import load_jsonl
from core.ner import extract_entities

DATA_PATH = "data/culturax_pl_clean.jsonl"
N_SAMPLES = 25

def main():
    docs = load_jsonl(DATA_PATH)
    samples = random.sample(docs, N_SAMPLES)

    for i, doc in enumerate(samples, 1):
        text = doc["text"]

        entities = extract_entities(text)
        print(entities)

        print("=" * 80)
        print(f"[{i}] ID: {doc['id']}")
        print(text[:500], "...\n")
        print("PERSONS:", entities["persons"])
        print("ORGANIZATIONS:", entities["organizations"])
        print("LOCATIONS:", entities["locations"])

if __name__ == "__main__":
    main()
