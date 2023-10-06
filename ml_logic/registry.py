import pandas as pd

def save_insights(encoded_df, candidate):
    """Saving insights locally from encoded_df and returning final_df if needed.

    Keyword arguments:
    encoded_df -- df with encoded labels
    Return: final_df with insights
    """

    # Defining the columns I want to ensure exist
    columns_to_ensure = ['Negative', 'Neutral', 'Positive']

    # Checking if the columns exist in the DataFrame
    missing_columns = [col for col in columns_to_ensure if col not in encoded_df.columns]

    # Adding missing columns with all False values
    if missing_columns:
        for col in missing_columns:
            encoded_df[col] = False

    final_df = encoded_df[encoded_df.score > 0.7].groupby('date').agg({'Negative' : 'sum', 'Neutral' : 'sum', 'Positive' : 'sum'})

    final_df['total'] = final_df.Negative + final_df.Neutral + final_df.Positive

    final_df['%Neg'],final_df['%Neu'],final_df['%Pos']  = final_df.Negative/final_df.total, final_df.Neutral/final_df.total, final_df.Positive/final_df.total

    final_df = final_df.reset_index()

    # saving insights locally
    final_df.to_csv(f'data/{candidate}_insights.csv', index=False)

    return final_df

def load_insights(candidate):
    """Loading insights locally.

    Keyword arguments:
    candidate -- candidate name
    Return: insights_df
    """
    try:
        insights_df = pd.read_csv(f'data/{candidate}_insights.csv')
        print(f'Insights found for {candidate}')

    except:
        print(f'No insights found for {candidate}')

    return insights_df
