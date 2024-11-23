# Function to read the API key from a local file
def read_api_key(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: API key file not found at {file_path}")
        exit()
    except Exception as e:
        print(f"Error reading API key: {e}")
        exit()