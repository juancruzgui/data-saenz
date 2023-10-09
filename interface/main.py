from params import *
from utils import *
from ml_logic.data import *
from ml_logic.model import *
from ml_logic.preprocessors import *
from ml_logic.encoders import *
import pandas as pd

def analysis(candidate, time_filter) -> pd.DataFrame:
    """
    Main function to run the complete analysis.
    """

    print("\n⭐️ Use case: Sentiment Analysis")
    print(f"⭐️ Candidate: {candidate}")
    print(f"⭐️ Time filter: {time_filter}")

    print("⭐️ Getting data from API and cleaning it...")

    # getting raw data
    processed_data = get_clean_reddits(candidate=candidate, time_filter=time_filter)

    print("⭐️ Loading models...")
    print(f"First model: {MODEL_PATH_SENTIMENT}")
    print(f"Second model: {MODEL_PATH_EMOTION}")

    # loading models
    model_sentiment = load_model(MODEL_PATH_SENTIMENT, tokenizer=True)
    model_emotion = load_model(MODEL_PATH_EMOTION, tokenizer=False)

    assert model_sentiment is not None
    assert model_emotion is not None

    # sentiment analysis
    print("\n⭐️ Sentiment Analysis")
    print("⭐️ Classifying sentiment...")
    aux_df = text_sentiment_classifier(processed_data, model_sentiment, only_neutrals=False)
    aux_df = text_sentiment_classifier(aux_df, model_emotion, only_neutrals=True)

    # processing sentiment labels
    print("⭐️ Processing sentiment labels...")
    aux_df = process_sentiment_labels(aux_df)

    # encoding sentiment labels
    print("⭐️ Encoding sentiment labels...")
    encoded_df = encode_sentiment_labels(aux_df)

    # getting insights
    print("⭐️ Getting insights...")
    final_df = get_insights(encoded_df)

    print("⭐️ Done!", final_df.shape)

if __name__ == "__main__":
    for i, candidate in enumerate(CANDIDATES_FRONT):
        print(f"[{i}] {candidate}")
    n_candidate = input("Choose a candidate: ")
    candidate = CANDIDATES_LIST[int(n_candidate)]

    analysis(candidate=candidate, time_filter='month') # should return only the metrics?
    # should search for the df in GCS before running the hole analysis

    # visualization
