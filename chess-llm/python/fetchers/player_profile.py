from typing import Dict, Any
from ..chess_api import ChessComClient


async def fetch_player_profile(client: ChessComClient, username: str) -> Dict[str, Any]:
    raw = await client.get_player_profile(username.lower())

    content = f"""
Chess.com Player Profile: {raw.get('username', username)}
Name: {raw.get('name', 'N/A')}
Status: {raw.get('status', 'N/A')}
Followers: {raw.get('followers', 0)}
Country: {raw.get('country', 'N/A').split('/')[-1] if raw.get('country') else 'N/A'}
Joined: {raw.get('joined', 'N/A')}
Last Online: {raw.get('last_online', 'N/A')}
Streamer: {raw.get('is_streamer', False)}
Verified: {raw.get('verified', False)}
League: {raw.get('league', 'N/A')}
""".strip()

    return {
        "type": "player_profile",
        "username": username.lower(),
        "content": content,
        "metadata": {
            "username": username.lower(),
            "name": raw.get('name'),
            "country": raw.get('country'),
            "followers": raw.get('followers'),
            "is_streamer": raw.get('is_streamer'),
            "league": raw.get('league'),
            "status": raw.get('status'),
            "joined": raw.get('joined'),
            "last_online": raw.get('last_online'),
            "verified": raw.get('verified'),
            "source": "chess.com/api/player",
            "url": f"https://api.chess.com/pub/player/{username}"
        }
    }