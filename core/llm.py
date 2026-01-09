import requests
from config import OLLAMA_URL, OLLAMA_MODEL

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
