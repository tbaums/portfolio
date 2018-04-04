from constants import NEWSAPI_KEY
from newsapi import NewsApiClient

class News:
    __newsclient = NewsApiClient(api_key='451cb1a39295459a8a5b5282a8c1af5e')
    
    def __init__(self):
        self.search_params = {}
        self.content = []

