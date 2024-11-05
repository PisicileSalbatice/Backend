from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/exams", tags=["exams"])


@router.get("/", response_model=list[schemas.ExamCreate])
def get_exams(db: Session = Depends(database.get_db)):
    return db.query(models.Exam).all()

@router.post("/exams/", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    return crud.create_exam(db=db, exam=exam)

@router.get("/exams/", response_model=List[schemas.Exam])
def read_exams(db: Session = Depends(get_db)):
    exams = crud.get_exams(db=db)
    return exams