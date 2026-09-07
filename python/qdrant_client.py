from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
import uuid


def doc_key(doc: Dict) -> str:
    dtype = doc.get("type", "unknown")
    meta = doc.get("metadata", {}) or {}
    if dtype == "leaderboard":
        return f"leaderboard:{meta.get('category')}:{doc.get('username')}"
    if dtype in ("player_profile", "player_stats", "streamer"):
        return f"{dtype}:{doc.get('username')}"
    return f"{dtype}:{doc.get('name') or doc.get('username') or doc.get('category')}"


class QdrantManager:
    def __init__(self, url: str, api_key: str, collection_name: str, vector_size: int = 3072):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )
            print(f"Created collection: {self.collection_name}")

    def upsert_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        if not documents or not embeddings:
            return
        points = [
            PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"chess-llm:{doc_key(doc)}")),
                vector=emb,
                payload=doc
            )
            for doc, emb in zip(documents, embeddings)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector: List[float], limit: int = 10, filter_: Optional[Filter] = None) -> List[Dict]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter_
        )
        return [{"score": r.score, "payload": r.payload} for r in results]

    def delete_by_filter(self, filter_: Filter):
        self.client.delete(collection_name=self.collection_name, points_selector=filter_)