from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class Post:
    platform: str
    author: str
    text: str
    hashtags: List[str]
    likes: int
    comments: int
    shares: int
    views: int
    created_at: str  # ISO format string YYYY-MM-DDTHH:MM:SS
    url: str
    media: Optional[str] = None
    language: str = "en"
    id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ScoredPost(Post):
    virality_score: float = 0.0
    engagement_score: float = 0.0
    freshness_score: float = 0.0
    authority_score: float = 0.0
    platform_weight: float = 1.0
    trend_score: float = 0.0
    score_breakdown: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""
    entities: Dict[str, List[str]] = field(default_factory=dict)
