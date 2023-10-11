import os
import datetime

### CREDENTIALS ###
NEWS_KEY = os.environ.get('NEWS_KEY')
REDDIT_KEY = os.environ.get('REDDIT_KEY')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET')

### VARIABLES ###
CANDIDATES_FRONT = ["Sergio Massa", "Javier Milei", "Patricia Bullrich", "Myriam Bregman", "Juan Schiaretti"]

CANDIDATES_LIST = ["massa", "milei", "bullrich", "bregman", "schiaretti"]

SUBREDDITS = ["Argentina","RepublicaArgentina","ArgentinaBenderStyle","Republica_Argentina","AskArgentina"]

DOMAINS = ['lanacion.com.ar', 'infobae.com', 'tn.com.ar', 'lavoz.com.ar', 'clarin.com',
           'pagina12.com.ar', 'ambito.com', 'cronista.com', 'perfil.com', 'c5n.com', 'lacapital.com.ar']

MODEL_PATH_SENTIMENT = os.environ.get('MODEL_PATH_SENTIMENT')
MODEL_PATH_EMOTION = os.environ.get('MODEL_PATH_EMOTION')

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

BUCKET_NAME = os.environ.get('BUCKET_NAME')
