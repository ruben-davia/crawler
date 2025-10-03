#!/usr/bin/env python3
"""
Configuration settings for the Reddit scraper
"""

# Scraping settings
SCRAPING_CONFIG = {
    # Number of results per query (1-10 recommended)
    "limit_per_query": 1,
    # Delay between queries in seconds (to avoid rate limiting)
    "delay_between_queries": 1,
    # Whether to save progress after each query
    "save_progress": True,
    # Maximum queries to process (None for all)
    "max_queries": None,
    # Query types to include (None for all)
    "query_types": None,  # ["question_pattern", "business_context", "industry_question", "subreddit_question"]
    # Subreddits to focus on (None for all)
    "target_subreddits": None,  # ["entrepreneur", "startups", "business"]
    # Categories to include (None for all)
    "categories": None,  # ["general_questions", "industry_specific", "subreddit_specific", "business_areas"]
}

# Output settings
OUTPUT_CONFIG = {
    # Base filename for results
    "base_filename": "reddit_insights",
    # Whether to include raw search data
    "include_raw_data": False,
    # Whether to analyze content for insights
    "analyze_insights": True,
    # Minimum insight intensity to include (1-10)
    "min_insight_intensity": 3,
}

# Analysis settings
ANALYSIS_CONFIG = {
    # Business terms to look for
    "business_terms": [
        "marketing",
        "sales",
        "funding",
        "investors",
        "customers",
        "revenue",
        "growth",
        "scaling",
        "hiring",
        "product",
        "service",
        "automation",
        "analytics",
        "lead generation",
        "email marketing",
        "social media",
        "website",
        "mobile app",
        "e-commerce",
        "inventory",
        "payments",
    ],
    # Pain point indicators
    "pain_indicators": [
        "frustrated",
        "struggling",
        "trouble",
        "problem",
        "issue",
        "challenge",
        "difficult",
        "hard",
        "expensive",
        "complicated",
        "waste of time",
        "too much work",
        "not worth it",
        "can't figure out",
        "don't understand",
        "failed to",
        "didn't work",
    ],
    # Desire indicators
    "desire_indicators": [
        "want to",
        "wish I could",
        "dream of",
        "would love to",
        "hoping to",
        "trying to",
        "looking for",
        "need",
        "wish there was",
    ],
}
