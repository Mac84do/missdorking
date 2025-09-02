#!/usr/bin/env python3
"""
Enhanced MissDorking Command Line Tool 💋
With bulk domains, smart file naming, flexible reports, and fabulous results! 🍒
"""

import argparse
import sys
import os
import logging
import json
from datetime import datetime
import re
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
from scraper import GoogleScraper
from hybrid_scraper_fixed import HybridScraper
from export import ResultExporter
from analysis import ResultAnalyzer

class EnhancedCommandLineDorking:
    def __init__(self):
        self.scraper = GoogleScraper()
        self.hybrid_scraper = HybridScraper()
        self.exporter = ResultExporter()
        self.analyzer = ResultAnalyzer()
        self.results = {}
        self.setup_logging()
    
    def setup_logging(self, log_level='INFO'):
        """Set up logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler('missdorking_cli.log'),
                logging.StreamHandler()
            ]
        )
    
    def generate_filename(self, domain, file_type, is_bulk=False, scan_date=None):
        """Generate smart filename with domain name and scan date"""
        if scan_date is None:
            scan_date = datetime.now()
        
        # Clean domain name for filename
        clean_domain = re.sub(r'[^\w\-_.]', '_', domain)
        
        # Format date
        date_str = scan_date.strftime("%Y%m%d_%H%M%S")
        
        if is_bulk:
            return f"MissDorking_BULK_scan_{date_str}.{file_type}"
        else:
            return f"MissDorking_{clean_domain}_{date_str}.{file_type}"
    
    def print_banner(self):
        """Print fabulous MissDorking banner"""
        banner = """
    💋 MissDorking™ - Enhanced CLI Dorking Tool 🍒
    ╔═══════════════════════════════════════════════╗
    ║  😘  Making Security Fun & Fabulous via CLI!  💅 ║
    ╚═══════════════════════════════════════════════╝
        """
        print(banner)
    
    def scan_single_domain(self, domain, categories=None, max_results=10, 
                          delay_range=(2, 4), use_hybrid=False, output_format='console'):
        """Scan a single domain with fabulous results"""
        
        print(f"\n🎯 Starting fabulous scan of: {domain}")
        print(f"💅 Using {'hybrid' if use_hybrid else 'standard'} scraper")
        
        # Set scraper delay
        if use_hybrid:
            self.hybrid_scraper.delay_range = delay_range
            scraper = self.hybrid_scraper
        else:
            self.scraper.delay_range = delay_range
            scraper = self.scraper
        
        # Get all dorks for domain
        all_dorks = get_all_dorks_for_domain(domain)
        
        # Filter by categories if specified
        if categories:
            available_categories = list(GOOGLE_DORKS.keys())
            valid_categories = [cat for cat in categories if cat in available_categories]
            if not valid_categories:
                print(f"❌ No valid categories found. Available: {', '.join(available_categories)}")
                return {}
            filtered_dorks = {cat: dorks for cat, dorks in all_dorks.items() 
                            if cat in valid_categories}
        else:
            filtered_dorks = all_dorks
        
        # Calculate total queries
        total_queries = sum(len(dorks) for dorks in filtered_dorks.values())
        print(f"📊 Total queries to execute: {total_queries}")
        
        results = {}
        current_query = 0
        
        for category, dorks in filtered_dorks.items():
            print(f"\n🔍 Scanning category: {category}")
            category_results = {}
            
            for dork in dorks:
                current_query += 1
                print(f"  💋 Query {current_query}/{total_queries}: {dork[:60]}...")
                
                # Search with selected scraper
                if use_hybrid:
                    search_results = scraper.search_with_fallback(dork, max_results)
                else:
                    search_results = scraper.search_google(dork, max_results)
                
                category_results[dork] = search_results
                
                if search_results:
                    print(f"    ✨ Found {len(search_results)} fabulous results!")
                    if output_format == 'verbose':
                        for i, result in enumerate(search_results[:3], 1):
                            print(f"      {i}. {result['title'][:60]}...")
                            print(f"         {result['url']}")
                else:
                    print("    💔 No results found")
            
            results[category] = category_results
        
        # Show summary
        total_results = sum(sum(len(results) for results in cat.values()) 
                          for cat in results.values())
        
        fun_messages = [
            f"💄 Scan complete for {domain}! Found {total_results} fabulous results! 💋",
            f"👠 All done dorking {domain}! {total_results} targets acquired with style! ✨",
            f"🔥 Mission accomplished for {domain}! {total_results} results ready for your viewing pleasure! 💅"
        ]
        
        import random
        print(f"\n{random.choice(fun_messages)}")
        
        return results
    
    def scan_bulk_domains(self, domains, categories=None, max_results=10, 
                         delay_range=(2, 4), use_hybrid=False, output_format='console',
                         report_format='individual'):
        """Scan multiple domains with bulk fabulous results"""
        
        print(f"\n👑 Starting bulk domain domination!")
        print(f"🎯 Domains to conquer: {len(domains)}")
        
        bulk_results = {}
        scan_start_time = datetime.now()
        
        for i, domain in enumerate(domains, 1):
            print(f"\n{'='*60}")
            print(f"🎯 SCANNING DOMAIN {i}/{len(domains)}: {domain}")
            print(f"{'='*60}")
            
            try:
                # Scan individual domain
                domain_results = self.scan_single_domain(
                    domain, categories, max_results, delay_range, 
                    use_hybrid, output_format
                )
                
                bulk_results[domain] = {
                    'results': domain_results,
                    'scan_time': datetime.now(),
                    'success': True
                }
                
                # Show summary for this domain
                total_results = sum(sum(len(results) for results in cat.values()) 
                                  for cat in domain_results.values())
                print(f"✅ {domain} completed: {total_results} results found")
                
            except Exception as e:
                logging.error(f"Error scanning {domain}: {e}")
                bulk_results[domain] = {
                    'results': {},
                    'scan_time': datetime.now(),
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ {domain} failed: {e}")
        
        # Generate final summary
        successful_scans = sum(1 for result in bulk_results.values() if result['success'])
        failed_scans = len(domains) - successful_scans
        total_results = sum(
            sum(sum(len(results) for results in cat.values()) 
                for cat in domain_result['results'].values())
            for domain_result in bulk_results.values() if domain_result['success']
        )
        
        scan_duration = datetime.now() - scan_start_time
        
        print(f"\n{'='*60}")
        print("🎉 BULK SCAN COMPLETE! 🎉")
        print(f"{'='*60}")
        print(f"📊 Summary:")
        print(f"   • Total domains scanned: {len(domains)}")
        print(f"   • Successful scans: {successful_scans}")
        print(f"   • Failed scans: {failed_scans}")
        print(f"   • Total results found: {total_results}")
        print(f"   • Scan duration: {scan_duration}")
        print(f"\n💋 MissDorking says: 'Bulk dorking complete with fabulous results!' 💅")
        
        # Generate reports based on format
        self.generate_bulk_reports(bulk_results, report_format)
        
        return bulk_results
    
    def generate_bulk_reports(self, bulk_results, report_format):
        """Generate bulk reports based on format selection"""
        print(f"\n📋 Generating reports in '{report_format}' format...")
        
        if report_format in ['individual', 'both']:
            # Generate individual reports for each domain
            for domain, domain_data in bulk_results.items():
                if domain_data['success']:
                    try:
                        scan_time = domain_data['scan_time']
                        results = domain_data['results']
                        
                        # Generate PDF
                        filename = self.generate_filename(domain, 'pdf', scan_date=scan_time)
                        filepath = self.exporter.export_to_pdf(results, domain, filename)
                        print(f"  📄 Individual PDF: {filepath}")
                        
                        # Generate CSV
                        filename = self.generate_filename(domain, 'csv', scan_date=scan_time)
                        filepath = self.exporter.export_to_csv(results, domain, filename)
                        print(f"  📊 Individual CSV: {filepath}")
                        
                    except Exception as e:
                        print(f"  ❌ Error generating report for {domain}: {e}")
        
        if report_format in ['combined', 'both']:
            try:
                # Combine all results
                combined_results = {}
                
                for domain, domain_data in bulk_results.items():
                    if domain_data['success']:
                        results = domain_data['results']
                        
                        for category, category_results in results.items():
                            if category not in combined_results:
                                combined_results[category] = {}
                            
                            # Prefix queries with domain name
                            for query, query_results in category_results.items():
                                prefixed_query = f"[{domain}] {query}"
                                combined_results[category][prefixed_query] = query_results
                
                # Generate combined PDF
                filename = self.generate_filename("ALL_DOMAINS", 'pdf', is_bulk=True)
                filepath = self.exporter.export_to_pdf(combined_results, "Bulk Scan", filename)
                print(f"  📄 Combined PDF: {filepath}")
                
                # Generate combined CSV
                filename = self.generate_filename("ALL_DOMAINS", 'csv', is_bulk=True)
                filepath = self.exporter.export_to_csv(combined_results, "Bulk Scan", filename)
                print(f"  📊 Combined CSV: {filepath}")
                
            except Exception as e:
                print(f"  ❌ Error generating combined report: {e}")
    
    def export_results(self, results, domain, formats=['pdf', 'csv', 'json']):
        """Export results in specified formats"""
        exported_files = []
        
        for format_type in formats:
            try:
                filename = self.generate_filename(domain, format_type)
                
                if format_type == 'pdf':
                    filepath = self.exporter.export_to_pdf(results, domain, filename)
                elif format_type == 'csv':
                    filepath = self.exporter.export_to_csv(results, domain, filename)
                elif format_type == 'json':
                    # Export as JSON
                    filepath = os.path.join(os.getcwd(), filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
                
                exported_files.append(filepath)
                print(f"💅 Exported {format_type.upper()}: {filepath}")
                
            except Exception as e:
                print(f"❌ Error exporting {format_type}: {e}")
        
        return exported_files


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="💋 MissDorking™ Enhanced CLI - Fabulous Google Dorking Tool! 🍒",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single domain scan
  python run_dorking_cli.py -d example.com
  
  # Bulk domain scan
  python run_dorking_cli.py -b domains.txt --report-format both
  
  # Fast hybrid scan with specific categories
  python run_dorking_cli.py -d target.com --hybrid --categories "File Extensions" "Login Pages"
  
  # Bulk scan with custom settings
  python run_dorking_cli.py -b "domain1.com,domain2.com" --max-results 20 --delay 1-3
        """
    )
    
    # Main operation mode
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--domain', type=str,
                      help='Single domain to scan')
    group.add_argument('-b', '--bulk', type=str,
                      help='Bulk domains (comma-separated or file path)')
    
    # Scan options
    parser.add_argument('--categories', nargs='+', 
                       help='Categories to scan (default: all)')
    parser.add_argument('--max-results', type=int, default=10,
                       help='Maximum results per query (default: 10)')
    parser.add_argument('--delay', type=str, default='2-4',
                       help='Delay between requests in seconds (default: 2-4)')
    parser.add_argument('--hybrid', action='store_true',
                       help='Use hybrid scraper for better results')
    
    # Output options
    parser.add_argument('--output-format', choices=['console', 'verbose', 'quiet'],
                       default='console', help='Output verbosity level')
    parser.add_argument('--export', nargs='+', choices=['pdf', 'csv', 'json'],
                       default=['pdf'], help='Export formats (default: pdf)')
    parser.add_argument('--report-format', choices=['individual', 'combined', 'both'],
                       default='individual', help='Bulk report format (default: individual)')
    
    # Advanced options
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    parser.add_argument('--no-banner', action='store_true',
                       help='Suppress banner display')
    
    args = parser.parse_args()
    
    # Initialize CLI tool
    cli = EnhancedCommandLineDorking()
    cli.setup_logging(args.log_level)
    
    # Show banner unless suppressed
    if not args.no_banner:
        cli.print_banner()
    
    # Parse delay range
    try:
        if '-' in args.delay:
            min_delay, max_delay = map(float, args.delay.split('-'))
            delay_range = (min_delay, max_delay)
        else:
            delay = float(args.delay)
            delay_range = (delay, delay)
    except ValueError:
        print("❌ Invalid delay format. Use single number or range (e.g., '2-5')")
        return 1
    
    # Handle single domain scan
    if args.domain:
        print(f"🎯 Single domain mode: {args.domain}")
        
        results = cli.scan_single_domain(
            args.domain,
            categories=args.categories,
            max_results=args.max_results,
            delay_range=delay_range,
            use_hybrid=args.hybrid,
            output_format=args.output_format
        )
        
        if results:
            # Export results
            cli.export_results(results, args.domain, args.export)
        else:
            print("💔 No results to export")
    
    # Handle bulk domain scan
    elif args.bulk:
        print(f"👑 Bulk domain mode")
        
        # Parse domains (file or comma-separated list)
        if os.path.isfile(args.bulk):
            print(f"📁 Loading domains from file: {args.bulk}")
            try:
                with open(args.bulk, 'r', encoding='utf-8') as f:
                    domains = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"❌ Error reading domains file: {e}")
                return 1
        else:
            # Comma-separated domains
            domains = [d.strip() for d in args.bulk.split(',') if d.strip()]
        
        if not domains:
            print("❌ No valid domains found")
            return 1
        
        print(f"📋 Found {len(domains)} domains to scan")
        
        bulk_results = cli.scan_bulk_domains(
            domains,
            categories=args.categories,
            max_results=args.max_results,
            delay_range=delay_range,
            use_hybrid=args.hybrid,
            output_format=args.output_format,
            report_format=args.report_format
        )
    
    print(f"\n✨ MissDorking CLI completed successfully! Check your reports! 💋")
    return 0


if __name__ == "__main__":
    sys.exit(main())
