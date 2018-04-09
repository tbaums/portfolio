from flask import Flask, render_template, session, redirect, request, url_for, g
from news import News
import constants


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def homepage():
    text = "this is some text"
    return render_template('home.html')

@application.route('/cv')
def cv():
    return render_template('cv.html')

@application.route('/cover_letter')
def cover_letter():
    return render_template('cover_letter.html')

@application.route('/apps')
def apps():
    return render_template('apps.html')


@application.route('/word_frequency')
def word_frequency():
    data_container = []
    spans = [
        {'from_parameter':'2017-11-01', 'to':'2017-11-30'},
        {'from_parameter':'2017-12-01', 'to':'2017-12-31'},
        {'from_parameter':'2018-01-01', 'to':'2018-01-31'},
        {'from_parameter':'2018-02-01', 'to':'2018-02-28'},
        {'from_parameter':'2018-03-01', 'to':'2018-03-31'}
        ]
    for span in spans:
        news = News()
        data = news.fetch_news(q='North Korea', language='en', from_parameter=span['from_parameter'], to=span['to'])
        # print(data)
        analysis = news.analyze_count(data)
        data_container.append(analysis) 

    wordset = set()
    combined_data_container = {}
    for analysis in data_container:
        for key in analysis.keys():
            if key in wordset:
                combined_data_container[key] = {**combined_data_container[key], **analysis[key]}
            else:
                wordset.add(key)
                combined_data_container[key] = analysis[key]
                
    # var trace1 = {
    #   x: [1, 2, 3, 4],
    #   y: [10, 15, 13, 17],
    #   mode: 'markers',
    #   name: 'Scatter'
    # };

    js_data_container = []
    for word in combined_data_container:
        x = list(combined_data_container[word].keys())
        x.sort()
        y = []
        for date in x:
            y.append(int(combined_data_container[word][date]))
        trace = {
            'x': x,
            'y': y,
            'name': word 
        }
        if sum(trace['y']) > 50:
            js_data_container.append(trace)
    
    return render_template("word_frequency.html", data=js_data_container)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.debug = True
    application.run()