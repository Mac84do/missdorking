"""
Debug Script to Test Specific Google Searches
"""

import sys
import logging
from scraper import GoogleScraper
from analysis import ResultAnalyzer

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_daytona_searches():
    """Test specific searches for daytona.co.za"""
    
    scraper = GoogleScraper(delay_range=(2, 4))  # Use longer delays for manual testing
    analyzer = ResultAnalyzer()
    
    # Test queries that should find the login page
    test_queries = [
        'site:daytona.co.za login',
        'site:daytona.co.za "log in"',
        'site:daytona.co.za inurl:login',
        'site:daytona.co.za account',
        'daytona.co.za login',
        # Original complex query
        'site:daytona.co.za (inurl:login OR inurl:signin OR inurl:admin OR inurl:administrator OR inurl:dashboard OR inurl:auth)'
    ]
    
    print("Testing Google searches for daytona.co.za login detection...")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing query: {query}")
        print("-" * 50)
        
        try:
            results = scraper.search_google(query, num_results=5)
            
            if results:
                print(f"✓ Found {len(results)} results:")
                for j, result in enumerate(results, 1):
                    print(f"  {j}. Title: {result['title']}")
                    print(f"     URL: {result['url']}")
                    print(f"     Snippet: {result['snippet'][:100]}...")
                    
                    # Analyze the result
                    analyzed = analyzer.analyze_result(result.copy())
                    analysis = analyzed['analysis']
                    
                    if 'login_page' in analysis['categories']:
                        print(f"     🎯 DETECTED as login page! (Risk: {analysis['risk_level']}, Score: {analysis['confidence_score']})")
                    else:
                        print(f"     ❌ Not detected as login page")
                    print()
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Add delay between queries
        import time
        time.sleep(3)
    
    print("\n" + "=" * 60)
    print("Debug test completed!")

if __name__ == "__main__":
    test_daytona_searches()
