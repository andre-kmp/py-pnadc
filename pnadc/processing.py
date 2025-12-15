# pnadc/processing.py
import os
import zipfile
import pandas as pd
from . import utils
from .settings import chunk_size, microdata_dir, processing_years

def txt_to_parquet(data_dir=microdata_dir, output_path=None, layout_path=None, chunk_size=chunk_size, years=processing_years):
    """
    Reads all .zip files in the directory, converts to .parquet, and consolidates into a single file.

    The reading is done via direct stream from the zip, without extracting the data to disk.

    Args:
        data_dir (str): Directory containing the PNADc .zip files.
        output_path (str): Complete path for the output .parquet file.
        layout_path (str): Path to the fixed column width dictionary file (.txt).
        chunk_size (int): Number of rows processed per chunk in memory.
    """
    # 1. Get metadata (names, widths and dtypes)
    print("Reading metadata from the input file...")

    if layout_path is None:
        raise ValueError(
            "layout_path is required. "
            "Run download_fixed_width_layout() first or pass an existing layout file."
        )

    encoding_input = utils.detect_encoding(layout_path)
    names, widths, dtypes = utils.parse_layout_metadata(layout_path, encoding=encoding_input)

    # 2. Prepare years filter
    if years is not None and isinstance(years, (int, str)):
        years = [years]

    # 3. List .zip files
    zip_files = sorted([
        os.path.join(data_dir, f) 
        for f in os.listdir(data_dir) 
        if f.endswith('.zip') and f.startswith('PNADC_')
        and (years is None or any(str(year) in f for year in years))
    ])
    
    if not zip_files:
        print(f"No zip file found matching years: {years}.")
        return

    # If restarting, remove the old file to avoid duplication
    if os.path.exists(output_path):
        print(f"Removing old file: {output_path}")
        os.remove(output_path)

    # 4. Processing
    for zip_path in zip_files:
        print(f"\nProcessing: {os.path.basename(zip_path)}")
        
        with zipfile.ZipFile(zip_path, 'r') as z:
            txt_name = [f for f in z.namelist() if f.endswith('.txt')][0]

            with z.open(txt_name) as f:
                # Chunks iterator
                reader = pd.read_fwf(
                    f,
                    names=names,
                    widths=widths,
                    dtype=dtypes,
                    encoding=encoding_input,
                    chunksize=chunk_size,
                    header=None
                )

                for i, chunk in enumerate(reader):
                    # Append mode: if file exists, append=True
                    append_mode = os.path.exists(output_path)
                    text_cols = chunk.select_dtypes(include=['object']).columns
                    chunk[text_cols] = chunk[text_cols].astype(str)
            
                    chunk.to_parquet(
                        output_path,
                        engine='fastparquet',
                        index=False,
                        append=append_mode
                    )


    print(f"\nFinished! File saved in: {output_path}")
    return output_path


def create_unique_keys(df):
    """
    Creates the unique identification keys for Domicile (ID_DO) and Person (ID_PE).
    ID_DO: Combines UPA + V1008 + V1014.
    ID_PE: Combines UPA + V1008 + V1014 + V2003.
    """
    
    df = df.copy()
    
    cols_keys = ['UPA', 'V1008', 'V1014', 'V2003']
    for col in cols_keys:
       df[col] = df[col].astype(int).astype(str)

    df['ID_DO'] = df['UPA'] + df['V1008'] + df['V1014']
    df['ID_PE'] = df['ID_DO'] + df['V2003']
    
    return df
