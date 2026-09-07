# ♟️ Chess LLM

A chess-focused RAG assistant. Chat about players, openings, ratings, live streamers, and leaderboards — powered by **Gemini**, **Qdrant**, and live **Chess.com** data.

![Chess LLM logo](chess-llm/client/public/logo.png)

## Architecture

Hybrid design — each runtime does what it's best at:

```
┌──────────────┐   periodic writes    ┌─────────────────┐
│  PYTHON      │ ──────────────────▶  │  QDRANT CLOUD   │
│  scheduler   │  streamers · 30 min  │  chess-llm      │
│              │  leaderboards · 2 h  │  3072-dim       │
│              │  players · daily     │  Cosine         │
└──────────────┘                      └────────┬────────┘
                                               │ read (RAG)
┌──────────────┐   live Chess.com     ┌────────▼────────┐
│  REACT       │ ◀──────────────────  │  NODE.JS        │
│  chat UI     │      HTTP /api       │  Express agent  │
│  :5173       │                      │  Gemini + tools │
└──────────────┘                      │  :3001          │
                                      └─────────────────┘
```

- **Python** (`python/`): periodic bulk ingestion into Qdrant (APScheduler). Embeddings via `gemini-embedding-001`.
- **Node.js** (`chess-llm/server/`): Express + LangGraph agent (`gemini-3.5-flash-lite`) with 5 tools — knowledge search + 4 live Chess.com tools (profile, stats, streamers, leaderboards). Vector search via Qdrant.
- **React** (`chess-llm/client/`): chat UI with pawn-green/black theme, light/dark toggle, suggestion chips. PDF uploader removed on purpose (ingestion is Python-owned).

## Repo layout

```
.
├── chess-llm/                 # web app (renamed from agentic-personal-assistant)
│   ├── server/                # Express + LangChain agent
│   │   ├── agent.js           # Gemini agent, chess system prompt
│   │   ├── tools.js           # Qdrant RAG search tool
│   │   ├── ingest.js          # (legacy) PDF ingestion endpoint
│   │   ├── data/
│   │   │   ├── chess-api.js   # live Chess.com client + TTL cache
│   │   │   ├── chess-tools.js # agent tools (profile/stats/streamers/boards)
│   │   │   └── cache.js       # in-memory TTL cache (Redis-ready)
│   │   └── .env -> ../../.env # symlink: single source of truth
│   ├── client/                # React + Vite chat UI
│   │   └── public/logo.png    # pawn logo (favicon, header, avatars)
│   └── package.json           # npm run dev → server + client
├── python/                    # data pipeline (ingestion + scheduler)
│   ├── config.py              # env config, TTLs, default players
│   ├── chess_api.py           # async Chess.com client (ETag cache)
│   ├── embeddings.py          # Gemini embeddings + 429 retry/backoff
│   ├── qdrant_client.py       # Qdrant ops, deterministic UUID5 point IDs
│   ├── fetchers/              # player_profile, player_stats, streamers,
│   │                          # leaderboards (top 10/category), public_sources
│   │                          # (34 openings, 31 concepts, 8 games, 18 champions)
│   ├── chess_ingest.py        # pipeline + SHA-256 change detection
│   ├── scheduler.py           # periodic jobs
│   └── main.py                # CLI: --ingest | --scheduler [--usernames ...]
├── src/llm_zoomcamp/          # original course project (untouched)
├── test.ipynb                 # Gemini SDK smoke test (untouched)
├── image.png                  # logo source
├── CHESS_LLM_IMPLEMENTATION_PLAN.md
└── .env                       # YOUR keys (gitignored, never commit)
```

## Prerequisites

- Node.js 18+ and npm
- Python 3.12+ with `uv` (or pip)
- A Gemini API key ([Google AI Studio](https://aistudio.google.com/)) — new keys serve 3.x models
- A Qdrant Cloud cluster (or self-hosted) with an empty `chess-llm` collection

## Setup

```bash
# 1. Environment — copy and fill (root .env is shared by Python + Node)
# Required: QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME=chess-llm,
#           GEMINI_API_KEY, (optional LangSmith vars, see server/.env.example)

# 2. Web app deps
cd chess-llm/server && npm install --legacy-peer-deps
cd ../client && npm install --legacy-peer-deps

# 3. Python deps
cd /workspaces/llm-zoomcamp && uv sync   # or: pip install -r requirements.txt
```

## Usage

```bash
# 1. Bulk ingest chess knowledge into Qdrant (curated + Chess.com data)
python -m python.main --ingest --usernames hikaru magnuscarlsen

# 2. Continuous background updates (streamers 30m, leaderboards 2h, players daily)
python -m python.main --scheduler &

# 3. Chat app (server :3001 + client :5173)
cd chess-llm && npm run dev
```

Try: *"Hikaru's blitz rating?"* · *"Who is streaming right now?"* · *"Explain the Sicilian Defense"* · *"Bullet leaderboard"*

## How the agent handles usernames

Usernames are auto-extracted from messages (`@hikaru`, `player Nakamura`, bare names). If a player question has no identifiable username, the agent asks for it instead of guessing.

## Limitations

1. **Gemini free-tier embedding quota (1000 calls/day).** Bulk ingestion consumes it fast; the pipeline mitigates with small batches (25), 4s pauses, exponential-backoff retries, top-10 trims (streamers, leaderboards), and SHA-256 change detection (unchanged docs embed zero calls). When quota is exhausted, ingestion/scheduler stall until UTC reset — chat keeps working on cached + live data.
2. **Chat model availability is key-dependent.** New API keys serve 3.x models only (`gemini-3.5-flash-lite` is the default; override via `GEMINI_CHAT_MODEL`). Older names like `gemini-1.5-flash` 404 on such keys.
3. **Vector dimension is fixed at 3072** (`gemini-embedding-001` default). The `chess-llm` collection must be created with 3072-dim Cosine vectors — a mismatched collection causes upsert errors.
4. **Scheduler re-ingests snapshots.** Deterministic UUID5 point IDs make upserts overwrite, and change detection skips unchanged docs — but a content change (e.g. rank shift) rewrites that doc. Stale docs for delisted streamers are not pruned.
5. **Chess.com API has no auth but expects polite use.** The clients add 100ms delays and ETag support (leaderboards); abusive polling risks IP throttling.
6. **In-memory caches only.** Both Python (`chess_api.py`) and Node (`data/cache.js`) cache in-process — restarts drop them. Swap `cache.js` for Redis when needed (interface-compatible).
7. **Bare single-word names are untested.** Questions containing a name work reliably; a lone `"hikaru"` with no question words should trigger a profile lookup per the system prompt but wasn't explicitly verified.
8. **Player data is cached 24h.** Profile/stats are cached a full day — intra-day rating changes won't show until expiry.
9. **Curated knowledge is static.** Openings/concepts/games/champions are hand-curated snapshots, not live data — verify critical lines against current theory.
