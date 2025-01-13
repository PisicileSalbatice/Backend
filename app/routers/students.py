from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Importăm List pentru a specifica tipul returnat
from ..database import get_db  # Importăm funcția get_db pentru a obține sesiunea de DB
from ..crud import get_student_exams
from ..routers.auth import authenticate_user, get_current_user_student
from app import crud, schemas
from ..schemas import Exam  # Importăm schema Exam pentru a specifica tipul de răspuns
from app import models
from app.schemas import UserDetails
from sqlalchemy.orm import joinedload
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter()





@router.get("/students", response_model=List[schemas.Student])
def get_all_students(db: Session = Depends(get_db)):
    """
    Returnează toți studenții din baza de date.
    """
    students = db.query(models.Student).all()
    return [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "year_of_study": student.year_of_study,
            "name": f"{student.first_name} {student.last_name}",
            "role": "student",  # Poți adapta logica pentru a include rolul corect
        }
        for student in students
    ]






