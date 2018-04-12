from database import CursorFromConnectionFromPool

class Analyzer:

    def analyze_count(self, data):
        # print(data)
        clean_data = []
        for article in data:
            if 'published_month' in article:
                month = article['published_month'].strftime('%U')
                clean_data.append([article['title'], month])

        # remove punctuation from titles and split into arrays of words
        for article in clean_data:
            article[0] =  article[0].replace(",", "")
            article[0] =  article[0].replace(".", "")
            article[0] =  article[0].replace("!", "")
            article[0] =  article[0].replace(";", "")
            article[0] =  article[0].replace(":", "")
            article[0] =  article[0].replace("?", "")
            article[0] =  article[0].replace("(", "")
            article[0] =  article[0].replace(")", "")
            article[0] =  article[0].replace("'", "")
            article[0] =  article[0].replace("\"", "")
            article[0] =  article[0].lower()

            article[0] = article[0].split(" ")

        # Goal: 
        # clean_data : [  
        #   word : {
        #       month: {count: }
        #   }
        # ]
        clean_data = self.count(clean_data)
        return clean_data

    def count(self, clean_data):
        pair_set = set()
        word_set = set()
        data_container = {}
        for article in clean_data:
            for word in article[0]:
                if not self.exclude_word(word):
                    pair = str([word, article[1]])
                    if pair in pair_set:
                        #look for it and add numbers
                        data_container[word][article[1]] = data_container[word][article[1]] + 1
                    elif word in word_set:
                        pair_set.add(pair)
                        # add a date and set word.date to 1
                        data_container[word][article[1]] = 1

                    else:
                        pair_set.add(pair)
                        word_set.add(word)
                        data_container[word] = { article[1] : 1}
        
        clean_data = data_container
        return clean_data


    def exclude_word(self, word):
        exclusion_string = "- & the of and a are  @ – i as says | to in is you that it he was for on areas with his they I at be this have from or one had by word but not what all were we when your can said there use an each which she do how their if will up other about out many then them these so some her would make like him into time has look two more write go see number no way could people my than first water been call who oil its now find long down day did get come made may part"
        exclusion_list = exclusion_string.split(" ")
        return word in exclusion_list
    

                



        # word_count = {}
        # for text in text_list:
        #     if text[0] != None: # [title, published_month]
        #         text_array = text[0].split(" ") 
        #         for   article[0] in text_array:
        #               article[0] = article[0].replace(",", "")
        #               article[0] = article[0].replace(".", "")
        #               article[0] = article[0].replace("!", "")
        #               article[0] = article[0].replace("?", "")
        #               article[0] = article[0].replace(";", "")
        #               article[0] = article[0].replace("(", "")
        #               article[0] = article[0].replace(")", "")
        #               article[0] = article[0].lower()
        #             if    article[0] in word_count and word_count   article[0]]['published_month'] != None:
        #                 word_count    article[0]]['count'] = word_count article[0]]['count'] + 1
        #             else:
        #                 word_count    article[0]] = {}
        #                 word_count    article[0]]['published_month'] = text[1]
        #                 word_count    article[0]]['count'] = 1    
        
        # print(word_count)
        # word_count = Cleaner.clean_freq_data(word_count)
        # return word_count

    @classmethod
    def save_analysis_to_db(cls, param_id, analysis):
        analysis = str(analysis)
        analysis = analysis.replace("'", "''")
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into public.wordcount values (default, %s, \'%s\');" % (param_id, analysis))