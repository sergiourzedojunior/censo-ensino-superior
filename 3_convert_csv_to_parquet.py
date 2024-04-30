import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

base_dir = os.getcwd()

def convert_csv_to_parquet(csv_file, parquet_file, delimiter):
    try:
        df = pd.read_csv(csv_file, delimiter=delimiter, on_bad_lines='skip', dtype=str)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_file, delimiter=delimiter, on_bad_lines='skip', encoding='ISO-8859-1', dtype=str)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, delimiter=delimiter, on_bad_lines='skip', encoding='cp1252', dtype=str)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file)

def process_directory(dir_path):
    csv_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    # Extract the year from the directory name
    year = int(dir_path.split("\\")[-1].split("_")[-1])
    delimiter = "|" if year <= 2008 else ";"

    for csv_file in csv_files:
        parquet_file = csv_file.replace('.csv', '.parquet').replace('.CSV', '.parquet')
        convert_csv_to_parquet(csv_file, parquet_file, delimiter)

# Process each subdirectory
for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    if os.path.isdir(subdir_path):
        try:
            process_directory(subdir_path)
        except ValueError:
            print(f"Skipping directory {subdir_path} because its name does not contain a valid year.")
            continue
        
        
        
