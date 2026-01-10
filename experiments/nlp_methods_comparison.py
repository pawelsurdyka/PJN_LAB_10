import re
from pprint import pprint

from core.retrieval import retrieve_documents
from core.utils import load_jsonl

# =============================
# KONFIGURACJA EKSPERYMENTU
# =============================

QUERIES = [
    "odpowiedzialność zespołowa",
    "przywództwo i liderzy",
    "zaufanie i jego utrata"
]

REGEX_PATTERNS = {
    "odpowiedzialność zespołowa": r"odpowiedzialn|zesp[oó]ł|wspóln",
    "przywództwo i liderzy": r"lider|przyw[oó]dztw|zarz[aą]dz",
    "zaufanie i jego utrata": r"zaufan|nieufn|utrac|zdrad"
}

ENTITIES = [
    'AGO Esports', 'Damian ', 'Kisłowski', 'Mateusz', 'Zawistowski', 'Jacek', 'Jeziak', 'Maciej Luz', 'Bugaj', 'Paweł', 'Jańczak', 'Venatores', 'Krzysztof', 'Lewandrowski', 'Karol', 'Kapczyński', 'SEAL Esports', 'Piotr peet', 'Ćwikliński', 'Marcin', 'Krzemiński', 'Izako Boars', 'Piotr', 'Nawrocki', 'Kamil', 'kamil', 'Kamiński', 'Mateusz', 'Świętochowski', 'Ministerstwa Zdrowia', 'Jabłonka', 'Uniwersytet Medyczny', 'Spaarti', 'Waylandzie', 'Biuro Projektowe Archimedia', 'Poznania', 'Rady Miejskiej 17', 'Adama Rucińskiego', 'Szkoły Podstawowej na Winnej Górze', 'PREFABRYKAT', 'Karpacza', 'Gminy Kobierzyce', 'Skarbków', 'Izbicy Kujawskiej', 'Justyna Krzyżanowskiej', 'Skarbków', 'Żelazowej Woli', 'Mikołaja Chopina', 'Chopin', 'Pomorze', 'płockiego', 'Karola Zboińskiego', 'Kikół', 'Franciszek Ksawery', 'Zboińskim', 'Chopinem', 'Kowalewie', 'Pomorze', 'rajkibica.pl', 'Spotify', 'Tidal', 'Audioquest', 'SYSTEM FIDELITY CD', '| AUDIO 2', 'Muzeum Historii Polski', 'Szkocja', 'FOK', 'IPMS', 'Muzeum Historii Polski Żołnierz', 'Pułku Ułanów', 'Pułku Strzelców Konnych', 'Szkocja', 'FOK', 'IPMS', 'Samorządowe Przedszkole Nr 107', 'Biuletyn Informacji Publicznej Samorządowe Przedszkole Nr 107', 'Polsat Box', 'Polsat Box', 'Polsat Box', 'Polsat Box', 'Polsat Box', 'pl store', 'Andrzej Ostrowski', 'twardsi', 'Mateusz Greloch', 'Tom Clancy', 'amerykański', 'Tom', 'Jankowice', 'gmina Srokowo', 'Warmii', 'Mazur Jankowice', 'gmina Srokowo', 'Konrad', 'Jankowice', 'województwie warmińsko-mazurskim', 'powiecie kętrzyńskim', 'gminie Srokowo', 'województwa olsztyńskiego', 'Niedziałami', 'Jankowice', 'Koronawirusa', 'Olsztyna', 'powiatu olsztyńskiego', 'koronawirusa', 'powiatach iławskim', 'ostródzkim', 'Olsztynie', 'powiecie olsztyńskim', 'Śląska', 'polskie', 'Austrią', 'Polski', 'Teresa Zielewicz-Lottspeich', 'polskiej', 'Danuta Załęska', 'Hypobanku', 'Gabriele Gebauer', 'Mileny Foltynovej', 'Polki', 'Teresa Zielewicz', 'Danuta Załęska', 'USA', 'WELL', 'Rozchylony', 'Derek M', 'BellyBoyBoy', 'Katy Perry', 'Orlando', 'Miranda Kerr', 'Miley Cyrus', 'Bloom', 'Bytomiu', 'Warszawa', 'francuskim', 'am', 'Polska', 'Piasecznie', 'Warszawą', 'Auchan', 'wykopywanego', 'sądeckiego', 'brytyjkie', 'Polskie', 'Polskie', 'SKOK', 'Polsce', 'SKOK', 'SKOK', 'Senat', 'chińskich', 'Mitomanka', 'Dorota', 'Tomasz Adamek', 'Tomasz Adamek', 'Tomasz Adamek', 'Kliczko', 'Włoszech', 'San Siro', 'Mediolanie', 'Hiszpanią', 'Europy', 'amerykańskiej', 'polsku', 'Queens Museum of Art | Muzea Nowego Jorku |', '| New York Online Flushing Meadows Corona Park Queens NY', 'Queens Museum of Art', 'Miasto Nowy Jork', 'New York City in', 'Wisły', 'Bugu', 'Wieprza', 'Tyśmienicy', 'Bystrzycy', 'Polskie', 'Julii', 'OBUW', 'Dorota Szubierajska', 'Alfred L', 'Tadeusz', 'Poznania', 'Województwa Poznańskiego', 'Kazimierz Bajon', 'Stanisław Fitas', 'Zygmunt Frąckowiak', 'Marian Ginter', 'Stanisław Gorlas', 'Stanisław Jaroch', 'Edmund Karaśkiewicz', 'Józef Kardzis', 'Władysław Kurasztkiewicz', 'Józef Lisowski', 'Henryk Łowmiański', 'Zygmunt N apierała', 'Zbigniew Panowicz', 'Grzegorz Parczuk', 'Stanisław Paszkowiak', 'Leon Rogaliński', '.65', 'Eugeniusz C o', 'Franciszek Hryniewicz', 'wielkopolskiej', 'Zbigniew N', 'Komisja Nadzoru Finansowego', 'Marii Gryczki', 'Restaurację Benitto', 'Andersena', 'Szkolnego Klubu Książki', 'Poleasingowe.pl', 'Henryka', 'Mariusza Nowoczesny', 'Poleasingowe.pl', 'Kayah', 'Kraków', 'Rynek Główny', 'Bazylikę Mariacką', 'Wawel', 'Hali Targowej', 'krakowskiego', 'Schindlera', 'polskich', 'Joe', 'Angela Scanlon', 'Krakowa', 'BOSiR-u', 'brzeską', 'Andrzej Lepper', 'Piotr Męcik', 'Piotr Kucia', 'Andrzej Lepper', 'Zielnowie', 'Jarosławem', 'Polska', 'Monika Mańkowska', 'Franiową', 'Katarzyna Kordella', 'stoiczek fisher price', 'Monika Mańkowska', 'Aniu', 'Microsoft', 'Microsoft', 'Spartana', 'Microsoft', 'Magdalena Pikul', 'Księżyca', 'Kampus ArcelorMittal University', 'Warszawy', 'Galop44', 'warszawskie', 'Niemiec', 'polskim', 'Holandii', 'szydłowieccy', 'Seroxat', 'Seroxat', 'Hurtownia Artnova PEN JEDNORAZOWY BEAUTY LINE', 'Olsztyn', 'Kalczyńska', 'Anna Kalczyńska', 'Anna', 'Interactive English School', 'Słoneczna', 'hiszpańskiego', 'Wasiołek', 'France', 'Toru Wyścigów Konnych', 'Marka Cichosza', 'Legii', 'Polski', 'Kolbuszowscy', 'Niwiskach', 'koronawirusa', 'Bach', 'MKOl', 'UEFA', 'Acer', 'angielski', 'Kaczor', 'katowice', 'prawniczejKancelaria', 'Katowice', 'Rotmanka', 'Rotmance', 'Trzyniec', 'Bogumin', 'Hażlach', 'Cieszyn', 'Czeski Cieszyn', 'Kocobędz', 'Karwinę', 'chińskim', 'Unigroup', 'Europy', 'brytyjskiego', 'CSR', 'Europie', 'Qualcomm', 'niemieckiego', 'Lantiq', 'europejskim', 'Intela', 'Europy', 'Milton H.', 'Greene', 'Marilyn Monroe', 'MGS5', 'Mgs5', 'głosów:0', 'Rockstar', 'Rybnik Samodzielne', 'krzesłaDobry', 'geodezjiPoradnik', 'ZEUX', 'Jana Pawła II', 'Zawoi', 'Anna Maciejewska', 'Centrum Myśli', 'Jana Pawła II',
]

K = 5
DATA_PATH = "data/culturax_pl_clean_small.jsonl"

FILTER_YEARS = [2018, 2019, 2020, 2021, 2022, 2023]

# =============================
# REGEXP SEARCH (BASELINE)
# =============================

def regex_search(query_key, docs, k=5):
    pattern = re.compile(REGEX_PATTERNS[query_key], re.IGNORECASE)
    results = []

    for d in docs:
        if pattern.search(d["text"]):
            results.append(d)

    return results[:k]

# =============================
# EKSPERYMENT
# =============================

def run_experiment():
    corpus = load_jsonl(DATA_PATH)

    for query in QUERIES:
        print("\n" + "=" * 100)
        print(f"POJĘCIE: {query}")
        print("=" * 100)

        # -------- REGEXP --------
        print("\n[REGEXP]")
        regex_results = regex_search(query, corpus, K)
        for r in regex_results:
            print("-", r["text"][:120])

        # -------- BM25 --------
        print("\n[BM25 – ElasticSearch]")
        bm25_results = retrieve_documents(
            query=query,
            method="bm25",
            k=K
        )
        for r in bm25_results:
            print("-", r["text"][:120])

        # -------- QDRANT --------
        print("\n[QDRANT – Semantic]")
        qdrant_results = retrieve_documents(
            query=query,
            method="qdrant",
            years=FILTER_YEARS,
            k=K,
            entities=ENTITIES
        )
        for r in qdrant_results:
            print("-", r["text"][:120])

        # -------- HYBRYDA --------
        print("\n[HYBRYDA – RRF]")
        hybrid_results = retrieve_documents(
            query=query,
            method="hybrid",
            years=FILTER_YEARS,
            k=K,
            entities=ENTITIES
        )
        for r in hybrid_results:
            print(f"- ({r['rrf_score']:.3f})", r["text"][:120])


if __name__ == "__main__":
    run_experiment()
