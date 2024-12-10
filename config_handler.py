import configparser
import glob
import os

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

        # Parse and validate column mappings
        original_columns = [col.strip() for col in config[block]['original_columns'].split(',')]
        enrichment_columns = [col.strip() for col in config[block]['enrichment_columns'].split(',')]

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
