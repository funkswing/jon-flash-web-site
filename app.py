"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request
import requests
import json
from blog import blog
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['MONGO_DBNAME'] = 'blog'
mongo = PyMongo(app)
app.mongo = mongo  # https://github.com/dcrosta/flask-pymongo/issues/11
app.register_blueprint(blog)


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template(
        'index.html',
        logo="logo",
        header="Jon Flaishans",
        skills="Web Application Developer - RESTful APIs - Cloud Computing Engineer"
    )


@app.route('/contact/', methods=['POST'])
def contact():
    """Send form to Mailgun REST API"""

    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    EMAIL_ADDR = os.environ.get('EMAIL_ADDR')

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    response = requests.post(
        "https://api.mailgun.net/v3/flaishans.com/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": name + " <" + email + ">",
              "to": EMAIL_ADDR,
              "subject": "Message from Flaishans.com",
              "text": message + " Phone: " + phone})

    return json.dumps({'success': response.content}), 200, {'ContentType': 'application/json'}


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template(
        '404.html',
        logo="404-error",
        header="404 - Not Found :'(",
        skills="""<a href="/" style="color: white;">Please navigate back to the good stuff</a>"""
    ), 404


if __name__ == '__main__':
    app.run(debug=True)
