import json

def load_jsonl(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def normalize_text(text: str) -> str:
    return text.lower().strip()
