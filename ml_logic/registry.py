import pandas as pd
import datetime

def save_insights(final_df, candidate):
    """Saving insights locally from encoded_df and returning final_df if needed.

    Keyword arguments:
    encoded_df -- df with encoded labels
    Return: final_df with insights
    """
    # saving final df to csv
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    final_df.to_csv(f'data/{candidate}_insights_{today}.csv')


def load_insights(candidate):
    """Loading insights locally.

    Keyword arguments:
    candidate -- candidate name
    Return: insights_df
    """
    try:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        insights_df = pd.read_csv(f'data/{candidate}_insights_{today}.csv')
        print(f'Insights found for {candidate}')

    except:
        print(f'No insights found for {candidate}')

    return insights_df
