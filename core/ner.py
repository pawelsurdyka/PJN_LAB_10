import spacy
from collections import defaultdict

# Ładujemy model tylko raz (ważne wydajnościowo)
nlp = spacy.load("pl_core_news_lg")

# Mapowanie etykiet spaCy → nasze kategorie
LABEL_MAP = {
    "persName": "persons",
    "orgName": "organizations",
    "placeName": "locations",
    "geogName": "locations",
    "facility": "locations"
}

def extract_entities(text: str) -> dict:
    """
    Zwraca encje nazwane z tekstu w ujednoliconym formacie.
    """
    # print(nlp.get_pipe("ner").labels)
    doc = nlp(text)

    entities = defaultdict(set)

    for ent in doc.ents:
        label = LABEL_MAP.get(ent.label_)
        if label:
            entities[label].add(ent.text)

    return {
        "persons": sorted(list(entities["persons"])),
        "organizations": sorted(list(entities["organizations"])),
        "locations": sorted(list(entities["locations"]))
    }
