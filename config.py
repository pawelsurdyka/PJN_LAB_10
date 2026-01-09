from sentence_transformers import SentenceTransformer

# ===== EMBEDDINGS =====
MODEL_NAME = "intfloat/multilingual-e5-small"
embedder = SentenceTransformer(MODEL_NAME)

# ===== ELASTICSEARCH =====
ES_URL = "http://localhost:9200"
# ES_INDEX = "culturax_es"
ES_INDEX = "culturax_es_rag"
HEADERS = {"Content-Type": "application/json"}

# ===== QDRANT =====
QDRANT_URL = "http://localhost:6333"
# QDRANT_COLLECTION = "culturax_qd"
QDRANT_COLLECTION = "culturax_qd_rag"

# ===== OLLAMA =====
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:2b"
