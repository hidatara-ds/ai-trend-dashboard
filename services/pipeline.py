import logging
import concurrent.futures
from datetime import datetime
from typing import List, Dict, Any, Tuple


from database.db import DatabaseManager
from crawler.base import BaseAdapter
from crawler.instagram import InstagramAdapter
from crawler.tiktok import TikTokAdapter
from crawler.threads import ThreadsAdapter
from crawler.facebook import FacebookAdapter
from crawler.x import XAdapter
from scoring.engine import ScoringEngine
from analyzer.deduplication import deduplicate_posts
from analyzer.clustering import cluster_topics_from_posts
from analyzer.translator import AutoTranslator
from models.post import Post, ScoredPost

logger = logging.getLogger(__name__)

class CrawlPipeline:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
        self.adapters: List[BaseAdapter] = [
            InstagramAdapter(),
            TikTokAdapter(),
            ThreadsAdapter(),
            FacebookAdapter(),
            XAdapter()
        ]
        self.scorer = ScoringEngine()
        self.translator = AutoTranslator()

    def run_crawl_cycle(self, limit_per_platform: int = 30) -> Dict[str, Any]:
        """
        Executes parallel crawl cycle across all 5 platform adapters.
        Independent error handling ensures failure of one platform adapter
        does NOT break execution for other platforms.
        """
        keywords = self.db.get_keywords_list()
        all_raw_posts: List[Post] = []
        platform_status = {}

        def fetch_single(adapter: BaseAdapter) -> Tuple[str, List[Post], str]:
            try:
                posts = adapter.fetch_posts(keywords, limit=limit_per_platform)
                return (adapter.platform_name, posts, "ok")
            except Exception as e:
                logger.error(f"Error crawling {adapter.platform_name}: {e}")
                return (adapter.platform_name, [], str(e))

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_adapter = {executor.submit(fetch_single, adp): adp for adp in self.adapters}
            for future in concurrent.futures.as_completed(future_to_adapter):
                platform, posts, err = future.result()
                if err == "ok":
                    all_raw_posts.extend(posts)
                    platform_status[platform] = f"OK ({len(posts)} posts)"
                    self.db.log_crawl(platform, "success", len(posts))
                else:
                    platform_status[platform] = f"Error: {err}"
                    self.db.log_crawl(platform, "failed", 0, err)

        # Score posts
        scored_posts = self.scorer.score_batch(all_raw_posts)

        # Deduplicate
        unique_posts = deduplicate_posts(scored_posts, similarity_threshold=0.88)

        # Auto-translate non-English posts if translation_en is missing
        for p in unique_posts:
            if not p.translation_en and p.language != "en":
                trans = self.translator.translate_to_english(p.text, source_language=p.language)
                if trans:
                    p.translation_en = trans

        # Save to database
        saved_count = self.db.save_posts(unique_posts)

        # Re-cluster topics from posts
        all_db_posts = [ScoredPost(**p) for p in self.db.get_posts(limit=200)]
        topics = cluster_topics_from_posts(all_db_posts)
        self.db.save_topics(topics)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "raw_fetched": len(all_raw_posts),
            "deduplicated_saved": saved_count,
            "topics_count": len(topics),
            "platform_status": platform_status
        }
