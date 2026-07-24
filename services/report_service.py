from typing import Dict, Any
from database.db import DatabaseManager
from analyzer.openrouter_client import OpenRouterAnalyzer
from models.post import ScoredPost
from models.topic import Topic

class ReportService:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()

    def generate_daily_digest(self) -> Dict[str, Any]:
        api_key = self.db.get_setting("openrouter_api_key", "")
        model = self.db.get_setting("openrouter_model", "anthropic/claude-3.5-sonnet")

        analyzer = OpenRouterAnalyzer(api_key=api_key, model=model)

        posts_data = self.db.get_posts(limit=50)
        topics_data = self.db.get_topics(limit=10)

        posts = [ScoredPost(**p) for p in posts_data]
        topics = [Topic(**t) for t in topics_data]

        digest = analyzer.generate_trend_digest(posts, topics)
        self.db.save_ai_report("daily_digest", digest)
        return digest

    def get_latest_digest(self) -> Dict[str, Any]:
        report = self.db.get_latest_ai_report("daily_digest")
        if not report:
            return self.generate_daily_digest()
        return report
