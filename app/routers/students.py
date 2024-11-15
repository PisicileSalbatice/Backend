from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Importăm List pentru a specifica tipul returnat
from ..database import get_db  # Importăm funcția get_db pentru a obține sesiunea de DB
from ..crud import get_student_exams
from ..routers.auth import authenticate_user
from app import crud, schemas
from ..schemas import Exam  # Importăm schema Exam pentru a specifica tipul de răspuns

router = APIRouter()


@router.get("/students/exams/", response_model=List[Exam])
def get_exams_for_student(student_id: str, db: Session = Depends(get_db)):
    return get_student_exams(db=db, student_id=student_id)

@router.get("/students/exams", response_model=List[schemas.Exam])
def read_student_exams(
    email: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    current_user = authenticate_user(email, password, db)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return crud.get_student_exams(db=db, student_id=current_user.id)