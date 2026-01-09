from core.llm import ollama_generate

def build_context(docs: list[dict], max_chars: int = 3000) -> str:
    context = ""
    for d in docs:
        text = d.get("text") or d.get("_source", {}).get("text", "")
        if len(context) + len(text) > max_chars:
            break
        context += text + "\n\n"
    return context

def rag_answer(question: str, context: str) -> str:
    prompt = f"""
Odpowiedz na pytanie wyłącznie na podstawie kontekstu.
Cytuj fragmenty tekstu.

KONTEKST:
{context}

PYTANIE:
{question}
"""
    return ollama_generate(prompt)
