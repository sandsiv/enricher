# CSV Data Enrichment Tool Documentation

## Overview
The CSV Data Enrichment Tool is a Python-based utility designed to enhance CSV files by combining data from multiple source files. It allows for flexible data mapping and enrichment using a configuration-driven approach.

## Goals
1. Enrich a primary CSV file with data from multiple secondary CSV files
2. Support flexible column mapping between original and enrichment files
3. Handle different file delimiters
4. Process files sequentially based on configuration
5. Support pattern-based file selection for enrichment data sources
6. Provide clear warning messages for unsuccessful enrichment attempts
7. Maintain data integrity throughout the enrichment process

## Project Structure

### Files Organization
```
csv_enrichment/
├── csv_enrichment_main.py   # Main script entry point
├── config_handler.py        # Configuration file processing
├── csv_utils.py            # CSV file operations
├── enrichment_processor.py # Core enrichment logic
├── requirements.txt        # Project dependencies
├── config.ini             # Configuration file
└── docs/                  # Documentation
```

### Key Components

#### 1. Main Script (csv_enrichment_main.py)
- Entry point for the application
- Handles command-line arguments
- Sets up logging
- Orchestrates the enrichment process

#### 2. Configuration Handler (config_handler.py)
- Loads and validates configuration from INI file
- Supports file pattern matching for enrichment sources
- Uses glob module for file pattern resolution
- Selects the most recent file when patterns are used (based on alphabetical sorting)

#### 3. CSV Utilities (csv_utils.py)
- Provides core CSV file operations
- Handles file reading and writing
- Manages data loading for enrichment files

#### 4. Enrichment Processor (enrichment_processor.py)
- Implements the core enrichment logic
- Processes data sequentially by configuration block
- Handles mapping between different column names
- Provides detailed warning messages for enrichment failures

## Configuration File Structure

### Format
The configuration file (config.ini) uses INI format with the following structure:

```ini
[original]
delimiter = <delimiter_char>

[block_name]
file = <file_pattern>
original_column = <column_name_in_original>
enrichment_column = <column_name_in_enrichment>
delimiter = <delimiter_char>
```

### Sections
1. `[original]` section (required):
   - `delimiter`: Specifies the delimiter for the original file

2. Enrichment blocks (one or more required):
   - `file`: File name or pattern for enrichment data
   - `original_column`: Column name in original file for mapping
   - `enrichment_column`: Column name in enrichment file for mapping
   - `delimiter`: Delimiter used in this enrichment file

## File Pattern Support
- Supports glob patterns in enrichment file names
- Example patterns:
  - `customer_data_*.csv`
  - `product_data_202[0-9]*.csv`
- Always selects the last file when sorted alphabetically
- Useful for periodic data updates with dated filenames

## Process Flow
1. Command line arguments processing
2. Configuration loading and validation
3. For each enrichment block:
   - Load enrichment data file
   - Find matching column in original data
   - Process each row for enrichment
   - Add new columns from enrichment data
4. Output generation

## Warning Messages
The tool provides detailed warning messages for various scenarios:
- Missing columns in original file
- Empty mapping values
- Unmatched values in enrichment files

Warning format:
```
Enrichment block '{block_name}': No matching value found in enrichment file '{filename}' for '{column}' = '{value}'
```

## Usage Examples

### Basic Usage
```bash
python csv_enrichment_main.py original_file.csv config.ini
```

### Sample Configuration
```ini
[original]
delimiter = ,

[customer_info]
file = customer_data_*.csv
original_column = customer_id
enrichment_column = cust_id
delimiter = ,
```

## Important Notes

### Data Processing
- Enrichment happens sequentially by block
- Current implementation does not support using enriched columns for mapping in subsequent blocks
- First matching record is used when multiple matches exist in enrichment file

### File Handling
- Original file is not modified
- New enriched file is created with "_enriched" suffix
- Memory usage depends on file sizes, particularly the original file size

### Limitations
1. Cannot use enriched columns for mapping in subsequent blocks
2. No support for complex data transformations
3. All data is treated as strings
4. No support for multi-value mappings

## Future Development Considerations

### Potential Enhancements
1. Support for using enriched columns in subsequent mappings
2. Advanced pattern matching for file selection
3. Data type handling and transformation
4. Parallel processing for large files
5. Custom column mapping functions
6. Support for different output formats
7. Advanced error handling and recovery
8. Progress reporting for large file processing

### Performance Optimization
Current implementation loads enrichment files into memory. For very large enrichment files, consider:
1. Implementing database backend
2. Chunk-based processing
3. Streaming data handling
4. Indexing for faster lookups

## Troubleshooting

### Common Issues
1. File not found: Check file patterns and paths
2. Column mapping errors: Verify column names in config
3. Memory issues: Consider file sizes and available RAM
4. Delimiter mismatches: Verify delimiter settings

### Debug Process
1. Enable detailed logging
2. Verify file contents and structure
3. Check configuration syntax
4. Validate column names and mappings

## Support and Maintenance
- Keep enrichment files organized with clear naming conventions
- Regularly backup original data
- Monitor warning messages for data quality issues
- Update configuration as data structures change
