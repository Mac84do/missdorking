"""
Hybrid Scraper - Combines direct site analysis with search engines
Works around Google blocking by using multiple strategies
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from urllib.parse import urljoin, urlparse
import logging

class HybridScraper:
    def __init__(self, delay_range=(2, 5)):
        """
        Initialize hybrid scraper with multiple strategies
        
        Args:
            delay_range (tuple): Min and max delay between requests in seconds
        """
        self.delay_range = delay_range
        self.session = requests.Session()
        self.request_count = 0
        self.last_request_time = 0
        
        # Common login paths to check directly
        self.common_login_paths = [
            '/login',
            '/signin',
            '/sign-in', 
            '/account/login',
            '/account',
            '/admin',
            '/administrator',
            '/dashboard',
            '/wp-admin',
            '/wp-login.php',
            '/user/login',
            '/auth',
            '/authentication',
            '/portal',
            '/member',
            '/customer/login',
            '/client/login'
        ]
        
        # Set up headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def _get_random_delay(self):
        """Get random delay between requests"""
        return random.uniform(self.delay_range[0], self.delay_range[1])
    
    def _ensure_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        
        if self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time
            min_delay = self.delay_range[0]
            
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def analyze_domain_directly(self, domain):
        """
        Analyze a domain directly by checking common login paths
        and parsing the homepage for login links
        
        Args:
            domain (str): Domain to analyze
            
        Returns:
            list: List of found login pages with details
        """
        results = []
        base_url = f"https://{domain}"
        
        logging.info(f"Starting direct analysis of {domain}")
        
        # Step 1: Check homepage for login links
        homepage_results = self._analyze_homepage(base_url)
        results.extend(homepage_results)
        
        # Step 2: Check common login paths
        path_results = self._check_common_login_paths(base_url)
        results.extend(path_results)
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        
        for result in results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        logging.info(f"Direct analysis found {len(unique_results)} unique results")
        return unique_results
    
    def _analyze_homepage(self, base_url):
        """Analyze homepage for login links"""
        results = []
        
        try:
            self._ensure_rate_limit()
            logging.info(f"Analyzing homepage: {base_url}")
            
            response = self.session.get(base_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for login-related links
                login_keywords = [
                    'login', 'log in', 'log-in',
                    'signin', 'sign in', 'sign-in',
                    'account', 'my account',
                    'member', 'member login',
                    'admin', 'administrator',
                    'dashboard', 'portal'
                ]
                
                all_links = soup.find_all('a', href=True)
                
                for link in all_links:
                    href = link.get('href', '').strip()
                    text = link.get_text().strip()
                    
                    # Skip empty or invalid links
                    if not href or href.startswith('#'):
                        continue
                    
                    # Convert relative URLs to absolute
                    full_url = urljoin(base_url, href)
                    
                    # Check if this looks like a login link
                    href_lower = href.lower()
                    text_lower = text.lower()
                    
                    is_login_link = False
                    matched_keyword = None
                    
                    for keyword in login_keywords:
                        if keyword in href_lower or keyword in text_lower:
                            is_login_link = True
                            matched_keyword = keyword
                            break
                    
                    if is_login_link:
                        results.append({
                            'title': f"{text} - {urlparse(base_url).netloc}",
                            'url': full_url,
                            'snippet': f"Login link found on homepage. Link text: '{text}', matched keyword: '{matched_keyword}'",
                            'query': f'homepage analysis',
                            'source': 'Direct Analysis',
                            'method': 'homepage_parsing'
                        })\
                        \n                logging.info(f\"Found login link on homepage: {text} -> {full_url}\")\n                        \n        except Exception as e:\n            logging.warning(f\"Error analyzing homepage {base_url}: {e}\")\n        \n        return results\n    \n    def _check_common_login_paths(self, base_url):\n        \"\"\"Check common login paths directly\"\"\"\n        results = []\n        domain = urlparse(base_url).netloc\n        \n        for path in self.common_login_paths:\n            try:\n                self._ensure_rate_limit()\n                \n                full_url = base_url.rstrip('/') + path\n                logging.info(f\"Checking path: {full_url}\")\n                \n                response = self.session.get(full_url, timeout=10, allow_redirects=True)\n                \n                # Consider it a valid login page if:\n                # 1. Status code is 200 (OK)\n                # 2. Status code is 401/403 (requires auth - often login pages)\n                # 3. Contains login-related content\n                \n                if response.status_code in [200, 401, 403]:\n                    soup = BeautifulSoup(response.content, 'html.parser')\n                    \n                    # Get page title\n                    title_elem = soup.find('title')\n                    page_title = title_elem.get_text().strip() if title_elem else f\"Login Page - {domain}\"\n                    \n                    # Look for login indicators in the content\n                    page_text = soup.get_text().lower()\n                    login_indicators = [\n                        'password', 'username', 'email', 'sign in', 'log in',\n                        'login', 'authentication', 'admin', 'dashboard'\n                    ]\n                    \n                    found_indicators = [indicator for indicator in login_indicators if indicator in page_text]\n                    \n                    # Look for form fields that suggest login\n                    forms = soup.find_all('form')\n                    has_login_form = False\n                    \n                    for form in forms:\n                        inputs = form.find_all('input')\n                        input_types = [inp.get('type', '').lower() for inp in inputs]\n                        input_names = [inp.get('name', '').lower() for inp in inputs]\n                        \n                        if ('password' in input_types or \n                            any(name in ['password', 'username', 'email', 'user'] for name in input_names)):\n                            has_login_form = True\n                            break\n                    \n                    # If we found login indicators or forms, consider it a login page\n                    if found_indicators or has_login_form or response.status_code in [401, 403]:\n                        results.append({\n                            'title': page_title,\n                            'url': response.url,  # Use final URL after redirects\n                            'snippet': f\"Direct path check found login page. Status: {response.status_code}, Indicators: {', '.join(found_indicators[:3])}, Has form: {has_login_form}\",\n                            'query': f'direct path check: {path}',\n                            'source': 'Direct Path Check',\n                            'method': 'path_checking'\n                        })\n                        \n                        logging.info(f\"Found login page at {full_url} -> {response.url}\")\n                \n            except Exception as e:\n                logging.debug(f\"Error checking path {path}: {e}\")\n                continue\n        \n        return results\n    \n    def search_with_fallback(self, query, num_results=10):\n        \"\"\"\n        Search using multiple engines as fallback\n        \n        Args:\n            query (str): Search query\n            num_results (int): Number of results desired\n            \n        Returns:\n            list: Combined results from available search engines\n        \"\"\"\n        all_results = []\n        \n        # Try DuckDuckGo first (more reliable)\n        try:\n            ddg_results = self._search_duckduckgo(query, num_results)\n            if ddg_results:\n                logging.info(f\"DuckDuckGo found {len(ddg_results)} results\")\n                all_results.extend(ddg_results)\n        except Exception as e:\n            logging.warning(f\"DuckDuckGo search failed: {e}\")\n        \n        # Try Bing if we need more results\n        if len(all_results) < num_results:\n            try:\n                bing_results = self._search_bing(query, num_results - len(all_results))\n                if bing_results:\n                    logging.info(f\"Bing found {len(bing_results)} results\")\n                    all_results.extend(bing_results)\n            except Exception as e:\n                logging.warning(f\"Bing search failed: {e}\")\n        \n        # Remove duplicates\n        unique_results = []\n        seen_urls = set()\n        \n        for result in all_results:\n            if result['url'] not in seen_urls:\n                unique_results.append(result)\n                seen_urls.add(result['url'])\n        \n        return unique_results[:num_results]\n    \n    def _search_duckduckgo(self, query, num_results):\n        \"\"\"Search DuckDuckGo\"\"\"\n        results = []\n        \n        self._ensure_rate_limit()\n        \n        url = \"https://html.duckduckgo.com/html/\"\n        params = {'q': query}\n        \n        response = self.session.get(url, params=params, timeout=15)\n        \n        if response.status_code == 200:\n            soup = BeautifulSoup(response.content, 'html.parser')\n            \n            # DuckDuckGo result parsing\n            result_links = soup.find_all('a', class_='result__a')\n            \n            for link in result_links:\n                href = link.get('href', '')\n                title = link.get_text().strip()\n                \n                # Extract actual URL from DuckDuckGo redirect\n                if href.startswith('//duckduckgo.com/l/'):\n                    # Parse the actual URL from the redirect\n                    import re\n                    url_match = re.search(r'uddg=([^&]+)', href)\n                    if url_match:\n                        actual_url = urllib.parse.unquote(url_match.group(1))\n                        if actual_url.startswith('http'):\n                            href = actual_url\n                \n                # Find snippet\n                snippet_elem = link.find_next('a', class_='result__snippet')\n                snippet = snippet_elem.get_text().strip() if snippet_elem else \"No snippet available\"\n                \n                if href and href.startswith('http'):\n                    results.append({\n                        'title': title,\n                        'url': href,\n                        'snippet': snippet,\n                        'query': query,\n                        'source': 'DuckDuckGo'\n                    })\n        \n        return results\n    \n    def _search_bing(self, query, num_results):\n        \"\"\"Search Bing\"\"\"\n        results = []\n        \n        self._ensure_rate_limit()\n        \n        url = \"https://www.bing.com/search\"\n        params = {'q': query}\n        \n        response = self.session.get(url, params=params, timeout=15)\n        \n        if response.status_code == 200:\n            soup = BeautifulSoup(response.content, 'html.parser')\n            \n            # Bing result parsing\n            result_items = soup.find_all('li', class_='b_algo')\n            \n            for item in result_items:\n                title_elem = item.find('h2')\n                if title_elem:\n                    link_elem = title_elem.find('a', href=True)\n                    if link_elem:\n                        title = title_elem.get_text().strip()\n                        href = link_elem.get('href')\n                        \n                        # Find snippet\n                        snippet_elem = item.find('p') or item.find('div', class_='b_caption')\n                        snippet = snippet_elem.get_text().strip() if snippet_elem else \"No snippet available\"\n                        \n                        if href and href.startswith('http'):\n                            results.append({\n                                'title': title,\n                                'url': href,\n                                'snippet': snippet,\n                                'query': query,\n                                'source': 'Bing'\n                            })\n        \n        return results\n    \n    def comprehensive_domain_analysis(self, domain, max_results_per_query=5):\n        \"\"\"\n        Perform comprehensive analysis combining direct checks and search engines\n        \n        Args:\n            domain (str): Domain to analyze\n            max_results_per_query (int): Max results per search query\n            \n        Returns:\n            dict: Analysis results organized by method\n        \"\"\"\n        results = {\n            'direct_analysis': [],\n            'search_results': {},\n            'summary': {}\n        }\n        \n        logging.info(f\"Starting comprehensive analysis of {domain}\")\n        \n        # 1. Direct domain analysis\n        direct_results = self.analyze_domain_directly(domain)\n        results['direct_analysis'] = direct_results\n        \n        # 2. Search engine queries (if available)\n        search_queries = [\n            f'site:{domain} login',\n            f'site:{domain} \"log in\"',\n            f'site:{domain} admin',\n            f'site:{domain} account',\n            f'{domain} login portal'\n        ]\n        \n        for query in search_queries:\n            try:\n                search_results = self.search_with_fallback(query, max_results_per_query)\n                if search_results:\n                    results['search_results'][query] = search_results\n                    logging.info(f\"Search query '{query}' found {len(search_results)} results\")\n                else:\n                    results['search_results'][query] = []\n                    logging.info(f\"Search query '{query}' found no results\")\n            except Exception as e:\n                logging.warning(f\"Search query '{query}' failed: {e}\")\n                results['search_results'][query] = []\n        \n        # 3. Generate summary\n        all_found_results = direct_results.copy()\n        for query_results in results['search_results'].values():\n            all_found_results.extend(query_results)\n        \n        # Remove duplicates for summary\n        unique_urls = set()\n        unique_results = []\n        for result in all_found_results:\n            if result['url'] not in unique_urls:\n                unique_results.append(result)\n                unique_urls.add(result['url'])\n        \n        results['summary'] = {\n            'total_unique_results': len(unique_results),\n            'direct_analysis_results': len(direct_results),\n            'search_engine_results': sum(len(r) for r in results['search_results'].values()),\n            'unique_results': unique_results\n        }\n        \n        logging.info(f\"Comprehensive analysis complete. Found {len(unique_results)} unique results\")\n        return results
