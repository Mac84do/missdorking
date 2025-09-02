#!/usr/bin/env python3
"""
Simple test script to verify core functionality of the Google Dorking Tool
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    try:
        from google_dorks import get_all_dorks_for_domain, get_dork_count, GOOGLE_DORKS
        from scraper import GoogleScraper
        from export import ResultExporter
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_dork_queries():
    """Test dork query generation"""
    try:
        from google_dorks import get_all_dorks_for_domain, get_dork_count
        
        total_dorks = get_dork_count()
        print(f"✓ Loaded {total_dorks} dork queries")
        
        # Test with a sample domain
        test_domain = "example.com"
        dorks = get_all_dorks_for_domain(test_domain)
        
        if len(dorks) > 0:
            print(f"✓ Generated dork queries for {test_domain}")
            print(f"  - Categories: {list(dorks.keys())}")
            
            # Show a few examples
            for category, queries in list(dorks.items())[:2]:
                print(f"  - {category}: {len(queries)} queries")
                for query in queries[:2]:
                    print(f"    * {query}")
            
            return True
        else:
            print("✗ No dork queries generated")
            return False
            
    except Exception as e:
        print(f"✗ Error testing dork queries: {e}")
        return False

def test_scraper_init():
    """Test scraper initialization"""
    try:
        from scraper import GoogleScraper
        
        scraper = GoogleScraper()
        if hasattr(scraper, 'session') and hasattr(scraper, 'delay_range'):
            print("✓ Google scraper initialized successfully")
            print(f"  - Delay range: {scraper.delay_range}")
            return True
        else:
            print("✗ Scraper missing required attributes")
            return False
            
    except Exception as e:
        print(f"✗ Error initializing scraper: {e}")
        return False

def test_export_init():
    """Test export functionality initialization"""
    try:
        from export import ResultExporter
        
        exporter = ResultExporter()
        if hasattr(exporter, 'export_to_pdf') and hasattr(exporter, 'export_to_csv'):
            print("✓ Result exporter initialized successfully")
            return True
        else:
            print("✗ Exporter missing required methods")
            return False
            
    except Exception as e:
        print(f"✗ Error initializing exporter: {e}")
        return False

def test_file_structure():
    """Test that all required files are present"""
    required_files = [
        'main_gui.py',
        'google_dorks.py',
        'scraper.py',
        'export.py',
        'requirements.txt',
        'README.md',
        'install_windows.bat',
        'install_debian.sh',
        'run_dorking_tool.bat'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not missing_files:
        print(f"✓ All {len(required_files)} required files are present")
        return True
    else:
        print(f"✗ Missing files: {missing_files}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Google Dorking Tool - Functionality Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Dork Query Generation", test_dork_queries),
        ("Scraper Initialization", test_scraper_init),
        ("Export Initialization", test_export_init),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
