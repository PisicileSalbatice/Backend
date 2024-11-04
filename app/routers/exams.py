from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    prefix="/exams",
    tags=["exams"]
)

@router.get("/", response_model=list[schemas.ExamCreate])
def get_exams(db: Session = Depends(database.get_db)):
    return db.query(models.Exam).all()

