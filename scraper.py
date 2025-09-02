"""
Google Search Scraper Module
Handles safe web scraping with proper delays and error handling
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from fake_useragent import UserAgent
import logging

class GoogleScraper:
    def __init__(self, delay_range=(1, 3)):
        """
        Initialize the Google scraper
        
        Args:
            delay_range (tuple): Min and max delay between requests in seconds
        """
        self.delay_range = delay_range
        self.ua = UserAgent()
        self.session = requests.Session()
        self.request_count = 0
        self.last_request_time = 0
        self.blocked_count = 0
        
        # Set up headers to mimic a real browser
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def _get_random_delay(self):
        """Get random delay between requests"""
        return random.uniform(self.delay_range[0], self.delay_range[1])
        
    def _get_random_user_agent(self):
        """Get random user agent string"""
        try:
            return self.ua.random
        except:
            # Fallback user agents if fake_useragent fails
            fallback_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            return random.choice(fallback_agents)
    
    def _ensure_rate_limit(self):
        """Ensure we don't exceed rate limits with exponential backoff"""
        current_time = time.time()
        
        # Enforce minimum delay between requests
        if self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time
            min_delay = self.delay_range[0]
            
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                logging.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Exponential backoff after many requests
        if self.request_count > 10:
            extra_delay = min(30, (self.request_count - 10) * 2)  # Max 30 seconds extra
            logging.info(f"Exponential backoff: extra {extra_delay} seconds after {self.request_count} requests")
            time.sleep(extra_delay)
    
    def _detect_google_block(self, response_text):
        """Detect if Google is blocking or showing captcha"""
        block_indicators = [
            'captcha',
            'unusual traffic',
            'automated queries',
            'blocked',
            'verify you are human',
            'our systems have detected unusual traffic',
            'sorry, but your computer or network',
            'distil_r_blocked',
            'access denied'
        ]
        
        text_lower = response_text.lower()
        for indicator in block_indicators:
            if indicator in text_lower:
                return True
        return False
    
    def search_google(self, query, num_results=10, start=0, retry_count=0):
        """
        Search Google for a specific query with retry logic
        
        Args:
            query (str): The Google search query
            num_results (int): Number of results to fetch
            start (int): Starting position for results
            retry_count (int): Current retry attempt
            
        Returns:
            list: List of dictionaries containing search results
        """
        results = []
        max_retries = 3
        
        try:
            # Enforce rate limiting
            self._ensure_rate_limit()
            
            # Update user agent for each request
            self.session.headers.update({'User-Agent': self._get_random_user_agent()})
            
            # Build search URL
            search_url = "https://www.google.com/search"
            params = {
                'q': query,
                'num': min(num_results, 10),  # Limit to 10 results max
                'start': start,
                'hl': 'en',
                'safe': 'off'
            }
            
            logging.info(f"Searching: {query} (attempt {retry_count + 1})")
            
            # Make request
            response = self.session.get(search_url, params=params, timeout=15)
            
            if response.status_code == 429:  # Too Many Requests
                if retry_count < max_retries:
                    backoff_time = (2 ** retry_count) * 10  # 10, 20, 40 seconds
                    logging.warning(f"Rate limited! Backing off for {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    return self.search_google(query, num_results, start, retry_count + 1)
                else:
                    logging.error(f"Max retries exceeded for query: {query}")
                    return results
            
            response.raise_for_status()
            
            # Check for block indicators in response
            if self._detect_google_block(response.text):
                self.blocked_count += 1
                if retry_count < max_retries:
                    backoff_time = (2 ** retry_count) * 20  # Longer backoff for blocks
                    logging.warning(f"Google block detected! Backing off for {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    return self.search_google(query, num_results, start, retry_count + 1)
                else:
                    logging.error(f"Max retries exceeded due to blocks for query: {query}")
                    return results
            
            # Parse results
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find search result containers (try multiple selectors)
            search_results = (
                soup.find_all('div', class_='g') or
                soup.find_all('div', class_='tF2Cxc') or
                soup.find_all('div', class_='rc') or
                soup.find_all('div', {'class': lambda x: x and 'g' in x}) or
                soup.find_all('div', {'data-ved': True})
            )
            
            # If no results found with div selectors, try broader search
            if not search_results:
                search_results = soup.find_all('a', href=True)
                # Filter to only include relevant links
                filtered_results = []
                for link in search_results:
                    href = link.get('href', '')
                    if href.startswith('http') and 'google.com' not in href:
                        parent = link.find_parent('div')
                        if parent:
                            filtered_results.append(parent)
                search_results = filtered_results[:20]  # Limit to first 20
            
            for result in search_results:
                try:
                    # Extract title (try multiple selectors)
                    title_elem = (
                        result.find('h3') or
                        result.find('h1') or
                        result.find('h2') or
                        result.find('a', href=True)
                    )
                    
                    if title_elem:
                        title = title_elem.get_text().strip()
                    else:
                        title = "No title"
                    
                    # Extract URL (try multiple approaches)
                    link_elem = result.find('a', href=True)
                    if link_elem:
                        url = link_elem.get('href')
                        # Clean up Google redirect URLs
                        if url.startswith('/url?q='):
                            url = urllib.parse.unquote(url.split('&')[0][7:])
                    else:
                        url = "No URL"
                    
                    # Extract snippet (try multiple selectors)
                    snippet_elem = (
                        result.find('span', class_=['aCOpRe', 'st', 'hgKElc']) or 
                        result.find('div', class_=['BNeawe', 's3v9rd', 'IsZvec']) or
                        result.find('span', {'data-ved': True}) or
                        result.find('div', string=True)
                    )
                    
                    if snippet_elem:
                        snippet = snippet_elem.get_text().strip()
                    else:
                        snippet = "No snippet"
                    
                    # Only include valid HTTP URLs that are not Google URLs
                    if (url and url.startswith('http') and len(url) > 10 and 
                        'google.com' not in url and 'googleusercontent.com' not in url):
                        
                        results.append({
                            'title': title[:200],  # Limit title length
                            'url': url,
                            'snippet': snippet[:500],  # Limit snippet length
                            'query': query
                        })
                        
                except Exception as e:
                    logging.debug(f"Error parsing search result: {e}")
                    continue
            
            logging.info(f"Found {len(results)} results for: {query}")
            
            # Add final delay
            delay = self._get_random_delay()
            logging.debug(f"Sleeping for {delay:.2f} seconds before next request")
            time.sleep(delay)
            
        except requests.RequestException as e:
            if "429" in str(e) and retry_count < max_retries:
                backoff_time = (2 ** retry_count) * 15
                logging.warning(f"Request error (429), retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                return self.search_google(query, num_results, start, retry_count + 1)
            else:
                logging.error(f"Request error for query '{query}': {e}")
        except Exception as e:
            logging.error(f"Unexpected error for query '{query}': {e}")
            
        return results
    
    def search_multiple_queries(self, queries, max_results_per_query=10, progress_callback=None):
        """
        Search Google for multiple queries
        
        Args:
            queries (list): List of search queries
            max_results_per_query (int): Maximum results per query
            progress_callback (function): Callback function to report progress
            
        Returns:
            dict: Dictionary with queries as keys and results as values
        """
        all_results = {}
        
        for i, query in enumerate(queries):
            if progress_callback:
                progress_callback(i + 1, len(queries), query)
                
            results = self.search_google(query, max_results_per_query)
            all_results[query] = results
            
            logging.info(f"Completed query {i + 1}/{len(queries)}: {query} - {len(results)} results")
            
        return all_results
    
    def get_total_results_count(self, query):
        """
        Get total number of results for a query (approximate)
        
        Args:
            query (str): The search query
            
        Returns:
            str: Total results count as string
        """
        try:
            self.session.headers.update({'User-Agent': self._get_random_user_agent()})
            
            search_url = "https://www.google.com/search"
            params = {'q': query, 'hl': 'en'}
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for results count
            stats_elem = soup.find('div', {'id': 'result-stats'})
            if stats_elem:
                return stats_elem.get_text()
            
            time.sleep(self._get_random_delay())
            
        except Exception as e:
            logging.error(f"Error getting results count for '{query}': {e}")
            
        return "Unknown"
