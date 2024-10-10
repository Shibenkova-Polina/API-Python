from http.client import HTTPException

from fastapi import FastAPI, Depends
import os
from typing import Optional, List

from utils import json_to_dict_list, SStudent, RBStudent, add_student, SUpdateFilter, SStudentUpdate, upd_student, \
    SDeleteFilter, dell_student

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет!"}


@app.get("/students")                                   # http://127.0.0.1:8000/students?course=1   (параметр запроса)
def get_all_students(course: Optional[int] = None):
    students = json_to_dict_list()
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list

# http://127.0.0.1:8000/students/1?enrollment_year=2019&major=Психология    (параметр пути)
# @app.get("/students/{course}")
# def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018) -> List[SStudent]:
#     students = json_to_dict_list(path_to_json)
#     filtered_students = []
#     for student in students:
#         if student["course"] == course:
#             filtered_students.append(student)
#
#     if major:
#         filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]
#
#     if enrollment_year:
#         filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]
#
#     return filtered_students


@app.get("/students/{course}")
def get_all_students_course(request_body: RBStudent = Depends()) -> List[SStudent]:
    students = json_to_dict_list()
    filtered_students = []
    for student in students:
        if student["course"] == request_body.course:
            filtered_students.append(student)

    if request_body.major:
        filtered_students = [student for student in filtered_students if
                             student['major'].lower() == request_body.major.lower()]

    if request_body.enrollment_year:
        filtered_students = [student for student in filtered_students if
                             student['enrollment_year'] == request_body.enrollment_year]

    return filtered_students

# http://127.0.0.1:8000/docs    документация

#@app.get("/student", response_model=SStudent)
#def get_student_from_param_id(student_id: int):
@app.get("/student")
def get_student_from_param_id(student_id: int) -> SStudent:
    students = json_to_dict_list()
    for student in students:
        if student["student_id"] == student_id:
            return student


########################################################################################################################
@app.post("/add_student")
def add_student_handler(student: SStudent):
    student_dict = student.dict()
    check = add_student(student_dict)
    if check:
        return {"message": "Студент успешно добавлен!"}
    else:
        return {"message": "Ошибка при добавлении студента"}


########################################################################################################################
@app.put("/update_student")
def update_student_handler(filter_student: SUpdateFilter, new_data: SStudentUpdate):
    check = upd_student(filter_student.dict(), new_data.dict())
    if check:
        return {"message": "Информация о студенте успешно обновлена!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о студенте")


########################################################################################################################
@app.delete("/delete_student")
def delete_student_handler(filter_student: SDeleteFilter):
    check = dell_student(filter_student.key, filter_student.value)
    if check:
        return {"message": "Студент успешно удален!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении студента")