import pandas as pd
import os

# Specify the paths to your directories
dir_paths = [
    r"D:\OneDrive\censo ensino superior\microdados_censo_da_educacao_superior_2007\microdadosdocensodaeducacosuperior2007\DADOS",
    r"D:\OneDrive\censo ensino superior\microdados_censo_da_educacao_superior_2008\microdadosdocensodaeducacosuperior2008\DADOS"
]

# Define the various forms of 'medicina'
medicina_forms = ['^medicina$', '^Medicina$', '^MEDICINA$', '^medICina$']  # Add more forms if needed

# Create a regular expression pattern
pattern = '|'.join(medicina_forms)

# Loop through each directory
for dir_path in dir_paths:
    # Get a list of all .parquet files in the directory
    parquet_files = [os.path.join(root, file) for root, dirs, files in os.walk(dir_path) for file in files if file.endswith('.parquet')]

    # Loop through each .parquet file
    for file_path in parquet_files:
        # Read the file into a DataFrame
        df = pd.read_parquet(file_path)

        # Check if 'NO_CURSO', 'NOMEDOCURSO' or 'NOME_CURSO' column exists
        if 'NO_CURSO' in df.columns:
            column_name = 'NO_CURSO'
        elif 'NOMEDOCURSO' in df.columns:
            column_name = 'NOMEDOCURSO'
        elif 'NOME_CURSO' in df.columns:
            column_name = 'NOME_CURSO'
        else:
            continue

        # Filter the DataFrame
        contains_medicina = df[column_name].str.contains(pattern, case=False, na=False)
        df_medicina = df[contains_medicina]

        # Save the filtered DataFrame to a new .parquet file
        new_file_path = file_path.replace('.parquet', '_med.parquet')
        df_medicina.to_parquet(new_file_path)