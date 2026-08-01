from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class PlatformMetrics:
    platform: str
    posts_count: int
    avg_engagement: float
    top_topic: str
    growth_pct: float
    status: str  # 'active', 'degraded', 'error'
    last_crawled: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlatformMetrics":
        return cls(
            platform=str(data.get("platform", "unknown")),
            posts_count=int(data.get("posts_count", 0)),
            avg_engagement=float(data.get("avg_engagement", 0.0)),
            top_topic=str(data.get("top_topic", "N/A")),
            growth_pct=float(data.get("growth_pct", 0.0)),
            status=str(data.get("status", "active")),
            last_crawled=str(data.get("last_crawled", ""))
        )

