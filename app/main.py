from fastapi import FastAPI
from .routers import auth, students, professors, exams, classrooms

app = FastAPI()

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(professors.router)
app.include_router(exams.router)
app.include_router(classrooms.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to USV Exam Planner API"}
