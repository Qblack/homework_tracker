from sqlite3 import dbapi2 as sqlite3
import os
from datetime import date

from flask import Flask, request, render_template, _app_ctx_stack
from jinja2 import environment


import sys
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.homework_manipulations import *



# configuration
DATABASE = os.path.join(app.root_path,'\data', 'summer2014courses.db')
print(DATABASE)

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

def format_datetime(value,format='%b-%d'):
    list_date = value.split('-')

    strdate = date(int(list_date[0]),int(list_date[1]),int(list_date[2]))
    return strdate.strftime(format)

environment.DEFAULT_FILTERS['datetimeformat']=format_datetime


if __name__ == "__main__":
    app.run(debug=True)

def init_db():
    import data.LoadDatabase
    data.LoadDatabase.load_database()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db


    return top.sqlite_db

TYPES = ['Readings', 'Assignments', 'Tests']

@app.route('/',methods=['POST','GET'])
def show_all():

    db = get_db()
    if request.method=='POST':
        update_completes(db,request)

    entries =[]
    for homework in TYPES:
        entries.append(select_homework(homework,db))
    homework = join_homework(entries)

    return render_template('show_all.html',entries=homework )

@app.route('/Assignments')
def show_assignments():
    db = get_db()
    sql = '''SELECT * FROM {0} ORDER BY date'''.format("Assignments")
    cur = db.execute(sql)
    entries = cur.fetchall()
    return render_template('show_assignments.html', entries=entries)

@app.route('/Tests')
def show_tests():
    db = get_db()
    sql = '''SELECT * FROM {0} ORDER BY date'''.format("Tests")
    cur = db.execute(sql)
    entries = cur.fetchall()
    return render_template('show_tests.html', entries=entries)

@app.route('/Readings')
def show_readings():
    db = get_db()
    sql = '''SELECT * FROM {0} ORDER BY date'''.format("Readings")
    cur = db.execute(sql)
    entries = cur.fetchall()
    return render_template('show_readings.html',entries=entries)


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()