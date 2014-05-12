__author__ = 'Q'
from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import os
# configuration
app.config.update(dict(
    DATABASE=os.path.join(os.environ.get('HOME'), 'homework_tracker/data/summer2014courses.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


from app import views