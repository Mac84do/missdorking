"""
Professional Bulk Scanner - Mimics Commercial Pentest Tools
Optimized for speed and reliability like Pentest-Tools.com
"""

import concurrent.futures
import threading
import time
import logging
import random
from datetime import datetime
import json
from pathlib import Path

from hybrid_scraper_fixed import HybridScraper
from analysis import ResultAnalyzer

class ProfessionalBulkScanner:
    def __init__(self, max_workers=3, delay_range=(5.0, 8.0)):
        """
        Professional bulk scanner optimized like commercial tools
        
        Args:
            max_workers (int): Number of concurrent threads (default: 3 for reliability)
            delay_range (tuple): Conservative delays between requests
        """
        self.max_workers = max_workers
        self.delay_range = delay_range
        self.analyzer = ResultAnalyzer()
        self.results = {}
        self.start_time = None
        
        # Professional tool strategy: Focus on high-value queries only
        self.priority_queries = {
            "Login & Admin Pages": [
                "site:{domain} inurl:login",
                "site:{domain} inurl:admin", 
                "site:{domain} inurl:dashboard",
                "site:{domain} \"admin panel\"",
                "site:{domain} \"login page\""
            ],
            "File Types & Directories": [
                "site:{domain} filetype:pdf",
                "site:{domain} filetype:doc OR filetype:docx",
                "site:{domain} intitle:\"index of\"",
                "site:{domain} filetype:xls OR filetype:xlsx"
            ],
            "Configuration Files": [
                "site:{domain} filetype:conf OR filetype:config",
                "site:{domain} filetype:env",
                "site:{domain} \".htaccess\" OR \".htpasswd\"",
                "site:{domain} filetype:xml"
            ],
            "Database Files": [
                "site:{domain} filetype:sql",
                "site:{domain} filetype:db",
                "site:{domain} \"mysql\" OR \"database\""
            ],
            "Error Messages & Debug Info": [
                "site:{domain} \"error\" OR \"warning\"",
                "site:{domain} \"debug\" OR \"stack trace\"",
                "site:{domain} \"exception\" OR \"fatal\""
            ]
        }
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def scan_single_domain_professional(self, domain, selected_categories=None):
        """
        Professional scan of single domain using high-value queries only
        
        Args:
            domain (str): Domain to scan
            selected_categories (list): Categories to scan (None for priority categories)
            
        Returns:
            dict: Scan results with timing info
        """
        start_time = time.time()
        thread_id = threading.current_thread().name
        
        logging.info(f"[{thread_id}] Starting professional scan of {domain}")
        
        try:
            from scraper import GoogleScraper
            
            # Use very conservative delays for reliability
            scraper = GoogleScraper(delay_range=self.delay_range)
            
            # Use only priority queries for speed and effectiveness
            categories_to_scan = selected_categories if selected_categories else list(self.priority_queries.keys())
            
            results = {}
            total_results_count = 0
            successful_queries = 0
            failed_queries = 0
            
            for category in categories_to_scan:
                if category not in self.priority_queries:
                    continue
                    
                category_results = {}
                category_queries = self.priority_queries[category]
                
                # Limit to 2 most effective queries per category for speed
                for query_template in category_queries[:2]:
                    try:
                        # Format query with domain
                        query = query_template.format(domain=domain)
                        
                        # Use very conservative result limits
                        search_results = scraper.search_google(query, 3)  # Only 3 results per query
                        category_results[query] = search_results
                        total_results_count += len(search_results)
                        successful_queries += 1
                        
                        # Add random delay between queries to avoid detection
                        if len(category_queries) > 1:
                            extra_delay = random.uniform(2.0, 4.0)
                            time.sleep(extra_delay)
                            
                    except Exception as e:
                        failed_queries += 1
                        logging.warning(f"[{thread_id}] Query failed for {domain}: {query_template} - {e}")
                        category_results[query_template.format(domain=domain)] = []
                        
                        # Longer delay after failure
                        time.sleep(random.uniform(10.0, 15.0))
                
                if category_results:
                    results[category] = category_results
                
                # Delay between categories
                if len(categories_to_scan) > 1:
                    category_delay = random.uniform(8.0, 12.0)
                    time.sleep(category_delay)
            
            # Add direct analysis for additional coverage (like professional tools)
            try:
                hybrid_scraper = HybridScraper(delay_range=(1.0, 2.0))  # Faster for direct analysis
                direct_results = hybrid_scraper.analyze_domain_directly(domain)
                
                if direct_results:
                    if "Login & Admin Pages" not in results:
                        results["Login & Admin Pages"] = {}
                    
                    direct_query = f"Direct site analysis of {domain}"
                    results["Login & Admin Pages"][direct_query] = direct_results
                    total_results_count += len(direct_results)
                    
            except Exception as e:
                logging.warning(f"[{thread_id}] Direct analysis failed for {domain}: {e}")
            
            # Perform analysis
            analyzed_results = self.analyzer.categorize_results(results)
            
            scan_time = time.time() - start_time
            
            result = {
                'domain': domain,
                'results': analyzed_results,
                'scan_time': round(scan_time, 2),
                'success': True,
                'error': None,
                'timestamp': datetime.now().isoformat(),
                'stats': {
                    'successful_queries': successful_queries,
                    'failed_queries': failed_queries,
                    'total_results': total_results_count
                }
            }
            
            summary = analyzed_results.get('_summary', {})
            login_count = summary.get('login_pages_count', 0)
            high_risk = summary.get('high_risk_count', 0)
            
            logging.info(f"[{thread_id}] ✅ {domain} completed in {scan_time:.2f}s - {total_results_count} results ({login_count} login pages, {high_risk} high-risk) - {successful_queries}/{successful_queries+failed_queries} queries successful")
            return result
            
        except Exception as e:
            scan_time = time.time() - start_time
            error_msg = str(e)
            
            logging.error(f"[{thread_id}] ❌ {domain} failed after {scan_time:.2f}s: {error_msg}")
            
            return {
                'domain': domain,
                'results': {'_summary': {'total_unique_results': 0, 'login_pages_count': 0, 'high_risk_count': 0}},
                'scan_time': round(scan_time, 2),
                'success': False,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def bulk_scan(self, domains, selected_categories=None, progress_callback=None):
        """
        Perform professional bulk scanning of multiple domains
        
        Args:
            domains (list): List of domains to scan
            selected_categories (list): Categories to scan
            progress_callback (function): Optional progress callback
            
        Returns:
            dict: Bulk scan results with summary
        """
        self.start_time = time.time()
        total_domains = len(domains)
        
        logging.info(f"🎯 Starting professional bulk scan of {total_domains} domains with {self.max_workers} workers")
        logging.info(f"📊 Strategy: High-value queries only, conservative delays, like commercial pentest tools")
        
        results = {}
        completed = 0
        
        # Use ThreadPoolExecutor with conservative worker count
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scan jobs
            future_to_domain = {
                executor.submit(self.scan_single_domain_professional, domain, selected_categories): domain 
                for domain in domains
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                completed += 1
                
                try:
                    result = future.result()
                    results[domain] = result
                    
                    if progress_callback:
                        progress_callback(completed, total_domains, domain, result)
                    
                    # Professional status update
                    status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
                    summary = result['results']['_summary']
                    login_count = summary.get('login_pages_count', 0)
                    high_risk = summary.get('high_risk_count', 0)
                    
                    # Calculate ETA
                    elapsed = time.time() - self.start_time
                    avg_time = elapsed / completed
                    eta = (total_domains - completed) * avg_time
                    
                    stats = result.get('stats', {})
                    queries_info = f"{stats.get('successful_queries', 0)}/{stats.get('successful_queries', 0) + stats.get('failed_queries', 0)} queries"
                    
                    print(f"[{completed}/{total_domains}] {status} {domain} ({result['scan_time']}s) - {login_count} login pages, {high_risk} high-risk ({queries_info}) | ETA: {eta/60:.1f}min")
                    
                except Exception as e:
                    logging.error(f"Failed to get result for {domain}: {e}")
                    results[domain] = {
                        'domain': domain,
                        'success': False,
                        'error': str(e),
                        'scan_time': 0,
                        'results': {'_summary': {'total_unique_results': 0, 'login_pages_count': 0, 'high_risk_count': 0}}
                    }
        
        # Generate comprehensive summary
        total_time = time.time() - self.start_time
        successful_scans = sum(1 for r in results.values() if r['success'])
        failed_scans = total_domains - successful_scans
        total_login_pages = sum(r['results']['_summary'].get('login_pages_count', 0) for r in results.values())
        total_high_risk = sum(r['results']['_summary'].get('high_risk_count', 0) for r in results.values())
        total_queries = sum(r.get('stats', {}).get('successful_queries', 0) + r.get('stats', {}).get('failed_queries', 0) for r in results.values())
        successful_queries = sum(r.get('stats', {}).get('successful_queries', 0) for r in results.values())
        
        bulk_summary = {
            'total_domains': total_domains,
            'successful_scans': successful_scans,
            'failed_scans': failed_scans,
            'total_scan_time': round(total_time, 2),
            'average_time_per_domain': round(total_time / total_domains, 2),
            'total_login_pages_found': total_login_pages,
            'total_high_risk_findings': total_high_risk,
            'total_queries_executed': total_queries,
            'successful_queries': successful_queries,
            'query_success_rate': round((successful_queries / max(total_queries, 1)) * 100, 1),
            'timestamp': datetime.now().isoformat()
        }
        
        self.results = {
            'summary': bulk_summary,
            'domain_results': results
        }
        
        logging.info(f"🎉 Professional bulk scan completed!")
        logging.info(f"📊 Results: {successful_scans}/{total_domains} domains successful, {total_login_pages} login pages, {total_high_risk} high-risk findings")
        logging.info(f"⚡ Performance: {total_time/60:.1f} minutes total, {successful_queries}/{total_queries} queries successful ({bulk_summary['query_success_rate']}%)")
        
        return self.results
    
    def save_results(self, filepath=None):
        """Save results to JSON file"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"professional_bulk_scan_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"💾 Results saved to {filepath}")
        return filepath
    
    def generate_professional_report(self):
        """Generate a professional summary report like commercial tools"""
        if not self.results:
            return "No results available"
        
        summary = self.results['summary']
        domain_results = self.results['domain_results']
        
        report = f"""
🎯 PROFESSIONAL BULK SCAN REPORT
=================================

📊 EXECUTIVE SUMMARY:
• Total Domains Scanned: {summary['total_domains']}
• Successful Scans: {summary['successful_scans']} ({summary['successful_scans']/summary['total_domains']*100:.1f}%)
• Failed Scans: {summary['failed_scans']}
• Scan Duration: {summary['total_scan_time']:.1f} seconds ({summary['total_scan_time']/60:.1f} minutes)
• Average Time per Domain: {summary['average_time_per_domain']:.2f} seconds
• Query Success Rate: {summary['query_success_rate']}%

🔍 SECURITY FINDINGS:
• Login Pages Found: {summary['total_login_pages_found']}
• High Risk Findings: {summary['total_high_risk_findings']}
• Total Queries Executed: {summary['total_queries_executed']}
• Successful Queries: {summary['successful_queries']}

🎯 HIGH-VALUE TARGETS (Login Pages Found):
=========================================="""
        
        # List domains with login pages found (highest value findings)
        high_value_targets = []
        for domain, result in domain_results.items():
            if result['success']:
                login_count = result['results']['_summary'].get('login_pages_count', 0)
                high_risk_count = result['results']['_summary'].get('high_risk_count', 0)
                if login_count > 0:
                    high_value_targets.append((domain, login_count, high_risk_count, result['scan_time']))
        
        if high_value_targets:
            # Sort by login pages found, then by high risk count
            high_value_targets.sort(key=lambda x: (x[1], x[2]), reverse=True)
            for domain, login_count, high_risk_count, scan_time in high_value_targets:
                risk_indicator = "🔴 HIGH RISK" if high_risk_count > 0 else "🟡 MEDIUM RISK"
                report += f"\n✅ {domain} - {login_count} login page(s), {high_risk_count} high-risk findings ({scan_time}s) {risk_indicator}"
        else:
            report += "\nNo login pages found across all scanned domains."
        
        report += f"\n\n❌ FAILED SCANS:\n" + "="*16
        
        failed_domains = [(d, r['error']) for d, r in domain_results.items() if not r['success']]
        if failed_domains:
            for domain, error in failed_domains:
                report += f"\n❌ {domain} - {error}"
        else:
            report += "\nAll domains scanned successfully!"
        
        report += f"\n\n🎯 METHODOLOGY:\n" + "="*15
        report += f"\n• Strategy: High-value queries only (like commercial pentest tools)"
        report += f"\n• Categories: Login pages, file types, configuration files, databases, errors"
        report += f"\n• Rate Limiting: Conservative delays to avoid blocks"
        report += f"\n• Quality over Quantity: 2-3 queries per category, 3 results per query"
        
        return report

def main():
    """Test the professional bulk scanner"""
    test_domains = [
        "example.com",
        "github.com", 
        "stackoverflow.com"
    ]
    
    print("🎯 Testing Professional Bulk Scanner")
    print("=" * 50)
    
    scanner = ProfessionalBulkScanner(max_workers=2, delay_range=(8.0, 12.0))
    
    results = scanner.bulk_scan(test_domains)
    
    print("\n📊 PROFESSIONAL RESULTS SUMMARY:")
    print(scanner.generate_professional_report())
    
    # Save results
    filepath = scanner.save_results()
    print(f"\n💾 Detailed results saved to: {filepath}")

if __name__ == "__main__":
    main()
