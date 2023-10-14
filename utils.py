from params import *
import pandas as pd

def create_search_query(candidate_used, candidates) -> str:
    """Creating search binary query for news API.

    Keyword arguments:
    candidate_used -- candidate name
    candidates -- list of candidates
    Return: query
    """

    query = f"{candidate_used.lower()}"

    for cand in candidates:
        if cand != candidate_used.lower():
            query+= f" NOT {cand}"
    return query

def create_reddit_query(candidate) -> str:
    return candidate.lower()

def get_label_score(model_pipeline, doc) -> tuple:
    """Runnning the sentiment analysis model on a document and returning the label and score.

    Keyword arguments:
    argument -- description
    Return: label, score (str, float)
    """
    try:
        label, score = model_pipeline(doc)[0].values()
    except:
        label = None
        score = None

    return label,score

def find_candidate_fullname(candidate):
    # using CANDIDATES_FRONT where I have the full name of the candidates, and the variable candidate where I have the last name
    for cand in CANDIDATES_FRONT:
        if candidate.capitalize() in cand:
            return cand

def merging_today_with_month_df(today_df, month_df):
    """Merging the today_df with the month_df.

    Keyword arguments:
    today_df -- dataframe with today's data
    month_df -- dataframe with the month's data
    Return: merged_df
    """
    # deleting first row of month_df (It's the farthest date from today)
    month_df = month_df.iloc[1:]

    # keeping today's data from today_df
    today_df = today_df.iloc[1:]

    # merging today_df into the last row of df_month
    df = pd.concat([month_df, today_df])

    return df
