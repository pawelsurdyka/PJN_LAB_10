import numpy as np
from config import embedder

def embed_text(text: str, prefix: str = "passage") -> np.ndarray:
    return embedder.encode(
        f"{prefix}: {text}",
        normalize_embeddings=True
    )

def embed_batch(texts: list[str], prefix: str = "passage") -> np.ndarray:
    return embedder.encode(
        [f"{prefix}: {t}" for t in texts],
        normalize_embeddings=True,
        show_progress_bar=True
    )
