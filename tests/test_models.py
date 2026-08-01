import unittest
from models.post import Post, ScoredPost
from models.topic import Topic
from models.platform import PlatformMetrics

class TestModels(unittest.TestCase):
    def test_post_from_dict_and_to_dict(self):
        raw_data = {
            "platform": "x",
            "author": "@testuser",
            "text": "DeepSeek R1 model released open weights!",
            "hashtags": ["AI", "OpenSource"],
            "likes": 1500,
            "comments": 200,
            "shares": 350,
            "views": 45000,
            "created_at": "2026-02-01T12:00:00",
            "url": "https://x.com/testuser/status/12345",
            "country": "China"
        }
        post = Post.from_dict(raw_data)
        self.assertEqual(post.platform, "x")
        self.assertEqual(post.author, "@testuser")
        self.assertEqual(post.likes, 1500)
        self.assertEqual(post.country, "China")
        
        post_dict = post.to_dict()
        self.assertEqual(post_dict["country"], "China")
        self.assertEqual(post_dict["likes"], 1500)

    def test_scored_post_from_dict(self):
        raw_data = {
            "platform": "threads",
            "author": "@dev",
            "text": "Claude 3.7 hybrid reasoning test",
            "likes": 500,
            "comments": 50,
            "shares": 10,
            "views": 2000,
            "created_at": "2026-02-01T12:00:00",
            "url": "https://threads.net/post/1",
            "trend_score": 88.5,
            "virality_score": 92.0
        }
        scored = ScoredPost.from_dict(raw_data)
        self.assertEqual(scored.trend_score, 88.5)
        self.assertEqual(scored.virality_score, 92.0)
        self.assertEqual(scored.platform, "threads")

    def test_topic_serialization(self):
        topic_data = {
            "name": "Reasoning LLMs",
            "trend_score": 94.2,
            "growth_pct": 145.0,
            "mentions_count": 520,
            "platforms_involved": ["x", "reddit"],
            "sentiment_score": 0.85,
            "confidence_score": 0.95
        }
        topic = Topic.from_dict(topic_data)
        self.assertEqual(topic.name, "Reasoning LLMs")
        self.assertEqual(topic.trend_score, 94.2)
        self.assertIn("x", topic.platforms_involved)

    def test_platform_metrics_serialization(self):
        data = {
            "platform": "tiktok",
            "posts_count": 45,
            "avg_engagement": 1200.5,
            "top_topic": "AI Video",
            "growth_pct": 25.0,
            "status": "active",
            "last_crawled": "12:00:00"
        }
        pm = PlatformMetrics.from_dict(data)
        self.assertEqual(pm.platform, "tiktok")
        self.assertEqual(pm.posts_count, 45)
        self.assertEqual(pm.status, "active")

if __name__ == "__main__":
    unittest.main()
