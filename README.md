# Data Processing and Analysis Pipeline for Censo Ensino Superior

This repository hosts a suite of Python scripts tailored for the processing and analysis of the Censo Ensino Superior dataset, with a specialized focus on medical education data. The scripts cover everything from data extraction and normalization to detailed analysis and predictions, culminating in a visualization dashboard using Streamlit.

## Project Structure

The project is divided into several scripts, each designed to perform specific tasks in the data processing pipeline:

### 1. **extraction.py**

Extracts ZIP files containing datasets into organized directories, ensuring filenames are safe and consistent across different operating systems.

**Key Functions:**
- `safe_filename()`: Normalizes filenames by making them lowercase and replacing spaces and special characters.
- `extract_zip()`: Extracts the contents of ZIP files into designated directories.

### 2. **normalize.py**

Renames files and directories to a uniform naming convention to avoid issues with different file systems or coding environments.

**Key Functions:**
- `normalize_name()`: Removes unwanted characters and spaces from filenames and directory names, preserving file extensions.
- `rename_entities()`: Applies `normalize_name` to all entities within the specified directory.

### 3. **convert_to_parquet.py**

Converts CSV files into the Parquet format for efficient data storage and access. This script handles various character encodings and uses different delimiters based on the dataset year.

**Key Functions:**
- `convert_csv_to_parquet()`: Detects the encoding of CSV files and converts them to Parquet format.
- `process_directory()`: Processes all CSV files within a specified directory.

### 4. **find_common_columns.py**

Identifies columns common across multiple datasets, which is crucial for consistent data analysis.

**Key Functions:**
- Script iterates through directories and identifies common columns across Parquet files.

### 5. **filter_medicine_courses.py**

Filters the dataset to focus solely on medical courses, facilitating targeted analyses in the field of medical education.

**Key Functions:**
- Filters data frames based on course names related to medicine and saves the refined dataset for further analysis.

### 6. **analysis.py**

Performs detailed data analysis, including descriptive statistics and future trend predictions using machine learning models.

**Key Functions:**
- Uses Prophet models to forecast future values based on historical data.
- Generates predictions and calculates errors such as MAE and MAPE.

## Streamlit Dashboard

A Streamlit dashboard provides a user-friendly interface to interact with the data analysis results. It allows users to visualize data trends and predictions dynamically.

### Streamlit Code Overview

The Streamlit scripts create interactive web applications that allow users to explore the data processed by the above scripts.

**Key Features Implemented in Streamlit:**
- **Data Caching**: Functions decorated with `@cache_data` to minimize reload times by caching loaded data.
- **Dynamic Graphs**: Uses Plotly to create interactive graphs that display historical data and predictions.
- **User Interactions**: Includes dropdowns and sliders allowing users to filter views according to specific parameters (e.g., year, region).

**Example Streamlit Function:**
```python
@cache_data
def load_data():
    return pd.read_csv("path_to_data.csv")

st.title('Censo Ensino Superior - Medicina')
df = load_data()
st.write(df)
```

## Installation and Setup

Ensure Python 3.x is installed and then install the required packages:

```bash
pip install pandas pyarrow unidecode chardet zipfile36 concurrent.futures streamlit plotly
```

To run the Streamlit dashboard:

```bash
streamlit run dashboard_script.py
```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

