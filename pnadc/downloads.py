# pnadc/download.py
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .constants import FTP_BASE_URL
from .settings import download_years, microdata_dir

def download_microdata(years=download_years, output_dir=microdata_dir):
    """
    Download the specified .zip microdata files of PNADC to the specified years.
    
    Args:
        years (list): List of years (ex: [2023, 2024]). If None, downloads the current year.
        output_dir (str): Directory to save the files.
    """
    if years is None:
        years = [2024] # Safe default
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    for year in years:
        year_url = f"{FTP_BASE_URL}/{year}/"
        print(f"\n--- Looking for data from: {year} ---")

        try:
            response = requests.get(year_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Catch only ZIPs
            links = [a.get('href') for a in soup.find_all('a') if a.get('href', '').endswith('.zip')]
            
            if not links:
                print(f"  No .zip file found in {year_url}")
                continue

            for file_name in links:
                file_url = urljoin(year_url, file_name)
                local_path = os.path.join(output_dir, file_name)
                
                # Check if the file already exists to not download it again
                if os.path.exists(local_path):
                    print(f"  File already exists: {file_name} (Skipping)")
                    continue

                print(f"  Downloading: {file_name} ...")
                
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    
                    with open(local_path, 'wb') as f:
                        downloaded_size = 0
                        last_print = 0
                        print_threshold = 1024 * 1024 * 10 # 10 MB
                        
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # Progress bar
                            if downloaded_size - last_print >= print_threshold:
                               print(".", end="", flush=True)
                               last_print = downloaded_size

                print(" OK!")

        except Exception as e:
            print(f"  Error while processing {year}: {e}")
