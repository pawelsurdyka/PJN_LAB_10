import re
import spacy
from core.llm import ollama_generate

nlp = spacy.load("pl_core_news_lg")

# =========================
# REGEXY – POLSKIE FORMATY
# =========================

YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
ISO_DATE_RE = re.compile(r"\b(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")
PL_DATE_RE = re.compile(r"\b(0?[1-9]|[12]\d|3[01])[.\-/](0?[1-9]|1[0-2])[.\-/](19\d{2}|20\d{2})\b")
YEAR_PHRASE_RE = re.compile(r"\bw\s+(19\d{2}|20\d{2})\s+roku\b", re.IGNORECASE)
RANGE_RE = re.compile(r"\bod\s+(19\d{2})\s+do\s+(20\d{2}|19\d{2})\b", re.IGNORECASE)

# =========================
# REGEXP
# =========================

def extract_dates_regex(text: str) -> dict:
    years = set()
    dates = set()
    ranges = set()

    for y in YEAR_RE.findall(text):
        years.add(int(y))

    for y, m, d in ISO_DATE_RE.findall(text):
        dates.add(f"{y}-{m}-{d}")
        years.add(int(y))

    for d, m, y in PL_DATE_RE.findall(text):
        dates.add(f"{y}-{int(m):02d}-{int(d):02d}")
        years.add(int(y))

    for y in YEAR_PHRASE_RE.findall(text):
        years.add(int(y))

    for start, end in RANGE_RE.findall(text):
        ranges.add(f"od {start} do {end}")
        years.update(range(int(start), int(end) + 1))

    return {
        "years": sorted(years),
        "dates": sorted(dates),
        "ranges": sorted(ranges)
    }

# =========================
# SPACY (NER → DATE)
# =========================

def extract_dates_spacy(text: str) -> dict:
    doc = nlp(text)

    years = set()
    dates = set()

    for ent in doc.ents:
        if ent.label_ == "date":
            found_years = YEAR_RE.findall(ent.text)
            for y in found_years:
                years.add(int(y))

    return {
        "years": sorted(years),
        "dates": sorted(dates),
        "ranges": []
    }

# =========================
# LLM – FALLBACK
# =========================

def extract_dates_llm(text: str) -> dict:
    prompt = f"""
Wyodrębnij z poniższego tekstu wszystkie daty i zakresy czasowe.

Zwróć wyłącznie JSON w formacie:
{{
  "years": [2020, 2021],
  "dates": ["YYYY-MM-DD"],
  "ranges": ["od YYYY do YYYY"]
}}

TEKST:
{text}
"""
    try:
        response = ollama_generate(prompt)
        return eval(response) if response.strip().startswith("{") else {}
    except Exception:
        return {}

# =========================
# HYBRYDA – FINALNA FUNKCJA
# =========================

def extract_dates(text: str) -> dict:
    regex_res = extract_dates_regex(text)
    spacy_res = extract_dates_spacy(text)

    years = set(regex_res["years"]) | set(spacy_res["years"])
    dates = set(regex_res["dates"])
    ranges = set(regex_res["ranges"])

    # fallback LLM tylko jeśli słabo
    if not years and not dates:
        llm_res = extract_dates_llm(text)
        years.update(llm_res.get("years", []))
        dates.update(llm_res.get("dates", []))
        ranges.update(llm_res.get("ranges", []))

    return {
        "years": sorted(years),
        "dates": sorted(dates),
        "ranges": sorted(ranges)
    }
