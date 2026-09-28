import os
from hindsight_client import Hindsight
from typing import List, Dict, Any

class MemoryManager:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY", "")
        self.base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
        self.enabled = bool(self.api_key)
        if self.enabled:
            self.client = Hindsight(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None

    def recall(self, customer_id: str, query: str) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []
        try:
            # Call hindsight API to recall facts
            # Note: actual structure of response might vary; mocking the extract of text.
            response = self.client.recall(bank_id=customer_id, query=query)
            
            # Handling hypothetical response structure based on common Vectorize SDKs
            # We'll just return what we get, or map it.
            memories = []
            if hasattr(response, 'memories'):
                for m in response.memories:
                    memories.append({"content": m.content, "metadata": getattr(m, 'metadata', {})})
            elif isinstance(response, list):
                # if it's a raw list of dicts or objects
                for m in response:
                    if isinstance(m, dict):
                        memories.append(m)
                    else:
                        memories.append({"content": getattr(m, 'content', str(m))})
            return memories
        except Exception as e:
            print(f"Error recalling memory for {customer_id}: {e}")
            return []

    def retain(self, customer_id: str, content: str) -> bool:
        if not self.enabled:
            return False
        try:
            self.client.retain(bank_id=customer_id, content=content)
            return True
        except Exception as e:
            print(f"Error retaining memory for {customer_id}: {e}")
            return False
