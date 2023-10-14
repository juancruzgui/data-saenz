import pandas as pd
from google.cloud import storage
from sentiment_analysis.params import *
import io

def save_insights(df, candidate):
    """Saving insights from GCS.

    Keyword arguments:
    encoded_df -- df with encoded labels
    Return: None
    """
    try:
        print(f"\nSaving insights for {candidate}")
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob_csv = bucket.blob(f'{candidate}_insights.csv')
        blob_csv.upload_from_string(df.to_csv(), content_type='text/csv')
        print(f"\n✅ {candidate} insights saved to GCS")

    except:
        print(f"\n❌No insights found for {candidate}")


def load_insights(candidate):
    """Loading insights from GCS.

    Keyword arguments:
    candidate -- candidate name
    Return: df with insights
    """
    try:
        print(f'\nLoading insights for {candidate}')
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob_csv = bucket.blob(f'{candidate}_insights.csv')
        data_bytesio = blob_csv.download_as_bytes()

        df = pd.read_csv(io.BytesIO(data_bytesio), index_col="date")

        print(f'\n✅ Insights found for {candidate}')

    except:
        print(f'\n❌ No insights found for {candidate}')

    return df
