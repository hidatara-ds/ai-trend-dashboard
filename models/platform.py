from dataclasses import dataclass

@dataclass
class PlatformMetrics:
    platform: str
    posts_count: int
    avg_engagement: float
    top_topic: str
    growth_pct: float
    status: str  # 'active', 'degraded', 'error'
    last_crawled: str
