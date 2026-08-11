from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Student Details Management API")

In-Memory Database
students_db = {
    1: {"name": "Aarav", "age": 21, "course": "Data Science"},
    2: {"name": "Priya", "age": 22, "course": "Web Development"},
    3: {"name": "Rohan", "age": 20, "course": "AI & ML"},
}


Data Validation Model
class Student(BaseModel):
    name: str
    age: int
    course: str


==========================================
READ (GET) - View All or Filter by Course
==========================================
@app.get("/students/")
def get_students(course: str = None):
    if course:
        filtered = {
            s_id: s
            for s_id, s in students_db.items()
            if s["course"].lower() == course.lower()
        }
        return filtered

    return students_db