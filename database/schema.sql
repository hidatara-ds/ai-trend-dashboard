CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    author TEXT NOT NULL,
    text TEXT NOT NULL,
    hashtags TEXT DEFAULT '[]',
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    url TEXT NOT NULL,
    media TEXT,
    language TEXT DEFAULT 'en',
    country TEXT DEFAULT 'International',
    translation_en TEXT DEFAULT '',
    virality_score REAL DEFAULT 0.0,
    engagement_score REAL DEFAULT 0.0,
    freshness_score REAL DEFAULT 0.0,
    authority_score REAL DEFAULT 0.0,
    platform_weight REAL DEFAULT 1.0,
    trend_score REAL DEFAULT 0.0,
    score_breakdown TEXT DEFAULT '{}',
    summary TEXT DEFAULT '',
    entities TEXT DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_country ON posts(country);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_posts_trend_score ON posts(trend_score DESC);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    trend_score REAL DEFAULT 0.0,
    growth_pct REAL DEFAULT 0.0,
    mentions_count INTEGER DEFAULT 0,
    platforms_involved TEXT DEFAULT '[]',
    sentiment_score REAL DEFAULT 0.0,
    confidence_score REAL DEFAULT 1.0,
    key_entities TEXT DEFAULT '{}',
    summary TEXT DEFAULT '',
    last_updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS keywords (
    keyword TEXT PRIMARY KEY,
    added_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS crawl_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL,
    posts_fetched INTEGER DEFAULT 0,
    error_message TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    report_type TEXT NOT NULL,
    content TEXT NOT NULL
);
