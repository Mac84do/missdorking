"""
Fast Bulk Scanner - Optimized for Speed and Multiple Domains
Bypasses Google completely, focuses on direct analysis for rapid results
"""

import concurrent.futures
import threading
import time
import logging
from datetime import datetime
import json
from pathlib import Path

from hybrid_scraper_fixed import HybridScraper
from analysis import ResultAnalyzer

class FastBulkScanner:
    def __init__(self, max_workers=8, delay_range=(0.1, 0.3)):
        """
        Fast bulk scanner optimized for speed
        
        Args:
            max_workers (int): Number of concurrent threads
            delay_range (tuple): Minimal delays between requests
        """
        self.max_workers = max_workers
        self.delay_range = delay_range
        self.analyzer = ResultAnalyzer()
        self.results = {}
        self.start_time = None
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def scan_single_domain_fast(self, domain):
        """
        Fast scan of single domain using only direct analysis
        
        Args:
            domain (str): Domain to scan
            
        Returns:
            dict: Scan results with timing info
        """
        start_time = time.time()
        thread_id = threading.current_thread().name
        
        logging.info(f"[{thread_id}] Starting fast scan of {domain}")
        
        try:
            # Use hybrid scraper with LUDICROUS SPEED delays 🚀
            scraper = HybridScraper(delay_range=self.delay_range)
            
            # Only do direct analysis - skip Google completely
            direct_results = scraper.analyze_domain_directly(domain)
            
            # Analyze results
            if direct_results:
                analyzed_results = {}
                login_pages = []
                
                for result in direct_results:
                    analyzed_result = self.analyzer.analyze_result(result.copy())
                    analysis = analyzed_result['analysis']
                    
                    if 'login_page' in analysis['categories']:
                        login_pages.append(analyzed_result)
                
                analyzed_results = {
                    'Login & Admin Pages': {
                        f'Direct analysis of {domain}': direct_results
                    }
                }
                
                analyzed_results['_summary'] = {
                    'total_unique_results': len(direct_results),
                    'login_pages_count': len(login_pages),
                    'high_risk_count': len([r for r in login_pages if r['analysis']['risk_level'] == 'high']),
                    'login_pages': login_pages
                }
            else:
                analyzed_results = {
                    '_summary': {
                        'total_unique_results': 0,
                        'login_pages_count': 0,
                        'high_risk_count': 0,
                        'login_pages': []
                    }
                }
            
            scan_time = time.time() - start_time
            
            result = {
                'domain': domain,
                'results': analyzed_results,
                'scan_time': round(scan_time, 2),
                'success': True,
                'error': None,
                'timestamp': datetime.now().isoformat()
            }
            
            logging.info(f"[{thread_id}] ✅ {domain} completed in {scan_time:.2f}s - {len(direct_results)} results")
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
    
    def bulk_scan(self, domains, progress_callback=None):
        """
        Perform fast bulk scanning of multiple domains
        
        Args:
            domains (list): List of domains to scan
            progress_callback (function): Optional progress callback
            
        Returns:
            dict: Bulk scan results with summary
        """
        self.start_time = time.time()
        total_domains = len(domains)
        
        logging.info(f"🚀 Starting bulk scan of {total_domains} domains with {self.max_workers} workers")
        
        results = {}
        completed = 0
        
        # Use ThreadPoolExecutor for concurrent scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scan jobs
            future_to_domain = {
                executor.submit(self.scan_single_domain_fast, domain): domain 
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
                    
                    # Quick status update
                    elapsed = time.time() - self.start_time
                    avg_time = elapsed / completed
                    eta = (total_domains - completed) * avg_time
                    
                    status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
                    summary = result['results']['_summary']
                    login_count = summary.get('login_pages_count', 0)
                    
                    print(f"[{completed}/{total_domains}] {status} {domain} ({result['scan_time']}s) - {login_count} login pages | ETA: {eta/60:.1f}min")
                    
                except Exception as e:
                    logging.error(f"Failed to get result for {domain}: {e}")
                    results[domain] = {
                        'domain': domain,
                        'success': False,
                        'error': str(e),
                        'scan_time': 0,
                        'results': {'_summary': {'total_unique_results': 0, 'login_pages_count': 0, 'high_risk_count': 0}}
                    }
        
        # Generate summary
        total_time = time.time() - self.start_time
        successful_scans = sum(1 for r in results.values() if r['success'])
        failed_scans = total_domains - successful_scans
        total_login_pages = sum(r['results']['_summary'].get('login_pages_count', 0) for r in results.values())
        total_high_risk = sum(r['results']['_summary'].get('high_risk_count', 0) for r in results.values())
        
        bulk_summary = {
            'total_domains': total_domains,
            'successful_scans': successful_scans,
            'failed_scans': failed_scans,
            'total_scan_time': round(total_time, 2),
            'average_time_per_domain': round(total_time / total_domains, 2),
            'total_login_pages_found': total_login_pages,
            'total_high_risk_findings': total_high_risk,
            'timestamp': datetime.now().isoformat()
        }
        
        self.results = {
            'summary': bulk_summary,
            'domain_results': results
        }
        
        logging.info(f"🎉 Bulk scan completed! {total_domains} domains in {total_time/60:.1f} minutes")
        logging.info(f"📊 Results: {successful_scans} success, {failed_scans} failed, {total_login_pages} login pages found")
        
        return self.results
    
    def save_results(self, filepath=None):
        """Save results to JSON file"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"bulk_scan_results_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"💾 Results saved to {filepath}")
        return filepath
    
    def generate_quick_report(self):
        """Generate a quick text summary report"""
        if not self.results:
            return "No results available"
        
        summary = self.results['summary']
        domain_results = self.results['domain_results']
        
        report = f"""
🚀 FAST BULK SCAN REPORT
========================

📊 SUMMARY:
- Total Domains: {summary['total_domains']}
- Successful Scans: {summary['successful_scans']}
- Failed Scans: {summary['failed_scans']}
- Total Time: {summary['total_scan_time']:.1f} seconds ({summary['total_scan_time']/60:.1f} minutes)
- Average per Domain: {summary['average_time_per_domain']:.2f} seconds
- Login Pages Found: {summary['total_login_pages_found']}
- High Risk Findings: {summary['total_high_risk_findings']}

🎯 LOGIN PAGES FOUND:
=====================
"""
        
        # List all domains with login pages found
        domains_with_logins = []
        for domain, result in domain_results.items():
            if result['success']:
                login_count = result['results']['_summary'].get('login_pages_count', 0)
                if login_count > 0:
                    domains_with_logins.append((domain, login_count, result['scan_time']))
        
        if domains_with_logins:
            for domain, count, scan_time in sorted(domains_with_logins, key=lambda x: x[1], reverse=True):
                report += f"✅ {domain} - {count} login page(s) ({scan_time}s)\n"
        else:
            report += "No login pages found across all scanned domains.\n"
        
        report += f"\n❌ FAILED DOMAINS:\n"
        report += "==================\n"
        
        failed_domains = [(d, r['error']) for d, r in domain_results.items() if not r['success']]
        if failed_domains:
            for domain, error in failed_domains:
                report += f"❌ {domain} - {error}\n"
        else:
            report += "All domains scanned successfully!\n"
        
        return report

def main():
    """Test the fast bulk scanner"""
    # Test with a few domains
    test_domains = [
        "daytona.co.za",
        "google.com", 
        "github.com"
    ]
    
    print("🚀 Testing Fast Bulk Scanner")
    print("=" * 50)
    
    scanner = FastBulkScanner(max_workers=3, delay_range=(0.5, 1.0))
    
    results = scanner.bulk_scan(test_domains)
    
    print("\n📊 RESULTS SUMMARY:")
    print(scanner.generate_quick_report())
    
    # Save results
    filepath = scanner.save_results()
    print(f"\n💾 Detailed results saved to: {filepath}")

if __name__ == "__main__":
    main()
