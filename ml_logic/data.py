import pandas as pd
import requests
import datetime
from ml_logic.utils import *
from params import *
from ml_logic.preprocessors import *

def get_raw_news(candidate):
    """
    Getting news based on candidate name
    Return: API content
    """

    base_url = "https://newsapi.org/v2/everything?"

    params = {
        "apiKey": NEWS_KEY,
        "q": candidate,
        "searchIn": ["title","description"],
        "domains": ['lanacion.com.ar, infobae.com'],
        "from": datetime.datetime.now() - datetime.timedelta(days=30)
    }

    response = requests.get(base_url, params=params)
    content = response.json()

    df = pd.DataFrame(content['articles'])
    df = df[['publishedAt', 'title', 'description', 'content']]
    df = df.sort_values(by=['publishedAt'], ascending=False)
    df = df.reset_index(drop=True)

    return df

def get_clean_news(candidate):
    """
    Getting news based on candidate name
    Return: Cleaned data
    """
    print(f"Getting raw news for {candidate}...")
    df = get_raw_news(candidate)

    print(f"Processing news for {candidate}...")
    df = process_news_data(df)
    return df
