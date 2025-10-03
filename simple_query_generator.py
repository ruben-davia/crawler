#!/usr/bin/env python3
"""
Simple Query Generator - Just generates queries, nothing else
"""

import json


def generate_queries():
    """Generate focused discovery queries for business subreddits only (50-60 queries max)"""

    # Core business subreddits only
    business_subreddits = [
        "entrepreneur",
        "startups",
        "smallbusiness",
        "business",
        "marketing",
        "sales",
        "SaaS",
        "ecommerce",
        "freelance",
        "consulting",
    ]

    # Core question patterns (focused on business struggles)
    core_patterns = [
        "how do I",
        "struggling with",
        "need help with",
        "can't figure out",
        "my business",
        "looking for",
    ]

    queries = []

    # Generate 5-6 queries per subreddit (50-60 total)
    for subreddit in business_subreddits:
        for pattern in core_patterns:
            query = f"{pattern} site:reddit.com/r/{subreddit}"
            queries.append(
                {
                    "query": query,
                    "type": "subreddit_question",
                    "subreddit": subreddit,
                    "category": "subreddit_specific",
                }
            )

    return queries


def main():
    """Generate and save queries"""
    print("🔍 Generating discovery queries...")

    queries = generate_queries()

    # Create JSON structure with metadata
    data = {
        "metadata": {
            "total_queries": len(queries),
            "generated_at": "2024-01-01T00:00:00Z",
            "description": "Focused discovery queries for business subreddits only",
            "query_types": {"subreddit_question": len(queries)},
            "subreddits": list(
                set([q["subreddit"] for q in queries if q["subreddit"] is not None])
            ),
            "categories": ["subreddit_specific"],
        },
        "queries": queries,
    }

    # Save to file
    with open("discovery_queries.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"💾 Saved {len(queries)} queries to discovery_queries.json")
    print(f"📊 Total queries: {len(queries)}")
    print(f"📈 Query types: {data['metadata']['query_types']}")
    print(f"🏷️  Subreddits: {len(data['metadata']['subreddits'])}")
    print(f"📂 Categories: {data['metadata']['categories']}")


if __name__ == "__main__":
    main()
