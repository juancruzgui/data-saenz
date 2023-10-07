import pandas as pd

def encode_labels(docs_df):
  docs_df = pd.concat([docs_df, pd.get_dummies(docs_df['label'])], axis=1).drop(columns = 'label')
  return docs_df
