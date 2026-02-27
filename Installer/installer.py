import os
from pathlib import Path


#main

appname = 'Money Mentor'
directory_path = Path(f'C:\{appname}')

if directory_path.is_dir():
    print(f"The directory '{directory_path}' exists.")
else:
    print(f"The directory '{directory_path}' does not exist or is a file.")
    os.makedirs(f'C:\{appname}')
