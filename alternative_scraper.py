"""
Alternative Scraper with Multiple Strategies
Tries different approaches when Google blocks us
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from fake_useragent import UserAgent
import logging

class AlternativeScraper:
    def __init__(self, delay_range=(3, 6)):
        """
        Initialize the alternative scraper with multiple strategies
        
        Args:
            delay_range (tuple): Min and max delay between requests in seconds
        """
        self.delay_range = delay_range
        self.ua = UserAgent()
        self.session = requests.Session()
        self.request_count = 0
        self.last_request_time = 0
        
        # Multiple search engines to try
        self.search_engines = [
            {
                'name': 'Google',
                'url': 'https://www.google.com/search',
                'params_func': self._google_params,
                'parser_func': self._parse_google_results
            },
            {
                'name': 'Bing',
                'url': 'https://www.bing.com/search',
                'params_func': self._bing_params,
                'parser_func': self._parse_bing_results
            },
            {
                'name': 'DuckDuckGo',
                'url': 'https://html.duckduckgo.com/html/',
                'params_func': self._ddg_params,
                'parser_func': self._parse_ddg_results
            }
        ]
        
        # Set up more convincing headers
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })
    
    def _google_params(self, query, num_results, start):
        """Generate Google search parameters"""
        return {
            'q': query,
            'num': min(num_results, 10),
            'start': start,
            'hl': 'en',
            'safe': 'off'
        }
    
    def _bing_params(self, query, num_results, start):
        """Generate Bing search parameters"""
        return {
            'q': query,
            'count': min(num_results, 10),
            'first': start + 1,
            'FORM': 'PERE'
        }
    
    def _ddg_params(self, query, num_results, start):
        """Generate DuckDuckGo search parameters"""
        return {
            'q': query,
            's': start,
            'dc': start + num_results,
            'o': 'json',
            'api': '/d.js'
        }
    
    def _parse_google_results(self, soup):
        """Parse Google search results"""
        results = []
        
        # Try multiple selectors for Google results
        search_results = (
            soup.find_all('div', class_='g') or
            soup.find_all('div', class_='tF2Cxc') or
            soup.find_all('div', class_='rc')
        )
        
        for result in search_results:
            try:
                # Extract title
                title_elem = result.find('h3') or result.find('h1') or result.find('h2')
                title = title_elem.get_text().strip() if title_elem else "No title"
                
                # Extract URL
                link_elem = result.find('a', href=True)
                if link_elem:
                    url = link_elem.get('href')
                    if url.startswith('/url?q='):
                        url = urllib.parse.unquote(url.split('&')[0][7:])
                else:
                    continue
                
                # Extract snippet
                snippet_elem = (
                    result.find('span', class_=['aCOpRe', 'st', 'hgKElc']) or 
                    result.find('div', class_=['BNeawe', 's3v9rd', 'IsZvec'])
                )
                snippet = snippet_elem.get_text().strip() if snippet_elem else "No snippet"
                
                # Only include valid HTTP URLs
                if url and url.startswith('http') and 'google.com' not in url:
                    results.append({
                        'title': title[:200],
                        'url': url,
                        'snippet': snippet[:500]
                    })
                    
            except Exception as e:
                logging.debug(f"Error parsing Google result: {e}")
                continue
        
        return results
    
    def _parse_bing_results(self, soup):
        """Parse Bing search results"""
        results = []
        
        # Bing result selectors
        search_results = soup.find_all('li', class_='b_algo')
        
        for result in search_results:
            try:
                # Extract title and URL
                title_elem = result.find('h2')
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find('a', href=True)
                if not link_elem:
                    continue
                
                title = title_elem.get_text().strip()
                url = link_elem.get('href')
                
                # Extract snippet
                snippet_elem = result.find('p') or result.find('div', class_='b_caption')
                snippet = snippet_elem.get_text().strip() if snippet_elem else "No snippet"
                
                if url and url.startswith('http'):
                    results.append({
                        'title': title[:200],
                        'url': url,
                        'snippet': snippet[:500]
                    })
                    
            except Exception as e:
                logging.debug(f"Error parsing Bing result: {e}")
                continue
        
        return results
    
    def _parse_ddg_results(self, soup):
        """Parse DuckDuckGo search results"""
        results = []
        
        # DuckDuckGo result selectors
        search_results = soup.find_all('div', class_='result')
        
        for result in search_results:
            try:
                # Extract title and URL
                title_elem = result.find('a', class_='result__a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()
                url = title_elem.get('href')
                
                # Extract snippet
                snippet_elem = result.find('a', class_='result__snippet')
                snippet = snippet_elem.get_text().strip() if snippet_elem else "No snippet"
                
                if url and url.startswith('http'):
                    results.append({
                        'title': title[:200],
                        'url': url,
                        'snippet': snippet[:500]
                    })
                    
            except Exception as e:
                logging.debug(f"Error parsing DuckDuckGo result: {e}")
                continue
        
        return results
    
    def _get_random_user_agent(self):
        """Get random user agent string"""
        try:
            return self.ua.random
        except:
            fallback_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            return random.choice(fallback_agents)
    
    def _ensure_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        
        if self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time
            min_delay = self.delay_range[0]
            
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                logging.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Random jitter
        jitter = random.uniform(0.5, 2.0)
        time.sleep(jitter)
    
    def search_alternative(self, query, num_results=10, start=0):
        """
        Search using alternative methods
        
        Args:
            query (str): The search query
            num_results (int): Number of results to fetch
            start (int): Starting position for results
            
        Returns:
            list: List of dictionaries containing search results
        """
        
        all_results = []
        
        for engine in self.search_engines:
            try:
                logging.info(f"Trying {engine['name']} for query: {query}")
                
                # Ensure rate limiting
                self._ensure_rate_limit()
                
                # Update user agent
                self.session.headers.update({'User-Agent': self._get_random_user_agent()})
                
                # Get search parameters
                params = engine['params_func'](query, num_results, start)
                
                # Make request
                response = self.session.get(engine['url'], params=params, timeout=15)
                response.raise_for_status()
                
                # Parse results
                soup = BeautifulSoup(response.content, 'html.parser')
                results = engine['parser_func'](soup)
                
                if results:
                    logging.info(f"{engine['name']} found {len(results)} results")
                    
                    # Add query and source to results
                    for result in results:
                        result['query'] = query
                        result['source'] = engine['name']
                    
                    all_results.extend(results)
                    
                    # If we get results, break (don't need to try other engines)
                    break
                else:
                    logging.info(f"{engine['name']} returned no results")
                    
            except Exception as e:
                logging.warning(f"{engine['name']} failed: {e}")
                continue
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        return unique_results[:num_results]
    
    def search_multiple_queries(self, queries, max_results_per_query=10, progress_callback=None):
        """
        Search multiple queries using alternative methods
        
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
                
            results = self.search_alternative(query, max_results_per_query)
            all_results[query] = results
            
            logging.info(f"Completed query {i + 1}/{len(queries)}: {query} - {len(results)} results")
            
        return all_results
