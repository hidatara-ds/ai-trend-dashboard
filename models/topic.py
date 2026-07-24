from dataclasses import dataclass, field
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
