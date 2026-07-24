import os
import logging
import httpx
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class InstagramAdapter(BaseAdapter):
    """
    Instagram Graph API Adapter.
    Uses Official Meta Graph API when INSTAGRAM_ACCESS_TOKEN is configured in .env.
    Falls back gracefully to high-fidelity seed generator when token is empty.
    """

    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()

    @property
    def platform_name(self) -> str:
        return "instagram"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        if self.access_token:
            try:
                real_posts = self._fetch_from_instagram_api(keywords, limit=limit)
                if real_posts:
                    return real_posts
            except Exception as e:
                logger.error(f"Instagram API call failed: {e}. Falling back to seed adapter.")

        return generate_mock_posts("instagram", keywords, limit=limit)

    def _fetch_from_instagram_api(self, keywords: List[str], limit: int = 30) -> List[Post]:
        url = "https://graph.facebook.com/v19.0/ig_hashtag_search"
        params = {
            "user_id": "me",
            "q": keywords[0] if keywords else "ai",
            "access_token": self.access_token
        }

        with httpx.Client(timeout=12.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("data", [])
            posts: List[Post] = []
            for idx, item in enumerate(items):
                post_id = item.get("id", str(idx))
                caption = item.get("caption", "")
                permalink = item.get("permalink", f"https://www.instagram.com/p/{post_id}")
                created_at = item.get("timestamp", "")

                posts.append(Post(
                    platform="instagram",
                    author="@instagram_creator",
                    text=caption,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in caption.lower()],
                    likes=item.get("like_count", 0),
                    comments=item.get("comments_count", 0),
                    shares=0,
                    views=0,
                    created_at=created_at,
                    url=permalink,
                    language="en",
                    country="International",
                    id=f"ig_real_{post_id}"
                ))
            return posts
