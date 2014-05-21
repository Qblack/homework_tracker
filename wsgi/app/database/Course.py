__author__ = 'Q'
import datetime

class Course:

    def __init__(self,course_code,course_name, db):
        self.course_code = course_code
        self.course_name = course_name
        self.db = db

    def add_reading(self,name,date,chapter=None,pages=None):
        date = clean_and_convert_date(date)
        reading = Reading(name,date,chapter,pages)
        self.db.insert_reading(self.course_code, reading)
        return

    def add_test(self,name,date,time):
        if None==time:
            time ="in-class"
        date = clean_and_convert_date(date)
        test = Gradeable(name,date,time)
        self.db.insert_test(self.course_code, test)
        return

    def add_assignment(self,name,date,time=None):
        date = clean_and_convert_date(date)
        assignment = Gradeable(name,date,time)
        self.db.insert_assignment(self.course_code, assignment)
        return



class Reading:
    def __init__(self,name,date,chapter,pages):
        self.name = name
        self.date = date
        self.chapter = chapter
        self.completed = False
        self.pages = pages


class Gradeable:
    def __init__(self,name,date,time):
        self.name = name
        self.date = date
        self.time = time

MONTHS = {'JAN':1,'FEB':2,'MAR':3,'APR':4,
           'MAY':5,'JUNE':6,'JULY':7,'AUG':8,
           'SEP':9,'OCT':10,'NOV':11,'DEC':12}


def clean_and_convert_date(date):
    if None!=date:
        date =date.strip().split()
        if len(date)==3:
            date.pop(0)
        month = date[0]
        day = date[1]
        if month =="Jun":
            month = "June"
        elif month =="Jul":
            month ="July"

        month = MONTHS.get(month.upper())

        date =datetime.date(2014,month,int(day))

    return date


