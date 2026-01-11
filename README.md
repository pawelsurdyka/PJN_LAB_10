---

# Inteligentny RAG (Lab 10)

Repozytorium zawiera implementację inteligentnego systemu RAG (Retrieval-Augmented Generation), który łączy klasyczne i semantyczne metody NLP z ekstrakcją encji nazwanych (NER) oraz informacji czasowych.

Główny kod z funkcjami znajduje się w folderze `core`, pozostałe foldery to testy/eksperymenty i dane.

---

 Dane

Projekt wykorzystuje korpus tekstowy w formacie JSONL:

```json
{
  "id": "123",
  "text": "Praca z ludźmi wymaga zaufania i jasnej komunikacji...",
  "domain": "interia.pl",
  "date": "2022-11-10"
}
```

Założenia:

* spójne `id` we wszystkich indeksach,
* embeddingi generowane modelem `intfloat/multilingual-e5-small`.

---

## Metody wyszukiwania

System obsługuje:

* **RegExp** – szybkie filtrowanie słów kluczowych,
* **BM25 (ElasticSearch)** – wyszukiwanie leksykalne,
* **Vector Search (ES + Qdrant)** – podobieństwo semantyczne,
* **Hybrid Search (RRF)**:

```
score = (1 / rank_es) + (1 / rank_qdrant)
```

Takie podejście uniezależnia ranking od skali score’ów.

---

## RAG – architektura

Pipeline RAG obejmuje:

1. analizę zapytania (intencja, czas),
2. ekstrakcję encji i dat,
3. hybrydowy retrieval z filtrami,
4. chunking i selekcję kontekstu,
5. generację odpowiedzi (LLM),
6. warstwę weryfikacji:

   * cytaty,
   * spójność czasowa,
   * encje,
7. zapis nierozwiązanych zapytań do pamięci.

---

## Wymagania

* Python 3.10+
* ElasticSearch 8.x
* Qdrant
* Ollama (model: `gemma2:2b`)

Instalacja zależności:

```bash
pip install -r requirements.txt
```

---

## Uruchomienie (skrót)

1. Reindeksacja:

```bash
python indexing/reindex_es.py
python indexing/reindex_qdrant.py
```

2. Benchmark:

```bash
python experiments/build_final_benchmark.py
```

3. Ewaluacja RAG:

```bash
python experiments/quality_loop.py
```

