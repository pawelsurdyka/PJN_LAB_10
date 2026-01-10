import json

CANDIDATES_PATH = "evaluation/benchmark_candidates.json"
OUTPUT_PATH = "evaluation/benchmark.json"

# ===== RĘCZNA SELEKCJA =====

SELECTION = {
    "odpowiedzialność": {
        "relevant": [140, 510, 380, 840, 410],
        "noise":    [980, 370, 150, 790, 510]
    },
    "przywództwo": {
        "relevant": [40, 20, 1000, 450, 470],
        "noise":    [310, 630, 980, 150, 900]
    },
    "zaufanie": {
        "relevant": [350, 570, 240, 500, 960],
        "noise":    [630, 980, 310, 150, 370]
    }
}


def main():
    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    by_id = {int(doc["id"]): doc for doc in candidates}

    benchmark = []

    for topic, labels in SELECTION.items():
        for label, ids in labels.items():
            for doc_id in ids:
                if doc_id not in by_id:
                    print(f"ID {doc_id} nie znalezione w kandydatach – pomijam")
                    continue

                doc = by_id[doc_id]
                benchmark.append({
                    "id": str(doc_id),
                    "text": doc["text"],
                    "label": label,
                    "topic": topic
                })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, ensure_ascii=False, indent=2)

    print(f"Benchmark zapisany → {OUTPUT_PATH}")
    print(f"Liczba rekordów: {len(benchmark)}")


if __name__ == "__main__":
    main()
