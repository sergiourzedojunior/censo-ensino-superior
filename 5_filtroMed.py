import pandas as pd
import os

# Specify the path to your directory
dir_path = r"D:\OneDrive\censo ensino superior"

# Get a list of all .parquet files in the directory
parquet_files = [os.path.join(root, file) for root, dirs, files in os.walk(dir_path) for file in files if file.endswith('.parquet')]

# Define the various forms of 'medicina'
medicina_forms = ['^medicina$', '^Medicina$', '^MEDICINA$', '^medICina$']  # Add more forms if needed

# Create a regular expression pattern
pattern = '|'.join(medicina_forms)

# Loop through each .parquet file
for file_path in parquet_files:
    # Read the file into a DataFrame
    df = pd.read_parquet(file_path)

    # Check if 'NO_CURSO' or 'NOMEDOCURSO' column exists
    if 'NO_CURSO' in df.columns:
        column_name = 'NO_CURSO'
    elif 'NOMEDOCURSO' in df.columns:
        column_name = 'NOMEDOCURSO'
    else:
        continue

    # Filter the DataFrame
    contains_medicina = df[column_name].str.contains(pattern, case=False, na=False)
    df_medicina = df[contains_medicina]

    # Save the filtered DataFrame to a new .parquet file
    new_file_path = file_path.replace('.parquet', '_med.parquet')
    df_medicina.to_parquet(new_file_path)