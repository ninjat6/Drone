import json
import os

CONFIG_FILE = 'test_cases.json'

def load_test_cases():
    """
    Loads test cases from the JSON configuration file.

    Returns:
        list: A list of test case dictionaries.

    Raises:
        FileNotFoundError: If the config file is not found.
        ValueError: If the JSON is invalid or the 'test_cases' key is missing.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {CONFIG_FILE}: {e}")

    if 'test_cases' not in data or not isinstance(data['test_cases'], list):
        raise ValueError(f"Missing or invalid 'test_cases' list in {CONFIG_FILE}")

    return data['test_cases']

# Example of how to use it (for testing purposes)
if __name__ == '__main__':
    try:
        test_cases = load_test_cases()
        print(f"Successfully loaded {len(test_cases)} test cases.")
        # Print the first test case to verify
        if test_cases:
            print("First test case:")
            print(json.dumps(test_cases[0], indent=2, ensure_ascii=False))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
