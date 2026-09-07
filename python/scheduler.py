import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import config
from .chess_ingest import ChessIngestionPipeline


class ChessDataScheduler:
    def __init__(self):
        self.pipeline = ChessIngestionPipeline()
        self.scheduler = AsyncIOScheduler()

    def start(self):
        self.scheduler.add_job(
            self.pipeline.ingest_streamers,
            "interval",
            minutes=30,
            id="streamers_update",
            replace_existing=True,
        )
        self.scheduler.add_job(
            self.pipeline.ingest_leaderboards,
            "interval",
            hours=2,
            id="leaderboards_update",
            replace_existing=True,
        )
        self.scheduler.add_job(
            lambda: self.pipeline.ingest_player_data(config.DEFAULT_PLAYERS),
            "cron",
            hour=3,
            minute=0,
            id="player_daily_update",
            replace_existing=True,
        )
        self.scheduler.start()
        print("Scheduler started: streamers(30m), leaderboards(2h), players(daily 3AM)")

    def stop(self):
        self.scheduler.shutdown()
