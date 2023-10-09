from transformers import pipeline
import pandas as pd
from params import *
from utils import *

def load_model(model_path, tokenizer=True):
    """Loading model from huggingface.
    Return: model_pipeline
    """
    if tokenizer:
        # used for first sentiment analysis model
        model_pipeline = pipeline("text-classification", model=model_path, tokenizer=model_path)
    else:
        model_pipeline = pipeline("text-classification", model=model_path)

    return model_pipeline

def text_sentiment_classifier(df, model_pipeline, only_neutrals=False):
    """Classifying text sentiment.

    Keyword arguments:
    docs_df -- df with datae and docs column
    model_pipeline -- sentiment analysis model
    Return: docs_df
    """
    if only_neutrals:
        docs_df = df.copy()
        docs_df[['label', 'score']] = docs_df.apply(lambda x: get_label_score(model_pipeline, x['docs']) if x['label'] == 'Neutral' else (x['label'],x['score']), axis = 1).apply(pd.Series)
    else:
        docs_df = df.copy()
        docs_df[['label', 'score']] = docs_df.docs.apply(lambda x: get_label_score(model_pipeline, x)).apply(pd.Series)

    return docs_df
