import re
from typing import List, Dict, Any, Tuple
from collections import Counter
from models.post import ScoredPost
from models.topic import Topic

# Known entity dictionary for deterministic AI entity extraction
KNOWN_ENTITIES = {
    "companies": ["OpenAI", "Anthropic", "Google", "DeepSeek", "Meta", "Microsoft", "Alibaba", "Mistral AI", "Supabase"],
    "models": ["Claude 3.7 Sonnet", "DeepSeek R1", "Gemini 2.0 Flash", "GPT-4.5", "Llama 3.3", "Qwen 2.5", "Sora 2", "o3-mini"],
    "tools": ["Cursor", "Lovable.dev", "PyTorch", "LangChain", "CrewAI", "AutoGen", "VSCode", "Supabase", "Docker"],
    "frameworks": ["PyTorch", "LangChain", "CrewAI", "AutoGen", "Transformers", "vLLM", "Ollama"],
    "countries": ["United States", "China", "France", "Germany", "Japan", "United Kingdom"],
    "programming_languages": ["Python", "TypeScript", "Rust", "C++", "JavaScript", "Go"]
}

TOPIC_SEEDS = [
    {
        "name": "Reasoning Models & Open Weights",
        "keywords": ["deepseek", "r1", "reasoning", "open source", "weights", "compute", "o3-mini", "llama"],
        "summary": "Surge in high-efficiency reasoning models with open-weights benchmarks challenging proprietary APIs."
    },
    {
        "name": "AI Coding Assistants & IDEs",
        "keywords": ["cursor", "vscode", "claude 3.7", "sonnet", "refactoring", "context", "developer", "ide"],
        "summary": "Development workflows rapidly integrating hybrid-reasoning models and full codebase context engines."
    },
    {
        "name": "Autonomous Agentic Frameworks",
        "keywords": ["agentic", "crewai", "autogen", "agents", "swarm", "sqlite", "tools", "multi-agent"],
        "summary": "Shift towards multi-agent orchestration swarms operating autonomously with persistent memory."
    },
    {
        "name": "Fullstack AI Web Generation",
        "keywords": ["lovable", "supabase", "no-code", "prompt", "saas", "full-stack", "app builder"],
        "summary": "Next-generation generative web builders generating full Supabase database and payment stack instantly."
    },
    {
        "name": "Spatial & Physics Video Generation",
        "keywords": ["sora", "text-to-video", "physics", "rendering", "60fps", "collision", "video"],
        "summary": "Text-to-video capabilities maturing with physical world consistency and spatial rendering fidelity."
    }
]

def extract_entities(text: str) -> Dict[str, List[str]]:
    found: Dict[str, List[str]] = {}
    text_lower = text.lower()

    for category, entities in KNOWN_ENTITIES.items():
        matched = []
        for ent in entities:
            if ent.lower() in text_lower:
                matched.append(ent)
        if matched:
            found[category] = matched

    return found

def cluster_topics_from_posts(posts: List[ScoredPost]) -> List[Topic]:
    if not posts:
        return []

    topic_buckets: Dict[str, List[ScoredPost]] = {t["name"]: [] for t in TOPIC_SEEDS}
    topic_buckets["General AI Intelligence"] = []

    for post in posts:
        text_lower = post.text.lower()
        assigned = False

        for seed in TOPIC_SEEDS:
            if any(kw in text_lower for kw in seed["keywords"]):
                topic_buckets[seed["name"]].append(post)
                assigned = True
                break

        if not assigned:
            topic_buckets["General AI Intelligence"].append(post)

    topics: List[Topic] = []
    for seed in TOPIC_SEEDS + [{"name": "General AI Intelligence", "keywords": [], "summary": "Broader AI industry discussions and ecosystem news."}]:
        name = seed["name"]
        bucket_posts = topic_buckets.get(name, [])
        if not bucket_posts:
            continue

        mentions_count = len(bucket_posts)
        avg_trend_score = sum(p.trend_score for p in bucket_posts) / max(1, mentions_count)
        platforms = list(set(p.platform for p in bucket_posts))

        # Collect entities across posts in topic
        topic_entities: Dict[str, Counter] = {}
        for p in bucket_posts:
            ents = extract_entities(p.text)
            p.entities = ents
            for cat, items in ents.items():
                if cat not in topic_entities:
                    topic_entities[cat] = Counter()
                topic_entities[cat].update(items)

        formatted_entities = {
            cat: [item for item, _ in counter.most_common(5)]
            for cat, counter in topic_entities.items()
        }

        # Calculate sentiment proxy (positive tech sentiment)
        pos_words = ["productive", "game changer", "fast", "future", "impressive", "breakthrough", "efficiency"]
        neg_words = ["slow", "bug", "hallucination", "crash", "expensive", "concern"]

        total_pos = sum(sum(1 for w in pos_words if w in p.text.lower()) for p in bucket_posts)
        total_neg = sum(sum(1 for w in neg_words if w in p.text.lower()) for p in bucket_posts)
        sentiment = min(1.0, max(-1.0, (total_pos - total_neg) / max(1, total_pos + total_neg)))

        topics.append(Topic(
            name=name,
            trend_score=round(avg_trend_score, 1),
            growth_pct=round(12.5 + (mentions_count * 1.8), 1),
            mentions_count=mentions_count,
            platforms_involved=platforms,
            sentiment_score=round(sentiment, 2),
            confidence_score=0.94 if mentions_count > 3 else 0.82,
            key_entities=formatted_entities,
            summary=seed["summary"]
        ))

    return sorted(topics, key=lambda t: t.trend_score, reverse=True)
