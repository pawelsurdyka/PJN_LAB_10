import requests
from config import OLLAMA_URL, OLLAMA_MODEL
from typing import List, Dict

def ollama_generate(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.2
) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }

    if system:
        payload["system"] = system

    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    return r.json()["response"]

def generate_answer(
    question: str,
    contexts: List[Dict],
    temperature: float = 0.2
) -> str:
    """
    Prosty RAG: kontekst + pytanie → odpowiedź
    """

    context_text = "\n\n".join(
        f"[DOC {i+1}]\n{ctx['text']}"
        for i, ctx in enumerate(contexts)
    )

    prompt = f"""
Na podstawie poniższych fragmentów tekstu odpowiedz na pytanie.
Odpowiedź MUSI być oparta wyłącznie na podanych fragmentach.
Jeżeli brakuje informacji napisz, BRAK DANYCH. 
Jeżeli fragmenty tekstu są lekko powiązane z pytaniem lub tylko zachaczają o ten temat to mimo to odpowiedz na ich bazie.


FRAGMENTY:
{context_text}

PYTANIE:
{question}
"""

    return ollama_generate(
        prompt=prompt,
        temperature=temperature
    )
