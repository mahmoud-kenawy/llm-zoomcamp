from google import genai
from google.genai import types
from google.genai import errors
from typing import List
import time


class GeminiEmbeddings:
    def __init__(self, api_key: str, model: str = "gemini-embedding-001", max_retries: int = 6):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries

    def _embed_with_retry(self, texts: List[str], task_type: str):
        delay = 2.0
        for attempt in range(self.max_retries):
            try:
                return self.client.models.embed_content(
                    model=self.model,
                    contents=texts,
                    config=types.EmbedContentConfig(task_type=task_type)
                )
            except errors.ClientError as e:
                if e.code == 429 and attempt < self.max_retries - 1:
                    print(f"  Rate limited, retrying in {delay:.0f}s (attempt {attempt + 1}/{self.max_retries})...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise

    def embed_documents(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        if not texts:
            return []
        result = self._embed_with_retry(texts, task_type)
        return [e.values for e in result.embeddings]

    def embed_query(self, text: str, task_type: str = "RETRIEVAL_QUERY") -> List[float]:
        result = self._embed_with_retry([text], task_type)
        return result.embeddings[0].values