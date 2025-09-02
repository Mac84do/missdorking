"""
Bypass Test - Alternative approaches to get search results
"""

import requests
from bs4 import BeautifulSoup
import time
import random

def test_different_approaches():
    """Test different approaches to get search results"""
    
    print("Testing Different Search Approaches")
    print("=" * 50)
    
    # Test 1: Try DuckDuckGo (less aggressive blocking)
    print("\n1. Testing DuckDuckGo...")
    try_duckduckgo()
    
    # Test 2: Try Bing  
    print("\n2. Testing Bing...")
    try_bing()
    
    # Test 3: Try a different Google endpoint
    print("\n3. Testing Google with different parameters...")
    try_google_alternatives()

def try_duckduckgo():
    """Test DuckDuckGo search"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        # DuckDuckGo HTML search
        url = "https://html.duckduckgo.com/html/"
        params = {
            'q': 'site:daytona.co.za login'
        }
        
        response = session.get(url, params=params, timeout=15)
        print(f"DDG Response Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for DuckDuckGo results
            results = soup.find_all('a', class_='result__a')
            if results:
                print(f"✓ Found {len(results)} DuckDuckGo results:")
                for i, result in enumerate(results[:3]):
                    href = result.get('href', '')
                    title = result.get_text().strip()
                    print(f"  {i+1}. {title}")
                    print(f"      {href}")
                    if 'daytona.co.za' in href and ('login' in href.lower() or 'login' in title.lower()):
                        print("      🎯 POTENTIAL LOGIN PAGE FOUND!")
            else:
                print("❌ No DuckDuckGo results found")
                # Let's see what we got
                print("First 300 chars:", response.text[:300])
        
    except Exception as e:
        print(f"❌ DuckDuckGo error: {e}")

def try_bing():
    """Test Bing search"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        url = "https://www.bing.com/search"
        params = {
            'q': 'site:daytona.co.za login'
        }
        
        response = session.get(url, params=params, timeout=15)
        print(f"Bing Response Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Bing results
            results = soup.find_all('li', class_='b_algo')
            if results:
                print(f"✓ Found {len(results)} Bing results:")
                for i, result in enumerate(results[:3]):
                    title_elem = result.find('h2')
                    if title_elem:
                        link_elem = title_elem.find('a')
                        if link_elem:
                            title = title_elem.get_text().strip()
                            href = link_elem.get('href', '')
                            print(f"  {i+1}. {title}")
                            print(f"      {href}")
                            if 'daytona.co.za' in href and ('login' in href.lower() or 'login' in title.lower()):
                                print("      🎯 POTENTIAL LOGIN PAGE FOUND!")
            else:
                print("❌ No Bing results found")
                print("First 300 chars:", response.text[:300])
        
    except Exception as e:
        print(f"❌ Bing error: {e}")

def try_google_alternatives():
    """Try Google with different approaches"""
    session = requests.Session()
    
    # Try with minimal headers and different user agent
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    for ua in user_agents:
        print(f"Trying with User-Agent: {ua[:50]}...")
        
        session.headers.clear()
        session.headers.update({
            'User-Agent': ua
        })
        
        try:
            # Wait longer between attempts
            time.sleep(random.randint(10, 20))
            
            url = "https://www.google.com/search"
            params = {
                'q': 'daytona.co.za login',  # Simpler query
                'hl': 'en',
                'safe': 'off'
            }
            
            response = session.get(url, params=params, timeout=15)
            print(f"Google Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ Success! Got Google response")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for any daytona.co.za links
                all_links = soup.find_all('a', href=True)
                daytona_links = [link for link in all_links if 'daytona.co.za' in link.get('href', '')]
                
                if daytona_links:
                    print(f"✓ Found {len(daytona_links)} daytona.co.za links:")
                    for i, link in enumerate(daytona_links[:5]):
                        href = link.get('href', '')
                        text = link.get_text().strip()
                        print(f"  {i+1}. {text[:50]}")
                        print(f"      {href}")
                        if 'login' in href.lower() or 'login' in text.lower():
                            print("      🎯 POTENTIAL LOGIN PAGE FOUND!")
                else:
                    print("❌ No daytona.co.za links found")
                break
                
            elif response.status_code == 429:
                print("❌ Still rate limited")
                
        except Exception as e:
            print(f"❌ Google alternative error: {e}")

def test_direct_site_check():
    """Test direct access to daytona.co.za to verify it's accessible"""
    print("\n4. Testing direct access to daytona.co.za...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        response = session.get('https://daytona.co.za', timeout=15)
        print(f"Direct access status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for login-related links on the homepage
            login_keywords = ['login', 'log in', 'signin', 'sign in', 'account', 'member']
            potential_login_links = []
            
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '').lower()
                text = link.get_text().strip().lower()
                
                for keyword in login_keywords:
                    if keyword in href or keyword in text:
                        potential_login_links.append({
                            'text': link.get_text().strip(),
                            'href': link.get('href')
                        })
                        break
            
            if potential_login_links:
                print(f"✓ Found {len(potential_login_links)} potential login links on homepage:")
                for i, link in enumerate(potential_login_links):
                    print(f"  {i+1}. {link['text']}")
                    print(f"      {link['href']}")
            else:
                print("❌ No obvious login links found on homepage")
                
    except Exception as e:
        print(f"❌ Direct access error: {e}")

if __name__ == "__main__":
    test_different_approaches()
    test_direct_site_check()
