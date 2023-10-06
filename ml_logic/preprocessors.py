import re
import datetime
import pandas as pd

def strip_texts(text):
    # Match "chars" preceded by a word, and delete both
    text = re.sub(r'(\w+)\s+chars\b', '', text)
    url_pattern = r'(https?://)?(www\.)?[\w-]+\.\w+'
    text = re.sub(url_pattern, '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub('<^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ',text.lower()) + ' '.join(emoticons).replace('-','')
    return text

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

def process_date(date):
    return datetime.datetime.fromtimestamp(date).date()

def process_comments(comments, candidate, candidates):
    comments_list = []
    dates_list = []
    candidates.remove(candidate.lower())

    for comment in comments:
        try:
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
        except:
            morecomments = comment.comments()
            for com in morecomments:
              date = process_date(com.created_utc)
              com = com.body.lower()
              i = 0
              for cand in candidates:
                  if cand in com or candidate not in com:
                      i+=1
              if i==0:
                  #stripping html tags, emoticons, and characters
                  com = strip_texts(com)
                  #appending comment
                  comments_list.append(com)
                  dates_list.append(date)
    comments_df = pd.DataFrame({'date':dates_list,
                                'docs' : comments_list})
    return comments_df
