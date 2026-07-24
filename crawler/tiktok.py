import logging
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class TikTokAdapter(BaseAdapter):
    @property
    def platform_name(self) -> str:
        return "tiktok"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        try:
            return generate_mock_posts("tiktok", keywords, limit=limit)
        except Exception as e:
            logger.error(f"TikTokAdapter error: {e}")
            return []
