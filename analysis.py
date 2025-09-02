"""
Result Analysis Module
Enhanced analysis and categorization of search results with better login/admin detection
"""

import re
from urllib.parse import urlparse

class ResultAnalyzer:
    def __init__(self):
        self.login_keywords = {
            'url_patterns': [
                r'/login', r'/signin', r'/sign-in', r'/auth', r'/authentication',
                r'/admin', r'/administrator', r'/dashboard', r'/control',
                r'/panel', r'/console', r'/manager', r'/portal',
                r'/wp-admin', r'/wp-login', r'/user', r'/account',
                r'/secure', r'/private', r'/restricted'
            ],
            'title_patterns': [
                r'login', r'sign in', r'sign-in', r'log in', r'log-in',
                r'admin', r'administrator', r'dashboard', r'control panel',
                r'management', r'manager', r'portal', r'console',
                r'authentication', r'auth', r'access', r'secure area'
            ],
            'content_patterns': [
                r'username', r'password', r'email', r'login form',
                r'sign in', r'log in', r'admin panel', r'dashboard',
                r'authentication required', r'please login', r'login page',
                r'member login', r'user login', r'admin login'
            ]
        }
        
        self.sensitive_keywords = {
            'config_files': [
                '.env', 'config.php', 'web.config', '.htaccess',
                'database.yml', 'settings.yml', 'app.config'
            ],
            'database_indicators': [
                'mysql', 'postgresql', 'mongodb', 'database',
                'sql', 'db', 'dump', 'backup'
            ],
            'error_indicators': [
                'error', 'exception', 'warning', 'fatal',
                'stack trace', 'debug', 'mysql error'
            ],
            'credentials': [
                'password', 'passwd', 'api_key', 'secret',
                'token', 'auth_token', 'access_token'
            ]
        }
    
    def analyze_result(self, result):
        """
        Analyze a single search result for security relevance
        
        Args:
            result (dict): Search result with title, url, snippet, query
            
        Returns:
            dict: Enhanced result with analysis
        """
        analysis = {
            'risk_level': 'low',
            'categories': [],
            'login_indicators': [],
            'sensitive_content': [],
            'confidence_score': 0
        }
        
        title = result.get('title', '').lower()
        url = result.get('url', '').lower()
        snippet = result.get('snippet', '').lower()
        
        # Analyze for login/admin pages
        login_score = self._analyze_login_indicators(title, url, snippet)
        if login_score > 0:
            analysis['categories'].append('login_page')
            analysis['confidence_score'] += login_score
            if login_score >= 3:
                analysis['risk_level'] = 'high'
            elif login_score >= 2:
                analysis['risk_level'] = 'medium'
        
        # Analyze for sensitive files
        sensitive_score = self._analyze_sensitive_content(title, url, snippet)
        if sensitive_score > 0:
            analysis['categories'].append('sensitive_file')
            analysis['confidence_score'] += sensitive_score
            if sensitive_score >= 2:
                analysis['risk_level'] = 'high'
        
        # Analyze for configuration exposure
        config_score = self._analyze_config_exposure(title, url, snippet)
        if config_score > 0:
            analysis['categories'].append('config_exposure')
            analysis['confidence_score'] += config_score
            if config_score >= 2:
                analysis['risk_level'] = 'high'
        
        # Analyze for directory listings
        if self._is_directory_listing(title, url, snippet):
            analysis['categories'].append('directory_listing')
            analysis['confidence_score'] += 2
            analysis['risk_level'] = 'medium'
        
        # Analyze for error pages
        if self._contains_error_info(title, url, snippet):
            analysis['categories'].append('error_page')
            analysis['confidence_score'] += 1
        
        # Update result with analysis
        result['analysis'] = analysis
        return result
    
    def _analyze_login_indicators(self, title, url, snippet):
        """Analyze for login page indicators"""
        score = 0
        indicators = []
        
        # Check URL patterns (strongest indicator)
        for pattern in self.login_keywords['url_patterns']:
            if re.search(pattern, url):
                score += 2
                indicators.append(f"URL contains: {pattern}")
        
        # Check title patterns
        for pattern in self.login_keywords['title_patterns']:
            if re.search(pattern, title):
                score += 1.5
                indicators.append(f"Title contains: {pattern}")
        
        # Check content patterns
        for pattern in self.login_keywords['content_patterns']:
            if re.search(pattern, snippet):
                score += 1
                indicators.append(f"Content contains: {pattern}")
        
        return score
    
    def _analyze_sensitive_content(self, title, url, snippet):
        """Analyze for sensitive content indicators"""
        score = 0
        
        # Check for credential-related content
        for keyword in self.sensitive_keywords['credentials']:
            if keyword in title or keyword in url or keyword in snippet:
                score += 1.5
        
        # Check for database indicators
        for keyword in self.sensitive_keywords['database_indicators']:
            if keyword in title or keyword in url or keyword in snippet:
                score += 1
        
        return score
    
    def _analyze_config_exposure(self, title, url, snippet):
        """Analyze for configuration file exposure"""
        score = 0
        
        for config_file in self.sensitive_keywords['config_files']:
            if config_file in url or config_file in title:
                score += 2  # High risk for config files
        
        return score
    
    def _is_directory_listing(self, title, url, snippet):
        """Check if result is a directory listing"""
        directory_indicators = ['index of', 'directory listing', 'parent directory']
        
        for indicator in directory_indicators:
            if indicator in title.lower() or indicator in snippet.lower():
                return True
        return False
    
    def _contains_error_info(self, title, url, snippet):
        """Check if result contains error information"""
        for indicator in self.sensitive_keywords['error_indicators']:
            if indicator in title or indicator in snippet:
                return True
        return False
    
    def categorize_results(self, results):
        """
        Categorize and prioritize all results
        
        Args:
            results (dict): Dictionary of category -> query -> results
            
        Returns:
            dict: Enhanced results with analysis and prioritization
        """
        analyzed_results = {}
        high_risk_results = []
        login_pages = []
        sensitive_files = []
        
        for category, queries in results.items():
            analyzed_category = {}
            
            for query, query_results in queries.items():
                analyzed_queries = []
                
                for result in query_results:
                    analyzed_result = self.analyze_result(result)
                    analyzed_queries.append(analyzed_result)
                    
                    # Collect high-priority results
                    analysis = analyzed_result['analysis']
                    if analysis['risk_level'] == 'high':
                        high_risk_results.append(analyzed_result)
                    
                    if 'login_page' in analysis['categories']:
                        login_pages.append(analyzed_result)
                    
                    if 'sensitive_file' in analysis['categories']:
                        sensitive_files.append(analyzed_result)
                
                analyzed_category[query] = analyzed_queries
            
            analyzed_results[category] = analyzed_category
        
        # Add summary statistics
        analyzed_results['_summary'] = {
            'high_risk_count': len(high_risk_results),
            'login_pages_count': len(login_pages),
            'sensitive_files_count': len(sensitive_files),
            'high_risk_results': high_risk_results[:10],  # Top 10
            'login_pages': login_pages[:10],
            'sensitive_files': sensitive_files[:10]
        }
        
        return analyzed_results
    
    def generate_report_summary(self, analyzed_results):
        """Generate a summary report of findings"""
        summary = analyzed_results.get('_summary', {})
        
        report = f"""
=== SECURITY ASSESSMENT SUMMARY ===

High Risk Findings: {summary.get('high_risk_count', 0)}
Login Pages Found: {summary.get('login_pages_count', 0)}
Sensitive Files: {summary.get('sensitive_files_count', 0)}

=== TOP PRIORITY FINDINGS ===
"""
        
        # Add high-risk results
        high_risk = summary.get('high_risk_results', [])
        if high_risk:
            report += "\n🚨 HIGH RISK RESULTS:\n"
            for i, result in enumerate(high_risk[:5], 1):
                report += f"{i}. {result['title'][:60]}...\n"
                report += f"   URL: {result['url']}\n"
                report += f"   Risk: {result['analysis']['risk_level'].upper()}\n"
                report += f"   Categories: {', '.join(result['analysis']['categories'])}\n\n"
        
        # Add login pages
        login_pages = summary.get('login_pages', [])
        if login_pages:
            report += "\n🔐 LOGIN PAGES FOUND:\n"
            for i, result in enumerate(login_pages[:5], 1):
                report += f"{i}. {result['title'][:60]}...\n"
                report += f"   URL: {result['url']}\n\n"
        
        return report
