import os
from pathlib import Path

def add_file(year, month):
    
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_DIR = "Data"
    #DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    path = os.path.join(f'{BASE_DIR}\{DATA_DIR}\{year}\{month}.json')
    print(path)
    
    if not os.path.isdir(path):
        os.makedirs(path)
        print("Folder created.")
    else:
        print("Folder already exists.")


add_file(2026, 'February')