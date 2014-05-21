__author__ = 'Q'

import sqlite3




class DataBase:

    def __init__(self,database_name):
        self.conn = sqlite3.connect(database_name)

    def execute_basic_sql(self,sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return

    def execute_with_values(self,sql,values):
        curr = self.conn.cursor()
        curr.execute(sql,values)
        self.conn.commit()
        return

    def close(self):
        self.conn.close()
        return

    def insert_reading(self, course_code, reading):
        sql = ''' INSERT INTO Readings
        VALUES (?, ?, ?, ?, ?, ?)'''
        values = (course_code, reading.name, reading.chapter,reading.date,reading.pages,False)
        self.execute_with_values(sql,values)
        return

    def insert_assignment(self, course_code, assignment):
        sql = ''' INSERT INTO Assignments
        VALUES (?, ?, ?, ?, ?)'''
        values = (course_code, assignment.name,assignment.date, assignment.time,False)
        self.execute_with_values(sql,values)
        return

    def insert_test(self, course_code, test):
        sql = ''' INSERT INTO Tests
        VALUES (?, ?, ?, ?, ?)'''
        values = (course_code, test.name,test.date, test.time, False)
        self.execute_with_values(sql,values)
        return

    def display_table(self,table_name):
        sql = '''SELECT * FROM {0}'''.format(table_name)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        return

    def display_table_by_date(self,table_name):
        sql = '''SELECT * FROM {0} ORDER BY date'''.format(table_name)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        return


