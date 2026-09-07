from typing import List, Dict, Any
from ..chess_api import ChessComClient


MAX_PER_CATEGORY = 10


async def fetch_leaderboards(client: ChessComClient) -> List[Dict[str, Any]]:
    raw = await client.get_leaderboards()
    documents = []

    for category, players in raw.items():
        if not isinstance(players, list):
            continue

        for i, player in enumerate(players[:MAX_PER_CATEGORY]):
            username = player.get("username", "").lower()
            content = f"""
Chess.com Leaderboard: {category.replace('_', ' ').title()}
Rank: {i + 1}
Player: {player.get('username')}
Rating: {player.get('score', 'N/A')}
""".strip()

            documents.append({
                "type": "leaderboard",
                "category": category,
                "rank": i + 1,
                "username": username,
                "content": content,
                "metadata": {
                    "category": category,
                    "rank": i + 1,
                    "username": username,
                    "rating": player.get('score'),
                    "source": "chess.com/api/leaderboards",
                    "fetched_at": "auto-updated-every-30-sec"
                }
            })

    return documents