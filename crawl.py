#!/usr/bin/env python3
"""
Reddit User Needs Discovery - Main Runner
This is the main entry point that demonstrates the separated architecture.
"""

import os
import sys


def print_banner():
    """Print a nice banner"""
    print("=" * 60)
    print("🔍 REDDIT USER NEEDS DISCOVERY SYSTEM")
    print("=" * 60)
    print("Discover what people actually want and struggle with on Reddit")
    print("=" * 60)


def print_usage():
    """Print usage instructions"""
    print("\n📖 USAGE:")
    print("1. Generate queries:  python3 query_generator.py")
    print("2. Run scraper:       python3 reddit_scraper.py")
    print("\n📁 FILES:")
    print("• query_generator.py  - Generates and saves discovery queries to JSON")
    print("• reddit_scraper.py   - Loads queries and scrapes Reddit for insights")
    print("• crawl.py           - This main runner (shows usage)")
    print("\n🔧 SETUP:")
    print("• pip install firecrawl-py python-dotenv")
    print("• Set FIRECRAWL_API_KEY in .env file")
    print("• Run query_generator.py first, then reddit_scraper.py")


def check_files():
    """Check if the required files exist"""
    files_to_check = ["query_generator.py", "reddit_scraper.py", "requirements.txt"]

    print("\n📋 FILE STATUS:")
    all_exist = True

    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing!")
            all_exist = False

    return all_exist


def check_environment():
    """Check if environment is properly set up"""
    print("\n🔧 ENVIRONMENT CHECK:")

    # Check for .env file
    if os.path.exists(".env"):
        print("  ✅ .env file exists")
    else:
        print("  ⚠️  .env file not found (create one with FIRECRAWL_API_KEY)")

    # Check for query files
    query_files = [
        f
        for f in os.listdir(".")
        if f.startswith("discovery_queries_") and f.endswith(".json")
    ]
    if query_files:
        print(f"  ✅ Found {len(query_files)} query file(s)")
        latest = max(query_files)
        print(f"     Latest: {latest}")
    else:
        print("  ⚠️  No query files found (run query_generator.py first)")


def main():
    """Main function"""
    print_banner()

    print_usage()

    # Check if files exist
    files_ok = check_files()

    # Check environment
    check_environment()

    print("\n🚀 QUICK START:")
    print("1. python3 query_generator.py")
    print("2. python3 reddit_scraper.py")

    if not files_ok:
        print(
            "\n❌ Some required files are missing. Please ensure all files are present."
        )
        sys.exit(1)
    else:
        print("\n✅ All files present. Ready to go!")


if __name__ == "__main__":
    main()
