"""
🚀 MissDorking™ Ultimate Launcher 🚀
Quick launch script for the ultimate experience!
"""

import sys
import os

def main():
    """Launch MissDorking Ultimate with style!"""
    
    print("🚀" + "="*60 + "🚀")
    print("    MISSDORKING™ ULTIMATE - LAUNCHING!")
    print("    The Future of Cybersecurity Intelligence")
    print("    Now with Dad Jokes & Professional Branding!")
    print("🚀" + "="*60 + "🚀")
    print()
    
    try:
        # Import and launch the ultimate app
        from missdorking_ultimate import main as launch_ultimate
        print("✅ All systems loaded... Initiating ultimate experience...")
        print("💋 Get ready for some digital domination with style!")
        print()
        
        launch_ultimate()
        
    except ImportError as e:
        print("❌ Failed to import MissDorking Ultimate modules.")
        print("Make sure all required files are in the same directory:")
        print("  • missdorking_ultimate.py")
        print("  • dad_jokes.py")
        print("  • branding_manager.py")
        print("  • export.py (enhanced)")
        print("  • All other MissDorking modules")
        print(f"\nError: {e}")
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Check the log files for more details.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
