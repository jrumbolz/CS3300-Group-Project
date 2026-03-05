import os
import json

class JSON_RW:

    @staticmethod
    def path_exists(filename):
    
        return os.path.exists(filename)
	
    @staticmethod
    def write_json_file(filename,data):

        if JSON_RW.path_exists(filename):

            with open(filename, 'r', encoding='utf-8') as f:

                existing = json.load(f)

                if isinstance(existing,list):

                    existing.append(data)
                
                else:

                    existing = [existing,data]

        else:

            existing = data

            with open(filename, 'w', encoding='utf-8') as f:

                json.dump(existing,f, indent = 4)
	
    @staticmethod

    def read_json_file(filename):

        with open(filename, 'r', encoding='utf-8') as f:

            return json.load(f)