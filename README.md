# CSV Data Enrichment Tool

A flexible Python tool for enriching CSV files with data from multiple sources. This tool allows you to combine data from various CSV files using configurable mapping rules and supports pattern matching for data source files.

## Features

- Enrich CSV files using data from multiple source files
- Support for different delimiters in source files
- Flexible column mapping between original and enrichment files
- Pattern matching support for enrichment file names
- Static value addition for missing columns
- Multi-column mapping support
- Detailed warning messages for unsuccessful mappings
- Configuration-driven approach using INI files
- No external dependencies - uses only Python standard library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sandsiv/enricher.git
cd enricher
```

2. The tool uses only Python standard library (no additional dependencies required)

## Usage

### Basic Usage

```bash
python csv_enrichment_main.py path/to/original_file.csv path/to/config.ini
```

### Configuration File Example

Create a `config.ini` file with your enrichment settings:

```ini
[original]
delimiter = ,
language = EN            # Static value - will be added to all rows
region = EMEA           # Another static value example

[customer_info]
file = customer_data.csv
original_columns = customer_id
enrichment_columns = cust_id
delimiter = ,

[product_details]
file = product_catalog.csv
original_columns = product_code
enrichment_columns = item_code
delimiter = ;

[multi_column_example]
file = survey.csv
original_columns = product_code, supplier_id
enrichment_columns = item_code, vendor_id
delimiter = ,
```

### Static Values

The tool supports adding static values through the `[original]` section:
- Any key in `[original]` section except 'delimiter' is treated as a column name
- The corresponding value will be added to all rows
- If the column already exists in the data, static value will only be applied to empty cells
- Useful for adding constant values like language, region, or system identifiers

### Multi-Column Mapping

For scenarios where matching needs to be done on multiple columns:
- Use comma-separated lists in `original_columns` and `enrichment_columns`
- The number of columns must match between original and enrichment
- Mapping is one-to-one in order (first to first, second to second, etc.)
- All specified columns must exist in respective files

### Example Data Files

Original file (`original_data.csv`):
```csv
customer_id,product_code,supplier_id,order_date,quantity
C001,P101,S01,2023-01-15,5
C002,P102,S02,2023-01-16,3
```

Customer enrichment file (`customer_data.csv`):
```csv
cust_id,customer_name,email,country
C001,John Doe,john.doe@example.com,USA
C002,Jane Smith,jane.smith@example.com,Canada
```

Multi-column enrichment file (`survey.csv`):
```csv
item_code,vendor_id,SURVEY_ID
P101,S01,1
P102,S02,2
```

## File Pattern Support

The tool supports glob patterns in enrichment file names:
- Use `*` to match any sequence of characters
- The most recent file (alphabetically sorted) will be used
- Example: `customer_data_*.csv` will match files like:
  - `customer_data_20230101.csv`
  - `customer_data_20230102.csv`
  - And use the last one when sorted

## Output

The tool creates a new file with the suffix "_enriched" added to the original filename:
- Input: `original_data.csv`
- Output: `original_data_enriched.csv`

## Error Handling

The tool provides detailed warning messages for:
- Missing columns in the original file
- Empty mapping values
- Unmatched values in enrichment files
- Invalid column mappings

Example warning message:
```
WARNING: Enrichment block 'customer_info': No matching value found in enrichment file 'customer_data.csv' for 'cust_id' = 'C999'
```

## Project Structure

```
csv_enrichment/
├── csv_enrichment_main.py   # Main script
├── config_handler.py        # Configuration processing
├── csv_utils.py            # CSV operations
├── enrichment_processor.py  # Core logic
├── config.ini             # Configuration
└── README.md              # This file
```

## Limitations

- Cannot use enriched columns for mapping in subsequent blocks
- All data is treated as strings
- No support for multi-value mappings
- Memory usage depends on file sizes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Search for existing issues
3. Create a new issue with:
   - Detailed description of the problem
   - Sample data (if possible)
   - Configuration file used
   - Error messages received
