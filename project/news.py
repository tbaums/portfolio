from constants import NEWSAPI_KEY
from newsapi import NewsApiClient
from database import CursorFromConnectionFromPool


class News:
    def __init__(self):
        self.search_params = {}
        self.content = []
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
            print(data)
            if data == None: 
                return False    
            else:
                return True

    # def __build_query(self, params):
    #     query = ""
    #     for key in params:
    #         query = query + str(key) + "=" + str(params[key])
    #         print(query)
    #     return query

    def __save_params(self, params):
        if not self.__dupe_query(params):
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("insert into public.search_params values (default, %s)", (str(params) ,))

    
    def __save_content(self, param_id, content):
        for item in content:
            source_id = item['source']['id']
            source_name = item['source']['name']
            author = item['author']
            title = item['title'].replace("'", "''")
            description = item['description'].replace("'", "''")
            url = item['url']
            url_to_image = item['urlToImage']
            published_at = item['publishedAt']
            query = "insert into public.search_content values (default, %s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');" % (param_id, source_id, source_name, 
                                                                                        author, title, description, url, url_to_image, published_at)
            #TODO insert statement above fails silently. add error handling.
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute(query)
                                                                                        
               

    def get_search_params(self):
        return self.search_params

    def get_content(self):
        return self.content
    
    def get_param_id(self, params):
        with CursorFromConnectionFromPool() as cursor: #TODO refactor
                cursor.execute("select * from public.search_params where parameters=%s;", (str(params) ,))
                data = cursor.fetchone()
                return data[0]


    #TODO implement load_from_db
    def load_from_db(self, params):
        pass 

    def fetch_news(self, **kwargs):
        self.__set_search_params(kwargs)
        if not self.__dupe_query(self.get_search_params()):
            response = self.client.get_top_headlines(q=self.get_search_params()['q'])
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
        return response

# x = News().get_param_id("test4")



# x = News().dupe_query("test")
# print(x)

# x = News().dupe_query("test")
# print(x)

print(News().fetch_news(q="trump"))

# print(news.toodle)

# print(news.poodle)