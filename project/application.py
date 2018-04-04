from flask import Flask, render_template, session, redirect, request, url_for, g
import constants
from database import CursorFromConnectionFromPool


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def homepage():
    # data = [
    #             {'Date': '2009-03-31', 'High': 18.79, 'Low': 17.78, 'Close': 18.37},
    #             {'Date': '2009-03-30', 'High': 17.76, 'Low': 17.27, 'Close': 17.48},
    #             {'Date': '2009-03-27', 'High': 18.62, 'Low': 18.05, 'Close': 18.13}
    #         ]
    
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


# run the app.
if __name__ == "__main__":
    # with CursorFromConnectionFromPool() as cursor:
    #     cursor.execute("select * from test;")
    #     data = cursor.fetchall()
    #     for t in data:
    #         print(t)
        
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
