from wsgi.app.database import Course

__author__ = 'Q'

import re

TIME_PATTERN = r"(\d|\s)\d\:\d\d"

TIME_PATTERN_AMPM = r"(\d|\s)\d\:\d\d\w\w"


def convert_schedule_to_course(schedule,course_code,class_name,db):

    time_prog = re.compile(TIME_PATTERN)
    course = Course(course_code,class_name,db)

    for line in schedule:
        line = line.strip()
        session  = line.split("|")
        if len(session)==3:
            date = session[1]
            reading_name = session[2]
            course.add_reading(reading_name,date)
        elif "DUE" in line.upper():
            name_and_time = session[1]
            time = time_prog.search(name_and_time)
            if None != time:
                time = time.group()
            name = name_and_time.split("DUE")[0].strip()
            course.add_assignment(name,date,time)

    return course

def convert_schedule_to_course_bu395(file_name,course_code,class_name,db):
    course = Course(course_code,class_name,db)
    prev_date =""
    with open(file_name,"r",encoding="utf-8") as schedule:
        for line in schedule:
            line = line.strip()
            session  = line.split("|")
            if len(session)==4:
                date = session[1]
                prev_date = date
                reading_name = session[2]
                chapter=session[3]
                course.add_reading(reading_name,date,chapter)
            elif "CASE" in line.upper():
                name = session[0]
                course.add_assignment(name,prev_date)
            elif "MIDTERM" in line.upper():
                midterm = line.split(",")
                title = midterm[0]
                date = midterm[1]
                time = midterm[2].split(';')[0]
                course.add_test(title,date,time)
    return course


def convert_schedule_to_course_bu398(file_name,course_code,class_name,db):
    course = Course(course_code,class_name,db)
    prev_date = "";
    prog_time = re.compile(TIME_PATTERN_AMPM)

    with open(file_name,"r",encoding="utf-8") as fh:
        schedule = fh.readlines()
        index = 0
        while index<len(schedule):
            session = schedule[index].strip()

            if session.startswith("(R)"):
                session = session[3:]
                chapter_pages = session.split(',')
                chapter = chapter_pages[0]
                pages = None
                if len(chapter_pages)>1:
                    pages = chapter_pages[1]
                course.add_reading(chapter,prev_date,chapter,pages)

            elif session.startswith("(D)"):
                time = prog_time.search(session)
                if None!=time:
                    time = time.group()
                    date = session[-7:-1]
                    index_of_bracket = session.find("(",2)
                    title = session[4:index_of_bracket-1]
                    course.add_assignment(title,date.strip(),time.strip())

            elif "MIDTERM" in session:
                title = "MIDTERM"
                time = prog_time.search(session)
                if None!=time:
                    time = time.group()
                    date = re.search(r"\w\w\w\s\d",session)
                    date = date.group()
                    course.add_test(title,date,time)
            else:
                line = session.split('|')
                if len(line)>=3:
                    prev_date = line[1]
            index+=1


    return course


def convert_schedule_to_course_bu415(file_name,course_code,class_name,db):
    course = Course(course_code,class_name,db)

    with open(file_name,"r",encoding="utf-8") as fh:
        for line in fh:
            day = line.strip().split("|")
            date = day[0]

            if 'TEST' in line.upper():
                name = day[1].strip()
                course.add_test(name,date,"in-class")
            elif 'MEMO' in line.upper():
                reading_memo = day[2].strip()
                mix_list = reading_memo.split("-")

                memo_name = mix_list[1]
                course.add_assignment(memo_name,date,"in-class")

                chapter = mix_list[0]
                course.add_reading(chapter,date,chapter)
            elif len(day)>=3:
                chapter = day[2].strip()
                course.add_reading(chapter,date,chapter)

    return course

def convert_schedule_to_course_bu393(file_name,course_code,class_name,db):
    course = Course(course_code,class_name,db)

    with open(file_name,"r",encoding="utf-8") as fh:
        for line in fh:
            quiz_text = line.strip().split("|")
            date = quiz_text[0]
            title = quiz_text[1]
            time = None
            if len(quiz_text)>2:
                time = quiz_text[2]
            course.add_test(title,date,time)
    return course


def replace_r(file_name):
    with open(file_name,"r+",encoding="utf-8") as fh:
        text = fh.read()
        text = text.replace("\n(R)",'|')
        fh.seek(0)
        fh.write(text)
    return


def remove_combine_every_other_line(file_name):
    '''
    This kind of works but too many inconsistencies in the file for it to be reliable
    '''
    with open(file_name,"r+",encoding="utf-8") as fh:

        lines = fh.readlines()
        new_lines = []
        i=0
        while i < len(lines)-1:
            monday_line = lines[i].strip()
            tuesday_line = lines[i+1].strip()
            new_lines.append(monday_line+'|'+tuesday_line)
            i+=2


        fh.seek(0)
        for line in new_lines:
            print(line,file=fh)
    return

def pull_up_next_line(file_name):

    with open(file_name,"r+",encoding="utf-8") as fh:

        lines = fh.readlines()
        new_lines = []
        i=0
        while i < len(lines)-1:

            match = re.match(r"^\d",lines[i])
            if match:
                line_one = lines[i].strip()
                line_two = lines[i+1].strip()
                new_lines.append(line_one+'|'+line_two)
                i+=2
            else:
                new_lines.append(lines[i])
                i+=1
        fh.seek(0)
        for line in new_lines:
            print(line,file=fh)
    return






