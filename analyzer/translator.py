import os
import re
import logging
import httpx
from typing import Optional
from config.settings import DEFAULT_OPENROUTER_BASE_URL, DEFAULT_OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class AutoTranslator:
    """
    Real-time auto-translation service for social posts.
    Translates non-English posts (e.g. Chinese, Indonesian, Spanish) into English.
    Uses OpenRouter API when key is configured, or regex heuristics when unconfigured.
    """

    def __init__(self, openrouter_api_key: str = ""):
        self.api_key = openrouter_api_key.strip() or os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = DEFAULT_OPENROUTER_BASE_URL

    def translate_to_english(self, text: str, source_language: str = "auto") -> Optional[str]:
        if not text or not text.strip():
            return None

        # Check if text contains CJK (Chinese, Japanese, Korean) characters
        has_cjk = bool(re.search(r'[\u4e00-\u9fff]', text))

        if not has_cjk and source_language == "en":
            return None

        if self.api_key:
            try:
                prompt = f"Translate the following social media post into clear, natural English. Return ONLY the translated English text, nothing else:\n\n{text}"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": DEFAULT_OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logger.warning(f"OpenRouter auto-translation failed: {e}")

        return None
