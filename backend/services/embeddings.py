import logging

from openai import OpenAI

from config import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL, LLM_API_KEY, LLM_BASE_URL

logger = logging.getLogger("embeddings")

_client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


def embed_text(text: str) -> list[float]:
    """SumoPod gemini-embedding-001, truncated to EMBEDDING_DIMENSIONS (Matryoshka)."""
    response = _client.embeddings.create(model=EMBEDDING_MODEL, input=text, dimensions=EMBEDDING_DIMENSIONS)
    return response.data[0].embedding
