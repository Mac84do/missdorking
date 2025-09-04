"""
Main GUI Application for Google Dorking Tool with Bulk Scanning
Cross-platform GUI using tkinter with tabbed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import logging
from datetime import datetime
import os
import sys
import webbrowser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

# Import our modules
from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
from scraper import GoogleScraper
from alternative_scraper import AlternativeScraper
from hybrid_scraper_fixed import HybridScraper
from export import ResultExporter
from analysis import ResultAnalyzer
from fast_bulk_scanner import FastBulkScanner
from professional_bulk_scanner import ProfessionalBulkScanner
from splash_screen import show_splash_screen

class DorkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Dorking Tool - MissDorking")
        self.root.geometry("1200x800")
        
        # Set up logging
        self.setup_logging()
        
        # Initialize components
        self.scraper = GoogleScraper()
        self.exporter = ResultExporter()
        self.analyzer = ResultAnalyzer()
        self.bulk_scanner = FastBulkScanner(max_workers=6, delay_range=(0.5, 1.0))
        self.results = {}
        self.bulk_results = {}
        self.is_running = False
        self.is_bulk_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Configure styles
        self.setup_styles()
        
        logging.info("Application with bulk scanning initialized successfully")
    
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
    
    def create_banner_image(self):
        """Create a sleek banner image"""
        try:
            # Create a banner with gradient effect
            width, height = 1200, 120
            image = Image.new('RGB', (width, height), color='#0a0a0a')
            draw = ImageDraw.Draw(image)
            
            # Create gradient background
            for y in range(height):
                alpha = int((y / height) * 255)
                color = (0, min(255, alpha), min(255, int(alpha * 0.8)))
                draw.line([(0, y), (width, y)], fill=color)
            
            # Add some futuristic elements
            # Circuit pattern
            for i in range(0, width, 100):
                draw.rectangle([i, 20, i+50, 25], fill='#00ccff')
                draw.rectangle([i+10, 95, i+60, 100], fill='#ff0099')
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Could not create banner image: {e}")
            return None
    
    def setup_styles(self):
        """Configure sleek futuristic theme styles"""
        style = ttk.Style()
        
        # Set the theme to a dark style
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Sleek futuristic color scheme
        ELECTRIC_BLUE = '#00ccff'      # Primary accent
        NEON_PINK = '#ff0099'          # Secondary accent 
        CYBER_GREEN = '#00ff88'        # Success/active
        LIGHT_GRAY = '#e0e0e0'         # Primary text
        MED_GRAY = '#a0a0a0'           # Secondary text
        DARK_GRAY = '#2a2a2a'          # Backgrounds
        DARKER_GRAY = '#1a1a1a'        # Input backgrounds
        BLACK_BG = '#0a0a0a'           # Main background
        
        # Configure main window background
        self.root.configure(bg=BLACK_BG)
        
        # Configure ttk styles with sleek futuristic theme
        style.configure('TLabel', 
                       foreground=LIGHT_GRAY, 
                       background=BLACK_BG,
                       font=('Segoe UI', 10))
        
        style.configure('Title.TLabel', 
                       foreground=ELECTRIC_BLUE, 
                       background=BLACK_BG,
                       font=('Segoe UI Light', 24, 'bold'))
        
        style.configure('Header.TLabel', 
                       foreground=NEON_PINK, 
                       background=BLACK_BG,
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Progress.TLabel', 
                       foreground=CYBER_GREEN, 
                       background=BLACK_BG,
                       font=('Segoe UI', 9))
        
        style.configure('Subtle.TLabel', 
                       foreground=MED_GRAY, 
                       background=BLACK_BG,
                       font=('Segoe UI', 8))
        
        style.configure('TFrame', background=BLACK_BG)
        
        style.configure('Card.TFrame', 
                       background=DARK_GRAY,
                       relief='flat',
                       borderwidth=1)
        
        style.configure('TLabelFrame', 
                       foreground=ELECTRIC_BLUE,
                       background=BLACK_BG,
                       bordercolor=ELECTRIC_BLUE,
                       lightcolor=ELECTRIC_BLUE,
                       darkcolor=DARKER_GRAY,
                       borderwidth=2,
                       relief='solid')
        
        style.configure('TLabelFrame.Label', 
                       foreground=ELECTRIC_BLUE,
                       background=BLACK_BG,
                       font=('Segoe UI', 10, 'bold'))
        
        # Entry field styling - sleek and modern
        style.configure('TEntry', 
                       foreground=LIGHT_GRAY,
                       fieldbackground=DARKER_GRAY,
                       bordercolor=ELECTRIC_BLUE,
                       insertcolor=ELECTRIC_BLUE,
                       selectbackground=ELECTRIC_BLUE,
                       selectforeground=BLACK_BG,
                       font=('Segoe UI', 10),
                       relief='flat',
                       borderwidth=2)
        
        style.map('TEntry',
                 bordercolor=[('focus', CYBER_GREEN)],
                 lightcolor=[('focus', CYBER_GREEN)])
        
        # Spinbox styling
        style.configure('TSpinbox', 
                       foreground=LIGHT_GRAY,
                       fieldbackground=DARKER_GRAY,
                       bordercolor=ELECTRIC_BLUE,
                       font=('Segoe UI', 9),
                       relief='flat')
        
        # Combobox styling
        style.configure('TCombobox', 
                       foreground=LIGHT_GRAY,
                       fieldbackground=DARKER_GRAY,
                       bordercolor=ELECTRIC_BLUE,
                       font=('Segoe UI', 9),
                       relief='flat')
        
        # Button styles - modern and sleek
        style.configure('Primary.TButton', 
                       foreground='white',
                       background=ELECTRIC_BLUE,
                       bordercolor=ELECTRIC_BLUE,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(20, 10))
        
        style.map('Primary.TButton',
                 background=[('active', '#0099cc'),
                           ('pressed', CYBER_GREEN)])
        
        style.configure('Secondary.TButton', 
                       foreground='white',
                       background=NEON_PINK,
                       bordercolor=NEON_PINK,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(15, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', '#cc0077'),
                           ('pressed', ELECTRIC_BLUE)])
        
        style.configure('Action.TButton', 
                       foreground=BLACK_BG,
                       background=CYBER_GREEN,
                       bordercolor=CYBER_GREEN,
                       focuscolor='none',
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(25, 12))
        
        style.map('Action.TButton',
                 background=[('active', '#00cc66'),
                           ('pressed', ELECTRIC_BLUE)])
        
        style.configure('Export.TButton', 
                       foreground=LIGHT_GRAY,
                       background=DARK_GRAY,
                       bordercolor=MED_GRAY,
                       focuscolor='none',
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=1,
                       padding=(12, 6))
        
        style.map('Export.TButton',
                 background=[('active', MED_GRAY),
                           ('pressed', ELECTRIC_BLUE)],
                 foreground=[('pressed', 'white')])
        
        style.configure('Bulk.TButton', 
                       foreground='white',
                       background=NEON_PINK,
                       bordercolor=NEON_PINK,
                       focuscolor='none',
                       font=('Segoe UI', 12, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(30, 15))
        
        style.map('Bulk.TButton',
                 background=[('active', '#cc0077'),
                           ('pressed', CYBER_GREEN)])
        
        # Progress bar - modern sleek style
        style.configure('Modern.Horizontal.TProgressbar', 
                       background=CYBER_GREEN,
                       troughcolor=DARKER_GRAY,
                       bordercolor=ELECTRIC_BLUE,
                       lightcolor=CYBER_GREEN,
                       darkcolor=CYBER_GREEN,
                       borderwidth=1,
                       relief='flat')
        
        # Notebook (tabs) styling
        style.configure('TNotebook', 
                       background=BLACK_BG,
                       bordercolor=ELECTRIC_BLUE,
                       tabmargins=[0, 5, 0, 0])
        
        style.configure('TNotebook.Tab', 
                       foreground=MED_GRAY,
                       background=DARK_GRAY,
                       bordercolor=ELECTRIC_BLUE,
                       font=('Segoe UI', 10),
                       padding=[20, 10],
                       focuscolor='none')
        
        style.map('TNotebook.Tab',
                 background=[('selected', BLACK_BG),
                           ('active', DARKER_GRAY)],
                 foreground=[('selected', ELECTRIC_BLUE),
                           ('active', LIGHT_GRAY)])
        
        # Checkbutton styling
        style.configure('TCheckbutton', 
                       foreground=LIGHT_GRAY,
                       background=BLACK_BG,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        style.map('TCheckbutton',
                 foreground=[('active', ELECTRIC_BLUE)])
    
    def create_widgets(self):
        """Create and layout all GUI widgets with modern sleek design"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="0")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Create and add banner
        banner_image = self.create_banner_image()
        if banner_image:
            banner_label = tk.Label(main_frame, image=banner_image, bg='#0a0a0a')
            banner_label.image = banner_image  # Keep a reference
            banner_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Title with modern styling
        title_frame = ttk.Frame(main_frame, padding="20")
        title_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, text="MissDorking™ Professional", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame, text="Advanced Google Dorking & Intelligence Platform", 
                                 style='Subtle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Create notebook for tabs with modern styling
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=(0, 20))
        
        # Create single domain tab
        self.create_single_domain_tab()
        
        # Create bulk scanning tab
        self.create_bulk_scanning_tab()
        
        # Modern status bar
        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="10")
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value=f"Ready • {get_dork_count()} intelligence queries loaded • System online")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, style='Subtle.TLabel')
        status_bar.grid(row=0, column=0, sticky=tk.W)
    
    def create_single_domain_tab(self):
        """Create single domain scanning tab"""
        single_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(single_frame, text="Single Domain Scan")
        
        single_frame.columnconfigure(1, weight=1)
        single_frame.rowconfigure(4, weight=1)
        
        # Domain input section
        ttk.Label(single_frame, text="Target Domain:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.domain_var = tk.StringVar()
        self.domain_entry = ttk.Entry(single_frame, textvariable=self.domain_var, 
                                     font=('Arial', 10), width=40)
        self.domain_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        self.domain_entry.bind('<Return>', self.on_enter_pressed)
        
        # Run button
        self.run_button = ttk.Button(single_frame, text="▶ Start Scan", 
                                    command=self.start_dorking, style='Primary.TButton')
        self.run_button.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(single_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
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
        progress_frame = ttk.LabelFrame(single_frame, text="[SCAN STATUS]", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="» System ready for infiltration...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                           style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(single_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
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
    
    def create_bulk_scanning_tab(self):
        """Create bulk scanning tab"""
        bulk_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(bulk_frame, text="🚀 Bulk Scanner")
        
        bulk_frame.columnconfigure(0, weight=1)
        bulk_frame.rowconfigure(2, weight=1)
        
        # Header
        header_label = ttk.Label(bulk_frame, text="🎯 PROFESSIONAL BULK SCANNER - RATE-LIMIT SAFE MODE", 
                               font=('Arial', 14, 'bold'), foreground='blue')
        header_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(bulk_frame, text="📋 Domain List", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        # Instructions
        instructions = ttk.Label(input_frame, 
                               text="Enter domains to scan (one per line). Example: example.com, google.com, github.com",
                               font=('Arial', 9), foreground='gray')
        instructions.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Domain input text area
        self.bulk_domains_text = scrolledtext.ScrolledText(input_frame, height=8, width=60,
                                                          font=('Arial', 10))
        self.bulk_domains_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Bulk control buttons
        bulk_controls = ttk.Frame(input_frame)
        bulk_controls.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.load_domains_button = ttk.Button(bulk_controls, text="📁 Load from File",
                                            command=self.load_domains_from_file, 
                                            style='Export.TButton')
        self.load_domains_button.grid(row=0, column=0, padx=(0, 10))
        
        self.bulk_scan_button = ttk.Button(bulk_controls, text="🚀 START BULK SCAN",
                                         command=self.start_bulk_scan, style='Bulk.TButton')
        self.bulk_scan_button.grid(row=0, column=1, padx=(0, 10))
        
        # Bulk options
        bulk_options_frame = ttk.Frame(bulk_controls)
        bulk_options_frame.grid(row=0, column=2, padx=(20, 0))
        
        ttk.Label(bulk_options_frame, text="Workers:").grid(row=0, column=0)
        self.bulk_workers_var = tk.StringVar(value="6")
        workers_spinbox = ttk.Spinbox(bulk_options_frame, from_=1, to=12, width=5,
                                    textvariable=self.bulk_workers_var)
        workers_spinbox.grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(bulk_options_frame, text="Speed:").grid(row=0, column=2)
        self.bulk_speed_var = tk.StringVar(value="Fast")
        speed_combo = ttk.Combobox(bulk_options_frame, textvariable=self.bulk_speed_var,
                                  values=["Conservative", "Fast", "Ludicrous"], width=10)
        speed_combo.grid(row=0, column=3, padx=(5, 0))
        speed_combo.state(['readonly'])
        
        # Category selection for bulk scanning
        bulk_categories_frame = ttk.LabelFrame(input_frame, text="🎯 Categories to Scan", padding="10")
        bulk_categories_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        bulk_categories_frame.columnconfigure(0, weight=1)
        
        self.bulk_categories_frame_inner = ttk.Frame(bulk_categories_frame)
        self.bulk_categories_frame_inner.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.bulk_category_vars = {}
        self.create_bulk_category_checkboxes()
        
        # Results section
        bulk_results_frame = ttk.LabelFrame(bulk_frame, text="📊 Bulk Scan Results", padding="10")
        bulk_results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        bulk_results_frame.columnconfigure(0, weight=1)
        bulk_results_frame.rowconfigure(1, weight=1)
        
        # Bulk progress section
        bulk_progress_frame = ttk.Frame(bulk_results_frame)
        bulk_progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        bulk_progress_frame.columnconfigure(0, weight=1)
        
        self.bulk_progress_var = tk.StringVar(value="» Multi-target infiltration mode ready...")
        self.bulk_progress_label = ttk.Label(bulk_progress_frame, textvariable=self.bulk_progress_var,
                                           font=('Arial', 10, 'bold'))
        self.bulk_progress_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.bulk_progress_bar = ttk.Progressbar(bulk_progress_frame, mode='determinate',
                                               style='Modern.Horizontal.TProgressbar')
        self.bulk_progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Bulk results text area
        self.bulk_results_text = scrolledtext.ScrolledText(bulk_results_frame, height=15, width=80,
                                                          font=('Courier', 9))
        self.bulk_results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Bulk export buttons
        bulk_export_frame = ttk.Frame(bulk_results_frame)
        bulk_export_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.bulk_export_pdf_button = ttk.Button(bulk_export_frame, text="📄 Export PDF",
                                                command=self.export_bulk_pdf, style='Export.TButton')
        self.bulk_export_pdf_button.grid(row=0, column=0, padx=(0, 10))
        self.bulk_export_pdf_button.config(state='disabled')
        
        self.bulk_export_csv_button = ttk.Button(bulk_export_frame, text="📊 Export CSV",
                                                command=self.export_bulk_csv, style='Export.TButton')
        self.bulk_export_csv_button.grid(row=0, column=1, padx=(0, 10))
        self.bulk_export_csv_button.config(state='disabled')
        
        self.bulk_export_json_button = ttk.Button(bulk_export_frame, text="💾 Export JSON",
                                                command=self.export_bulk_json, style='Export.TButton')
        self.bulk_export_json_button.grid(row=0, column=2, padx=(0, 10))
        self.bulk_export_json_button.config(state='disabled')
        
        self.bulk_clear_button = ttk.Button(bulk_export_frame, text="🗑️ Clear Results",
                                          command=self.clear_bulk_results, style='Export.TButton')
        self.bulk_clear_button.grid(row=0, column=3, padx=(0, 10))
    
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
    
    def create_bulk_category_checkboxes(self):
        """Create checkboxes for each dork category for bulk scanning"""
        row = 0
        col = 0
        max_cols = 4
        
        for category in GOOGLE_DORKS.keys():
            var = tk.BooleanVar(value=True)  # All categories selected by default
            self.bulk_category_vars[category] = var
            
            checkbox = ttk.Checkbutton(self.bulk_categories_frame_inner, text=category, variable=var)
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 10), pady=2)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def load_domains_from_file(self):
        """Load domains from file for bulk processing"""
        filepath = filedialog.askopenfilename(
            title="Select domain list file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    domains = f.read()
                
                self.bulk_domains_text.delete(1.0, tk.END)
                self.bulk_domains_text.insert(tk.END, domains)
                
                domain_count = len([d.strip() for d in domains.split('\n') if d.strip()])
                messagebox.showinfo("Success", f"Loaded {domain_count} domains from {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load domain list: {e}")
    
    def start_bulk_scan(self):
        """Start bulk scanning process"""
        if self.is_bulk_running:
            messagebox.showwarning("Warning", "Bulk scan is already running!")
            return
        
        # Get domains from text area
        domains_text = self.bulk_domains_text.get(1.0, tk.END).strip()
        if not domains_text:
            messagebox.showerror("Error", "Please enter domains to scan!")
            return
        
        domains = [d.strip() for d in domains_text.split('\n') if d.strip()]
        if not domains:
            messagebox.showerror("Error", "No valid domains found!")
            return
        
        # Check if at least one category is selected
        selected_bulk_categories = [cat for cat, var in self.bulk_category_vars.items() if var.get()]
        if not selected_bulk_categories:
            messagebox.showerror("Error", "Please select at least one category to scan!")
            return
        
        # Configure professional scanner based on settings
        workers = int(self.bulk_workers_var.get())
        speed = self.bulk_speed_var.get()
        
        if speed == "Conservative":
            delay_range = (8.0, 12.0)
            max_workers = min(workers, 2)  # Very conservative
        elif speed == "Fast":
            delay_range = (5.0, 8.0)
            max_workers = min(workers, 3)  # Moderate
        else:  # Ludicrous
            delay_range = (3.0, 5.0)
            max_workers = min(workers, 4)  # Still reasonable to avoid blocks
        
        # Use ProfessionalBulkScanner for better reliability and rate limit handling
        self.professional_scanner = ProfessionalBulkScanner(
            max_workers=max_workers, 
            delay_range=delay_range
            # Professional scanner uses fixed 3 results per query internally for conservative approach
        )
        
        self.is_bulk_running = True
        self.bulk_scan_button.config(state='disabled', text='🚀 SCANNING...')
        self.bulk_export_pdf_button.config(state='disabled')
        self.bulk_export_csv_button.config(state='disabled')
        self.bulk_export_json_button.config(state='disabled')
        
        # Clear results
        self.bulk_results_text.delete(1.0, tk.END)
        self.bulk_progress_bar.config(maximum=len(domains), value=0)
        
        # Start bulk scanning in thread
        thread = threading.Thread(target=self.run_bulk_scan, args=(domains,))
        thread.daemon = True
        thread.start()
    
    def run_bulk_scan(self, domains):
        """Run bulk scanning process using ProfessionalBulkScanner"""
        try:
            self.root.after(0, lambda: self.bulk_progress_var.set(f"🚀 Starting professional bulk scan of {len(domains)} domains..."))
            
            # Get selected categories for filtering
            selected_bulk_categories = [cat for cat, var in self.bulk_category_vars.items() if var.get()]
            
            def progress_callback(completed, total, domain, result):
                """Enhanced progress callback for professional scanner"""
                self.root.after(0, lambda: self.bulk_progress_bar.config(value=completed))
                
                if result.get('success', False):
                    # Get professional scanner result details
                    summary = result.get('results', {}).get('_summary', {})
                    stats = result.get('stats', {})
                    
                    login_count = summary.get('login_pages_count', 0)
                    high_risk_count = summary.get('high_risk_count', 0)
                    total_results = stats.get('total_results', 0)
                    
                    status_msg = f"[{completed}/{total}] ✅ {domain} ({result.get('scan_time', 0):.1f}s) - {login_count} login/{high_risk_count} high-risk"
                    
                    # Add detailed log entry
                    result_line = f"✅ {domain} - {login_count} login pages, {high_risk_count} high-risk, {total_results} total ({result.get('scan_time', 0):.1f}s)\n"
                    
                    # Show categories found
                    results_data = result.get('results', {})
                    found_categories = [cat for cat in results_data.keys() if cat != '_summary' and results_data[cat]]
                    if found_categories:
                        result_line += f"   🎯 Categories found: {', '.join(found_categories)}\n"
                    
                else:
                    error_msg = result.get('error', 'Unknown error')
                    status_msg = f"[{completed}/{total}] ❌ {domain} - {error_msg}"
                    result_line = f"❌ {domain} - FAILED: {error_msg}\n"
                
                self.root.after(0, lambda: self.bulk_progress_var.set(status_msg))
                self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, result_line))
                self.root.after(0, lambda: self.bulk_results_text.see(tk.END))
            
            # Run professional bulk scan with category filtering
            results = self.professional_scanner.bulk_scan(domains, selected_categories=selected_bulk_categories, progress_callback=progress_callback)
            
            # Store results in the expected format for GUI
            self.bulk_results = {
                'summary': results.get('summary', {}),
                'domains': results.get('domain_results', {})  # ProfessionalBulkScanner uses 'domain_results' key
            }
            
            # Display comprehensive summary report
            self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, "\n" + "="*80 + "\n"))
            self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, "📊 PROFESSIONAL BULK SCAN SUMMARY REPORT\n"))
            self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, "="*80 + "\n"))
            
            summary = results.get('summary', {})
            report_lines = [
                f"📋 Total Domains Scanned: {summary.get('total_domains', 0)}",
                f"✅ Successful Scans: {summary.get('successful_scans', 0)}",
                f"❌ Failed Scans: {summary.get('failed_scans', 0)}",
                f"⏱️  Total Scan Time: {summary.get('total_time', 0):.2f} seconds",
                f"🎯 High-Value Results: {summary.get('high_value_results', 0)}",
                f"📊 Total Results Found: {summary.get('total_results', 0)}",
                f"📈 Success Rate: {summary.get('success_rate', 0):.1f}%",
                f"🚫 Rate Limit Incidents: {summary.get('rate_limit_hits', 0)}"
            ]
            
            for line in report_lines:
                self.root.after(0, lambda l=line: self.bulk_results_text.insert(tk.END, f"{l}\n"))
            
            # Show category breakdown if available
            if 'category_breakdown' in summary:
                self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, "\n🎯 CATEGORY BREAKDOWN:\n"))
                for category, count in summary['category_breakdown'].items():
                    self.root.after(0, lambda c=category, cnt=count: 
                                   self.bulk_results_text.insert(tk.END, f"   • {c}: {cnt} results\n"))
            
            self.root.after(0, lambda: self.bulk_results_text.insert(tk.END, "\n💎 Professional scan completed with enhanced accuracy and rate limit protection!\n"))
            self.root.after(0, lambda: self.bulk_results_text.see(tk.END))
            
            # Update final status
            final_status = f"🎉 PROFESSIONAL SCAN COMPLETE! {summary.get('successful_scans', 0)}/{summary.get('total_domains', 0)} domains - {summary.get('high_value_results', 0)} high-value results found!"
            self.root.after(0, lambda: self.bulk_progress_var.set(final_status))
            
            logging.info(f"Professional bulk scan completed: {summary}")
            
        except Exception as e:
            error_msg = f"Professional bulk scan failed: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            logging.error(error_msg)
        
        finally:
            self.is_bulk_running = False
            self.root.after(0, lambda: self.bulk_scan_button.config(state='normal', text='🚀 START BULK SCAN'))
            self.root.after(0, lambda: self.bulk_export_pdf_button.config(state='normal'))
            self.root.after(0, lambda: self.bulk_export_csv_button.config(state='normal'))
            self.root.after(0, lambda: self.bulk_export_json_button.config(state='normal'))
    
    def export_bulk_pdf(self):
        """Export bulk scan results to PDF"""
        if not self.bulk_results:
            messagebox.showwarning("Warning", "No bulk scan results to export!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Bulk Scan PDF Report"
            )
            
            if filename:
                # Convert bulk results format to single domain format for export compatibility
                combined_results = self._convert_bulk_to_single_format()
                
                filepath = self.exporter.export_to_pdf(combined_results, "bulk_scan", filename)
                messagebox.showinfo("Success", f"Bulk PDF report saved to:\n{filepath}")
                
                if messagebox.askyesno("Open File", "Would you like to open the PDF file?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export bulk PDF: {e}")
    
    def export_bulk_csv(self):
        """Export bulk scan results to CSV"""
        if not self.bulk_results:
            messagebox.showwarning("Warning", "No bulk scan results to export!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Bulk Scan CSV Report"
            )
            
            if filename:
                # Convert bulk results format to single domain format for export compatibility
                combined_results = self._convert_bulk_to_single_format()
                
                filepath = self.exporter.export_to_csv(combined_results, "bulk_scan", filename)
                messagebox.showinfo("Success", f"Bulk CSV report saved to:\n{filepath}")
                
                if messagebox.askyesno("Open File", "Would you like to open the CSV file?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export bulk CSV: {e}")
    
    def export_bulk_json(self):
        """Export bulk scan results to JSON"""
        if not self.bulk_results:
            messagebox.showwarning("Warning", "No bulk scan results to export!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Bulk Scan JSON Results"
            )
            
            if filename:
                # Use professional scanner if available, otherwise fallback to bulk scanner
                if hasattr(self, 'professional_scanner') and self.professional_scanner:
                    filepath = self.professional_scanner.save_results(filename)
                else:
                    filepath = self.bulk_scanner.save_results(filename)
                    
                messagebox.showinfo("Success", f"Bulk JSON results saved to:\n{filepath}")
                
                if messagebox.askyesno("Open Folder", "Would you like to open the folder containing the file?"):
                    folder = os.path.dirname(filepath)
                    if sys.platform.startswith('win'):
                        os.startfile(folder)
                    else:
                        webbrowser.open(f'file://{folder}')
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export bulk JSON: {e}")
    
    def _convert_bulk_to_single_format(self):
        """Convert bulk scan results to single domain format for PDF/CSV export"""
        combined_results = {}
        
        # Get domain results from bulk_results
        domains = self.bulk_results.get('domains', {})
        
        for domain, domain_data in domains.items():
            if domain_data.get('success', False):
                domain_results = domain_data.get('results', {})
                
                # Combine all results across domains
                for category, queries in domain_results.items():
                    if category == '_summary':  # Skip summary data
                        continue
                        
                    if category not in combined_results:
                        combined_results[category] = {}
                    
                    for query, results in queries.items():
                        # Ensure results is iterable (list/dict) and not None or integer
                        if results is not None and hasattr(results, '__iter__') and not isinstance(results, str):
                            # Prefix query with domain name for clarity
                            prefixed_query = f"[{domain}] {query}"
                            combined_results[category][prefixed_query] = results
        
        # Add combined summary
        summary = self.bulk_results.get('summary', {})
        combined_results['_summary'] = {
            'total_domains': summary.get('total_domains', 0),
            'successful_scans': summary.get('successful_scans', 0),
            'failed_scans': summary.get('failed_scans', 0),
            'total_results': sum(len(queries) for queries in combined_results.values() if isinstance(queries, dict)),
            'scan_type': 'bulk_scan'
        }
        
        return combined_results
    
    def clear_bulk_results(self):
        """Clear bulk scan results"""
        self.bulk_results_text.delete(1.0, tk.END)
        self.bulk_results = {}
        self.bulk_progress_bar.config(value=0)
        self.bulk_progress_var.set("Ready for bulk domination...")
        self.bulk_export_pdf_button.config(state='disabled')
        self.bulk_export_csv_button.config(state='disabled')
        self.bulk_export_json_button.config(state='disabled')
    
    # Single domain scanning methods (same as original)
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
        """Run the dorking process (same as original)"""
        # Implementation same as original main_gui.py
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
                
            # Add hybrid scraper results for better coverage
            self.root.after(0, lambda: self.progress_var.set("Running direct site analysis for additional coverage..."))
            
            try:
                hybrid_scraper = HybridScraper()
                direct_results = hybrid_scraper.analyze_domain_directly(domain)
                
                if direct_results:
                    # Add direct analysis results to the "Login & Admin Pages" category
                    if "Login & Admin Pages" not in results:
                        results["Login & Admin Pages"] = {}
                    
                    # Create a special query for direct analysis results
                    direct_query = f"Direct site analysis of {domain}"
                    results["Login & Admin Pages"][direct_query] = direct_results
                    
                    self.root.after(0, lambda: self.append_to_results(
                        f"\n=== DIRECT SITE ANALYSIS ===\n{direct_query}: {len(direct_results)} results\n"))
                    
                    for result in direct_results:
                        self.root.after(0, lambda r=result: 
                                       self.append_to_results(f"  🎯 {r['title'][:80]}...\n    {r['url']}\n"))
                    
                    self.root.after(0, lambda: self.append_to_results("\n"))
                    
                    logging.info(f"Direct analysis found {len(direct_results)} additional results")
                else:
                    logging.info("Direct analysis found no additional results")
                    
            except Exception as e:
                logging.warning(f"Direct analysis failed: {e}")
            
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
        self.progress_var.set("» System ready for infiltration...")
        self.status_var.set(f"» System online - {get_dork_count()} neural queries loaded")
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
