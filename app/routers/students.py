from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  # Importăm List pentru a specifica tipul returnat
from ..database import get_db  # Importăm funcția get_db pentru a obține sesiunea de DB
from ..crud import get_student_exams
from ..schemas import Exam  # Importăm schema Exam pentru a specifica tipul de răspuns

router = APIRouter()


@router.get("/students/exams/", response_model=List[Exam])
def get_exams_for_student(student_id: str, db: Session = Depends(get_db)):
    return get_student_exams(db=db, student_id=student_id)
