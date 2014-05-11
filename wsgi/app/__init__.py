__author__ = 'Q'
from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# configuration
app.config['DATABASE'] = 'app/tmp/summer2014courses.db'
from app import views