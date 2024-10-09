import logging
from csv_utils import read_csv, load_enrichment_data

def process_enrichment(original_file, config):
    original_data = read_csv(original_file, config['original_delimiter'])
    
    for block in config['enrichment_blocks']:
        enrichment_data = load_enrichment_data(block['file'], block['delimiter'], block['enrichment_column'])
        
        if block['original_column'] not in original_data[0]:
            logging.warning(f"Enrichment block '{block['name']}': Original column '{block['original_column']}' not found in original file. Skipping this enrichment block.")
            continue
        
        for row in original_data:
            map_value = row[block['original_column']]
            if not map_value:
                logging.warning(f"Enrichment block '{block['name']}': Empty mapping value in original file for column '{block['original_column']}'. Skipping enrichment for this row.")
                continue
            
            if map_value in enrichment_data:
                enrichment_row = enrichment_data[map_value]
                for key, value in enrichment_row.items():
                    if key != block['enrichment_column']:
                        row[key] = value
            else:
                logging.warning(f"Enrichment block '{block['name']}': No matching value found in enrichment file '{block['file']}' for '{block['enrichment_column']}' = '{map_value}'. Skipping enrichment for this row.")
    
    return original_data