# Dream Car Finder: A Semantic Search MLOps Project

This project is a complete, end-to-end web application that allows users to find used car listings using natural language. It serves as a practical introduction to MLOps principles, including data processing, model inference, and building an interactive API.

The application uses a powerful `sentence-transformer` model to understand the *meaning* behind a user's prompt (e.g., "a reliable truck for work") and find the most relevant cars from a dataset, even if the keywords don't match exactly.

## Features

- **Semantic Search Engine:** Go beyond simple keyword matching to understand user intent.
- **Conversational UI:** Delivers search results with a friendly, chatbot-like message.
- **Modern Web Stack:** Built with a FastAPI backend and a vanilla HTML, CSS, and JavaScript frontend.
- **Reproducible ML Pipeline:** Contains separate, runnable scripts for each stage of the MLOps lifecycle.
- **Centralized Configuration:** All important settings (like file paths and model parameters) are in one place.
- **Dependency Management:** Uses `pdm` for clear and isolated dependency management.

## Project Structure

The project is organized into distinct modules, following common software engineering and MLOps best practices:

```
CigiMLOPS/
├── res/
│   └── data/
│       ├── tc20171021.csv          # (Required) The original large dataset of car listings.
│       ├── tc20171021_sample.csv   # The 100-listing sample file for development.
│       └── processed/
│           ├── listings.parquet    # Cleaned, processed car data.
│           ├── embeddings.npy      # Semantic embeddings for each car.
│           └── listing_ids.npy     # Corresponding IDs for the embeddings.
├── src/
│   ├── config.py                 # Central configuration file for all paths and settings.
│   ├── main.py                     # The main FastAPI backend application.
│   └── modules/
│       ├── 00_create_sample.py     # Script to generate the small sample CSV.
│       ├── 01_prepare_data.py      # Script for cleaning and preparing the raw data.
│       └── 02_generate_embeddings.py # Script to generate sentence embeddings.
├── static/
│   ├── index.html                  # The main frontend page.
│   ├── style.css                   # CSS for styling the frontend.
│   └── script.js                   # JavaScript for frontend interactivity.
├── pyproject.toml                  # Project definition and dependencies for pdm.
└── README.md                       # This file.
```

## Configuration

This project uses a central configuration file, `src/config.py`, to manage all important parameters. If you want to change how the pipeline works, this is the first place to look.

For example, to process a different number of listings, you can simply change the `NUM_LISTINGS` variable inside `src/config.py`:

```python
# src/config.py
NUM_LISTINGS = 1000 # Change this value to 5000 to process more data
```

The entire pipeline—from data sampling to the web application—will automatically use the new value.

## How to Run

This project is managed by `pdm`. Ensure you have Python and `pdm` installed.

### 1. Setup

First, place your raw dataset (`tc20171021.csv`) in the `res/data/` directory.

Then, install all the required dependencies using `pdm`:

```bash
pdm install
```

### 2. Run the MLOps Pipeline

The following steps will process the data and prepare the assets needed for the web application. You can run them individually or all at once.

**Option A: Run the Automated Pipeline (Recommended)**

This single command will create the data sample, prepare it, and generate the necessary embeddings in one step.

```bash
pdm run pipeline
```

**Option B: Run Each Step Manually**

If you need more control, you can still run each script individually.

*Note: The first time you generate embeddings, it will download the ML model (a few hundred MB).*

```bash
pdm run c-sample
pdm run p-data
pdm run g-embeddings
```

### 3. Launch the Web Application

With all the data processed and assets generated, you can now launch the FastAPI web server using the custom `start` script:

```bash
pdm start
```

The server will automatically restart if you make changes to the code.

Once it's running, open your web browser and navigate to:

**http://127.0.0.1:8000**

You should see the Dream Car Finder application, ready to use! 

All data belongs to 'jpayne' and they are only used for educational purposes
https://www.kaggle.com/datasets/jpayne/852k-used-car-listings