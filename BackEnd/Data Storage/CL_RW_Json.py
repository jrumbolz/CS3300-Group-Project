import os
import json
# Should write a modify json file method
class JSON_RW:
    #Return bool based on if path exists
    @staticmethod
    def path_exists(filename):
    
        return os.path.exists(filename)
	
    @staticmethod
    def write_json_file(filename,data):

        if JSON_RW.path_exists(filename):

            with open(filename, 'r', encoding='utf-8') as f:

                existing = json.load(f)

                if isinstance(existing,dict):

                    # Merges existing dict with new key pair

                    existing = existing | data

                    with open(filename, 'w', encoding='utf-8') as f:

                        json.dump(existing,f, indent = 4)

        else:

            existing = data

            with open(filename, 'w', encoding='utf-8') as f:

                json.dump(existing,f, indent = 4)
	
    @staticmethod

    def read_json_file(filename):

        if JSON_RW.path_exists(filename):

            with open(filename, 'r') as f:

                return json.load(f)
        else:

            return "File does not exist"

