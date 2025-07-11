import os

# --- Global Settings ---
NUM_LISTINGS = 1000
MODEL_NAME = 'all-MiniLM-L6-v2'
BATCH_SIZE = 32

# --- Path Definitions ---
# Source data
RAW_DATA_PATH = os.path.join("res", "data", "tc20171021.csv")
SAMPLE_DATA_PATH = os.path.join("res", "data", f"tc20171021_sample_{NUM_LISTINGS}.csv")

# Processed data files
PROCESSED_DIR = os.path.join("res", "data", "processed")
LISTINGS_PATH = os.path.join(PROCESSED_DIR, "listings.parquet")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
LISTING_IDS_PATH = os.path.join(PROCESSED_DIR, "listing_ids.npy")

# Frontend static files
STATIC_DIR = "static" 