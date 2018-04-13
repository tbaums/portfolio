from flask import Flask, render_template, session, redirect, request, url_for, g, abort, request
from news import News
from employee_analyzer import EmployeeAnalyzer
import json
import constants


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def homepage():
    return render_template('cv.html')

@application.route('/cv')
def cv():
    return render_template('cv.html')

@application.route('/cover_letter')
def cover_letter():
    return render_template('cover_letter.html')

@application.route('/apps')
def apps():
    return render_template('apps.html')


@application.route('/trump')
def trump():
    tmp = word_frequency('Trump')
    js_data_container = tmp[0]
    layout = tmp[1]
    return render_template('trump.html', data=js_data_container, layout=layout)

@application.route('/obama')
def obama():
    tmp = word_frequency('Obama')
    js_data_container = tmp[0]
    layout = tmp[1]
    return render_template('obama.html', data=js_data_container, layout=layout)

@application.route('/mueller')
def mueller():
    tmp = word_frequency('Mueller')
    js_data_container = tmp[0]
    layout = tmp[1]
    return render_template('mueller.html', data=js_data_container, layout=layout)

@application.route('/fbi')
def fbi():
    tmp = word_frequency('FBI')
    js_data_container = tmp[0]
    layout = tmp[1]
    return render_template('fbi.html', data=js_data_container, layout=layout)

@application.route('/syria')
def syria():
    tmp = word_frequency('syria')
    js_data_container = tmp[0]
    layout = tmp[1]
    return render_template('syria.html', data=js_data_container, layout=layout)

@application.route('/chicago')
def chicago():
    ea = EmployeeAnalyzer()
    js_data_container = ea.get_police_salaries_by_title()
    return render_template('chicago.html', data=js_data_container)


def word_frequency(query_name):
    data_container = []
    query_name = query_name
    spans = [
        {'from_parameter':'2018-01-01', 'to':'2018-01-15'},
        {'from_parameter':'2018-01-16', 'to':'2018-01-31'},
        {'from_parameter':'2018-02-01', 'to':'2018-02-15'},
        {'from_parameter':'2018-02-15', 'to':'2018-02-28'},
        {'from_parameter':'2018-03-01', 'to':'2018-03-15'},
        {'from_parameter':'2018-03-16', 'to':'2018-03-31'}
        ]
    for span in spans:
        news = News()
        data = news.fetch_news(q=query_name, language='en', from_parameter=span['from_parameter'], to=span['to'])
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
        if sum(trace['y']) > 100 and trace['name'] != query_name.lower():
            js_data_container.append(trace)

    layout = {
        'title': 'Other Words Found in Headlines that include "{}" (2018-YTD)'.format(query_name),
        'xaxis': {
            'title': 'Week Number'
        },
        'yaxis': {
            'title': 'Count of Appearances in Headlines'}
    }


    # save raw js to the database with id=query_name above

    return [js_data_container, layout]

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.debug = True
    application.run()

