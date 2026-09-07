from typing import List, Dict, Any
from ..chess_api import ChessComClient

MAX_LIVE_STREAMERS = 10


async def fetch_streamers(client: ChessComClient) -> List[Dict[str, Any]]:
    raw = await client.get_streamers()
    documents = []

    live = [s for s in raw.get("streamers", []) if s.get("is_live")]

    for streamer in live[:MAX_LIVE_STREAMERS]:
        username = streamer.get("username", "").lower()
        platforms = streamer.get("platforms", []) or []
        live_platforms = ", ".join(
            f"{p.get('type')}: {p.get('stream_url')}"
            for p in platforms if p.get("is_live") and p.get("stream_url")
        ) or "N/A"
        content = f"""
Chess.com Live Streamer: {streamer.get('username')}
Is Live: True
Watch: {live_platforms}
Twitch: {streamer.get('twitch_url', 'N/A')}
Profile: {streamer.get('url', 'N/A')}
Community Streamer: {streamer.get('is_community_streamer', False)}
""".strip()

        documents.append({
            "type": "streamer",
            "username": username,
            "content": content,
            "metadata": {
                "username": username,
                "is_live": True,
                "twitch_url": streamer.get('twitch_url'),
                "url": streamer.get('url'),
                "is_community_streamer": streamer.get('is_community_streamer'),
                "source": "chess.com/api/streamers",
                "fetched_at": "auto-updated-every-5-min"
            }
        })

    return documents
