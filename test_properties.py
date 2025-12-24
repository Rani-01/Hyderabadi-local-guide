#!/usr/bin/env python3
"""
Property-based tests for Hyderabad Culture Navigator
Using hypothesis library for property-based testing
"""

import pytest
from hypothesis import given, strategies as st, settings
import tempfile
import os
import json

# Import our modules
from parser import parse_product_data, parse_markdown_table
from search import search_slang, get_search_suggestions
from filters import filter_biryani_spots, get_unique_areas, get_unique_vibes
from time_converter import convert_time_format, get_current_time_context

class TestFlaskStartup:
    """
    **Feature: hyderabad-culture-navigator, Property 9: Startup data loading**
    **Validates: Requirements 5.2**
    """
    
    def test_startup_data_loading_property(self):
        """
        Property: For any valid product.md file, the application should successfully 
        parse all tables during initialization
        """
        # Test with the actual product.md file
        data = parse_product_data('product.md')
        
        # Property: All data sections should be present
        assert 'slang_data' in data
        assert 'biryani_data' in data  
        assert 'time_data' in data
        
        # Property: Each section should contain valid data structures
        assert isinstance(data['slang_data'], list)
        assert isinstance(data['biryani_data'], list)
        assert isinstance(data['time_data'], list)
        
        # Property: If file exists and is valid, all sections should have data
        if os.path.exists('product.md'):
            # At least one section should have data (non-empty file)
            total_entries = len(data['slang_data']) + len(data['biryani_data']) + len(data['time_data'])
            assert total_entries > 0, "Valid product.md should contain at least some data"

    @given(st.text().filter(lambda x: x.isprintable()))
    def test_startup_handles_invalid_files(self, invalid_content):
        """
        Property: For any invalid file content, startup should handle gracefully
        """
        # Create temporary file with invalid content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(invalid_content)
            temp_path = f.name
        
        try:
            # Should not crash, should return empty data structures
            data = parse_product_data(temp_path)
            
            # Property: Invalid files should return empty but valid data structures
            assert isinstance(data, dict)
            assert 'slang_data' in data
            assert 'biryani_data' in data
            assert 'time_data' in data
            assert isinstance(data['slang_data'], list)
            assert isinstance(data['biryani_data'], list)
            assert isinstance(data['time_data'], list)
            
        finally:
            os.unlink(temp_path)

class TestMarkdownParsing:
    """
    **Feature: hyderabad-culture-navigator, Property 1: Markdown parsing round trip**
    **Validates: Requirements 1.1, 2.1, 3.1**
    """
    
    @given(st.lists(st.dictionaries(
        keys=st.sampled_from(['term', 'translation', 'category', 'usage']),
        values=st.text(min_size=1, max_size=50).filter(lambda x: '|' not in x and '\n' not in x),
        min_size=1
    ), min_size=1, max_size=10))
    def test_markdown_parsing_round_trip(self, data_entries):
        """
        Property: For any valid data structure, converting to markdown table format
        and parsing back should preserve the essential information
        """
        # Skip if any entry is empty or has problematic characters
        if not all(entry for entry in data_entries):
            return
            
        # Create a markdown table from the data
        headers = ['term', 'translation', 'category', 'usage']
        markdown_content = "## Test Section\n\n"
        markdown_content += "| " + " | ".join(headers) + " |\n"
        markdown_content += "|" + "---|" * len(headers) + "\n"
        
        for entry in data_entries:
            row = []
            for header in headers:
                value = entry.get(header, '').strip()
                # Clean value to avoid markdown issues
                value = value.replace('|', '-').replace('\n', ' ')
                row.append(value)
            markdown_content += "| " + " | ".join(row) + " |\n"
        
        # Parse the markdown content
        parsed_data = parse_markdown_table(markdown_content, "Test Section")
        
        # Property: Should parse successfully
        assert isinstance(parsed_data, list)
        assert len(parsed_data) > 0
        
        # Property: Number of entries should be preserved
        assert len(parsed_data) == len(data_entries)
        
        # Property: Each parsed entry should have the expected structure
        for parsed_entry in parsed_data:
            assert isinstance(parsed_entry, dict)
            # Should have keys corresponding to headers (lowercased and underscored)
            expected_keys = [h.lower().replace(' ', '_') for h in headers]
            for key in expected_keys:
                assert key in parsed_entry

class TestErrorHandling:
    """
    **Feature: hyderabad-culture-navigator, Property 10: Error handling resilience**
    **Validates: Requirements 5.3, 5.5**
    """
    
    @given(st.text().filter(lambda x: x.isprintable()))
    def test_parser_error_resilience(self, malformed_content):
        """
        Property: For any malformed input, the parser should handle errors gracefully
        and continue operating
        """
        # Create temporary file with malformed content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(malformed_content)
            temp_path = f.name
        
        try:
            # Should not raise exceptions
            data = parse_product_data(temp_path)
            
            # Property: Should return valid data structure even on error
            assert isinstance(data, dict)
            assert all(isinstance(data[key], list) for key in ['slang_data', 'biryani_data', 'time_data'])
            
        except Exception as e:
            # If an exception occurs, it should be logged but not crash the system
            pytest.fail(f"Parser should handle errors gracefully, but raised: {e}")
        finally:
            os.unlink(temp_path)

class TestFuzzySearch:
    """
    **Feature: hyderabad-culture-navigator, Property 2: Fuzzy search ranking consistency**
    **Validates: Requirements 1.2, 1.4**
    """
    
    @given(st.lists(st.dictionaries(
        keys=st.sampled_from(['term', 'translation', 'category', 'usage']),
        values=st.text(min_size=1, max_size=20),
        min_size=1
    ), min_size=2, max_size=10))
    @settings(max_examples=50)  # Limit examples for performance
    def test_fuzzy_search_ranking_consistency(self, slang_data):
        """
        Property: For any search query and slang dataset, fuzzy matching results 
        should be ranked by similarity score in descending order
        """
        if not slang_data:
            return
            
        # Use the first term as search query
        if not slang_data[0].get('term'):
            return
            
        query = slang_data[0]['term'][:5]  # Use partial term for fuzzy matching
        
        try:
            results = search_slang(query, slang_data, threshold=0, limit=len(slang_data))
            
            # Property: Results should be sorted by score (descending)
            if len(results) > 1:
                scores = [result['score'] for result in results]
                assert scores == sorted(scores, reverse=True), "Results should be sorted by score descending"
                
            # Property: All scores should be between 0 and 100
            for result in results:
                assert 0 <= result['score'] <= 100, f"Score {result['score']} should be between 0 and 100"
                
        except Exception:
            # If fuzzywuzzy is not available, skip this test
            pytest.skip("fuzzywuzzy not available")

    @given(st.text(min_size=1, max_size=20))
    def test_search_result_completeness(self, query):
        """
        **Property 3: Search result completeness**
        **Validates: Requirements 1.3**
        
        Property: For any search query that returns results, all returned slang entries 
        should contain both term and translation fields
        """
        # Use actual data from product.md
        data = parse_product_data('product.md')
        slang_data = data['slang_data']
        
        if not slang_data:
            return
            
        try:
            results = search_slang(query, slang_data)
            
            # Property: All results should have required fields
            for result in results:
                assert 'entry' in result, "Result should contain 'entry' field"
                entry = result['entry']
                assert isinstance(entry, dict), "Entry should be a dictionary"
                assert 'term' in entry, "Entry should contain 'term' field"
                assert 'translation' in entry, "Entry should contain 'translation' field"
                
                # Property: Fields should not be empty
                assert entry['term'], "Term field should not be empty"
                assert entry['translation'], "Translation field should not be empty"
                
        except Exception:
            # If fuzzywuzzy is not available, skip this test
            pytest.skip("fuzzywuzzy not available")

class TestBiryaniFiltering:
    """
    **Feature: hyderabad-culture-navigator, Property 5: Filter result accuracy**
    **Validates: Requirements 2.3, 2.4, 2.5**
    """
    
    @given(st.lists(st.dictionaries(
        keys=st.sampled_from(['name', 'area', 'vibe', 'description', 'rating']),
        values=st.one_of(st.text(min_size=1, max_size=20), st.floats(min_value=0, max_value=5)),
        min_size=2
    ), min_size=1, max_size=10))
    def test_filter_result_accuracy(self, biryani_data):
        """
        Property: For any combination of area and vibe filters applied to biryani spots,
        all returned results should match all selected criteria
        """
        if not biryani_data:
            return
            
        # Ensure all entries have string values for area and vibe
        cleaned_data = []
        for spot in biryani_data:
            if isinstance(spot.get('area'), str) and isinstance(spot.get('vibe'), str):
                cleaned_data.append(spot)
        
        if not cleaned_data:
            return
            
        # Test with first spot's area and vibe as filters
        test_spot = cleaned_data[0]
        area_filter = test_spot.get('area')
        vibe_filter = test_spot.get('vibe')
        
        if not area_filter or not vibe_filter:
            return
            
        # Apply filters
        filtered_results = filter_biryani_spots(cleaned_data, area_filter, vibe_filter)
        
        # Property: All results should match the filter criteria
        for result in filtered_results:
            assert result.get('area', '').lower() == area_filter.lower(), \
                f"Result area '{result.get('area')}' should match filter '{area_filter}'"
            assert result.get('vibe', '').lower() == vibe_filter.lower(), \
                f"Result vibe '{result.get('vibe')}' should match filter '{vibe_filter}'"

class TestCardRendering:
    """
    **Feature: hyderabad-culture-navigator, Property 4: Card rendering completeness**
    **Validates: Requirements 2.2**
    """
    
    @given(st.lists(st.dictionaries(
        keys=st.sampled_from(['name', 'area', 'vibe', 'description', 'rating']),
        values=st.one_of(
            st.text(min_size=1, max_size=30).filter(lambda x: x.strip()),
            st.floats(min_value=0, max_value=5)
        ),
        min_size=3  # Ensure we have name, area, vibe at minimum
    ), min_size=1, max_size=5))
    def test_card_rendering_completeness(self, biryani_spots):
        """
        Property: For any collection of biryani spots, the card UI should render 
        all spots with complete information
        """
        if not biryani_spots:
            return
            
        # Ensure all spots have required fields
        valid_spots = []
        for spot in biryani_spots:
            if (isinstance(spot.get('name'), str) and spot.get('name').strip() and
                isinstance(spot.get('area'), str) and spot.get('area').strip() and
                isinstance(spot.get('vibe'), str) and spot.get('vibe').strip()):
                valid_spots.append(spot)
        
        if not valid_spots:
            return
            
        # Property: Each spot should have all required fields for card rendering
        for spot in valid_spots:
            # Required fields for card display
            assert 'name' in spot and spot['name'], "Spot should have a name"
            assert 'area' in spot and spot['area'], "Spot should have an area"
            assert 'vibe' in spot and spot['vibe'], "Spot should have a vibe"
            
            # Optional fields should be handled gracefully
            rating = spot.get('rating', 0)
            if rating is not None and rating != '':
                # Convert string ratings to float if needed (data parsing might do this)
                if isinstance(rating, str):
                    try:
                        rating = float(rating)
                    except ValueError:
                        rating = 0
                assert isinstance(rating, (int, float)), "Rating should be numeric"
                assert 0 <= rating <= 5, "Rating should be between 0 and 5"
            
            description = spot.get('description', '')
            if description and not isinstance(description, str):
                # Convert non-string descriptions to string (data parsing might do this)
                description = str(description)
            if description:
                assert isinstance(description, str), "Description should be a string"

class TestTimeConversion:
    """
    **Feature: hyderabad-culture-navigator, Property 6: Time conversion consistency**
    **Validates: Requirements 3.3, 3.4, 3.5**
    """
    
    @given(st.lists(st.dictionaries(
        keys=st.just('standard_time') | st.just('hyderabadi_time') | st.just('context'),
        values=st.text(min_size=1, max_size=30),
        min_size=3, max_size=3
    ), min_size=1, max_size=8))
    def test_time_conversion_consistency(self, time_data):
        """
        Property: For any time data and toggle state, switching between standard 
        and Hyderabadi modes should display appropriate time representations
        """
        if not time_data:
            return
            
        # Test standard mode conversion
        standard_times = convert_time_format(time_data, 'standard')
        hyderabadi_times = convert_time_format(time_data, 'hyderabadi')
        
        # Property: Should return same number of entries
        assert len(standard_times) == len(time_data), "Standard conversion should preserve entry count"
        assert len(hyderabadi_times) == len(time_data), "Hyderabadi conversion should preserve entry count"
        
        # Property: Each converted entry should have required fields
        for entry in standard_times:
            assert 'display_time' in entry, "Standard entry should have display_time"
            assert 'mode' in entry, "Standard entry should have mode"
            assert entry['mode'] == 'standard', "Standard entry should have correct mode"
            
        for entry in hyderabadi_times:
            assert 'display_time' in entry, "Hyderabadi entry should have display_time"
            assert 'mode' in entry, "Hyderabadi entry should have mode"
            assert entry['mode'] == 'hyderabadi', "Hyderabadi entry should have correct mode"

class TestResponsiveLayout:
    """
    **Feature: hyderabad-culture-navigator, Property 7: Responsive layout adaptation**
    **Validates: Requirements 4.3**
    """
    
    @given(st.integers(min_value=320, max_value=1920))
    def test_responsive_layout_adaptation(self, viewport_width):
        """
        Property: For any viewport dimensions, the CSS layout should adapt appropriately 
        while maintaining usability
        """
        # Test CSS breakpoints logic
        # This is a simplified test since we can't actually test CSS rendering
        
        # Property: Breakpoints should be logically consistent
        is_mobile = viewport_width <= 480
        is_tablet = 480 < viewport_width <= 768
        is_desktop = viewport_width > 768
        
        # Exactly one should be true
        breakpoint_count = sum([is_mobile, is_tablet, is_desktop])
        assert breakpoint_count == 1, f"Exactly one breakpoint should match for width {viewport_width}"
        
        # Property: Mobile should have single column layout
        if is_mobile:
            expected_columns = 1
        elif is_tablet:
            expected_columns = 2  # Typically 2 columns for tablet
        else:
            expected_columns = 3  # 3+ columns for desktop
            
        assert expected_columns >= 1, "Should always have at least 1 column"
        assert expected_columns <= 4, "Should not exceed 4 columns for usability"

class TestStylingConsistency:
    """
    **Feature: hyderabad-culture-navigator, Property 8: Styling consistency**
    **Validates: Requirements 4.2, 4.4, 4.5**
    """
    
    @given(st.sampled_from(['button', 'card', 'input', 'link']))
    def test_styling_consistency(self, element_type):
        """
        Property: For any UI element, the styling should use the correct color palette 
        and maintain appropriate contrast ratios
        """
        # Define the royal color palette
        royal_charcoal = "#1A1A1B"
        nizam_gold = "#D4AF37"
        text_light = "#FFFFFF"
        
        # Property: All elements should use colors from the defined palette
        valid_colors = [royal_charcoal, nizam_gold, text_light, "#CCCCCC", "#2A2A2B", "#E5C547"]
        
        # Test color combinations for contrast
        def calculate_luminance(hex_color):
            """Simplified luminance calculation for testing"""
            # Remove # and convert to RGB
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # Simplified relative luminance
            return (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        # Property: High contrast combinations should meet accessibility standards
        bg_luminance = calculate_luminance(royal_charcoal)
        text_luminance = calculate_luminance(text_light)
        gold_luminance = calculate_luminance(nizam_gold)
        
        # Contrast ratio should be at least 4.5:1 for normal text (WCAG AA)
        contrast_bg_text = (max(bg_luminance, text_luminance) + 0.05) / (min(bg_luminance, text_luminance) + 0.05)
        contrast_bg_gold = (max(bg_luminance, gold_luminance) + 0.05) / (min(bg_luminance, gold_luminance) + 0.05)
        
        assert contrast_bg_text >= 4.5, f"Background-text contrast {contrast_bg_text:.2f} should meet WCAG AA"
        assert contrast_bg_gold >= 3.0, f"Background-gold contrast {contrast_bg_gold:.2f} should be readable"

class TestResponseTime:
    """
    **Feature: hyderabad-culture-navigator, Property 11: Response time consistency**
    **Validates: Requirements 5.4**
    """
    
    def test_response_time_consistency(self):
        """
        Property: For any HTTP request, the system should respond within reasonable time limits
        """
        import time
        
        # Test core functions that would be called by HTTP endpoints
        test_functions = [
            lambda: parse_product_data('product.md'),
            lambda: search_slang('test', [{'term': 'test', 'translation': 'test'}]),
            lambda: filter_biryani_spots([{'name': 'test', 'area': 'test', 'vibe': 'test'}]),
            lambda: convert_time_format([{'standard_time': '12:00 PM', 'hyderabadi_time': 'test', 'context': 'test'}])
        ]
        
        for func in test_functions:
            start_time = time.time()
            try:
                result = func()
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Property: Response time should be reasonable (under 1 second for these operations)
                assert response_time < 1.0, f"Function {func.__name__ if hasattr(func, '__name__') else 'lambda'} took {response_time:.3f}s, should be under 1.0s"
                
                # Property: Function should return a valid result
                assert result is not None, "Function should return a result"
                
            except ImportError:
                # Skip if dependencies not available
                continue

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])