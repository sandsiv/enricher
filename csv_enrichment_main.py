import argparse
import logging
from config_handler import load_config
from enrichment_processor import process_enrichment
from csv_utils import read_csv, write_csv

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Enrich CSV file with data from other files.')
    parser.add_argument('original_file', help='Path to the original CSV file to be enriched')
    parser.add_argument('config_file', help='Path to the configuration INI file')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load configuration
    config = load_config(args.config_file)

    # Process enrichment
    enriched_data = process_enrichment(args.original_file, config)

    # Write enriched data to new file
    output_file = f"{args.original_file.rsplit('.', 1)[0]}_enriched.csv"
    write_csv(output_file, enriched_data, config['original_delimiter'])

    print(f"Enrichment complete. Output written to {output_file}")

if __name__ == "__main__":
    main()
