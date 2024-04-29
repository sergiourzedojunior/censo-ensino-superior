import os
import re
from unidecode import unidecode
import chardet  # For detecting character encoding

def normalize_name(name, is_file=False):
    """Normalize names by removing spaces, converting to lowercase, and removing special characters, preserving file extensions."""
    if is_file:
        # Split the name and extension
        base_name, ext = os.path.splitext(name)
        name = base_name
    else:
        ext = ''

    try:
        # Attempt to detect encoding and decode accordingly
        detected_encoding = chardet.detect(name.encode())['encoding']
        if detected_encoding:
            name = name.encode(detected_encoding).decode('utf-8')
    except UnicodeDecodeError:
        # Fallback to transliteration when decoding fails
        name = unidecode(name)
    except UnicodeEncodeError:
        # Fallback to UTF-8 when encoding fails
        name = name.encode('utf-8', 'ignore').decode('utf-8')

    # Transliterate to ASCII, remove accents
    name = unidecode(name)
    # Remove spaces and convert to lowercase
    name = name.lower().replace(' ', '')
    # Remove non-alphanumeric characters except dashes and underscores
    name = re.sub(r'[^a-z0-9_\-]', '', name)

    # Reattach the extension for files
    if is_file:
        name += ext  # Add back the original extension

    return name

def rename_entities(root_dir):
    """Walk through the directory structure and rename files and directories as necessary."""
    for subdir, dirs, files in os.walk(root_dir, topdown=False):
        # Rename files
        for file_name in files:
            # Skip temporary files if needed
            if file_name.startswith('~$'):
                continue
            normalized_file_name = normalize_name(file_name, is_file=True)
            if file_name != normalized_file_name:
                original_file_path = os.path.join(subdir, file_name)
                new_file_path = os.path.join(subdir, normalized_file_name)
                if not os.path.exists(new_file_path):
                    os.rename(original_file_path, new_file_path)
                    print(f"Renamed file '{original_file_path}' to '{new_file_path}'")
                else:
                    print(f"Cannot rename file '{original_file_path}' to '{new_file_path}' because the target already exists")

        # Rename directories
        for dir_name in dirs:
            normalized_dir_name = normalize_name(dir_name)
            if dir_name != normalized_dir_name:
                original_dir_path = os.path.join(subdir, dir_name)
                new_dir_path = os.path.join(subdir, normalized_dir_name)
                if not os.path.exists(new_dir_path):
                    os.rename(original_dir_path, new_dir_path)
                    print(f"Renamed directory '{original_dir_path}' to '{new_dir_path}'")
                else:
                    print(f"Cannot rename directory '{original_dir_path}' to '{new_dir_path}' because the target already exists")

def main():
    root_dir = r"D:\OneDrive\censo ensino superior"
    rename_entities(root_dir)

if __name__ == "__main__":
    main()
