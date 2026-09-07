# Chess LLM — Web App

This folder holds the web app (Express backend + React frontend) for **Chess LLM**, a chess-focused RAG assistant.

> **Full documentation lives in the [root README](../README.md)** — setup, usage, architecture, and limitations.

## Quick start

```bash
# Backend :3001 + frontend :5173
npm run dev

# Install first (if needed)
npm run install:all
```

## Layout

- `server/` — Express + LangGraph agent (Gemini) with Qdrant RAG search and live Chess.com tools
- `client/` — React + Vite chat UI
- `server/.env.example` — required env vars (copy values into the repo-root `.env`)
