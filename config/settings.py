import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "ai_trends.db"
ASSETS_DIR = BASE_DIR / "assets"
ENV_PATH = BASE_DIR / ".env"

def load_env_file():
    if ENV_PATH.exists():
        try:
            for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k_str = k.strip()
                    v_str = v.strip().strip('"').strip("'")
                    if k_str:
                        os.environ[k_str] = v_str
        except Exception:
            pass

load_env_file()

DEFAULT_KEYWORDS: List[str] = [
    "ChatGPT",
    "Claude",
    "Gemini",
    "Cursor",
    "DeepSeek",
    "Lovable",
    "Llama",
    "Qwen",
    "Mistral",
    "Sora",
    "OpenAI",
    "Anthropic",
    "Agentic AI",
    "Reasoning Models"
]

DEFAULT_PLATFORM_WEIGHTS: Dict[str, float] = {
    "x": 1.2,
    "github": 1.3,
    "threads": 1.1,
    "youtube": 1.1,
    "reddit": 1.1,
    "tiktok": 1.0,
    "instagram": 0.9,
    "facebook": 0.8,
    "pinterest": 0.8
}

DEFAULT_OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_SOCIALCRAWL_BASE_URL = "https://api.socialcrawl.io/v1"

@dataclass
class AppConfig:
    db_path: Path = DB_PATH
    socialcrawl_api_key: str = field(default_factory=lambda: os.getenv("SOCIALCRAWL_API_KEY", ""))
    socialcrawl_base_url: str = field(default_factory=lambda: os.getenv("SOCIALCRAWL_BASE_URL", DEFAULT_SOCIALCRAWL_BASE_URL))
    openrouter_api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_model: str = DEFAULT_OPENROUTER_MODEL
    twitter_bearer_token: str = field(default_factory=lambda: os.getenv("TWITTER_BEARER_TOKEN", ""))
    threads_access_token: str = field(default_factory=lambda: os.getenv("THREADS_ACCESS_TOKEN", ""))
    tiktok_access_token: str = field(default_factory=lambda: os.getenv("TIKTOK_ACCESS_TOKEN", ""))
    instagram_access_token: str = field(default_factory=lambda: os.getenv("INSTAGRAM_ACCESS_TOKEN", ""))
    facebook_access_token: str = field(default_factory=lambda: os.getenv("FACEBOOK_ACCESS_TOKEN", ""))
    news_api_key: str = field(default_factory=lambda: os.getenv("NEWS_API_KEY", ""))
    platform_weights: Dict[str, float] = field(default_factory=lambda: DEFAULT_PLATFORM_WEIGHTS.copy())
    keywords: List[str] = field(default_factory=lambda: DEFAULT_KEYWORDS.copy())
    update_interval_minutes: int = 15
    auto_refresh_sec: int = 60
