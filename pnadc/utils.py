import io
import os
import re
import chardet
import zipfile
import requests
from . import constants
from .settings import processing_years, layout_dir


def download_fixed_width_layout(output_dir=layout_dir):
    """
    Downloads the specific version of the input dictionary defined in constants.py.

    Args:
        output_dir (str): Directory where the file will be saved. Defaults to './data/data_cache'.
    
    Return:
        str: Complete path to the extracted .txt file
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    target_url = constants.LAYOUT_ZIP_URL
    print(f"Downloading input dictionary (Version {constants.LAYOUT_VERSION_DATE})...")
    print(f"Source: {target_url}")

    try:
        r = requests.get(target_url)
        r.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            input_files = [
                f for f in z.namelist() 
                if 'input' in f.lower() and 'trimestral' in f.lower() and f.endswith('.txt')
            ]
            
            if not input_files:
                raise FileNotFoundError(f".txt file not found in: {constants.LAYOUT_ZIP_URL}")
            
            target_file = input_files[0]
            z.extract(target_file, output_dir)
            
        final_path = os.path.join(output_dir, target_file)
        print(f"Input file ready: {final_path}")
        return final_path

    except Exception as e:
        print(f"Error: {e}")
        raise e

def detect_encoding(filepath):
    """
    Analyses the first bytes of a file in order to detect the encoding.
    Useful to IBGE files that may use Latin-1/ISO-8859-1.

    Args:
        filepath (str): Complete path to the .txt input file.
        
    Return:
        encoding (str): The detected encoding of the input file.
    """
    with open(filepath, 'rb') as f:
        raw_bytes = f.read(10000)
        result = chardet.detect(raw_bytes)
    return result['encoding']


def parse_layout_metadata(filepath, encoding):
    """
    Reads the script and returns the metadata to read the fixed-witdh file (FWF).

    Args:
        filepath (str): Complete path to the .txt layout file.
        encoding (str): The detected encoding of the layout file.
    
    Return:
        names (list of strs): List of the columns names.
        widths (list of ints): List of the columns widths.
        dtypes (dict): Dicitonary mapping {column: type} to optimize memory usage.
    """

    with open(filepath, encoding=encoding) as file:
        layout_content = file.read()
    
    names = []
    widths = []
    dtypes = {}
    
    # Regex Explained:
    # -----------------------------------
    # @\d+        -> Matches the position marker (e.g., @0001), but does not capture it.
    # \s+         -> Whitespace.
    # (\w+)       -> GROUP 1: The Variable Name (e.g., Ano, V1028001).
    # \s+         -> Spaces.
    # (\$?)       -> GROUP 2: The Dollar sign (optional). If present, it indicates a String.
    # (\d+)       -> GROUP 3: The Width (e.g., 4).
    # \.          -> The mandatory period (dot) in the txt.
    
    pattern = re.compile(r'@\d+\s+(\w+)\s+(\$?)(\d+)\.')

    for line in layout_content.splitlines():
        match = pattern.search(line)
        if match:
            var_name = match.group(1)
            is_string = match.group(2) == '$' # Se tiver cifrão, é True
            width = int(match.group(3))
            
            names.append(var_name)
            widths.append(width)
            
            # Memory optimization:
            # If there is an $, it is a string ("object" in pandas or "string" in pyarrow).
            # If not, it is set as float32 to economize memory.
            if is_string:
                dtypes[var_name] = "object"
            else:
                dtypes[var_name] = "float32"
            
    return names, widths, dtypes

def set_parquet_path(years=processing_years, base_dir='./data'):
    years_str = '_'.join(str(year) for year in years)
    return f"{base_dir}/pnadc_microdata_{years_str}.parquet"