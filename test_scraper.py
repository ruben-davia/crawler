#!/usr/bin/env python3
"""
Test version of Reddit Scraper - runs only a few queries for testing
"""

import json
import os
from reddit_scraper import RedditUserInsightsScraper


def test_scraper():
    """Test the scraper with a small subset of queries"""
    print("🧪 Testing Reddit Scraper with limited queries...")

    # Load queries
    query_file = "discovery_queries.json"
    scraper = RedditUserInsightsScraper(query_file)
    all_queries = scraper.load_queries_from_json(query_file)

    if not all_queries:
        print("❌ No queries loaded. Exiting.")
        return

    # Test with just the first 5 queries
    test_queries = all_queries[:5]
    print(f"🧪 Testing with {len(test_queries)} queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"  {i}. {query}")

    print("\n🚀 Starting test scrape...")

    # Run the scraper
    insights = scraper.scrape_and_save(queries=test_queries, limit_per_query=1)

    # Display results
    scraper.display_summary()

    # Save test results
    if insights:
        test_filename = "test_results.json"
        scraper.save_results(test_filename)
        print(f"\n✅ Test completed! Results saved to: {test_filename}")
    else:
        print("\n❌ No results found in test.")


if __name__ == "__main__":
    test_scraper()
