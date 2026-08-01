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
    country: str = "International"
    translation_en: Optional[str] = None
    id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Post":
        hashtags = data.get("hashtags", [])
        if isinstance(hashtags, str):
            hashtags = [h.strip() for h in hashtags.split(",") if h.strip()]
        return cls(
            platform=str(data.get("platform", "unknown")),
            author=str(data.get("author", "Anonymous")),
            text=str(data.get("text", "")),
            hashtags=hashtags,
            likes=int(data.get("likes", 0)),
            comments=int(data.get("comments", 0)),
            shares=int(data.get("shares", 0)),
            views=int(data.get("views", 0)),
            created_at=str(data.get("created_at", datetime.utcnow().isoformat())),
            url=str(data.get("url", "")),
            media=data.get("media"),
            language=str(data.get("language", "en")),
            country=str(data.get("country", "International")),
            translation_en=data.get("translation_en"),
            id=data.get("id")
        )

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScoredPost":
        base_post = Post.from_dict(data)
        base_dict = base_post.to_dict()
        base_dict.update({
            "virality_score": float(data.get("virality_score", 0.0)),
            "engagement_score": float(data.get("engagement_score", 0.0)),
            "freshness_score": float(data.get("freshness_score", 0.0)),
            "authority_score": float(data.get("authority_score", 0.0)),
            "platform_weight": float(data.get("platform_weight", 1.0)),
            "trend_score": float(data.get("trend_score", 0.0)),
            "score_breakdown": data.get("score_breakdown", {}),
            "summary": str(data.get("summary", "")),
            "entities": data.get("entities", {})
        })
        return cls(**base_dict)

