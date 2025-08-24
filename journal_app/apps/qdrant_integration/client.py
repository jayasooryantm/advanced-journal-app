import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

hf_token = os.getenv("HF_TOKEN")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "journal_entries")

# Use a free model all-MiniLM-L6-v2
embedder = SentenceTransformer("all-MiniLM-L12-v2", token=hf_token)
qdrant_client = QdrantClient(url=QDRANT_URL)


def upsert_entry(entry_id, text):
    vector = embedder.encode(text).tolist()
    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[{
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {"text": text, "entry_id": entry_id}
        }]
    )


def search_entries(query, top_k=5):
    vector = embedder.encode(query).tolist()
    results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=vector,
        limit=top_k
    )
    return results


def delete_entry(entry_id):
    qdrant_client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector={
            "filter": {
                "must": [
                    {"key": "entry_id", "match": {"value": entry_id}}
                ]
            }
        }
    )


# Create collection if it doesn't exist
if not qdrant_client.collection_exists(QDRANT_COLLECTION):
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=384, distance=Distance.COSINE),  # 384 for MiniLM models
    )
