from src.cosine_similarity import cosine_similarity
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def embed_chunks(chunks: list[str]) -> list[np.ndarray]:
    """
    Batch embed chunks for efficiency.
    """
    embeddings = embedding_model.encode(chunks)
    return [np.array(e) for e in embeddings]


def get_query_embedding(query: str) -> np.ndarray:
    return np.array(embedding_model.encode(query))


def retrieve_relevant_chunks(query: str, chunks: list[str], chunk_embeddings: list[np.ndarray], max_chars: int = 20000):
    query_embedding = get_query_embedding(query)

    scores = []
    for i, emb in enumerate(chunk_embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    selected = []
    total_chars = 0

    for score, chunk in scores:
        if total_chars + len(chunk) > max_chars:
            break
        selected.append(chunk)
        total_chars += len(chunk)

    return "\n\n---\n\n".join(selected)
