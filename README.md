# py-pnadc: Unofficial Python Package for PNADcIBGE

🇺🇸 [English](#us-english)  / 🇧🇷 [Português](#brazil-português)

## :us: English

### About this package
**py-pnadc** is a Python package containing tools for downloading and reading the microdata from the **Continuous National Household Sample Survey (PNAD Contínua)** from Brazilian Institute of Geography and Statistics (IBGE). 

This package solves common issues related to handling large PNADC files by streaming data in stream and converting it directly to .parquet.

It provides a pythonic alternative to the [R official package](https://github.com/Gabriel-Assuncao/PNADcIBGE).

### Main funcionalities

- Analytics-ready: Converts the Fixed-Width-Files (FWF) files direct to .parquet.
- Low RAM consumption: Processes data in chunks, enabling execution in regular notebooks.
- Automatic ETL: Manages downloading, layout parsing and convertion in a single command.

### Installation / Instalação

#### Development mode (local)
To install the package locally to download and read the microdata:

```bash
git clone https://github.com/andre-kmp/py-pnadc.git
cd py-pnadc
pip install .
```

### How to use it

#### Running the main function

```python
import pnadc

# This will:
# 1. Download the layout and the microdata (if they don't exist yet)
# 2. Convert to .parquet
# 3. Return a pandas dataframe with the selected columns
df = pnadc.load_microdata()

print(df.head())
```

#### Setting parameters

You may override the package defaults by passing arguments directly to the `load_microdata` function.

* **columns_to_keep**: List of columns (IBGE codes) to keep.
* **load_years**: List of years to process (e.g.: `['2023', '2024']`).
* **chunk_size**: Number of rows per batch in memory (reduce it for low RAM environments). Default is 25,000.

Usage example:

```python
import pnadc

# 1. Setting preferences
my_columns = ['UF', 'V2007', 'V2009', 'VD4001', 'VD4002']
target_years = ['2023', '2024']

# 2. Loading data with custom arguments
df = pnadc.load_microdata(
    columns_to_keep=my_columns,
    load_years=target_years,
    chunk_size=10000
)

print(f"Loaded data: {df.shape}")
print(df.head())
```

### :warning:  Disclaimer
This is an unofficial project and is not affiliated with IBGE.

## :brazil: Português

### Sobre este pacote
**py-pnadc** é um pacote Python com ferramentas para baixar e ler os microdados da **Pesquisa Nacional de Domicílios Contínua (PNADC)** do Instituto Brasileiro de Geografia e Estatística (IBGE).

Esse pacote resolve os problemas comuns ao lidar com os arquivos de texto gigantes da PNADC, processando os dados em stream e convertendo-os para .parquet.

É uma alternativa pythonica ao [pacote oficial em R](https://github.com/Gabriel-Assuncao/PNADcIBGE).

### Principais funcionalidades

- Eficiente para análises: Converte os arquivos de largura fixa (FWF) diretamente para .parquet.
- Baixo consumo de RAM: Processa os dados em chunks, o que permite rodar em notebooks comuns.
- ETL automático: Gerencia o download, leitura do layout e conversão em um único comando.

### Instalação

#### Modo de desenvolvedor (local)

Para instalar o pacote localmente para baixar e ler os microdados:

```bash
git clone https://github.com/andre-kmp/py-pnadc.git
cd py-pnadc
pip install .
```

### Como usar

#### Rodando a função principal

```python
import pnadc

# Isso irá:
# 1. Baixar o dicionário e os dados (se ainda não existirem)
# 2. Converter para Parquet
# 3. Retornar um pandas DataFrame com as colunas selecionadas
df = pnadc.load_microdata()

print(df.head())
```

#### Configurando os parâmetros

Você pode sobrescrever os padrões do pacote passando argumentos diretamente para a função `load_microdata`:

* **columns_to_keep**: Lista de colunas (códigos do IBGE) para manter.
* **load_years**: Lista de anos a serem processados (ex: `['2023', '2024']`).
* **chunk_size**: Número de linhas por lote na memória (diminua se tiver pouca RAM). Por default, 25000.

Exemplo de uso:

```python
import pnadc

# 1. Definindo suas preferências
minhas_colunas = ['UF', 'V2007', 'V2009', 'VD4001', 'VD4002']
anos_alvo = ['2023', '2024']

# 2. Carregando os dados com os seus argumentos
df = pnadc.load_microdata(
    columns_to_keep=minhas_colunas,
    load_years=anos_alvo,
    chunk_size=10000
)

print(f"Dados carregados: {df.shape}")
print(df.head())
```

## :warning: Isenção de responsabilidade

Este é um projeto não-oficial e não possui afiliação com o IBGE.
