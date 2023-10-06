from transformers import pipeline
import pandas as pd
from params import *
from utils import *

def load_model():
    """Loading model from huggingface.
    Return: model_pipeline
    """
    model_path = MODEL_PATH
    model_pipeline = pipeline("text-classification", model=model_path, tokenizer=model_path)
    return model_pipeline

def text_sentiment_classifier(docs_df, model_pipeline):
    """Classifying text sentiment.

    Keyword arguments:
    docs_df -- df with datae and docs column
    model_pipeline -- sentiment analysis model
    Return: docs_dfs
    """

    docs_dfs = docs_df.copy()
    docs_dfs[['label', 'score']] = docs_dfs.docs.apply(lambda x: get_label_score(model_pipeline, x)).apply(pd.Series)
    return docs_dfs
