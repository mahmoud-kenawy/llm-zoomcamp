import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION_NAME", "chess-llm")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    CACHE_TTL_STREAMERS = 300
    CACHE_TTL_LEADERBOARDS = 30
    CACHE_TTL_PLAYER_PROFILE = 86400
    CACHE_TTL_PLAYER_STATS = 86400

    CHESS_COM_BASE = "https://api.chess.com/pub"
    REQUEST_DELAY = 0.1

    DEFAULT_PLAYERS = [
        "hikaru",
        "magnuscarlsen",
        "fabianocaruana",
        "alirezafirouzja",
        "dingliren",
        "iannepomniachtchi",
        "wesleyso",
        "anishgiri",
    ]


config = Config()