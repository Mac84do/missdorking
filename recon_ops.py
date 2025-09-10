"""
RECON-OPS v2.0 - Tactical Intelligence Gathering System
========================================================
Advanced Google Dork Query Generator for Intelligence Operations
No scanning - Pure query generation for manual HUMINT/SIGINT operations

Author: Tactical Operations Team
Classification: UNCLASSIFIED
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import pyperclip
import os
import sys
import webbrowser
import urllib.parse
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
import json

# Import our dorks module
from google_dorks import GOOGLE_DORKS, get_dork_count

class ReconOpsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RECON-OPS v2.0 - Tactical Intelligence Platform")
        
        # Get screen dimensions for responsive sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Load saved window settings or use defaults
        self.config_file = "recon_ops_settings.json"
        self.window_settings = self.load_window_settings()
        
        # Calculate responsive window size with user preferences
        if self.window_settings.get('remember_size', True):
            window_width = self.window_settings.get('width', min(max(1000, int(screen_width * 0.75)), 1400))
            window_height = self.window_settings.get('height', min(max(700, int(screen_height * 0.75)), 1000))
        else:
            window_width = min(max(1000, int(screen_width * 0.75)), 1400)
            window_height = min(max(700, int(screen_height * 0.75)), 1000)
        
        # Set initial geometry
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#0a0a0a')
        
        # Set more reasonable minimum size for better usability
        self.root.minsize(800, 600)
        
        # Make window resizable and set maximum size
        self.root.resizable(True, True)
        self.root.maxsize(screen_width, screen_height)
        
        # Auto-maximize if preferred by user or if screen is small
        if (self.window_settings.get('start_maximized', False) or 
            screen_width <= 1366 or screen_height <= 768):  # Maximize on smaller screens
            try:
                self.root.state('zoomed')  # Windows equivalent of maximize
            except:
                pass  # Fallback gracefully if zoomed is not supported
        
        # Bind window closing event to save settings
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Military color scheme
        self.colors = {
            'bg_primary': '#0a0a0a',      # Deep black
            'bg_secondary': '#1a1a1a',    # Dark gray
            'bg_tertiary': '#2a2a2a',     # Medium gray
            'accent_green': '#00ff41',    # Matrix green
            'accent_amber': '#ffb000',    # Tactical amber
            'accent_red': '#ff2600',      # Danger red
            'text_primary': '#00ff41',    # Matrix green text
            'text_secondary': '#cccccc',  # Light gray text
            'text_subtle': '#888888',     # Subtle gray
            'border': '#444444'           # Border gray
        }
        
        # Application state
        self.target_domain = tk.StringVar()
        self.generated_queries = {}
        self.category_vars = {}
        self.browser_offset = 0  # Track which queries have been opened
        
        # Initialize UI
        self.setup_styles()
        self.create_widgets()
        
        # Focus on domain entry
        self.domain_entry.focus()

    def setup_styles(self):
        """Configure military-grade tactical styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure main styles with military theme
        style.configure('Military.TLabel',
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'],
                       font=('Consolas', 10, 'bold'))
        
        style.configure('Header.TLabel',
                       foreground=self.colors['accent_amber'],
                       background=self.colors['bg_primary'],
                       font=('Consolas', 16, 'bold'))
        
        style.configure('Title.TLabel',
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'],
                       font=('Consolas', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       foreground=self.colors['text_subtle'],
                       background=self.colors['bg_primary'],
                       font=('Consolas', 10))
        
        style.configure('Status.TLabel',
                       foreground=self.colors['accent_amber'],
                       background=self.colors['bg_secondary'],
                       font=('Consolas', 9, 'bold'))
        
        # Frame styling
        style.configure('Military.TFrame',
                       background=self.colors['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Panel.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='solid',
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        style.configure('TLabelFrame',
                       foreground=self.colors['accent_green'],
                       background=self.colors['bg_primary'],
                       bordercolor=self.colors['accent_green'],
                       font=('Consolas', 10, 'bold'))
        
        style.configure('TLabelFrame.Label',
                       foreground=self.colors['accent_green'],
                       background=self.colors['bg_primary'],
                       font=('Consolas', 10, 'bold'))
        
        # Entry styling
        style.configure('Military.TEntry',
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       bordercolor=self.colors['accent_green'],
                       insertcolor=self.colors['accent_green'],
                       selectbackground=self.colors['accent_green'],
                       selectforeground=self.colors['bg_primary'],
                       font=('Consolas', 12, 'bold'),
                       relief='solid',
                       borderwidth=2)
        
        # Button styling - Tactical operations
        style.configure('Tactical.TButton',
                       foreground=self.colors['bg_primary'],
                       background=self.colors['accent_green'],
                       bordercolor=self.colors['accent_green'],
                       focuscolor='none',
                       font=('Consolas', 12, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(20, 10))
        
        style.map('Tactical.TButton',
                 background=[('active', '#00cc33'),
                           ('pressed', self.colors['accent_amber'])])
        
        style.configure('Command.TButton',
                       foreground=self.colors['bg_primary'],
                       background=self.colors['accent_amber'],
                       bordercolor=self.colors['accent_amber'],
                       focuscolor='none',
                       font=('Consolas', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(15, 8))
        
        style.map('Command.TButton',
                 background=[('active', '#cc8800'),
                           ('pressed', self.colors['accent_green'])])
        
        style.configure('Danger.TButton',
                       foreground='white',
                       background=self.colors['accent_red'],
                       bordercolor=self.colors['accent_red'],
                       focuscolor='none',
                       font=('Consolas', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(15, 8))
        
        # Checkbox styling
        style.configure('Military.TCheckbutton',
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'],
                       focuscolor='none',
                       font=('Consolas', 9))
        
        style.map('Military.TCheckbutton',
                 foreground=[('active', self.colors['accent_green'])])

    def create_banner(self, parent):
        """Create tactical ASCII-style banner"""
        banner_frame = ttk.Frame(parent, style='Military.TFrame')
        banner_frame.pack(fill=tk.X, pady=(0, 20))
        
        banner_text = """
╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔═╗╔═╗╔═╗   ╦  ╦╔═╗  ╔═╗
╠╦╝╠═ ║  ║ ║║║║  ║ ║╠═╝╚═╗   ╚╗╔╝╔═╝  ║ ║
╩╚═╚═╝╚═╝╚═╝╝╚╝  ╚═╝╩  ╚═╝    ╚╝ ╚═╝  ╚═╝

TACTICAL INTELLIGENCE GATHERING SYSTEM
========================================
        """
        
        banner_label = tk.Label(banner_frame, 
                               text=banner_text,
                               foreground=self.colors['accent_green'],
                               background=self.colors['bg_primary'],
                               font=('Consolas', 8, 'bold'),
                               justify=tk.CENTER)
        banner_label.pack()
        
        subtitle = tk.Label(banner_frame,
                           text="[ GOOGLE DORK QUERY GENERATOR - NO ACTIVE SCANNING ]",
                           foreground=self.colors['accent_amber'],
                           background=self.colors['bg_primary'],
                           font=('Consolas', 10, 'bold'))
        subtitle.pack(pady=(5, 0))

    def create_donation_section(self, parent):
        """Create prominent donation section"""
        donation_frame = ttk.Frame(parent, style='Panel.TFrame', padding="15")
        donation_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Main donation container
        donation_container = ttk.Frame(donation_frame, style='Panel.TFrame')
        donation_container.pack(fill=tk.X)
        
        # Left side - Message
        left_frame = ttk.Frame(donation_container, style='Panel.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Coffee emoji and title
        title_frame = ttk.Frame(left_frame, style='Panel.TFrame')
        title_frame.pack(anchor=tk.W, pady=(0, 5))
        
        coffee_label = tk.Label(title_frame,
                               text="☕",
                               foreground='#ffb000',
                               background=self.colors['bg_secondary'],
                               font=('Consolas', 20, 'bold'))
        coffee_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame,
                              text="SUPPORT RECON-OPS DEVELOPMENT",
                              foreground=self.colors['accent_amber'],
                              background=self.colors['bg_secondary'],
                              font=('Consolas', 12, 'bold'))
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Description
        desc_label = tk.Label(left_frame,
                             text="Help keep this tactical tool free and updated! Your support enables new features,\nbug fixes, and continued development. Every coffee helps! 🎯⚡",
                             foreground=self.colors['text_secondary'],
                             background=self.colors['bg_secondary'],
                             font=('Consolas', 9),
                             justify=tk.LEFT)
        desc_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Right side - Donation button
        right_frame = ttk.Frame(donation_container, style='Panel.TFrame')
        right_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Big prominent donation button
        donate_big_btn = tk.Button(right_frame,
                                  text="☕ BUY ME A COFFEE",
                                  command=lambda: webbrowser.open('https://ko-fi.com/macedo84'),
                                  bg='#ff813f',  # Ko-fi orange color
                                  fg='white',
                                  font=('Consolas', 14, 'bold'),
                                  relief='flat',
                                  borderwidth=0,
                                  padx=30,
                                  pady=15,
                                  cursor='hand2')
        donate_big_btn.pack()
        
        # Hover effects
        def on_enter(e):
            donate_big_btn.config(bg='#e66f2e')
        def on_leave(e):
            donate_big_btn.config(bg='#ff813f')
            
        donate_big_btn.bind('<Enter>', on_enter)
        donate_big_btn.bind('<Leave>', on_leave)
        
        # Ko-fi link
        link_label = tk.Label(right_frame,
                             text="ko-fi.com/macedo84",
                             foreground=self.colors['accent_green'],
                             background=self.colors['bg_secondary'],
                             font=('Consolas', 8),
                             cursor='hand2')
        link_label.pack(pady=(5, 0))
        link_label.bind('<Button-1>', lambda e: webbrowser.open('https://ko-fi.com/macedo84'))

    def create_widgets(self):
        """Create main application interface"""
        # Main container with fixed structure
        main_frame = ttk.Frame(self.root, style='Military.TFrame', padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # TOP SECTION - Banner (Fixed height)
        top_frame = ttk.Frame(main_frame, style='Military.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        self.create_banner(top_frame)
        
        # DONATION SECTION - Prominent display
        self.create_donation_section(main_frame)
        
        # MIDDLE SECTION - Controls (Fixed height)
        controls_frame = ttk.Frame(main_frame, style='Military.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Target input - COMPACT
        target_frame = ttk.LabelFrame(controls_frame, text="[ TARGET ACQUISITION ]", padding="10")
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        target_input_frame = ttk.Frame(target_frame, style='Military.TFrame')
        target_input_frame.pack(fill=tk.X)
        
        ttk.Label(target_input_frame, text="DOMAIN:", style='Military.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.domain_entry = ttk.Entry(target_input_frame, 
                                     textvariable=self.target_domain,
                                     style='Military.TEntry',
                                     width=40)
        self.domain_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        self.domain_entry.bind('<Return>', self.generate_queries)
        
        self.generate_btn = ttk.Button(target_input_frame, 
                                     text="⚡ GENERATE",
                                     command=self.generate_queries,
                                     style='Tactical.TButton')
        self.generate_btn.pack(side=tk.RIGHT)
        
        # Categories - COMPACT
        categories_frame = ttk.LabelFrame(controls_frame, text="[ CATEGORIES ]", padding="10")
        categories_frame.pack(fill=tk.X, pady=(0, 10))
        self.create_category_selection(categories_frame)
        
        # QUERIES SECTION - Expandable with flexible height
        queries_main_frame = ttk.Frame(main_frame, style='Military.TFrame')
        queries_main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        queries_frame = ttk.LabelFrame(queries_main_frame, text="[ TACTICAL QUERIES ]", padding="10")
        queries_frame.pack(fill=tk.BOTH, expand=True)
        
        # RESPONSIVE text area that expands with window
        self.queries_text = scrolledtext.ScrolledText(
            queries_frame,
            font=('Consolas', 9),  # Slightly larger font for better readability
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_green'],
            selectbackground=self.colors['accent_green'],
            selectforeground=self.colors['bg_primary'],
            relief='solid',
            borderwidth=2,
            wrap=tk.WORD  # Enable word wrapping for better text flow
        )
        self.queries_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # BOTTOM SECTION - GUARANTEED VISIBLE BUTTONS
        bottom_frame = ttk.Frame(main_frame, style='Military.TFrame')
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Command buttons frame - ALWAYS AT BOTTOM
        command_frame = ttk.Frame(bottom_frame, style='Military.TFrame', padding="10")
        command_frame.pack(fill=tk.X)
        
        # BIG VISIBLE BUTTONS
        btn_frame = ttk.Frame(command_frame, style='Military.TFrame')
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # First row of buttons
        btn_row1 = ttk.Frame(btn_frame, style='Military.TFrame')
        btn_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(btn_row1, text="📋 COPY ALL",
                  command=self.copy_all_queries, style='Command.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_row1, text="💾 EXPORT",
                  command=self.export_queries, style='Command.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_row1, text="🌐 OPEN BROWSER",
                  command=self.open_queries_in_browser, style='Tactical.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_row1, text="🗑️ CLEAR",
                  command=self.clear_queries, style='Danger.TButton').pack(side=tk.LEFT)
        
        # Status bar - ALWAYS VISIBLE
        status_frame = ttk.Frame(bottom_frame, style='Panel.TFrame', padding="5")
        status_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value=f"⚡ RECON-OPS READY | {get_dork_count()} QUERIES LOADED")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.pack(side=tk.LEFT)
        
        # DONATION BUTTON - BIG AND VISIBLE
        donate_btn = ttk.Button(status_frame, 
                               text="☕ DONATE",
                               command=lambda: webbrowser.open('https://ko-fi.com/macedo84'),
                               style='Command.TButton')
        donate_btn.pack(side=tk.RIGHT, padx=(10, 0))

    def create_category_selection(self, parent):
        """Create intelligence category selection checkboxes"""
        # Select all/none buttons
        select_frame = ttk.Frame(parent, style='Military.TFrame')
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(select_frame, text="✓ SELECT ALL", 
                  command=self.select_all_categories, style='Command.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(select_frame, text="✗ CLEAR ALL", 
                  command=self.clear_all_categories, style='Command.TButton').pack(side=tk.LEFT)
        
        # Category grid
        categories_grid = ttk.Frame(parent, style='Military.TFrame')
        categories_grid.pack(fill=tk.X)
        
        # Create checkboxes for each category
        row = 0
        col = 0
        max_cols = 4
        
        for category in GOOGLE_DORKS.keys():
            var = tk.BooleanVar(value=True)  # All selected by default
            self.category_vars[category] = var
            
            # Create checkbox with military styling
            cb = ttk.Checkbutton(categories_grid, 
                               text=f"⚡ {category}",
                               variable=var,
                               style='Military.TCheckbutton')
            cb.grid(row=row, column=col, sticky=tk.W, padx=(0, 30), pady=5)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def generate_queries(self, event=None):
        """Generate Google dork queries for the target domain"""
        domain = self.target_domain.get().strip()
        
        if not domain:
            messagebox.showerror("ERROR", "Target domain required for intelligence operation.")
            return
        
        # Clean domain
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').strip('/')
        self.target_domain.set(domain)
        
        # Get selected categories
        selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
        
        if not selected_categories:
            messagebox.showerror("ERROR", "Select at least one intelligence category.")
            return
        
        # Generate queries
        self.generated_queries = {}
        self.browser_offset = 0  # Reset browser batch tracking for new queries
        query_output = []
        
        query_output.append("="*80)
        query_output.append(f"TACTICAL INTELLIGENCE QUERIES FOR: {domain.upper()}")
        query_output.append(f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        query_output.append(f"CATEGORIES: {len(selected_categories)} selected")
        query_output.append("="*80)
        query_output.append("")
        
        total_queries = 0
        
        for category in selected_categories:
            if category in GOOGLE_DORKS:
                category_queries = []
                query_output.append(f"◆ {category.upper()}")
                query_output.append("-" * (len(category) + 2))
                
                for i, dork in enumerate(GOOGLE_DORKS[category], 1):
                    formatted_query = dork.format(domain=domain)
                    category_queries.append(formatted_query)
                    query_output.append(f"{i:2d}. {formatted_query}")
                    total_queries += 1
                
                query_output.append("")
                self.generated_queries[category] = category_queries
        
        query_output.append("="*80)
        query_output.append(f"OPERATION SUMMARY:")
        query_output.append(f"• Total Queries Generated: {total_queries}")
        query_output.append(f"• Categories Covered: {len(selected_categories)}")
        query_output.append(f"• Target Domain: {domain}")
        query_output.append("")
        query_output.append("INSTRUCTIONS:")
        query_output.append("1. Copy individual queries or export all")
        query_output.append("2. Execute manually in Google Search")
        query_output.append("3. Analyze results for intelligence value")
        query_output.append("4. Maintain operational security")
        query_output.append("="*80)
        
        # Display in text area
        self.queries_text.delete(1.0, tk.END)
        self.queries_text.insert(tk.END, "\n".join(query_output))
        
        # Update status
        self.status_var.set(f"⚡ QUERIES GENERATED | {total_queries} TACTICAL QUERIES | TARGET: {domain.upper()}")

    def copy_all_queries(self):
        """Copy all generated queries to clipboard"""
        if not self.generated_queries:
            messagebox.showwarning("WARNING", "No queries generated. Execute intelligence generation first.")
            return
        
        try:
            # Get all text from the text widget
            all_text = self.queries_text.get(1.0, tk.END)
            pyperclip.copy(all_text)
            messagebox.showinfo("SUCCESS", "All tactical queries copied to clipboard!")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to copy queries: {str(e)}")

    def export_queries(self):
        """Export queries to file"""
        if not self.generated_queries:
            messagebox.showwarning("WARNING", "No queries generated. Execute intelligence generation first.")
            return
        
        domain = self.target_domain.get().strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"RECON_OPS_{domain}_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialname=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    all_text = self.queries_text.get(1.0, tk.END)
                    f.write(all_text)
                messagebox.showinfo("SUCCESS", f"Tactical queries exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("ERROR", f"Failed to export queries: {str(e)}")

    def get_all_queries_flat(self):
        """Get all queries as a flat list for batch processing"""
        all_queries = []
        for category, queries in self.generated_queries.items():
            all_queries.extend(queries)
        return all_queries

    def open_queries_in_browser(self):
        """Open queries in browser tabs with batch processing support"""
        if not self.generated_queries:
            messagebox.showwarning("WARNING", "No queries generated. Execute intelligence generation first.")
            return
        
        # Get all queries as flat list
        all_queries = self.get_all_queries_flat()
        total_queries = len(all_queries)
        remaining_queries = total_queries - self.browser_offset
        
        if remaining_queries <= 0:
            # All queries have been opened, offer to restart
            result = messagebox.askyesno(
                "ALL QUERIES OPENED",
                f"All {total_queries} queries have been opened in browser tabs.\n\n"
                "Do you want to restart from the beginning?"
            )
            if result:
                self.browser_offset = 0
                remaining_queries = total_queries
            else:
                return
        
        # Determine how many tabs to open in this batch
        max_tabs_per_batch = 15
        tabs_to_open = min(remaining_queries, max_tabs_per_batch)
        
        # Confirmation dialog
        batch_info = f"BATCH {(self.browser_offset // max_tabs_per_batch) + 1}"
        result = messagebox.askyesnocancel(
            f"TACTICAL BROWSER OPERATION - {batch_info}", 
            f"Opening queries {self.browser_offset + 1} to {self.browser_offset + tabs_to_open} of {total_queries}\n\n"
            f"📊 This batch: {tabs_to_open} tabs\n"
            f"⏳ Remaining after this batch: {remaining_queries - tabs_to_open} queries\n\n"
            "⚡ Perfect for evidence gathering and pentest reports!\n\n"
            "☕ Support RECON-OPS: https://ko-fi.com/macedo84\n\n"
            "Continue with browser operation?"
        )
        
        if result is None:  # Cancel clicked - open donation
            try:
                webbrowser.open("https://ko-fi.com/macedo84")
                messagebox.showinfo("SUPPORT", "Thank you for supporting RECON-OPS development! ☕⚡")
            except:
                messagebox.showinfo("SUPPORT", "Support link: https://ko-fi.com/macedo84")
            return
        elif not result:  # No clicked
            return
        
        # Open queries in browser tabs
        opened_count = 0
        start_index = self.browser_offset
        end_index = min(start_index + max_tabs_per_batch, total_queries)
        
        try:
            for i in range(start_index, end_index):
                query = all_queries[i]
                
                # Encode query for URL
                encoded_query = urllib.parse.quote_plus(query)
                google_url = f"https://www.google.com/search?q={encoded_query}"
                
                # Open in browser
                webbrowser.open_new_tab(google_url)
                opened_count += 1
            
            # Update offset for next batch
            self.browser_offset += opened_count
            remaining_after_batch = total_queries - self.browser_offset
            
            # Update status
            if remaining_after_batch > 0:
                self.status_var.set(f"🌐 BATCH COMPLETE | {opened_count} TABS OPENED | {remaining_after_batch} QUERIES REMAINING")
            else:
                self.status_var.set(f"🌐 ALL QUERIES OPENED | {total_queries} TOTAL TABS | EVIDENCE GATHERING COMPLETE")
            
            # Success message with next steps
            if remaining_after_batch > 0:
                next_batch_size = min(remaining_after_batch, max_tabs_per_batch)
                messagebox.showinfo(
                    "BATCH OPERATION SUCCESS", 
                    f"✅ Batch {(start_index // max_tabs_per_batch) + 1} opened successfully!\n\n"
                    f"📊 This batch: {opened_count} Google Search tabs\n"
                    f"🎯 Target: {self.target_domain.get().upper()}\n\n"
                    f"⏭️ NEXT: {remaining_after_batch} queries remaining\n"
                    f"📝 Click '🌐 OPEN BROWSER' again to open next {next_batch_size} tabs\n\n"
                    f"☕ Support development: https://ko-fi.com/macedo84"
                )
            else:
                messagebox.showinfo(
                    "ALL QUERIES OPENED", 
                    f"🎉 ALL QUERIES COMPLETED!\n\n"
                    f"📊 Total opened: {total_queries} Google Search tabs\n"
                    f"🎯 Target: {self.target_domain.get().upper()}\n\n"
                    f"✅ Evidence gathering phase complete!\n"
                    f"📝 Perfect for pentest reports and documentation\n\n"
                    f"☕ Support development: https://ko-fi.com/macedo84"
                )
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Browser operation failed: {str(e)}")
    
    def clear_queries(self):
        """Clear all generated queries"""
        if messagebox.askyesno("CONFIRM", "Clear all generated intelligence queries?"):
            self.queries_text.delete(1.0, tk.END)
            self.generated_queries = {}
            self.browser_offset = 0  # Reset browser batch tracking
            self.status_var.set(f"⚡ SYSTEM READY | {get_dork_count()} TACTICAL QUERIES LOADED | AWAITING TARGET")

    def select_all_categories(self):
        """Select all intelligence categories"""
        for var in self.category_vars.values():
            var.set(True)

    def clear_all_categories(self):
        """Clear all category selections"""
        for var in self.category_vars.values():
            var.set(False)
            
    def load_window_settings(self):
        """Load window settings from config file"""
        default_settings = {
            'width': 1200,
            'height': 900,
            'remember_size': True,
            'start_maximized': False
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to handle missing keys
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception:
            pass  # Silently fall back to defaults on any error
            
        return default_settings
    
    def save_window_settings(self):
        """Save current window settings to config file"""
        try:
            settings = {
                'width': self.root.winfo_width(),
                'height': self.root.winfo_height(),
                'remember_size': self.window_settings.get('remember_size', True),
                'start_maximized': self.window_settings.get('start_maximized', False)
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception:
            pass  # Silently fail - don't interrupt user experience
    
    def on_window_close(self):
        """Handle window closing event"""
        # Save window settings before closing
        if self.window_settings.get('remember_size', True):
            self.save_window_settings()
        
        # Close the application
        self.root.destroy()

def main():
    """Launch RECON-OPS application"""
    root = tk.Tk()
    app = ReconOpsApp(root)
    
    # Set window icon if available
    try:
        # You can add a custom icon here
        pass
    except:
        pass
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
