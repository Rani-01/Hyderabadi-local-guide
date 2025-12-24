import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

def convert_time_format(time_data, mode='standard'):
    """
    Convert time data between standard and Hyderabadi formats.
    
    Args:
        time_data (list): List of time mapping dictionaries
        mode (str): 'standard' or 'hyderabadi'
    
    Returns:
        list: List of time entries formatted for the specified mode
    """
    if not time_data:
        return []
    
    try:
        converted_times = []
        
        for entry in time_data:
            if mode == 'hyderabadi':
                converted_entry = {
                    'display_time': entry.get('hyderabadi_time', ''),
                    'description': entry.get('context', ''),
                    'standard_reference': entry.get('standard_time', ''),
                    'mode': 'hyderabadi'
                }
            else:  # standard mode
                converted_entry = {
                    'display_time': entry.get('standard_time', ''),
                    'description': entry.get('context', ''),
                    'hyderabadi_reference': entry.get('hyderabadi_time', ''),
                    'mode': 'standard'
                }
            
            converted_times.append(converted_entry)
        
        # Sort by time if possible
        converted_times = sort_time_entries(converted_times, mode)
        
        logger.info(f"Converted {len(converted_times)} time entries to {mode} mode")
        return converted_times
        
    except Exception as e:
        logger.error(f"Error converting time format: {str(e)}")
        return []

def sort_time_entries(time_entries, mode):
    """
    Sort time entries chronologically.
    
    Args:
        time_entries (list): List of time entry dictionaries
        mode (str): 'standard' or 'hyderabadi'
    
    Returns:
        list: Sorted time entries
    """
    try:
        if mode == 'standard':
            # Sort by standard time
            def get_sort_key(entry):
                time_str = entry.get('display_time', '')
                return parse_time_for_sorting(time_str)
        else:
            # For Hyderabadi mode, use the standard reference for sorting
            def get_sort_key(entry):
                time_str = entry.get('standard_reference', '')
                return parse_time_for_sorting(time_str)
        
        return sorted(time_entries, key=get_sort_key)
        
    except Exception as e:
        logger.error(f"Error sorting time entries: {str(e)}")
        return time_entries

def parse_time_for_sorting(time_str):
    """
    Parse time string for sorting purposes.
    
    Args:
        time_str (str): Time string (e.g., "9:00 AM", "12:00 PM")
    
    Returns:
        int: Minutes since midnight for sorting
    """
    try:
        if not time_str:
            return 0
        
        # Remove quotes if present
        time_str = time_str.strip('"\'')
        
        # Handle common time formats
        if 'AM' in time_str.upper() or 'PM' in time_str.upper():
            # Parse 12-hour format
            time_obj = datetime.strptime(time_str.upper(), '%I:%M %p').time()
        else:
            # Try 24-hour format
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                # If parsing fails, return a default value
                return 0
        
        # Convert to minutes since midnight
        return time_obj.hour * 60 + time_obj.minute
        
    except Exception as e:
        logger.warning(f"Could not parse time '{time_str}': {str(e)}")
        return 0

def get_current_time_context(time_data):
    """
    Get the current time context based on the current hour.
    
    Args:
        time_data (list): List of time mapping dictionaries
    
    Returns:
        dict: Current time context or None if not found
    """
    try:
        current_hour = datetime.now().hour
        
        # Find the closest time mapping
        best_match = None
        min_diff = float('inf')
        
        for entry in time_data:
            standard_time = entry.get('standard_time', '')
            entry_hour = parse_time_for_sorting(standard_time) // 60
            
            diff = abs(current_hour - entry_hour)
            if diff < min_diff:
                min_diff = diff
                best_match = entry
        
        if best_match:
            return {
                'standard_time': best_match.get('standard_time', ''),
                'hyderabadi_time': best_match.get('hyderabadi_time', ''),
                'context': best_match.get('context', ''),
                'is_current': True
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting current time context: {str(e)}")
        return None

def format_time_display(entry, highlight_current=False):
    """
    Format a time entry for display.
    
    Args:
        entry (dict): Time entry dictionary
        highlight_current (bool): Whether to highlight if this is current time
    
    Returns:
        dict: Formatted time entry for display
    """
    try:
        formatted = {
            'display_time': entry.get('display_time', ''),
            'description': entry.get('context', entry.get('description', '')),
            'mode': entry.get('mode', 'standard'),
            'is_current': entry.get('is_current', False)
        }
        
        # Add reference time for comparison
        if entry.get('mode') == 'hyderabadi':
            formatted['reference'] = f"({entry.get('standard_reference', '')})"
        else:
            formatted['reference'] = f"({entry.get('hyderabadi_reference', '')})"
        
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting time display: {str(e)}")
        return entry

if __name__ == "__main__":
    # Test the time conversion functionality
    sample_data = [
        {'standard_time': '9:00 AM', 'hyderabadi_time': '"Subah subah"', 'context': 'Early morning'},
        {'standard_time': '12:00 PM', 'hyderabadi_time': '"Dopahar"', 'context': 'Lunch time'},
        {'standard_time': '4:00 PM', 'hyderabadi_time': '"Chai time"', 'context': 'Tea time'},
        {'standard_time': '8:00 PM', 'hyderabadi_time': '"Raat ka khana"', 'context': 'Dinner time'},
        {'standard_time': '10:00 PM', 'hyderabadi_time': '"Thoda late"', 'context': 'Getting late'}
    ]
    
    print("Standard mode:")
    standard_times = convert_time_format(sample_data, 'standard')
    for time_entry in standard_times[:3]:
        print(f"  {time_entry['display_time']} - {time_entry['description']}")
    
    print("\nHyderabadi mode:")
    hyderabadi_times = convert_time_format(sample_data, 'hyderabadi')
    for time_entry in hyderabadi_times[:3]:
        print(f"  {time_entry['display_time']} - {time_entry['description']}")
    
    print("\nCurrent time context:")
    current = get_current_time_context(sample_data)
    if current:
        print(f"  {current['standard_time']} = {current['hyderabadi_time']} ({current['context']})")