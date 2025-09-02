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
    def __init__(self, delay_range=(2, 5)):
        """
        Initialize the Google scraper
        
        Args:
            delay_range (tuple): Min and max delay between requests in seconds
        """
        self.delay_range = delay_range
        self.ua = UserAgent()
        self.session = requests.Session()
        
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
    
    def search_google(self, query, num_results=10, start=0):
        """
        Search Google for a specific query
        
        Args:
            query (str): The Google search query
            num_results (int): Number of results to fetch
            start (int): Starting position for results
            
        Returns:
            list: List of dictionaries containing search results
        """
        results = []
        
        try:
            # Update user agent for each request
            self.session.headers.update({'User-Agent': self._get_random_user_agent()})
            
            # Build search URL
            search_url = "https://www.google.com/search"
            params = {
                'q': query,
                'num': num_results,
                'start': start,
                'hl': 'en'
            }
            
            # Make request
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find search result containers
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results:
                try:
                    # Extract title
                    title_elem = result.find('h3')
                    title = title_elem.get_text() if title_elem else "No title"
                    
                    # Extract URL
                    link_elem = result.find('a')
                    url = link_elem.get('href') if link_elem else "No URL"
                    
                    # Extract snippet
                    snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                    if not snippet_elem:
                        snippet_elem = result.find('div', class_=['BNeawe', 's3v9rd'])
                    snippet = snippet_elem.get_text() if snippet_elem else "No snippet"
                    
                    if url and url.startswith('http'):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'query': query
                        })
                        
                except Exception as e:
                    logging.warning(f"Error parsing search result: {e}")
                    continue
            
            # Add delay between requests
            time.sleep(self._get_random_delay())
            
        except requests.RequestException as e:
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
