# ♟️ Chess LLM

<p align="center">
  <img src="chess-llm/client/public/logo.png" alt="Chess LLM logo" width="180">
</p>

Chat about chess players, openings, ratings, live streamers, and leaderboards.
Powered by **Gemini**, **Qdrant**, and live **Chess.com** data.

## What you need

- **Node.js 18+** + npm — `node --version`
- **Python 3.12+** — `python3 --version` (plus `uv`, or use `pip`)
- **Gemini API key** (free) — https://aistudio.google.com/
- **Qdrant** Cloud cluster (free tier works) — https://cloud.qdrant.io/ — with a `chess-llm` collection
- Chess.com API needs **no key** (public)

## Setup

**1. Create `.env`** at the repo root:

```env
QDRANT_URL=https://xyz.us-east-1-1.aws.cloud.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
QDRANT_COLLECTION_NAME=chess-llm
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Then link it into the server (the server reads `.env` from its own folder):

```bash
ln -s ../../.env chess-llm/server/.env
```

**2. Install dependencies:**

```bash
cd chess-llm/server && npm install --legacy-peer-deps
cd ../client && npm install --legacy-peer-deps
cd ../.. && uv sync   # or: pip install -r requirements.txt
```

## Run

**3. Load chess data into Qdrant** (one time, ~11 embedding calls):

```bash
cd chess-llm && python -m python.main --ingest --usernames hikaru magnuscarlsen
```

**4. Start the app:**

```bash
cd chess-llm && npm run dev
```

Open **http://localhost:5173** — backend runs on :3001.

**5. (Optional) Keep data fresh** — background scheduler (streamers 30m, leaderboards 2h, players daily):

```bash
cd chess-llm && python -m python.main --scheduler &
```

**6. Stop everything:**

```bash
pkill -f "node index.js"; pkill -f vite; pkill -f "python.main --scheduler"
```

Try: *"Hikaru's blitz rating?"* · *"Who is streaming right now?"* · *"Explain the Sicilian Defense"*

Usernames are auto-detected (`@hikaru`, `player Nakamura`, bare names). If your question
names no player, the assistant asks for one.

**How data stays fresh:** ingestion (step 3) and the scheduler (step 5) are the only things
that write vectors to Qdrant — nothing auto-ingests on app start (this protects your
embedding quota). But every answer about players, streamers, or leaderboards is fetched
live from Chess.com at question time, so those are always current.

## Limits to know

- **Embedding quota:** Gemini free tier allows 1000 embedding calls/day. The pipeline batches,
  throttles, trims (top-10 streamers/leaderboards), and skips unchanged docs — but a big
  first ingest can still exhaust it until UTC reset. Chat keeps working on cached + live data.
- **Chat model depends on your key:** new keys serve 3.x models only (`gemini-3.5-flash-lite`
  is default; override with `GEMINI_CHAT_MODEL`).
- **Qdrant collection must be 3072-dim Cosine** to match `gemini-embedding-001`.
- **Player stats cache 24h** — intra-day rating changes appear after expiry.
- **Curated knowledge is static** (openings, concepts, famous games, champions) — verify
  critical lines against current theory.
- Chess.com data is fetched politely (delays + ETag); don't hammer it.
