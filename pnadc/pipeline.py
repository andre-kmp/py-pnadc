import pandas as pd
from . import constants, settings, utils, downloads, processing
from .settings import columns_to_keep, processing_years, chunk_size

def load_microdata(columns_to_keep=columns_to_keep, load_years=processing_years, chunk_size=chunk_size):
    """
    Loads the PNADc microdata into a reduced DataFrame.

    Args:
        columns_to_keep (list): List of columns to retain in the final DataFrame. If None, uses settings.columns_to_keep.
        load_years (list): List of years to load data for. If None, loads the years specified in settings.processing_years.
        chunk_size (int): Number of rows to process per chunk. If None, loads the chunk size specified in settings.chunk_size.

    Returns:
        pd.DataFrame: DataFrame containing the reduced PNADc microdata.
    """

    layout_pnadc_path = utils.download_fixed_width_layout()

    downloads.download_microdata(years=load_years)
    parquet_path = utils.set_parquet_path()
    final_parquet_file = processing.txt_to_parquet(output_path=parquet_path, 
                                                   layout_path=layout_pnadc_path, 
                                                   chunk_size=chunk_size,
                                                   years=load_years)

    reduced_df = pd.read_parquet(
        final_parquet_file, 
        engine='fastparquet', 
        columns=columns_to_keep
    )
    
    return reduced_df
