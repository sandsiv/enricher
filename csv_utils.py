import csv

def read_csv(file_path, delimiter):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        return [row for row in reader]

def write_csv(file_path, data, delimiter):
    if not data:
        return

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)

def load_enrichment_data(file_path, delimiter, map_column):
    data = read_csv(file_path, delimiter)
    return {row[map_column]: row for row in data}