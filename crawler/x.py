import os
import logging
import httpx
from typing import List
from crawler.base import BaseAdapter
from crawler.mock_data import generate_mock_posts
from models.post import Post

logger = logging.getLogger(__name__)

class XAdapter(BaseAdapter):
    """
    X / Twitter Adapter.
    Uses Official Twitter v2 API when TWITTER_BEARER_TOKEN is configured in .env.
    Falls back gracefully to high-fidelity seed generator when token is empty.
    """

    def __init__(self):
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "").strip()

    @property
    def platform_name(self) -> str:
        return "x"

    def fetch_posts(self, keywords: List[str], limit: int = 30) -> List[Post]:
        if self.bearer_token:
            try:
                real_posts = self._fetch_from_twitter_api(keywords, limit=limit)
                if real_posts:
                    return real_posts
            except Exception as e:
                logger.error(f"Twitter API call failed: {e}. Falling back to seed adapter.")

        return generate_mock_posts("x", keywords, limit=limit)

    def _fetch_from_twitter_api(self, keywords: List[str], limit: int = 30) -> List[Post]:
        query = f"({' OR '.join(keywords[:5])}) -is:retweet lang:en"
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {
            "query": query,
            "max_results": min(100, max(10, limit)),
            "tweet.fields": "created_at,public_metrics,lang,author_id",
            "expansions": "author_id",
            "user.fields": "username,name"
        }

        with httpx.Client(timeout=12.0) as client:
            resp = client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            tweets = data.get("data", [])
            users = {u["id"]: u["username"] for u in data.get("includes", {}).get("users", [])}

            posts: List[Post] = []
            for tweet in tweets:
                author_id = tweet.get("author_id", "")
                username = f"@{users.get(author_id, 'user')}"
                metrics = tweet.get("public_metrics", {})
                tweet_id = tweet.get("id", "")
                created_at = tweet.get("created_at", "")
                text = tweet.get("text", "")

                posts.append(Post(
                    platform="x",
                    author=username,
                    text=text,
                    hashtags=[f"#{kw}" for kw in keywords if kw.lower() in text.lower()],
                    likes=metrics.get("like_count", 0),
                    comments=metrics.get("reply_count", 0),
                    shares=metrics.get("retweet_count", 0),
                    views=metrics.get("impression_count", 0),
                    created_at=created_at,
                    url=f"https://x.com/{users.get(author_id, 'i')}/status/{tweet_id}",
                    language=tweet.get("lang", "en"),
                    country="International",
                    id=f"x_real_{tweet_id}"
                ))
            return posts
