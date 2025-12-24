# Design Document

## Overview

The Hyderabad Culture & Slang Navigator is a Flask web application that provides an interactive cultural guide for Hyderabad. The system parses structured markdown data on startup and serves three main features: slang translation with fuzzy search, biryani spot recommendations with filtering, and time conversion between standard and cultural interpretations. The application emphasizes a royal aesthetic using Hyderabad's cultural colors and responsive design principles.

## Architecture

The application follows a traditional Flask MVC pattern with the following layers:

- **Presentation Layer**: HTML templates with responsive CSS using Royal Charcoal and Nizam Gold palette
- **Application Layer**: Flask routes handling HTTP requests and coordinating business logic
- **Business Logic Layer**: Core functionality for search, filtering, and data transformation
- **Data Layer**: In-memory Python data structures populated from markdown parsing

The system uses server-side rendering with minimal JavaScript for interactive elements like toggles and filters.

## Components and Interfaces

### Data Parser Component
- **Purpose**: Parse product.md markdown tables into Python data structures
- **Interface**: `parse_product_data() -> Dict[str, List[Dict]]`
- **Dependencies**: Python `re` module for markdown table parsing
- **Error Handling**: Graceful degradation when tables are malformed

### Slang Search Component
- **Purpose**: Provide fuzzy matching search for local slang terms
- **Interface**: `search_slang(query: str, threshold: float) -> List[Dict]`
- **Dependencies**: `fuzzywuzzy` library for fuzzy string matching
- **Features**: Configurable similarity threshold, ranked results

### Biryani Filter Component
- **Purpose**: Filter biryani spots by area and vibe criteria
- **Interface**: `filter_biryani_spots(area: str, vibe: str) -> List[Dict]`
- **Features**: Multiple filter support, case-insensitive matching

### Time Converter Component
- **Purpose**: Convert between standard time and Hyderabadi cultural time
- **Interface**: `convert_time(time_str: str, mode: str) -> str`
- **Features**: Bidirectional conversion, cultural time interpretations

### UI Renderer Component
- **Purpose**: Generate consistent HTML components with royal styling
- **Interface**: Template functions for cards, toggles, and search interfaces
- **Features**: Responsive design, accessibility compliance

## Data Models

### Slang Entry
```python
{
    "term": str,           # Local slang term
    "translation": str,    # English translation/explanation
    "category": str,       # Optional categorization
    "usage": str          # Optional usage example
}
```

### Biryani Spot
```python
{
    "name": str,          # Restaurant/spot name
    "area": str,          # Geographic area in Hyderabad
    "vibe": str,          # Atmosphere category
    "description": str,   # Optional description
    "rating": float       # Optional rating
}
```

### Time Mapping
```python
{
    "standard_time": str,     # Standard time representation
    "hyderabadi_time": str,   # Cultural time interpretation
    "context": str            # Optional cultural context
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*
### Property Reflection

After reviewing all identified properties, I found several areas for consolidation:

- Properties 1.1, 2.1, and 3.1 all test markdown parsing functionality and can be combined into one comprehensive parsing property
- Properties 2.3, 2.4, and 2.5 all test filtering functionality and can be combined into one comprehensive filtering property
- Properties 3.3, 3.4, and 3.5 all test time display functionality and can be combined into one comprehensive time conversion property
- Properties 4.2, 4.4, and 4.5 all test styling consistency and can be combined into one comprehensive styling property

**Property 1: Markdown parsing round trip**
*For any* valid markdown table structure in product.md, parsing then reconstructing the data should preserve all original information
**Validates: Requirements 1.1, 2.1, 3.1**

**Property 2: Fuzzy search ranking consistency**
*For any* search query and slang dataset, fuzzy matching results should be ranked by similarity score in descending order
**Validates: Requirements 1.2, 1.4**

**Property 3: Search result completeness**
*For any* search query that returns results, all returned slang entries should contain both term and translation fields
**Validates: Requirements 1.3**

**Property 4: Card rendering completeness**
*For any* collection of biryani spots, the card UI should render all spots with complete information
**Validates: Requirements 2.2**

**Property 5: Filter result accuracy**
*For any* combination of area and vibe filters applied to biryani spots, all returned results should match all selected criteria
**Validates: Requirements 2.3, 2.4, 2.5**

**Property 6: Time conversion consistency**
*For any* time data and toggle state, switching between standard and Hyderabadi modes should display appropriate time representations and update immediately
**Validates: Requirements 3.3, 3.4, 3.5**

**Property 7: Responsive layout adaptation**
*For any* viewport dimensions, the CSS layout should adapt appropriately while maintaining usability
**Validates: Requirements 4.3**

**Property 8: Styling consistency**
*For any* UI element, the styling should use the correct color palette and maintain appropriate contrast ratios
**Validates: Requirements 4.2, 4.4, 4.5**

**Property 9: Startup data loading**
*For any* valid product.md file, the application should successfully parse all tables during initialization
**Validates: Requirements 5.2**

**Property 10: Error handling resilience**
*For any* error condition during parsing or request handling, the system should log appropriately and continue operating
**Validates: Requirements 5.3, 5.5**

**Property 11: Response time consistency**
*For any* HTTP request, the system should respond within reasonable time limits
**Validates: Requirements 5.4**

## Error Handling

The application implements comprehensive error handling at multiple levels:

### Data Parsing Errors
- Malformed markdown tables: Log warning and continue with available data
- Missing product.md file: Initialize with empty datasets and log error
- Invalid data formats: Skip invalid entries and process remaining data

### Runtime Errors
- Search query errors: Return empty results with appropriate user feedback
- Filter operation errors: Fall back to unfiltered results
- Template rendering errors: Serve basic HTML with error message

### HTTP Errors
- 404 errors: Custom page with navigation back to main sections
- 500 errors: Generic error page with system status information
- Request timeout: Graceful degradation with cached responses

## Testing Strategy

The application uses a dual testing approach combining unit tests and property-based tests:

### Unit Testing
- Test specific examples of markdown parsing with known inputs
- Test edge cases like empty search queries and invalid filters
- Test error conditions and recovery mechanisms
- Test UI component rendering with sample data

### Property-Based Testing
- Use `hypothesis` library for Python property-based testing
- Configure each property test to run minimum 100 iterations
- Test universal properties across randomly generated inputs
- Each property test tagged with format: **Feature: hyderabad-culture-navigator, Property {number}: {property_text}**

### Testing Framework
- **Unit Tests**: Python `unittest` framework
- **Property Tests**: `hypothesis` library for property-based testing
- **Web Testing**: `pytest` with Flask test client
- **CSS Testing**: Automated accessibility and contrast checking

### Test Organization
- Co-locate tests with source files using `_test.py` suffix
- Separate test files for each major component
- Integration tests for full request-response cycles
- Performance tests for response time validation

The testing strategy ensures both specific functionality works correctly (unit tests) and universal properties hold across all inputs (property tests), providing comprehensive coverage for the cultural navigation features.