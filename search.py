from fuzzywuzzy import fuzz, process
import logging

logger = logging.getLogger(__name__)

def search_slang(query, slang_data, threshold=60, limit=10):
    """
    Search for slang terms using fuzzy matching.
    
    Args:
        query (str): Search query
        slang_data (list): List of slang dictionaries
        threshold (int): Minimum similarity score (0-100)
        limit (int): Maximum number of results to return
    
    Returns:
        list: List of matching slang entries with similarity scores
    """
    if not query or not query.strip():
        # Return all slang terms if query is empty
        return [{'entry': entry, 'score': 100} for entry in slang_data]
    
    if not slang_data:
        return []
    
    query = query.strip().lower()
    results = []
    
    try:
        # Search in term field
        for entry in slang_data:
            term = entry.get('term', '').lower()
            translation = entry.get('translation', '').lower()
            category = entry.get('category', '').lower()
            usage = entry.get('usage', '').lower()
            
            # Calculate similarity scores for different fields
            term_score = fuzz.ratio(query, term)
            translation_score = fuzz.partial_ratio(query, translation)
            category_score = fuzz.partial_ratio(query, category)
            usage_score = fuzz.partial_ratio(query, usage)
            
            # Use the highest score among all fields
            max_score = max(term_score, translation_score, category_score, usage_score)
            
            if max_score >= threshold:
                results.append({
                    'entry': entry,
                    'score': max_score,
                    'match_field': get_best_match_field(query, entry)
                })
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Limit results
        results = results[:limit]
        
        logger.info(f"Search for '{query}' returned {len(results)} results")
        return results
        
    except Exception as e:
        logger.error(f"Error in slang search: {str(e)}")
        return []

def get_best_match_field(query, entry):
    """
    Determine which field had the best match for highlighting.
    
    Args:
        query (str): Search query
        entry (dict): Slang entry
    
    Returns:
        str: Field name with best match
    """
    query = query.lower()
    scores = {
        'term': fuzz.ratio(query, entry.get('term', '').lower()),
        'translation': fuzz.partial_ratio(query, entry.get('translation', '').lower()),
        'category': fuzz.partial_ratio(query, entry.get('category', '').lower()),
        'usage': fuzz.partial_ratio(query, entry.get('usage', '').lower())
    }
    
    return max(scores, key=scores.get)

def get_search_suggestions(query, slang_data, limit=5):
    """
    Get search suggestions for when no results are found.
    
    Args:
        query (str): Original search query
        slang_data (list): List of slang dictionaries
        limit (int): Maximum number of suggestions
    
    Returns:
        list: List of suggested search terms
    """
    if not query or not slang_data:
        return []
    
    try:
        # Extract all terms for suggestions
        terms = [entry.get('term', '') for entry in slang_data if entry.get('term')]
        
        # Get closest matches
        suggestions = process.extract(query, terms, limit=limit, scorer=fuzz.ratio)
        
        # Return just the terms (not the scores)
        return [suggestion[0] for suggestion in suggestions if suggestion[1] > 30]
        
    except Exception as e:
        logger.error(f"Error getting search suggestions: {str(e)}")
        return []

if __name__ == "__main__":
    # Test the search functionality
    sample_data = [
        {'term': 'Baigan', 'translation': 'Eggplant/Nonsense', 'category': 'Food/Slang', 'usage': 'Yeh sab baigan hai'},
        {'term': 'Nakko', 'translation': 'No/Don\'t want', 'category': 'Expression', 'usage': 'Nakko re, I don\'t want'},
        {'term': 'Bindaas', 'translation': 'Carefree/Cool', 'category': 'Attitude', 'usage': 'Bindaas raho yaar'}
    ]
    
    # Test searches
    print("Search for 'baigan':", search_slang('baigan', sample_data))
    print("Search for 'cool':", search_slang('cool', sample_data))
    print("Search for 'xyz':", search_slang('xyz', sample_data))
    print("Suggestions for 'bagan':", get_search_suggestions('bagan', sample_data))