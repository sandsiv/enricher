import logging
from csv_utils import read_csv, load_enrichment_data

def process_enrichment(original_file, config):
    original_data = read_csv(original_file, config['original_delimiter'])
    
    for block in config['enrichment_blocks']:
        enrichment_data = load_enrichment_data(block['file'], block['delimiter'], block['enrichment_column'])
        
        if block['original_column'] not in original_data[0]:
            logging.warning(f"Original column '{block['original_column']}' not found in original file. Skipping enrichment block '{block['name']}'.")
            continue
        
        for row in original_data:
            map_value = row[block['original_column']]
            if not map_value:
                logging.warning(f"Empty mapping value in original file for column '{block['original_column']}'. Skipping enrichment for this row.")
                continue
            
            if map_value in enrichment_data:
                enrichment_row = enrichment_data[map_value]
                for key, value in enrichment_row.items():
                    if key != block['enrichment_column']:
                        row[key] = value
            else:
                logging.warning(f"No matching value found in enrichment file for '{map_value}'. Skipping enrichment for this row.")
    
    return original_data