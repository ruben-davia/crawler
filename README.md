# Reddit User Needs Discovery System

A modular system to discover what people actually want and struggle with on Reddit, focusing on business and entrepreneurship topics.

## 🎯 Purpose

This system generates exploratory queries to find user needs, pain points, and desires rather than pre-defining questions. It discovers what people want and struggle with through sentiment analysis of Reddit discussions.

## 🔄 Methodology

1. **Generate Subqueries**: Create targeted search queries for different subreddits and topics
2. **Firecrawl Search**: Use Firecrawl API to search Reddit with rate limiting (5 searches/minute)
3. **Extract Insights**: Process results to identify pain points, desires, and solutions

## 📁 File Structure

### Core Files

- **`query_generator.py`** - Generates and saves discovery queries to JSON
- **`reddit_scraper.py`** - Loads queries and scrapes Reddit for user insights
- **`crawl.py`** - Main runner that shows usage and system status
- **`requirements.txt`** - Python dependencies

### Generated Files

- **`discovery_queries_YYYYMMDD_HHMMSS.json`** - Generated query tables
- **`user_insights_YYYYMMDD_HHMMSS.json`** - Final scraped insights
- **`user_insights_YYYYMMDD_HHMMSS_progress.json`** - Progress saves during scraping

## 🚀 Usage

### 1. Setup

```bash
# Install dependencies
pip install firecrawl-py python-dotenv

# Create .env file with your Firecrawl API key
echo "FIRECRAWL_API_KEY=your_api_key_here" > .env
```

### 2. Generate Queries

```bash
python3 query_generator.py
```

This creates a JSON file with 682+ discovery queries including:

- Base discovery queries (42)
- Subreddit-specific queries (190)
- Topic-specific queries (450)

### 3. Run Scraper

```bash
python3 reddit_scraper.py
```

This loads the queries and scrapes Reddit to find user insights. The scraper respects Firecrawl's rate limit of 5 searches per minute (15-second delays between searches).

### 4. Check Status

```bash
python3 crawl.py
```

Shows system status, file checks, and usage instructions.

## 🔍 Query Types

The system generates queries to discover:

### Pain Points

- "frustrated with reddit.com"
- "struggling with reddit.com"
- "having trouble reddit.com"
- "problem with reddit.com"

### Desires

- "want to reddit.com"
- "wish I could reddit.com"
- "looking for reddit.com"
- "need reddit.com"

### Solutions

- "worked for me reddit.com"
- "succeeded in reddit.com"
- "helped me reddit.com"

### Comparisons

- "better than reddit.com"
- "alternative to reddit.com"
- "vs reddit.com"

## 📊 Target Subreddits

- r/entrepreneur, r/startups, r/smallbusiness
- r/marketing, r/sales, r/finance
- r/webdev, r/programming, r/SaaS
- r/AskReddit, r/legaladvice, r/careerguidance
- And more...

## 🧠 Insight Analysis

The scraper analyzes content for:

- **Insight Type**: pain_point, desire, solution, comparison
- **Intensity**: 1-10 scale based on emotional language
- **Key Phrases**: business terms (marketing, sales, funding, etc.)
- **Platform Classification**: Reddit-focused

## 📈 Output Format

```json
{
  "total_insights": 150,
  "timestamp": "2025-01-XX...",
  "insights": [...],
  "insight_summary": {
    "by_type": {"pain_point": 45, "desire": 38, "solution": 67},
    "by_intensity": {"high": 23, "medium": 89, "low": 38},
    "top_key_phrases": {"marketing": 15, "sales": 12, "funding": 8},
    "platforms": {"reddit": 150}
  }
}
```

## ⚡ Key Features

- **Modular Architecture**: Separate query generation and scraping
- **No Pre-defined Questions**: Discovers what people actually want
- **Rate Limited**: Respects Firecrawl's 5 searches/minute limit
- **Progress Saving**: Saves progress during long scraping sessions
- **Business-Focused**: Targets entrepreneurship and business topics

## 🔧 Dependencies

- `firecrawl-py` - Web scraping and search
- `python-dotenv` - Environment variable management
- `json` - Data serialization
- `datetime` - Timestamping

## 📝 Example Workflow

1. Run `query_generator.py` → Creates query table
2. Run `reddit_scraper.py` → Discovers user insights
3. Analyze JSON output → Find business opportunities
4. Use insights → Build products people actually want

This system helps you understand what people really struggle with and want, rather than guessing or using predefined questions.
