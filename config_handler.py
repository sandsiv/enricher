import configparser
import glob
import os
import csv

def parse_column_spec(col_spec):
    """
    Parse a column specification that may contain a default value.
    Handles quoted values and preserves spaces in default values.
    
    Args:
        col_spec (str): Column specification (e.g., "column_name::default value" or 'column::\"quoted value\"')
    
    Returns:
        dict: Dictionary with 'column' and 'default' keys
    """
    # First split by :: but preserve anything in quotes
    parts = []
    current_part = ''
    in_quotes = False
    i = 0
    
    while i < len(col_spec):
        if col_spec[i:i+2] == '::' and not in_quotes:
            parts.append(current_part.strip())
            current_part = ''
            i += 2
            continue
            
        if col_spec[i] == '"':
            in_quotes = not in_quotes
            
        current_part += col_spec[i]
        i += 1
        
    parts.append(current_part.strip())
    
    # Clean up quotes if present
    if len(parts) == 2:
        default_value = parts[1]
        if default_value.startswith('"') and default_value.endswith('"'):
            default_value = default_value[1:-1]
        return {
            'column': parts[0].strip(),
            'default': default_value
        }
    else:
        return {
            'column': parts[0].strip(),
            'default': None
        }

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Validate config structure
    if 'original' not in config:
        raise ValueError("Config file must have an 'original' section")

    if 'delimiter' not in config['original']:
        raise ValueError("'original' section must specify a delimiter")

    # Extract enrichment blocks
    enrichment_blocks = [section for section in config.sections() if section != 'original']

    if not enrichment_blocks:
        raise ValueError("Config file must have at least one enrichment block")

    # Validate enrichment blocks
    required_keys = ['file', 'original_columns', 'enrichment_columns', 'delimiter']
    for block in enrichment_blocks:
        if not all(key in config[block] for key in required_keys):
            raise ValueError(f"Enrichment block '{block}' must have 'file', 'original_columns', 'enrichment_columns', and 'delimiter' keys")

    # Prepare config dictionary
    config_dict = {
        'original_delimiter': config['original']['delimiter'],
        'static_values': {},
        'enrichment_blocks': []
    }

    # Extract static values from original section
    for key, value in config['original'].items():
        if key != 'delimiter':
            config_dict['static_values'][key] = value

    # Process enrichment blocks
    for block in enrichment_blocks:
        file_pattern = config[block]['file']
        matching_files = glob.glob(file_pattern)
        
        if not matching_files:
            raise ValueError(f"No files found matching pattern '{file_pattern}' for block '{block}'")
        
        # Sort the matching files and select the last one (most recent)
        file_to_use = sorted(matching_files)[-1]

        # Parse original columns using csv module to handle commas within quotes
        original_columns_raw = next(csv.reader([config[block]['original_columns']]))
        enrichment_columns = [col.strip() for col in config[block]['enrichment_columns'].split(',')]

        # Process original columns to extract default values
        original_columns = []
        for col_spec in original_columns_raw:
            try:
                column_info = parse_column_spec(col_spec)
                original_columns.append(column_info)
            except Exception as e:
                raise ValueError(
                    f"Invalid column specification '{col_spec}' in block '{block}'. "
                    f"Format should be 'column_name' or 'column_name::default_value'. Error: {str(e)}"
                )

        if len(original_columns) != len(enrichment_columns):
            raise ValueError(
                f"Number of original columns must match number of enrichment columns in block '{block}'. "
                f"Got {len(original_columns)} original columns and {len(enrichment_columns)} enrichment columns."
            )

        config_dict['enrichment_blocks'].append({
            'name': block,
            'file': file_to_use,
            'original_columns': original_columns,
            'enrichment_columns': enrichment_columns,
            'delimiter': config[block]['delimiter']
        })

    return config_dict
