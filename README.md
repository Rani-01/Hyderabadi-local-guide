# 🏛️ Hyderabad Culture & Slang Navigator

A Flask web application that serves as your comprehensive guide to Hyderabad's local culture, slang, biryani spots, and unique time perception.

## ✨ Features

### 🗣️ Slang Translator
- **Fuzzy Search**: Find local slang terms with smart matching
- **Real-time Results**: Instant search as you type
- **Comprehensive Database**: Covers popular Hyderabadi expressions
- **Smart Suggestions**: Get suggestions for misspelled terms

### 🍛 Biryani Recommender
- **Card-based UI**: Beautiful visual presentation of biryani spots
- **Smart Filtering**: Filter by area and vibe
- **Star Ratings**: See ratings for each restaurant
- **Responsive Design**: Works perfectly on mobile devices

### ⏰ Time Converter
- **Dual Mode**: Switch between Standard Time and "Hyderabadi Reality"
- **Current Time Context**: See what time it is in Hyderabadi terms
- **Cultural Insights**: Understand local time perceptions
- **Interactive Toggle**: Smooth switching between modes

## 🎨 Design

- **Royal Theme**: Uses Royal Charcoal (#1A1A1B) and Nizam Gold (#D4AF37)
- **Responsive**: Optimized for desktop, tablet, and mobile
- **Accessible**: WCAG compliant with proper contrast ratios
- **Modern**: Clean, elegant interface with smooth animations

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   ```
   http://localhost:8000
   ```

## 📁 Project Structure

```
hyderabad-culture-navigator/
├── app.py                 # Main Flask application
├── parser.py             # Markdown table parser
├── search.py             # Fuzzy search functionality
├── filters.py            # Biryani filtering system
├── time_converter.py     # Time conversion logic
├── product.md            # Data source (slang, biryani, time)
├── requirements.txt      # Python dependencies
├── test_integration.py   # Integration tests
├── static/
│   └── style.css        # Complete styling with royal theme
└── templates/
    ├── base.html        # Base template with navigation
    ├── index.html       # Home page
    ├── slang.html       # Slang translator interface
    ├── biryani.html     # Biryani recommender interface
    ├── time.html        # Time converter interface
    ├── 404.html         # Custom 404 error page
    └── 500.html         # Custom 500 error page
```

## 🛠️ Technical Details

### Backend
- **Framework**: Flask 2.3.3
- **Search**: FuzzyWuzzy for intelligent string matching
- **Data**: Markdown table parsing with error handling
- **API**: RESTful endpoints for all features

### Frontend
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS for interactivity
- **Responsive**: Mobile-first design approach
- **Accessibility**: Skip links, proper ARIA labels, keyboard navigation

### Data Format
The application parses data from `product.md` with three main sections:
- **Lingo Section**: Local slang terms with translations
- **Biryani Spots**: Restaurant data with areas and vibes
- **Time Tables**: Standard to Hyderabadi time mappings

## 🧪 Testing

The application includes comprehensive testing with both integration tests and property-based tests:

### Integration Tests
Run the integration tests to verify core functionality:

```bash
python test_integration.py
```

### Property-Based Tests
Run the property-based tests using Hypothesis to verify universal properties:

```bash
python -m pytest test_properties.py -v
```

The property-based tests validate:
- **Startup Data Loading**: Application handles any valid/invalid product.md files
- **Markdown Parsing Round Trip**: Data preservation through parse/reconstruct cycles
- **Error Handling Resilience**: Graceful handling of malformed inputs
- **Fuzzy Search Ranking**: Consistent similarity-based result ordering
- **Search Result Completeness**: All results contain required fields
- **Filter Result Accuracy**: Filtered results match all specified criteria
- **Card Rendering Completeness**: UI cards display all required information
- **Time Conversion Consistency**: Proper mode switching and data preservation
- **Responsive Layout Adaptation**: Logical breakpoint behavior
- **Styling Consistency**: Color palette and contrast ratio compliance
- **Response Time Consistency**: Performance within acceptable limits

### Run All Tests
```bash
python test_integration.py && python -m pytest test_properties.py
```

## 🌟 Key Features Implemented

- ✅ **Port 8000**: Application runs on specified port
- ✅ **Markdown Parsing**: Converts product.md tables to Python dictionaries
- ✅ **Fuzzy Search**: Smart slang term matching
- ✅ **Card UI**: Beautiful biryani spot presentation
- ✅ **Time Toggle**: Smooth switching between time modes
- ✅ **Royal Styling**: Consistent Hyderabadi theme throughout
- ✅ **Responsive Design**: Works on all device sizes
- ✅ **Error Handling**: Graceful error pages and API responses

## 🎯 Usage Examples

### Search for Slang
- Type "baigan" to find its meaning
- Get suggestions for misspelled terms
- Browse all available slang terms

### Find Biryani Spots
- Filter by area (e.g., "Secunderabad")
- Filter by vibe (e.g., "Traditional")
- View ratings and descriptions

### Convert Time
- Toggle between standard and Hyderabadi time
- See current time in cultural context
- Understand local time expressions

## 🏗️ Architecture

The application follows a clean separation of concerns:
- **Data Layer**: Markdown parsing and in-memory storage
- **Business Logic**: Search, filtering, and conversion algorithms
- **API Layer**: RESTful endpoints for frontend communication
- **Presentation Layer**: Responsive HTML templates with royal styling

## 🔧 Configuration

The application is configured to:
- Run on `0.0.0.0:8000` for external access
- Parse data on startup with error handling
- Serve static files from `/static`


- Handle errors gracefully with custom pages

---

**Built with ❤️ for the Pearl City of Hyderabad** 🏛️✨


https://github.com/user-attachments/assets/10c391b9-4291-4401-9241-892bfadefbf4


