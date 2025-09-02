#!/usr/bin/env python3
"""
MissDorking™ LUDICROUS SPEED Edition Launcher! 🚀💋
The fastest, sassiest, most fabulous dorking tool ever created!

Performance Optimizations:
- Reduced delays from 2-4s to 0.1-0.3s (10-40x faster!)
- Increased workers from 3 to 8 (2.6x more parallel power!)
- Reduced timeouts for faster failures
- Parallel analysis processing
- Fun elements to make you smile while waiting!

Run this to launch the ultimate speed demon dorking experience!
"""

import sys
import os
import logging
import time
import threading

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging():
    """Setup logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('missdorking_ludicrous_speed.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        ('tkinter', 'tkinter', 'Built into Python'),
        ('requests', 'requests', 'pip install requests'),
        ('beautifulsoup4', 'bs4', 'pip install beautifulsoup4'),
        ('concurrent.futures', 'concurrent.futures', 'Built into Python 3.2+'),
        ('reportlab', 'reportlab', 'pip install reportlab (for PDF export)')
    ]
    
    missing_modules = []
    optional_missing = []
    
    for display_name, import_name, install_cmd in required_modules:
        try:
            __import__(import_name)
        except ImportError:
            if display_name == 'reportlab':
                optional_missing.append((display_name, install_cmd))
            else:
                missing_modules.append((display_name, install_cmd))
    
    if missing_modules:
        print("❌ Missing REQUIRED dependencies:")
        for module, install in missing_modules:
            print(f"   💄 {module}: {install}")
        print("\n💋 Install required dependencies with:")
        print("   pip install requests beautifulsoup4")
        return False
    
    if optional_missing:
        print("⚠️ Missing OPTIONAL dependencies:")
        for module, install in optional_missing:
            print(f"   💄 {module}: {install}")
        print("\n💡 The app will work without these, but some features may be limited.")
    
    if not missing_modules and not optional_missing:
        print("✅ All dependencies available! Full functionality ready!")
    
    return True

def print_welcome():
    """Print a fabulous welcome message"""
    welcome_art = """
💋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💋
                                                                        
    ███╗   ███╗██╗███████╗███████╗██████╗  ██████╗ ██████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗ ™
    ████╗ ████║██║██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║████╗  ██║██╔════╝
    ██╔████╔██║██║███████╗███████╗██║  ██║██║   ██║██████╔╝█████╔╝ ██║██╔██╗ ██║██║  ███╗
    ██║╚██╔╝██║██║╚════██║╚════██║██║  ██║██║   ██║██╔══██╗██╔═██╗ ██║██║╚██╗██║██║   ██║
    ██║ ╚═╝ ██║██║███████║███████║██████╔╝╚██████╔╝██║  ██║██║  ██╗██║██║ ╚████║╚██████╔╝
    ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                        
                        🚀 LUDICROUS SPEED EDITION! 🚀                        
                                                                        
💋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💋

🔥 Welcome to the fastest, sassiest dorking tool in the universe! 🔥

⚡ PERFORMANCE STATS:
   • Request Delays: 0.1-0.3 seconds (LUDICROUS SPEED!)
   • Parallel Workers: 8 threads (MAXIMUM POWER!)
   • Timeouts: 5-8 seconds (QUICK & EFFICIENT!)
   • Fun Level: OVER 9000! 💅

💄 FEATURES:
   • Speed Demon Mode - Single domain obliteration
   • Bulk Boss Mode - Multiple domain domination  
   • Fun Configuration - Tune the madness
   • Humor & Sass - Making boring tasks fabulous!

👑 Ready to hack with style, grace, and maximum attitude? Let's go!

"""
    print(welcome_art)

def run_performance_test():
    """Run a quick performance test to show off speed"""
    print("🚀 Running quick performance test...")
    
    try:
        from fast_bulk_scanner import FastBulkScanner
        
        # Test with super fast settings
        scanner = FastBulkScanner(max_workers=8, delay_range=(0.1, 0.3))
        
        test_domains = ["example.com"]  # Quick test domain
        start_time = time.time()
        
        print("   💫 Testing LUDICROUS SPEED settings...")
        
        # Run a quick test (this might fail but that's OK - we're testing speed)
        try:
            results = scanner.bulk_scan(test_domains)
            test_time = time.time() - start_time
            print(f"   ✅ Performance test completed in {test_time:.2f} seconds!")
        except Exception as e:
            test_time = time.time() - start_time
            print(f"   ⚡ Speed test ran in {test_time:.2f} seconds (connection issues are normal)")
        
        print(f"   🏎️  Speed Rating: {'LUDICROUS! 🔥' if test_time < 5 else 'VERY FAST! ⚡' if test_time < 10 else 'FAST! 💨'}")
        
    except Exception as e:
        print(f"   ⚠️  Performance test skipped: {e}")
    
    print()

def launch_app():
    """Launch the main application"""
    try:
        print("💋 Starting MissDorking LUDICROUS SPEED Edition...")
        
        # Import the fun splash screen
        try:
            from fun_splash import show_fun_splash
            splash_available = True
        except ImportError:
            print("💄 Splash screen not available, starting directly...")
            splash_available = False
        
        # Define main app launcher
        def start_main_app():
            try:
                from super_fast_gui import main as super_main
                print("🚀 Launching SPEED DEMON mode...")
                super_main()
            except ImportError:
                try:
                    # Fallback to optimized GUI
                    from main_gui_optimized import main as optimized_main
                    print("⚡ Launching optimized mode...")
                    optimized_main()
                except ImportError:
                    # Final fallback to regular GUI
                    from main_gui import main as regular_main
                    print("🐌 Launching regular mode (consider upgrading!)...")
                    regular_main()
        
        # Launch with or without splash
        if splash_available:
            show_fun_splash(start_main_app)
        else:
            start_main_app()
            
    except KeyboardInterrupt:
        print("\n💋 Thanks for using MissDorking! Stay fabulous! ✨")
    except Exception as e:
        print(f"💄 Oops! Something went wrong: {e}")
        logging.error(f"Application error: {e}")
        
        # Try fallback launch
        try:
            print("🔧 Attempting fallback launch...")
            from main_gui import main as fallback_main
            fallback_main()
        except:
            print("❌ All launch attempts failed. Check your installation!")

def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    
    # Print fabulous welcome
    print_welcome()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n💋 Please install missing dependencies and try again!")
        sys.exit(1)
    
    print("✅ All dependencies ready!")
    print()
    
    # Run performance test
    run_performance_test()
    
    # Launch the app
    print("🚀 Launching MissDorking LUDICROUS SPEED Edition!")
    print("💄 Get ready for the ride of your life!")
    print("=" * 70)
    
    launch_app()
    
    print("\n💋 Thanks for using MissDorking LUDICROUS SPEED Edition!")
    print("🌟 Remember: Always hack with style and maximum sass! 💅")

if __name__ == "__main__":
    main()
