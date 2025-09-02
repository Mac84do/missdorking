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
    def __init__(self, delay_range=(0.1, 0.3)):
        """
        Initialize hybrid scraper with multiple strategies
        OPTIMIZED FOR LUDICROUS SPEED! 🚀
        
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
            
            response = self.session.get(base_url, timeout=8)  # Faster timeout
            
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
                        })
                        
                        logging.info(f"Found login link on homepage: {text} -> {full_url}")
                        
        except Exception as e:
            logging.warning(f"Error analyzing homepage {base_url}: {e}")
        
        return results
    
    def _check_common_login_paths(self, base_url):
        """Check common login paths directly"""
        results = []
        domain = urlparse(base_url).netloc
        
        for path in self.common_login_paths:
            try:
                self._ensure_rate_limit()
                
                full_url = base_url.rstrip('/') + path
                logging.info(f"Checking path: {full_url}")
                
                response = self.session.get(full_url, timeout=5, allow_redirects=True)  # Super fast timeout
                
                # Consider it a valid login page if:
                # 1. Status code is 200 (OK)
                # 2. Status code is 401/403 (requires auth - often login pages)
                # 3. Contains login-related content
                
                if response.status_code in [200, 401, 403]:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Get page title
                    title_elem = soup.find('title')
                    page_title = title_elem.get_text().strip() if title_elem else f"Login Page - {domain}"
                    
                    # Look for login indicators in the content
                    page_text = soup.get_text().lower()
                    login_indicators = [
                        'password', 'username', 'email', 'sign in', 'log in',
                        'login', 'authentication', 'admin', 'dashboard'
                    ]
                    
                    found_indicators = [indicator for indicator in login_indicators if indicator in page_text]
                    
                    # Look for form fields that suggest login
                    forms = soup.find_all('form')
                    has_login_form = False
                    
                    for form in forms:
                        inputs = form.find_all('input')
                        input_types = [inp.get('type', '').lower() for inp in inputs]
                        input_names = [inp.get('name', '').lower() for inp in inputs]
                        
                        if ('password' in input_types or 
                            any(name in ['password', 'username', 'email', 'user'] for name in input_names)):
                            has_login_form = True
                            break
                    
                    # If we found login indicators or forms, consider it a login page
                    if found_indicators or has_login_form or response.status_code in [401, 403]:
                        results.append({
                            'title': page_title,
                            'url': response.url,  # Use final URL after redirects
                            'snippet': f"Direct path check found login page. Status: {response.status_code}, Indicators: {', '.join(found_indicators[:3])}, Has form: {has_login_form}",
                            'query': f'direct path check: {path}',
                            'source': 'Direct Path Check',
                            'method': 'path_checking'
                        })
                        
                        logging.info(f"Found login page at {full_url} -> {response.url}")
                
            except Exception as e:
                logging.debug(f"Error checking path {path}: {e}")
                continue
        
        return results
