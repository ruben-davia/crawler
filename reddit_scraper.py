#!/usr/bin/env python3
"""
Reddit Scraper for User Needs Discovery
Loads queries from JSON file and scrapes Reddit to find user insights.
"""

import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Only import Firecrawl if we're actually going to use it
try:
    from firecrawl import Firecrawl

    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False
    print("⚠️  Firecrawl not available. Install with: pip install firecrawl-py")

load_dotenv()


class RedditSearchScraper:
    """Scrapes search results using pre-generated queries"""

    def __init__(self, queries_file=None):
        self.search_results = []
        self.queries_file = queries_file

        if FIRECRAWL_AVAILABLE:
            api_key = os.getenv("FIRECRAWL_API_KEY")
            if not api_key:
                raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
            self.firecrawl = Firecrawl(api_key=api_key)
        else:
            self.firecrawl = None

    def load_queries_from_json(self, filename):
        """Load queries from JSON file"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Return full query objects instead of just query strings
            queries = data["queries"]
            print(f"📂 Loaded {len(queries)} queries from {filename}")
            return queries

        except FileNotFoundError:
            print(f"❌ Query file {filename} not found.")
            return []
        except Exception as e:
            print(f"❌ Error loading queries: {str(e)}")
            return []

    def scrape_and_save(self, queries=None, limit_per_query=1, progress_save=True):
        """Scrape Reddit using queries and save user insights"""
        if not self.firecrawl:
            print("❌ Cannot scrape without Firecrawl. Please install firecrawl-py")
            return []

        if not queries:
            if self.queries_file:
                queries = self.load_queries_from_json(self.queries_file)
            else:
                print("❌ No queries provided and no queries file specified")
                return []

        base_filename = "search_results"

        print(f"🚀 Starting to scrape {len(queries)} queries...")

        for i, query_obj in enumerate(queries):
            query_text = query_obj["query"]
            print(f"Discovery search {i + 1}/{len(queries)}: {query_text}")

            try:
                # Search with Firecrawl
                results = self.firecrawl.search(
                    query=query_text,
                    limit=limit_per_query,
                    scrape_options={
                        "formats": ["markdown", "links"],
                        "onlyMainContent": True,
                    },
                    timeout=30000,
                )

                # Process search results with full query metadata
                self.process_search_results(results, query_obj)

                # Save progress after each search
                if progress_save and self.search_results:
                    progress_filename = f"{base_filename}_progress.json"
                    self.save_results(progress_filename)

                # Rate limiting: 5 searches per minute = 12 seconds between searches
                print(f"⏳ Waiting 12 seconds for rate limiting (5 searches/minute)...")
                time.sleep(15)

            except Exception as e:
                print(f"Error searching '{query_text}': {str(e)}")
                continue

        return self.search_results

    def extract_url_title_description(self, searchdata):
        """Extract URL, title, and description from search results"""
        web_results = getattr(searchdata, "web", None)
        if not web_results:
            return []
        extracted = []
        for item in web_results:
            url = getattr(item, "url", "")
            title = getattr(item, "title", "")
            description = getattr(item, "description", "")
            extracted.append({"url": url, "title": title, "description": description})
        return extracted

    def process_search_results(self, results, query_obj):
        """Save raw search results to JSON"""
        if not results:
            return

        extracted_results = self.extract_url_title_description(results)

        for result in extracted_results:
            # Add the original query and platform to the result
            result["source_query"] = query_obj["query"]
            result["query_type"] = query_obj["type"]
            result["subreddit"] = query_obj["subreddit"]
            result["category"] = query_obj["category"]
            result["timestamp"] = datetime.now().isoformat()
            result["platform"] = self.get_platform(result.get("url", ""))

            self.search_results.append(result)
            print(f"  ✅ Saved result: {result['title'][:60]}...")

    def get_platform(self, url):
        """Determine the platform from URL"""
        if "reddit.com" in url:
            return "reddit"
        elif "stackoverflow.com" in url:
            return "stackoverflow"
        elif "github.com" in url:
            return "github"
        else:
            return "other"

    def save_results(self, filename=None):
        """Save search results to JSON file"""
        if not filename:
            filename = "search_results.json"

        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()

        for result in self.search_results:
            if result["url"] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result["url"])

        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "total_results": len(unique_results),
                    "timestamp": datetime.now().isoformat(),
                    "results": unique_results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"💾 Saved {len(unique_results)} unique search results to {filename}")
        return filename

    def generate_summary(self, results):
        """Generate a simple summary of the search results"""
        summary = {"platforms": {}, "total_results": len(results)}

        for result in results:
            # Count platforms
            platform = result.get("platform", "other")
            summary["platforms"][platform] = summary["platforms"].get(platform, 0) + 1

        return summary

    def load_existing_progress(self, filename):
        """Load existing progress from a previous session"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing_insights = data.get("results", [])

            # Add existing results to current session
            for result in existing_insights:
                if result not in self.search_results:
                    self.search_results.append(result)

            print(
                f"📂 Loaded {len(existing_insights)} existing results from {filename}"
            )
            return True

        except FileNotFoundError:
            print(f"⚠️  Progress file {filename} not found. Starting fresh.")
            return False
        except Exception as e:
            print(f"❌ Error loading progress file: {str(e)}")
            return False

    def display_summary(self):
        """Display a summary of found search results"""
        if not self.search_results:
            print("❌ No search results found.")
            return

        print("\n📊 SEARCH RESULTS SUMMARY:")
        print(f"Total results found: {len(self.search_results)}")

        # Group by platform
        platforms = {}
        for result in self.search_results:
            platform = result.get("platform", "other")
            platforms[platform] = platforms.get(platform, 0) + 1

        print("\n📈 By platform:")
        for platform, count in platforms.items():
            print(f"  {platform}: {count}")

        # Group by query type
        query_types = {}
        for result in self.search_results:
            query_type = result.get("query_type", "other")
            query_types[query_type] = query_types.get(query_type, 0) + 1

        print("\n📊 By query type:")
        for query_type, count in query_types.items():
            print(f"  {query_type}: {count}")

        # Group by subreddit
        subreddits = {}
        for result in self.search_results:
            subreddit = result.get("subreddit", "other")
            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1

        print("\n🏷️  By subreddit:")
        for subreddit, count in subreddits.items():
            print(f"  r/{subreddit}: {count}")

        # Group by category
        categories = {}
        for result in self.search_results:
            category = result.get("category", "other")
            categories[category] = categories.get(category, 0) + 1

        print("\n📂 By category:")
        for category, count in categories.items():
            print(f"  {category}: {count}")

        print("\n🔝 Top 5 results:")
        for i, result in enumerate(self.search_results[:5]):
            print(f"  {i + 1}. {result['title'][:80]}...")
            print(f"     URL: {result['url']}")
            print(f"     Query: {result.get('source_query', 'N/A')}")
            print(f"     Type: {result.get('query_type', 'N/A')}")
            print(f"     Subreddit: {result.get('subreddit', 'N/A')}")
            print(f"     Category: {result.get('category', 'N/A')}")
            print()


def main():
    """Main execution function for scraping"""
    print("🚀 Starting Reddit Search Scraper...")

    # Check if queries file exists
    query_file = "discovery_queries.json"

    if not os.path.exists(query_file):
        print("❌ Query file not found. Please run query_generator.py first.")
        return

    print(f"📂 Using query file: {query_file}")

    # Create scraper instance
    scraper = RedditSearchScraper(query_file)

    # Load and display query info
    queries = scraper.load_queries_from_json(query_file)
    if not queries:
        print("❌ No queries loaded. Exiting.")
        return

    print(f"📊 Loaded {len(queries)} queries")
    print(
        f"Sample query: {queries[0]['query']} (Type: {queries[0]['type']}, Subreddit: {queries[0]['subreddit']})"
    )

    # Start scraping
    results = scraper.scrape_and_save(limit_per_query=5)

    # Display summary
    scraper.display_summary()

    # Save final results
    if results:
        final_filename = scraper.save_results()
        print("\n✅ Scraping completed!")
        print(f"📁 Final results saved to: {final_filename}")
    else:
        print("\n❌ No results found.")


if __name__ == "__main__":
    main()
