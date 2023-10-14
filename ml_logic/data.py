import pandas as pd
import requests
import datetime
from utils import *
from ml_logic.preprocessors import *
from params import *

def get_raw_reddits(subreddit, candidate, time_filter) -> pd.DataFrame:
    """Getting raw data from reddit API.

    Keyword arguments:
    subreddit -- subreddit name
    candidate -- candidate name you want to search
    time_filter -- time filter for reddit search (day, week, month, year, all)
    Return: raw_data (pd.DataFrame)
    """

    reddit = praw.Reddit(
    client_id= REDDIT_KEY,
    client_secret= REDDIT_SECRET,
    user_agent= "Data Saenz 1.0" )

    titles = []
    body = []
    comments = []
    date = []
    query = create_reddit_query(candidate)

    for submission in reddit.subreddit(subreddit).search(query = query, sort = 'comments', time_filter = time_filter):
        titles.append(strip_texts(submission.title))
        body.append(strip_texts(submission.selftext))
        try:
            comments.append(submission.comments)
        except:
            comments.append('')
        date.append(process_date(submission.created_utc))
    raw_data = pd.DataFrame({'date' : date,
                       'title' : titles,
                       'body' : body,
                       'comments' : comments}).sort_values(by='date', ascending = False)
    return raw_data

def get_clean_reddits(candidate, time_filter) -> pd.DataFrame:
    """Getting clean data processed from reddit API.

    Keyword arguments:
    candidate -- candidate name you want to search
    time -- time filter for reddit search (day, week, month, year, all)
    Return: df (pd.DataFrame) with processed data [date, docs]
    """

    aux_df = pd.DataFrame(columns = ['date', 'title', 'body', 'comments'])
    subreddit = SUBREDDITS

    for name in subreddit:
        aux_df = pd.concat([aux_df, get_raw_reddits(name, candidate, time_filter)], ignore_index = True)

    df = process_raw_data(aux_df, candidate)
    return df
