import pandas as pd
from . import constants, settings, utils, downloads, processing
from .settings import columns_to_keep

def load_microdata(columns_to_keep=columns_to_keep):
    layout_pnadc_path = utils.download_fixed_width_layout()
    layout_pnadc_encoding = utils.detect_encoding(layout_pnadc_path)

    downloads.download_microdata()
    parquet_path = utils.set_parquet_path()
    final_parquet_file = processing.txt_to_parquet(output_path=parquet_path, layout_path=layout_pnadc_path)

    reduced_df = pd.read_parquet(
        final_parquet_file, 
        engine='fastparquet', 
        columns=columns_to_keep
    )
    
    return reduced_df
