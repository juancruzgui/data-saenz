import re
import datetime
import pandas as pd
import praw
from sentiment_analysis.params import *

def strip_texts(text) -> str:
    """Remove urls, numbers, and special characters from text.

    Return: text
    """
    # removing urls
    url_pattern = r'(https?://)?(www\.)?[\w-]+\.\w+'
    text = re.sub(url_pattern, '', text)

    # removing "chars" characters
    text = re.sub(r'(\w+)\s+chars\b', '', text)

    # removing numbers
    text = re.sub(r'\d+', '', text)

    # removing html tags
    text = re.sub('<^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)

    # removing non-word characters and converting to lowercase
    text = re.sub('[\W]+', ' ',text.lower()) + ' '.join(emoticons).replace('-','')

    return text

def process_news_data(df) -> pd.DataFrame:
    """Processing news data in order to be used in the model.

    Return: df
    """

    # cleaning text
    df['title'] = df['title'].apply(strip_texts)
    df['description'] = df['description'].apply(strip_texts)
    df['content'] = df['content'].apply(strip_texts)

    # setting date with datetime format YYYY-MM-DD HH:MM:SS
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['date'] = df['publishedAt'].dt.strftime('%Y-%m-%d')

    # merging title, description and content
    df['docs'] = df['title'] + ', ' + df['description'] + ', ' + df['content']

    # dropping columns
    df = df.drop(columns=['title', 'description', 'content', 'publishedAt'])

    # deleting spaces at the beginning and end of the text
    df['docs'] = df['docs'].str.strip()

    df = df.sort_values(by=['date'], ascending=False)
    df = df.reset_index(drop=True)
    return df

def process_date(date) -> datetime.date:
    """Processing date in order to get YYYY-MM-DD format.

    Return: date
    """
    return datetime.datetime.fromtimestamp(date).date()

def process_comments(comments, candidate) -> pd.DataFrame:
    """Processing comments in order to get every comment who mentions the candidate and not the others.

    Keyword arguments:
    comments -- comments object from reddit
    candidate -- candidate name
    Return: comments_df
    """

    comments_list = []
    dates_list = []
    candidates = CANDIDATES_LIST.copy()
    candidates.remove(candidate.lower())

    for comment in comments:
      if isinstance(comment, praw.models.reddit.comment.Comment):
        date = process_date(comment.created_utc)
        comment = comment.body.lower()
        i = 0
        for cand in candidates:
            if cand in comment or candidate not in comment:
                i+=1
        if i==0:
            #stripping html tags, emoticons, and characters
            comment = strip_texts(comment)
            #appending comment
            comments_list.append(comment)
            dates_list.append(date)
      else:
        morecomments = comment.comments()
        process_comments(morecomments, candidate)


    comments_df = pd.DataFrame({'date': dates_list,
                                'docs' : comments_list})
    return comments_df

def process_raw_data(raw_data, candidate) -> pd.DataFrame:
    """Processing raw data in order to be used in the model, merging comments and title into docs column.

    Keyword arguments:
    raw_data -- df with raw data getted from reddit API
    candidate -- candidate name
    Return: processed_data
    """

    data = raw_data.copy()
    docs = []
    dates = []
    data.comments = data.comments.apply(lambda x: process_comments(x, candidate))
    processed_data = pd.DataFrame({'date' : data.date,
                                   'docs' : data.title})

    for index, row in raw_data.iterrows():
        processed_data = pd.concat([processed_data, data.comments[index]], axis = 0)

    processed_data.reset_index(inplace = True)
    processed_data.drop(columns = 'index', inplace = True)

    return processed_data

def process_sentiment_labels(df) -> pd.DataFrame:
    df['label'] = df['label'].str.capitalize()
    df['label'] = df['label'].replace({'Negative': 'Negativo',
                                       'Others': 'Neutral',
                                       'Positive': 'Positivo',
                                       'Anger': 'Enojo',
                                       'Joy': 'Alegria',
                                       'Sadness': 'Tristeza',
                                       'Disgust': 'Disgusto',
                                       'Fear': 'Miedo',
                                       'Surprise': 'Sorpresa'})
    return df

def get_insights(encoded_df):
    # Defining the columns I want to ensure exist
    columns_to_ensure = ['Neutral', 'Negativo', 'Positivo', 'Alegria', 'Sorpresa', 'Tristeza', 'Enojo', 'Disgusto', 'Miedo']

    # Checking if the columns exist in the DataFrame
    missing_columns = [col for col in columns_to_ensure if col not in encoded_df.columns]

    # Adding missing columns with all False values
    if missing_columns:
        for col in missing_columns:
            encoded_df[col] = False

    final_df = encoded_df[encoded_df.score > 0.7].groupby('date').agg({'Negativo' : 'sum',
                                                                        'Neutral' : 'sum',
                                                                        'Positivo' : 'sum',
                                                                        'Alegria' : 'sum',
                                                                        'Sorpresa' : 'sum',
                                                                        'Tristeza' : 'sum',
                                                                        'Enojo' : 'sum',
                                                                        'Disgusto' : 'sum',
                                                                        'Miedo' : 'sum'})

    final_df['total'] = final_df.Negativo + final_df.Neutral + final_df.Positivo + final_df.Alegria + final_df.Sorpresa + final_df.Tristeza + final_df.Enojo + final_df.Disgusto + final_df.Miedo

    final_df['%Neg'], final_df['%Neu'], final_df['%Pos'], final_df['%Ale'], final_df['%Sor'], final_df['%Tri'], final_df['%Eno'], final_df['%Dis'], final_df['%Mie']  = final_df.Negativo/final_df.total, final_df.Neutral/final_df.total, final_df.Positivo/final_df.total, final_df.Alegria/final_df.total, final_df.Sorpresa/final_df.total, final_df.Tristeza/final_df.total, final_df.Enojo/final_df.total, final_df.Disgusto/final_df.total, final_df.Miedo/final_df.total

    return final_df
