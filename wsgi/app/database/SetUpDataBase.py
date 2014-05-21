__author__ = 'Q'
import sqlite3


SQL_Create_Course_Table = '''CREATE TABLE IF NOT EXISTS Courses
             (course_code text, course_name text,complete bool)'''

SQL_Create_Readings_Tables ='''CREATE TABLE IF NOT EXISTS Readings
            (course_code text, name text, chapter int, date text, pages text, complete bool)'''

SQL_Create_Assignment_Tables ='''CREATE TABLE IF NOT EXISTS Assignments
            (course_code text, name text,  date text, time text, complete bool)'''

SQL_Create_Test_Tables ='''CREATE TABLE IF NOT EXISTS Tests
            (course_code text, name text, date text, time text, complete bool)'''

TABLE_NAMES = ["Courses","Readings","Assignments","Tests"]

def create_table(connection,sql):
        cur = connection.cursor()
        cur.execute(sql)
        connection.commit()
        return

def reset_database():

    conn = sqlite3.connect("summer2014courses.db")


    for name in TABLE_NAMES:
        drop = '''DROP TABLE IF EXISTS {0}'''.format(name)
        create_table(conn,drop)


    create_table(conn,SQL_Create_Course_Table)
    create_table(conn,SQL_Create_Readings_Tables)
    create_table(conn,SQL_Create_Assignment_Tables)
    create_table(conn,SQL_Create_Test_Tables)

    conn.close()



