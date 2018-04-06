from constants import NEWSAPI_KEY
from newsapi import NewsApiClient
from database import CursorFromConnectionFromPool
from analyzer import Analyzer

class News:
    def __init__(self):
        self.search_params = {}
        self.param_id = None
        self.content = []
        self.total_results = None
        self.pages = None
        self.client = NewsApiClient(api_key='451cb1a39295459a8a5b5282a8c1af5e')

    def __repr__(self):
        return "<News object {}>".format(self.search_params)

    def __set_search_params(self, params):
        self.search_params = dict(params)
        for item in self.search_params:
            self.item = self.search_params[item]
    
    def __dupe_query(self, query):
        query = str(query)
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from public.search_params where parameters = %s", (query ,))
            data = cursor.fetchone()
            if data == None: 
                return False    
            else:
                return True

    def __save_params(self, params):
        if not self.__dupe_query(params):
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("insert into public.search_params values (default, %s)", (str(params) ,))

    
    def __save_content(self, param_id, content):
        for item in content:
            source_id = item['source']['id']
            source_name = item['source']['name']
            author = str(item['author']).replace("'", "''")
            title = str(item['title']).replace("'", "''")
            description = str(item['description']).replace("'", "''")
            url = item['url']
            url_to_image = item['urlToImage']
            published_at = item['publishedAt']
            query = "insert into public.search_content values (default, %s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');" % (param_id, source_id, source_name, 
                                                                                        author, title, description, url, url_to_image, published_at)
            #TODO insert statement above fails silently by default. add error handling.
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute(query)
                                                                                        
               

    def get_search_params(self):
        return self.search_params

    def get_content(self):
        return self.content
    
    def get_param_id(self, params=None):
        if self.param_id == None:
            with CursorFromConnectionFromPool() as cursor: #TODO refactor
                cursor.execute("select * from public.search_params where parameters=%s;", (str(params) ,))
                data = cursor.fetchone()
                self.param_id = data[0]
                return self.param_id
        return self.param_id


    #TODO implement load_from_db
    def load_from_db(self, params):
        pass 

    def fetch_news(self, **kwargs):
        self.__set_search_params(kwargs)
        if not self.__dupe_query(self.get_search_params()):
            response = self.client.get_everything(q=self.get_search_params()['q'],
                                                    language=self.get_search_params()['language'],
                                                    from_parameter=self.get_search_params()['from_parameter'],
                                                    to=self.get_search_params()['to'],
                                                    page_size=100, 
                                                    page=1)
            # calculate number of pages
            self.total_results = response['totalResults']
            self.pages = min(self.total_results / 100, 10)

            for page in range(1, self.pages):
                if page != 1:
                    response = self.client.get_everything(q=self.get_search_params()['q'],
                                                        language=self.get_search_params()['language'],
                                                        from_parameter=self.get_search_params()['from_parameter'],
                                                        to=self.get_search_params()['to'],
                                                        page_size=100, 
                                                        page=page)
                if response['status'] != 'ok':
                    return "newsapi client request failed"
                for article in response['articles']:
                    self.content.append(article)
                    
                # save news to db automatically
                self.__save_params(self.get_search_params())
                param_id = self.get_param_id(self.get_search_params())
                self.__save_content(param_id, self.get_content())
        else:
            response = self.load_from_db(self.get_search_params())
        return self.content

    def analyze_count(self, text_dict):
        text_list = []
        for text in text_dict:
            text_list.append(text['title'])
        response = Analyzer.analyze_count(text_list)
        Analyzer.save_analysis_to_db(self.get_param_id(), response)
        return response


# news = News()
# r = news.fetch_news(q='North Korea', language='en', from_parameter='2017-12-31', to='2018-01-31')
# c = news.analyze_count(r)
# print(c)