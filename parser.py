import re
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_markdown_table(content, section_name):
    """
    Parse a markdown table from content under a specific section.
    
    Args:
        content (str): The markdown content
        section_name (str): The section header to look for
    
    Returns:
        list: List of dictionaries representing table rows
    """
    try:
        # Find the section
        section_pattern = rf"## {re.escape(section_name)}.*?\n\n(.*?)(?=\n## |\n# |$)"
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            logger.warning(f"Section '{section_name}' not found")
            return []
        
        section_content = section_match.group(1).strip()
        
        # Find table in the section
        lines = section_content.split('\n')
        table_lines = []
        in_table = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('|') and line.endswith('|'):
                table_lines.append(line)
                in_table = True
            elif in_table and not line:
                break
            elif in_table and not line.startswith('|'):
                break
        
        if len(table_lines) < 2:
            logger.warning(f"No valid table found in section '{section_name}'")
            return []
        
        # Parse header row
        header_line = table_lines[0]
        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
        
        # Skip separator line (second line with dashes)
        data_lines = table_lines[2:]
        
        # Parse data rows
        result = []
        for line in data_lines:
            if not line.strip():
                continue
                
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            # Ensure we have the right number of cells
            if len(cells) != len(headers):
                logger.warning(f"Row has {len(cells)} cells but expected {len(headers)}: {line}")
                continue
            
            # Create dictionary for this row
            row_dict = {}
            for i, header in enumerate(headers):
                # Convert header to lowercase and replace spaces with underscores
                key = header.lower().replace(' ', '_')
                value = cells[i] if i < len(cells) else ""
                
                # Try to convert numeric values
                if value.replace('.', '').replace('-', '').isdigit():
                    try:
                        if '.' in value:
                            row_dict[key] = float(value)
                        else:
                            row_dict[key] = int(value)
                    except ValueError:
                        row_dict[key] = value
                else:
                    row_dict[key] = value
            
            result.append(row_dict)
        
        logger.info(f"Successfully parsed {len(result)} rows from '{section_name}' section")
        return result
        
    except Exception as e:
        logger.error(f"Error parsing section '{section_name}': {str(e)}")
        return []

def parse_product_data(file_path='product.md'):
    """
    Parse all sections from the product.md file.
    
    Args:
        file_path (str): Path to the product.md file
    
    Returns:
        dict: Dictionary containing parsed data for all sections
    """
    if not os.path.exists(file_path):
        logger.error(f"File {file_path} not found")
        return {
            'slang_data': [],
            'biryani_data': [],
            'time_data': []
        }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse each section
        slang_data = parse_markdown_table(content, "Lingo Section")
        biryani_data = parse_markdown_table(content, "Biryani Spots")
        time_data = parse_markdown_table(content, "Time Tables")
        
        logger.info(f"Parsed data: {len(slang_data)} slang terms, {len(biryani_data)} biryani spots, {len(time_data)} time mappings")
        
        return {
            'slang_data': slang_data,
            'biryani_data': biryani_data,
            'time_data': time_data
        }
        
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return {
            'slang_data': [],
            'biryani_data': [],
            'time_data': []
        }

if __name__ == "__main__":
    # Test the parser
    data = parse_product_data()
    print("Slang data:", len(data['slang_data']))
    print("Biryani data:", len(data['biryani_data']))
    print("Time data:", len(data['time_data']))
    
    if data['slang_data']:
        print("Sample slang entry:", data['slang_data'][0])
    if data['biryani_data']:
        print("Sample biryani entry:", data['biryani_data'][0])
    if data['time_data']:
        print("Sample time entry:", data['time_data'][0])