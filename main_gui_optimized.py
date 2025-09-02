"""
Optimized Google Dorking GUI - Fast Version
Implements speed optimizations including:
- Reduced delays (1-2 seconds instead of 2-4)
- Batched OR queries to reduce total searches
- Hybrid scraper runs first for instant results
- Configurable query limits per category
- Parallel processing where possible
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import time
import random
from datetime import datetime
from urllib.parse import urljoin, urlparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

# Import our modules
from dorking import DorkingEngine
from hybrid_scraper_fixed import HybridScraper
from analysis import ResultAnalyzer
from fast_bulk_scanner import FastBulkScanner

class OptimizedDorkingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Google Dorking Tool - Optimized Edition")
        self.master.geometry("1000x700")
        
        # Configuration
        self.config = {
            'delay_range': (1, 2),  # Reduced from (2, 4)
            'max_queries_per_category': 3,  # Limit queries per category
            'batch_queries': True,  # Use OR batching
            'hybrid_first': True,   # Run hybrid scraper first
            'max_workers': 3        # Parallel workers
        }
        
        # Initialize components
        self.dorking_engine = DorkingEngine()
        self.hybrid_scraper = HybridScraper(delay_range=self.config['delay_range'])
        self.analyzer = ResultAnalyzer()
        self.fast_scanner = FastBulkScanner(max_workers=self.config['max_workers'])
        
        # State
        self.is_scanning = False
        self.current_results = {}
        self.scan_start_time = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the optimized GUI"""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Single Domain tab
        self.setup_single_domain_tab()
        
        # Bulk Scanner tab
        self.setup_bulk_scanner_tab()
        
        # Configuration tab
        self.setup_config_tab()
        
    def setup_single_domain_tab(self):
        """Setup single domain scanning tab"""
        single_frame = ttk.Frame(self.notebook)
        self.notebook.add(single_frame, text="Single Domain")
        
        # Input section
        input_frame = ttk.LabelFrame(single_frame, text="Domain Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Domain:").pack(anchor=tk.W)
        self.domain_entry = ttk.Entry(input_frame, font=('Arial', 12))
        self.domain_entry.pack(fill=tk.X, pady=(5, 10))
        self.domain_entry.insert(0, "daytona.co.za")
        
        # Scan options
        options_frame = ttk.LabelFrame(single_frame, text="Scan Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.hybrid_first_var = tk.BooleanVar(value=self.config['hybrid_first'])
        ttk.Checkbutton(options_frame, text="Run Hybrid Scanner First (Recommended)", 
                       variable=self.hybrid_first_var).pack(anchor=tk.W)
        
        self.google_dorking_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include Google Dorking (May be rate limited)", 
                       variable=self.google_dorking_var).pack(anchor=tk.W)
        
        # Scan button
        button_frame = ttk.Frame(single_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.scan_button = ttk.Button(button_frame, text="🚀 Start Fast Scan", 
                                     command=self.start_optimized_scan)
        self.scan_button.pack(side=tk.LEFT)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(single_frame, text="Progress", padding=10)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready to scan")
        self.status_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(single_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results text with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     font=('Consolas', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Save results button
        save_frame = ttk.Frame(results_frame)
        save_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(save_frame, text="💾 Save Results", 
                  command=self.save_results).pack(side=tk.RIGHT)
        
    def setup_bulk_scanner_tab(self):
        """Setup bulk scanner tab"""
        bulk_frame = ttk.Frame(self.notebook)
        self.notebook.add(bulk_frame, text="Bulk Scanner")
        
        # Input section
        input_frame = ttk.LabelFrame(bulk_frame, text="Domain List Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Domains (one per line):").pack(anchor=tk.W)
        
        self.bulk_domains_text = scrolledtext.ScrolledText(input_frame, height=8, 
                                                          font=('Arial', 10))
        self.bulk_domains_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        self.bulk_domains_text.insert(tk.END, "daytona.co.za\\ngoogle.com\\ngithub.com")
        
        # Bulk scan button
        bulk_button_frame = ttk.Frame(input_frame)
        bulk_button_frame.pack(fill=tk.X)
        
        self.bulk_scan_button = ttk.Button(bulk_button_frame, text="⚡ Start Bulk Scan", 
                                          command=self.start_bulk_scan)
        self.bulk_scan_button.pack(side=tk.LEFT)
        
        ttk.Button(bulk_button_frame, text="📁 Load from File", 
                  command=self.load_domains_from_file).pack(side=tk.LEFT, padx=(10, 0))
        
        # Bulk progress section
        bulk_progress_frame = ttk.LabelFrame(bulk_frame, text="Bulk Progress", padding=10)
        bulk_progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.bulk_status_label = ttk.Label(bulk_progress_frame, text="Ready for bulk scan")
        self.bulk_status_label.pack(anchor=tk.W)
        
        self.bulk_progress_bar = ttk.Progressbar(bulk_progress_frame, mode='determinate')
        self.bulk_progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Bulk results section
        bulk_results_frame = ttk.LabelFrame(bulk_frame, text="Bulk Results", padding=10)
        bulk_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.bulk_results_text = scrolledtext.ScrolledText(bulk_results_frame, height=15, 
                                                          font=('Consolas', 10))
        self.bulk_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Save bulk results button
        bulk_save_frame = ttk.Frame(bulk_results_frame)
        bulk_save_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(bulk_save_frame, text="💾 Save Bulk Results", 
                  command=self.save_bulk_results).pack(side=tk.RIGHT)
        
    def setup_config_tab(self):
        """Setup configuration tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuration")
        
        # Speed settings
        speed_frame = ttk.LabelFrame(config_frame, text="Speed Settings", padding=10)
        speed_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Delay range
        ttk.Label(speed_frame, text="Request Delay Range (seconds):").pack(anchor=tk.W)
        delay_frame = ttk.Frame(speed_frame)
        delay_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Label(delay_frame, text="Min:").pack(side=tk.LEFT)
        self.min_delay_var = tk.DoubleVar(value=self.config['delay_range'][0])
        ttk.Entry(delay_frame, textvariable=self.min_delay_var, width=10).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(delay_frame, text="Max:").pack(side=tk.LEFT)
        self.max_delay_var = tk.DoubleVar(value=self.config['delay_range'][1])
        ttk.Entry(delay_frame, textvariable=self.max_delay_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # Max queries per category
        ttk.Label(speed_frame, text="Max Queries per Category:").pack(anchor=tk.W)
        self.max_queries_var = tk.IntVar(value=self.config['max_queries_per_category'])
        ttk.Entry(speed_frame, textvariable=self.max_queries_var, width=10).pack(anchor=tk.W, pady=(5, 10))
        
        # Workers
        ttk.Label(speed_frame, text="Parallel Workers:").pack(anchor=tk.W)
        self.max_workers_var = tk.IntVar(value=self.config['max_workers'])
        ttk.Entry(speed_frame, textvariable=self.max_workers_var, width=10).pack(anchor=tk.W, pady=(5, 10))
        
        # Optimization options
        opt_frame = ttk.LabelFrame(config_frame, text="Optimization Options", padding=10)
        opt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.batch_queries_var = tk.BooleanVar(value=self.config['batch_queries'])
        ttk.Checkbutton(opt_frame, text="Batch queries with OR operators", 
                       variable=self.batch_queries_var).pack(anchor=tk.W)
        
        # Save config button
        ttk.Button(opt_frame, text="💾 Save Configuration", 
                  command=self.save_config).pack(anchor=tk.W, pady=(10, 0))
        
    def save_config(self):
        """Save current configuration"""
        try:
            self.config['delay_range'] = (self.min_delay_var.get(), self.max_delay_var.get())
            self.config['max_queries_per_category'] = self.max_queries_var.get()
            self.config['max_workers'] = self.max_workers_var.get()
            self.config['batch_queries'] = self.batch_queries_var.get()
            
            # Update components with new config
            self.hybrid_scraper = HybridScraper(delay_range=self.config['delay_range'])
            self.fast_scanner = FastBulkScanner(max_workers=self.config['max_workers'])
            
            messagebox.showinfo("Configuration", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def start_optimized_scan(self):
        """Start optimized scanning of single domain"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "Please enter a domain to scan")
            return
            
        # Start scanning in thread
        self.is_scanning = True
        self.scan_start_time = time.time()
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        scan_thread = threading.Thread(target=self.run_optimized_scan, args=(domain,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def run_optimized_scan(self, domain):
        """Run the optimized scanning process"""
        try:
            self.update_status("🚀 Starting optimized scan...")
            
            all_results = {}
            total_time = 0
            
            # Step 1: Run Hybrid Scraper First (if enabled)
            if self.hybrid_first_var.get():
                self.update_status("🔍 Running direct site analysis (hybrid scraper)...")
                start_time = time.time()
                
                hybrid_results = self.hybrid_scraper.analyze_domain_directly(domain)
                hybrid_time = time.time() - start_time
                
                if hybrid_results:
                    all_results['Login & Admin Pages'] = {
                        f'Direct analysis of {domain}': hybrid_results
                    }
                    self.update_status(f"✅ Hybrid scan completed in {hybrid_time:.2f}s - Found {len(hybrid_results)} pages")
                else:
                    self.update_status(f"⚠️ Hybrid scan completed in {hybrid_time:.2f}s - No results found")
                
                total_time += hybrid_time
            
            # Step 2: Google Dorking (if enabled and not stopped)
            if self.google_dorking_var.get() and self.is_scanning:
                self.update_status("🔍 Running optimized Google dorking...")
                start_time = time.time()
                
                # Use optimized dorking with batched queries
                google_results = self.run_optimized_dorking(domain)
                google_time = time.time() - start_time
                
                # Merge Google results
                for category, results in google_results.items():
                    if category not in all_results:
                        all_results[category] = {}
                    all_results[category].update(results)
                
                total_time += google_time
                self.update_status(f"✅ Google dorking completed in {google_time:.2f}s")
            
            # Analysis
            if self.is_scanning:
                self.update_status("📊 Analyzing results...")
                analyzed_results = self.analyze_all_results(all_results)
                
                # Display results
                self.current_results = analyzed_results
                self.display_results(analyzed_results, total_time)
                
                self.update_status(f"✅ Scan completed in {total_time:.2f}s")
            
        except Exception as e:
            self.update_status(f"❌ Scan failed: {str(e)}")
            logging.error(f"Scan error: {e}")
        
        finally:
            # Reset UI state
            self.master.after(0, self.reset_scan_ui)
    
    def run_optimized_dorking(self, domain):
        """Run optimized Google dorking with batching"""
        results = {}
        
        # Get dork queries with limits
        all_dorks = self.dorking_engine.get_all_dork_queries()
        
        for category, queries in all_dorks.items():
            if not self.is_scanning:
                break
                
            # Limit queries per category
            limited_queries = queries[:self.config['max_queries_per_category']]
            
            if self.config['batch_queries'] and len(limited_queries) > 1:
                # Batch queries using OR operator
                batched_query = f"site:{domain} (" + " OR ".join([f"({q.replace(f'site:{domain}', '').strip()})" for q in limited_queries]) + ")"
                
                self.update_status(f"🔍 Searching {category} (batched query)...")
                
                try:
                    batch_results = self.dorking_engine.search(batched_query)
                    if batch_results:
                        results[category] = {f"Batched search for {category}": batch_results}
                except Exception as e:
                    logging.error(f"Batched search failed for {category}: {e}")
            else:
                # Run individual queries
                category_results = {}
                for query in limited_queries:
                    if not self.is_scanning:
                        break
                        
                    try:
                        formatted_query = query.format(domain=domain)
                        self.update_status(f"🔍 Searching: {formatted_query[:50]}...")
                        
                        query_results = self.dorking_engine.search(formatted_query)
                        if query_results:
                            category_results[formatted_query] = query_results
                            
                        # Shorter delay between queries
                        time.sleep(random.uniform(*self.config['delay_range']))
                        
                    except Exception as e:
                        logging.error(f"Query failed: {e}")
                
                if category_results:
                    results[category] = category_results
        
        return results
    
    def analyze_all_results(self, raw_results):
        """Analyze all results and generate summary"""
        analyzed_results = {}
        all_login_pages = []
        total_unique_results = 0
        
        for category, category_results in raw_results.items():
            analyzed_category = {}
            
            for query, results in category_results.items():
                analyzed_query_results = []
                
                for result in results:
                    analyzed_result = self.analyzer.analyze_result(result.copy())
                    analyzed_query_results.append(analyzed_result)
                    
                    # Collect login pages
                    analysis = analyzed_result.get('analysis', {})
                    if 'login_page' in analysis.get('categories', []):
                        all_login_pages.append(analyzed_result)
                
                analyzed_category[query] = analyzed_query_results
                total_unique_results += len(results)
            
            analyzed_results[category] = analyzed_category
        
        # Add summary
        analyzed_results['_summary'] = {
            'total_unique_results': total_unique_results,
            'login_pages_count': len(all_login_pages),
            'high_risk_count': len([r for r in all_login_pages if r.get('analysis', {}).get('risk_level') == 'high']),
            'login_pages': all_login_pages
        }
        
        return analyzed_results
    
    def display_results(self, results, scan_time):
        """Display analyzed results in the UI"""
        self.results_text.delete(1.0, tk.END)
        
        summary = results.get('_summary', {})
        
        # Header
        header = f"""🚀 OPTIMIZED DORKING SCAN RESULTS
Domain: {self.domain_entry.get()}
Scan Time: {scan_time:.2f} seconds
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📊 SUMMARY:
Total Results: {summary.get('total_unique_results', 0)}
Login Pages Found: {summary.get('login_pages_count', 0)}
High Risk Findings: {summary.get('high_risk_count', 0)}

"""
        self.results_text.insert(tk.END, header)
        
        # Login pages priority section
        login_pages = summary.get('login_pages', [])
        if login_pages:
            self.results_text.insert(tk.END, "🎯 LOGIN & ADMIN PAGES FOUND:\\n")
            self.results_text.insert(tk.END, "=" * 40 + "\\n")
            
            for i, page in enumerate(login_pages, 1):
                risk = page.get('analysis', {}).get('risk_level', 'unknown')
                risk_emoji = "🔴" if risk == 'high' else "🟡" if risk == 'medium' else "🟢"
                
                self.results_text.insert(tk.END, f"\\n{i}. {risk_emoji} {page['title']}\\n")
                self.results_text.insert(tk.END, f"   URL: {page['url']}\\n")
                
                reasoning = page.get('analysis', {}).get('reasoning', '')
                if reasoning:
                    self.results_text.insert(tk.END, f"   Analysis: {reasoning}\\n")
        
        # Detailed results by category
        self.results_text.insert(tk.END, f"\\n\\n📋 DETAILED RESULTS BY CATEGORY:\\n")
        self.results_text.insert(tk.END, "=" * 50 + "\\n")
        
        for category, category_results in results.items():
            if category == '_summary':
                continue
                
            self.results_text.insert(tk.END, f"\\n[{category.upper()}]\\n")
            self.results_text.insert(tk.END, "-" * 30 + "\\n")
            
            for query, query_results in category_results.items():
                self.results_text.insert(tk.END, f"\\nQuery: {query}\\n")
                self.results_text.insert(tk.END, f"Results: {len(query_results)}\\n")
                
                for result in query_results[:3]:  # Show first 3 results
                    risk_level = result.get('analysis', {}).get('risk_level', 'low')
                    risk_emoji = "🔴" if risk_level == 'high' else "🟡" if risk_level == 'medium' else "🟢"
                    
                    self.results_text.insert(tk.END, f"  {risk_emoji} {result['title']}\\n")
                    self.results_text.insert(tk.END, f"     {result['url']}\\n")
                
                if len(query_results) > 3:
                    self.results_text.insert(tk.END, f"     ... and {len(query_results) - 3} more results\\n")
    
    def start_bulk_scan(self):
        """Start bulk scanning"""
        domains_text = self.bulk_domains_text.get(1.0, tk.END).strip()
        if not domains_text:
            messagebox.showerror("Error", "Please enter domains to scan")
            return
        
        domains = [d.strip() for d in domains_text.split('\\n') if d.strip()]
        if not domains:
            messagebox.showerror("Error", "No valid domains found")
            return
        
        # Start bulk scan in thread
        self.bulk_scan_button.config(state=tk.DISABLED)
        self.bulk_progress_bar.config(mode='determinate', maximum=len(domains), value=0)
        
        bulk_thread = threading.Thread(target=self.run_bulk_scan, args=(domains,))
        bulk_thread.daemon = True
        bulk_thread.start()
    
    def run_bulk_scan(self, domains):
        """Run bulk scanning"""
        try:
            def progress_callback(completed, total, domain, result):
                # Update progress bar
                self.master.after(0, lambda: self.bulk_progress_bar.config(value=completed))
                
                # Update status
                status = f"[{completed}/{total}] Scanning {domain}..."
                self.master.after(0, lambda: self.bulk_status_label.config(text=status))
            
            self.master.after(0, lambda: self.bulk_status_label.config(text="Starting bulk scan..."))
            
            # Run fast bulk scan
            results = self.fast_scanner.bulk_scan(domains, progress_callback)
            
            # Display results
            report = self.fast_scanner.generate_quick_report()
            
            self.master.after(0, lambda: self.bulk_results_text.delete(1.0, tk.END))
            self.master.after(0, lambda: self.bulk_results_text.insert(tk.END, report))
            
            self.master.after(0, lambda: self.bulk_status_label.config(text="Bulk scan completed!"))
            
        except Exception as e:
            error_msg = f"Bulk scan failed: {str(e)}"
            self.master.after(0, lambda: self.bulk_status_label.config(text=error_msg))
            logging.error(error_msg)
        
        finally:
            self.master.after(0, lambda: self.bulk_scan_button.config(state=tk.NORMAL))
    
    def load_domains_from_file(self):
        """Load domains from a file"""
        filepath = filedialog.askopenfilename(
            title="Select domains file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    domains = f.read()
                
                self.bulk_domains_text.delete(1.0, tk.END)
                self.bulk_domains_text.insert(tk.END, domains)
                
                messagebox.showinfo("Success", f"Domains loaded from {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load domains: {e}")
    
    def stop_scan(self):
        """Stop current scan"""
        self.is_scanning = False
        self.update_status("⏹️ Scan stopped by user")
        self.reset_scan_ui()
    
    def reset_scan_ui(self):
        """Reset scan UI to ready state"""
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
    
    def update_status(self, message):
        """Update status label"""
        self.master.after(0, lambda: self.status_label.config(text=message))
        logging.info(message)
    
    def save_results(self):
        """Save current results to file"""
        if not self.current_results:
            messagebox.showwarning("Warning", "No results to save")
            return
            
        filepath = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                if filepath.endswith('.json'):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=2, ensure_ascii=False)
                else:
                    # Save as text
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(self.results_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"Results saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {e}")
    
    def save_bulk_results(self):
        """Save bulk results to file"""
        if not hasattr(self.fast_scanner, 'results') or not self.fast_scanner.results:
            messagebox.showwarning("Warning", "No bulk results to save")
            return
        
        filepath = self.fast_scanner.save_results()
        messagebox.showinfo("Success", f"Bulk results saved to {filepath}")

def main():
    root = tk.Tk()
    app = OptimizedDorkingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
