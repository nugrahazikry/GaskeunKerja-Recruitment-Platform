from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import EMBEDDING_DIMENSIONS, QDRANT_URL

CANDIDATE_VECTORS_COLLECTION = "candidate_vectors"
JD_VECTORS_COLLECTION = "jd_vectors"

client = QdrantClient(url=QDRANT_URL)


def create_collections() -> None:
    for name in (CANDIDATE_VECTORS_COLLECTION, JD_VECTORS_COLLECTION):
        if not client.collection_exists(name):
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
            )
