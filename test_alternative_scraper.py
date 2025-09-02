"""
Test Alternative Scraper for Daytona Login Detection
"""

import logging
from alternative_scraper import AlternativeScraper
from analysis import ResultAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_alternative_scraper():
    """Test alternative scraper with daytona.co.za queries"""
    
    scraper = AlternativeScraper(delay_range=(3, 6))
    analyzer = ResultAnalyzer()
    
    # Test queries focused on finding login pages
    test_queries = [
        'site:daytona.co.za login',
        'daytona.co.za login',
        'site:daytona.co.za "log in"',
        'site:daytona.co.za account',
        'daytona.co.za account login'
    ]
    
    print("Testing Alternative Scraper for Daytona Login Detection")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing query: {query}")
        print("-" * 50)
        
        try:
            results = scraper.search_alternative(query, num_results=5)
            
            if results:
                print(f"✓ Found {len(results)} results from {results[0]['source']}:")
                
                login_found = False
                for j, result in enumerate(results, 1):
                    print(f"  {j}. Title: {result['title']}")
                    print(f"     URL: {result['url']}")
                    print(f"     Source: {result['source']}")
                    print(f"     Snippet: {result['snippet'][:80]}...")
                    
                    # Analyze the result
                    analyzed = analyzer.analyze_result(result.copy())
                    analysis = analyzed['analysis']
                    
                    if 'login_page' in analysis['categories']:
                        print(f"     🎯 LOGIN PAGE DETECTED! (Risk: {analysis['risk_level']}, Score: {analysis['confidence_score']})")
                        login_found = True
                    else:
                        print(f"     ❌ Not detected as login page")
                    print()
                
                if login_found:
                    print("🎉 SUCCESS: Login page found and detected!")
                else:
                    print("❌ No login pages detected in results")
                    
            else:
                print("❌ No results found from any search engine")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("=" * 50)
    
    print("\nAlternative scraper test completed!")

if __name__ == "__main__":
    test_alternative_scraper()
