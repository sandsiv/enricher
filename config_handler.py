import configparser

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
    required_keys = ['file', 'original_column', 'enrichment_column', 'delimiter']
    for block in enrichment_blocks:
        if not all(key in config[block] for key in required_keys):
            raise ValueError(f"Enrichment block '{block}' must have 'file', 'original_column', 'enrichment_column', and 'delimiter' keys")

    # Prepare config dictionary
    config_dict = {
        'original_delimiter': config['original']['delimiter'],
        'enrichment_blocks': []
    }

    for block in enrichment_blocks:
        config_dict['enrichment_blocks'].append({
            'name': block,
            'file': config[block]['file'],
            'original_column': config[block]['original_column'],
            'enrichment_column': config[block]['enrichment_column'],
            'delimiter': config[block]['delimiter']
        })

    return config_dict