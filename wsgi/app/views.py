from sqlite3 import dbapi2 as sqlite3
from datetime import date
from flask import request, render_template, _app_ctx_stack
from jinja2 import environment
import os
from app import app



def format_datetime(value,format='%b-%d'):
    list_date = value.split('-')
    strdate = date(int(list_date[0]),int(list_date[1]),int(list_date[2]))
    return strdate.strftime(format)

environment.DEFAULT_FILTERS['datetimeformat']=format_datetime

def init_db():
    import data.LoadDatabase
    data.LoadDatabase.load_database()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect( app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

TYPES = ['Readings', 'Assignments', 'Tests']

@app.route('/',methods=['POST','GET'])
def show_all():
    db = get_db()
    if request.method=='POST':
        update_completes(db)

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



def select_homework(homework_type,db):
    sql = ''' SELECT rowid,* FROM {0} ORDER BY date'''.format(homework_type)
    cur = db.execute(sql)
    entries = cur.fetchall()
    return entries

def join_homework(homework):
    entries=[]
    i=0
    for table in homework:
        for row in table:
            name = row['name']
            if 'chapter' in row.keys() and 'pages' in row.keys():
                if None!= row['chapter'] and row['chapter']!=name:
                    name='--'.join([name,row['chapter']])
                if None!= row['pages']:
                     name='--'.join([name,row['pages']])
            if 'time' not in row.keys():
                time = 'in-class'
            else:
                time = row['time']

            new_row = {'id':'-'.join([TYPES[i],str(row['rowid'])]),'type':TYPES[i],
                       'course_code':row['course_code'],'name':name,
                       'date':row['date'],'time':time,'complete':row['complete']}
            entries.append(new_row)
        i+=1
    return entries



def update_table(db,table,completed,rowid):
    sql = '''UPDATE {0}
            SET complete='{1}'
            WHERE rowid = {2}
            '''.format(table,completed,rowid)
    db.execute(sql)
    db.commit()
    return


def update_completes(db):
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            table_id=key.split("-")
            table= table_id[0]
            rowid = table_id[1]
            complete = int(value)
            complete^=1
            update_table(db,table,complete,rowid)
    return