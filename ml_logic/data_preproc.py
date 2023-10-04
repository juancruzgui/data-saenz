import pandas as pd
import requests
import datetime
import re
import praw
from params import *

def strip_texts(text):
    # Match "chars" preceded by a word, and delete both
    text = re.sub(r'(\w+)\s+chars\b', '', text)
    text = re.sub('<^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ',text.lower()) + ' '.join(emoticons).replace('-','')
    return text

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

def process_news_data(df):
    # cleaning text
    df['title'] = df['title'].apply(strip_texts)
    df['description'] = df['description'].apply(strip_texts)
    df['content'] = df['content'].apply(strip_texts)

    # setting date with datetime format YYYY-MM-DD HH:MM:SS
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['date'] = df['publishedAt'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # merging title, description and content
    df['docs'] = df['title'] + ', ' + df['description'] + ', ' + df['content']

    # dropping columns
    df = df.drop(columns=['title', 'description', 'content', 'publishedAt'])

    # deleting spaces at the beginning and end of the text
    df['docs'] = df['docs'].str.strip()

    df = df.sort_values(by=['date'], ascending=False)
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
