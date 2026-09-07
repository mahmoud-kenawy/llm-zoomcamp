import asyncio
import argparse
from .chess_ingest import ChessIngestionPipeline
from .scheduler import ChessDataScheduler


async def run_ingestion(usernames=None):
    pipeline = ChessIngestionPipeline()
    await pipeline.run_full_ingestion(usernames=usernames)


async def run_scheduler():
    scheduler = ChessDataScheduler()
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        scheduler.stop()


def main():
    parser = argparse.ArgumentParser(description="Chess LLM Data Pipeline")
    parser.add_argument("--ingest", action="store_true", help="Run one-time ingestion")
    parser.add_argument("--scheduler", action="store_true", help="Run continuous scheduler")
    parser.add_argument("--usernames", nargs="+", help="Usernames to ingest")
    args = parser.parse_args()

    if args.ingest:
        asyncio.run(run_ingestion(args.usernames))
    elif args.scheduler:
        asyncio.run(run_scheduler())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
