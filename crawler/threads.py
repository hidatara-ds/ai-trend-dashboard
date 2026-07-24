import logging
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class ThreadsAdapter(BaseAdapter):
    @property
    def platform_name(self) -> str:
        return "threads"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        try:
            return generate_mock_posts("threads", keywords, limit=limit)
        except Exception as e:
            logger.error(f"ThreadsAdapter error: {e}")
            return []
