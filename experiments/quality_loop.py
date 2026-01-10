import json
from collections import defaultdict
from core.retrieval import retrieve_documents
from core.llm import generate_answer
from core.ner import extract_entities
from core.dates import extract_dates

BENCHMARK_PATH = "evaluation/benchmark.json"
OUTPUT_PATH = "evaluation/quality_results.json"

K = 5


def check_citations(answer: str, contexts: list) -> bool:
    return any(ctx["text"][:50] in answer for ctx in contexts)


def check_year_consistency(contexts: list, min_year=2020) -> bool:
    for ctx in contexts:
        years = ctx.get("years", [])
        if any(y < min_year for y in years):
            return False
    return True


def check_entity_overlap(answer: str, contexts: list) -> bool:
    entities = set()
    for ctx in contexts:
        for e in ctx.get("named_entities", []):
            entities.add(e.lower())
    return any(e in answer.lower() for e in entities)


def main():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    results = []

    for item in benchmark:
        query = f"Jak zmienia się sposób mówienia o {item['topic']} po 2020 roku?"

        contexts = retrieve_documents(
            query=query,
            method="hybrid",
            years=[2020, 2021, 2022, 2023],
            k=K
        )

        answer = generate_answer(
            question=query,
            contexts=contexts
        )

        entities_dict = extract_entities(answer)

        all_entity_names = (
                entities_dict["persons"] +
                entities_dict["organizations"] +
                entities_dict["locations"]
        )

        results.append({
            "query": query,
            "context": contexts,
            "topic": item["topic"],
            "label": item["label"],
            "citation": 1 if check_citations(answer, contexts) else 0,
            "dates": 1 if check_year_consistency(extract_dates(answer)["years"]) else 0,
            "entitiies": all_entity_names,
            "answer": answer
        })

        print(f"✔ {item['topic']} | label={item['label']}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ QUALITY LOOP zakończony → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
