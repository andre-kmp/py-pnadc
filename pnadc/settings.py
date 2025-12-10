COLUMNS_TO_KEEP = [
    'Ano', 'Trimestre', 'UF', 'UPA', 'V1008', 'V1014', 'V2003', # Chaves
    'V2007', 'V2009', 'V2010', 'VD3004', # Demografia
    'V1028', # Peso
    'V2001', # Pessoas no domicílio
    'VD4016', 'VD4017', 'VD4019', 'VD4020', # Rendimentos
    'V4029' # Carteira assinada
]

TARGET_YEARS_DOWNLOAD = [2023, 2024, 2025]

TARGET_YEARS_PROCESSING = [2024]

CHUNK_SIZE = 25000
