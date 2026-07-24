import os
import logging
import httpx
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class ThreadsAdapter(BaseAdapter):
    """
    Meta Threads Adapter.
    Uses Official Meta Threads API when THREADS_ACCESS_TOKEN is configured in .env.
    Falls back gracefully to high-fidelity seed generator when token is empty.
    """

    def __init__(self):
        self.access_token = os.getenv("THREADS_ACCESS_TOKEN", "").strip()

    @property
    def platform_name(self) -> str:
        return "threads"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        if self.access_token:
            try:
                real_posts = self._fetch_from_threads_api(keywords, limit=limit)
                if real_posts:
                    return real_posts
            except Exception as e:
                logger.error(f"Threads API call failed: {e}. Falling back to seed adapter.")

        return generate_mock_posts("threads", keywords, limit=limit)

    def _fetch_from_threads_api(self, keywords: List[str], limit: int = 30) -> List[Post]:
        url = "https://graph.threads.net/v1.0/me/threads"
        params = {
            "fields": "id,media_product_type,media_type,text,timestamp,username,permalink,like_count,reply_count",
            "access_token": self.access_token,
            "limit": min(100, max(10, limit))
        }

        with httpx.Client(timeout=12.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("data", [])
            posts: List[Post] = []
            for item in items:
                text = item.get("text", "")
                post_id = item.get("id", "")
                username = f"@{item.get('username', 'threads_user')}"
                permalink = item.get("permalink", f"https://www.threads.net/{username}/post/{post_id}")
                created_at = item.get("timestamp", "")

                posts.append(Post(
                    platform="threads",
                    author=username,
                    text=text,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in text.lower()],
                    likes=item.get("like_count", 0),
                    comments=item.get("reply_count", 0),
                    shares=0,
                    views=0,
                    created_at=created_at,
                    url=permalink,
                    language="en",
                    country="International",
                    id=f"threads_real_{post_id}"
                ))
            return posts
