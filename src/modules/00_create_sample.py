import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import config

def create_sample_file():
    """
    Creates a small sample CSV file from the large raw data file.
    """
    print(f"Creating a sample file with {config.NUM_LISTINGS} listings...")
    
    if not os.path.exists(config.RAW_DATA_PATH):
        print(f"Error: Raw data file not found at {config.RAW_DATA_PATH}")
        return

    try:
        with open(config.RAW_DATA_PATH, 'r', encoding='utf-8') as f_in:
            with open(config.SAMPLE_DATA_PATH, 'w', encoding='utf-8') as f_out:
                # Copy the header
                header = f_in.readline()
                f_out.write(header)
                # Copy the first N data rows
                for i in range(config.NUM_LISTINGS):
                    line = f_in.readline()
                    f_out.write(line)
        
        print(f"Successfully created sample file at: {config.SAMPLE_DATA_PATH}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_sample_file() 