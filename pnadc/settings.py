columns_to_keep = [
    'Ano', 'Trimestre', 'UF', 'UPA', 'V1008', 'V1014', 'V2003', # Chaves
    'V2007', 'V2009', 'V2010', 'VD3004', # Demografia
    'V1028', # Peso
    'V2001', # Pessoas no domicílio
    'VD4016', 'VD4017', 'VD4019', 'VD4020', # Rendimentos
    'V4029' # Carteira assinada
]

download_years = [2023, 2024, 2025]

processing_years = [2024, 2025]

chunk_size = 25000

microdata_dir = './data/pnadc_microdata'

layout_dir = './data/cache/'