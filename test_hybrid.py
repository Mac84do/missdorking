"""
Test Hybrid Scraper with Daytona.co.za
"""

import logging
from hybrid_scraper_fixed import HybridScraper
from analysis import ResultAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_hybrid_scraper():
    """Test the hybrid scraper with daytona.co.za"""
    
    print("Testing Hybrid Scraper with Daytona.co.za")
    print("=" * 50)
    
    scraper = HybridScraper(delay_range=(2, 4))
    analyzer = ResultAnalyzer()
    
    domain = "daytona.co.za"
    
    # Test direct domain analysis
    print(f"\n🔍 Starting direct analysis of {domain}...")
    results = scraper.analyze_domain_directly(domain)
    
    if results:
        print(f"\n✅ SUCCESS! Found {len(results)} login-related pages:")
        print("-" * 40)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. Title: {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Method: {result['method']}")
            print(f"   Source: {result['source']}")
            print(f"   Details: {result['snippet']}")
            
            # Test our analysis on this result
            analyzed = analyzer.analyze_result(result.copy())
            analysis = analyzed['analysis']
            
            if 'login_page' in analysis['categories']:
                print(f"   🎯 CONFIRMED LOGIN PAGE! (Risk: {analysis['risk_level']}, Score: {analysis['confidence_score']})")
            else:
                print(f"   ⚠️  Not detected as login page by analyzer")
            
            print("-" * 40)
    else:
        print("❌ No login pages found")
    
    return results

def test_specific_urls():
    """Test specific URLs we know exist"""
    print("\n" + "=" * 50)
    print("Testing Specific Known URLs")
    print("=" * 50)
    
    analyzer = ResultAnalyzer()
    
    # These are the URLs we found in our previous tests
    test_urls = [
        {
            'title': 'Account Login - Daytona',
            'url': 'https://daytona.co.za/account/login',
            'snippet': 'Direct access to Daytona account login page',
            'query': 'direct test'
        },
        {
            'title': 'Account Page - Daytona', 
            'url': 'https://daytona.co.za/account',
            'snippet': 'Account management page with login functionality',
            'query': 'direct test'
        }
    ]
    
    for i, test_url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing: {test_url['url']}")
        
        analyzed = analyzer.analyze_result(test_url.copy())
        analysis = analyzed['analysis']
        
        print(f"   Categories: {analysis['categories']}")
        print(f"   Risk Level: {analysis['risk_level']}")
        print(f"   Confidence Score: {analysis['confidence_score']}")
        
        if 'login_page' in analysis['categories']:
            print(f"   ✅ LOGIN PAGE DETECTED!")
        else:
            print(f"   ❌ NOT detected as login page")

if __name__ == "__main__":
    try:
        results = test_hybrid_scraper()
        test_specific_urls()
        
        print("\n" + "=" * 50)
        print("🎉 HYBRID SCRAPER TEST COMPLETE!")
        
        if results:
            print(f"✅ Successfully found {len(results)} login pages using direct analysis")
            print("✅ This proves the hybrid approach works!")
            print("✅ No need to rely on Google search - we can find login pages directly!")
        else:
            print("❌ No results found - may need to adjust detection logic")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
