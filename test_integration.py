#!/usr/bin/env python3
"""
Integration test script for Hyderabad Culture Navigator
Tests core functionality without requiring Flask to be installed
"""

import sys
import os

def test_parser():
    """Test the markdown parser functionality"""
    print("🧪 Testing markdown parser...")
    try:
        from parser import parse_product_data
        data = parse_product_data()
        
        assert len(data['slang_data']) > 0, "No slang data parsed"
        assert len(data['biryani_data']) > 0, "No biryani data parsed"
        assert len(data['time_data']) > 0, "No time data parsed"
        
        print(f"   ✅ Parsed {len(data['slang_data'])} slang terms")
        print(f"   ✅ Parsed {len(data['biryani_data'])} biryani spots")
        print(f"   ✅ Parsed {len(data['time_data'])} time mappings")
        return True
    except Exception as e:
        print(f"   ❌ Parser test failed: {str(e)}")
        return False

def test_search():
    """Test the slang search functionality"""
    print("🧪 Testing slang search...")
    try:
        from parser import parse_product_data
        from search import search_slang, get_search_suggestions
        
        data = parse_product_data()
        slang_data = data['slang_data']
        
        # Test search
        results = search_slang('baigan', slang_data)
        assert len(results) > 0, "No search results for 'baigan'"
        
        # Test suggestions
        suggestions = get_search_suggestions('bagan', slang_data)
        assert len(suggestions) > 0, "No suggestions for misspelled term"
        
        print(f"   ✅ Search for 'baigan' returned {len(results)} results")
        print(f"   ✅ Suggestions for 'bagan': {suggestions[:3]}")
        return True
    except Exception as e:
        print(f"   ❌ Search test failed: {str(e)}")
        return False

def test_filters():
    """Test the biryani filtering functionality"""
    print("🧪 Testing biryani filters...")
    try:
        from parser import parse_product_data
        from filters import filter_biryani_spots, get_unique_areas, get_unique_vibes
        
        data = parse_product_data()
        biryani_data = data['biryani_data']
        
        # Test filtering
        filtered = filter_biryani_spots(biryani_data, area_filter='Secunderabad')
        areas = get_unique_areas(biryani_data)
        vibes = get_unique_vibes(biryani_data)
        
        assert len(areas) > 0, "No unique areas found"
        assert len(vibes) > 0, "No unique vibes found"
        
        print(f"   ✅ Found {len(areas)} unique areas")
        print(f"   ✅ Found {len(vibes)} unique vibes")
        print(f"   ✅ Filtering by 'Secunderabad' returned {len(filtered)} spots")
        return True
    except Exception as e:
        print(f"   ❌ Filter test failed: {str(e)}")
        return False

def test_time_converter():
    """Test the time conversion functionality"""
    print("🧪 Testing time converter...")
    try:
        from parser import parse_product_data
        from time_converter import convert_time_format, get_current_time_context
        
        data = parse_product_data()
        time_data = data['time_data']
        
        # Test conversion
        standard_times = convert_time_format(time_data, 'standard')
        hyderabadi_times = convert_time_format(time_data, 'hyderabadi')
        current_context = get_current_time_context(time_data)
        
        assert len(standard_times) > 0, "No standard time conversions"
        assert len(hyderabadi_times) > 0, "No Hyderabadi time conversions"
        
        print(f"   ✅ Generated {len(standard_times)} standard time entries")
        print(f"   ✅ Generated {len(hyderabadi_times)} Hyderabadi time entries")
        if current_context:
            print(f"   ✅ Current time context: {current_context['standard_time']} = {current_context['hyderabadi_time']}")
        return True
    except Exception as e:
        print(f"   ❌ Time converter test failed: {str(e)}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("🧪 Testing file structure...")
    required_files = [
        'app.py',
        'parser.py',
        'search.py',
        'filters.py',
        'time_converter.py',
        'product.md',
        'requirements.txt',
        'static/style.css',
        'templates/base.html',
        'templates/index.html',
        'templates/slang.html',
        'templates/biryani.html',
        'templates/time.html',
        'templates/404.html',
        'templates/500.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    else:
        print(f"   ✅ All {len(required_files)} required files present")
        return True

def main():
    """Run all integration tests"""
    print("🏛️ Hyderabad Culture Navigator - Integration Tests")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_parser,
        test_search,
        test_filters,
        test_time_converter
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the application:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run the app: python app.py")
        print("   3. Open browser to: http://localhost:8000")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)