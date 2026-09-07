import { tool } from "langchain";
import { z } from "zod";
import { QdrantVectorStore } from "@langchain/qdrant";
import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";
import { QdrantClient } from "@qdrant/js-client-rest";

let vectorStore;

const getVectorStore = async () => {
  if (vectorStore) return vectorStore;

  const apiKey = process.env.GEMINI_API_KEY;
  const qdrantUrl = process.env.QDRANT_URL;
  const qdrantApiKey = process.env.QDRANT_API_KEY;
  const collectionName = process.env.QDRANT_COLLECTION_NAME || "chess-llm";

  if (!apiKey) {
    throw new Error("Missing GEMINI_API_KEY");
  }
  if (!qdrantUrl) {
    throw new Error("Missing QDRANT_URL");
  }
  if (!qdrantApiKey) {
    throw new Error("Missing QDRANT_API_KEY");
  }

  const client = new QdrantClient({ url: qdrantUrl, apiKey: qdrantApiKey });

  // This MUST match the embedding model used during ingestion
  const embeddings = new GoogleGenerativeAIEmbeddings({
    model: "gemini-embedding-001",
    apiKey,
    taskType: "RETRIEVAL_QUERY",
  });

  vectorStore = new QdrantVectorStore(embeddings, {
    client,
    collectionName,
  });

  return vectorStore;
};

export const searchKnowledgeBase = tool(
  async ({ query }) => {
    console.log(`🔍 Agent is searching Qdrant for: "${query}"`);

    const store = await getVectorStore();

    // We fetch the top 10 most similar chunks
    const results = await store.similaritySearch(query, 10);

    // For demo purposes
    results.forEach((r, i) => {
      const type = r.metadata?.type ?? "unknown";
      console.log(`Result ${i + 1} [${type}]:`, r.pageContent.slice(0, 200));
    });

    if (results.length === 0) {
      return "No relevant chess information found in the knowledge base.";
    }

    // Join the chunks so the LLM can read them as one context block
    return results.map((doc) => doc.pageContent).join("\n\n---\n\n");
  },
  {
    name: "search_knowledge_base",
    description:
      "Searches the chess knowledge base for openings, famous games, concepts, champions, players, streamers, and leaderboards. Use this first for general chess questions.",
    schema: z.object({
      query: z.string().describe("The search query for chess information"),
    }),
  }
);
