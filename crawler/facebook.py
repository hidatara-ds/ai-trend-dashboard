import os
import logging
import httpx
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class FacebookAdapter(BaseAdapter):
    """
    Facebook Graph API Adapter.
    Uses Official Meta Graph API when FACEBOOK_ACCESS_TOKEN is configured in .env.
    Falls back gracefully to high-fidelity seed generator when token is empty.
    """

    def __init__(self):
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "").strip()

    @property
    def platform_name(self) -> str:
        return "facebook"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        if self.access_token:
            try:
                real_posts = self._fetch_from_facebook_api(keywords, limit=limit)
                if real_posts:
                    return real_posts
            except Exception as e:
                logger.error(f"Facebook API call failed: {e}. Falling back to seed adapter.")

        return generate_mock_posts("facebook", keywords, limit=limit)

    def _fetch_from_facebook_api(self, keywords: List[str], limit: int = 30) -> List[Post]:
        url = "https://graph.facebook.com/v19.0/me/feed"
        params = {
            "fields": "id,message,created_time,permalink_url,shares,reactions.summary(total_count)",
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
                msg = item.get("message", "")
                post_id = item.get("id", "")
                permalink = item.get("permalink_url", f"https://www.facebook.com/{post_id}")
                created_at = item.get("created_time", "")
                likes = item.get("reactions", {}).get("summary", {}).get("total_count", 0)

                posts.append(Post(
                    platform="facebook",
                    author="AI Tech Community",
                    text=msg,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in msg.lower()],
                    likes=likes,
                    comments=0,
                    shares=item.get("shares", {}).get("count", 0),
                    views=0,
                    created_at=created_at,
                    url=permalink,
                    language="en",
                    country="International",
                    id=f"fb_real_{post_id}"
                ))
            return posts
