import asyncio
import aiohttp
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from .config import config


@dataclass
class CacheEntry:
    data: Any
    expires_at: float
    etag: Optional[str] = None


class ChessComClient:
    def __init__(self):
        self.cache: Dict[str, CacheEntry] = {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get(self, endpoint: str, cache_key: str, ttl: int, use_etag: bool = False) -> Any:
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() < entry.expires_at:
                return entry.data

        headers = {}
        if use_etag and cache_key in self.cache:
            headers["If-None-Match"] = self.cache[cache_key].etag

        url = f"{config.CHESS_COM_BASE}{endpoint}"
        async with self.session.get(url, headers=headers) as resp:
            if resp.status == 304:
                self.cache[cache_key].expires_at = time.time() + ttl
                return self.cache[cache_key].data

            if resp.status != 200:
                raise Exception(f"Chess.com API error: {resp.status} for {url}")

            data = await resp.json()
            etag = resp.headers.get("ETag")

            self.cache[cache_key] = CacheEntry(
                data=data,
                expires_at=time.time() + ttl,
                etag=etag
            )
            await asyncio.sleep(config.REQUEST_DELAY)
            return data

    async def get_player_profile(self, username: str) -> Dict:
        return await self._get(
            f"/player/{username.lower()}",
            f"profile:{username.lower()}",
            config.CACHE_TTL_PLAYER_PROFILE
        )

    async def get_player_stats(self, username: str) -> Dict:
        return await self._get(
            f"/player/{username.lower()}/stats",
            f"stats:{username.lower()}",
            config.CACHE_TTL_PLAYER_STATS
        )

    async def get_streamers(self) -> Dict:
        return await self._get(
            "/streamers",
            "streamers",
            config.CACHE_TTL_STREAMERS
        )

    async def get_leaderboards(self) -> Dict:
        return await self._get(
            "/leaderboards",
            "leaderboards",
            config.CACHE_TTL_LEADERBOARDS,
            use_etag=True
        )