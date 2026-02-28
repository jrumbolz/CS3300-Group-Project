import os


folder_path = 'C:\Users\Jedidiah Rumbolz\OneDrive - University of Colorado Colorado Springs\Desktop\MoneyMentor\Data'

# Create the folder and any necessary parent folders.
# exist_ok=True prevents an error if the folder already exists.
os.makedirs(folder_path, exist_ok=True)

print(f"Folder '{folder_path}' ensured to exist.")