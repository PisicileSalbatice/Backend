from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Importăm List pentru a specifica tipul returnat
from ..database import get_db  # Importăm funcția get_db pentru a obține sesiunea de DB
from ..crud import get_student_exams
from ..routers.auth import authenticate_user, get_current_user_student
from app import crud, schemas
from ..schemas import Exam  # Importăm schema Exam pentru a specifica tipul de răspuns
from app import models
router = APIRouter()


@router.get("/students/exams/", response_model=List[Exam])
def get_exams_for_student(student_id: str, db: Session = Depends(get_db)):
    return get_student_exams(db=db, student_id=student_id)

@router.get("/students/exams", response_model=List[schemas.ExamRequest])
def read_student_exams(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Obține studentul asociat utilizatorului curent
    current_student = get_current_user_student(email, password, db)
    print(f"Authenticated student ID: {current_student.id}")

    # Caută examenele asociate studentului în baza de date
    student_exams = db.query(models.ExamRequest).filter(
        models.ExamRequest.student_id == current_student.id
    ).all()

    print(f"Query result: {student_exams}")
    return student_exams




