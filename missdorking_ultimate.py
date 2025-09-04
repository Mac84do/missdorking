"""
🚀 MISSDORKING™ ULTIMATE 🚀
The Futuristic All-in-One Google Dorking & Intelligence Platform
Enhanced with Dad Jokes, Professional Branding, and Export Excellence!

Because cybersecurity should be both powerful AND fun! 💋✨
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import logging
import time
import random
from datetime import datetime
import os
import sys
import webbrowser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

# Import our enhanced modules
from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
from scraper import GoogleScraper
from alternative_scraper import AlternativeScraper
from hybrid_scraper_fixed import HybridScraper
from export import ResultExporter
from analysis import ResultAnalyzer
from fast_bulk_scanner import FastBulkScanner
from professional_bulk_scanner import ProfessionalBulkScanner

# Import our new awesome modules
from dad_jokes import DadJokesManager, get_startup_message, get_scan_message, get_export_message, get_progress_message
from branding_manager import BrandingManager, show_branding_config, get_branding_manager

class MissDorkingUltimate:
    def __init__(self, root):
        """Initialize the Ultimate MissDorking Experience! 🎯"""
        self.root = root
        self.root.title("🚀 MissDorking™ ULTIMATE - Futuristic Intelligence Platform 💋")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize all our awesome components
        self.setup_logging()
        self.dad_jokes = DadJokesManager()
        self.branding_manager = get_branding_manager()
        
        # Core functionality
        self.scraper = GoogleScraper()
        self.exporter = ResultExporter()
        self.analyzer = ResultAnalyzer()
        self.bulk_scanner = FastBulkScanner(max_workers=6, delay_range=(0.5, 1.0))
        
        # State management
        self.results = {}
        self.bulk_results = {}
        self.is_running = False
        self.is_bulk_running = False
        self.joke_timer_id = None
        
        # Create the ultimate UI
        self.create_futuristic_interface()
        self.setup_ultimate_styles()
        
        # Start dad joke rotation
        self.start_joke_rotation()
        
        # Welcome message
        welcome_joke = get_startup_message()
        self.show_notification(f"🎉 {welcome_joke}", "info")
        
        logging.info("MissDorking Ultimate initialized successfully! 🚀")
    
    def setup_logging(self):
        """Enhanced logging setup"""
        log_format = '%(asctime)s - %(levelname)s - [MissD Ultimate] %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('missdorking_ultimate.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_futuristic_interface(self):
        """Create the ultimate futuristic interface! 🌟"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="0")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Create futuristic banner
        self.create_ultimate_banner(main_frame)
        
        # Title section with dynamic jokes
        self.create_title_section(main_frame)
        
        # Enhanced tabbed interface
        self.create_enhanced_tabs(main_frame)
        
        # Ultimate status bar with jokes
        self.create_ultimate_status_bar(main_frame)
    
    def create_ultimate_banner(self, parent):
        """Create the ultimate futuristic banner"""
        try:
            # Create a more advanced banner
            width, height = 1400, 140
            image = Image.new('RGB', (width, height), color='#0a0a0a')
            draw = ImageDraw.Draw(image)
            
            # Futuristic gradient background
            for y in range(height):
                r = int(min(255, (y / height) * 50))
                g = int(min(255, (y / height) * 200 + 55))
                b = int(min(255, (y / height) * 255))
                color = (r, g, b)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Add circuit patterns
            circuit_color = '#00FFFF'
            for i in range(0, width, 120):
                # Horizontal lines
                draw.rectangle([i, 20, i+80, 25], fill=circuit_color)
                draw.rectangle([i+20, 115, i+100, 120], fill=circuit_color)
                # Vertical connectors
                draw.rectangle([i+40, 25, i+45, 35], fill=circuit_color)
                draw.rectangle([i+60, 105, i+65, 115], fill=circuit_color)
            
            # Add glowing orbs
            for i in range(3):
                x = 200 + i * 400
                y = 70
                for radius in range(15, 5, -2):
                    alpha = int((15 - radius) * 17)
                    glow_color = (0, 255 - alpha, 255, alpha)
                    # Simulate glow effect
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               fill=(0, 255-alpha//3, 255-alpha//3))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            banner_label = tk.Label(parent, image=photo, bg='#0a0a0a')
            banner_label.image = photo  # Keep reference
            banner_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
            
        except Exception as e:
            print(f"Could not create ultimate banner: {e}")
    
    def create_title_section(self, parent):
        """Create title section with dynamic content"""
        title_frame = ttk.Frame(parent, padding="20")
        title_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        # Main title
        main_title = ttk.Label(
            title_frame,
            text="🚀 MISSDORKING™ ULTIMATE 🚀",
            style='Ultimate.TLabel'
        )
        main_title.grid(row=0, column=0)
        
        # Subtitle with company branding if available
        company_info = self.branding_manager.get_company_info() if self.branding_manager else None
        if company_info and company_info.get('name') != 'Your Company Name':
            subtitle_text = f"Professional Intelligence Platform - Powered by {company_info['name']}"
        else:
            subtitle_text = "The Ultimate Google Dorking & Cybersecurity Intelligence Suite"
            
        subtitle = ttk.Label(
            title_frame,
            text=subtitle_text,
            style='Subtitle.TLabel'
        )
        subtitle.grid(row=1, column=0, pady=(5, 0))
        
        # Dynamic joke display
        self.joke_label = ttk.Label(
            title_frame,
            text=self.dad_jokes.get_smart_joke(),
            style='Joke.TLabel'
        )
        self.joke_label.grid(row=2, column=0, pady=(10, 0))
        
        # Quick access buttons
        self.create_quick_access_buttons(title_frame)
    
    def create_quick_access_buttons(self, parent):
        """Create quick access buttons for common actions"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=3, column=0, pady=(15, 0))
        
        # Branding config button
        branding_btn = ttk.Button(
            buttons_frame,
            text="🎨 Company Branding",
            command=self.open_branding_config,
            style='QuickAccess.TButton'
        )
        branding_btn.pack(side=tk.LEFT, padx=5)
        
        # New joke button
        joke_btn = ttk.Button(
            buttons_frame,
            text="😂 New Dad Joke",
            command=self.show_random_joke,
            style='QuickAccess.TButton'
        )
        joke_btn.pack(side=tk.LEFT, padx=5)
        
        # About button
        about_btn = ttk.Button(
            buttons_frame,
            text="ℹ️ About Ultimate",
            command=self.show_about_dialog,
            style='QuickAccess.TButton'
        )
        about_btn.pack(side=tk.LEFT, padx=5)
    
    def create_enhanced_tabs(self, parent):
        """Create enhanced tabbed interface"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=(0, 20))
        
        # Enhanced single domain tab
        self.create_enhanced_single_tab()
        
        # Enhanced bulk scanning tab
        self.create_enhanced_bulk_tab()
        
        # New customer management tab
        self.create_customer_tab()
        
        # Export hub tab
        self.create_export_hub_tab()
    
    def create_enhanced_single_tab(self):
        """Enhanced single domain scanning tab"""
        single_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(single_frame, text="🎯 Single Domain Intel")
        
        single_frame.columnconfigure(1, weight=1)
        single_frame.rowconfigure(5, weight=1)
        
        # Enhanced input section
        input_frame = ttk.LabelFrame(single_frame, text="🎯 TARGET ACQUISITION", padding="15")
        input_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Domain Target:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.domain_var = tk.StringVar()
        self.domain_entry = ttk.Entry(input_frame, textvariable=self.domain_var, 
                                     font=('Segoe UI', 12), width=40)
        self.domain_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.domain_entry.bind('<Return>', self.on_enter_pressed)
        
        self.scan_button = ttk.Button(input_frame, text="🚀 LAUNCH SCAN", 
                                    command=self.start_enhanced_scan, style='Launch.TButton')
        self.scan_button.grid(row=0, column=2)
        
        # Enhanced options
        self.create_enhanced_options(single_frame)
        
        # Progress section with jokes
        self.create_progress_section(single_frame)
        
        # Enhanced results section
        self.create_enhanced_results(single_frame)
    
    def create_enhanced_options(self, parent):
        """Create enhanced options section"""
        options_frame = ttk.LabelFrame(parent, text="⚙️ SCAN CONFIGURATION", padding="15")
        options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        options_frame.columnconfigure(1, weight=1)
        
        # Results per query
        ttk.Label(options_frame, text="Results per query:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.results_per_query_var = tk.StringVar(value="10")
        results_spinbox = ttk.Spinbox(options_frame, from_=1, to=50, width=10,
                                     textvariable=self.results_per_query_var)
        results_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Delay settings
        ttk.Label(options_frame, text="Scan speed:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.speed_var = tk.StringVar(value="Balanced")
        speed_combo = ttk.Combobox(options_frame, textvariable=self.speed_var,
                                  values=["Conservative", "Balanced", "Aggressive", "Ludicrous"], 
                                  width=12, state='readonly')
        speed_combo.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Category selection with enhanced display
        self.create_enhanced_categories(options_frame)
    
    def create_enhanced_categories(self, parent):
        """Enhanced category selection with improved visibility"""
        cat_frame = ttk.LabelFrame(parent, text="🎯 Intelligence Categories", padding="10")
        cat_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        cat_frame.columnconfigure(0, weight=1)
        
        # Select all / none buttons with improved styling
        button_frame = ttk.Frame(cat_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        select_all_btn = ttk.Button(button_frame, text="✅ Select All", 
                                  command=self.select_all_categories, style='Action.TButton')
        select_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_all_btn = ttk.Button(button_frame, text="❌ Clear All", 
                                 command=self.clear_all_categories, style='Secondary.TButton')
        clear_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Categories with enhanced styling and visibility
        categories_frame = ttk.Frame(cat_frame)
        categories_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.category_vars = {}
        self.category_checkboxes = {}  # Store checkbox references for styling
        row, col = 0, 0
        
        for category in GOOGLE_DORKS.keys():
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            
            dork_count = len(GOOGLE_DORKS[category])
            text = f"{category} ({dork_count})"
            
            # Create enhanced checkbox with custom styling
            checkbox = tk.Checkbutton(
                categories_frame, 
                text=text, 
                variable=var,
                bg='#0a0a0a',
                fg='#00FF88',  # Matrix green when selected
                selectcolor='#0a0a0a',
                activebackground='#1a1a1a',
                activeforeground='#00FFFF',
                font=('Segoe UI', 10, 'bold'),
                command=lambda c=category: self.update_checkbox_color(c)
            )
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=4)
            
            # Store checkbox reference
            self.category_checkboxes[category] = checkbox
            
            # Set initial color
            self.update_checkbox_color(category)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def create_progress_section(self, parent):
        """Enhanced progress section with dad jokes"""
        progress_frame = ttk.LabelFrame(parent, text="📊 SCAN STATUS", padding="15")
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="🎯 Ready to unleash digital reconnaissance...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var, 
                                       style='Progress.TLabel')
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                           style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Live stats
        self.stats_label = ttk.Label(progress_frame, text="", 
                                    style='Stats.TLabel')
        self.stats_label.grid(row=2, column=0, sticky=tk.W)
    
    def create_enhanced_results(self, parent):
        """Enhanced results section"""
        results_frame = ttk.LabelFrame(parent, text="🎯 INTELLIGENCE RESULTS", padding="15")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results display with enhanced formatting
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            height=20, 
            width=100,
            font=('Consolas', 9),
            bg='#1a1a1a',
            fg='#00FF88',
            insertbackground='#00CCFF',
            selectbackground='#FF1493'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Enhanced export options
        self.create_enhanced_export_buttons(results_frame)
    
    def create_enhanced_export_buttons(self, parent):
        """Enhanced export buttons with customer selection"""
        export_frame = ttk.Frame(parent)
        export_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Customer selection for exports
        ttk.Label(export_frame, text="Customer:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(export_frame, textvariable=self.customer_var, 
                                     width=20, state='readonly')
        customer_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.customer_combo = customer_combo
        self.update_customer_list()
        
        # Export buttons
        self.pdf_button = ttk.Button(export_frame, text="📄 Export Professional PDF",
                                   command=self.export_enhanced_pdf, style='Export.TButton')
        self.pdf_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.csv_button = ttk.Button(export_frame, text="📊 Export CSV Data",
                                   command=self.export_enhanced_csv, style='Export.TButton')
        self.csv_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(export_frame, text="🗑️ Clear Results",
                                     command=self.clear_results, style='Utility.TButton')
        self.clear_button.pack(side=tk.RIGHT)
        
        # Initially disable export buttons
        self.pdf_button.config(state='disabled')
        self.csv_button.config(state='disabled')
    
    def create_enhanced_bulk_tab(self):
        """Enhanced bulk scanning tab"""
        bulk_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(bulk_frame, text="🚀 Mass Intelligence")
        
        # Enhanced bulk scanning would go here
        ttk.Label(bulk_frame, text="🚀 MASS INTELLIGENCE OPERATIONS", 
                 style='Ultimate.TLabel').pack(pady=20)
        
        ttk.Label(bulk_frame, 
                 text="Enhanced bulk scanning with professional reporting\nand customer management integration!", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        ttk.Label(bulk_frame, 
                 text="🚧 Advanced bulk features coming in the next version! 🚧",
                 style='Info.TLabel').pack(pady=30)
    
    def create_customer_tab(self):
        """Customer management tab"""
        customer_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(customer_frame, text="👥 Customer Hub")
        
        ttk.Label(customer_frame, text="👥 CUSTOMER MANAGEMENT HUB", 
                 style='Ultimate.TLabel').pack(pady=20)
        
        # Quick customer management
        mgmt_frame = ttk.LabelFrame(customer_frame, text="Customer Management", padding="15")
        mgmt_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(mgmt_frame, text="➕ Add New Customer", 
                  command=self.add_customer_quick, style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(mgmt_frame, text="🎨 Open Branding Studio", 
                  command=self.open_branding_config, style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Customer list
        list_frame = ttk.LabelFrame(customer_frame, text="Current Customers", padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.customer_listbox = tk.Listbox(list_frame, height=15, 
                                          bg='#2a2a2a', fg='#00CCFF', 
                                          selectbackground='#FF1493')
        self.customer_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_customer_display()
    
    def create_export_hub_tab(self):
        """Export hub tab"""
        export_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(export_frame, text="📄 Export Hub")
        
        ttk.Label(export_frame, text="📄 PROFESSIONAL EXPORT HUB", 
                 style='Ultimate.TLabel').pack(pady=20)
        
        # Export templates and options would go here
        ttk.Label(export_frame, 
                 text="Professional PDF and CSV export with company branding,\ncustomer information, and dad jokes!",
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Export history
        ttk.Label(export_frame, text="📋 Recent Exports", 
                 style='Header.TLabel').pack(anchor=tk.W, pady=(30, 10))
        
        export_list = tk.Listbox(export_frame, height=10, 
                                bg='#2a2a2a', fg='#00CCFF')
        export_list.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def create_ultimate_status_bar(self, parent):
        """Ultimate status bar with jokes and stats"""
        status_frame = ttk.Frame(parent, style='Status.TFrame', padding="15")
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value=f"🎯 System Online • {get_dork_count()} Neural Queries Loaded • Ready for Digital Domination")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Version info
        version_label = ttk.Label(status_frame, text="v2.0 ULTIMATE 🚀", style='Version.TLabel')
        version_label.grid(row=0, column=1, sticky=tk.E)
    
    def setup_ultimate_styles(self):
        """Setup ultimate futuristic styles"""
        style = ttk.Style()
        
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Ultimate color scheme
        NEON_CYAN = '#00FFFF'
        HOT_PINK = '#FF1493'
        CYBER_GREEN = '#00FF88'
        ELECTRIC_BLUE = '#00CCFF'
        DEEP_PURPLE = '#8A2BE2'
        LIGHT_GRAY = '#E0E0E0'
        DARK_GRAY = '#2A2A2A'
        DARKER_GRAY = '#1A1A1A'
        BLACK_BG = '#0A0A0A'
        
        # Configure root
        self.root.configure(bg=BLACK_BG)
        
        # Ultimate title style
        style.configure('Ultimate.TLabel', 
                       foreground=NEON_CYAN, 
                       background=BLACK_BG,
                       font=('Segoe UI Light', 28, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       foreground=ELECTRIC_BLUE, 
                       background=BLACK_BG,
                       font=('Segoe UI', 12))
        
        style.configure('Joke.TLabel', 
                       foreground=HOT_PINK, 
                       background=BLACK_BG,
                       font=('Segoe UI', 10, 'italic'))
        
        # Button styles
        style.configure('Launch.TButton', 
                       foreground='white',
                       background=CYBER_GREEN,
                       font=('Segoe UI', 12, 'bold'),
                       relief='flat')
        
        style.configure('QuickAccess.TButton', 
                       foreground='white',
                       background=ELECTRIC_BLUE,
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        
        # More button styles
        style.configure('Action.TButton', 
                       foreground='white',
                       background=CYBER_GREEN,
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        
        style.configure('Secondary.TButton', 
                       foreground='white',
                       background=HOT_PINK,
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        
        style.configure('Export.TButton', 
                       foreground='white',
                       background=DARK_GRAY,
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        
        style.configure('Utility.TButton', 
                       foreground=LIGHT_GRAY,
                       background=DARKER_GRAY,
                       font=('Segoe UI', 9),
                       relief='flat')
        
        # Status and info styles
        style.configure('Status.TLabel', 
                       foreground=LIGHT_GRAY, 
                       background=BLACK_BG,
                       font=('Segoe UI', 9))
        
        style.configure('Version.TLabel', 
                       foreground=DEEP_PURPLE, 
                       background=BLACK_BG,
                       font=('Segoe UI', 8, 'bold'))
        
        style.configure('Progress.TLabel', 
                       foreground=CYBER_GREEN, 
                       background=BLACK_BG,
                       font=('Segoe UI', 10))
        
        style.configure('Stats.TLabel', 
                       foreground=ELECTRIC_BLUE, 
                       background=BLACK_BG,
                       font=('Segoe UI', 8))
        
        style.configure('Header.TLabel', 
                       foreground=HOT_PINK, 
                       background=BLACK_BG,
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Info.TLabel', 
                       foreground='orange', 
                       background=BLACK_BG,
                       font=('Segoe UI', 12))
    
    # Enhanced functionality methods
    
    def start_joke_rotation(self):
        """Start rotating dad jokes"""
        def rotate_joke():
            if hasattr(self, 'joke_label'):
                try:
                    new_joke = self.dad_jokes.get_smart_joke()
                    self.joke_label.config(text=new_joke)
                except:
                    pass
            # Schedule next rotation
            self.joke_timer_id = self.root.after(30000, rotate_joke)  # Every 30 seconds
        
        self.joke_timer_id = self.root.after(30000, rotate_joke)
    
    def show_random_joke(self):
        """Show a random dad joke immediately"""
        joke = self.dad_jokes.get_random_joke()
        self.joke_label.config(text=joke)
        self.show_notification(f"😂 {joke}", "info")
    
    def show_notification(self, message, msg_type="info"):
        """Show notification message"""
        if msg_type == "info":
            messagebox.showinfo("🎯 MissDorking Ultimate", message)
        elif msg_type == "error":
            messagebox.showerror("❌ MissDorking Ultimate", message)
        elif msg_type == "success":
            messagebox.showinfo("✅ MissDorking Ultimate", message)
    
    def open_branding_config(self):
        """Open branding configuration"""
        show_branding_config(self.root)
        # Refresh customer list after potential changes
        self.root.after(500, self.update_customer_list)
    
    def update_customer_list(self):
        """Update customer dropdown"""
        if hasattr(self, 'customer_combo'):
            customers = self.branding_manager.get_all_customers()
            customer_list = ["[No Customer Selected]"]
            for cust_id, cust_data in customers.items():
                name = cust_data.get('name', 'Unknown')
                company = cust_data.get('company', '')
                display_name = f"{name} - {company}" if company else name
                customer_list.append(f"{cust_id}:{display_name}")
            
            self.customer_combo['values'] = customer_list
            if not self.customer_var.get():
                self.customer_var.set(customer_list[0])
    
    def refresh_customer_display(self):
        """Refresh customer display list"""
        if hasattr(self, 'customer_listbox'):
            self.customer_listbox.delete(0, tk.END)
            customers = self.branding_manager.get_all_customers()
            
            if not customers:
                self.customer_listbox.insert(tk.END, "No customers added yet - Click 'Add New Customer' to get started!")
            else:
                for cust_id, cust_data in customers.items():
                    display_text = f"👤 {cust_data.get('name', 'Unknown')}"
                    if cust_data.get('company'):
                        display_text += f" ({cust_data['company']})"
                    display_text += f" - ID: {cust_id}"
                    self.customer_listbox.insert(tk.END, display_text)
    
    def add_customer_quick(self):
        """Quick add customer dialog"""
        # Simple dialog for adding customers
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("400x300")
        dialog.configure(bg='#0a0a0a')
        
        # Simple form
        ttk.Label(dialog, text="Customer Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Company:").pack(pady=5)
        company_entry = ttk.Entry(dialog, width=40)
        company_entry.pack(pady=5)
        
        def save_customer():
            name = name_entry.get().strip()
            company = company_entry.get().strip()
            if name:
                import uuid
                customer_id = str(uuid.uuid4())[:8]
                self.branding_manager.add_customer(customer_id, name, company)
                dialog.destroy()
                self.refresh_customer_display()
                self.update_customer_list()
                self.show_notification(f"✅ Customer '{name}' added successfully!", "success")
            else:
                self.show_notification("Please enter a customer name.", "error")
        
        ttk.Button(dialog, text="Save Customer", command=save_customer).pack(pady=20)
    
    def update_checkbox_color(self, category):
        """Update checkbox color based on selection state"""
        if category in self.category_checkboxes:
            checkbox = self.category_checkboxes[category]
            is_selected = self.category_vars[category].get()
            
            if is_selected:
                # Matrix green when selected
                checkbox.config(fg='#00FF88', activeforeground='#00FFFF')
            else:
                # Neon red when not selected
                checkbox.config(fg='#FF1493', activeforeground='#FF69B4')
    
    def select_all_categories(self):
        """Select all categories with visual feedback"""
        for category, var in self.category_vars.items():
            var.set(True)
            self.update_checkbox_color(category)
        
        # Show feedback
        self.progress_var.set("✅ All categories selected - Ready for maximum intel!")
    
    def clear_all_categories(self):
        """Clear all categories with visual feedback"""
        for category, var in self.category_vars.items():
            var.set(False)
            self.update_checkbox_color(category)
        
        # Show feedback
        self.progress_var.set("❌ All categories cleared - Select categories to scan!")
    
    def on_enter_pressed(self, event):
        """Handle Enter key in domain entry"""
        if not self.is_running:
            self.start_enhanced_scan()
    
    def start_enhanced_scan(self):
        """Start enhanced scanning with dad jokes"""
        if self.is_running:
            self.show_notification("Scan already in progress! 🚀", "info")
            return
        
        # Try to get domain from both the variable and directly from the entry widget
        domain_from_var = self.domain_var.get().strip()
        domain_from_entry = self.domain_entry.get().strip()
        
        print(f"DEBUG: Domain from variable: '{domain_from_var}'")
        print(f"DEBUG: Domain from entry widget: '{domain_from_entry}'")
        
        # Use whichever one has content
        domain = domain_from_entry if domain_from_entry else domain_from_var
        
        print(f"DEBUG: Final domain value: '{domain}'")  
        print(f"DEBUG: Final domain length: {len(domain)}")
        
        if not domain:
            print("DEBUG: Domain validation failed - empty domain")
            self.show_notification("Please enter a domain to scan! 🎯", "error")
            return
        
        print(f"DEBUG: Domain validation passed: {domain}")
        
        # Update the variable with the correct value
        self.domain_var.set(domain)
        
        # Check categories
        if not any(var.get() for var in self.category_vars.values()):
            self.show_notification("Please select at least one category! 📋", "error")
            return
        
        # Show scan joke
        scan_joke = get_scan_message()
        self.progress_var.set(f"🚀 {scan_joke}")
        
        self.is_running = True
        self.scan_button.config(state='disabled', text='🔄 SCANNING...')
        self.pdf_button.config(state='disabled')
        self.csv_button.config(state='disabled')
        
        # Start scan in thread
        thread = threading.Thread(target=self.run_enhanced_scan)
        thread.daemon = True
        thread.start()
    
    def run_enhanced_scan(self):
        """Run the enhanced scanning process with jokes and progress tracking"""
        try:
            domain = self.domain_var.get().strip()
            max_results = int(self.results_per_query_var.get())
            
            # Clean domain
            domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
            
            # Get selected categories
            selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
            
            # Get dorks
            all_dorks = get_all_dorks_for_domain(domain)
            filtered_dorks = {cat: dorks for cat, dorks in all_dorks.items() 
                            if cat in selected_categories}
            
            # Count total queries and initialize timing
            total_queries = sum(len(dorks) for dorks in filtered_dorks.values())
            scan_start_time = time.time()
            
            self.root.after(0, lambda: self.progress_bar.config(maximum=total_queries))
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            
            # Add header with style
            header = f"""
🎯 MISSDORKING™ ULTIMATE SCAN REPORT
{'='*80}
Target: {domain}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Categories: {', '.join(selected_categories)}
Total Queries: {total_queries}
{'='*80}

"""
            
            self.root.after(0, lambda: self.results_text.insert(tk.END, header))
            
            results = {}
            current_query = 0
            
            for category, dorks in filtered_dorks.items():
                category_results = {}
                self.root.after(0, lambda c=category: self.results_text.insert(
                    tk.END, f"\n🎯 === {c.upper()} === 🎯\n"))
                
                for dork in dorks:
                    current_query += 1
                    progress_pct = (current_query / total_queries) * 100
                    
                    # Calculate timing and ETA
                    elapsed_time = time.time() - scan_start_time
                    if current_query > 0:
                        avg_time_per_query = elapsed_time / current_query
                        remaining_queries = total_queries - current_query
                        eta_seconds = remaining_queries * avg_time_per_query
                        
                        # Format ETA
                        if eta_seconds > 60:
                            eta_text = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
                        else:
                            eta_text = f"{int(eta_seconds)}s"
                    else:
                        eta_text = "Calculating..."
                    
                    # Update progress with enhanced information
                    progress_joke = get_progress_message(progress_pct)
                    status_text = f"[{current_query}/{total_queries}] {progress_pct:.1f}% • ETA: {eta_text} • {progress_joke}"
                    
                    self.root.after(0, lambda st=status_text: self.progress_var.set(st))
                    self.root.after(0, lambda v=current_query: self.progress_bar.config(value=v))
                    
                    # Update stats display
                    elapsed_text = f"{int(elapsed_time)}s" if elapsed_time < 60 else f"{int(elapsed_time // 60)}m {int(elapsed_time % 60)}s"
                    stats_text = f"⚡ Speed: {current_query/elapsed_time:.1f} queries/sec • ⏱️ Elapsed: {elapsed_text} • 🎯 Found: {sum(len(category_results.get(d, [])) for d in category_results)} results"
                    self.root.after(0, lambda st=stats_text: self.stats_label.config(text=st))
                    
                    # Perform search
                    search_results = self.scraper.search_google(dork, max_results)
                    category_results[dork] = search_results
                    
                    # Display results with enhanced formatting
                    result_count = len(search_results)
                    if result_count > 0:
                        self.root.after(0, lambda d=dork, c=result_count: 
                                       self.results_text.insert(tk.END, f"✅ {d}: {c} results\n"))
                        
                        # Show top results
                        for i, result in enumerate(search_results[:3]):
                            title = result.get('title', 'No title')[:100]
                            url = result.get('url', 'No URL')
                            self.root.after(0, lambda t=title, u=url: 
                                           self.results_text.insert(tk.END, f"  🎯 {t}\n     🔗 {u}\n"))
                        
                        if result_count > 3:
                            self.root.after(0, lambda c=result_count: 
                                           self.results_text.insert(tk.END, f"  📋 ... and {c-3} more results\n"))
                    else:
                        self.root.after(0, lambda d=dork: 
                                       self.results_text.insert(tk.END, f"❌ {d}: No results\n"))
                    
                    self.root.after(0, lambda: self.results_text.insert(tk.END, "\n"))
                    self.root.after(0, lambda: self.results_text.see(tk.END))
                
                results[category] = category_results
            
            # Final analysis and completion
            self.root.after(0, lambda: self.progress_var.set("🎯 Analyzing results for security intelligence..."))
            analyzed_results = self.analyzer.categorize_results(results)
            
            # Generate summary
            summary_report = self.analyzer.generate_report_summary(analyzed_results)
            self.root.after(0, lambda: self.results_text.insert(tk.END, summary_report))
            
            self.results = analyzed_results
            
            # Completion with dad joke
            total_results = sum(sum(len(results) for results in cat.values()) 
                              for cat in results.values())
            
            completion_joke = get_export_message()
            final_message = f"🎉 SCAN COMPLETE! 🎉\n{total_results} total results found!\n\n😂 {completion_joke}"
            
            self.root.after(0, lambda: self.progress_var.set(final_message.split('\n')[0]))
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"\n{'='*80}\n{final_message}\n{'='*80}\n"))
            self.root.after(0, lambda: self.results_text.see(tk.END))
            
            logging.info(f"Enhanced scan completed for {domain}. Total results: {total_results}")
            
        except Exception as e:
            error_msg = f"Scan failed: {str(e)}"
            self.root.after(0, lambda: self.show_notification(f"❌ {error_msg}", "error"))
            logging.error(error_msg)
        
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.scan_button.config(state='normal', text='🚀 LAUNCH SCAN'))
            self.root.after(0, lambda: self.pdf_button.config(state='normal'))
            self.root.after(0, lambda: self.csv_button.config(state='normal'))
    
    def export_enhanced_pdf(self):
        """Export PDF with enhanced branding and customer info"""
        if not self.results:
            self.show_notification("No results to export! Run a scan first. 🎯", "error")
            return
        
        # Get customer ID if selected
        customer_selection = self.customer_var.get()
        customer_id = None
        if customer_selection and not customer_selection.startswith('[No Customer'):
            customer_id = customer_selection.split(':')[0]
        
        try:
            domain = self.domain_var.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Professional PDF Report"
            )
            
            if filename:
                # Show export joke
                export_joke = get_export_message()
                self.progress_var.set(f"📄 {export_joke}")
                
                # Export with customer info
                filepath = self.exporter.export_to_pdf(self.results, domain, filename, customer_id)
                self.show_notification(f"✅ Professional PDF report saved!\n{filepath}", "success")
                
                if messagebox.askyesno("Open Report", "Would you like to open the PDF report?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            self.show_notification(f"❌ PDF export failed: {str(e)}", "error")
    
    def export_enhanced_csv(self):
        """Export CSV with enhanced data"""
        if not self.results:
            self.show_notification("No results to export! Run a scan first. 🎯", "error")
            return
        
        try:
            domain = self.domain_var.get().strip()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save CSV Data Export"
            )
            
            if filename:
                export_joke = get_export_message()
                self.progress_var.set(f"📊 {export_joke}")
                
                filepath = self.exporter.export_to_csv(self.results, domain, filename)
                self.show_notification(f"✅ CSV data exported successfully!\n{filepath}", "success")
                
                if messagebox.askyesno("Open File", "Would you like to open the CSV file?"):
                    if sys.platform.startswith('win'):
                        os.startfile(filepath)
                    else:
                        webbrowser.open(f'file://{filepath}')
                        
        except Exception as e:
            self.show_notification(f"❌ CSV export failed: {str(e)}", "error")
    
    def clear_results(self):
        """Clear results with confirmation"""
        if messagebox.askyesno("Clear Results", "Are you sure you want to clear all results?"):
            self.results_text.delete(1.0, tk.END)
            self.results = {}
            self.progress_bar.config(value=0)
            self.progress_var.set("🎯 Results cleared - Ready for next mission!")
            self.pdf_button.config(state='disabled')
            self.csv_button.config(state='disabled')
            
            # Show a dad joke to cheer up
            joke = self.dad_jokes.get_random_joke()
            self.root.after(2000, lambda: self.progress_var.set(f"😂 {joke}"))
    
    def show_about_dialog(self):
        """Show about dialog with dad joke"""
        about_text = f"""
🚀 MISSDORKING™ ULTIMATE v2.0 🚀

The most advanced Google Dorking platform ever created!

✨ Features:
• Professional PDF/CSV exports with company branding
• Customer management and logo integration
• Dad jokes for enhanced user experience
• Futuristic UI with cyberpunk aesthetics
• Advanced intelligence categorization
• Bulk scanning capabilities

💋 Making cybersecurity fabulous since 2024!

😂 Random Dad Joke:
{self.dad_jokes.get_random_joke()}

© 2024 MissDorking™ - Professional Intelligence Suite
        """
        
        messagebox.showinfo("About MissDorking Ultimate", about_text)
    
    def __del__(self):
        """Cleanup when app is destroyed"""
        if hasattr(self, 'joke_timer_id') and self.joke_timer_id:
            try:
                self.root.after_cancel(self.joke_timer_id)
            except:
                pass

def main():
    """Launch MissDorking Ultimate! 🚀"""
    
    def start_ultimate_app():
        """Start the ultimate application"""
        root = tk.Tk()
        app = MissDorkingUltimate(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            logging.info("Ultimate app interrupted by user")
        except Exception as e:
            logging.error(f"Ultimate app error: {e}")
            messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n{e}")
    
    # Show fun splash screen if available, then start app
    try:
        from fun_splash import show_fun_splash
        show_fun_splash(start_ultimate_app)
    except ImportError:
        # No splash screen available, start directly
        start_ultimate_app()

if __name__ == "__main__":
    main()
