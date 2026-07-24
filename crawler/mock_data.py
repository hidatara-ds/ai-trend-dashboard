import random
from datetime import datetime, timedelta
from typing import List
from models.post import Post

SAMPLE_AUTHORS = {
    "x": ["@sama", "@karpathy", "@ylecun", "@drfeifei", "@bindureddy", "@swyx", "@goodfellow_ian", "@EMostaque"],
    "threads": ["@zuck", "@mosseri", "@techcrunch", "@theverge", "@mit_tech_review", "@ai_insights"],
    "tiktok": ["@ai_technician", "@future_tools_tech", "@coder_daily", "@automation_guy", "@deep_tech_tok"],
    "instagram": ["@ai_future_official", "@tech_insider", "@modern_developer", "@ai_lab_daily", "@futurism"],
    "facebook": ["Artificial Intelligence Community", "Tech Trends Today", "AI Developers Network", "OpenSource AI Group"]
}

SAMPLE_TEMPLATES = [
    {
        "text": "DeepSeek R1 open weights are completely altering the open-source LLM landscape. Achieving high reasoning capability with 1/10th the compute budget is a game changer for local deployments.",
        "hashtags": ["#DeepSeek", "#OpenSourceAI", "#LLM", "#AIReasoning"],
        "keywords": ["DeepSeek", "Reasoning Models"]
    },
    {
        "text": "Testing Claude 3.7 Sonnet hybrid reasoning mode on complex refactoring tasks. The ability to dynamically toggle thinking budget per API call makes developer workflows insanely productive.",
        "hashtags": ["#Claude37", "#Anthropic", "#AI", "#CodingAssistant"],
        "keywords": ["Claude", "Anthropic"]
    },
    {
        "text": "Cursor rules configuration combined with DeepSeek R1 local server gives full context-aware code generation inside VSCode without sending IP to external clouds. This is the future of software engineering.",
        "hashtags": ["#CursorIDE", "#DevTools", "#AI", "#Productivity"],
        "keywords": ["Cursor", "DeepSeek"]
    },
    {
        "text": "Gemini 2.0 Flash is ridiculously fast for multimodal live stream token processing. We built a zero-latency visual assistant running in browser WebRTC.",
        "hashtags": ["#Gemini20", "#GoogleAI", "#Multimodal", "#WebRTC"],
        "keywords": ["Gemini", "Google"]
    },
    {
        "text": "Lovable.dev just shipped full-stack Supabase integration auto-generation. You can prompt an entire SaaS application with database, auth, and Stripe payments in under 4 minutes.",
        "hashtags": ["#Lovable", "#NoCode", "#AIAppBuilder", "#WebDev"],
        "keywords": ["Lovable"]
    },
    {
        "text": "ChatGPT o3-mini and web search integration: reasoning models are rapidly blurring the line between traditional search engines and decision-making agents.",
        "hashtags": ["#ChatGPT", "#OpenAI", "#SearchGPT", "#AIAgents"],
        "keywords": ["ChatGPT", "OpenAI"]
    },
    {
        "text": "Llama 3.3 70B fine-tuned on specialized medical datasets is matching proprietary model scores on clinical reasoning benchmarks while preserving patient data privacy.",
        "hashtags": ["#Llama3", "#MetaAI", "#HealthcareAI", "#OpenSource"],
        "keywords": ["Llama"]
    },
    {
        "text": "Agentic AI frameworks like CrewAI and AutoGen are shifting from simple prompt pipelines to autonomous multi-agent swarms with persistent SQLite memory.",
        "hashtags": ["#AgenticAI", "#AIAgents", "#Python", "#SoftwareArchitecture"],
        "keywords": ["Agentic AI"]
    },
    {
        "text": "Qwen 2.5 Max benchmark results released! The open model matches top tier closed APIs across code execution, math, and multi-step tool use.",
        "hashtags": ["#Qwen25", "#AlibabaCloud", "#OpenWeights", "#LLM"],
        "keywords": ["Qwen"]
    },
    {
        "text": "Sora 2 preview displays physics-consistent spatial rendering and realistic object collision in generated 60fps video clips. Text-to-video is maturing rapidly.",
        "hashtags": ["#Sora", "#OpenAI", "#AIModels", "#GenerativeVideo"],
        "keywords": ["Sora", "OpenAI"]
    }
]

def generate_mock_posts(platform: str, keywords: List[str], limit: int = 30) -> List[Post]:
    posts: List[Post] = []
    authors = SAMPLE_AUTHORS.get(platform, ["@ai_news_daily"])

    now = datetime.utcnow()

    for i in range(limit):
        tmpl = random.choice(SAMPLE_TEMPLATES)
        author = random.choice(authors)

        # random creation time within last 48 hours
        hours_ago = random.uniform(0.1, 48.0)
        created_at = (now - timedelta(hours=hours_ago)).isoformat()

        # scale engagement based on platform
        base_likes = random.randint(150, 18000)
        comments = int(base_likes * random.uniform(0.05, 0.25))
        shares = int(base_likes * random.uniform(0.02, 0.15))
        views = base_likes * random.randint(8, 35)

        url = f"https://{platform}.com/{author.replace('@', '')}/status/{1000000 + i + random.randint(100, 999)}"

        posts.append(Post(
            platform=platform,
            author=author,
            text=tmpl["text"],
            hashtags=tmpl["hashtags"],
            likes=base_likes,
            comments=comments,
            shares=shares,
            views=views,
            created_at=created_at,
            url=url,
            media=f"https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=60" if i % 3 == 0 else None,
            language="en",
            id=f"{platform}_{i}_{int(hours_ago)}"
        ))
    return posts
