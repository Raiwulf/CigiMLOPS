import pandas as pd
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import config

def prepare_data(raw_path):
    """
    Loads and cleans the raw data, saving it as a single file.
    """
    print(f"Loading raw data from: {raw_path}")
    
    # Use the robust settings we found during EDA
    try:
        df = pd.read_csv(raw_path, engine='python', on_bad_lines='skip')
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    # --- 1. Data Cleaning ---
    print("Cleaning data...")
    
    # Drop only the Vin column, we need the Id as a listing identifier
    df_cleaned = df.drop(columns=['Vin'])

    # Remove clear outliers and data errors by creating a new, filtered DataFrame
    # Chaining conditions before the .copy() can make the type clearer for linters
    df_cleaned = df_cleaned[(df_cleaned['Year'] <= 2017) & (df_cleaned['Mileage'] < 1000000)].copy()

    # For this example, we'll drop rows with any remaining missing values, if any.
    # Reassigning is better practice than using inplace=True
    df_cleaned = df_cleaned.dropna()

    print(f"Data shape after cleaning: {df_cleaned.shape}")

    # --- 2. Save Processed Data ---
    print("Saving processed data...")
    
    # Ensure the output directory exists
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    
    try:
        df_cleaned.to_parquet(config.LISTINGS_PATH, index=False)
        print(f"Successfully saved cleaned listings to: {config.LISTINGS_PATH}")
    except Exception as e:
        print(f"Failed to save data: {e}")

if __name__ == "__main__":
    # By default, the pipeline uses the generated sample file
    prepare_data(config.SAMPLE_DATA_PATH) 