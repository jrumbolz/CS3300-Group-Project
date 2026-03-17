from CL_RW_Json import JSON_RW
import os
#Right now just checking if JSON_RW is working. will also add logic for creating file system or traversing it.
def DataHandler(year,month,mode,data):

    # Creates file path from script to year data directory requested

    abs_path = os.path.abspath(__file__)

    path = os.path.dirname(abs_path)

    dir_path = os.path.join(path,year)

    month_file = month + ".json"

    # Full path has both the year dir and the month json file

    full_path = os.path.join(dir_path,month_file)

    # If the directory does not exist then it creates that years directory
    if not os.path.exists(dir_path):

        os.mkdir(dir_path)

        print("Creating a new year dir")
    
    # Read json and return contents
    if(mode == "read"):

        return JSON_RW.read_json_file(full_path)

    # Append new key-pair to json
    elif(mode == 'append'):

        JSON_RW.write_json_file(full_path,data)
        
        return 
    # TO-DO modify json keypair or maybe access IDK maybe not depends on how data is given


if __name__ == "__main__":
    year = input("year: ")

    month = input("month: ")

    data = {"income" : 20000}

    print(DataHandler(year,month,"append",data))

