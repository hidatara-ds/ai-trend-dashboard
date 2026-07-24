import logging
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class InstagramAdapter(BaseAdapter):
    @property
    def platform_name(self) -> str:
        return "instagram"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        try:
            # Live crawler/scraper integration point
            # Falls back to high quality mock data generator
            return generate_mock_posts("instagram", keywords, limit=limit)
        except Exception as e:
            logger.error(f"InstagramAdapter error: {e}")
            return []
