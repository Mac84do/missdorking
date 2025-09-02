"""
Super Fast MissDorking GUI - LUDICROUS SPEED Edition! 🚀
Optimized for maximum speed with humor and fun elements to make you smile!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import json
from pathlib import Path

# Import our optimized modules
from hybrid_scraper_fixed import HybridScraper
from fast_bulk_scanner import FastBulkScanner
from analysis import ResultAnalyzer
try:
    from export import ResultExporter
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    print("⚠️ Export functionality not available (install reportlab for PDF export)")

class SuperFastDorkingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MissDorking™ - LUDICROUS SPEED Edition! 💋🚀")
        self.master.geometry("1200x800")
        
        # Super optimized config - NEED FOR SPEED! 🏎️
        self.config = {
            'delay_range': (0.1, 0.3),  # SUPER FAST - was (0.5, 1.5)
            'max_workers': 8,           # MORE POWER! - was 3
            'timeout': 5,               # Quick timeout - was 10
            'batch_size': 20            # Process more at once
        }
        
        # Initialize super fast components
        self.hybrid_scraper = HybridScraper(delay_range=self.config['delay_range'])
        self.fast_scanner = FastBulkScanner(
            max_workers=self.config['max_workers'], 
            delay_range=self.config['delay_range']
        )
        self.analyzer = ResultAnalyzer()
        
        # Initialize exporter if available
        if EXPORT_AVAILABLE:
            self.exporter = ResultExporter()
        else:
            self.exporter = None
        
        # State management
        self.is_scanning = False
        self.current_results = {}
        self.scan_start_time = None
        
        # Fun variables for humor! 😂
        self.fun_messages = [
            "💋 Looking for login pages like a boss babe! 💄",
            "🔥 Dorking harder than your ex! 💅",
            "👠 Scanning with style and sass! ✨", 
            "💎 Finding secrets faster than gossip spreads! 🗣️",
            "🌟 Being fabulous while hacking! 💖",
            "🎯 Targeting login pages like a sniper in heels! 👠",
            "💥 Exploding through firewalls in lipstick! 💋",
            "🦄 Magical dorking powers activated! ✨",
            "🍑 Working that code like it owes you money! 💰",
            "🌈 Rainbow hacking with glitter! ✨"
        ]
        
        self.completion_messages = [
            "💋 Finished! Hope you enjoyed the ride, honey! 😘",
            "🔥 Done and dusted! You're welcome, gorgeous! 💅",
            "✨ Mission accomplished with maximum sass! 💄",
            "💎 All done, beautiful! Time to celebrate! 🥂",
            "👑 Queen of dorking strikes again! 💋",
            "🌟 Boom! Nailed it like a pro! 💥",
            "💖 Scan complete! You're absolutely fabulous! ✨",
            "🦄 Magic happened here today! Believe it! 🌈",
            "🍑 That's how we do it in the fast lane! 🏎️",
            "💋 MissDorking says: 'You're welcome, darling!' 😘"
        ]
        
        self.setup_super_gui()
        
        # Start with a fun welcome message
        self.show_fun_welcome()
    
    def setup_super_gui(self):
        """Setup the super fast GUI with fun elements"""
        
        # Create main notebook with style
        style = ttk.Style()
        style.configure('Fun.TNotebook.Tab', padding=[20, 10])
        
        self.notebook = ttk.Notebook(self.master, style='Fun.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Speed Demon tab - for single domain ultra-fast scanning
        self.setup_speed_demon_tab()
        
        # Bulk Boss tab - for multiple domains
        self.setup_bulk_boss_tab()
        
        # Fun Config tab - for tweaking the madness
        self.setup_fun_config_tab()
    
    def setup_speed_demon_tab(self):
        """Setup the speed demon single domain tab"""
        speed_frame = ttk.Frame(self.notebook)
        self.notebook.add(speed_frame, text="⚡ SPEED DEMON")
        
        # Fun title with animations
        title_frame = ttk.Frame(speed_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.title_label = ttk.Label(
            title_frame, 
            text="💋 SPEED DEMON MODE - DORKING AT LIGHT SPEED! 🚀",
            font=('Arial', 16, 'bold'),
            foreground='hotpink'
        )
        self.title_label.pack()
        
        # Input section with style
        input_frame = ttk.LabelFrame(speed_frame, text="🎯 Target Acquisition", padding=15)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Domain input with fun placeholder
        domain_label = ttk.Label(input_frame, text="💄 Enter domain to obliterate:", font=('Arial', 11, 'bold'))
        domain_label.pack(anchor=tk.W)
        
        self.domain_entry = ttk.Entry(input_frame, font=('Arial', 12), width=50)
        self.domain_entry.pack(fill=tk.X, pady=(5, 10))
        self.domain_entry.insert(0, "daytona.co.za")
        
        # Quick options
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.turbo_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame, 
            text="🚀 TURBO MODE (Recommended for maximum sass!)",
            variable=self.turbo_mode_var
        ).pack(anchor=tk.W)
        
        self.fun_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="💋 FUN MODE (Keep the humor coming!)",
            variable=self.fun_mode_var
        ).pack(anchor=tk.W)
        
        # Action buttons with attitude
        button_frame = ttk.Frame(speed_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.scan_button = ttk.Button(
            button_frame, 
            text="💥 UNLEASH THE DORKING! 🔥", 
            command=self.start_speed_demon_scan
        )
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            button_frame, 
            text="⏹️ STAHP!", 
            command=self.stop_scan, 
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT)
        
        # Fun progress section
        progress_frame = ttk.LabelFrame(speed_frame, text="💫 Progress & Attitude", padding=15)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(progress_frame, text="Ready to rock and roll! 💋", font=('Arial', 10, 'bold'))
        self.status_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', style='TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(speed_frame, text="🏆 Spectacular Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            height=15, 
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Export buttons with sass
        export_frame = ttk.Frame(results_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(export_frame, text="💾 Save JSON", command=self.save_results).pack(side=tk.RIGHT, padx=(5, 0))
        
        if EXPORT_AVAILABLE:
            ttk.Button(export_frame, text="📊 Export CSV", command=self.export_csv).pack(side=tk.RIGHT, padx=(5, 0))
            ttk.Button(export_frame, text="📄 Export PDF", command=self.export_pdf).pack(side=tk.RIGHT, padx=(5, 0))
    
    def setup_bulk_boss_tab(self):
        """Setup the bulk boss tab for multiple domains"""
        bulk_frame = ttk.Frame(self.notebook)
        self.notebook.add(bulk_frame, text="👑 BULK BOSS")
        
        # Title
        title_label = ttk.Label(
            bulk_frame, 
            text="👑 BULK BOSS MODE - DOMINATING MULTIPLE DOMAINS! 💪",
            font=('Arial', 16, 'bold'),
            foreground='purple'
        )
        title_label.pack(pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(bulk_frame, text="📋 Domain Army List", padding=15)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(input_frame, text="💼 Enter domains to conquer (one per line):", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        self.bulk_domains_text = scrolledtext.ScrolledText(input_frame, height=8, font=('Arial', 10))
        self.bulk_domains_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        self.bulk_domains_text.insert(tk.END, "daytona.co.za\ngoogle.com\ngithub.com\nstackoverflow.com\nreddit.com")
        
        # Bulk buttons
        bulk_button_frame = ttk.Frame(input_frame)
        bulk_button_frame.pack(fill=tk.X)
        
        self.bulk_scan_button = ttk.Button(
            bulk_button_frame, 
            text="🚀 LAUNCH BULK ATTACK!", 
            command=self.start_bulk_boss_scan
        )
        self.bulk_scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            bulk_button_frame, 
            text="📁 Load Army List", 
            command=self.load_domains_from_file
        ).pack(side=tk.LEFT)
        
        # Bulk progress
        bulk_progress_frame = ttk.LabelFrame(bulk_frame, text="⚡ Bulk Domination Progress", padding=15)
        bulk_progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.bulk_status_label = ttk.Label(bulk_progress_frame, text="Ready for bulk domination! 👑", font=('Arial', 10, 'bold'))
        self.bulk_status_label.pack(anchor=tk.W)
        
        self.bulk_progress_bar = ttk.Progressbar(bulk_progress_frame, mode='determinate')
        self.bulk_progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Bulk results
        bulk_results_frame = ttk.LabelFrame(bulk_frame, text="🎊 Epic Bulk Results", padding=15)
        bulk_results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.bulk_results_text = scrolledtext.ScrolledText(bulk_results_frame, height=15, font=('Consolas', 10))
        self.bulk_results_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(bulk_results_frame, text="💾 Save Epic Results!", command=self.save_bulk_results).pack(side=tk.RIGHT, pady=(10, 0))
    
    def setup_fun_config_tab(self):
        """Setup configuration tab with personality"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ FUN CONFIG")
        
        # Title
        title_label = ttk.Label(
            config_frame, 
            text="⚙️ CONFIGURATION CENTRAL - TUNE THE MADNESS! 🎛️",
            font=('Arial', 16, 'bold'),
            foreground='darkorange'
        )
        title_label.pack(pady=10)
        
        # Speed settings
        speed_frame = ttk.LabelFrame(config_frame, text="🏎️ LUDICROUS SPEED SETTINGS", padding=15)
        speed_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Delay settings
        delay_frame = ttk.Frame(speed_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delay_frame, text="⚡ Request Delay (seconds) - Lower = Faster!", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        delay_input_frame = ttk.Frame(delay_frame)
        delay_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delay_input_frame, text="Min:").pack(side=tk.LEFT)
        self.min_delay_var = tk.DoubleVar(value=self.config['delay_range'][0])
        ttk.Entry(delay_input_frame, textvariable=self.min_delay_var, width=8).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(delay_input_frame, text="Max:").pack(side=tk.LEFT)
        self.max_delay_var = tk.DoubleVar(value=self.config['delay_range'][1])
        ttk.Entry(delay_input_frame, textvariable=self.max_delay_var, width=8).pack(side=tk.LEFT, padx=(5, 0))
        
        # Workers
        workers_frame = ttk.Frame(speed_frame)
        workers_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(workers_frame, text="👥 Parallel Workers (More = Faster!):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.max_workers_var = tk.IntVar(value=self.config['max_workers'])
        workers_scale = ttk.Scale(workers_frame, from_=1, to=16, variable=self.max_workers_var, orient=tk.HORIZONTAL)
        workers_scale.pack(fill=tk.X, pady=5)
        
        self.workers_label = ttk.Label(workers_frame, text=f"Current: {self.config['max_workers']} workers")
        self.workers_label.pack(anchor=tk.W)
        workers_scale.configure(command=self.update_workers_label)
        
        # Timeout
        timeout_frame = ttk.Frame(speed_frame)
        timeout_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(timeout_frame, text="⏱️ Request Timeout:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.timeout_var = tk.IntVar(value=self.config['timeout'])
        ttk.Entry(timeout_frame, textvariable=self.timeout_var, width=8).pack(anchor=tk.W, pady=5)
        
        # Save config
        ttk.Button(speed_frame, text="💾 Save Speed Settings!", command=self.save_super_config).pack(pady=10)
        
        # Fun stats
        stats_frame = ttk.LabelFrame(config_frame, text="📊 Performance Stats", padding=15)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=10, font=('Courier', 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        self.update_performance_stats()
    
    def show_fun_welcome(self):
        """Show a fun welcome message"""
        welcome_messages = [
            "💋 Welcome to MissDorking LUDICROUS SPEED Edition! Buckle up, buttercup! 🚀",
            "🔥 Ready to dork at the speed of light? Let's break the internet! 💥", 
            "✨ Time to hack with style, grace, and maximum sass! 💅",
            "👑 The Queen of Speed Dorking has arrived! Bow down! 💋",
            "🌟 Let's make login pages cry with our awesomeness! 😘"
        ]
        
        message = random.choice(welcome_messages)
        self.status_label.config(text=message)
        
        # Flash the title for fun
        self.animate_title()
    
    def animate_title(self):
        """Animate the title for fun"""
        colors = ['hotpink', 'purple', 'darkorange', 'red', 'blue']
        
        def flash():
            for color in colors:
                self.title_label.config(foreground=color)
                self.master.update()
                time.sleep(0.1)
        
        threading.Thread(target=flash, daemon=True).start()
    
    def update_workers_label(self, value):
        """Update workers label"""
        workers = int(float(value))
        self.workers_label.config(text=f"Current: {workers} workers")
    
    def save_super_config(self):
        """Save the super configuration"""
        try:
            self.config['delay_range'] = (self.min_delay_var.get(), self.max_delay_var.get())
            self.config['max_workers'] = int(self.max_workers_var.get())
            self.config['timeout'] = self.timeout_var.get()
            
            # Reinitialize components with new config
            self.hybrid_scraper = HybridScraper(delay_range=self.config['delay_range'])
            self.fast_scanner = FastBulkScanner(
                max_workers=self.config['max_workers'],
                delay_range=self.config['delay_range']
            )
            
            messagebox.showinfo("Configuration", "⚡ Speed settings saved! Ready for ludicrous speed! 🚀")
            self.update_performance_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def start_speed_demon_scan(self):
        """Start the speed demon single domain scan"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "💄 Please enter a domain to obliterate, darling!")
            return
        
        self.is_scanning = True
        self.scan_start_time = time.time()
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start(10)  # Faster animation
        
        # Start with a fun message
        if self.fun_mode_var.get():
            fun_msg = random.choice(self.fun_messages)
            self.update_status(fun_msg)
        
        # Start scanning in thread
        scan_thread = threading.Thread(target=self.run_speed_demon_scan, args=(domain,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def run_speed_demon_scan(self, domain):
        """Run the super fast speed demon scan"""
        try:
            self.update_status(f"🚀 LUDICROUS SPEED activated for {domain}!")
            
            all_results = {}
            total_time = 0
            
            # Use our super optimized hybrid scraper
            if self.turbo_mode_var.get():
                start_time = time.time()
                
                # Run multiple scans in parallel for even faster results!
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = [
                        executor.submit(self.hybrid_scraper.analyze_domain_directly, domain),
                        executor.submit(self.hybrid_scraper._analyze_homepage, f"https://{domain}"),
                        executor.submit(self.hybrid_scraper._check_common_login_paths, f"https://{domain}")
                    ]
                    
                    combined_results = []
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                combined_results.extend(result)
                        except Exception as e:
                            logging.error(f"Parallel scan failed: {e}")
                
                # Remove duplicates
                unique_results = []
                seen_urls = set()
                for result in combined_results:
                    if result['url'] not in seen_urls:
                        unique_results.append(result)
                        seen_urls.add(result['url'])
                
                if unique_results:
                    all_results['Login & Admin Pages'] = {
                        f'SPEED DEMON analysis of {domain}': unique_results
                    }
                
                scan_time = time.time() - start_time
                total_time += scan_time
                
                if self.fun_mode_var.get():
                    self.update_status(f"💥 BOOM! Found {len(unique_results)} pages in {scan_time:.2f}s! That's what I call SPEED! 🔥")
            
            # Analyze results super fast
            if all_results and self.is_scanning:
                analyzed_results = self.analyze_super_fast(all_results)
                self.current_results = analyzed_results
                self.display_super_results(analyzed_results, total_time, domain)
            
            # Fun completion message
            if self.fun_mode_var.get() and self.is_scanning:
                completion_msg = random.choice(self.completion_messages)
                self.update_status(completion_msg)
            else:
                self.update_status(f"✅ Speed demon scan completed in {total_time:.2f}s")
                
        except Exception as e:
            self.update_status(f"❌ Speed demon crashed: {str(e)}")
            logging.error(f"Speed demon scan error: {e}")
        
        finally:
            self.master.after(0, self.reset_scan_ui)
    
    def analyze_super_fast(self, raw_results):
        """Super fast analysis of results"""
        analyzed_results = {}
        all_login_pages = []
        total_unique_results = 0
        
        for category, category_results in raw_results.items():
            analyzed_category = {}
            
            for query, results in category_results.items():
                analyzed_query_results = []
                
                # Process in batches for speed
                batch_size = 10
                for i in range(0, len(results), batch_size):
                    batch = results[i:i+batch_size]
                    
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        futures = [executor.submit(self.analyzer.analyze_result, result.copy()) for result in batch]
                        
                        for future in as_completed(futures):
                            try:
                                analyzed_result = future.result()
                                analyzed_query_results.append(analyzed_result)
                                
                                # Collect login pages
                                analysis = analyzed_result.get('analysis', {})
                                if 'login_page' in analysis.get('categories', []):
                                    all_login_pages.append(analyzed_result)
                            except Exception as e:
                                logging.error(f"Analysis failed: {e}")
                
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
    
    def display_super_results(self, results, scan_time, domain):
        """Display results with maximum sass"""
        self.results_text.delete(1.0, tk.END)
        
        summary = results.get('_summary', {})
        
        # Super sassy header
        header = f"""🚀 SPEED DEMON RESULTS - LUDICROUS SUCCESS! 💋
{'='*60}
Domain Obliterated: {domain}
LUDICROUS SPEED Time: {scan_time:.2f} seconds ⚡
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📊 DEVASTATION SUMMARY:
💥 Total Results Found: {summary.get('total_unique_results', 0)}
🎯 Login Pages Discovered: {summary.get('login_pages_count', 0)}
🔥 High Risk Targets: {summary.get('high_risk_count', 0)}

"""
        self.results_text.insert(tk.END, header)
        
        # Priority login pages with attitude
        login_pages = summary.get('login_pages', [])
        if login_pages:
            self.results_text.insert(tk.END, "🎯 HIGH-VALUE TARGETS ACQUIRED:\\n")
            self.results_text.insert(tk.END, "=" * 50 + "\\n")
            
            for i, page in enumerate(login_pages, 1):
                risk = page.get('analysis', {}).get('risk_level', 'unknown')
                risk_emoji = "🔴" if risk == 'high' else "🟡" if risk == 'medium' else "🟢"
                
                self.results_text.insert(tk.END, f"\\n{i}. {risk_emoji} TARGET ACQUIRED: {page['title']}\\n")
                self.results_text.insert(tk.END, f"   💀 URL: {page['url']}\\n")
                
                reasoning = page.get('analysis', {}).get('reasoning', '')
                if reasoning:
                    self.results_text.insert(tk.END, f"   🧠 Intelligence: {reasoning}\\n")
        
        # Fun completion message
        if self.fun_mode_var.get():
            fun_footer = f"""
{'='*60}
💋 SPEED DEMON MODE COMPLETE! 💋
{random.choice(self.completion_messages)}

🏎️ Performance Stats:
- Speed: LUDICROUS ⚡
- Style: MAXIMUM 💅  
- Sass Level: OVER 9000! 📈
- Fun Factor: INFINITE 🦄

Thanks for letting MissDorking show off! 😘
{'='*60}
"""
            self.results_text.insert(tk.END, fun_footer)
    
    def start_bulk_boss_scan(self):
        """Start bulk boss mode scanning"""
        domains_text = self.bulk_domains_text.get(1.0, tk.END).strip()
        if not domains_text:
            messagebox.showerror("Error", "👑 The Boss needs domains to conquer!")
            return
        
        domains = [d.strip() for d in domains_text.split('\n') if d.strip()]
        if not domains:
            messagebox.showerror("Error", "👑 No valid domains found for domination!")
            return
        
        # Start bulk scanning
        self.bulk_scan_button.config(state=tk.DISABLED)
        self.bulk_progress_bar.config(mode='determinate', maximum=len(domains), value=0)
        
        bulk_thread = threading.Thread(target=self.run_bulk_boss_scan, args=(domains,))
        bulk_thread.daemon = True
        bulk_thread.start()
    
    def run_bulk_boss_scan(self, domains):
        """Run the bulk boss scan with maximum power"""
        try:
            def progress_callback(completed, total, domain, result):
                self.master.after(0, lambda: self.bulk_progress_bar.config(value=completed))
                
                status = f"👑 [{completed}/{total}] DOMINATING {domain}..."
                self.master.after(0, lambda: self.bulk_status_label.config(text=status))
            
            self.master.after(0, lambda: self.bulk_status_label.config(text="👑 BULK BOSS MODE ACTIVATED!"))
            
            # Use our super fast scanner with max power
            results = self.fast_scanner.bulk_scan(domains, progress_callback)
            
            # Generate epic report
            report = self.generate_boss_report(results)
            
            self.master.after(0, lambda: self.bulk_results_text.delete(1.0, tk.END))
            self.master.after(0, lambda: self.bulk_results_text.insert(tk.END, report))
            
            self.master.after(0, lambda: self.bulk_status_label.config(text="👑 BULK DOMINATION COMPLETE! ALL HAIL THE BOSS!"))
            
        except Exception as e:
            error_msg = f"👑 Boss mode crashed: {str(e)}"
            self.master.after(0, lambda: self.bulk_status_label.config(text=error_msg))
            logging.error(error_msg)
        
        finally:
            self.master.after(0, lambda: self.bulk_scan_button.config(state=tk.NORMAL))
    
    def generate_boss_report(self, results):
        """Generate a boss-level report with attitude"""
        if not results:
            return "👑 No results available for the Boss!"
        
        summary = results['summary']
        domain_results = results['domain_results']
        
        report = f"""👑 BULK BOSS DOMINATION REPORT 👑
{'='*50}

📊 EMPIRE STATISTICS:
- Domains Conquered: {summary['total_domains']}
- Successful Conquests: {summary['successful_scans']}
- Failed Attempts: {summary['failed_scans']} 
- Total Domination Time: {summary['total_scan_time']:.1f}s ({summary['total_scan_time']/60:.1f} minutes)
- Average Conquest Speed: {summary['average_time_per_domain']:.2f}s per domain
- Login Portals Captured: {summary['total_login_pages_found']}
- High-Value Targets: {summary['total_high_risk_findings']}

🎯 CONQUERED TERRITORIES WITH LOGIN PORTALS:
{'='*50}
"""
        
        # List successful conquests
        successful_domains = []
        for domain, result in domain_results.items():
            if result['success']:
                login_count = result['results']['_summary'].get('login_pages_count', 0)
                if login_count > 0:
                    successful_domains.append((domain, login_count, result['scan_time']))
        
        if successful_domains:
            for domain, count, scan_time in sorted(successful_domains, key=lambda x: x[1], reverse=True):
                report += f"👑 {domain} - {count} portals captured ({scan_time}s)\\n"
        else:
            report += "😢 No login portals found across the empire.\\n"
        
        # Boss completion message
        report += f"""
{'='*50}
👑 BULK BOSS MODE COMPLETE! 👑

💋 The Boss says: "Another successful day of digital domination! 
   {summary['successful_scans']} domains fell to my awesome power!"

🏆 Performance Rating: {"LEGENDARY" if summary['successful_scans'] > 3 else "EXCELLENT" if summary['successful_scans'] > 1 else "DECENT"}
⚡ Speed Rating: {"LUDICROUS" if summary['average_time_per_domain'] < 10 else "FAST" if summary['average_time_per_domain'] < 20 else "NORMAL"}
💅 Style Points: MAXIMUM

Thanks for letting the Boss show off! 😘
{'='*50}
"""
        
        return report
    
    def load_domains_from_file(self):
        """Load domains from file for bulk processing"""
        filepath = filedialog.askopenfilename(
            title="Select domain army list",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    domains = f.read()
                
                self.bulk_domains_text.delete(1.0, tk.END)
                self.bulk_domains_text.insert(tk.END, domains)
                
                messagebox.showinfo("Success", f"👑 Domain army loaded from {filepath}!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load domain army: {e}")
    
    def stop_scan(self):
        """Stop current scan"""
        self.is_scanning = False
        self.update_status("⏹️ SCAN STOPPED! The speed demon takes a break... 😴")
        self.reset_scan_ui()
    
    def reset_scan_ui(self):
        """Reset scan UI to ready state"""
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
    
    def update_status(self, message):
        """Update status label with thread safety"""
        self.master.after(0, lambda: self.status_label.config(text=message))
        logging.info(message)
    
    def save_results(self):
        """Save current results to file"""
        if not self.current_results:
            messagebox.showwarning("Warning", "💄 No fabulous results to save, honey!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = filedialog.asksaveasfilename(
            title="Save speed demon results",
            defaultextension=".json",
            initialvalue=f"speed_demon_results_{timestamp}.json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                if filepath.endswith('.json'):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=2, ensure_ascii=False)
                else:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(self.results_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"💾 Results saved to {filepath}! You're amazing! ✨")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {e}")
    
    def save_bulk_results(self):
        """Save bulk results to file"""
        if not hasattr(self.fast_scanner, 'results') or not self.fast_scanner.results:
            messagebox.showwarning("Warning", "👑 No bulk empire to save!")
            return
        
        try:
            filepath = self.fast_scanner.save_results()
            messagebox.showinfo("Success", f"👑 Bulk empire saved to {filepath}! The Boss is pleased! 💋")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bulk results: {e}")
    
    def export_pdf(self):
        """Export results to PDF with sass!"""
        if not self.current_results:
            messagebox.showwarning("Warning", "💄 No fabulous results to export, darling!")
            return
        
        if not EXPORT_AVAILABLE or not self.exporter:
            messagebox.showerror("Error", "💋 PDF export not available! Install reportlab: pip install reportlab")
            return
        
        try:
            domain = self.domain_entry.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save fabulous PDF report"
            )
            
            if filename:
                # Convert analyzed results back to exportable format
                export_results = {}
                for category, category_results in self.current_results.items():
                    if category == '_summary':
                        continue
                    export_results[category] = category_results
                
                filepath = self.exporter.export_to_pdf(export_results, domain, filename)
                messagebox.showinfo("Success", f"💋 PDF report saved with maximum sass!\n{filepath}")
                
                # Ask to open file
                if messagebox.askyesno("Open File", "💄 Want to admire your fabulous report?"):
                    import os, sys
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        import webbrowser
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            messagebox.showerror("Error", f"💋 PDF export had a drama: {str(e)}")
            logging.error(f"PDF export error: {e}")
    
    def export_csv(self):
        """Export results to CSV with style!"""
        if not self.current_results:
            messagebox.showwarning("Warning", "💄 No spectacular results to export, honey!")
            return
        
        if not EXPORT_AVAILABLE or not self.exporter:
            messagebox.showerror("Error", "💋 CSV export not available! Missing export module!")
            return
        
        try:
            domain = self.domain_entry.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save stunning CSV report"
            )
            
            if filename:
                # Convert analyzed results back to exportable format
                export_results = {}
                for category, category_results in self.current_results.items():
                    if category == '_summary':
                        continue
                    export_results[category] = category_results
                
                filepath = self.exporter.export_to_csv(export_results, domain, filename)
                messagebox.showinfo("Success", f"💅 CSV report saved with style!\n{filepath}")
                
                # Ask to open file
                if messagebox.askyesno("Open File", "📊 Want to see your data in spreadsheet glory?"):
                    import os, sys
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        import webbrowser
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            messagebox.showerror("Error", f"💋 CSV export threw a tantrum: {str(e)}")
            logging.error(f"CSV export error: {e}")
    
    def update_performance_stats(self):
        """Update performance statistics display"""
        stats = f"""🚀 LUDICROUS SPEED CONFIGURATION STATS 🚀
{'='*50}

⚡ CURRENT SPEED SETTINGS:
- Request Delay Range: {self.config['delay_range'][0]}-{self.config['delay_range'][1]} seconds
- Parallel Workers: {self.config['max_workers']} threads
- Request Timeout: {self.config['timeout']} seconds
- Batch Size: {self.config['batch_size']} items

💪 PERFORMANCE ESTIMATES:
- Expected Speed: {"LUDICROUS" if self.config['delay_range'][1] < 0.5 else "VERY FAST" if self.config['delay_range'][1] < 1 else "FAST"}
- Concurrency Level: {"MAXIMUM" if self.config['max_workers'] >= 6 else "HIGH" if self.config['max_workers'] >= 3 else "NORMAL"}
- Risk Level: {"YOLO" if self.config['delay_range'][1] < 0.5 else "MODERATE" if self.config['delay_range'][1] < 1 else "CONSERVATIVE"}

🎯 OPTIMIZATION TIPS:
- Lower delay = Faster speed (but higher detection risk)
- More workers = More parallel power (but more resources)
- Lower timeout = Faster failures (but might miss slow sites)

💋 MissDorking's Recommendation:
Current settings are {"PERFECT for speed demons! 🔥" if self.config['delay_range'][1] < 0.5 and self.config['max_workers'] >= 6 else "GOOD for balanced performance! ⚡" if self.config['delay_range'][1] < 1 else "SAFE but could be faster! 🐌"}
"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)

def main():
    """Launch the super fast dorking GUI"""
    root = tk.Tk()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = SuperFastDorkingGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Speed demon interrupted by user")
    except Exception as e:
        logging.error(f"Speed demon crashed: {e}")
        messagebox.showerror("Fatal Error", f"Speed demon had an oopsie:\\n{e}")

if __name__ == "__main__":
    main()
