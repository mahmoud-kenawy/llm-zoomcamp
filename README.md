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

## Dependencies

### 1. Software you must install

| Software | Version | Check with | Install |
|----------|---------|------------|---------|
| Node.js + npm | 18+ | `node --version` | https://nodejs.org/ |
| Python | 3.12+ | `python3 --version` | https://www.python.org/ |
| uv (Python package manager) | any | `uv --version` | https://docs.astral.sh/uv/ (or use `pip` instead) |
| Git | any | `git --version` | https://git-scm.com/ |

### 2. Free accounts & API keys

| Service | Used for | Where to get it | Env vars |
|---------|----------|-----------------|----------|
| Google AI Studio (Gemini) | Chat (`gemini-3.5-flash-lite`) + embeddings (`gemini-embedding-001`) | https://aistudio.google.com/ | `GEMINI_API_KEY` |
| Qdrant Cloud | Vector database (`chess-llm` collection, 3072-dim, Cosine) | https://cloud.qdrant.io/ | `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME` |
| LangSmith (optional) | Tracing/debugging | https://smith.langchain.com/ | `LANGSMITH_*` (see `chess-llm/server/.env.example`) |
| Chess.com API | Player/streamer/leaderboard data — **no key needed**, public | — | — |

### 3. Project packages (installed automatically)

**Node.js** (`npm install --legacy-peer-deps` in `chess-llm/server` and `chess-llm/client`):
`langchain`, `@langchain/core`, `@langchain/langgraph`, `@langchain/google-genai`,
`@langchain/qdrant`, `@qdrant/js-client-rest`, `express`, `cors`, `dotenv`, `zod`,
`multer`, `pdf-parse`, `react`, `react-dom`, `react-markdown`, `vite`

**Python** (`uv sync` or `pip install -r requirements.txt` at repo root):
`google-genai`, `langchain-google-genai`, `langchain-qdrant`, `qdrant-client`,
`aiohttp`, `apscheduler`, `beautifulsoup4`, `python-dotenv`, `requests`

## How to run this project

### Step 0 — Environment file

Create a `.env` file at the repo root (it is gitignored; both Python and Node read it —
`chess-llm/server/.env` is a symlink to it):

```env
QDRANT_URL=https://xyz.us-east-1-1.aws.cloud.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
QDRANT_COLLECTION_NAME=chess-llm
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Step 1 — Install everything

```bash
# Web app deps
cd chess-llm/server && npm install --legacy-peer-deps
cd ../client && npm install --legacy-peer-deps

# Python deps
cd /workspaces/llm-zoomcamp && uv sync   # or: pip install -r requirements.txt
```

### Step 2 — Load chess data into Qdrant (one time)

```bash
cd /workspaces/llm-zoomcamp
python -m python.main --ingest --usernames hikaru magnuscarlsen
```

This embeds 91 curated docs (openings, concepts, famous games, champions) plus live
Chess.com data, then upserts them into the `chess-llm` collection.
Note: free-tier embedding quota is 1000 calls/day — the pipeline batches, throttles,
and skips unchanged docs automatically.

### Step 3 — Start background updates (optional, keeps data fresh)

```bash
cd /workspaces/llm-zoomcamp
python -m python.main --scheduler &
```

Runs forever: streamers every 30 min, leaderboards every 2 h, top players daily at 3 AM.

### Step 4 — Start the chat app

```bash
cd chess-llm && npm run dev
```

| Service | URL |
|---------|-----|
| App (frontend) | http://localhost:5173 |
| API (backend) | http://localhost:3001 |

Or start each side separately in its own terminal:

```bash
# Terminal 1 — backend
cd chess-llm/server && node index.js

# Terminal 2 — frontend
cd chess-llm/client && npm run dev
```

### Step 5 — Try it

Try: *"Hikaru's blitz rating?"* · *"Who is streaming right now?"* · *"Explain the Sicilian Defense"* · *"Bullet leaderboard"*

### Step 6 — Stop everything

```bash
# Kill backend + frontend (adjust PIDs from ps output if needed)
pkill -f "node index.js"; pkill -f vite

# Stop the Python scheduler (if started with &)
pkill -f "python.main --scheduler"
```

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
