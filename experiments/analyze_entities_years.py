import json
from collections import Counter, defaultdict
from core.ner import extract_entities
from core.dates import extract_dates

BENCHMARK_PATH = "evaluation/benchmark.json"

def normalize_entity(e: str) -> str:
    return e.lower().strip()

def main():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = defaultdict(lambda: {
        "relevant": {
            "entities": Counter(),
            "years": Counter()
        },
        "noise": {
            "entities": Counter(),
            "years": Counter()
        }
    })

    for doc in data:
        print(doc["id"])
        topic = doc["topic"]
        label = doc["label"]
        text  = doc["text"]

        entities_dict = extract_entities(text)
        dates_dict = extract_dates(text)

        all_entity_names = (
                entities_dict["persons"] +
                entities_dict["organizations"] +
                entities_dict["locations"]
        )

        # print(entities)
        # print(years)

        # stats[topic][label]["entities"].update(entities)
        # stats[topic][label]["years"].update(years)
        stats[topic][label]["entities"].update(all_entity_names)
        stats[topic][label]["years"].update(dates_dict["years"])  # Tutaj też przekazujemy listę lat

    # ===== RAPORT TEKSTOWY =====
    for topic, topic_stats in stats.items():
        print("\n" + "=" * 80)
        print(f"🧠 TEMAT: {topic.upper()}")

        for label in ["relevant", "noise"]:
            print("\n" + "-" * 40)
            print(f"{label.upper()}")

            print("\nTop encje:")
            for ent, cnt in topic_stats[label]["entities"].most_common(10):
                print(f"  {ent}: {cnt}")

            print("\nTop lata:")
            for year, cnt in topic_stats[label]["years"].most_common(10):
                print(f"  {year}: {cnt}")

    print("\n✅ Analiza zakończona")

if __name__ == "__main__":
    main()
