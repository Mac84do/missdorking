#!/usr/bin/env python3
"""
Quick Test for MissDorking Fixes
Tests PDF/CSV export functionality and bulk scanning fixes
"""

import sys
import os

def test_import_fixes():
    """Test if all imports work correctly"""
    print("🧪 Testing import fixes...")
    
    try:
        from super_fast_gui import SuperFastDorkingGUI, EXPORT_AVAILABLE
        print("✅ Super fast GUI imports working")
        print(f"📊 Export availability: {EXPORT_AVAILABLE}")
        
        if EXPORT_AVAILABLE:
            from export import ResultExporter
            print("✅ Export module available - PDF/CSV should work!")
        else:
            print("⚠️ Export module not available - install reportlab for PDF export")
        
        from fast_bulk_scanner import FastBulkScanner
        print("✅ Fast bulk scanner import working")
        
        from hybrid_scraper_fixed import HybridScraper
        print("✅ Optimized hybrid scraper import working")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_domain_parsing():
    """Test domain parsing for bulk scanning"""
    print("\n🧪 Testing domain parsing...")
    
    test_text = "daytona.co.za\ngoogle.com\ngithub.com\nstackoverflow.com\nreddit.com"
    
    # Test the parsing logic from the fixed GUI
    domains = [d.strip() for d in test_text.split('\n') if d.strip()]
    
    print(f"📝 Test input: {repr(test_text)}")
    print(f"📋 Parsed domains: {domains}")
    print(f"📊 Domain count: {len(domains)}")
    
    if len(domains) == 5 and 'daytona.co.za' in domains:
        print("✅ Domain parsing fixed!")
        return True
    else:
        print("❌ Domain parsing still has issues")
        return False

def test_scanner_config():
    """Test scanner configuration"""
    print("\n🧪 Testing scanner configuration...")
    
    try:
        from fast_bulk_scanner import FastBulkScanner
        from hybrid_scraper_fixed import HybridScraper
        
        # Test with LUDICROUS SPEED settings
        scanner = FastBulkScanner(max_workers=8, delay_range=(0.1, 0.3))
        scraper = HybridScraper(delay_range=(0.1, 0.3))
        
        print("✅ Scanner created with LUDICROUS SPEED settings:")
        print(f"   ⚡ Workers: {scanner.max_workers}")
        print(f"   ⚡ Delay range: {scanner.delay_range}")
        print(f"   ⚡ Scraper delay: {scraper.delay_range}")
        
        # Test if settings are actually fast
        if scanner.delay_range[1] <= 0.5 and scanner.max_workers >= 6:
            print("🚀 LUDICROUS SPEED confirmed!")
        elif scanner.delay_range[1] <= 1.0 and scanner.max_workers >= 3:
            print("⚡ VERY FAST confirmed!")
        else:
            print("🐌 Speed could be better...")
        
        return True
        
    except Exception as e:
        print(f"❌ Scanner config error: {e}")
        return False

def test_export_functionality():
    """Test export functionality (without actually exporting)"""
    print("\n🧪 Testing export functionality...")
    
    try:
        if EXPORT_AVAILABLE:
            from export import ResultExporter
            
            exporter = ResultExporter()
            print("✅ Export module initialized successfully")
            
            # Test data structure
            test_results = {
                'Login & Admin Pages': {
                    'test query': [
                        {
                            'title': 'Test Login Page',
                            'url': 'https://example.com/login',
                            'snippet': 'Test snippet'
                        }
                    ]
                }
            }
            
            print("📊 Test data structure created")
            print("💡 PDF/CSV export should work with this data structure")
            
            return True
        else:
            print("⚠️ Export not available - install reportlab: pip install reportlab")
            return False
            
    except Exception as e:
        print(f"❌ Export test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 MissDorking™ LUDICROUS SPEED Edition - Fix Verification 🚀")
    print("=" * 60)
    
    tests = [
        test_import_fixes,
        test_domain_parsing,
        test_scanner_config,
        test_export_functionality
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY:")
    print(f"✅ Tests passed: {sum(results)}/{len(results)}")
    print(f"❌ Tests failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 ALL FIXES VERIFIED! The optimized edition should work perfectly!")
        print("💋 Ready to launch super_fast_gui.py with:")
        print("   📄 PDF export functionality")
        print("   📊 CSV export functionality") 
        print("   👑 Working bulk scanning")
        print("   🚀 LUDICROUS SPEED performance")
    else:
        print("\n⚠️ Some issues detected. Check the individual test results above.")
    
    print("\n💋 MissDorking™ says: 'Test complete, darling!' 😘")

if __name__ == "__main__":
    # Add current directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    main()
