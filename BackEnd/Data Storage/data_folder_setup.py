import os


path = '\MoneyMentor\Data'
main_file = os.path.join(os.getcwd() , path)
# Create the folder and any necessary parent folders.
# exist_ok=True prevents an error if the folder already exists.
#os.makedirs(folder_path, exist_ok=True)

#print(f"Folder '{folder_path}' ensured to exist.")
print(main_file)