# Module for testing finance logic functions


import json
from pathlib import Path
from finance_logic import calculate_budget

# Get the folder this file lives in
current_dir = Path(__file__).parent

# Build the path to the JSON file
json_path = current_dir / "test_inputs.json" 

with open(json_path, "r") as f:
    test_data = json.load(f)
    
tests = test_data['tests']

for test in tests:
    income = test['income']
    expenses = test['expenses']
    expected_budget = test['expected_budget']
    
    calculated_budget = calculate_budget(income, expenses)
    
    if calculated_budget != expected_budget:
        print(f"Test failed: expected {expected_budget}, got {calculated_budget}")
    else:
        print("Test passed")