# CSV Enrichment tool
Created for internal usage

Enriches "original file" with columns from "enrichment files" using defined columns as "linking keys"

## How to run
/ python csv_enrichment_main.py original_data.csv config.ini /

original_data.csv - file than need to be enriched from connected dictionaries
config.ini - file with configuration that defines how it should be enriched and from what sources

## Config file

### Sample of config

[original]

delimiter = ,

[customer_info]

file = customer_data.csv

original_column = customer_id

enrichment_column = cust_id

delimiter = ,

### Explanation

Block [original] describes what delimiter we will use in the file that we want to enrich

Other blocks are blocks that describes dictionary files for enrichment of original file.
"original_column" defiles the name of column in the original file that used as "key", while 
"enrichment_column" is the name of linked column in enrichment dictionary "file".

There can be as many separate blocks for enrichment with different files.

*Enrichment process is not "sequental", i.e. "original_column" has to be in the original file header*