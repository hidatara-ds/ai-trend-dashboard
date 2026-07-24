import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "ai_trends.db"
ASSETS_DIR = BASE_DIR / "assets"

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
    "threads": 1.1,
    "tiktok": 1.0,
    "instagram": 0.9,
    "facebook": 0.8
}

DEFAULT_OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

@dataclass
class AppConfig:
    db_path: Path = DB_PATH
    openrouter_api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_model: str = DEFAULT_OPENROUTER_MODEL
    platform_weights: Dict[str, float] = field(default_factory=lambda: DEFAULT_PLATFORM_WEIGHTS.copy())
    keywords: List[str] = field(default_factory=lambda: DEFAULT_KEYWORDS.copy())
    update_interval_minutes: int = 15
    auto_refresh_sec: int = 60
