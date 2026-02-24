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


def get_relevant_chunks(query: str, chunks: list[str], max_chars: int = 20000) -> str:
    """
    Score chunks by keyword overlap with the query and return the most relevant ones.
    """

    STOPWORDS = {"is", "the", "it", "and", "of", "to", "a"}

    query_words = {
        word.strip(".,!?")
        for word in query.lower().split()
        if word.strip(".,!?") not in STOPWORDS
    }

    scored = []
    for chunk in chunks:
        chunk_words = {
            word.strip(".,!?")
            for word in chunk.lower().split()
        }
        score = len(query_words & chunk_words)  # number of shared words
        if score > 0:
            scored.append((score, chunk))

    # sort by score, descending
    scored.sort(key=lambda x: x[0], reverse=True)

    selected = []
    total_chars = 0

    for score, chunk in scored:
        if total_chars + len(chunk) > max_chars:
            break
        selected.append(chunk)
        total_chars += len(chunk)

    return "\n\n---\n\n".join(selected)
