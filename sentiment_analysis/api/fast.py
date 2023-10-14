import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentiment_analysis.interface.main import analysis, plot_neg_pos, plot_bar_hor, stacked_bars
from sentiment_analysis.ml_logic.model import load_model
from sentiment_analysis.params import *

app = FastAPI()

app.state.model_sentiment = load_model(MODEL_PATH_SENTIMENT, tokenizer=True)
print(type(app.state.model_sentiment))

app.state.model_emotion = load_model(MODEL_PATH_EMOTION, tokenizer=False)
print(type(app.state.model_emotion))

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/analysis-update")
def update() -> dict:
    """
    Update the analysis data
    Returns:
        dict: A message indicating the update is complete.
    """
    try:
        print("\n⭐️ Use case: update the analysis data")

        candidates_dfs = []
        for candidate in CANDIDATES_LIST:
            df = analysis(candidate=candidate, model_loaded=True)
            plot_neg_pos(df, candidate)
            plot_bar_hor(df, candidate)
            candidates_dfs.append(df)

        stacked_bars(candidates_dfs)

        return {"message": "✅ Analysis data has been updated."}
    except Exception as e:
        print(e)
        return {"message": "❌ Analysis data has not been updated."}

@app.get("/")
def root():

    return {"message": "Welcome to Data-Saenz API",
             "documentation": "/docs",
             "analysis_url": "/analysis-update"}
