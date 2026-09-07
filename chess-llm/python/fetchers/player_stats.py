from typing import Dict, Any
from ..chess_api import ChessComClient


async def fetch_player_stats(client: ChessComClient, username: str) -> Dict[str, Any]:
    raw = await client.get_player_stats(username.lower())

    time_controls = [
        "chess_rapid", "chess_blitz", "chess_bullet", "chess_daily",
        "chess960_rapid", "chess960_blitz", "chess960_bullet", "chess960_daily",
        "fide", "tactics", "lessons", "puzzle_rush"
    ]

    content_parts = [f"Chess.com Player Stats: {username}"]
    metadata = {"username": username.lower(), "time_controls": {}}

    for tc in time_controls:
        if tc in raw:
            stats = raw[tc]
            last = stats.get("last", {})
            best = stats.get("best", {})
            record = stats.get("record", {})

            content_parts.append(f"""
{tc.replace('_', ' ').title()}:
Current Rating: {last.get('rating', 'N/A')}
Best Rating: {best.get('rating', 'N/A')} (achieved {best.get('date', 'N/A')})
Record: W{record.get('win', 0)} L{record.get('loss', 0)} D{record.get('draw', 0)}
""".strip())

            metadata["time_controls"][tc] = {
                "current_rating": last.get('rating'),
                "best_rating": best.get('rating'),
                "best_date": best.get('date'),
                "wins": record.get('win'),
                "losses": record.get('loss'),
                "draws": record.get('draw')
            }

    return {
        "type": "player_stats",
        "username": username.lower(),
        "content": "\n\n".join(content_parts).strip(),
        "metadata": metadata
    }