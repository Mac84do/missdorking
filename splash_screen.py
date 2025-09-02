"""
Splash Screen for MissDorking
A fun splash screen with ASCII art to make users smile!
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class SplashScreen:
    def __init__(self, callback=None):
        """
        Initialize splash screen
        
        Args:
            callback: Function to call when splash screen closes
        """
        self.callback = callback
        self.root = tk.Tk()
        self.setup_window()
        self.create_content()
        
    def setup_window(self):
        """Setup the splash window properties"""
        # Window configuration
        self.root.title("MissDorking")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Remove window decorations for splash effect
        self.root.overrideredirect(True)
        
        # Set background color
        self.root.configure(bg='#1a1a2e')
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
    def create_content(self):
        """Create the splash screen content"""
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # ASCII Art - Playful hacker girl
        ascii_art = """
    ╔════════════════════════════════════════╗
    ║             MissDorking™               ║
    ╚════════════════════════════════════════╝
    
         👩‍💻 The Sexy Side of Cybersecurity 👩‍💻
    
                    ( ͡° ͜ʖ ͡°)
                   /|     |\\
                  / |  💻  | \\
                    |_____|
                   /       \\
                  /  👠   👠  \\
                 /_____________\\
    
    ┌─────────────────────────────────────────┐
    │  "I dork... therefore I pwn!" 💋       │
    │                                         │
    │  🔍 109 Google Dork Queries             │
    │  📊 Professional PDF Reports            │
    │  🌐 Cross-Platform Compatible           │
    │  🛡️  Ethical Hacking Tools              │
    │  💕 Made with Love & Code               │
    └─────────────────────────────────────────┘
        """
        
        # ASCII art label with custom font
        art_label = tk.Label(
            main_frame,
            text=ascii_art,
            font=('Courier New', 10, 'bold'),
            fg='#ff6b9d',
            bg='#1a1a2e',
            justify='center'
        )
        art_label.pack(pady=10)
        
        # Animated loading message
        self.loading_text = tk.StringVar()
        self.loading_text.set("Warming up the dorks... 💄")
        
        loading_label = tk.Label(
            main_frame,
            textvariable=self.loading_text,
            font=('Arial', 12, 'bold'),
            fg='#4ecdc4',
            bg='#1a1a2e'
        )
        loading_label.pack(pady=10)
        
        # Progress bar with custom style
        style = ttk.Style()
        style.configure(
            "Splash.Horizontal.TProgressbar",
            background='#ff6b9d',
            troughcolor='#16213e',
            borderwidth=0,
            lightcolor='#ff6b9d',
            darkcolor='#ff6b9d'
        )
        
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            style="Splash.Horizontal.TProgressbar",
            length=300
        )
        self.progress.pack(pady=10)
        
        # Fun disclaimer
        disclaimer = tk.Label(
            main_frame,
            text="⚠️ For Authorized Penetration Testing Only! ⚠️\n(But let's make it fun! 😉)",
            font=('Arial', 9, 'italic'),
            fg='#feca57',
            bg='#1a1a2e',
            justify='center'
        )
        disclaimer.pack(pady=(20, 10))
        
        # Copyright
        copyright_label = tk.Label(
            main_frame,
            text="© 2024 MissDorking™ - Ethical Hacking with Style 💅",
            font=('Arial', 8),
            fg='#a4b3b6',
            bg='#1a1a2e'
        )
        copyright_label.pack(side='bottom')
        
        # Skip button (small, in corner)
        skip_button = tk.Button(
            self.root,
            text="Skip 😴",
            command=self.close_splash,
            font=('Arial', 8),
            bg='#16213e',
            fg='#a4b3b6',
            bd=0,
            padx=5,
            pady=2
        )
        skip_button.place(x=520, y=10)
        
    def show(self):
        """Show the splash screen with animation"""
        # Start progress bar animation
        self.progress.start(10)
        
        # Start loading animation in separate thread
        self.animation_thread = threading.Thread(target=self.animate_loading)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
        # Auto-close after 4 seconds
        self.root.after(4000, self.close_splash)
        
        # Show the splash screen
        self.root.mainloop()
        
    def animate_loading(self):
        """Animate the loading messages"""
        messages = [
            "Warming up the dorks... 💄",
            "Applying digital lipstick... 💋",
            "Putting on hacking heels... 👠",
            "Loading sexy queries... 🔥",
            "Ready to pwn with style! ✨"
        ]
        
        for i, message in enumerate(messages):
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.loading_text.set(message)
                time.sleep(0.8)
            else:
                break
                
    def close_splash(self):
        """Close splash screen and call callback"""
        try:
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.destroy()
            
            if self.callback:
                self.callback()
        except:
            pass

def show_splash_screen(callback=None):
    """
    Show splash screen
    
    Args:
        callback: Function to call when splash closes
    """
    splash = SplashScreen(callback)
    splash.show()

if __name__ == "__main__":
    # Test the splash screen
    def test_callback():
        print("Splash screen closed!")
        
    show_splash_screen(test_callback)
