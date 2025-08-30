# Database Configuration
DATABASE_PATH = "data/misinformation_detector.db"

# Twitter/Data Collection Configuration
TWITTER_CONFIG = {
    "max_tweets_per_run": 100,
    "days_back": 7,
    "languages": ["en"],
    "min_tweet_length": 10,
    "max_tweet_length": 280
}

# Keywords for different types of misinformation
MISINFORMATION_KEYWORDS = {
    "health": [
        "vaccine conspiracy", "covid hoax", "fake pandemic", 
        "vaccine side effects", "big pharma", "medical conspiracy"
    ],
    "politics": [
        "election fraud", "stolen election", "voting machines", 
        "ballot harvesting", "deep state", "political conspiracy"
    ],
    "science": [
        "climate change hoax", "global warming fake", "science conspiracy",
        "fake research", "bought scientists", "climate denial"
    ],
    "general": [
        "fake news", "mainstream media lies", "conspiracy theory",
        "cover up", "they don't want you to know", "wake up"
    ]
}

# Classification Configuration
CLASSIFICATION_CONFIG = {
    "model_name": "microsoft/DialoGPT-medium",
    "batch_size": 10,
    "max_length": 512,
    "confidence_threshold": 0.7,
    "use_rule_based_fallback": True
}

# Fact-checking Configuration
FACT_CHECK_CONFIG = {
    "enabled": True,
    "google_api_key": None,  # Set your API key here
    "timeout": 10,
    "max_sources": 5,
    "reliability_threshold": 0.6
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "page_title": "Misinformation Detection Dashboard",
    "page_icon": "🔍",
    "layout": "wide",
    "refresh_interval": 300,  # seconds
    "max_display_tweets": 1000
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/misinformation_detector.log"
}

# Pipeline Configuration
PIPELINE_CONFIG = {
    "run_interval_minutes": 60,
    "enable_scheduling": False,
    "enable_fact_checking": True,
    "auto_classify": True,
    "max_retries": 3
}
