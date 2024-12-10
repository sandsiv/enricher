import csv

def read_csv(file_path, delimiter):
    with open(file_path, 'r', newline='') as csvfile:
        # Create reader
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        # Clean up fieldnames - strip any whitespace
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        # Read all rows
        return [row for row in reader]

def write_csv(file_path, data, delimiter):
    if not data:
        return

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)

def load_enrichment_data(file_path, delimiter, mapping_columns):
    """
    Load enrichment data with support for multi-column mapping
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): CSV delimiter character
        mapping_columns (list): List of column names to use for mapping
    
    Returns:
        dict: Dictionary with tuple of mapping column values as key and full row as value
    """
    data = read_csv(file_path, delimiter)
    return {
        tuple(row[col] for col in mapping_columns): row 
        for row in data
    }