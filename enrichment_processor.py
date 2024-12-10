import logging
from csv_utils import read_csv, load_enrichment_data

def process_enrichment(original_file, config):
    """
    Process enrichment of the original CSV file using the provided configuration
    
    Args:
        original_file (str): Path to the original CSV file
        config (dict): Configuration dictionary containing enrichment rules
    
    Returns:
        list: List of dictionaries containing the enriched data
    """
    # Load original data
    original_data = read_csv(original_file, config['original_delimiter'])
    
    # Process static values first
    for column, value in config['static_values'].items():
        for row in original_data:
            # Add value only if column doesn't exist or current value is empty
            if column not in row or not row[column]:
                row[column] = value
    
    # Process enrichment blocks
    for block in config['enrichment_blocks']:
        # Load enrichment data with multi-column mapping
        enrichment_data = load_enrichment_data(
            block['file'], 
            block['delimiter'],
            block['enrichment_columns']
        )
        
        # Validate all original columns exist
        missing_columns = [col for col in block['original_columns'] if col not in original_data[0]]
        if missing_columns:
            logging.warning(
                f"Enrichment block '{block['name']}': Original columns {missing_columns} "
                f"not found in original file. Skipping this enrichment block."
            )
            continue
        
        # Process each row in original data
        for row in original_data:
            # Get values from original columns for mapping
            original_values = tuple(row[col] for col in block['original_columns'])
            
            # Check if any mapping value is empty
            if any(not val for val in original_values):
                logging.warning(
                    f"Enrichment block '{block['name']}': Empty mapping value in "
                    f"original file for columns {block['original_columns']}. "
                    f"Skipping enrichment for this row."
                )
                continue
            
            # Find and apply enrichment data
            if original_values in enrichment_data:
                enrichment_row = enrichment_data[original_values]
                # Add all columns except mapping columns
                for key, value in enrichment_row.items():
                    if key not in block['enrichment_columns']:
                        row[key] = value
            else:
                logging.warning(
                    f"Enrichment block '{block['name']}': No matching values found in "
                    f"enrichment file '{block['file']}' for {dict(zip(block['original_columns'], original_values))}. "
                    f"Skipping enrichment for this row."
                )
    
    return original_data