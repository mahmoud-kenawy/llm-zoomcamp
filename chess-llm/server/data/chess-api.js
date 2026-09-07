import { cache } from "./cache.js";

const CHESS_COM_BASE = "https://api.chess.com/pub";
const REQUEST_DELAY_MS = 100;

const TTL = {
  profile: 24 * 60 * 60 * 1000, // 24 hours
  stats: 24 * 60 * 60 * 1000, // 24 hours
  streamers: 5 * 60 * 1000, // 5 minutes
  leaderboards: 30 * 1000, // 30 seconds
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Matches @username mentions or "player <name>" phrases.
const USERNAME_PATTERN = /(?:@|player\s+)([a-zA-Z0-9_-]{3,25})/gi;

const STOPWORDS = new Set([
  "the", "and", "for", "with", "from", "about", "chess", "game", "games",
  "play", "player", "profile", "stats", "rating", "stream", "streamers",
]);

export function extractUsernames(text) {
  if (!text) return [];
  const found = [];
  let match;
  USERNAME_PATTERN.lastIndex = 0;
  while ((match = USERNAME_PATTERN.exec(text)) !== null) {
    const candidate = match[1].toLowerCase();
    if (!STOPWORDS.has(candidate) && !found.includes(candidate)) {
      found.push(candidate);
    }
  }
  return found;
}

export function needsUsername(query) {
  const indicators = ["rating", "stats", "profile", "games", "opening", "style", "elo", "rank"];
  const lower = (query || "").toLowerCase();
  const hasIndicator = indicators.some((w) => lower.includes(w));
  return hasIndicator && extractUsernames(query).length === 0;
}

async function fetchJson(endpoint) {
  const res = await fetch(`${CHESS_COM_BASE}${endpoint}`, {
    headers: { "User-Agent": "chess-llm/1.0" },
  });
  if (res.status === 304) return null;
  if (!res.ok) {
    throw new Error(`Chess.com API error ${res.status} for ${endpoint}`);
  }
  const data = await res.json();
  await sleep(REQUEST_DELAY_MS);
  return data;
}

export async function getPlayerProfileLive(username) {
  const key = `profile:${username.toLowerCase()}`;
  const cached = cache.get(key);
  if (cached) return cached;
  const data = await fetchJson(`/player/${username.toLowerCase()}`);
  cache.set(key, data, TTL.profile);
  return data;
}

export async function getPlayerStatsLive(username) {
  const key = `stats:${username.toLowerCase()}`;
  const cached = cache.get(key);
  if (cached) return cached;
  const data = await fetchJson(`/player/${username.toLowerCase()}/stats`);
  cache.set(key, data, TTL.stats);
  return data;
}

export async function getStreamersLive() {
  const cached = cache.get("streamers");
  if (cached) return cached;
  const data = await fetchJson("/streamers");
  cache.set("streamers", data, TTL.streamers);
  return data;
}

export async function getLeaderboardsLive() {
  const cached = cache.get("leaderboards");
  if (cached) return cached;
  const data = await fetchJson("/leaderboards");
  cache.set("leaderboards", data, TTL.leaderboards);
  return data;
}

export function formatProfile(raw) {
  if (!raw) return "No profile data available.";
  const country = raw.country ? raw.country.split("/").pop() : "N/A";
  return [
    `Player: ${raw.username ?? "N/A"}`,
    `Name: ${raw.name ?? "N/A"}`,
    `Status: ${raw.status ?? "N/A"}`,
    `Followers: ${raw.followers ?? 0}`,
    `Country: ${country}`,
    `League: ${raw.league ?? "N/A"}`,
    `Streamer: ${raw.is_streamer ?? false}`,
    `Verified: ${raw.verified ?? false}`,
  ].join("\n");
}

export function formatStats(username, raw) {
  if (!raw) return `No stats available for ${username}.`;
  const lines = [`Stats for ${username}:`];
  for (const [tc, stats] of Object.entries(raw)) {
    if (!stats || typeof stats !== "object" || !stats.last) continue;
    const last = stats.last ?? {};
    const best = stats.best ?? {};
    const record = stats.record ?? {};
    lines.push(
      `${tc.replace(/_/g, " ")}: rating ${last.rating ?? "N/A"} ` +
        `(best ${best.rating ?? "N/A"}), ` +
        `W${record.win ?? 0}/L${record.loss ?? 0}/D${record.draw ?? 0}`
    );
  }
  return lines.join("\n");
}

export function formatStreamers(raw) {
  const list = raw?.streamers ?? [];
  const live = list.filter((s) => s.is_live).slice(0, 10);
  if (live.length === 0) return "No streamers are currently live.";
  const lines = [`Currently live streamers (top ${live.length}):`];
  for (const s of live) {
    const watch = (s.platforms ?? [])
      .filter((p) => p.is_live && p.stream_url)
      .map((p) => `${p.type}: ${p.stream_url}`)
      .join(", ");
    lines.push(`- ${s.username} [LIVE]${watch ? ` — watch: ${watch}` : ""}`);
  }
  return lines.join("\n");
}

export function formatLeaderboards(raw) {
  if (!raw) return "No leaderboard data available.";
  const lines = ["Current Chess.com leaderboards (top 5 per category):"];
  for (const [category, players] of Object.entries(raw)) {
    if (!Array.isArray(players)) continue;
    lines.push(`\n${category.replace(/_/g, " ")}:`);
    for (const p of players.slice(0, 5)) {
      lines.push(`  ${p.rank ?? ""} ${p.username}: ${p.score ?? "N/A"}`);
    }
  }
  return lines.join("\n");
}
