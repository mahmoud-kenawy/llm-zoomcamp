import asyncio
import hashlib
import json
import os
from typing import List, Dict, Optional
from .config import config
from .chess_api import ChessComClient
from .embeddings import GeminiEmbeddings
from .qdrant_client import QdrantManager, doc_key
from .fetchers import (
    player_profile,
    player_stats,
    streamers,
    leaderboards,
    public_sources,
)

HASH_FILE = os.path.join(os.path.dirname(__file__), ".ingest_hashes.json")


def _load_hashes() -> Dict[str, str]:
    try:
        with open(HASH_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_hashes(hashes: Dict[str, str]):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f)


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class ChessIngestionPipeline:
    def __init__(self):
        self.embeddings = GeminiEmbeddings(config.GEMINI_API_KEY)
        self.qdrant = QdrantManager(
            config.QDRANT_URL,
            config.QDRANT_API_KEY,
            config.QDRANT_COLLECTION,
        )

    async def ingest_player_data(self, usernames: List[str]):
        all_docs: List[Dict] = []
        async with ChessComClient() as client:
            for username in usernames:
                try:
                    profile = await player_profile.fetch_player_profile(client, username)
                    stats = await player_stats.fetch_player_stats(client, username)
                    all_docs.extend([profile, stats])
                    print(f"  Fetched: {username}")
                except Exception as e:
                    print(f"  Failed {username}: {e}")
        await self._embed_and_store(all_docs)

    async def ingest_streamers(self):
        async with ChessComClient() as client:
            docs = await streamers.fetch_streamers(client)
        print(f"  Fetched {len(docs)} streamers")
        await self._embed_and_store(docs)

    async def ingest_leaderboards(self):
        async with ChessComClient() as client:
            docs = await leaderboards.fetch_leaderboards(client)
        print(f"  Fetched {len(docs)} leaderboard entries")
        await self._embed_and_store(docs)

    async def ingest_public_knowledge(self):
        docs: List[Dict] = []
        docs.extend(public_sources.get_chess_openings())
        docs.extend(public_sources.get_chess_concepts())
        docs.extend(public_sources.get_famous_games())
        docs.extend(public_sources.get_world_champions())
        print(f"  Curated docs: {len(docs)}")
        await self._embed_and_store(docs)

    def _filter_changed(self, documents: List[Dict]) -> List[Dict]:
        """Return only docs whose content changed since last ingest."""
        known = _load_hashes()
        changed = []
        for doc in documents:
            key = doc_key(doc)
            h = content_hash(doc["content"])
            if known.get(key) != h:
                doc["content_hash"] = h
                changed.append(doc)
        print(f"  Changed: {len(changed)}/{len(documents)} (skipping {len(documents) - len(changed)} unchanged)")
        return changed

    def _mark_ingested(self, documents: List[Dict]):
        known = _load_hashes()
        for doc in documents:
            known[doc_key(doc)] = doc.get("content_hash") or content_hash(doc["content"])
        _save_hashes(known)

    async def _embed_and_store(self, documents: List[Dict], batch_size: int = 25):
        documents = self._filter_changed(documents)
        if not documents:
            return
        texts = [doc["content"] for doc in documents]
        done: List[Dict] = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_docs = documents[i:i + batch_size]
            embs = self.embeddings.embed_documents(batch_texts)
            self.qdrant.upsert_documents(batch_docs, embs)
            done.extend(batch_docs)
            print(f"  Ingested batch: {len(batch_docs)} docs")
            if i + batch_size < len(texts):
                await asyncio.sleep(4)
        self._mark_ingested(done)

    async def run_full_ingestion(self, usernames: Optional[List[str]] = None):
        print("Starting chess data ingestion...")
        print("[1/3] Public knowledge...")
        await self.ingest_public_knowledge()
        print("[2/3] Streamers + leaderboards...")
        await self.ingest_streamers()
        await self.ingest_leaderboards()
        if usernames:
            print(f"[3/3] Players: {usernames}...")
            await self.ingest_player_data(usernames)
        print("Ingestion complete!")
