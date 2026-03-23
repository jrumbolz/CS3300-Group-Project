import os
from pathlib import Path


#main
class installer:

    def __init__(self, dir, foldername, filename, filetype):
        self.dir = dir,
        self.foldername = foldername,
        self.filename = filename,
        self.filetype = filetype
    
    def install_folder(self):
        directory_path = Path(self.dir)

        if directory_path.is_dir():
            print(f"The directory '{directory_path}' exists.")
        else:
            print(f"The directory '{directory_path}' does not exist or is a file.")
            os.makedirs(f'{self.dir}{self.foldername}')

    def install_folder(self):
            directory_path = Path(self.dir)

            if directory_path.is_dir():
                print(f"The directory '{directory_path}' exists.")
            else:
                print(f"The directory '{directory_path}' does not exist or is a file.")
                os.makedirs(f'{self.dir}{self.filename}')