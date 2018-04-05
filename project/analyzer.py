from database import CursorFromConnectionFromPool

class Analyzer:

    @classmethod
    def analyze_count(cls, text_list):
        word_count = {}
        for text in text_list:
            if text != None:
                text_array = text.split(" ") 
                for word in text_array:
                    word = word.replace(",", "")
                    word = word.replace(".", "")
                    word = word.replace("!", "")
                    word = word.replace("?", "")
                    word = word.lower()
                    if word in word_count:
                        word_count[word] = word_count[word] + 1
                    else:
                        word_count[word] = 1
        
        return word_count

    @classmethod
    def save_analysis_to_db(cls, param_id, analysis):
        analysis = str(analysis)
        analysis = analysis.replace("'", "''")
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into public.wordcount values (default, %s, \'%s\');" % (param_id, analysis))