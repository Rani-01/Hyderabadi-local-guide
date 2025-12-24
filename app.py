from flask import Flask, render_template, request, jsonify
import os
from parser import parse_product_data
from search import search_slang, get_search_suggestions
from filters import filter_biryani_spots, get_unique_areas, get_unique_vibes, get_filter_stats
from time_converter import convert_time_format, get_current_time_context, format_time_display

app = Flask(__name__)

# Global data storage
slang_data = []
biryani_data = []
time_data = []

def load_data():
    """Load data from product.md on startup"""
    global slang_data, biryani_data, time_data
    
    try:
        data = parse_product_data()
        slang_data = data['slang_data']
        biryani_data = data['biryani_data']
        time_data = data['time_data']
        
        print(f"✅ Data loaded successfully:")
        print(f"   - {len(slang_data)} slang terms")
        print(f"   - {len(biryani_data)} biryani spots")
        print(f"   - {len(time_data)} time mappings")
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        # Continue with empty data

@app.route('/')
def home():
    """Main landing page with navigation to all features"""
    return render_template('index.html')

@app.route('/slang')
def slang_translator():
    """Slang translator page"""
    return render_template('slang.html')

@app.route('/biryani')
def biryani_recommender():
    """Biryani recommender page"""
    return render_template('biryani.html')

@app.route('/time')
def time_converter():
    """Time converter page"""
    return render_template('time.html')

@app.route('/api/search/slang')
def api_search_slang():
    """API endpoint for slang search"""
    query = request.args.get('q', '').strip()
    threshold = int(request.args.get('threshold', 60))
    limit = int(request.args.get('limit', 10))
    
    try:
        results = search_slang(query, slang_data, threshold=threshold, limit=limit)
        
        # If no results and query is not empty, provide suggestions
        suggestions = []
        if not results and query:
            suggestions = get_search_suggestions(query, slang_data)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'suggestions': suggestions,
            'total': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'query': query,
            'results': [],
            'suggestions': [],
            'total': 0
        }), 500

@app.route('/api/slang/all')
def api_get_all_slang():
    """API endpoint to get all slang terms"""
    try:
        return jsonify({
            'success': True,
            'data': slang_data,
            'total': len(slang_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': [],
            'total': 0
        }), 500

@app.route('/api/biryani/filter')
def api_filter_biryani():
    """API endpoint for filtering biryani spots"""
    area = request.args.get('area', '').strip()
    vibe = request.args.get('vibe', '').strip()
    
    try:
        # Convert empty strings to None for filtering
        area_filter = area if area else None
        vibe_filter = vibe if vibe else None
        
        filtered_spots = filter_biryani_spots(biryani_data, area_filter, vibe_filter)
        
        return jsonify({
            'success': True,
            'filters': {
                'area': area_filter,
                'vibe': vibe_filter
            },
            'results': filtered_spots,
            'total': len(filtered_spots)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'filters': {'area': area, 'vibe': vibe},
            'results': [],
            'total': 0
        }), 500

@app.route('/api/biryani/all')
def api_get_all_biryani():
    """API endpoint to get all biryani spots"""
    try:
        return jsonify({
            'success': True,
            'data': biryani_data,
            'total': len(biryani_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': [],
            'total': 0
        }), 500

@app.route('/api/biryani/filters')
def api_get_biryani_filters():
    """API endpoint to get available filter options"""
    try:
        stats = get_filter_stats(biryani_data)
        
        return jsonify({
            'success': True,
            'areas': stats['unique_areas'],
            'vibes': stats['unique_vibes'],
            'area_counts': stats['area_counts'],
            'vibe_counts': stats['vibe_counts'],
            'total_spots': stats['total_spots']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'areas': [],
            'vibes': [],
            'area_counts': {},
            'vibe_counts': {},
            'total_spots': 0
        }), 500

@app.route('/api/time/convert')
def api_convert_time():
    """API endpoint for time conversion"""
    mode = request.args.get('mode', 'standard').lower()
    
    if mode not in ['standard', 'hyderabadi']:
        return jsonify({
            'success': False,
            'error': 'Invalid mode. Use "standard" or "hyderabadi"',
            'mode': mode,
            'times': []
        }), 400
    
    try:
        converted_times = convert_time_format(time_data, mode)
        
        # Format for display
        formatted_times = [format_time_display(entry) for entry in converted_times]
        
        return jsonify({
            'success': True,
            'mode': mode,
            'times': formatted_times,
            'total': len(formatted_times)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mode': mode,
            'times': [],
            'total': 0
        }), 500

@app.route('/api/time/current')
def api_get_current_time():
    """API endpoint to get current time context"""
    try:
        current_context = get_current_time_context(time_data)
        
        if current_context:
            return jsonify({
                'success': True,
                'current_time': current_context
            })
        else:
            return jsonify({
                'success': True,
                'current_time': None,
                'message': 'No matching time context found'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'current_time': None
        }), 500

@app.route('/api/time/all')
def api_get_all_times():
    """API endpoint to get all time mappings"""
    try:
        return jsonify({
            'success': True,
            'data': time_data,
            'total': len(time_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': [],
            'total': 0
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    # Log the error
    app.logger.error(f"Unhandled exception: {str(e)}")
    
    # Return 500 error page
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Parse product.md data on startup
    load_data()
    
    # Run on port 8000 as specified
    app.run(host='0.0.0.0', port=8000, debug=True)