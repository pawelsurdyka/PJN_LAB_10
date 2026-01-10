import json
from core.retrieval import retrieve_documents

OUTPUT_PATH = "evaluation/benchmark_candidates.json"

TOPICS = {
    "odpowiedzialność": "odpowiedzialność zespołowa",
    "przywództwo": "przywództwo i liderzy",
    "zaufanie": "zaufanie i jego utrata"
}

K = 30

def main():
    all_candidates = []

    for topic, query in TOPICS.items():
        results = retrieve_documents(
            query=query,
            method="hybrid",
            years=[2018, 2019, 2020, 2021, 2022, 2023],
            k=K
        )

        for r in results:
            all_candidates.append({
                "id": r["id"],
                "text": r["text"],
                "topic": topic
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, ensure_ascii=False, indent=2)

    print(f"Zapisano kandydatów do benchmarku → {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
