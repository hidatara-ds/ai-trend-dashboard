import os
import logging
import httpx
from typing import List, Dict, Any
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post
from config.settings import DEFAULT_SOCIALCRAWL_BASE_URL

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = ["tiktok", "threads", "instagram", "x", "github", "youtube", "reddit", "pinterest"]

class SocialCrawlAdapter(BaseAdapter):
    """
    SocialCrawl 3rd-Party Unified Multi-Platform Search Adapter.
    Executes a single API query across TikTok, Threads, Instagram, X, GitHub, YouTube, Reddit, Pinterest.
    Normalizes multi-platform social results into standard Post dataclasses.
    Falls back gracefully when SOCIALCRAWL_API_KEY is unconfigured.
    """

    def __init__(self):
        self.api_key = os.getenv("SOCIALCRAWL_API_KEY", "").strip()
        self.base_url = os.getenv("SOCIALCRAWL_BASE_URL", DEFAULT_SOCIALCRAWL_BASE_URL).strip()

    @property
    def platform_name(self) -> str:
        return "socialcrawl"

    def fetch_posts(self, keywords: List[str], limit: int = 50) -> List[Post]:
        if self.api_key:
            try:
                posts = self._fetch_from_socialcrawl_api(keywords, limit=limit)
                if posts:
                    return posts
            except Exception as e:
                logger.error(f"SocialCrawl API call failed: {e}. Falling back to multi-platform generator.")

        # Fallback multi-platform seed generation
        fallback_posts: List[Post] = []
        platforms_to_seed = ["x", "threads", "tiktok", "instagram", "facebook"]
        seed_limit = max(5, limit // len(platforms_to_seed))
        for plat in platforms_to_seed:
            fallback_posts.extend(generate_mock_posts(plat, keywords, limit=seed_limit))

        return fallback_posts

    def _fetch_from_socialcrawl_api(self, keywords: List[str], limit: int = 50) -> List[Post]:
        query_str = " OR ".join(keywords[:6]) if keywords else "AI"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "query": query_str,
            "platforms": ",".join(SUPPORTED_PLATFORMS),
            "limit": limit
        }

        with httpx.Client(timeout=15.0) as client:
            resp = client.get(f"{self.base_url}/search", headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("data", []) or data.get("results", []) or data.get("posts", [])
            posts: List[Post] = []

            for idx, item in enumerate(items):
                platform = item.get("platform", "x").lower()
                author = item.get("author") or item.get("username") or f"@{platform}_user"
                if not author.startswith("@") and not author.startswith("http"):
                    author = f"@{author}"

                text = item.get("text") or item.get("caption") or item.get("title") or item.get("content", "")
                created_at = item.get("created_at") or item.get("timestamp") or item.get("date", "")
                url = item.get("url") or item.get("permalink") or item.get("link", f"https://{platform}.com/{idx}")
                lang = item.get("language") or item.get("lang", "en")
                country = item.get("country", "International")
                translation_en = item.get("translation_en")

                metrics = item.get("metrics", {})
                likes = item.get("likes") or metrics.get("likes", 0)
                comments = item.get("comments") or metrics.get("comments", 0)
                shares = item.get("shares") or metrics.get("shares", 0)
                views = item.get("views") or metrics.get("views", 0)

                post_id = item.get("id") or f"{platform}_{idx}"

                posts.append(Post(
                    platform=platform,
                    author=author,
                    text=text,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in text.lower()],
                    likes=int(likes or 0),
                    comments=int(comments or 0),
                    shares=int(shares or 0),
                    views=int(views or 0),
                    created_at=str(created_at),
                    url=str(url),
                    media=item.get("media_url") or item.get("image"),
                    language=lang,
                    country=country,
                    translation_en=translation_en,
                    id=f"socialcrawl_{post_id}"
                ))

            return posts
