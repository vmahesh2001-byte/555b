from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Student Details Management API")

# 1. In-Memory Database
students_db = {
    1: {"name": "Aarav", "age": 21, "course": "Data Science"},
    2: {"name": "Priya", "age": 22, "course": "Web Development"},
    3: {"name": "Rohan", "age": 20, "course": "AI & ML"},
}


# 2. Data Validation Model
class Student(BaseModel):
    name: str
    age: int
    course: str


# ==========================================
# 1. READ (GET) - View All or Filter by Course
# ==========================================


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


# READ SINGLE STUDENT BY ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students_db:
        return {"error": "Student not found"}
    return students_db[student_id]


# ==========================================
# 2. CREATE (POST) - Add New Student
# ==========================================


@app.post("/students/")
def create_student(student: Student):
    new_id = max(students_db.keys(), default=0) + 1
    students_db[new_id] = student.dict()
    return {
        "message": "Student created successfully",
        "student_id": new_id,
        "data": students_db[new_id],
    }


# ==========================================
# 3. UPDATE (PUT) - Update Existing Student
# ==========================================


@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    if student_id not in students_db:
        return {"error": "Student not found"}

    students_db[student_id] = updated_student.dict()
    return {
        "message": "Student updated successfully",
        "data": students_db[student_id],
    }


# ==========================================
# 4. DELETE (DELETE) - Remove Student
# ==========================================


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        return {"error": "Student not found"}

    deleted = students_db.pop(student_id)
    return {"message": "Student deleted successfully", "deleted_data": deleted}
