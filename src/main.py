import pandas as pd
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer, util
import torch
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import config

# --- FastAPI App Initialization ---
app = FastAPI()
app.mount(f"/{config.STATIC_DIR}", StaticFiles(directory=config.STATIC_DIR), name="static")

# --- Load Model and Data at startup ---
# This dictionary will hold our loaded models and data
ml_models = {}

@app.on_event("startup")
async def startup_event():
    """
    Load all ML models and data into memory on server startup.
    """
    print("Loading ML model and data...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    ml_models['model'] = SentenceTransformer(config.MODEL_NAME, device=device)
    ml_models['embeddings'] = np.load(config.EMBEDDINGS_PATH)
    ml_models['listing_ids'] = np.load(config.LISTING_IDS_PATH)
    # Load the original sample CSV for the listings view
    ml_models['listings_df'] = pd.read_csv(config.SAMPLE_DATA_PATH)
    print("ML model and data loaded successfully.")

# --- Pydantic Models for Request Body ---
class SearchRequest(BaseModel):
    prompt: str

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(config.STATIC_DIR, "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/listings")
async def get_listings():
    """
    Returns the list of all cars from the sample CSV.
    """
    listings = ml_models.get('listings_df')
    if listings is None:
        return JSONResponse(content={"error": "Listings not loaded"}, status_code=500)
    return JSONResponse(content=listings.to_dict(orient='records'))

@app.post("/search")
async def search(request: SearchRequest):
    """
    Performs semantic search based on the user's prompt.
    """
    # --- Start of new, more robust checks ---
    prompt = request.prompt
    if not prompt:
        return JSONResponse(content={"error": "Prompt cannot be empty"}, status_code=400)

    model = ml_models.get('model')
    if model is None:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    embeddings = ml_models.get('embeddings')
    if embeddings is None:
        return JSONResponse(content={"error": "Embeddings not loaded"}, status_code=500)
    
    listing_ids = ml_models.get('listing_ids')
    if listing_ids is None:
        return JSONResponse(content={"error": "Listing IDs not loaded"}, status_code=500)

    listings_df_full = ml_models.get('listings_df')
    if listings_df_full is None:
        return JSONResponse(content={"error": "Listings data not loaded"}, status_code=500)
    # --- End of new checks ---

    # --- Search Logic ---
    prompt = request.prompt
    model = ml_models['model']
    embeddings = ml_models['embeddings']
    listing_ids = ml_models['listing_ids']
    listings_df_full = ml_models['listings_df']

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    cosine_scores = util.cos_sim(prompt_embedding, embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(10, len(cosine_scores)))

    # --- Format Results ---
    results = []
    listings_df = listings_df_full.set_index('Id')
    for score, idx in zip(top_results[0], top_results[1]):
        listing_id = listing_ids[idx]
        try:
            car_info = listings_df.loc[listing_id]
            car_desc = f"{int(car_info.Year)} {car_info.Make} {car_info.Model} ({int(car_info.Mileage)} miles)"
            
            results.append({
                'listing_id': int(listing_id),
                'description': car_desc,
                'match_percentage': score.item() * 100
            })
        except KeyError:
            # This can happen if the listings.parquet and listing_ids get out of sync
            print(f"Warning: Listing ID {listing_id} found in embeddings but not in listings data.")
            continue

    # --- NEW: Generate Chatbot Response ---
    response_text = ""
    if not results:
        response_text = f"I'm sorry, I couldn't find any listings that closely match '{prompt}'. Please try a different search."
    else:
        top_score = results[0]['match_percentage']
        if top_score > 35: # Arbitrary threshold for a "good" match
            response_text = f"Excellent! Based on your request for '{prompt}', I found some great options. Here are the top results:"
        elif top_score > 25:
            response_text = f"Based on '{prompt}', I found a few possibilities that might be a good fit. Take a look:"
        else:
            response_text = f"I couldn't find a very close match for '{prompt}', but here are the most similar listings I have:"

    # --- NEW: Return Structured Response ---
    return JSONResponse(content={
        "response_text": response_text,
        "results": results
    })

# To run the app:
# pdm run uvicorn src.main:app --reload 