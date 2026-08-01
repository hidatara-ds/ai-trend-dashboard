import unittest
import tempfile
import gc
from pathlib import Path
from database.db import DatabaseManager
from models.post import ScoredPost

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "test_ai_trends.db"
        self.db = DatabaseManager(db_path=self.db_file)

    def tearDown(self):
        del self.db
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_database_manager_init(self):
        self.assertTrue(self.db_file.exists())
        keywords = self.db.get_keywords_list()
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)

    def test_save_and_get_posts(self):
        scored_post = ScoredPost(
            platform="x",
            author="@test",
            text="Test post",
            hashtags=["test"],
            likes=10,
            comments=2,
            shares=1,
            views=100,
            created_at="2026-02-01T12:00:00",
            url="https://x.com/test/1",
            id="test_post_1",
            trend_score=75.0
        )
        self.db.save_posts([scored_post])
        
        count = self.db.get_posts_count()
        self.assertGreaterEqual(count, 1)
        
        posts = self.db.get_posts_paginated(limit=10, offset=0)
        self.assertGreaterEqual(len(posts), 1)
        self.assertEqual(posts[0]["id"], "test_post_1")

if __name__ == "__main__":
    unittest.main()
