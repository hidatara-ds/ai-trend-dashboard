import random
from datetime import datetime, timedelta
from typing import List
from models.post import Post

SAMPLE_AUTHORS = {
    "x": ["@sama", "@karpathy", "@ylecun", "@drfeifei", "@bindureddy", "@swyx", "@deepseek_ai", "@alibabagroup", "@tekno_indo"],
    "threads": ["@zuck", "@mosseri", "@techcrunch", "@theverge", "@mit_tech_review", "@ai_indonesia", "@weibo_tech"],
    "tiktok": ["@ai_technician", "@future_tools_tech", "@coder_daily", "@automation_guy", "@deep_tech_tok", "@indotech_tok"],
    "instagram": ["@ai_future_official", "@tech_insider", "@modern_developer", "@ai_lab_daily", "@futurism", "@ai_nusantara"],
    "facebook": ["Artificial Intelligence Community", "Tech Trends Today", "AI Developers Network", "Komunitas AI Indonesia", "China AI Lab"]
}

SAMPLE_TEMPLATES = [
    # International (English)
    {
        "text": "DeepSeek R1 open weights are completely altering the open-source LLM landscape. Achieving high reasoning capability with 1/10th the compute budget is a game changer for local deployments.",
        "hashtags": ["#DeepSeek", "#OpenSourceAI", "#LLM", "#AIReasoning"],
        "keywords": ["DeepSeek", "Reasoning Models"],
        "country": "International",
        "language": "en",
        "translation_en": None
    },
    {
        "text": "Testing Claude 3.7 Sonnet hybrid reasoning mode on complex refactoring tasks. The ability to dynamically toggle thinking budget per API call makes developer workflows insanely productive.",
        "hashtags": ["#Claude37", "#Anthropic", "#AI", "#CodingAssistant"],
        "keywords": ["Claude", "Anthropic"],
        "country": "International",
        "language": "en",
        "translation_en": None
    },
    {
        "text": "Cursor rules configuration combined with DeepSeek R1 local server gives full context-aware code generation inside VSCode without sending IP to external clouds.",
        "hashtags": ["#CursorIDE", "#DevTools", "#AI", "#Productivity"],
        "keywords": ["Cursor", "DeepSeek"],
        "country": "International",
        "language": "en",
        "translation_en": None
    },
    {
        "text": "Gemini 2.0 Flash is ridiculously fast for multimodal live stream token processing. We built a zero-latency visual assistant running in browser WebRTC.",
        "hashtags": ["#Gemini20", "#GoogleAI", "#Multimodal", "#WebRTC"],
        "keywords": ["Gemini", "Google"],
        "country": "International",
        "language": "en",
        "translation_en": None
    },
    {
        "text": "Lovable.dev just shipped full-stack Supabase integration auto-generation. You can prompt an entire SaaS application with database, auth, and Stripe payments in under 4 minutes.",
        "hashtags": ["#Lovable", "#NoCode", "#AIAppBuilder", "#WebDev"],
        "keywords": ["Lovable"],
        "country": "International",
        "language": "en",
        "translation_en": None
    },
    # China (Chinese + English Translation)
    {
        "text": "DeepSeek R1 671B 满血版模型在推理 benchmark 上完全媲美 OpenAI o1！本地化部署只需蒸馏版 32B 即可在 RTX 4090 上平稳运行，国产大模型迎来重大突破。",
        "hashtags": ["#DeepSeek", "#深度求索", "#国产大模型", "#人工智能"],
        "keywords": ["DeepSeek", "Reasoning Models"],
        "country": "China",
        "language": "zh",
        "translation_en": "DeepSeek R1 671B full-powered model matches OpenAI o1 on reasoning benchmarks! Local deployment of the 32B distilled version runs smoothly on an RTX 4090—a major breakthrough for Chinese LLMs."
    },
    {
        "text": "通义千问 Qwen 2.5 Max 最新发布！在代码生成、数学解题和多步骤 Agent 调用上全面超越 Claude 3.5 Sonnet，阿里云开放在线 API 试用。",
        "hashtags": ["#Qwen25", "#阿里云", "#通义千问", "#大语言模型"],
        "keywords": ["Qwen", "Alibaba"],
        "country": "China",
        "language": "zh",
        "translation_en": "Tongyi Qwen 2.5 Max released! Completely surpasses Claude 3.5 Sonnet in code generation, math problem solving, and multi-step Agent calls. Alibaba Cloud opens online API trial."
    },
    {
        "text": "月之暗面 Kimi k1.5 长上下文推理更新，支持 200 万字无损上下文理解，金融研报和法律长文本分析效率提升 10 倍。",
        "hashtags": ["#Kimi", "#月之暗面", "#长文本推理", "#AI应用"],
        "keywords": ["Kimi", "Reasoning Models"],
        "country": "China",
        "language": "zh",
        "translation_en": "Moonshot AI Kimi k1.5 long-context reasoning updated! Supports 2M characters of lossless context understanding, boosting financial research and legal long-text analysis by 10x."
    },
    {
        "text": "智谱 AI GLM-4-Voice 开源端到端语音大模型，支持实时双工语音对话，延迟低至 300ms，拟人化情绪非常真实。",
        "hashtags": ["#智谱AI", "#GLM4", "#语音大模型", "#开源AI"],
        "keywords": ["Zhipu AI", "GLM"],
        "country": "China",
        "language": "zh",
        "translation_en": "Zhipu AI GLM-4-Voice open-sources end-to-end voice LLM! Supports real-time duplex speech conversation with latency under 300ms and ultra-realistic natural emotion."
    },
    # Indonesia (Indonesian)
    {
        "text": "Model LLM Sahabat-AI buatan konsorsium Indonesia resmi meluncurkan checkpoint 8B dan 70B! Sangat akurat memahami dialek lokal, Bahasa Indonesia formal, dan konteks budaya Nusantara.",
        "hashtags": ["#SahabatAI", "#AIIndonesia", "#InovasiLokal", "#TeknologiNusantara"],
        "keywords": ["Sahabat-AI", "Indonesia AI"],
        "country": "Indonesia",
        "language": "id",
        "translation_en": "Sahabat-AI LLM built by Indonesian consortium officially launches 8B and 70B checkpoints! Highly accurate in understanding local dialects, formal Indonesian, and Nusantara cultural context."
    },
    {
        "text": "Adopsi AI di startup Indonesia meningkat pesat! Banyak developer lokal beralih dari prompt manual ke agentic workflow dengan Cursor IDE dan DeepSeek R1 untuk menghemat biaya cloud server.",
        "hashtags": ["#AIIndonesia", "#StartupIndo", "#DeveloperLokal", "#CursorIDE"],
        "keywords": ["Cursor", "DeepSeek"],
        "country": "Indonesia",
        "language": "id",
        "translation_en": "AI adoption in Indonesian startups is surging! Many local developers are switching from manual prompts to agentic workflows with Cursor IDE & DeepSeek R1 to cut cloud server costs."
    },
    {
        "text": "Kementerian Komdigi dan Indosat resmi meresmikan AI Center Indonesia di Solo untuk mendorong riset generative AI dan talenta digital berstandar global.",
        "hashtags": ["#Komdigi", "#IndosatOoredoo", "#AICenter Solo", "#DigitalIndonesia"],
        "keywords": ["AI Center", "Indonesia AI"],
        "country": "Indonesia",
        "language": "id",
        "translation_en": "Ministry of Communications & Digital with Indosat inaugurate AI Center Indonesia in Solo to drive generative AI research and global-standard digital tech talents."
    }
]

def generate_mock_posts(platform: str, count: int = 10) -> List[Post]:
    """Mock seed generation disabled in favor of 100% real live news crawling."""
    return []
