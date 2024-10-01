from fastapi import FastAPI
from utils import json_to_dict_list
import os
from typing import Optional

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))  # C:\Users\Полина\Desktop\Проекты\API\app

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)  # C:\Users\Полина\Desktop\Проекты\API

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'students.json')  # C:\Users\Полина\Desktop\Проекты\API\students.json

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Привет!"}

# @app.get("/students")                                 # http://127.0.0.1:8000/students
# def get_all_students():
#     return json_to_dict_list(path_to_json)
#
# @app.get("/students/{course}")                        # http://127.0.0.1:8000/students/2      (параметр пути)
# def get_all_students_course(course: int):
#     students = json_to_dict_list(path_to_json)
#     return_list = []
#
#     for student in students:
#         if student["course"] == course:
#             return_list.append(student)
#     return return_list

# вместо предыдущих двух:
@app.get("/students")                                   # http://127.0.0.1:8000/students?course=1   (параметр запроса)
def get_all_students(course: Optional[int] = None):
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list

@app.get("/students/{course}")      # http://127.0.0.1:8000/students/1?enrollment_year=2019&major=Психология
def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    for student in students:
        if student["course"] == course:
            filtered_students.append(student)

    if major:
        filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]

    if enrollment_year:
        filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]

    return filtered_students

# http://127.0.0.1:8000/docs    документация