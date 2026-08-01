import unittest
from datetime import datetime
from models.post import Post
from scoring.engine import ScoringEngine

class TestScoring(unittest.TestCase):
    def test_scoring_engine_calculation(self):
        engine = ScoringEngine(half_life_hours=24.0)
        now_str = datetime.utcnow().isoformat()
        post = Post(
            platform="x",
            author="@sama",
            text="Launching next generation AI capabilities!",
            hashtags=["AI"],
            likes=10000,
            comments=2000,
            shares=1500,
            views=250000,
            created_at=now_str,
            url="https://x.com/sama/status/1"
        )
        scored = engine.calculate_scores(post, sentiment_score=0.5)
        self.assertGreater(scored.trend_score, 0)
        self.assertGreater(scored.virality_score, 0)
        self.assertEqual(scored.authority_score, 95.0)
        self.assertEqual(scored.platform, "x")
        self.assertIn("hours_old", scored.score_breakdown)

    def test_scoring_batch(self):
        engine = ScoringEngine()
        now_str = datetime.utcnow().isoformat()
        posts = [
            Post("x", "@user1", "Post 1", [], 100, 10, 5, 1000, now_str, "url1"),
            Post("threads", "@user2", "Post 2", [], 500, 50, 25, 5000, now_str, "url2")
        ]
        results = engine.score_batch(posts)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].platform, "x")
        self.assertEqual(results[1].platform, "threads")

if __name__ == "__main__":
    unittest.main()
