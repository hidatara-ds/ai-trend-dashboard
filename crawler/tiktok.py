import os
import logging
import httpx
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class TikTokAdapter(BaseAdapter):
    """
    TikTok Research/Display API Adapter.
    Uses Official TikTok API when TIKTOK_ACCESS_TOKEN is configured in .env.
    Falls back gracefully to high-fidelity seed generator when token is empty.
    """

    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "").strip()

    @property
    def platform_name(self) -> str:
        return "tiktok"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        if self.access_token:
            try:
                real_posts = self._fetch_from_tiktok_api(keywords, limit=limit)
                if real_posts:
                    return real_posts
            except Exception as e:
                logger.error(f"TikTok API call failed: {e}. Falling back to seed adapter.")

        return generate_mock_posts("tiktok", keywords, limit=limit)

    def _fetch_from_tiktok_api(self, keywords: List[str], limit: int = 30) -> List[Post]:
        url = "https://open.tiktokapis.com/v2/research/video/query/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": {
                "and": [{"field_name": "keyword", "operation": "IN", "field_values": keywords[:3]}]
            },
            "max_count": limit
        }

        with httpx.Client(timeout=12.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json().get("data", {})

            videos = data.get("videos", [])
            posts: List[Post] = []
            for vid in videos:
                vid_id = vid.get("id", "")
                username = f"@{vid.get('username', 'creator')}"
                title = vid.get("video_description", "")
                created_at = vid.get("create_time", "")

                posts.append(Post(
                    platform="tiktok",
                    author=username,
                    text=title,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in title.lower()],
                    likes=vid.get("like_count", 0),
                    comments=vid.get("comment_count", 0),
                    shares=vid.get("share_count", 0),
                    views=vid.get("view_count", 0),
                    created_at=str(created_at),
                    url=f"https://www.tiktok.com/{username}/video/{vid_id}",
                    language="en",
                    country="International",
                    id=f"tiktok_real_{vid_id}"
                ))
            return posts
