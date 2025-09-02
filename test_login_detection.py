"""
Test Login Detection Logic Directly
"""

from analysis import ResultAnalyzer

def test_login_detection():
    """Test login detection on known examples"""
    
    analyzer = ResultAnalyzer()
    
    # Test cases - simulate what Google would return
    test_cases = [
        {
            'title': 'Log in - Daytona',
            'url': 'https://daytona.co.za/account/login',
            'snippet': 'Login to your Daytona account to manage your orders and preferences.',
            'query': 'site:daytona.co.za login'
        },
        {
            'title': 'Daytona - Account Login',
            'url': 'https://daytona.co.za/account',
            'snippet': 'Sign in to your account. Username or email. Password.',
            'query': 'site:daytona.co.za inurl:login'
        },
        {
            'title': 'Daytona | Experts on all luxury vehicles',
            'url': 'https://daytona.co.za/',
            'snippet': 'Log in Search Cart Search Close Collections Aston Martin Lotus McLaren Pagani',
            'query': 'site:daytona.co.za'
        },
        {
            'title': 'Admin Panel - Daytona',
            'url': 'https://daytona.co.za/admin',
            'snippet': 'Administrator login portal for Daytona staff members.',
            'query': 'site:daytona.co.za admin'
        },
        {
            'title': 'Customer Portal - Daytona',
            'url': 'https://daytona.co.za/customer/signin',
            'snippet': 'Customer sign in page for accessing your account dashboard.',
            'query': 'site:daytona.co.za signin'
        }
    ]
    
    print("Testing Login Detection Logic")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing case:")
        print(f"   Title: {test_case['title']}")
        print(f"   URL: {test_case['url']}")
        print(f"   Snippet: {test_case['snippet'][:60]}...")
        
        # Analyze the result
        analyzed = analyzer.analyze_result(test_case.copy())
        analysis = analyzed['analysis']
        
        print(f"   Analysis Results:")
        print(f"   - Categories: {analysis['categories']}")
        print(f"   - Risk Level: {analysis['risk_level']}")
        print(f"   - Confidence Score: {analysis['confidence_score']}")
        
        if 'login_page' in analysis['categories']:
            print(f"   ✅ DETECTED as login page!")
        else:
            print(f"   ❌ NOT detected as login page")
        
        # Show detailed analysis
        print(f"   - All detected categories: {analysis['categories']}")
        print("-" * 30)

def test_individual_patterns():
    """Test individual pattern matching"""
    
    analyzer = ResultAnalyzer()
    
    # Test URL patterns
    test_urls = [
        'https://daytona.co.za/login',
        'https://daytona.co.za/account/login',
        'https://daytona.co.za/signin',
        'https://daytona.co.za/admin',
        'https://daytona.co.za/dashboard',
        'https://daytona.co.za/auth',
        'https://daytona.co.za/'
    ]
    
    print("\n" + "=" * 50)
    print("Testing Individual URL Patterns")
    print("=" * 50)
    
    for url in test_urls:
        score = analyzer._analyze_login_indicators(
            title="test title",
            url=url.lower(),
            snippet="test snippet"
        )
        
        print(f"URL: {url}")
        print(f"Login Score: {score}")
        print(f"Would be detected: {'YES' if score > 0 else 'NO'}")
        print("-" * 20)
    
    # Test title patterns
    test_titles = [
        'Log in - Daytona',
        'Login Page',
        'Sign In',
        'Admin Panel',
        'Dashboard',
        'User Authentication',
        'Home Page'
    ]
    
    print("\nTesting Title Patterns")
    print("=" * 30)
    
    for title in test_titles:
        score = analyzer._analyze_login_indicators(
            title=title.lower(),
            url="https://example.com",
            snippet="test snippet"
        )
        
        print(f"Title: {title}")
        print(f"Login Score: {score}")
        print(f"Would be detected: {'YES' if score > 0 else 'NO'}")
        print("-" * 20)

if __name__ == "__main__":
    test_login_detection()
    test_individual_patterns()
