from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

@dataclass
class Topic:
    name: str
    trend_score: float
    growth_pct: float
    mentions_count: int
    platforms_involved: List[str]
    sentiment_score: float  # -1.0 to 1.0
    confidence_score: float  # 0.0 to 1.0
    key_entities: Dict[str, List[str]] = field(default_factory=dict)
    summary: str = ""
    id: int = 0
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Topic":
        return cls(
            name=str(data.get("name", "")),
            trend_score=float(data.get("trend_score", 0.0)),
            growth_pct=float(data.get("growth_pct", 0.0)),
            mentions_count=int(data.get("mentions_count", 0)),
            platforms_involved=data.get("platforms_involved", []),
            sentiment_score=float(data.get("sentiment_score", 0.0)),
            confidence_score=float(data.get("confidence_score", 1.0)),
            key_entities=data.get("key_entities", {}),
            summary=str(data.get("summary", "")),
            id=int(data.get("id", 0)),
            last_updated=str(data.get("last_updated", ""))
        )

