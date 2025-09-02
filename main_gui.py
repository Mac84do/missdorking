"""
Main GUI Application for Google Dorking Tool
Cross-platform GUI using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import logging
from datetime import datetime
import os
import sys
import webbrowser

# Import our modules
from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
from scraper import GoogleScraper
from export import ResultExporter
from analysis import ResultAnalyzer
from splash_screen import show_splash_screen

class DorkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Dorking Tool - MissDorking")
        self.root.geometry("1000x700")
        
        # Set up logging
        self.setup_logging()
        
        # Initialize components
        self.scraper = GoogleScraper()
        self.exporter = ResultExporter()
        self.analyzer = ResultAnalyzer()
        self.results = {}
        self.is_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Configure styles
        self.setup_styles()
        
        logging.info("Application initialized successfully")
    
    def setup_logging(self):
        """Set up logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('dorking_app.log'),
                logging.StreamHandler()
            ]
        )
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Run.TButton', font=('Arial', 10, 'bold'))
        style.configure('Export.TButton', font=('Arial', 9))
        
        # Configure progress bar style
        style.configure('Custom.Horizontal.TProgressbar', thickness=20)
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title with playful touch
        title_label = ttk.Label(main_frame, text="MissDorking™ - Google Dorking Tool 💋", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Domain input section
        ttk.Label(main_frame, text="Target Domain:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        self.domain_var = tk.StringVar()
        self.domain_entry = ttk.Entry(main_frame, textvariable=self.domain_var, 
                                     font=('Arial', 10), width=40)
        self.domain_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        self.domain_entry.bind('<Return>', self.on_enter_pressed)
        
        # Run button
        self.run_button = ttk.Button(main_frame, text="Start Dorking", 
                                    command=self.start_dorking, style='Run.TButton')
        self.run_button.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
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
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to start...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                           style='Custom.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
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
        
        self.export_pdf_button = ttk.Button(export_frame, text="Export PDF",
                                           command=self.export_pdf, style='Export.TButton')
        self.export_pdf_button.grid(row=0, column=0, padx=(0, 10))
        self.export_pdf_button.config(state='disabled')
        
        self.export_csv_button = ttk.Button(export_frame, text="Export CSV",
                                           command=self.export_csv, style='Export.TButton')
        self.export_csv_button.grid(row=0, column=1, padx=(0, 10))
        self.export_csv_button.config(state='disabled')
        
        self.clear_results_button = ttk.Button(export_frame, text="Clear Results",
                                              command=self.clear_results, style='Export.TButton')
        self.clear_results_button.grid(row=0, column=2, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Ready - {get_dork_count()} dork queries available")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief='sunken', font=('Arial', 8))
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
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
    
    def on_enter_pressed(self, event):
        """Handle Enter key press in domain entry"""
        if not self.is_running:
            self.start_dorking()
    
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
    
    def start_dorking(self):
        """Start the dorking process in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Warning", "Dorking is already in progress.")
            return
        
        if not self.validate_inputs():
            return
        
        self.is_running = True
        self.run_button.config(state='disabled', text='Running...')
        self.export_pdf_button.config(state='disabled')
        self.export_csv_button.config(state='disabled')
        
        # Start dorking in separate thread
        thread = threading.Thread(target=self.run_dorking)
        thread.daemon = True
        thread.start()
    
    def run_dorking(self):
        """Run the dorking process"""
        try:
            domain = self.domain_var.get().strip()
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
                category_results = {}
                
                self.root.after(0, lambda c=category: self.append_to_results(f"\n=== {c} ===\n"))
                
                for dork in dorks:
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
                                   self.append_to_results(f"{d}: {c} results\n"))
                    
                    if search_results:
                        for result in search_results[:3]:  # Show first 3 results
                            self.root.after(0, lambda r=result: 
                                           self.append_to_results(f"  • {r['title'][:80]}...\n    {r['url']}\n"))
                        
                        if result_count > 3:
                            self.root.after(0, lambda c=result_count: 
                                           self.append_to_results(f"  ... and {c-3} more results\n"))
                    
                    self.root.after(0, lambda: self.append_to_results("\n"))
                
                results[category] = category_results
                
            # Perform enhanced analysis on results
            self.root.after(0, lambda: self.progress_var.set("Analyzing results for security relevance..."))
            analyzed_results = self.analyzer.categorize_results(results)
            
            # Generate and display analysis summary
            summary_report = self.analyzer.generate_report_summary(analyzed_results)
            self.root.after(0, lambda: self.append_to_results(summary_report))
            
            self.results = analyzed_results
            
            # Completion with fun messages
            total_results = sum(sum(len(results) for results in cat.values()) 
                              for cat in results.values())
            
            # Get summary stats
            summary = analyzed_results.get('_summary', {})
            high_risk_count = summary.get('high_risk_count', 0)
            login_count = summary.get('login_pages_count', 0)
            
            # Enhanced completion messages with analysis
            fun_messages = [
                f"💄 Scan complete! Found {total_results} results ({high_risk_count} high-risk, {login_count} login pages)! 💋",
                f"👠 Done dorking around! {total_results} results ready ({high_risk_count} critical findings)! ✨",
                f"🔥 Mission accomplished! {total_results} targets acquired ({login_count} login portals found)! 💅",
                f"💎 All done, darling! {total_results} beautiful results ({high_risk_count} high-priority)! 😘",
                f"🌟 Finished with style! {total_results} results analyzed and prioritized! 💖"
            ]
            
            import random
            fun_message = random.choice(fun_messages)
            
            self.root.after(0, lambda: self.progress_var.set(fun_message))
            self.root.after(0, lambda: self.append_to_results(f"\n=== SCAN COMPLETE ===\n{fun_message}\n\n💋 MissDorking says: 'Hope you enjoyed the show!' 💋\n"))
            
            logging.info(f"Dorking completed for {domain}. Total results: {total_results}")
            
        except Exception as e:
            error_msg = f"Error during dorking: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            logging.error(error_msg)
            
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.run_button.config(state='normal', text='Start Dorking'))
            self.root.after(0, lambda: self.export_pdf_button.config(state='normal'))
            self.root.after(0, lambda: self.export_csv_button.config(state='normal'))
    
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
    
    def export_pdf(self):
        """Export results to PDF"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        try:
            domain = self.domain_var.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save PDF Report"
            )
            
            if filename:
                filepath = self.exporter.export_to_pdf(self.results, domain, filename)
                messagebox.showinfo("Success", f"PDF report saved to:\n{filepath}")
                
                # Ask to open file
                if messagebox.askyesno("Open File", "Would you like to open the PDF file?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
                logging.info(f"PDF report exported: {filepath}")
                
        except Exception as e:
            error_msg = f"Error exporting PDF: {str(e)}"
            messagebox.showerror("Error", error_msg)
            logging.error(error_msg)
    
    def export_csv(self):
        """Export results to CSV"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        try:
            domain = self.domain_var.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save CSV Report"
            )
            
            if filename:
                filepath = self.exporter.export_to_csv(self.results, domain, filename)
                messagebox.showinfo("Success", f"CSV report saved to:\n{filepath}")
                
                # Ask to open file
                if messagebox.askyesno("Open File", "Would you like to open the CSV file?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
                logging.info(f"CSV report exported: {filepath}")
                
        except Exception as e:
            error_msg = f"Error exporting CSV: {str(e)}"
            messagebox.showerror("Error", error_msg)
            logging.error(error_msg)
    
    def clear_results(self):
        """Clear results display"""
        self.results_text.delete(1.0, tk.END)
        self.results = {}
        self.progress_bar.config(value=0)
        self.progress_var.set("Ready to start...")
        self.status_var.set(f"Ready - {get_dork_count()} dork queries available")
        self.export_pdf_button.config(state='disabled')
        self.export_csv_button.config(state='disabled')

def main():
    """Main application entry point"""
    
    def start_main_app():
        """Start the main application after splash screen"""
        root = tk.Tk()
        app = DorkingApp(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            logging.info("Application interrupted by user")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n{e}")
    
    # Show splash screen first, then start main app
    try:
        show_splash_screen(start_main_app)
    except Exception as e:
        # If splash fails, start main app directly
        logging.warning(f"Splash screen failed: {e}")
        start_main_app()

if __name__ == "__main__":
    main()
