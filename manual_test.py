"""
Manual Test - Direct Google Search for Daytona Login
Let's see exactly what we get back from Google
"""

import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

def manual_google_test():
    """Manually test Google search for daytona login"""
    
    # Create a session with the most basic, human-like request possible
    session = requests.Session()
    ua = UserAgent()
    
    # Use very simple headers - like a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Test the exact query we know works manually
    queries_to_test = [
        'site:daytona.co.za login',
        'daytona.co.za login',
        'site:daytona.co.za "log in"'
    ]
    
    print("Manual Google Test - Daytona Login Search")
    print("=" * 50)
    
    for query in queries_to_test:
        print(f"\nTesting: {query}")
        print("-" * 30)
        
        try:
            # Build URL exactly like manual search
            search_url = "https://www.google.com/search"
            params = {
                'q': query,
                'hl': 'en'
            }
            
            print(f"Request URL: {search_url}")
            print(f"Parameters: {params}")
            
            # Make the request
            response = session.get(search_url, params=params, timeout=30)
            print(f"Response Status: {response.status_code}")
            print(f"Response URL: {response.url}")
            
            if response.status_code == 200:
                # Save the raw HTML to see what we actually got
                with open(f'google_response_{query.replace(":", "_").replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✓ Response saved to file")
                
                # Parse and look for results
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check if we got blocked
                if 'captcha' in response.text.lower() or 'unusual traffic' in response.text.lower():
                    print("❌ BLOCKED - Google is showing captcha/block page")
                    continue
                
                # Look for search results using various selectors
                selectors_to_try = [
                    'div.g',
                    'div.tF2Cxc', 
                    'div.rc',
                    'div[data-ved]',
                    'h3',
                    'a[href*="daytona.co.za"]'
                ]
                
                found_results = False
                for selector in selectors_to_try:
                    elements = soup.select(selector)
                    if elements:
                        print(f"✓ Found {len(elements)} elements with selector: {selector}")
                        found_results = True
                        
                        # Show first few results
                        for i, elem in enumerate(elements[:3]):
                            print(f"  {i+1}. {elem.get_text()[:100]}...")
                    else:
                        print(f"❌ No elements found with selector: {selector}")
                
                # Look specifically for daytona.co.za links
                daytona_links = soup.find_all('a', href=lambda x: x and 'daytona.co.za' in x)
                if daytona_links:
                    print(f"✓ Found {len(daytona_links)} daytona.co.za links:")
                    for i, link in enumerate(daytona_links[:5]):
                        print(f"  {i+1}. {link.get('href')}")
                        print(f"      Text: {link.get_text()[:50]}...")
                else:
                    print("❌ No daytona.co.za links found")
                    
                if not found_results:
                    print("❌ NO SEARCH RESULTS FOUND - Possible parsing issue")
                    # Let's see what we actually got
                    print("First 500 characters of response:")
                    print(response.text[:500])
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)
        time.sleep(5)  # Wait between queries
    
    print("\nManual test completed!")

if __name__ == "__main__":
    manual_google_test()
