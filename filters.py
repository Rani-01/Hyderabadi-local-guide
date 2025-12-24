import logging

logger = logging.getLogger(__name__)

def filter_biryani_spots(biryani_data, area_filter=None, vibe_filter=None):
    """
    Filter biryani spots by area and vibe criteria.
    
    Args:
        biryani_data (list): List of biryani spot dictionaries
        area_filter (str): Area to filter by (case-insensitive)
        vibe_filter (str): Vibe to filter by (case-insensitive)
    
    Returns:
        list: Filtered list of biryani spots
    """
    if not biryani_data:
        return []
    
    try:
        filtered_spots = biryani_data.copy()
        
        # Apply area filter
        if area_filter and area_filter.strip():
            area_filter = area_filter.strip().lower()
            filtered_spots = [
                spot for spot in filtered_spots 
                if spot.get('area', '').lower() == area_filter
            ]
            logger.info(f"Applied area filter '{area_filter}': {len(filtered_spots)} spots remaining")
        
        # Apply vibe filter
        if vibe_filter and vibe_filter.strip():
            vibe_filter = vibe_filter.strip().lower()
            filtered_spots = [
                spot for spot in filtered_spots 
                if spot.get('vibe', '').lower() == vibe_filter
            ]
            logger.info(f"Applied vibe filter '{vibe_filter}': {len(filtered_spots)} spots remaining")
        
        # Sort by rating (highest first) if rating exists
        filtered_spots.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        logger.info(f"Filter results: {len(filtered_spots)} spots match criteria")
        return filtered_spots
        
    except Exception as e:
        logger.error(f"Error filtering biryani spots: {str(e)}")
        return biryani_data  # Return original data on error

def get_unique_areas(biryani_data):
    """
    Get list of unique areas from biryani data.
    
    Args:
        biryani_data (list): List of biryani spot dictionaries
    
    Returns:
        list: Sorted list of unique areas
    """
    if not biryani_data:
        return []
    
    try:
        areas = set()
        for spot in biryani_data:
            area = spot.get('area', '').strip()
            if area:
                areas.add(area)
        
        return sorted(list(areas))
        
    except Exception as e:
        logger.error(f"Error getting unique areas: {str(e)}")
        return []

def get_unique_vibes(biryani_data):
    """
    Get list of unique vibes from biryani data.
    
    Args:
        biryani_data (list): List of biryani spot dictionaries
    
    Returns:
        list: Sorted list of unique vibes
    """
    if not biryani_data:
        return []
    
    try:
        vibes = set()
        for spot in biryani_data:
            vibe = spot.get('vibe', '').strip()
            if vibe:
                vibes.add(vibe)
        
        return sorted(list(vibes))
        
    except Exception as e:
        logger.error(f"Error getting unique vibes: {str(e)}")
        return []

def get_filter_stats(biryani_data):
    """
    Get statistics about available filters.
    
    Args:
        biryani_data (list): List of biryani spot dictionaries
    
    Returns:
        dict: Statistics including unique areas, vibes, and counts
    """
    try:
        areas = get_unique_areas(biryani_data)
        vibes = get_unique_vibes(biryani_data)
        
        # Count spots per area
        area_counts = {}
        for spot in biryani_data:
            area = spot.get('area', '').strip()
            if area:
                area_counts[area] = area_counts.get(area, 0) + 1
        
        # Count spots per vibe
        vibe_counts = {}
        for spot in biryani_data:
            vibe = spot.get('vibe', '').strip()
            if vibe:
                vibe_counts[vibe] = vibe_counts.get(vibe, 0) + 1
        
        return {
            'total_spots': len(biryani_data),
            'unique_areas': areas,
            'unique_vibes': vibes,
            'area_counts': area_counts,
            'vibe_counts': vibe_counts
        }
        
    except Exception as e:
        logger.error(f"Error getting filter stats: {str(e)}")
        return {
            'total_spots': 0,
            'unique_areas': [],
            'unique_vibes': [],
            'area_counts': {},
            'vibe_counts': {}
        }

if __name__ == "__main__":
    # Test the filtering functionality
    sample_data = [
        {'name': 'Paradise', 'area': 'Secunderabad', 'vibe': 'Traditional', 'rating': 4.2},
        {'name': 'Bawarchi', 'area': 'RTC X Roads', 'vibe': 'Bustling', 'rating': 4.0},
        {'name': 'Shah Ghouse', 'area': 'Tolichowki', 'vibe': 'Local', 'rating': 4.3},
        {'name': 'Lucky Restaurant', 'area': 'Banjara Hills', 'vibe': 'Upscale', 'rating': 4.4},
        {'name': 'Hotel Shadab', 'area': 'Charminar', 'vibe': 'Heritage', 'rating': 4.0}
    ]
    
    print("All spots:", len(sample_data))
    print("Filter by area 'Secunderabad':", filter_biryani_spots(sample_data, area_filter='Secunderabad'))
    print("Filter by vibe 'Traditional':", filter_biryani_spots(sample_data, vibe_filter='Traditional'))
    print("Filter by both:", filter_biryani_spots(sample_data, area_filter='Secunderabad', vibe_filter='Traditional'))
    print("Unique areas:", get_unique_areas(sample_data))
    print("Unique vibes:", get_unique_vibes(sample_data))
    print("Filter stats:", get_filter_stats(sample_data))