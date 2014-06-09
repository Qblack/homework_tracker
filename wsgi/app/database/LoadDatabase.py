__author__ = 'Q'
from wsgi.app.database.Database import DataBase
from wsgi.app.database.ReadCourseInfo import *
import wsgi.app.database.SetUpDataBase


def load_database():
    wsgi.app.database.SetUpDataBase.reset_database()

    db = DataBase("summer2014courses.db")
    fh = open("schedules/bu362.txt","r+",encoding="utf-8")
    convert_schedule_to_course(fh,"BU362","Building and Managing A Brand", db)
    fh.close()


    convert_schedule_to_course_bu395("schedules/BU395.txt","BU395","Operations Management II",db)


    convert_schedule_to_course_bu398("schedules/BU398.txt","BU398","Organizational Behaviour II",db)
    convert_schedule_to_course_bu415("schedules/BU415.txt","BU415","Intro Management of IS",db)

    convert_schedule_to_course_bu393("schedules/BU393.txt","BU393","Financial Management II",db)


load_database()