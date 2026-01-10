import random
from core.utils import load_jsonl
from core.dates import extract_dates

DATA_PATH = "data/culturax_pl_clean.jsonl"
N_SAMPLES = 5

def main():
    docs = load_jsonl(DATA_PATH)
    samples = random.sample(docs, N_SAMPLES)

    for i, doc in enumerate(samples, 1):
        text = doc["text"]

        dates = extract_dates(text)

        print("=" * 80)
        print(f"[{i}] ID: {doc['id']}")
        print(text[:500], "...\n")
        print("YEARS:", dates["years"])
        print("DATES:", dates["dates"])
        print("RANGES:", dates["ranges"])

if __name__ == "__main__":
    main()
