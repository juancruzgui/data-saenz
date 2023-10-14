from sentiment_analysis.params import *
from sentiment_analysis.utils import *
from sentiment_analysis.ml_logic.data import *
from sentiment_analysis.ml_logic.model import *
from sentiment_analysis.ml_logic.preprocessors import *
from sentiment_analysis.ml_logic.encoders import *
from sentiment_analysis.ml_logic.registry import *
from sentiment_analysis.ml_logic.visualizations import plot_neg_pos, plot_bar_hor,stacked_bars
import pandas as pd

def analysis_old(candidate, time_filter) -> pd.DataFrame:
    """
    Main function to run the complete analysis.
    Via GCS or running the whole analysis.
    """

    try:
        print(f"\n⭐️ Use case: Sentiment Analysis - GCS")
        print(f"⭐️ Candidate: {candidate}")
        print(f"⭐️ Time filter: {time_filter}")

        final_df = load_insights(candidate=candidate)
        print("⭐️ Done!", final_df.shape)

        return final_df
    except:
        print("\n⭐️ Use case: Sentiment Analysis - Running")
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

        # saving insights
        save_insights(final_df, candidate=candidate)

        print("⭐️ Done!", final_df.shape)

        return final_df

def analysis(candidate, time_filter='day', model_loaded=False) -> pd.DataFrame:
    """
    Main function to run the complete analysis.
    Via GCS or running the whole analysis.
    """
    try:
        print(f"\n⭐️ Use case: Sentiment Analysis - GCS")
        print(f"⭐️ Candidate: {candidate}")
        print(f"⭐️ Time filter: month (but not today)")

        main_df = load_insights(candidate=candidate)

        print("⭐️ Main DF Returned!", main_df.shape)

    except:
        print("\n⭐️ Use case: Sentiment Analysis - Running")
        print("\n⭐️ Getting whole month including today...")
        print(f"⭐️ Candidate: {candidate}")
        print(f"⭐️ Time filter: month")

        print("⭐️ Getting data from API and cleaning it...")

        # getting raw data
        processed_data = get_clean_reddits(candidate=candidate, time_filter='month')

        if model_loaded == False:
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
        main_df = get_insights(encoded_df)

        # saving insights
        save_insights(main_df, candidate=candidate)

        print("⭐️ Final DF Returned!", main_df.shape)

        return main_df

    print("\n📍 Adding today's data...")
    print("\n📍 Use case: Sentiment Analysis - Running")
    print("\n📍 Getting todays data...")
    print(f"📍 Candidate: {candidate}")
    print(f"📍 Time filter: day")

    print("📍 Getting data from API and cleaning it...")

    # getting raw data
    processed_data = get_clean_reddits(candidate=candidate, time_filter=time_filter)



    print("📍 Loading models...")
    print(f"First model: {MODEL_PATH_SENTIMENT}")
    print(f"Second model: {MODEL_PATH_EMOTION}")

    # loading models
    model_sentiment = load_model(MODEL_PATH_SENTIMENT, tokenizer=True)
    model_emotion = load_model(MODEL_PATH_EMOTION, tokenizer=False)

    assert model_sentiment is not None
    assert model_emotion is not None

    # sentiment analysis
    print("\n📍 Sentiment Analysis")
    print("📍 Classifying sentiment...")
    aux_df = text_sentiment_classifier(processed_data, model_sentiment, only_neutrals=False)
    aux_df = text_sentiment_classifier(aux_df, model_emotion, only_neutrals=True)

    # processing sentiment labels
    print("📍 Processing sentiment labels...")
    aux_df = process_sentiment_labels(aux_df)

    # encoding sentiment labels
    print("📍 Encoding sentiment labels...")
    encoded_df = encode_sentiment_labels(aux_df)

    # getting insights
    print("📍 Getting insights...")
    today_df = get_insights(encoded_df)

    print("📍 Today's DF: ", today_df.shape)
    print("Mergin with main DF...")
    new_df = merging_today_with_month_df(today_df, main_df)
    save_insights(new_df, candidate=candidate)

    return new_df

def visualizations():
    pass

if __name__ == "__main__":
    ### the next flow should be executed once a day (23:50) ###
    candidates_dfs = []
    for candidate in CANDIDATES_LIST:
        # df = analysis_old(candidate=candidate, time_filter='month')
        df = analysis(candidate=candidate)
        plot_neg_pos(df, candidate)
        plot_bar_hor(df, candidate)
        candidates_dfs.append(df)

    stacked_bars(candidates_dfs)
