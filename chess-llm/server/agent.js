import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { createAgent } from "langchain";
import { MemorySaver } from "@langchain/langgraph-checkpoint";
import { searchKnowledgeBase } from "./tools.js";
import {
  getPlayerProfile,
  getPlayerStats,
  getStreamers,
  getLeaderboards,
} from "./data/chess-tools.js";

// Create a memory saver for persisting conversation history
const checkpointer = new MemorySaver();

const CHESS_SYSTEM_PROMPT = `You are Chess LLM, an expert chess assistant with access to:
1. A knowledge base of chess openings, famous games, concepts, and world champions (search_knowledge_base).
2. Live Chess.com data: player profiles, ratings, statistics (get_player_profile, get_player_stats).
3. Current streamers and leaderboards (get_streamers, get_leaderboards).

Rules:
- For general chess questions (openings, tactics, endgames, history), search the knowledge base first.
- When the user asks about a specific player, extract the username from the message
  (e.g. "@hikaru", "Hikaru Nakamura", "magnus carlsen") and call get_player_profile
  and get_player_stats with it.
- If a player-related question has no identifiable username, ask: "Which player? Please give me the Chess.com username."
- For "who is streaming / live streamers", call get_streamers.
- For "leaderboards / top players / ratings", call get_leaderboards.
- Be concise, accurate, and chess-focused.`;

export async function runAgent({ sessionId = "default", message }) {
  try {
    const model = new ChatGoogleGenerativeAI({
      model: process.env.GEMINI_CHAT_MODEL || "gemini-3.5-flash-lite",
      temperature: 0,
      apiKey: process.env.GEMINI_API_KEY,
    });

    const agent = createAgent({
      model,
      tools: [
        searchKnowledgeBase,
        getPlayerProfile,
        getPlayerStats,
        getStreamers,
        getLeaderboards,
      ],
      checkpointer,
      systemPrompt: CHESS_SYSTEM_PROMPT,
    });

    console.log(`♟️ Chess LLM running for: "${message}"`);

    // Invoke here has an agentic behavior and it will decide to use the tool or not.
    const response = await agent.invoke(
      {
        messages: [{ role: "user", content: message }],
      },
      {
        configurable: {
          thread_id: sessionId, // This maintains conversation history per session
        },
      }
    );

    // Extract the last message content
    const lastMessage = response.messages[response.messages.length - 1];
    const output = lastMessage?.content || "";

    console.log(`✅ Agent response: ${output.slice(0, 100)}...`);

    return { output };
  } catch (error) {
    console.error("❌ Error in runAgent:", error);
    throw error;
  }
}
