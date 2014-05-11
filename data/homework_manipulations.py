__author__ = 'Q'

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


def update_completes(db,request):
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