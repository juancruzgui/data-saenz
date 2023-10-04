import os

### CREDENTIALS ###
NEWS_KEY = os.environ.get('NEWS_KEY')
REDDIT_KEY = os.environ.get('REDDIT_KEY')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET')

### VARIABLES ###
CANDIDATES_LIST= {
    "Sergio Massa": "Massa NOT Milei NOT Bullrich NOT Bregman NOT Schiaretti NOT Macri NOT Alberto NOT Cristina",
    "Javier Milei": "Milei NOT Massa NOT Bullrich NOT Bregman NOT Schiaretti NOT Macri NOT Alberto NOT Cristina",
    "Patricia Bullrich": "Bullrich NOT Massa NOT Milei NOT Bregman NOT Schiaretti NOT Macri NOT Alberto NOT Cristina",
    "Myriam Bregman": "Bregman NOT Massa NOT Milei NOT Bullrich NOT Schiaretti NOT Macri NOT Alberto NOT Cristina",
    "Juan Schiaretti": "Schiaretti NOT Massa NOT Milei NOT Bullrich NOT Bregman NOT Macri NOT Alberto NOT Cristina",
}

SUBREDDITS = "Argentina+RepublicaArgentina"
