"""
Enhanced Main GUI Application for MissDorking Tool 
With bulk domains, smart file naming, flexible reports, and fun visual elements! 😄
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import logging
from datetime import datetime
import os
import sys
import webbrowser
import re

# Import our modules
from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
from scraper import GoogleScraper
from alternative_scraper import AlternativeScraper
from hybrid_scraper_fixed import HybridScraper
from export import ResultExporter
from analysis import ResultAnalyzer

class EnhancedDorkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MissDorking™ - Enhanced Google Dorking Tool 💋🍒")
        self.root.geometry("1200x800")
        
        # Set up logging
        self.setup_logging()
        
        # Initialize components
        self.scraper = GoogleScraper()
        self.exporter = ResultExporter()
        self.analyzer = ResultAnalyzer()
        self.results = {}
        self.bulk_results = {}  # Store results for multiple domains
        self.is_running = False
        self.current_domain = ""
        
        # Create GUI
        self.create_widgets()
        
        # Configure styles
        self.setup_styles()
        
        logging.info("Enhanced MissDorking application initialized successfully")
    
    def setup_logging(self):
        """Set up logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('missdorking_enhanced.log'),
                logging.StreamHandler()
            ]
        )
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Run.TButton', font=('Arial', 10, 'bold'))
        style.configure('Export.TButton', font=('Arial', 9))
        style.configure('Bulk.TButton', font=('Arial', 10, 'bold'), foreground='purple')
        
        # Configure progress bar style
        style.configure('Custom.Horizontal.TProgressbar', thickness=25)
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Single Domain tab
        self.create_single_domain_tab()
        
        # Bulk Domains tab
        self.create_bulk_domains_tab()
        
    def create_single_domain_tab(self):
        """Create the single domain scanning tab"""
        single_frame = ttk.Frame(self.notebook)
        self.notebook.add(single_frame, text="🎯 Single Domain")
        
        # Main container
        main_frame = ttk.Frame(single_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title with enhanced visual elements (adding the requested "enhancements" 😄)
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Fun title with ASCII art "enhancements"
        title_text = """
    💋 MissDorking™ - Enhanced Dorking Tool 🍒
    ╔═══════════════════════════════════════╗
    ║  😘  Making Security Fun & Fabulous!  💅 ║
    ╚═══════════════════════════════════════╝
        """
        
        title_label = tk.Label(title_frame, text=title_text, font=('Courier', 12, 'bold'), 
                              fg='hotpink', justify=tk.CENTER)
        title_label.pack()
        
        # Domain input section
        input_frame = ttk.LabelFrame(main_frame, text="🎯 Target Configuration", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Target Domain:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.domain_var = tk.StringVar()
        self.domain_entry = ttk.Entry(input_frame, textvariable=self.domain_var, 
                                     font=('Arial', 10), width=40)
        self.domain_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        self.domain_entry.bind('<Return>', self.on_enter_pressed)
        
        # Run button
        self.run_button = ttk.Button(input_frame, text="🚀 Start Dorking", 
                                    command=self.start_single_dorking, style='Run.TButton')
        self.run_button.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Scan Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Results per query
        ttk.Label(options_frame, text="Results per query:").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        
        self.results_per_query_var = tk.StringVar(value="10")
        results_spinbox = ttk.Spinbox(options_frame, from_=1, to=50, width=10,
                                     textvariable=self.results_per_query_var)
        results_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Delay between requests
        ttk.Label(options_frame, text="Delay between requests (seconds):").grid(
            row=0, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        
        self.delay_var = tk.StringVar(value="2-4")
        delay_entry = ttk.Entry(options_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Category selection
        ttk.Label(options_frame, text="Categories to scan:").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        
        self.categories_frame = ttk.Frame(options_frame)
        self.categories_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), 
                                  padx=(10, 0), pady=5)
        
        self.category_vars = {}
        self.create_category_checkboxes()
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to start...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                           style='Custom.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="📋 Scan Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80,
                                                     font=('Courier', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Export buttons frame
        export_frame = ttk.Frame(results_frame)
        export_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.export_pdf_button = ttk.Button(export_frame, text="📄 Export PDF",
                                           command=self.export_single_pdf, style='Export.TButton')
        self.export_pdf_button.grid(row=0, column=0, padx=(0, 10))
        self.export_pdf_button.config(state='disabled')
        
        self.export_csv_button = ttk.Button(export_frame, text="📊 Export CSV",
                                           command=self.export_single_csv, style='Export.TButton')
        self.export_csv_button.grid(row=0, column=1, padx=(0, 10))
        self.export_csv_button.config(state='disabled')
        
        self.clear_results_button = ttk.Button(export_frame, text="🗑️ Clear Results",
                                              command=self.clear_results, style='Export.TButton')
        self.clear_results_button.grid(row=0, column=2, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Ready - {get_dork_count()} dork queries available 💋")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief='sunken', font=('Arial', 8))
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_bulk_domains_tab(self):
        """Create the bulk domains scanning tab"""
        bulk_frame = ttk.Frame(self.notebook)
        self.notebook.add(bulk_frame, text="🎯 Bulk Domains")
        
        # Main container
        main_frame = ttk.Frame(bulk_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="👑 Bulk Domain Dorking - Dominate Multiple Sites! 💪", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="📋 Domain List & Options", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(0, weight=1)
        
        # Domain list input
        ttk.Label(input_frame, text="Enter domains to scan (one per line):", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.bulk_domains_text = scrolledtext.ScrolledText(input_frame, height=8, 
                                                          font=('Arial', 10))
        self.bulk_domains_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.bulk_domains_text.insert(tk.END, "example.com\ngoogle.com\ngithub.com")
        
        # Bulk options frame
        bulk_options_frame = ttk.Frame(input_frame)
        bulk_options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        bulk_options_frame.columnconfigure(1, weight=1)
        
        # Report options
        ttk.Label(bulk_options_frame, text="Report Format:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.report_format_var = tk.StringVar(value="individual")
        report_frame = ttk.Frame(bulk_options_frame)
        report_frame.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Radiobutton(report_frame, text="📄 Individual reports per domain", 
                       variable=self.report_format_var, value="individual").pack(anchor=tk.W)
        ttk.Radiobutton(report_frame, text="📊 Single combined report for all", 
                       variable=self.report_format_var, value="combined").pack(anchor=tk.W)
        ttk.Radiobutton(report_frame, text="📋 Both individual and combined", 
                       variable=self.report_format_var, value="both").pack(anchor=tk.W)
        
        # Load domains button
        load_button = ttk.Button(bulk_options_frame, text="📁 Load from File",
                               command=self.load_domains_from_file)
        load_button.grid(row=0, column=2, padx=(20, 0))
        
        # Bulk control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        self.bulk_run_button = ttk.Button(button_frame, text="🚀 Start Bulk Dorking",
                                         command=self.start_bulk_dorking, style='Bulk.TButton')
        self.bulk_run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.bulk_stop_button = ttk.Button(button_frame, text="⏹️ Stop Bulk Scan",
                                          command=self.stop_bulk_dorking, state='disabled')
        self.bulk_stop_button.pack(side=tk.LEFT)
        
        # Progress section
        bulk_progress_frame = ttk.LabelFrame(main_frame, text="📊 Bulk Progress", padding="10")
        bulk_progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        bulk_progress_frame.columnconfigure(0, weight=1)
        
        self.bulk_progress_var = tk.StringVar(value="Ready for bulk scanning...")
        self.bulk_progress_label = ttk.Label(bulk_progress_frame, textvariable=self.bulk_progress_var)
        self.bulk_progress_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.bulk_progress_bar = ttk.Progressbar(bulk_progress_frame, mode='determinate',
                                               style='Custom.Horizontal.TProgressbar')
        self.bulk_progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Results section
        bulk_results_frame = ttk.LabelFrame(main_frame, text="📋 Bulk Results", padding="10")
        bulk_results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        bulk_results_frame.columnconfigure(0, weight=1)
        bulk_results_frame.rowconfigure(0, weight=1)
        
        # Bulk results text area
        self.bulk_results_text = scrolledtext.ScrolledText(bulk_results_frame, height=15, width=80,
                                                          font=('Courier', 9))
        self.bulk_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Bulk export buttons
        bulk_export_frame = ttk.Frame(bulk_results_frame)
        bulk_export_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.bulk_export_pdf_button = ttk.Button(bulk_export_frame, text="📄 Export Bulk PDF",
                                                command=self.export_bulk_pdf, style='Export.TButton')
        self.bulk_export_pdf_button.grid(row=0, column=0, padx=(0, 10))
        self.bulk_export_pdf_button.config(state='disabled')
        
        self.bulk_export_csv_button = ttk.Button(bulk_export_frame, text="📊 Export Bulk CSV",
                                                command=self.export_bulk_csv, style='Export.TButton')
        self.bulk_export_csv_button.grid(row=0, column=1, padx=(0, 10))
        self.bulk_export_csv_button.config(state='disabled')
        
        self.bulk_clear_button = ttk.Button(bulk_export_frame, text="🗑️ Clear Results",
                                           command=self.clear_bulk_results, style='Export.TButton')
        self.bulk_clear_button.grid(row=0, column=2, padx=(0, 10))
    
    def create_category_checkboxes(self):
        """Create checkboxes for each dork category"""
        row = 0
        col = 0
        max_cols = 3
        
        for category in GOOGLE_DORKS.keys():
            var = tk.BooleanVar(value=True)  # All categories selected by default
            self.category_vars[category] = var
            
            checkbox = ttk.Checkbutton(self.categories_frame, text=category, variable=var)
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 15), pady=2)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
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
    
    def on_enter_pressed(self, event):
        """Handle Enter key press in domain entry"""
        if not self.is_running:
            self.start_single_dorking()
    
    def start_single_dorking(self):
        """Start single domain dorking"""
        if self.is_running:
            messagebox.showwarning("Warning", "Dorking is already in progress.")
            return
        
        domain = self.domain_var.get().strip()
        if not domain:
            messagebox.showerror("Error", "Please enter a target domain.")
            return
        
        if not self.validate_inputs():
            return
        
        self.current_domain = domain
        self.is_running = True
        self.run_button.config(state='disabled', text='Running...')
        self.export_pdf_button.config(state='disabled')
        self.export_csv_button.config(state='disabled')
        
        # Start dorking in separate thread
        thread = threading.Thread(target=self.run_single_dorking)
        thread.daemon = True
        thread.start()
    
    def start_bulk_dorking(self):
        """Start bulk domain dorking"""
        if self.is_running:
            messagebox.showwarning("Warning", "Bulk dorking is already in progress.")
            return
        
        domains_text = self.bulk_domains_text.get(1.0, tk.END).strip()
        if not domains_text:
            messagebox.showerror("Error", "Please enter domains to scan.")
            return
        
        # Parse domains
        domains = [d.strip() for d in domains_text.split('\n') if d.strip()]
        if not domains:
            messagebox.showerror("Error", "No valid domains found.")
            return
        
        self.bulk_domains = domains
        self.bulk_results = {}
        self.is_running = True
        
        # Update UI
        self.bulk_run_button.config(state='disabled', text='Running...')
        self.bulk_stop_button.config(state='normal')
        self.bulk_export_pdf_button.config(state='disabled')
        self.bulk_export_csv_button.config(state='disabled')
        
        # Start bulk dorking in separate thread
        thread = threading.Thread(target=self.run_bulk_dorking)
        thread.daemon = True
        thread.start()
    
    def validate_inputs(self):
        """Validate user inputs"""
        domain = self.domain_var.get().strip()
        if not domain:
            messagebox.showerror("Error", "Please enter a target domain.")
            return False
        
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.replace('www.', '')
        self.domain_var.set(domain)
        
        # Validate delay format
        delay_str = self.delay_var.get().strip()
        try:
            if '-' in delay_str:
                min_delay, max_delay = map(float, delay_str.split('-'))
                if min_delay >= max_delay or min_delay < 0:
                    raise ValueError
                self.scraper.delay_range = (min_delay, max_delay)
            else:
                delay = float(delay_str)
                if delay < 0:
                    raise ValueError
                self.scraper.delay_range = (delay, delay)
        except ValueError:
            messagebox.showerror("Error", "Invalid delay format. Use single number or range (e.g., '2-5').")
            return False
        
        # Check if at least one category is selected
        if not any(var.get() for var in self.category_vars.values()):
            messagebox.showerror("Error", "Please select at least one category to scan.")
            return False
        
        return True
    
    def run_single_dorking(self):
        """Run single domain dorking process"""
        try:
            domain = self.current_domain
            max_results = int(self.results_per_query_var.get())
            
            # Get selected categories
            selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
            
            # Get all dorks for domain
            all_dorks = get_all_dorks_for_domain(domain)
            
            # Filter by selected categories
            filtered_dorks = {cat: dorks for cat, dorks in all_dorks.items() 
                            if cat in selected_categories}
            
            # Flatten queries for progress tracking
            all_queries = []
            for category, dorks in filtered_dorks.items():
                all_queries.extend(dorks)
            
            total_queries = len(all_queries)
            
            self.root.after(0, lambda: self.progress_bar.config(maximum=total_queries))
            self.root.after(0, lambda: self.progress_var.set(f"Starting scan of {domain}..."))
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            
            results = {}
            current_query = 0
            
            for category, dorks in filtered_dorks.items():
                if not self.is_running:
                    break
                    
                category_results = {}
                
                self.root.after(0, lambda c=category: self.append_to_results(f"\\n=== {c} ===\\n"))
                
                for dork in dorks:
                    if not self.is_running:
                        break
                        
                    current_query += 1
                    
                    # Update progress
                    self.root.after(0, lambda q=current_query, t=total_queries, d=dork: 
                                   self.update_progress(q, t, d))
                    
                    # Search Google
                    search_results = self.scraper.search_google(dork, max_results)
                    category_results[dork] = search_results
                    
                    # Update results display
                    result_count = len(search_results)
                    self.root.after(0, lambda d=dork, c=result_count: 
                                   self.append_to_results(f"{d}: {c} results\\n"))
                    
                    if search_results:
                        for result in search_results[:3]:  # Show first 3 results
                            self.root.after(0, lambda r=result: 
                                           self.append_to_results(f"  • {r['title'][:80]}...\\n    {r['url']}\\n"))
                        
                        if result_count > 3:
                            self.root.after(0, lambda c=result_count: 
                                           self.append_to_results(f"  ... and {c-3} more results\\n"))
                    
                    self.root.after(0, lambda: self.append_to_results("\\n"))
                
                results[category] = category_results
            
            # Store results
            self.results = results
            
            # Enhanced completion message
            total_results = sum(sum(len(results) for results in cat.values()) 
                              for cat in results.values())
            
            fun_messages = [
                f"💄 Scan complete for {domain}! Found {total_results} fabulous results! 💋",
                f"👠 All done dorking {domain}! {total_results} targets acquired with style! ✨",
                f"🔥 Mission accomplished for {domain}! {total_results} results ready for your viewing pleasure! 💅"
            ]
            
            import random
            completion_message = random.choice(fun_messages)
            
            self.root.after(0, lambda: self.progress_var.set(completion_message))
            self.root.after(0, lambda: self.append_to_results(f"\\n=== SCAN COMPLETE ===\\n{completion_message}\\n"))
            
            logging.info(f"Single domain dorking completed for {domain}. Total results: {total_results}")
            
        except Exception as e:
            error_msg = f"Error during dorking: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            logging.error(error_msg)
            
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.run_button.config(state='normal', text='🚀 Start Dorking'))
            self.root.after(0, lambda: self.export_pdf_button.config(state='normal'))
            self.root.after(0, lambda: self.export_csv_button.config(state='normal'))
    
    def run_bulk_dorking(self):
        """Run bulk domain dorking process"""
        try:
            domains = self.bulk_domains
            total_domains = len(domains)
            
            self.root.after(0, lambda: self.bulk_progress_bar.config(maximum=total_domains))
            self.root.after(0, lambda: self.bulk_results_text.delete(1.0, tk.END))
            
            scan_start_time = datetime.now()
            
            for i, domain in enumerate(domains):
                if not self.is_running:
                    break
                
                self.current_domain = domain
                
                # Update progress
                self.root.after(0, lambda d=domain, i=i, t=total_domains: 
                               self.bulk_progress_var.set(f"Scanning {d} ({i+1}/{t})..."))
                self.root.after(0, lambda i=i: self.bulk_progress_bar.config(value=i))
                
                # Add domain header to results
                self.root.after(0, lambda d=domain: 
                               self.append_to_bulk_results(f"\\n{'='*60}\\n🎯 SCANNING: {d}\\n{'='*60}\\n"))
                
                try:
                    # Run dorking for this domain
                    domain_results = self.scan_single_domain_for_bulk(domain)
                    self.bulk_results[domain] = {
                        'results': domain_results,
                        'scan_time': datetime.now(),
                        'success': True
                    }
                    
                    # Show summary for this domain
                    total_results = sum(sum(len(results) for results in cat.values()) 
                                      for cat in domain_results.values())
                    
                    self.root.after(0, lambda d=domain, t=total_results: 
                                   self.append_to_bulk_results(f"✅ {d} completed: {t} results found\\n\\n"))
                    
                except Exception as e:
                    logging.error(f"Error scanning {domain}: {e}")
                    self.bulk_results[domain] = {
                        'results': {},
                        'scan_time': datetime.now(),
                        'success': False,
                        'error': str(e)
                    }
                    
                    self.root.after(0, lambda d=domain, e=str(e): 
                                   self.append_to_bulk_results(f"❌ {d} failed: {e}\\n\\n"))
            
            # Final progress update
            self.root.after(0, lambda: self.bulk_progress_bar.config(value=total_domains))
            
            # Generate summary
            successful_scans = sum(1 for result in self.bulk_results.values() if result['success'])
            failed_scans = total_domains - successful_scans
            total_results = sum(
                sum(sum(len(results) for results in cat.values()) 
                    for cat in domain_result['results'].values())
                for domain_result in self.bulk_results.values() if domain_result['success']
            )
            
            scan_duration = datetime.now() - scan_start_time
            
            summary = f"""
{'='*60}
🎉 BULK SCAN COMPLETE! 🎉
{'='*60}
📊 Summary:
   • Total domains scanned: {total_domains}
   • Successful scans: {successful_scans}
   • Failed scans: {failed_scans}
   • Total results found: {total_results}
   • Scan duration: {scan_duration}
   
💋 MissDorking says: "Bulk dorking complete with fabulous results!" 💅
"""
            
            self.root.after(0, lambda: self.append_to_bulk_results(summary))
            self.root.after(0, lambda: self.bulk_progress_var.set(f"Bulk scan complete! {successful_scans}/{total_domains} domains successful"))
            
            # Generate reports based on user selection
            if self.is_running:  # Only if not stopped by user
                self.generate_bulk_reports()
            
        except Exception as e:
            error_msg = f"Error during bulk dorking: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            logging.error(error_msg)
            
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.bulk_run_button.config(state='normal', text='🚀 Start Bulk Dorking'))
            self.root.after(0, lambda: self.bulk_stop_button.config(state='disabled'))
            self.root.after(0, lambda: self.bulk_export_pdf_button.config(state='normal'))
            self.root.after(0, lambda: self.bulk_export_csv_button.config(state='normal'))
    
    def scan_single_domain_for_bulk(self, domain):
        """Scan a single domain as part of bulk operation"""
        max_results = int(self.results_per_query_var.get())
        
        # Get selected categories
        selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
        
        # Get all dorks for domain
        all_dorks = get_all_dorks_for_domain(domain)
        
        # Filter by selected categories
        filtered_dorks = {cat: dorks for cat, dorks in all_dorks.items() 
                        if cat in selected_categories}
        
        results = {}
        
        for category, dorks in filtered_dorks.items():
            if not self.is_running:
                break
                
            category_results = {}
            
            for dork in dorks:
                if not self.is_running:
                    break
                    
                # Search Google
                search_results = self.scraper.search_google(dork, max_results)
                category_results[dork] = search_results
            
            results[category] = category_results
        
        return results
    
    def generate_bulk_reports(self):
        """Generate bulk reports based on user selection"""
        report_format = self.report_format_var.get()
        
        if report_format in ['individual', 'both']:
            # Generate individual reports for each domain
            for domain, domain_data in self.bulk_results.items():
                if domain_data['success']:
                    self.generate_individual_report(domain, domain_data)
        
        if report_format in ['combined', 'both']:
            # Generate combined report
            self.generate_combined_report()
    
    def generate_individual_report(self, domain, domain_data):
        """Generate individual report for a domain"""
        try:
            scan_time = domain_data['scan_time']
            results = domain_data['results']
            
            # Generate PDF
            filename = self.generate_filename(domain, 'pdf', scan_date=scan_time)
            filepath = self.exporter.export_to_pdf(results, domain, filename)
            
            logging.info(f"Individual PDF report generated for {domain}: {filepath}")
            
        except Exception as e:
            logging.error(f"Error generating individual report for {domain}: {e}")
    
    def generate_combined_report(self):
        """Generate combined report for all domains"""
        try:
            # Combine all results
            combined_results = {}
            
            for domain, domain_data in self.bulk_results.items():
                if domain_data['success']:
                    results = domain_data['results']
                    
                    for category, category_results in results.items():
                        if category not in combined_results:
                            combined_results[category] = {}
                        
                        # Prefix queries with domain name
                        for query, query_results in category_results.items():
                            prefixed_query = f"[{domain}] {query}"
                            combined_results[category][prefixed_query] = query_results
            
            # Generate PDF
            filename = self.generate_filename("ALL_DOMAINS", 'pdf', is_bulk=True)
            filepath = self.exporter.export_to_pdf(combined_results, "Bulk Scan", filename)
            
            logging.info(f"Combined PDF report generated: {filepath}")
            
        except Exception as e:
            logging.error(f"Error generating combined report: {e}")
    
    def stop_bulk_dorking(self):
        """Stop bulk dorking process"""
        self.is_running = False
        self.bulk_progress_var.set("Bulk scan stopped by user")
        logging.info("Bulk dorking stopped by user")
    
    def load_domains_from_file(self):
        """Load domains from a text file"""
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
    
    def update_progress(self, current, total, query):
        """Update progress bar and label"""
        self.progress_bar.config(value=current)
        self.progress_var.set(f"Query {current}/{total}: {query[:60]}...")
        self.status_var.set(f"Processing query {current} of {total}")
    
    def append_to_results(self, text):
        """Append text to results display"""
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.results_text.update()
    
    def append_to_bulk_results(self, text):
        """Append text to bulk results display"""
        self.bulk_results_text.insert(tk.END, text)
        self.bulk_results_text.see(tk.END)
        self.bulk_results_text.update()
    
    def export_single_pdf(self):
        """Export single domain results to PDF"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        try:
            domain = self.current_domain
            filename = self.generate_filename(domain, 'pdf')
            filepath = self.exporter.export_to_pdf(self.results, domain, filename)
            messagebox.showinfo("Success", f"PDF report saved to:\\n{filepath}")
            
            # Ask to open file
            if messagebox.askyesno("Open File", "Would you like to open the PDF file?"):
                if sys.platform.startswith('win'):
                    os.startfile(filepath)
                else:
                    webbrowser.open(f'file://{filepath}')
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting PDF: {str(e)}")
    
    def export_single_csv(self):
        """Export single domain results to CSV"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        try:
            domain = self.current_domain
            filename = self.generate_filename(domain, 'csv')
            filepath = self.exporter.export_to_csv(self.results, domain, filename)
            messagebox.showinfo("Success", f"CSV report saved to:\\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting CSV: {str(e)}")
    
    def export_bulk_pdf(self):
        """Export bulk results to PDF"""
        if not self.bulk_results:
            messagebox.showwarning("Warning", "No bulk results to export.")
            return
        
        # Use the same logic as generate_combined_report
        self.generate_combined_report()
        messagebox.showinfo("Success", "Bulk PDF reports generated successfully!")
    
    def export_bulk_csv(self):
        """Export bulk results to CSV"""
        if not self.bulk_results:
            messagebox.showwarning("Warning", "No bulk results to export.")
            return
        
        try:
            # Generate CSV for each domain
            for domain, domain_data in self.bulk_results.items():
                if domain_data['success']:
                    scan_time = domain_data['scan_time']
                    results = domain_data['results']
                    
                    filename = self.generate_filename(domain, 'csv', scan_date=scan_time)
                    filepath = self.exporter.export_to_csv(results, domain, filename)
                    
            messagebox.showinfo("Success", "Bulk CSV reports generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting bulk CSV: {str(e)}")
    
    def clear_results(self):
        """Clear single domain results"""
        self.results_text.delete(1.0, tk.END)
        self.results = {}
        self.progress_bar.config(value=0)
        self.progress_var.set("Ready to start...")
        self.status_var.set(f"Ready - {get_dork_count()} dork queries available 💋")
        self.export_pdf_button.config(state='disabled')
        self.export_csv_button.config(state='disabled')
    
    def clear_bulk_results(self):
        """Clear bulk results"""
        self.bulk_results_text.delete(1.0, tk.END)
        self.bulk_results = {}
        self.bulk_progress_bar.config(value=0)
        self.bulk_progress_var.set("Ready for bulk scanning...")
        self.bulk_export_pdf_button.config(state='disabled')
        self.bulk_export_csv_button.config(state='disabled')


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    try:
        app = EnhancedDorkingApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Fatal Error", f"An unexpected error occurred:\\n{e}")


if __name__ == "__main__":
    main()
