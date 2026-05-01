from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    
    }
}

@app.get("/")
async def root():
    return {"name": "Hello World"}

#127.0.0.1/docs 
#then got to the 'try it out' -> 'excuter'

#http://127.0.0.1:8000/get-student/1
#can get directly via url or else by the docs by entering the id

@app.get("/get-student/{student_id}")
#gt-> greater than , lt-> less than 
def get_student(student_id: int= Path(description="Need Id of the student", gt=0, lt=3)):
    return students[student_id] 

@app.get('/get-by-name/{student_id}')
def get_student(*,student_id: int , name: Optional[str] = None, ):#test: int #def get_student(*,student_id: int , name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]['name'] == name :#or students[student_id] == student_id:
            return students[student_id]
    # raise HTTPException(status_code=404, detail="Student not found")
    return {"Data": "Not found"}

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"} #or else raise HTTPException(status_code=400, detail="Student already exists")
    students[student_id] = student#.dict()
    return students[student_id]

@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    students[student_id] = student
    return students[student_id]

@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted successfully"}

