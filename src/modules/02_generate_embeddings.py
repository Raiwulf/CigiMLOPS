import pandas as pd
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer
import torch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import config

def generate_embeddings():
    """
    Generates and saves embeddings for all car listings.
    """
    print("Starting embedding generation...")
    
    # --- 1. Load Data ---
    if not os.path.exists(config.LISTINGS_PATH):
        print(f"Error: Cleaned listings file not found at {config.LISTINGS_PATH}")
        print("Please run src/prepare_data.py first.")
        return
        
    print("Loading cleaned listings...")
    listings_df = pd.read_parquet(config.LISTINGS_PATH)

    # --- 2. Initialize Model ---
    # Check if a GPU is available and use it
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load the pre-trained sentence transformer model
    # The model will be downloaded from the internet on first run
    print(f"Loading model '{config.MODEL_NAME}'...")
    model = SentenceTransformer(config.MODEL_NAME, device=device)

    # --- 3. Create Descriptive Sentences ---
    print("Creating descriptive sentences for each listing...")
    
    # Combine relevant features into a single descriptive string for each car
    descriptions = (
        listings_df['Year'].astype(str) + " " +
        listings_df['Make'] + " " +
        listings_df['Model'] + " from " +
        listings_df['State'] + " with " +
        listings_df['Mileage'].astype(str) + " miles"
    ).tolist()

    # --- 4. Generate Embeddings ---
    print(f"Generating embeddings for {len(descriptions)} listings... (This may take a while)")
    
    # Use the model's encode function, which is highly optimized
    embeddings = model.encode(descriptions, batch_size=config.BATCH_SIZE, show_progress_bar=True)
    
    # --- 5. Save Embeddings and IDs ---
    print("Saving embeddings and corresponding listing IDs...")
    
    try:
        # Save the embeddings array to a .npy file
        np.save(config.EMBEDDINGS_PATH, embeddings)
        
        # Save the listing IDs to a separate .npy file
        # Use .to_numpy() to ensure it's a NumPy array for type safety
        listing_ids = listings_df['Id'].to_numpy()
        np.save(config.LISTING_IDS_PATH, listing_ids)
        
        print(f"Successfully saved embeddings to: {config.EMBEDDINGS_PATH}")
        print(f"Successfully saved listing IDs to: {config.LISTING_IDS_PATH}")

    except Exception as e:
        print(f"An error occurred while saving files: {e}")


if __name__ == "__main__":
    generate_embeddings() 