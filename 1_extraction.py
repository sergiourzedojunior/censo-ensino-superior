import os
import zipfile
import re
from concurrent.futures import ThreadPoolExecutor
from unidecode import unidecode

def safe_filename(filename):
    """Normalize filenames to be lowercase, alphanumeric with underscores and dashes, removing accents."""
    # Transliterate to ASCII (removes accents)
    transliterated = unidecode(filename)
    # Remove spaces and convert to lowercase
    safe_name = transliterated.lower().replace(' ', '')
    # Remove non-alphanumeric characters except underscores and dashes
    safe_name = re.sub(r'[^a-z0-9_\-]', '', safe_name)
    return safe_name

def extract_zip(file_path, output_dir):
    """Extracts a ZIP file to a specified output directory."""
    # Normalize the base name of the zip file for directory creation
    base_name = safe_filename(os.path.splitext(os.path.basename(file_path))[0])
    specific_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(specific_output_dir, exist_ok=True)  # Ensure the subfolder exists or create it if not

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extract all files into the created subfolder
        zip_ref.extractall(specific_output_dir)

def main():
    root_dir = r"D:\OneDrive\censo ensino superior"  # Directory containing the ZIP files
    # List all zip files in the specified directory
    zip_files = [os.path.join(root_dir, file) for file in os.listdir(root_dir) if file.endswith('.zip')]

    # Extract all zip files concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(extract_zip, zip_files, [root_dir] * len(zip_files))

if __name__ == "__main__":
    main()  # Run the main function if this script is the main module
