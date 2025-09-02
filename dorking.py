"""
Google Dorking Engine
Provides a unified interface for performing Google dork searches with multiple fallback methods
"""

import logging
import time
import random
from scraper import GoogleScraper
from alternative_scraper import AlternativeScraper
from google_dorks import get_all_dorks_for_domain, GOOGLE_DORKS

class DorkingEngine:
    def __init__(self, delay_range=(1, 2), max_results=10):
        """
        Initialize the dorking engine with multiple scrapers
        
        Args:
            delay_range (tuple): Min and max delay between requests
            max_results (int): Maximum results per query
        """
        self.delay_range = delay_range
        self.max_results = max_results
        
        # Initialize scrapers
        self.google_scraper = GoogleScraper(delay_range=delay_range)
        self.alternative_scraper = AlternativeScraper(delay_range=delay_range)
        
        # Stats
        self.google_success = 0
        self.google_failures = 0
        self.fallbacks_used = 0
        
    def search(self, query, use_fallbacks=True):
        """
        Search using Google with fallbacks if needed
        
        Args:
            query (str): The search query (Google dork)
            use_fallbacks (bool): Whether to use fallback scrapers on failure
            
        Returns:
            list: Search results
        """
        logging.info(f"Searching: {query}")
        
        # Try Google search first
        try:
            results = self.google_scraper.search_google(query, self.max_results)
            
            if results:
                self.google_success += 1
                return results
        except Exception as e:
            logging.error(f"Google search failed: {e}")
            self.google_failures += 1
        
        # If Google search failed or returned no results, try fallbacks
        if use_fallbacks:
            logging.info(f"Trying alternative search engines for: {query}")
            self.fallbacks_used += 1
            
            try:
                fallback_results = self.alternative_scraper.search(query, self.max_results)
                if fallback_results:
                    return fallback_results
            except Exception as e:
                logging.error(f"Alternative search failed: {e}")
        
        # Return empty list if all methods failed
        return []
    
    def batch_search(self, queries, use_fallbacks=True):
        """
        Search for multiple queries at once, with delay between each
        
        Args:
            queries (list): List of search queries
            use_fallbacks (bool): Whether to use fallback scrapers
            
        Returns:
            dict: Results for each query
        """
        results = {}
        
        for query in queries:
            results[query] = self.search(query, use_fallbacks)
            
            # Add delay between queries
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
        
        return results
    
    def get_all_dork_queries(self):
        """
        Get all available dork queries (without domain formatting)
        
        Returns:
            dict: Categories and their dork queries
        """
        return GOOGLE_DORKS
    
    def get_status(self):
        """
        Get status of dorking engine
        
        Returns:
            dict: Status information
        """
        return {
            'google_success': self.google_success,
            'google_failures': self.google_failures,
            'fallbacks_used': self.fallbacks_used,
            'google_success_rate': self.google_success / (self.google_success + self.google_failures) * 100 if (self.google_success + self.google_failures) > 0 else 0
        }
