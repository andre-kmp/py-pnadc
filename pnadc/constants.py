FTP_BASE_URL = "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados"

DOC_BASE_URL = f"{FTP_BASE_URL}/Documentacao"

# TODO: Criar função para descobrir qual o arquivo mais recente automaticamente
LAYOUT_VERSION_DATE = "20221031"

LAYOUT_ZIP_URL = f"{DOC_BASE_URL}/Dicionario_e_input_{LAYOUT_VERSION_DATE}.zip"
