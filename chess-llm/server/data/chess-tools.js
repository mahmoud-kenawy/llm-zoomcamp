import { tool } from "langchain";
import { z } from "zod";
import {
  extractUsernames,
  getPlayerProfileLive,
  getPlayerStatsLive,
  getStreamersLive,
  getLeaderboardsLive,
  formatProfile,
  formatStats,
  formatStreamers,
  formatLeaderboards,
} from "./chess-api.js";

export const getPlayerProfile = tool(
  async ({ username, message }) => {
    const name = (username || extractUsernames(message)[0] || "").toLowerCase();
    if (!name) {
      return "No username provided. Which player? Please give me the Chess.com username.";
    }
    console.log(`♟️ Fetching live profile for: "${name}"`);
    try {
      const raw = await getPlayerProfileLive(name);
      return formatProfile(raw);
    } catch (e) {
      return `Error fetching profile for ${name}: ${e.message}`;
    }
  },
  {
    name: "get_player_profile",
    description:
      "Fetch a live Chess.com player profile. Pass username directly, or pass the user message so it can be auto-extracted.",
    schema: z.object({
      username: z.string().optional().describe("Chess.com username (lowercase)"),
      message: z.string().optional().describe("Full user message for username auto-extraction"),
    }),
  }
);

export const getPlayerStats = tool(
  async ({ username, message }) => {
    const name = (username || extractUsernames(message)[0] || "").toLowerCase();
    if (!name) {
      return "No username provided. Which player? Please give me the Chess.com username.";
    }
    console.log(`♟️ Fetching live stats for: "${name}"`);
    try {
      const raw = await getPlayerStatsLive(name);
      return formatStats(name, raw);
    } catch (e) {
      return `Error fetching stats for ${name}: ${e.message}`;
    }
  },
  {
    name: "get_player_stats",
    description:
      "Fetch live Chess.com player ratings and stats (rapid, blitz, bullet, daily, etc.). Pass username or the user message for auto-extraction.",
    schema: z.object({
      username: z.string().optional().describe("Chess.com username (lowercase)"),
      message: z.string().optional().describe("Full user message for username auto-extraction"),
    }),
  }
);

export const getStreamers = tool(
  async () => {
    console.log("♟️ Fetching live streamers");
    try {
      const raw = await getStreamersLive();
      return formatStreamers(raw);
    } catch (e) {
      return `Error fetching streamers: ${e.message}`;
    }
  },
  {
    name: "get_streamers",
    description: "Fetch currently listed Chess.com streamers and who is live.",
    schema: z.object({}),
  }
);

export const getLeaderboards = tool(
  async () => {
    console.log("♟️ Fetching live leaderboards");
    try {
      const raw = await getLeaderboardsLive();
      return formatLeaderboards(raw);
    } catch (e) {
      return `Error fetching leaderboards: ${e.message}`;
    }
  },
  {
    name: "get_leaderboards",
    description: "Fetch current Chess.com leaderboards across all time controls.",
    schema: z.object({}),
  }
);
