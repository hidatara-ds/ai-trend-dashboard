import math
from datetime import datetime
from typing import Dict, Any, List
from models.post import Post, ScoredPost
from config.settings import DEFAULT_PLATFORM_WEIGHTS

class ScoringEngine:
    """
    Explainable, multi-factor scoring engine for social media AI trend intelligence.
    Calculates:
    - Engagement Score: Weighted sum of interactions (likes, comments, shares, views).
    - Virality Score: Acceleration of engagement relative to post age.
    - Freshness Score: Exponential half-life time decay.
    - Authority Score: Author reputation proxy.
    - Platform Weight: Configurable platform importance multiplier.
    - Overall Trend Score: Explainable weighted combination (0.0 to 100.0).
    """

    def __init__(self, platform_weights: Dict[str, float] = None):
        self.platform_weights = platform_weights or DEFAULT_PLATFORM_WEIGHTS

    def calculate_scores(self, post: Post) -> ScoredPost:
        now = datetime.utcnow()
        try:
            created_dt = datetime.fromisoformat(post.created_at.replace("Z", "+00:00"))
            if created_dt.tzinfo is not None:
                created_dt = created_dt.replace(tzinfo=None)
        except Exception:
            created_dt = now

        hours_elapsed = max(0.1, (now - created_dt).total_seconds() / 3600.0)

        # 1. Engagement Score (0 - 100 scale)
        raw_engagement = post.likes + (post.comments * 2.5) + (post.shares * 4.0) + (post.views * 0.05)
        # Logarithmic scaling for engagement
        engagement_score = min(100.0, math.log10(max(1.0, raw_engagement)) * 20.0)

        # 2. Virality Score (0 - 100 scale)
        virality_rate = raw_engagement / math.sqrt(hours_elapsed)
        virality_score = min(100.0, math.log10(max(1.0, virality_rate)) * 22.0)

        # 3. Freshness Score (Exponential decay with ~24h half-life)
        freshness_score = 100.0 * math.exp(-0.04 * hours_elapsed)

        # 4. Authority Score (Proxy based on author and verification hints)
        authority_score = 70.0
        if post.author.startswith("@sama") or post.author.startswith("@karpathy") or post.author.startswith("@zuck"):
            authority_score = 95.0
        elif post.author.startswith("@"):
            authority_score = 75.0

        # 5. Platform Weight
        platform_weight = self.platform_weights.get(post.platform.lower(), 1.0)

        # 6. Combined Trend Score
        base_trend = (
            (0.35 * virality_score) +
            (0.25 * engagement_score) +
            (0.25 * freshness_score) +
            (0.15 * authority_score)
        )
        final_trend_score = min(100.0, round(base_trend * platform_weight, 1))

        breakdown = {
            "hours_old": round(hours_elapsed, 1),
            "raw_engagement": int(raw_engagement),
            "engagement_score": round(engagement_score, 1),
            "virality_score": round(virality_score, 1),
            "freshness_score": round(freshness_score, 1),
            "authority_score": round(authority_score, 1),
            "platform_weight": platform_weight,
            "final_trend_score": final_trend_score,
            "formula": "(0.35*Virality + 0.25*Engagement + 0.25*Freshness + 0.15*Authority) * PlatformWeight"
        }

        return ScoredPost(
            platform=post.platform,
            author=post.author,
            text=post.text,
            hashtags=post.hashtags,
            likes=post.likes,
            comments=post.comments,
            shares=post.shares,
            views=post.views,
            created_at=post.created_at,
            url=post.url,
            media=post.media,
            language=post.language,
            country=getattr(post, "country", "International"),
            translation_en=getattr(post, "translation_en", None),
            id=post.id,
            virality_score=round(virality_score, 1),
            engagement_score=round(engagement_score, 1),
            freshness_score=round(freshness_score, 1),
            authority_score=round(authority_score, 1),
            platform_weight=platform_weight,
            trend_score=final_trend_score,
            score_breakdown=breakdown,
            summary="",
            entities={}
        )

    def score_batch(self, posts: List[Post]) -> List[ScoredPost]:
        return [self.calculate_scores(p) for p in posts]
