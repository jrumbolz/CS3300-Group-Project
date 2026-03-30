# This file contains a class and methods to validate the structure and data in a json file
# It checks for the existence of the specified files, validates their json structure, and ensures they contain expected fields.
# Import the class as an object to use the methods in other files, I provided an example below

# ---- Usage Example ----
#
# from file_check import FileValidator
#
# result = FileValidator.check_data_integrity("../Data Storage", ["categories.json", "goals.json"])
# print(f"Valid: {result['is_valid']}")
# for msg in result['messages']:
#     print(f"  {msg}")



import os
import json


class FileValidator:
    
    @staticmethod
    def load_json_file(filepath):
        # Load in the file and return a bool for success and a data/error message
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return True, data
        except FileNotFoundError:
            return False, f"File not found: {filepath}"
        except json.JSONDecodeError:
            return False, f"Invalid JSON in: {filepath}"
        except Exception as e:
            return False, f"Error reading {filepath}: {str(e)}"
    
    @staticmethod
    def validate_json_structure(filepath, expected_fields=None, expected_type='dict'):
        # Args:
        #    filepath (str): Path to json file
        #    expected_fields (list): List of required field names (for dicts)
        #    expected_type (str): Expected root type: 'dict', 'list', or 'any'
        
        # Check if file exists
        if not os.path.exists(filepath):
            return False, f"File does not exist: {filepath}"
        
        # Try to load and parse json
        success, result = FileValidator.load_json_file(filepath)
        if not success:
            return False, result  # result is error message
        
        data = result
        
        # Check expected type
        if expected_type == 'dict' and not isinstance(data, dict):
            return False, f"Expected dict in {filepath}, got {type(data).__name__}"
        elif expected_type == 'list' and not isinstance(data, list):
            return False, f"Expected list in {filepath}, got {type(data).__name__}"
        
        # Check for required fields
        if expected_fields and isinstance(data, dict):
            missing_fields = [field for field in expected_fields if field not in data]
            if missing_fields:
                return False, f"Missing fields in {filepath}: {', '.join(missing_fields)}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_categories_file(categories_path):
        # Args:
        #    categories_path (str): Path to categories.json 
       
        if not os.path.exists(categories_path):
            return False, "File does not exist: categories.json"
        
        success, result = FileValidator.load_json_file(categories_path)
        if not success:
            return False, result
        
        data = result
        
        # Expected: list of category strings
        if not isinstance(data, list):
            return False, f"categories.json should be a list, got {type(data).__name__}"
        
        # Optionally check each item is a string
        for i, item in enumerate(data):
            if not isinstance(item, str):
                return False, f"categories.json[{i}] should be string, got {type(item).__name__}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_goals_file(goals_path):
        # Args:
        #    goals_path (str): Path to goals.json
        
        if not os.path.exists(goals_path):
            return False, "File does not exist: goals.json"
        
        success, result = FileValidator.load_json_file(goals_path)
        if not success:
            return False, result
        
        data = result
        
        # Expected: list (may be empty)
        if not isinstance(data, list):
            return False, f"goals.json should be a list, got {type(data).__name__}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_monthly_file(monthly_path):
        # Args:
        #    monthly_path (str): Path to monthly JSON file
        
        if not os.path.exists(monthly_path):
            return False, f"File does not exist: {os.path.basename(monthly_path)}"
        
        success, result = FileValidator.load_json_file(monthly_path)
        if not success:
            return False, result
        
        data = result
        
        # Expected: dict for financial data
        if not isinstance(data, dict):
            return False, f"{os.path.basename(monthly_path)} should be a dict, got {type(data).__name__}"
        
        return True, "Valid"
    
    @staticmethod
    def check_data_integrity(data_root_path, file_targets=None):
        # Validate the list of files that should be checked
        #
        # Args:
        #    data_root_path (str): Path to data storage directory
        #    file_targets (list): Required. Can contain:
        #       - str: relative file path (e.g., "categories.json", "2025/March.json")
        #       - dict: {"path": "relative/path.json", "expected_type": "dict|list|any", "expected_fields": [...]} for additional checks
        #
        # Returns:
        #     dict: {
        #         'is_valid': bool,
        #         'messages': [list of validation messages],
        #         'summary': str
        #     }

        results = []
        base_path = os.path.abspath(data_root_path)

        if not os.path.exists(base_path):
            return {
                'is_valid': False,
                'messages': [f"Data directory does not exist: {base_path}"],
                'summary': "Invalid"
            }

        if not file_targets:
            return {
                'is_valid': True,
                'messages': ["No files provided to check."],
                'summary': "No checks performed"
            }

        for entry in file_targets:
            if isinstance(entry, str):
                candidate_path = os.path.join(base_path, entry)
                valid, msg = FileValidator.validate_json_structure(candidate_path, expected_type='any')
                results.append({"file": entry, "valid": valid, "message": msg})
                continue

            if isinstance(entry, dict):
                rel_path = entry.get("path")
                expected_type = entry.get("expected_type", "any")
                expected_fields = entry.get("expected_fields")

                if not rel_path:
                    results.append({"file": str(entry), "valid": False, "message": "Missing 'path' in file target"})
                    continue

                candidate_path = os.path.join(base_path, rel_path)
                valid, msg = FileValidator.validate_json_structure(candidate_path, expected_fields=expected_fields, expected_type=expected_type)
                results.append({"file": rel_path, "valid": valid, "message": msg})
                continue

            results.append({"file": str(entry), "valid": False, "message": "Invalid file target format"})

        all_valid = all(r['valid'] for r in results)
        messages = [f"{r['file']}: {r['message']}" for r in results]

        return {
            'is_valid': all_valid,
            'messages': messages,
            'summary': "All files valid" if all_valid else "Some files are invalid"
        }
