"""
Fun Splash Screen for MissDorking - Making People Smile! 😂
Adds some humor and visual entertainment while the app loads
"""

import tkinter as tk
from tkinter import ttk
import time
import random
import threading
from datetime import datetime

class FunSplashScreen:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.title("MissDorking™ - Loading with Style! 💋")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Remove window decorations for a sleek look
        self.root.overrideredirect(True)
        
        # Set background gradient effect
        self.root.configure(bg='#FF1493')  # Hot pink background
        
        self.setup_splash_content()
        self.start_animations()
        
        # Auto-close after 3 seconds
        self.root.after(3000, self.close_splash)
    
    def setup_splash_content(self):
        """Setup the fun splash screen content"""
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#FF1493', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fun title with multiple lines
        title_frame = tk.Frame(main_frame, bg='#FF1493')
        title_frame.pack(expand=True)
        
        # Big title
        self.title_label = tk.Label(
            title_frame,
            text="💋 MISSDORKING™ 💋",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#FF1493'
        )
        self.title_label.pack(pady=(20, 10))
        
        # Subtitle with humor
        self.subtitle_label = tk.Label(
            title_frame,
            text="LUDICROUS SPEED Edition! 🚀",
            font=('Arial', 16, 'bold'),
            fg='yellow',
            bg='#FF1493'
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Rotating fun messages
        self.fun_messages = [
            "💄 Loading with maximum sass...",
            "🔥 Warming up the dorking engines...",
            "👠 Putting on digital stilettos...",
            "💎 Applying hacker lipgloss...",
            "🌟 Charging up the sass batteries...",
            "🦄 Summoning unicorn powers...",
            "🍑 Getting ready to work it...",
            "💅 Filing digital nails to perfection...",
            "🌈 Adding rainbow sparkles to code...",
            "😘 Blowing kisses at the firewall..."
        ]
        
        self.status_label = tk.Label(
            title_frame,
            text=random.choice(self.fun_messages),
            font=('Arial', 12),
            fg='white',
            bg='#FF1493'
        )
        self.status_label.pack(pady=10)
        
        # Animated progress bar
        progress_frame = tk.Frame(main_frame, bg='#FF1493')
        progress_frame.pack(fill=tk.X, pady=20)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style='Pink.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, padx=40)
        
        # Fun facts about the app
        facts_frame = tk.Frame(main_frame, bg='#FF1493')
        facts_frame.pack(expand=True)
        
        fun_facts = [
            "💋 Fun Fact: This app has more sass than your ex!",
            "🔥 Did you know? We dork faster than gossip spreads!",
            "✨ Pro Tip: Always hack with style and attitude!",
            "👑 MissDorking Motto: 'If you're not fabulous, you're doing it wrong!'",
            "💅 Remember: Confidence is the best security tool!",
            "🌟 Today's Vibe: Hacking hearts and breaking systems!",
            "🦄 MissDorking Magic: Making boring tasks fabulous!",
            "💖 Disclaimer: May cause excessive confidence and success!"
        ]
        
        self.fact_label = tk.Label(
            facts_frame,
            text=random.choice(fun_facts),
            font=('Arial', 10, 'italic'),
            fg='lightpink',
            bg='#FF1493',
            wraplength=500
        )
        self.fact_label.pack(pady=20)
        
        # Version and credits
        version_label = tk.Label(
            main_frame,
            text="v2.0 LUDICROUS SPEED - Built with 💋 and maximum sass!",
            font=('Arial', 8),
            fg='lightgray',
            bg='#FF1493'
        )
        version_label.pack(side=tk.BOTTOM, pady=10)
        
        # Click to continue hint
        self.click_label = tk.Label(
            main_frame,
            text="💄 Click anywhere to skip this fabulous intro! 💄",
            font=('Arial', 9),
            fg='white',
            bg='#FF1493'
        )
        self.click_label.pack(side=tk.BOTTOM, pady=5)
        
        # Bind click to skip
        self.root.bind('<Button-1>', lambda e: self.close_splash())
        for widget in [main_frame, title_frame, facts_frame]:
            widget.bind('<Button-1>', lambda e: self.close_splash())
    
    def start_animations(self):
        """Start fun animations"""
        # Start progress bar
        self.progress_bar.start(20)
        
        # Start message rotation
        self.rotate_messages()
        
        # Start title color animation
        self.animate_title()
    
    def rotate_messages(self):
        """Rotate through fun loading messages"""
        def update_message():
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                message = random.choice(self.fun_messages)
                self.status_label.config(text=message)
                self.root.after(800, update_message)
        
        self.root.after(800, update_message)
    
    def animate_title(self):
        """Animate the title colors"""
        colors = ['white', 'yellow', 'lightpink', 'lightgreen', 'lightblue', 'orange']
        
        def change_color():
            if hasattr(self, 'title_label') and self.title_label.winfo_exists():
                color = random.choice(colors)
                self.title_label.config(fg=color)
                self.root.after(300, change_color)
        
        self.root.after(300, change_color)
    
    def close_splash(self):
        """Close splash screen and start main app"""
        try:
            self.root.destroy()
            if self.callback:
                self.callback()
        except:
            pass

def show_fun_splash(callback):
    """Show the fun splash screen"""
    try:
        # Create a temporary root window
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide it
        
        # Show splash
        splash = FunSplashScreen(callback)
        
        # Start event loop for splash only
        splash.root.mainloop()
        
        # Clean up temp root
        temp_root.destroy()
        
    except Exception as e:
        print(f"Splash screen failed: {e}")
        # Fall back to direct callback
        if callback:
            callback()

if __name__ == "__main__":
    def test_callback():
        print("💋 Main app would start here!")
    
    show_fun_splash(test_callback)
