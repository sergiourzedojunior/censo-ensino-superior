import os
import pandas as pd

# Base directory
base_dir = "D:\\OneDrive\\censo ensino superior"

# Initialize a dictionary for the common columns
common_columns = {}

# Iterate over the directories
for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    
    # Check if the directory exists
    if os.path.isdir(subdir_path):
        # Iterate over the subdirectories
        for subsubdir in os.listdir(subdir_path):
            subsubdir_path = os.path.join(subdir_path, subsubdir, "DADOS")

            # Check if the subsubdirectory exists
            if os.path.isdir(subsubdir_path):
                # Initialize a set for the columns of this directory
                dir_columns = set()

                # Get all parquet files in the directory
                parquet_files = [f for f in os.listdir(subsubdir_path) if f.endswith('.parquet')]

                # Process each parquet file
                for file_name in parquet_files:
                    # Construct the full file path
                    file_path = os.path.join(subsubdir_path, file_name)

                    # Read the parquet file
                    df = pd.read_parquet(file_path)

                    # If this is the first file, initialize the dir_columns set
                    if not dir_columns:
                        dir_columns = set(df.columns)
                    else:
                        # Intersect the dir_columns set with the columns of this file
                        dir_columns &= set(df.columns)

                # Store the common columns for this directory
                common_columns[subsubdir] = dir_columns

# Print the common columns for each directory
for subdir, columns in common_columns.items():
    print(f"Subdirectory: {subdir}, Common Columns: {columns}")