from flask import Flask, render_template, session, redirect, request, url_for, g


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def homepage():
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
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()