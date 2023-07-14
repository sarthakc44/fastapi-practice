from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John"
        ,"age": 17
        ,"year": "year 12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel): # in above all 3 are required
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/")
# the endpoint goes in the ()
# / means homepage
def index():
    return {"name":"First Data","age":2}

@app.get("/get-student/{students_id}") #path
def get_student(students_id: int = Path(description = "The ID of the student you want to view.", gt=0, lt=3)):
    return students[students_id]
# description: will show in /docs
# gt: grater than 
# lt, ge, le

@app.get("/get-by-name") #query search
def get_student(*, name: Optional[str] = None, testvar:int): 
    for student_id in students: 
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}
# Optional[] = none makes it optional to enter
# default [optional] argument should be after non-default [required] (name after test)
# but to overcome that, put * in beginning

@app.get("/get-by-nameandid/{students_id}") #query + path
def get_student_detail(*,student_id:int,  name: Optional[str] = None, test:int): 
    for student_id in students: 
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return{"Error": "Student exists"}

    students[student_id] = student
    return students[student_id]
# but this only stores the new data in memory, will be gone on refreshing


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return{"Error": "Student does not exist"}
    
    #students[student_id] = student # this will make all other parameters None, which were optional and not entered

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year    
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return{"Error": "Student does not exist"}
    del students[student_id]
    return {"Message":"Student deleted!"}

# to run in cmd
#uvicorn myfastapi:app --reload